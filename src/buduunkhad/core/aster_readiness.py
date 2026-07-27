"""Exact-source technical readiness evidence for the Phase 02 ASTER HDF workflow."""

from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Iterable
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

from buduunkhad.ai.fingerprint import sha256_value
from buduunkhad.core.aster import BAND_SUBDATASETS
from buduunkhad.core.run_artifacts import (
    ArtifactSealError,
    canonical_relative_path,
    require_regular_file_under,
    sha256_file,
)

ASTER_READINESS_FORMAT_VERSION = "1.0.0"
ASTER_READINESS_COMPONENT = "buduunkhad.phase02.aster-readiness-v1"

Sha256 = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
NonEmpty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class AsterReadinessError(RuntimeError):
    """An ASTER readiness record or one of its bound files cannot be trusted."""


class AsterReadinessStatus(StrEnum):
    READY = "ready"
    UNAVAILABLE = "unavailable"


class _StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        revalidate_instances="always",
        allow_inf_nan=False,
    )

    @classmethod
    def model_construct(
        cls,
        _fields_set: set[str] | None = None,
        **values: object,
    ) -> Self:
        del _fields_set, values
        raise TypeError("model_construct is unsupported; use validated construction")


class AsterFileIdentity(_StrictModel):
    path: str
    sha256: Sha256
    size_bytes: int = Field(ge=0)

    @model_validator(mode="after")
    def _portable_path(self) -> AsterFileIdentity:
        canonical_relative_path(self.path)
        return self


