"""Human-reviewed prospect-polygon scoring kept separate from the legacy grid comparator."""

from __future__ import annotations

import csv
import json
import os
import uuid
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any, Literal, Self, cast

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from buduunkhad.ai.fingerprint import sha256_value
from buduunkhad.core.evidence_manifest import (
    EvidenceAuthorityResolver,
    EvidenceManifestBinding,
    EvidenceRole,
    ResolvedEvidence,
    evidence_bindings,
)
from buduunkhad.core.phase03_science import (
    Phase03ScientificHandoff,
    load_phase03_scientific_handoff,
)
from buduunkhad.core.run_artifacts import (
    canonical_relative_path,
    require_regular_file_under,
    sha256_file,
)
from buduunkhad.core.run_storage import resolve_source_phase, validate_run_id
from buduunkhad.geospatial_ai.methodology import load_phase04_migration_contract
from buduunkhad.geospatial_ai.path_safety import StorageRoots

PHASE04_ACTIVATION_CANDIDATE_FORMAT_VERSION = "1.0.0"
PHASE04_ACTIVATION_REVIEW_FORMAT_VERSION = "1.0.0"
PHASE04_ACTIVATION_FORMAT_VERSION = "1.0.0"
PHASE04_SCORECARD_FORMAT_VERSION = "1.0.0"
PHASE04_RESULT_FORMAT_VERSION = "1.0.0"
PHASE04_IMPLEMENTATION_COMPONENT = "buduunkhad.phase04.prospect-polygon-v1"
PHASE04_ACTIVATION_RESOLVER = "buduunkhad.phase04.activation-resolver-v1"

Sha256 = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
NonEmpty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

CRITERION_MAXIMA: tuple[tuple[str, int], ...] = (
    ("geology", 20),
    ("occurrence", 15),
    ("geochemistry", 20),
    ("remote_sensing", 15),
    ("structure", 10),
    ("deposit_model_fit", 10),
    ("access", 5),
    ("confidence", 5),
)
MEASURED_ROLES: tuple[EvidenceRole, ...] = (
    EvidenceRole.ACCESS,
    EvidenceRole.ALTERATION_SUPPORT,
    EvidenceRole.GEOCHEMICAL_ANOMALY,
    EvidenceRole.GEOLOGY,
    EvidenceRole.OCCURRENCE,
    EvidenceRole.STRUCTURE,
)


class Phase04AuthoritativeError(RuntimeError):
    """The authoritative prospect workflow cannot trust an input or output."""


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


class ExactFileIdentity(_StrictModel):
    path: str
    sha256: Sha256
    size_bytes: int = Field(ge=0)

    _portable_path = field_validator("path")(canonical_relative_path)


