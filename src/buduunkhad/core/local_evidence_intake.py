"""Immutable intake of existing local GIS layers into evidence authority.

The intake copies source bytes before they become executable evidence. GeoPackages retain their
exact bytes; shapefile bundles are preserved together and converted to a single-layer GeoPackage
so downstream phases consume one stable, CRS-bearing artifact.
"""

from __future__ import annotations

import os
import shutil
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Literal, Self

import fiona
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)
from pyproj import CRS
from pyproj.exceptions import CRSError

from buduunkhad.ai.fingerprint import sha256_value
from buduunkhad.core.evidence_manifest import (
    EvidenceAuthorityResolver,
    EvidenceExecutionMode,
    EvidenceLifecycleState,
    EvidenceManifest,
    EvidenceManifestError,
    EvidenceOrigin,
    EvidenceRecord,
    EvidenceRole,
    EvidenceSourceKind,
    PhaseId,
)
from buduunkhad.core.run_artifacts import (
    ArtifactSealError,
    canonical_relative_path,
    has_symlink_component,
    require_regular_file_under,
    sha256_file,
)
from buduunkhad.core.run_storage import generate_run_id

LOCAL_INTAKE_FORMAT_VERSION = "1.0.0"
LOCAL_INTAKE_FILENAME = "intake_authority.json"
_SHAPEFILE_COMPONENTS = frozenset(
    {".shp", ".shx", ".dbf", ".prj", ".cpg", ".qix", ".sbn", ".sbx", ".shp.xml"}
)
_REQUIRED_SHAPEFILE_COMPONENTS = frozenset({".shp", ".shx", ".dbf", ".prj"})

Sha256 = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
NonEmpty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, revalidate_instances="always")

    @classmethod
    def model_construct(
        cls,
        _fields_set: set[str] | None = None,
        **values: object,
    ) -> Self:
        del _fields_set, values
        raise TypeError("model_construct is unsupported; use validated construction")


class LocalEvidenceSourceFile(_StrictModel):
    relative_path: str
    sha256: Sha256
    size_bytes: int = Field(ge=0)

    _path_is_portable = field_validator("relative_path")(canonical_relative_path)


