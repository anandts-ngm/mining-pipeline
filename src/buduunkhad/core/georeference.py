"""Measured georeferencing evidence, separate human reviews, and exact acceptance resolution."""

from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from buduunkhad.ai.fingerprint import sha256_value
from buduunkhad.core.run_artifacts import (
    ArtifactSealError,
    canonical_relative_path,
    require_regular_file_under,
    sha256_file,
)

GEOREFERENCE_RECORD_FORMAT_VERSION = "1.0.0"
GEOREFERENCE_REVIEW_FORMAT_VERSION = "1.0.0"
GEOREFERENCE_ACCEPTANCE_FORMAT_VERSION = "1.0.0"
GEOREFERENCE_COMPONENT = "buduunkhad.phase03.georeference-evidence-v1"
GEOREFERENCE_RESOLVER = "buduunkhad.phase03.georeference-acceptance-resolver-v1"

Sha256 = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
NonEmpty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class GeoreferenceError(RuntimeError):
    """A georeference record, review, or bound file cannot be trusted."""


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


class GeoreferenceFileIdentity(_StrictModel):
    path: str
    sha256: Sha256
    size_bytes: int = Field(ge=0)

    @field_validator("path")
    @classmethod
    def _portable_path(cls, value: str) -> str:
        return canonical_relative_path(value)


class GcpMeasurement(_StrictModel):
    gcp_id: NonEmpty
    source_pixel_x: float
    source_pixel_y: float
    target_x: float
    target_y: float
    residual_x_metres: float
    residual_y_metres: float
    residual_metres: float = Field(ge=0)
    evidence_source: NonEmpty

    @model_validator(mode="after")
    def _residual_is_derived(self) -> GcpMeasurement:
        expected = math.hypot(self.residual_x_metres, self.residual_y_metres)
        if not math.isclose(self.residual_metres, expected, rel_tol=1e-9, abs_tol=1e-6):
            raise ValueError("GCP residual magnitude is inconsistent")
        return self


class ResidualSummary(_StrictModel):
    gcp_count: int = Field(gt=0)
    rmse_metres: float = Field(ge=0)
    mean_residual_metres: float = Field(ge=0)
    maximum_residual_metres: float = Field(ge=0)


class GeoreferenceMeasurementStatus(StrEnum):
    MEASURED = "measured"
    INCOMPLETE = "incomplete"


class _GeoreferenceRecordIdentity(_StrictModel):
    format_version: Literal["1.0.0"] = GEOREFERENCE_RECORD_FORMAT_VERSION
    processing_run_id: NonEmpty
    source_run_id: NonEmpty
    source: GeoreferenceFileIdentity
    derivative: GeoreferenceFileIdentity
    proposed_source_crs: NonEmpty | None
    source_crs_evidence: tuple[NonEmpty, ...] = ()
    target_epsg: int = Field(gt=0)
    transformation: NonEmpty
    resampling: NonEmpty
    gcps: tuple[GcpMeasurement, ...] = ()
    residual_summary: ResidualSummary | None
    spatial_distribution_findings: tuple[NonEmpty, ...] = Field(min_length=1)
    status: GeoreferenceMeasurementStatus
    limitations: tuple[NonEmpty, ...] = Field(min_length=1)
    component: Literal["buduunkhad.phase03.georeference-evidence-v1"] = GEOREFERENCE_COMPONENT

    @model_validator(mode="after")
    def _coherent_measurements(self) -> _GeoreferenceRecordIdentity:
        ids = tuple(item.gcp_id for item in self.gcps)
        if tuple(sorted(set(ids))) != ids:
            raise ValueError("GCP identities must be unique and ordered")
        if tuple(sorted(set(self.source_crs_evidence))) != self.source_crs_evidence:
            raise ValueError("source CRS evidence must be unique and ordered")
        if tuple(sorted(set(self.spatial_distribution_findings))) != (
            self.spatial_distribution_findings
        ):
            raise ValueError("spatial-distribution findings must be unique and ordered")
        if tuple(sorted(set(self.limitations))) != self.limitations:
            raise ValueError("georeference limitations must be unique and ordered")
        if self.gcps:
            if self.residual_summary is None:
                raise ValueError("GCP measurements require a residual summary")
            residuals = tuple(item.residual_metres for item in self.gcps)
            expected_rmse = math.sqrt(sum(item * item for item in residuals) / len(residuals))
            if (
                self.residual_summary.gcp_count != len(self.gcps)
                or not math.isclose(
                    self.residual_summary.rmse_metres,
                    expected_rmse,
                    rel_tol=1e-9,
                    abs_tol=1e-6,
                )
                or not math.isclose(
                    self.residual_summary.mean_residual_metres,
                    sum(residuals) / len(residuals),
                    rel_tol=1e-9,
                    abs_tol=1e-6,
                )
                or not math.isclose(
                    self.residual_summary.maximum_residual_metres,
                    max(residuals),
                    rel_tol=1e-9,
                    abs_tol=1e-6,
                )
            ):
                raise ValueError("georeference residual summary is inconsistent")
        elif self.residual_summary is not None:
            raise ValueError("residual summary cannot exist without GCP measurements")
        complete = bool(
            self.proposed_source_crs
            and self.source_crs_evidence
            and self.gcps
            and self.residual_summary
        )
        expected = (
            GeoreferenceMeasurementStatus.MEASURED
            if complete
            else GeoreferenceMeasurementStatus.INCOMPLETE
        )
        if self.status is not expected:
            raise ValueError("georeference measurement status is inconsistent")
        return self


