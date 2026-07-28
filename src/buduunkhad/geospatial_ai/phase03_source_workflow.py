"""Source-level Phase 03 request preparation and deterministic overlap review."""

from __future__ import annotations

import json
from decimal import Decimal
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

from buduunkhad.ai.contracts import TaskType
from buduunkhad.ai.fingerprint import sha256_file, sha256_value
from buduunkhad.geospatial_ai.path_safety import StorageRoots
from buduunkhad.geospatial_ai.requests import (
    PreparedProvider,
    PreparedReasoningEffort,
    load_request_package,
    prepare_request_package,
)
from buduunkhad.geospatial_ai.stitching import (
    OverlapReviewCandidate,
    OverlapReviewPair,
    review_candidate_overlaps,
)
from buduunkhad.geospatial_ai.tiles import TileParameters

PHASE03_SOURCE_WORKFLOW_FORMAT_VERSION = "1.0.0"
PHASE03_OVERLAP_REVIEW_FORMAT_VERSION = "1.0.0"

Sha256 = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
NonEmpty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Phase03SourceWorkflowError(RuntimeError):
    """A source workflow or overlap report cannot be trusted."""


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


class SourceTaskBinding(_StrictModel):
    task_type: Literal["legend_extraction", "geological_feature_proposal"]
    package_path: str
    package_manifest_sha256: Sha256
    request_fingerprint: Sha256

    @field_validator("package_path")
    @classmethod
    def _portable_path(cls, value: str) -> str:
        path = Path(value)
        if path.is_absolute() or "\\" in value or ".." in path.parts:
            raise ValueError("source-workflow package paths must be portable and relative")
        return value