class _Phase04ActivationCandidateIdentity(_StrictModel):
    format_version: Literal["1.0.0"] = PHASE04_ACTIVATION_CANDIDATE_FORMAT_VERSION
    phase03_handoff_id: Sha256
    phase03_handoff_file_sha256: Sha256
    reference_set: ExactFileIdentity
    calibration_report: ExactFileIdentity
    methodology_authority_sha256: Sha256
    implementation_component: Literal["buduunkhad.phase04.prospect-polygon-v1"] = (
        PHASE04_IMPLEMENTATION_COMPONENT
    )
    limitations: tuple[NonEmpty, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _coherent_candidate(self) -> _Phase04ActivationCandidateIdentity:
        if self.reference_set.path == self.calibration_report.path:
            raise ValueError("reference set and calibration report must be separate files")
        if tuple(sorted(set(self.limitations))) != self.limitations:
            raise ValueError("activation limitations must be unique and ordered")
        return self


class Phase04ActivationCandidate(_Phase04ActivationCandidateIdentity):
    candidate_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> Phase04ActivationCandidate:
        identity = _Phase04ActivationCandidateIdentity.model_validate(
            self.model_dump(mode="python", exclude={"candidate_id"})
        )
        if self.candidate_id != sha256_value(identity):
            raise ValueError("Phase 04 activation candidate identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> Phase04ActivationCandidate:
        identity = _Phase04ActivationCandidateIdentity.model_validate(values)
        return cls(**identity.model_dump(mode="python"), candidate_id=sha256_value(identity))


class Phase04ActivationRole(StrEnum):
    METHODOLOGY_OWNER = "methodology-owner"
    PROJECT_GEOLOGIST = "project-geologist"


class Phase04ActivationDecision(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class _Phase04ActivationReviewIdentity(_StrictModel):
    format_version: Literal["1.0.0"] = PHASE04_ACTIVATION_REVIEW_FORMAT_VERSION
    candidate_id: Sha256
    candidate_file_sha256: Sha256
    reviewer: NonEmpty
    reviewer_role: Phase04ActivationRole
    reviewer_authorization_id: NonEmpty
    reviewed_at: datetime
    decision: Phase04ActivationDecision
    rationale: NonEmpty
    limitations: tuple[NonEmpty, ...] = ()

    @model_validator(mode="after")
    def _truthful_review(self) -> _Phase04ActivationReviewIdentity:
        if self.reviewed_at.tzinfo is None or self.reviewed_at.utcoffset() is None:
            raise ValueError("Phase 04 activation review time must be timezone-aware")
        if self.reviewed_at.utcoffset() != UTC.utcoffset(None):
            raise ValueError("Phase 04 activation review time must be recorded in UTC")
        if tuple(sorted(set(self.limitations))) != self.limitations:
            raise ValueError("activation review limitations must be unique and ordered")
        return self


class Phase04ActivationReview(_Phase04ActivationReviewIdentity):
    review_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> Phase04ActivationReview:
        identity = _Phase04ActivationReviewIdentity.model_validate(
            self.model_dump(mode="python", exclude={"review_id"})
        )
        if self.review_id != sha256_value(identity):
            raise ValueError("Phase 04 activation review identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> Phase04ActivationReview:
        identity = _Phase04ActivationReviewIdentity.model_validate(values)
        return cls(**identity.model_dump(mode="python"), review_id=sha256_value(identity))


class _Phase04ActivationIdentity(_StrictModel):
    format_version: Literal["1.0.0"] = PHASE04_ACTIVATION_FORMAT_VERSION
    candidate_id: Sha256
    candidate_file_sha256: Sha256
    phase03_handoff_id: Sha256
    accepted_review_ids: tuple[Sha256, Sha256]
    activated_at: datetime
    readiness_id_resolved: Literal["METH-READY-007"] = "METH-READY-007"
    resolver_component: Literal["buduunkhad.phase04.activation-resolver-v1"] = (
        PHASE04_ACTIVATION_RESOLVER
    )

    @model_validator(mode="after")
    def _coherent_activation(self) -> _Phase04ActivationIdentity:
        if tuple(sorted(set(self.accepted_review_ids))) != self.accepted_review_ids:
            raise ValueError("Phase 04 activation reviews must be unique and ordered")
        if self.activated_at.tzinfo is None or self.activated_at.utcoffset() is None:
            raise ValueError("Phase 04 activation time must be timezone-aware")
        if self.activated_at.utcoffset() != UTC.utcoffset(None):
            raise ValueError("Phase 04 activation time must be recorded in UTC")
        return self


class Phase04Activation(_Phase04ActivationIdentity):
    activation_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> Phase04Activation:
        identity = _Phase04ActivationIdentity.model_validate(
            self.model_dump(mode="python", exclude={"activation_id"})
        )
        if self.activation_id != sha256_value(identity):
            raise ValueError("Phase 04 activation identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> Phase04Activation:
        identity = _Phase04ActivationIdentity.model_validate(values)
        return cls(**identity.model_dump(mode="python"), activation_id=sha256_value(identity))


class CriterionScore(_StrictModel):
    criterion_id: NonEmpty
    awarded_points: int = Field(ge=0, le=100)
    rationale: NonEmpty
    evidence_ids: tuple[NonEmpty, ...]
    data_gap: bool

    @model_validator(mode="after")
    def _ordered_evidence(self) -> CriterionScore:
        if tuple(sorted(set(self.evidence_ids))) != self.evidence_ids:
            raise ValueError("criterion evidence IDs must be unique and ordered")
        if self.data_gap and self.awarded_points > 0:
            raise ValueError("a criterion with a data gap cannot receive positive points")
        if self.awarded_points > 0 and not self.evidence_ids:
            raise ValueError("a positive criterion score requires exact evidence identities")
        return self


class ProspectScore(_StrictModel):
    prospect_id: NonEmpty
    scores: tuple[CriterionScore, ...]
    dominant_deposit_model: NonEmpty
    model_confidence: NonEmpty
    missing_model_evidence: tuple[NonEmpty, ...]
    validation_priority: NonEmpty
    confidence: NonEmpty
    limitations: tuple[NonEmpty, ...]
    data_gaps: tuple[NonEmpty, ...]
    next_action: NonEmpty

    @model_validator(mode="after")
    def _complete_score(self) -> ProspectScore:
        actual = tuple((item.criterion_id, item.awarded_points) for item in self.scores)
        if tuple(item[0] for item in actual) != tuple(item[0] for item in CRITERION_MAXIMA):
            raise ValueError("prospect criteria must exactly follow the adopted order")
        maxima = dict(CRITERION_MAXIMA)
        if any(points > maxima[criterion] for criterion, points in actual):
            raise ValueError("prospect criterion score exceeds its adopted maximum")
        for values, description in (
            (self.missing_model_evidence, "missing model evidence"),
            (self.limitations, "limitations"),
            (self.data_gaps, "data gaps"),
        ):
            if tuple(sorted(set(values))) != values:
                raise ValueError(f"prospect {description} must be unique and ordered")
        return self

    @property
    def total_score(self) -> int:
        return sum(item.awarded_points for item in self.scores)


class _Phase04ScorecardIdentity(_StrictModel):
    format_version: Literal["1.0.0"] = PHASE04_SCORECARD_FORMAT_VERSION
    prospect_source_sha256: Sha256
    prospect_layer: NonEmpty
    reviewer: NonEmpty
    reviewer_role: Literal["project-geologist"] = "project-geologist"
    reviewer_authorization_id: NonEmpty
    reviewed_at: datetime
    geometry_review_decision: Literal["accepted"]
    scores: tuple[ProspectScore, ...] = Field(min_length=1)
    limitations: tuple[NonEmpty, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _coherent_scorecard(self) -> _Phase04ScorecardIdentity:
        if self.reviewed_at.tzinfo is None or self.reviewed_at.utcoffset() is None:
            raise ValueError("Phase 04 score review time must be timezone-aware")
        if self.reviewed_at.utcoffset() != UTC.utcoffset(None):
            raise ValueError("Phase 04 score review time must be recorded in UTC")
        ids = tuple(item.prospect_id for item in self.scores)
        if tuple(sorted(set(ids))) != ids:
            raise ValueError("prospect score records must be unique and ordered")
        if tuple(sorted(set(self.limitations))) != self.limitations:
            raise ValueError("scorecard limitations must be unique and ordered")
        return self


class Phase04Scorecard(_Phase04ScorecardIdentity):
    scorecard_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> Phase04Scorecard:
        identity = _Phase04ScorecardIdentity.model_validate(
            self.model_dump(mode="python", exclude={"scorecard_id"})
        )
        if self.scorecard_id != sha256_value(identity):
            raise ValueError("Phase 04 scorecard identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> Phase04Scorecard:
        identity = _Phase04ScorecardIdentity.model_validate(values)
        return cls(**identity.model_dump(mode="python"), scorecard_id=sha256_value(identity))


class _Phase04ResultIdentity(_StrictModel):
    format_version: Literal["1.0.0"] = PHASE04_RESULT_FORMAT_VERSION
    run_id: NonEmpty
    workflow_mode: Literal["authoritative-prospect-polygons"] = "authoritative-prospect-polygons"
    phase03_handoff_id: Sha256
    phase03_handoff_file_sha256: Sha256
    activation_id: Sha256
    activation_file_sha256: Sha256
    prospect_source: ExactFileIdentity
    prospect_layer: NonEmpty
    scorecard_id: Sha256
    scorecard_file_sha256: Sha256
    evidence_manifest_bindings: tuple[EvidenceManifestBinding, ...] = Field(min_length=1)
    output_artifacts: tuple[ExactFileIdentity, ExactFileIdentity]
    prospect_count: int = Field(gt=0)
    class_counts: tuple[tuple[Literal["A", "B", "C", "D"], int], ...]
    limitations: tuple[NonEmpty, ...] = Field(min_length=1)
    implementation_component: Literal["buduunkhad.phase04.prospect-polygon-v1"] = (
        PHASE04_IMPLEMENTATION_COMPONENT
    )

    @model_validator(mode="after")
    def _coherent_result(self) -> _Phase04ResultIdentity:
        validate_run_id(self.run_id)
        if tuple(item.path for item in self.output_artifacts) != (
            "prospect_measurements.csv",
            "ranked_prospects.gpkg",
        ):
            raise ValueError("Phase 04 output inventory is incomplete or out of order")
        expected_classes = ("A", "B", "C", "D")
        if tuple(item[0] for item in self.class_counts) != expected_classes:
            raise ValueError("Phase 04 class counts are incomplete or out of order")
        if sum(item[1] for item in self.class_counts) != self.prospect_count:
            raise ValueError("Phase 04 class counts do not match the prospect count")
        if tuple(sorted(set(self.limitations))) != self.limitations:
            raise ValueError("Phase 04 result limitations must be unique and ordered")
        return self


class Phase04AuthoritativeResult(_Phase04ResultIdentity):
    result_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> Phase04AuthoritativeResult:
        identity = _Phase04ResultIdentity.model_validate(
            self.model_dump(mode="python", exclude={"result_id"})
        )
        if self.result_id != sha256_value(identity):
            raise ValueError("Phase 04 result identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> Phase04AuthoritativeResult:
        identity = _Phase04ResultIdentity.model_validate(values)
        return cls(**identity.model_dump(mode="python"), result_id=sha256_value(identity))


def create_phase04_activation_candidate(
    handoff_path: Path,
    *,
    reference_root: Path,
    reference_set_path: Path,
    calibration_report_path: Path,
    limitations: tuple[str, ...],
) -> Phase04ActivationCandidate:
    handoff = load_phase03_scientific_handoff(handoff_path)
    contract = load_phase04_migration_contract()
    return Phase04ActivationCandidate.create(
        phase03_handoff_id=handoff.handoff_id,
        phase03_handoff_file_sha256=sha256_file(Path(handoff_path)),
        reference_set=_file_identity(reference_root, reference_set_path),
        calibration_report=_file_identity(reference_root, calibration_report_path),
        methodology_authority_sha256=contract.authority_sha256,
        limitations=tuple(sorted(set(limitations))),
    )


def create_phase04_activation_review(
    candidate_path: Path,
    *,
    reviewer: str,
    reviewer_role: Phase04ActivationRole,
    reviewer_authorization_id: str,
    reviewed_at: datetime,
    decision: Phase04ActivationDecision,
    rationale: str,
    limitations: tuple[str, ...] = (),
) -> Phase04ActivationReview:
    candidate = load_phase04_activation_candidate(candidate_path)
    return Phase04ActivationReview.create(
        candidate_id=candidate.candidate_id,
        candidate_file_sha256=sha256_file(Path(candidate_path)),
        reviewer=reviewer,
        reviewer_role=reviewer_role,
        reviewer_authorization_id=reviewer_authorization_id,
        reviewed_at=reviewed_at,
        decision=decision,
        rationale=rationale,
        limitations=tuple(sorted(set(limitations))),
    )


def resolve_phase04_activation(
    candidate_path: Path,
    *,
    handoff_path: Path,
    reference_root: Path,
    review_paths: tuple[Path, ...],
) -> Phase04Activation:
    candidate = load_phase04_activation_candidate(candidate_path)
    handoff = load_phase03_scientific_handoff(handoff_path)
    if (
        handoff.handoff_id != candidate.phase03_handoff_id
        or sha256_file(Path(handoff_path)) != candidate.phase03_handoff_file_sha256
    ):
        raise Phase04AuthoritativeError("activation candidate does not bind the exact handoff")
    _verify_file(reference_root, candidate.reference_set)
    _verify_file(reference_root, candidate.calibration_report)
    contract = load_phase04_migration_contract()
    if candidate.methodology_authority_sha256 != contract.authority_sha256:
        raise Phase04AuthoritativeError("activation candidate methodology authority changed")
    reviews = tuple(load_phase04_activation_review(path) for path in review_paths)
    if len(reviews) != 2 or {item.reviewer_role for item in reviews} != {
        Phase04ActivationRole.METHODOLOGY_OWNER,
        Phase04ActivationRole.PROJECT_GEOLOGIST,
    }:
        raise Phase04AuthoritativeError("activation requires both exact reviewer roles")
    candidate_hash = sha256_file(Path(candidate_path))
    if any(
        item.candidate_id != candidate.candidate_id or item.candidate_file_sha256 != candidate_hash
        for item in reviews
    ):
        raise Phase04AuthoritativeError("activation review does not bind the exact candidate")
    if any(item.decision is not Phase04ActivationDecision.ACCEPTED for item in reviews):
        raise Phase04AuthoritativeError("activation requires two accepted decisions")
    return Phase04Activation.create(
        candidate_id=candidate.candidate_id,
        candidate_file_sha256=candidate_hash,
        phase03_handoff_id=handoff.handoff_id,
        accepted_review_ids=tuple(sorted(item.review_id for item in reviews)),
        activated_at=max(item.reviewed_at for item in reviews),
    )


def create_phase04_scorecard(
    prospect_path: Path,
    *,
    prospect_layer: str,
    reviewer: str,
    reviewer_authorization_id: str,
    reviewed_at: datetime,
    scores: tuple[ProspectScore, ...],
    limitations: tuple[str, ...],
) -> Phase04Scorecard:
    """Bind human geometry acceptance and score judgments to exact prospect bytes."""

    return Phase04Scorecard.create(
        prospect_source_sha256=sha256_file(Path(prospect_path)),
        prospect_layer=prospect_layer,
        reviewer=reviewer,
        reviewer_authorization_id=reviewer_authorization_id,
        reviewed_at=reviewed_at,
        geometry_review_decision="accepted",
        scores=tuple(sorted(scores, key=lambda item: item.prospect_id)),
        limitations=tuple(sorted(set(limitations))),
    )


def run_phase04_authoritative(
    *,
    roots: StorageRoots,
    run_id: str,
    runs_root: Path,
    evidence_root: Path,
    target_epsg: int,
    handoff_path: Path,
    activation_path: Path,
    activation_candidate_path: Path,
    activation_reference_root: Path,
    prospect_path: Path,
    prospect_layer: str,
    scorecard_path: Path,
    evidence_manifest_ids: tuple[str, ...],
) -> tuple[Path, Phase04AuthoritativeResult]:
    """Measure reviewed polygons and apply only exact human-reviewed score judgments."""

    run_directory = roots.run_directory(run_id, create=True)
    handoff_file = roots.assert_run_artifact(handoff_path, run_id=run_id)
    activation_file = roots.assert_run_artifact(activation_path, run_id=run_id)
    candidate_file = roots.assert_run_artifact(activation_candidate_path, run_id=run_id)
    prospect_file = roots.assert_run_artifact(prospect_path, run_id=run_id)
    scorecard_file = roots.assert_run_artifact(scorecard_path, run_id=run_id)
    handoff = load_phase03_scientific_handoff(handoff_file)
    activation = load_phase04_activation(activation_file)
    candidate = load_phase04_activation_candidate(candidate_file)
    if (
        activation.phase03_handoff_id != handoff.handoff_id
        or activation.candidate_id != candidate.candidate_id
        or activation.candidate_file_sha256 != sha256_file(candidate_file)
        or candidate.phase03_handoff_id != handoff.handoff_id
        or candidate.phase03_handoff_file_sha256 != sha256_file(handoff_file)
    ):
        raise Phase04AuthoritativeError("Phase 04 activation chain is inconsistent")
    _verify_file(activation_reference_root, candidate.reference_set)
    _verify_file(activation_reference_root, candidate.calibration_report)
    source = resolve_source_phase(
        runs_root,
        "03",
        handoff.phase03_source.source_run_id,
        require_advance=False,
        require_qaqc_passed=True,
    )
    if source.binding != handoff.phase03_source:
        raise Phase04AuthoritativeError("sealed Phase 03 source changed after handoff")

    resolver = EvidenceAuthorityResolver(
        runs_root=runs_root,
        evidence_root=evidence_root,
        target_epsg=target_epsg,
    )
    evidence = resolver.resolve_selected(evidence_manifest_ids)
    if evidence_bindings(evidence) != handoff.evidence_manifest_bindings:
        raise Phase04AuthoritativeError("Phase 04 evidence differs from the scientific handoff")
    if {item.record.evidence_id for item in evidence} != set(handoff.accepted_evidence_ids):
        raise Phase04AuthoritativeError("Phase 04 evidence inventory differs from the handoff")
    for item in evidence:
        item.verify_current_artifact()

    scorecard = load_phase04_scorecard(scorecard_file)
    if (
        scorecard.prospect_source_sha256 != sha256_file(prospect_file)
        or scorecard.prospect_layer != prospect_layer
    ):
        raise Phase04AuthoritativeError("scorecard does not bind the exact prospect geometry")
    allowed_score_evidence = set(handoff.accepted_evidence_ids) | {
        handoff.handoff_id,
        handoff.boundary_acceptance.record_id,
        handoff.deposit_model_assessment.record_id,
        handoff.deposit_model_review.record_id,
    }
    for prospect in scorecard.scores:
        for criterion in prospect.scores:
            unknown = set(criterion.evidence_ids) - allowed_score_evidence
            if unknown:
                raise Phase04AuthoritativeError(
                    f"prospect score cites evidence outside the handoff: {sorted(unknown)}"
                )

    final = run_directory / "phase04-authoritative"
    if final.exists():
        existing = load_phase04_result(final / "phase04_authoritative_result.json")
        verify_phase04_result(
            existing,
            result_directory=final,
            handoff_path=handoff_file,
            activation_path=activation_file,
            prospect_path=prospect_file,
            scorecard_path=scorecard_file,
        )
        return final, existing
    staging = roots.assert_writable(
        run_directory / f".phase04-authoritative.{uuid.uuid4().hex}.staging",
        run_id=run_id,
    )
    staging.mkdir()
    try:
        result = _produce_phase04_outputs(
            staging=staging,
            run_id=run_id,
            target_epsg=target_epsg,
            handoff=handoff,
            handoff_path=handoff_file,
            activation=activation,
            activation_path=activation_file,
            prospect_path=prospect_file,
            prospect_layer=prospect_layer,
            scorecard=scorecard,
            scorecard_path=scorecard_file,
            evidence=evidence,
        )
        (staging / "phase04_authoritative_result.json").write_text(
            result.model_dump_json(indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        os.replace(staging, final)
    except Exception:
        # A failed staging directory is deliberately not reusable or mistaken for a result.
        raise
    return final, result


def _produce_phase04_outputs(
    *,
    staging: Path,
    run_id: str,
    target_epsg: int,
    handoff: Phase03ScientificHandoff,
    handoff_path: Path,
    activation: Phase04Activation,
    activation_path: Path,
    prospect_path: Path,
    prospect_layer: str,
    scorecard: Phase04Scorecard,
    scorecard_path: Path,
    evidence: tuple[ResolvedEvidence, ...],
) -> Phase04AuthoritativeResult:
    import geopandas as gpd

    prospects = gpd.read_file(prospect_path, layer=prospect_layer)
    _validate_prospects(prospects, target_epsg)
    prospect_ids = tuple(sorted(str(value).strip() for value in prospects["prospect_id"]))
    score_ids = tuple(item.prospect_id for item in scorecard.scores)
    if prospect_ids != score_ids:
        raise Phase04AuthoritativeError(
            "scorecard prospect identities do not match reviewed geometry"
        )
    prospects = prospects.set_index(prospects["prospect_id"].astype(str), drop=False)
    role_frames = _evidence_frames(evidence, target_epsg)
    measurements: list[dict[str, object]] = []
    ranked_rows: list[dict[str, object]] = []
    classes: dict[str, int] = {"A": 0, "B": 0, "C": 0, "D": 0}
    score_by_id = {item.prospect_id: item for item in scorecard.scores}
    for prospect_id in prospect_ids:
        geometry = prospects.loc[prospect_id].geometry
        score = score_by_id[prospect_id]
        total = score.total_score
        prospect_class = _class_for_score(total)
        classes[prospect_class] += 1
        row: dict[str, object] = {
            "prospect_id": prospect_id,
            "area_m2": float(geometry.area),
            "perimeter_m": float(geometry.length),
        }
        for role in MEASURED_ROLES:
            row.update(_measure_role(geometry, role_frames.get(role), role.value))
        measurements.append(row)
        score_values = {item.criterion_id: item.awarded_points for item in score.scores}
        ranked_rows.append(
            {
                "prospect_id": prospect_id,
                **{f"score_{key}": value for key, value in score_values.items()},
                "total_score": total,
                "prospect_class": prospect_class,
                "dominant_deposit_model": score.dominant_deposit_model,
                "model_confidence": score.model_confidence,
                "missing_model_evidence": _json_list(score.missing_model_evidence),
                "validation_priority": score.validation_priority,
                "confidence": score.confidence,
                "limitations": _json_list(score.limitations),
                "data_gaps": _json_list(score.data_gaps),
                "next_action": score.next_action,
                "reviewer": scorecard.reviewer,
                "review_timestamp": scorecard.reviewed_at.isoformat(),
                "scorecard_id": scorecard.scorecard_id,
            }
        )

    measurements_path = staging / "prospect_measurements.csv"
    _write_measurements(measurements_path, measurements)
    geo_frame = cast(Any, gpd.GeoDataFrame)
    ranked = geo_frame(
        ranked_rows,
        geometry=[prospects.loc[item["prospect_id"]].geometry for item in ranked_rows],
        crs=prospects.crs,
    )
    ranked = ranked.sort_values(
        ["total_score", "prospect_id"],
        ascending=[False, True],
        kind="stable",
    )
    ranked.insert(1, "rank", range(1, len(ranked) + 1))
    ranked_path = staging / "ranked_prospects.gpkg"
    ranked.to_file(ranked_path, layer="authoritative_prospects", driver="GPKG")
    outputs = (
        _file_identity(staging, measurements_path),
        _file_identity(staging, ranked_path),
    )
    return Phase04AuthoritativeResult.create(
        run_id=run_id,
        phase03_handoff_id=handoff.handoff_id,
        phase03_handoff_file_sha256=sha256_file(handoff_path),
        activation_id=activation.activation_id,
        activation_file_sha256=sha256_file(activation_path),
        prospect_source=_file_identity(prospect_path.parent, prospect_path),
        prospect_layer=prospect_layer,
        scorecard_id=scorecard.scorecard_id,
        scorecard_file_sha256=sha256_file(scorecard_path),
        evidence_manifest_bindings=evidence_bindings(evidence),
        output_artifacts=outputs,
        prospect_count=len(ranked),
        class_counts=tuple((class_id, classes[class_id]) for class_id in ("A", "B", "C", "D")),
        limitations=(
            "Desktop prospect ranking is support for exploration decisions, not proof of mineralization.",
            "Raw spatial measurements remain separate from human score judgments.",
        ),
    )


def _validate_prospects(frame, target_epsg: int) -> None:
    if "prospect_id" not in frame.columns or frame.empty:
        raise Phase04AuthoritativeError("prospect layer requires non-empty prospect_id geometry")
    ids = tuple(str(value).strip() for value in frame["prospect_id"])
    if any(not value for value in ids) or len(set(ids)) != len(ids):
        raise Phase04AuthoritativeError("prospect identities must be non-empty and unique")
    if frame.crs is None or frame.crs.to_epsg() != target_epsg:
        raise Phase04AuthoritativeError("prospect geometry must use the configured target CRS")
    if any(
        geometry is None
        or geometry.is_empty
        or not geometry.is_valid
        or geometry.geom_type not in {"Polygon", "MultiPolygon"}
        for geometry in frame.geometry
    ):
        raise Phase04AuthoritativeError("prospect geometry must be valid non-empty polygons")


def _evidence_frames(
    evidence: tuple[ResolvedEvidence, ...],
    target_epsg: int,
) -> dict[EvidenceRole, Any]:
    import geopandas as gpd
    import pandas as pd

    by_role: dict[EvidenceRole, list[Any]] = {}
    for item in evidence:
        frame = gpd.read_file(item.artifact, layer=item.record.layer_name)
        if frame.crs is None:
            raise Phase04AuthoritativeError(
                f"accepted evidence has no CRS: {item.record.evidence_id}"
            )
        if frame.crs.to_epsg() != target_epsg:
            frame = frame.to_crs(epsg=target_epsg)
        by_role.setdefault(item.record.evidence_role, []).append(frame[["geometry"]])
    geo_frame = cast(Any, gpd.GeoDataFrame)
    concat = cast(Any, pd.concat)
    return {
        role: geo_frame(
            concat(frames, ignore_index=True),
            geometry="geometry",
            crs=f"EPSG:{target_epsg}",
        )
        for role, frames in by_role.items()
    }


def _measure_role(prospect, frame, prefix: str) -> dict[str, object]:
    columns = {
        f"{prefix}_available": False,
        f"{prefix}_feature_count": 0,
        f"{prefix}_overlap_area_m2": 0.0,
        f"{prefix}_overlap_length_m": 0.0,
        f"{prefix}_point_count": 0,
        f"{prefix}_nearest_distance_m": "",
    }
    if frame is None or frame.empty:
        return columns
    geometries = [item for item in frame.geometry if item is not None and not item.is_empty]
    if not geometries:
        return columns
    intersections = [
        item.intersection(prospect) for item in geometries if item.intersects(prospect)
    ]
    columns[f"{prefix}_available"] = True
    columns[f"{prefix}_feature_count"] = len(intersections)
    columns[f"{prefix}_overlap_area_m2"] = float(sum(item.area for item in intersections))
    columns[f"{prefix}_overlap_length_m"] = float(
        sum(item.length for item in intersections if item.geom_type not in {"Point", "MultiPoint"})
    )
    columns[f"{prefix}_point_count"] = sum(
        1
        for geometry in geometries
        if geometry.geom_type in {"Point", "MultiPoint"} and geometry.intersects(prospect)
    )
    columns[f"{prefix}_nearest_distance_m"] = float(
        min(geometry.distance(prospect) for geometry in geometries)
    )
    return columns


def _write_measurements(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise Phase04AuthoritativeError("Phase 04 has no prospect measurements")
    columns = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _class_for_score(score: int) -> Literal["A", "B", "C", "D"]:
    contract = load_phase04_migration_contract()
    for band in contract.class_bands:
        if band.minimum_score <= score <= band.maximum_score:
            return band.class_id
    raise Phase04AuthoritativeError(f"score does not fit the adopted class bands: {score}")


def _json_list(values: tuple[str, ...]) -> str:
    return json.dumps(values, ensure_ascii=False, separators=(",", ":"))


def write_phase04_record(
    record: (
        Phase04ActivationCandidate | Phase04ActivationReview | Phase04Activation | Phase04Scorecard
    ),
    path: Path,
) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = record.model_dump_json(indent=2) + "\n"
    if target.exists():
        if target.read_text(encoding="utf-8") != payload:
            raise Phase04AuthoritativeError("Phase 04 authority record already exists and differs")
        return target
    target.write_text(payload, encoding="utf-8", newline="\n")
    return target


def load_phase04_activation_candidate(path: Path) -> Phase04ActivationCandidate:
    return _load(path, Phase04ActivationCandidate, "Phase 04 activation candidate")


def load_phase04_activation_review(path: Path) -> Phase04ActivationReview:
    return _load(path, Phase04ActivationReview, "Phase 04 activation review")


def load_phase04_activation(path: Path) -> Phase04Activation:
    return _load(path, Phase04Activation, "Phase 04 activation")


def load_phase04_scorecard(path: Path) -> Phase04Scorecard:
    return _load(path, Phase04Scorecard, "Phase 04 scorecard")


def load_phase04_result(path: Path) -> Phase04AuthoritativeResult:
    return _load(path, Phase04AuthoritativeResult, "Phase 04 result")


def verify_phase04_result(
    result: Phase04AuthoritativeResult,
    *,
    result_directory: Path,
    handoff_path: Path,
    activation_path: Path,
    prospect_path: Path,
    scorecard_path: Path,
) -> None:
    if (
        sha256_file(handoff_path) != result.phase03_handoff_file_sha256
        or sha256_file(activation_path) != result.activation_file_sha256
        or sha256_file(prospect_path) != result.prospect_source.sha256
        or prospect_path.stat().st_size != result.prospect_source.size_bytes
        or sha256_file(scorecard_path) != result.scorecard_file_sha256
    ):
        raise Phase04AuthoritativeError("Phase 04 result input identity changed")
    for identity in result.output_artifacts:
        _verify_file(result_directory, identity)


def _file_identity(root: Path, path: Path) -> ExactFileIdentity:
    safe = require_regular_file_under(root, path, description="Phase 04 exact file")
    return ExactFileIdentity(
        path=safe.relative_to(Path(root).absolute().resolve()).as_posix(),
        sha256=sha256_file(safe),
        size_bytes=safe.stat().st_size,
    )


def _verify_file(root: Path, identity: ExactFileIdentity) -> None:
    safe = require_regular_file_under(
        root,
        Path(root) / identity.path,
        description="Phase 04 exact file",
    )
    if safe.stat().st_size != identity.size_bytes or sha256_file(safe) != identity.sha256:
        raise Phase04AuthoritativeError(f"Phase 04 file bytes changed: {identity.path}")


def _load(path: Path, model: type[_StrictModel], description: str):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        return model.model_validate(data)
    except (OSError, UnicodeError, ValueError) as exc:
        raise Phase04AuthoritativeError(f"{description} is invalid") from exc


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result