class GeoreferenceRecord(_GeoreferenceRecordIdentity):
    record_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> GeoreferenceRecord:
        identity = _GeoreferenceRecordIdentity.model_validate(
            self.model_dump(mode="python", exclude={"record_id"})
        )
        if self.record_id != sha256_value(identity):
            raise ValueError("georeference record identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> GeoreferenceRecord:
        identity = _GeoreferenceRecordIdentity.model_validate(values)
        return cls(**identity.model_dump(mode="python"), record_id=sha256_value(identity))


class GeoreferenceReviewerRole(StrEnum):
    GEOSPATIAL_REVIEWER = "qualified-geospatial-reviewer"
    PROJECT_GEOLOGIST = "project-geologist"


class GeoreferenceReviewDecision(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class _GeoreferenceReviewIdentity(_StrictModel):
    format_version: Literal["1.0.0"] = GEOREFERENCE_REVIEW_FORMAT_VERSION
    record_id: Sha256
    record_file_sha256: Sha256
    source_sha256: Sha256
    derivative_sha256: Sha256
    processing_run_id: NonEmpty
    reviewer: NonEmpty
    reviewer_role: GeoreferenceReviewerRole
    reviewer_authorization_id: NonEmpty
    reviewed_at: datetime
    decision: GeoreferenceReviewDecision
    rationale: NonEmpty
    visual_alignment_findings: tuple[NonEmpty, ...] = Field(min_length=1)
    limitations: tuple[NonEmpty, ...] = ()

    @model_validator(mode="after")
    def _truthful_review(self) -> _GeoreferenceReviewIdentity:
        if self.reviewed_at.tzinfo is None or self.reviewed_at.utcoffset() is None:
            raise ValueError("georeference review time must be timezone-aware")
        if self.reviewed_at.utcoffset() != UTC.utcoffset(None):
            raise ValueError("georeference review time must be recorded in UTC")
        if tuple(sorted(set(self.visual_alignment_findings))) != (self.visual_alignment_findings):
            raise ValueError("visual-alignment findings must be unique and ordered")
        if tuple(sorted(set(self.limitations))) != self.limitations:
            raise ValueError("georeference review limitations must be unique and ordered")
        return self


class GeoreferenceReviewAttestation(_GeoreferenceReviewIdentity):
    attestation_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> GeoreferenceReviewAttestation:
        identity = _GeoreferenceReviewIdentity.model_validate(
            self.model_dump(mode="python", exclude={"attestation_id"})
        )
        if self.attestation_id != sha256_value(identity):
            raise ValueError("georeference review identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> GeoreferenceReviewAttestation:
        identity = _GeoreferenceReviewIdentity.model_validate(values)
        return cls(
            **identity.model_dump(mode="python"),
            attestation_id=sha256_value(identity),
        )


class _GeoreferenceAcceptanceIdentity(_StrictModel):
    format_version: Literal["1.0.0"] = GEOREFERENCE_ACCEPTANCE_FORMAT_VERSION
    record_id: Sha256
    record_file_sha256: Sha256
    processing_run_id: NonEmpty
    source: GeoreferenceFileIdentity
    derivative: GeoreferenceFileIdentity
    accepted_attestation_ids: tuple[Sha256, Sha256]
    accepted_at: datetime
    resolver_component: Literal["buduunkhad.phase03.georeference-acceptance-resolver-v1"] = (
        GEOREFERENCE_RESOLVER
    )

    @model_validator(mode="after")
    def _ordered_resolution(self) -> _GeoreferenceAcceptanceIdentity:
        if tuple(sorted(set(self.accepted_attestation_ids))) != self.accepted_attestation_ids:
            raise ValueError("georeference acceptance attestations must be unique and ordered")
        if self.accepted_at.tzinfo is None or self.accepted_at.utcoffset() is None:
            raise ValueError("georeference acceptance time must be timezone-aware")
        if self.accepted_at.utcoffset() != UTC.utcoffset(None):
            raise ValueError("georeference acceptance time must be recorded in UTC")
        return self


class GeoreferenceAcceptanceRecord(_GeoreferenceAcceptanceIdentity):
    acceptance_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> GeoreferenceAcceptanceRecord:
        identity = _GeoreferenceAcceptanceIdentity.model_validate(
            self.model_dump(mode="python", exclude={"acceptance_id"})
        )
        if self.acceptance_id != sha256_value(identity):
            raise ValueError("georeference acceptance identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> GeoreferenceAcceptanceRecord:
        identity = _GeoreferenceAcceptanceIdentity.model_validate(values)
        return cls(
            **identity.model_dump(mode="python"),
            acceptance_id=sha256_value(identity),
        )


def create_georeference_record(
    *,
    processing_run_id: str,
    source_run_id: str,
    source_root: Path,
    source_path: Path,
    derivative_root: Path,
    derivative_path: Path,
    proposed_source_crs: str | None,
    source_crs_evidence: tuple[str, ...],
    target_epsg: int,
    transformation: str,
    resampling: str,
    gcps: tuple[GcpMeasurement, ...],
    spatial_distribution_findings: tuple[str, ...],
    limitations: tuple[str, ...],
) -> GeoreferenceRecord:
    residuals = tuple(item.residual_metres for item in gcps)
    summary = (
        ResidualSummary(
            gcp_count=len(gcps),
            rmse_metres=math.sqrt(sum(item * item for item in residuals) / len(residuals)),
            mean_residual_metres=sum(residuals) / len(residuals),
            maximum_residual_metres=max(residuals),
        )
        if residuals
        else None
    )
    status = (
        GeoreferenceMeasurementStatus.MEASURED
        if proposed_source_crs and source_crs_evidence and gcps
        else GeoreferenceMeasurementStatus.INCOMPLETE
    )
    return GeoreferenceRecord.create(
        processing_run_id=processing_run_id,
        source_run_id=source_run_id,
        source=_file_identity(source_root, source_path),
        derivative=_file_identity(derivative_root, derivative_path),
        proposed_source_crs=proposed_source_crs,
        source_crs_evidence=tuple(sorted(set(source_crs_evidence))),
        target_epsg=target_epsg,
        transformation=transformation,
        resampling=resampling,
        gcps=tuple(sorted(gcps, key=lambda item: item.gcp_id)),
        residual_summary=summary,
        spatial_distribution_findings=tuple(sorted(set(spatial_distribution_findings))),
        status=status,
        limitations=tuple(sorted(set(limitations))),
    )


def create_georeference_review(
    record_path: Path,
    *,
    reviewer: str,
    reviewer_role: GeoreferenceReviewerRole,
    reviewer_authorization_id: str,
    reviewed_at: datetime,
    decision: GeoreferenceReviewDecision,
    rationale: str,
    visual_alignment_findings: tuple[str, ...],
    limitations: tuple[str, ...] = (),
) -> GeoreferenceReviewAttestation:
    record = load_georeference_record(record_path)
    return GeoreferenceReviewAttestation.create(
        record_id=record.record_id,
        record_file_sha256=sha256_file(Path(record_path)),
        source_sha256=record.source.sha256,
        derivative_sha256=record.derivative.sha256,
        processing_run_id=record.processing_run_id,
        reviewer=reviewer,
        reviewer_role=reviewer_role,
        reviewer_authorization_id=reviewer_authorization_id,
        reviewed_at=reviewed_at,
        decision=decision,
        rationale=rationale,
        visual_alignment_findings=tuple(sorted(set(visual_alignment_findings))),
        limitations=tuple(sorted(set(limitations))),
    )


def resolve_georeference_acceptance(
    record_path: Path,
    *,
    source_root: Path,
    derivative_root: Path,
    attestation_paths: tuple[Path, ...],
) -> GeoreferenceAcceptanceRecord:
    """Resolve exactly one accepted review for each required role."""

    record = load_georeference_record(record_path)
    if record.status is not GeoreferenceMeasurementStatus.MEASURED:
        raise GeoreferenceError("incomplete georeference measurements cannot be accepted")
    verify_georeference_files(
        record,
        source_root=source_root,
        derivative_root=derivative_root,
    )
    record_hash = sha256_file(Path(record_path))
    attestations = tuple(load_georeference_review(path) for path in attestation_paths)
    if len(attestations) != 2:
        raise GeoreferenceError("georeference acceptance requires exactly two review attestations")
    expected_roles = {
        GeoreferenceReviewerRole.GEOSPATIAL_REVIEWER,
        GeoreferenceReviewerRole.PROJECT_GEOLOGIST,
    }
    roles = {item.reviewer_role for item in attestations}
    if roles != expected_roles:
        raise GeoreferenceError("georeference acceptance requires both exact reviewer roles")
    if any(
        item.record_id != record.record_id
        or item.record_file_sha256 != record_hash
        or item.source_sha256 != record.source.sha256
        or item.derivative_sha256 != record.derivative.sha256
        or item.processing_run_id != record.processing_run_id
        for item in attestations
    ):
        raise GeoreferenceError("georeference review does not bind the exact measured record")
    if any(item.decision is not GeoreferenceReviewDecision.ACCEPTED for item in attestations):
        raise GeoreferenceError("georeference acceptance requires two accepted decisions")
    return GeoreferenceAcceptanceRecord.create(
        record_id=record.record_id,
        record_file_sha256=record_hash,
        processing_run_id=record.processing_run_id,
        source=record.source,
        derivative=record.derivative,
        accepted_attestation_ids=tuple(sorted(item.attestation_id for item in attestations)),
        accepted_at=max(item.reviewed_at for item in attestations),
    )


def write_georeference_record(
    record: GeoreferenceRecord | GeoreferenceReviewAttestation | GeoreferenceAcceptanceRecord,
    path: Path,
) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(record.model_dump_json(indent=2) + "\n", encoding="utf-8", newline="\n")
    return target


def load_georeference_record(path: Path) -> GeoreferenceRecord:
    return _load(path, GeoreferenceRecord, "georeference record")


def load_georeference_review(path: Path) -> GeoreferenceReviewAttestation:
    return _load(path, GeoreferenceReviewAttestation, "georeference review")


def load_georeference_acceptance(path: Path) -> GeoreferenceAcceptanceRecord:
    return _load(path, GeoreferenceAcceptanceRecord, "georeference acceptance")


def verify_georeference_files(
    record: GeoreferenceRecord,
    *,
    source_root: Path,
    derivative_root: Path,
) -> None:
    try:
        _verify_file_identity(source_root, record.source)
        _verify_file_identity(derivative_root, record.derivative)
    except (ArtifactSealError, OSError) as exc:
        raise GeoreferenceError("georeference file identity is invalid") from exc


def _load(path: Path, model: type[_StrictModel], description: str):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        return model.model_validate(data)
    except (OSError, UnicodeError, ValueError) as exc:
        raise GeoreferenceError(f"{description} is invalid") from exc


def _file_identity(root: Path, path: Path) -> GeoreferenceFileIdentity:
    safe = require_regular_file_under(root, path, description="georeference artifact")
    relative = safe.relative_to(Path(root).absolute().resolve()).as_posix()
    return GeoreferenceFileIdentity(
        path=relative,
        sha256=sha256_file(safe),
        size_bytes=safe.stat().st_size,
    )


def _verify_file_identity(root: Path, identity: GeoreferenceFileIdentity) -> None:
    safe = require_regular_file_under(
        root,
        Path(root) / identity.path,
        description="georeference artifact",
    )
    if safe.stat().st_size != identity.size_bytes or sha256_file(safe) != identity.sha256:
        raise GeoreferenceError(f"georeference artifact bytes changed: {identity.path}")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result