class AsterSubdatasetInspection(_StrictModel):
    """Portable inspection of one HDF subdataset; source paths are never persisted."""

    logical_name: NonEmpty
    description: NonEmpty
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    band_types: tuple[NonEmpty, ...] = Field(min_length=1)
    geolocation_evidence: tuple[NonEmpty, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _ordered_values(self) -> AsterSubdatasetInspection:
        if tuple(sorted(set(self.band_types))) != self.band_types:
            raise ValueError("ASTER band types must be unique and ordered")
        if tuple(sorted(set(self.geolocation_evidence))) != self.geolocation_evidence:
            raise ValueError("ASTER geolocation evidence must be unique and ordered")
        return self


class AsterRasterValidation(_StrictModel):
    artifact: AsterFileIdentity
    epsg: int = Field(gt=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    band_count: int = Field(gt=0)
    nodata_values: tuple[float | None, ...]
    finite_pixel_count: int = Field(ge=0)

    @model_validator(mode="after")
    def _band_metadata_matches(self) -> AsterRasterValidation:
        if len(self.nodata_values) != self.band_count:
            raise ValueError("ASTER output nodata values must match its band count")
        return self


class _AsterReadinessIdentity(_StrictModel):
    format_version: Literal["1.0.0"] = ASTER_READINESS_FORMAT_VERSION
    source_run_id: NonEmpty
    processing_run_id: NonEmpty
    source_input_no: Literal[73] = 73
    source: AsterFileIdentity
    target_epsg: int = Field(gt=0)
    gdal_version: NonEmpty | None = None
    source_opened: bool
    subdatasets: tuple[AsterSubdatasetInspection, ...] = ()
    required_logical_subdatasets: tuple[NonEmpty, ...]
    required_subdatasets_present: bool
    geolocation_evidence_complete: bool
    reprojection_test_passed: bool
    outputs: tuple[AsterRasterValidation, ...] = ()
    status: AsterReadinessStatus
    findings: tuple[NonEmpty, ...] = Field(min_length=1)
    limitations: tuple[NonEmpty, ...] = Field(min_length=1)
    validator_component: Literal["buduunkhad.phase02.aster-readiness-v1"] = (
        ASTER_READINESS_COMPONENT
    )

    @model_validator(mode="after")
    def _coherent_status(self) -> _AsterReadinessIdentity:
        logical_names = tuple(item.logical_name for item in self.subdatasets)
        if tuple(sorted(set(logical_names))) != logical_names:
            raise ValueError("ASTER subdataset inspections must be unique and ordered")
        if tuple(sorted(set(self.required_logical_subdatasets))) != (
            self.required_logical_subdatasets
        ):
            raise ValueError("ASTER required subdataset identities must be unique and ordered")
        present = set(self.required_logical_subdatasets) <= set(logical_names)
        if self.required_subdatasets_present != present:
            raise ValueError("ASTER required-subdataset result is inconsistent")
        geolocation_complete = bool(self.subdatasets) and all(
            "none" not in item.geolocation_evidence for item in self.subdatasets
        )
        if self.geolocation_evidence_complete != geolocation_complete:
            raise ValueError("ASTER geolocation result is inconsistent")
        output_ready = bool(self.outputs) and all(
            item.epsg == self.target_epsg and item.finite_pixel_count > 0 for item in self.outputs
        )
        if self.reprojection_test_passed != output_ready:
            raise ValueError("ASTER reprojection result is inconsistent")
        ready = all(
            (
                self.source_opened,
                self.required_subdatasets_present,
                self.geolocation_evidence_complete,
                self.reprojection_test_passed,
            )
        )
        expected = AsterReadinessStatus.READY if ready else AsterReadinessStatus.UNAVAILABLE
        if self.status is not expected:
            raise ValueError("ASTER readiness status does not match its validation results")
        if tuple(sorted(set(self.findings))) != self.findings:
            raise ValueError("ASTER readiness findings must be unique and ordered")
        if tuple(sorted(set(self.limitations))) != self.limitations:
            raise ValueError("ASTER readiness limitations must be unique and ordered")
        return self


class AsterReadinessRecord(_AsterReadinessIdentity):
    readiness_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> AsterReadinessRecord:
        identity = _AsterReadinessIdentity.model_validate(
            self.model_dump(mode="python", exclude={"readiness_id"})
        )
        if self.readiness_id != sha256_value(identity):
            raise ValueError("ASTER readiness identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> AsterReadinessRecord:
        identity = _AsterReadinessIdentity.model_validate(values)
        return cls(
            **identity.model_dump(mode="python"),
            readiness_id=sha256_value(identity),
        )


def validate_aster_readiness(
    *,
    source_run_id: str,
    processing_run_id: str,
    source_phase_root: Path,
    source_path: Path,
    phase_root: Path,
    target_epsg: int,
    gdalwarp: Path | None,
    output_rasters: Iterable[Path] = (),
    processing_finding: str | None = None,
) -> AsterReadinessRecord:
    """Inspect one exact HDF and its produced rasters without changing either."""

    source = _file_identity(source_phase_root, source_path)
    required = tuple(
        sorted(f"{swath}:{subdataset}" for swath, subdataset in BAND_SUBDATASETS.values())
    )
    inspections: tuple[AsterSubdatasetInspection, ...] = ()
    gdal_version: str | None = None
    source_opened = False
    findings: list[str] = []

    gdalinfo = _gdalinfo_path(gdalwarp)
    if gdalinfo is None:
        findings.append("HDF4-capable gdalinfo is unavailable.")
    else:
        try:
            gdal_version = _gdal_version(gdalinfo)
            inspections = _inspect_hdf(gdalinfo, source_path)
            source_opened = True
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            findings.append(f"HDF inspection failed: {type(exc).__name__}: {str(exc)[:240]}")

    outputs: list[AsterRasterValidation] = []
    for output in sorted((Path(item) for item in output_rasters), key=lambda item: item.as_posix()):
        try:
            outputs.append(_validate_output(phase_root, output))
        except (OSError, ValueError, ArtifactSealError) as exc:
            findings.append(
                f"Output validation failed for {output.name}: {type(exc).__name__}: {str(exc)[:200]}"
            )

    logical_names = {item.logical_name for item in inspections}
    required_present = set(required) <= logical_names
    geolocation_complete = bool(inspections) and all(
        "none" not in item.geolocation_evidence for item in inspections
    )
    reprojection_passed = bool(outputs) and all(
        item.epsg == target_epsg and item.finite_pixel_count > 0 for item in outputs
    )
    if processing_finding:
        findings.append(processing_finding)
    if source_opened:
        findings.append(f"Inspected {len(inspections)} HDF subdataset(s).")
    if not required_present:
        missing = sorted(set(required) - logical_names)
        findings.append(f"Required ASTER subdatasets missing: {', '.join(missing) or 'all'}.")
    if not geolocation_complete:
        findings.append("One or more ASTER subdatasets lack geolocation or CRS evidence.")
    if not reprojection_passed:
        findings.append("No complete target-CRS raster validation set was produced.")
    status = (
        AsterReadinessStatus.READY
        if source_opened and required_present and geolocation_complete and reprojection_passed
        else AsterReadinessStatus.UNAVAILABLE
    )
    if status is AsterReadinessStatus.READY:
        findings.append("Exact-source ASTER technical readiness checks passed.")

    return AsterReadinessRecord.create(
        source_run_id=source_run_id,
        processing_run_id=processing_run_id,
        source=source,
        target_epsg=target_epsg,
        gdal_version=gdal_version,
        source_opened=source_opened,
        subdatasets=inspections,
        required_logical_subdatasets=required,
        required_subdatasets_present=required_present,
        geolocation_evidence_complete=geolocation_complete,
        reprojection_test_passed=reprojection_passed,
        outputs=tuple(sorted(outputs, key=lambda item: item.artifact.path)),
        status=status,
        findings=tuple(sorted(set(findings))),
        limitations=tuple(
            sorted(
                {
                    "Technical readiness does not establish geological interpretation or mineralization.",
                    "Project-geologist acceptance remains separate from deterministic HDF validation.",
                }
            )
        ),
    )


def write_aster_readiness_record(record: AsterReadinessRecord, path: Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(record.model_dump_json(indent=2) + "\n", encoding="utf-8", newline="\n")
    return target


def load_aster_readiness_record(path: Path) -> AsterReadinessRecord:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        return AsterReadinessRecord.model_validate(data)
    except (OSError, UnicodeError, ValueError) as exc:
        raise AsterReadinessError("ASTER readiness record is invalid") from exc


def verify_aster_readiness_files(
    record: AsterReadinessRecord,
    *,
    source_phase_root: Path,
    phase_root: Path,
) -> None:
    try:
        _verify_file_identity(source_phase_root, record.source)
        for output in record.outputs:
            _verify_file_identity(phase_root, output.artifact)
    except (ArtifactSealError, OSError) as exc:
        raise AsterReadinessError("ASTER readiness file identity is invalid") from exc


def _gdalinfo_path(gdalwarp: Path | None) -> Path | None:
    if gdalwarp is None:
        return None
    suffix = ".exe" if Path(gdalwarp).suffix.casefold() == ".exe" else ""
    candidate = Path(gdalwarp).with_name(f"gdalinfo{suffix}")
    return candidate if candidate.is_file() else None


def _gdal_version(gdalinfo: Path) -> str:
    result = subprocess.run(
        [str(gdalinfo), "--version"],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    value = (result.stdout or result.stderr).strip()
    if not value:
        raise ValueError("gdalinfo returned an empty version")
    return value[:256]


def _inspect_hdf(gdalinfo: Path, source: Path) -> tuple[AsterSubdatasetInspection, ...]:
    container = _gdalinfo_json(gdalinfo, str(source))
    metadata = container.get("metadata", {})
    subdataset_metadata = metadata.get("SUBDATASETS", {}) if isinstance(metadata, dict) else {}
    names = [
        str(value)
        for key, value in sorted(subdataset_metadata.items())
        if key.startswith("SUBDATASET_") and key.endswith("_NAME")
    ]
    if not names:
        raise ValueError("gdalinfo reported no HDF subdatasets")
    inspections = [_inspect_subdataset(gdalinfo, name) for name in names]
    return tuple(sorted(inspections, key=lambda item: item.logical_name))


def _inspect_subdataset(gdalinfo: Path, name: str) -> AsterSubdatasetInspection:
    data = _gdalinfo_json(gdalinfo, name)
    size = data.get("size")
    bands = data.get("bands")
    if (
        not isinstance(size, list)
        or len(size) != 2
        or not all(isinstance(value, int) and value > 0 for value in size)
        or not isinstance(bands, list)
        or not bands
    ):
        raise ValueError("ASTER subdataset dimensions or bands are invalid")
    types = tuple(sorted({str(item.get("type", "")).strip() for item in bands if item.get("type")}))
    if not types:
        raise ValueError("ASTER subdataset has no band data type")
    evidence: set[str] = set()
    coordinate_system = data.get("coordinateSystem")
    if isinstance(coordinate_system, dict) and coordinate_system:
        evidence.add("coordinate-system")
    if data.get("geoTransform"):
        evidence.add("geotransform")
    if data.get("gcps"):
        evidence.add("gcps")
    metadata = data.get("metadata")
    if isinstance(metadata, dict) and any(
        str(key).casefold() in {"geolocation", "rpc"} for key in metadata
    ):
        evidence.add("geolocation-metadata")
    if not evidence:
        evidence.add("none")
    return AsterSubdatasetInspection(
        logical_name=_logical_subdataset_name(name),
        description=_portable_subdataset_name(str(data.get("description") or name)),
        width=size[0],
        height=size[1],
        band_types=types,
        geolocation_evidence=tuple(sorted(evidence)),
    )


def _gdalinfo_json(gdalinfo: Path, dataset: str) -> dict[str, Any]:
    result = subprocess.run(
        [str(gdalinfo), "-json", dataset],
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    value = json.loads(result.stdout, object_pairs_hook=_unique_object)
    if not isinstance(value, dict):
        raise ValueError("gdalinfo JSON root is invalid")
    return value


def _logical_subdataset_name(value: str) -> str:
    match = re.search(r":([^:\"]+):([^:\"]+)$", value)
    if match is None:
        raise ValueError("ASTER subdataset name has no portable swath identity")
    return f"{match.group(1)}:{match.group(2)}"


def _portable_subdataset_name(value: str) -> str:
    return re.sub(r'"[^"]+"', '"<source>"', value)


def _validate_output(root: Path, path: Path) -> AsterRasterValidation:
    import numpy as np
    import rasterio

    artifact = _file_identity(root, path)
    with rasterio.open(Path(path)) as dataset:
        epsg = dataset.crs.to_epsg() if dataset.crs is not None else None
        if epsg is None:
            raise ValueError("output CRS cannot be expressed as EPSG")
        finite_count = 0
        for band in dataset.read(masked=True):
            values = band.compressed()
            finite_count += int(np.isfinite(values).sum())
        return AsterRasterValidation(
            artifact=artifact,
            epsg=epsg,
            width=dataset.width,
            height=dataset.height,
            band_count=dataset.count,
            nodata_values=tuple(dataset.nodatavals),
            finite_pixel_count=finite_count,
        )


def _file_identity(root: Path, path: Path) -> AsterFileIdentity:
    safe = require_regular_file_under(root, path, description="ASTER readiness artifact")
    relative = safe.relative_to(Path(root).absolute().resolve()).as_posix()
    return AsterFileIdentity(
        path=relative,
        sha256=sha256_file(safe),
        size_bytes=safe.stat().st_size,
    )


def _verify_file_identity(root: Path, identity: AsterFileIdentity) -> None:
    safe = require_regular_file_under(
        root,
        Path(root) / identity.path,
        description="ASTER readiness artifact",
    )
    if safe.stat().st_size != identity.size_bytes or sha256_file(safe) != identity.sha256:
        raise AsterReadinessError(f"ASTER readiness artifact bytes changed: {identity.path}")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result