class _Phase03SourceWorkflowIdentity(_StrictModel):
    format_version: Literal["1.0.0"] = PHASE03_SOURCE_WORKFLOW_FORMAT_VERSION
    run_id: NonEmpty
    source_asset_id: NonEmpty
    source_sha256: Sha256
    source_target_crs: NonEmpty
    tasks: tuple[SourceTaskBinding, SourceTaskBinding]
    limitations: tuple[NonEmpty, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _exact_tasks(self) -> _Phase03SourceWorkflowIdentity:
        if tuple(item.task_type for item in self.tasks) != (
            TaskType.LEGEND_EXTRACTION.value,
            TaskType.GEOLOGICAL_FEATURE_PROPOSAL.value,
        ):
            raise ValueError("Phase 03 source workflow requires legend then feature proposal")
        if tuple(sorted(set(self.limitations))) != self.limitations:
            raise ValueError("source-workflow limitations must be unique and ordered")
        return self


class Phase03SourceWorkflowManifest(_Phase03SourceWorkflowIdentity):
    workflow_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> Phase03SourceWorkflowManifest:
        identity = _Phase03SourceWorkflowIdentity.model_validate(
            self.model_dump(mode="python", exclude={"workflow_id"})
        )
        if self.workflow_id != sha256_value(identity):
            raise ValueError("Phase 03 source workflow identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> Phase03SourceWorkflowManifest:
        identity = _Phase03SourceWorkflowIdentity.model_validate(values)
        return cls(**identity.model_dump(mode="python"), workflow_id=sha256_value(identity))


class OverlapPairRecord(_StrictModel):
    left_feature_id: NonEmpty
    right_feature_id: NonEmpty
    reason: NonEmpty
    overlap_ratio: float = Field(ge=0, le=1)
    endpoint_distance: float | None = Field(default=None, ge=0)

    @classmethod
    def from_pair(cls, pair: OverlapReviewPair) -> OverlapPairRecord:
        return cls(
            left_feature_id=pair.left_feature_id,
            right_feature_id=pair.right_feature_id,
            reason=pair.reason,
            overlap_ratio=pair.overlap_ratio,
            endpoint_distance=pair.endpoint_distance,
        )


class _Phase03OverlapReviewIdentity(_StrictModel):
    format_version: Literal["1.0.0"] = PHASE03_OVERLAP_REVIEW_FORMAT_VERSION
    run_id: NonEmpty
    draft_path: str
    draft_sha256: Sha256
    draft_size_bytes: int = Field(ge=0)
    inspected_layers: tuple[NonEmpty, ...]
    duplicate_pairs: tuple[OverlapPairRecord, ...] = ()
    conflict_pairs: tuple[OverlapPairRecord, ...] = ()
    continuity_pairs: tuple[OverlapPairRecord, ...] = ()
    review_required: bool
    limitations: tuple[NonEmpty, ...] = Field(min_length=1)

    @field_validator("draft_path")
    @classmethod
    def _portable_path(cls, value: str) -> str:
        path = Path(value)
        if path.is_absolute() or "\\" in value or ".." in path.parts:
            raise ValueError("overlap-review draft path must be portable and relative")
        return value

    @model_validator(mode="after")
    def _coherent_result(self) -> _Phase03OverlapReviewIdentity:
        if tuple(sorted(set(self.inspected_layers))) != self.inspected_layers:
            raise ValueError("overlap-review layers must be unique and ordered")
        expected = bool(self.duplicate_pairs or self.conflict_pairs or self.continuity_pairs)
        if self.review_required != expected:
            raise ValueError("overlap-review required status is inconsistent")
        if tuple(sorted(set(self.limitations))) != self.limitations:
            raise ValueError("overlap-review limitations must be unique and ordered")
        return self


class Phase03OverlapReviewReport(_Phase03OverlapReviewIdentity):
    report_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> Phase03OverlapReviewReport:
        identity = _Phase03OverlapReviewIdentity.model_validate(
            self.model_dump(mode="python", exclude={"report_id"})
        )
        if self.report_id != sha256_value(identity):
            raise ValueError("Phase 03 overlap-review identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> Phase03OverlapReviewReport:
        identity = _Phase03OverlapReviewIdentity.model_validate(values)
        return cls(**identity.model_dump(mode="python"), report_id=sha256_value(identity))


def prepare_phase03_source_workflow(
    source: Path,
    *,
    roots: StorageRoots,
    run_id: str,
    target_crs: str,
    provider: PreparedProvider = "disabled",
    model: str | None = None,
    reasoning_effort: PreparedReasoningEffort | None = None,
    tile_parameters: TileParameters | None = None,
    estimated_cost_usd: Decimal = Decimal("0"),
    page_number: int = 1,
    render_scale: float = 1.0,
) -> tuple[Path, Phase03SourceWorkflowManifest]:
    """Prepare the two existing inspectable request packages needed for one source map."""

    run_directory = roots.run_directory(run_id, create=True)
    bindings: list[SourceTaskBinding] = []
    packages = []
    for task in (TaskType.LEGEND_EXTRACTION, TaskType.GEOLOGICAL_FEATURE_PROPOSAL):
        directory, package = prepare_request_package(
            source,
            roots=roots,
            run_id=run_id,
            task_type=task,
            target_crs=target_crs,
            provider=provider,
            model=model,
            reasoning_effort=reasoning_effort,
            tile_parameters=tile_parameters,
            estimated_cost_usd=estimated_cost_usd,
            page_number=page_number,
            render_scale=render_scale,
        )
        packages.append(package)
        bindings.append(
            SourceTaskBinding(
                task_type=task.value,
                package_path=directory.relative_to(run_directory).as_posix(),
                package_manifest_sha256=sha256_file(directory / "request-package.json"),
                request_fingerprint=package.request_fingerprint,
            )
        )
    first, second = packages
    if first.source != second.source:
        raise Phase03SourceWorkflowError("source workflow task packages do not bind one source")
    manifest = Phase03SourceWorkflowManifest.create(
        run_id=run_id,
        source_asset_id=first.source.asset_id,
        source_sha256=first.source.sha256,
        source_target_crs=first.source.target_crs,
        tasks=tuple(bindings),
        limitations=tuple(
            sorted(
                (
                    "Prepared requests are proposals only and require separate egress approval before execution.",
                    "Human review and evidence-manifest promotion remain separate operations.",
                )
            )
        ),
    )
    path = run_directory / "phase03-sources" / f"{first.source.sha256}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(manifest.model_dump_json(indent=2) + "\n", encoding="utf-8", newline="\n")
    return path, manifest


def load_phase03_source_workflow(
    path: Path,
    *,
    roots: StorageRoots,
) -> Phase03SourceWorkflowManifest:
    try:
        safe = roots.assert_run_artifact(path)
        data = json.loads(safe.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        manifest = Phase03SourceWorkflowManifest.model_validate(data)
        run_directory = roots.run_directory(manifest.run_id)
        for binding in manifest.tasks:
            package_directory = roots.assert_run_artifact(
                run_directory / binding.package_path,
                run_id=manifest.run_id,
            )
            package_file = package_directory / "request-package.json"
            if sha256_file(package_file) != binding.package_manifest_sha256:
                raise Phase03SourceWorkflowError("source-workflow package bytes changed")
            package = load_request_package(package_directory)
            if (
                package.request_fingerprint != binding.request_fingerprint
                or package.source.asset_id != manifest.source_asset_id
                or package.source.sha256 != manifest.source_sha256
            ):
                raise Phase03SourceWorkflowError("source-workflow package identity changed")
        return manifest
    except (OSError, UnicodeError, ValueError) as exc:
        if isinstance(exc, Phase03SourceWorkflowError):
            raise
        raise Phase03SourceWorkflowError("Phase 03 source workflow is invalid") from exc


def review_phase03_draft_overlaps(
    draft: Path,
    *,
    roots: StorageRoots,
    run_id: str,
    output: Path,
    duplicate_overlap_threshold: float = 0.8,
    conflict_overlap_threshold: float = 0.2,
    continuity_tolerance: float = 0.0,
) -> Phase03OverlapReviewReport:
    """Inspect cross-tile relationships and report ambiguity without modifying geometry."""

    import geopandas as gpd

    safe = roots.assert_run_artifact(draft, run_id=run_id)
    run_directory = roots.run_directory(run_id)
    output_path = roots.assert_writable(output, run_id=run_id)
    layers = tuple(sorted(name for name in fiona.listlayers(safe) if name != "validation_findings"))
    candidates: list[OverlapReviewCandidate] = []
    for layer in layers:
        frame = gpd.read_file(safe, layer=layer)
        for _, row in frame.iterrows():
            feature_id = str(row.get("feature_id", "")).strip()
            if not feature_id:
                raise Phase03SourceWorkflowError("draft feature has no stable feature_id")
            tile_ids_value = row.get("tile_ids", "[]")
            tile_ids_data = json.loads(str(tile_ids_value))
            if not isinstance(tile_ids_data, list) or not all(
                isinstance(item, str) and item for item in tile_ids_data
            ):
                raise Phase03SourceWorkflowError("draft feature tile_ids are invalid")
            tile_ids = tuple(sorted({str(item) for item in tile_ids_data}))
            candidates.append(
                OverlapReviewCandidate(
                    feature_id=feature_id,
                    layer_name=layer,
                    legend_code=str(row.get("legend_code", "")).strip(),
                    tile_ids=tile_ids,
                    confidence=float(row.get("confidence", 0.0)),
                    geometry=row.geometry,
                )
            )
    result = review_candidate_overlaps(
        tuple(candidates),
        duplicate_overlap_threshold=duplicate_overlap_threshold,
        conflict_overlap_threshold=conflict_overlap_threshold,
        continuity_tolerance=continuity_tolerance,
    )
    report = Phase03OverlapReviewReport.create(
        run_id=run_id,
        draft_path=safe.relative_to(run_directory).as_posix(),
        draft_sha256=sha256_file(safe),
        draft_size_bytes=safe.stat().st_size,
        inspected_layers=layers,
        duplicate_pairs=tuple(OverlapPairRecord.from_pair(item) for item in result.duplicate_pairs),
        conflict_pairs=tuple(OverlapPairRecord.from_pair(item) for item in result.conflict_pairs),
        continuity_pairs=tuple(
            OverlapPairRecord.from_pair(item) for item in result.continuity_pairs
        ),
        review_required=bool(
            result.duplicate_pairs or result.conflict_pairs or result.continuity_pairs
        ),
        limitations=tuple(
            sorted(
                (
                    "No proposal geometry was stitched, deleted, or reclassified automatically.",
                    "Reported relationships require human resolution in the Phase 03 review package.",
                )
            )
        ),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        existing = load_phase03_overlap_review(output_path, roots=roots, run_id=run_id)
        if existing != report:
            raise Phase03SourceWorkflowError("overlap-review output already exists and differs")
        return existing
    output_path.write_text(report.model_dump_json(indent=2) + "\n", encoding="utf-8", newline="\n")
    return report


def load_phase03_overlap_review(
    path: Path,
    *,
    roots: StorageRoots,
    run_id: str,
) -> Phase03OverlapReviewReport:
    """Load one report and revalidate the exact draft bytes it inspected."""

    try:
        safe = roots.assert_run_artifact(path, run_id=run_id)
        data = json.loads(safe.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        report = Phase03OverlapReviewReport.model_validate(data)
        if report.run_id != run_id:
            raise Phase03SourceWorkflowError("overlap review belongs to a different run")
        run_directory = roots.run_directory(run_id)
        draft = roots.assert_run_artifact(
            run_directory / report.draft_path,
            run_id=run_id,
        )
        if draft.stat().st_size != report.draft_size_bytes or sha256_file(draft) != (
            report.draft_sha256
        ):
            raise Phase03SourceWorkflowError("overlap-review draft bytes changed")
        return report
    except (OSError, UnicodeError, ValueError) as exc:
        raise Phase03SourceWorkflowError("Phase 03 overlap review is invalid") from exc


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result