class _LocalEvidenceIntakeIdentity(_StrictModel):
    format_version: Literal["1.0.0"] = "1.0.0"
    intake_id: NonEmpty
    created_at: datetime
    imported_by: NonEmpty
    import_reason: NonEmpty
    source_format: Literal["gpkg", "shapefile"]
    source_layer: NonEmpty
    source_files: tuple[LocalEvidenceSourceFile, ...] = Field(min_length=1)
    authority_relative_path: str
    artifact_relative_path: str
    artifact_sha256: Sha256
    artifact_size_bytes: int = Field(ge=0)
    artifact_layer: NonEmpty
    conversion: Literal["exact-copy", "shapefile-to-gpkg-v1"]
    limitations: tuple[NonEmpty, ...] = ()

    _authority_path_is_portable = field_validator("authority_relative_path")(
        canonical_relative_path
    )
    _artifact_path_is_portable = field_validator("artifact_relative_path")(canonical_relative_path)

    @field_validator("created_at")
    @classmethod
    def _aware_created_at(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("local evidence intake timestamp must be timezone-aware")
        return value

    @model_validator(mode="after")
    def _consistent_paths(self) -> _LocalEvidenceIntakeIdentity:
        prefix = f"intakes/{self.intake_id}/"
        if not self.authority_relative_path.startswith(prefix):
            raise ValueError("local evidence authority path does not match its intake identity")
        if not self.artifact_relative_path.startswith(prefix):
            raise ValueError("local evidence artifact path does not match its intake identity")
        paths = tuple(item.relative_path for item in self.source_files)
        if paths != tuple(sorted(paths)) or len(paths) != len(set(paths)):
            raise ValueError("local evidence source files must be unique and sorted")
        if any(not path.startswith(prefix) for path in paths):
            raise ValueError("local evidence source path does not match its intake identity")
        expected_conversion = (
            "exact-copy" if self.source_format == "gpkg" else "shapefile-to-gpkg-v1"
        )
        if self.conversion != expected_conversion:
            raise ValueError("local evidence conversion does not match its source format")
        return self


class LocalEvidenceIntakeAuthority(_LocalEvidenceIntakeIdentity):
    authority_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> LocalEvidenceIntakeAuthority:
        identity = _LocalEvidenceIntakeIdentity.model_validate(
            self.model_dump(mode="python", exclude={"authority_id"})
        )
        if self.authority_id != sha256_value(identity):
            raise ValueError("local evidence intake identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> LocalEvidenceIntakeAuthority:
        identity = _LocalEvidenceIntakeIdentity.model_validate(values)
        return cls(**identity.model_dump(mode="python"), authority_id=sha256_value(identity))


def register_local_evidence(
    *,
    runs_root: Path,
    evidence_root: Path,
    target_epsg: int,
    source_path: Path,
    source_layer: str | None,
    evidence_role: EvidenceRole,
    origin: EvidenceOrigin,
    eligible_phases: tuple[PhaseId, ...],
    eligible_modes: tuple[EvidenceExecutionMode, ...],
    target_layer_name: str | None = None,
    evidence_id: str | None = None,
    limitations: tuple[str, ...] = (),
    registered_by: str,
    registration_reason: str,
) -> EvidenceManifest:
    """Copy one local GIS source into immutable authority and register its exact layer."""

    source = Path(source_path).absolute()
    if has_symlink_component(source):
        raise EvidenceManifestError(f"local evidence source must not use a symlink: {source}")
    try:
        source = require_regular_file_under(
            source.parent, source, description="local evidence source"
        )
    except ArtifactSealError as exc:
        raise EvidenceManifestError(str(exc)) from exc
    suffix = source.suffix.casefold()
    if suffix not in {".gpkg", ".shp"}:
        raise EvidenceManifestError("local evidence intake supports only GeoPackage or shapefile")
    root = Path(evidence_root).absolute()
    if has_symlink_component(root):
        raise EvidenceManifestError(f"evidence root must not use a symlink: {root}")
    source_resolved = source.resolve()
    root_resolved = root.resolve(strict=False)
    if source_resolved == root_resolved or root_resolved in source_resolved.parents:
        raise EvidenceManifestError("local evidence source must be outside the evidence root")

    layer = _select_layer(source, source_layer)
    intake_id = generate_run_id()
    package_relative = Path("intakes") / intake_id
    destination = root / package_relative
    temporary = root / "intakes" / f".{intake_id}.{uuid.uuid4().hex}.tmp"
    authority_relative = (package_relative / LOCAL_INTAKE_FILENAME).as_posix()
    artifact_relative = (package_relative / "artifact" / "evidence.gpkg").as_posix()
    source_format: Literal["gpkg", "shapefile"] = "gpkg" if suffix == ".gpkg" else "shapefile"
    conversion: Literal["exact-copy", "shapefile-to-gpkg-v1"] = (
        "exact-copy" if source_format == "gpkg" else "shapefile-to-gpkg-v1"
    )
    artifact_layer = layer if source_format == "gpkg" else "evidence"
    identity = (
        evidence_id or f"EV-{sha256_value((intake_id, artifact_relative, artifact_layer))[:24]}"
    )
    # Invalid role, phase, and target claims must fail before an intake writes any bytes.
    EvidenceRecord(
        evidence_id=identity,
        source_kind=EvidenceSourceKind.LOCAL_INTAKE,
        source_run_id=intake_id,
        source_authority_path=authority_relative,
        source_authority_sha256="0" * 64,
        artifact_path=artifact_relative,
        artifact_sha256="0" * 64,
        artifact_size_bytes=0,
        layer_name=artifact_layer,
        target_layer_name=target_layer_name,
        evidence_role=evidence_role,
        origin=origin,
        lifecycle_state=EvidenceLifecycleState.SEALED_SUPPORT_EVIDENCE,
        eligible_phases=eligible_phases,
        eligible_modes=eligible_modes,
        limitations=limitations,
    )
    root.mkdir(parents=True, exist_ok=True)
    temporary.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise EvidenceManifestError("local evidence intake identity already exists")
    try:
        (temporary / "source").mkdir(parents=True)
        (temporary / "artifact").mkdir()
        source_files = _copy_source_bundle(source, temporary, package_relative)
        artifact = temporary / "artifact" / "evidence.gpkg"
        if source_format == "gpkg":
            shutil.copyfile(source, artifact)
        else:
            _convert_shapefile(source, artifact, artifact_layer)
        _verify_layer(artifact, artifact_layer)
        authority = LocalEvidenceIntakeAuthority.create(
            intake_id=intake_id,
            created_at=datetime.now(UTC),
            imported_by=registered_by,
            import_reason=registration_reason,
            source_format=source_format,
            source_layer=layer,
            source_files=source_files,
            authority_relative_path=authority_relative,
            artifact_relative_path=artifact_relative,
            artifact_sha256=sha256_file(artifact),
            artifact_size_bytes=artifact.stat().st_size,
            artifact_layer=artifact_layer,
            conversion=conversion,
            limitations=limitations,
        )
        (temporary / LOCAL_INTAKE_FILENAME).write_text(
            authority.model_dump_json(indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        os.replace(temporary, destination)
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise

    authority_path = destination / LOCAL_INTAKE_FILENAME
    artifact_path = destination / "artifact" / "evidence.gpkg"
    record = EvidenceRecord(
        evidence_id=identity,
        source_kind=EvidenceSourceKind.LOCAL_INTAKE,
        source_run_id=intake_id,
        source_authority_path=authority_relative,
        source_authority_sha256=sha256_file(authority_path),
        artifact_path=artifact_relative,
        artifact_sha256=sha256_file(artifact_path),
        artifact_size_bytes=artifact_path.stat().st_size,
        layer_name=authority.artifact_layer,
        target_layer_name=target_layer_name,
        evidence_role=evidence_role,
        origin=origin,
        lifecycle_state=EvidenceLifecycleState.SEALED_SUPPORT_EVIDENCE,
        eligible_phases=eligible_phases,
        eligible_modes=eligible_modes,
        limitations=limitations,
    )
    manifest = EvidenceManifest.create(records=(record,))
    EvidenceAuthorityResolver(
        runs_root=runs_root,
        evidence_root=root,
        target_epsg=target_epsg,
    ).write(
        manifest,
        registered_by=registered_by,
        registration_reason=registration_reason,
    )
    return manifest


def _select_layer(source: Path, requested: str | None) -> str:
    try:
        layers = list(fiona.listlayers(source))
    except (OSError, ValueError) as exc:
        raise EvidenceManifestError("local evidence source cannot be opened") from exc
    if requested is None:
        if len(layers) != 1:
            raise EvidenceManifestError("multi-layer local evidence requires an exact --layer")
        return layers[0]
    if layers.count(requested) != 1:
        raise EvidenceManifestError("local evidence layer must exist exactly once")
    return requested


def _copy_source_bundle(
    source: Path,
    temporary: Path,
    package_relative: Path,
) -> tuple[LocalEvidenceSourceFile, ...]:
    if source.suffix.casefold() == ".gpkg":
        components = (source,)
    else:
        components = tuple(
            sorted(
                (
                    item
                    for item in source.parent.iterdir()
                    if item.is_file()
                    and item.name.casefold().startswith(source.stem.casefold() + ".")
                    and _component_suffix(item.name, source.stem) in _SHAPEFILE_COMPONENTS
                ),
                key=lambda item: item.name.casefold(),
            )
        )
        found = {_component_suffix(item.name, source.stem) for item in components}
        missing = sorted(_REQUIRED_SHAPEFILE_COMPONENTS - found)
        if missing:
            raise EvidenceManifestError(
                f"shapefile evidence bundle is incomplete; missing {', '.join(missing)}"
            )
    records: list[LocalEvidenceSourceFile] = []
    for component in components:
        if has_symlink_component(component):
            raise EvidenceManifestError(
                f"local evidence source bundle must not use symlinks: {component}"
            )
        target = temporary / "source" / component.name
        shutil.copyfile(component, target)
        relative = (package_relative / "source" / component.name).as_posix()
        records.append(
            LocalEvidenceSourceFile(
                relative_path=relative,
                sha256=sha256_file(target),
                size_bytes=target.stat().st_size,
            )
        )
    return tuple(sorted(records, key=lambda item: item.relative_path))


def _component_suffix(filename: str, stem: str) -> str:
    return filename[len(stem) :].casefold()


def _convert_shapefile(source: Path, artifact: Path, layer: str) -> None:
    import geopandas as gpd

    try:
        gdf = gpd.read_file(source)
        if gdf.empty or gdf.crs is None:
            raise EvidenceManifestError("local evidence layer is empty or lacks CRS evidence")
        gdf.to_file(artifact, layer=layer, driver="GPKG")
    except EvidenceManifestError:
        raise
    except Exception as exc:
        raise EvidenceManifestError(
            "shapefile evidence could not be converted to GeoPackage"
        ) from exc


def _verify_layer(artifact: Path, layer: str) -> None:
    try:
        layers = list(fiona.listlayers(artifact))
        if layers.count(layer) != 1:
            raise EvidenceManifestError("local evidence artifact layer must exist exactly once")
        with fiona.open(artifact, layer=layer) as collection:
            if len(collection) == 0:
                raise EvidenceManifestError("local evidence artifact layer must not be empty")
            CRS.from_user_input(collection.crs_wkt or collection.crs)
    except EvidenceManifestError:
        raise
    except (CRSError, OSError, TypeError, ValueError) as exc:
        raise EvidenceManifestError(
            "local evidence artifact is unreadable or lacks CRS evidence"
        ) from exc
