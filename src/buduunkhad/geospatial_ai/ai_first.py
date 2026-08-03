"""One-command Phase 03 AI execution attached to an exact sealed pipeline run."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Annotated, Literal, Self, cast

from pydantic import ConfigDict, Field, StringConstraints, field_validator, model_validator

from buduunkhad.ai.contracts import (
    ArtifactSubjectIdentity,
    CanonicalJSONValue,
    FrozenModel,
    NamedJSONValue,
    TaskType,
)
from buduunkhad.ai.fingerprint import sha256_file, sha256_value
from buduunkhad.ai.providers import AIProvider
from buduunkhad.config import AIConfig, ExecutionProfile, ProjectConfig
from buduunkhad.core.run_storage import generate_run_id, resolve_source_phase, validate_run_id
from buduunkhad.geospatial_ai.draft_gpkg import process_validated_response
from buduunkhad.geospatial_ai.execution import execute_request_package
from buduunkhad.geospatial_ai.integrated_review import build_integrated_phase03_review_project
from buduunkhad.geospatial_ai.manifests import RequestPackageManifest, ValidatedResponseRecord
from buduunkhad.geospatial_ai.path_safety import StorageRoots
from buduunkhad.geospatial_ai.phase03_handoff import import_ai_draft_review_package
from buduunkhad.geospatial_ai.qgis_output import write_ai_draft_qgz
from buduunkhad.geospatial_ai.requests import (
    approve_request_package_egress,
    prepare_request_package,
    verify_package_source,
)
from buduunkhad.geospatial_ai.responses import ingest_saved_response
from buduunkhad.geospatial_ai.tiles import TileParameters

PHASE03_AI_FIRST_FORMAT_VERSION = "1.2.0"
PHASE03_AI_FIRST_MANIFEST = "ai-first-manifest.json"

Sha256 = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
NonEmpty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Phase03AIFirstError(RuntimeError):
    """A Phase 03 AI-first session could not complete without weakening its provenance."""


class _StrictModel(FrozenModel):
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


class Phase03AITaskRecord(_StrictModel):
    task_type: Literal["legend_extraction", "geological_feature_proposal", "feature_critique"]
    source_relative_path: NonEmpty
    source_sha256: Sha256
    request_package_path: NonEmpty
    request_fingerprint: Sha256
    response_path: NonEmpty
    response_sha256: Sha256
    validated_response_path: NonEmpty
    validated_response_sha256: Sha256
    response_id: NonEmpty
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)

    @field_validator(
        "source_relative_path",
        "request_package_path",
        "response_path",
        "validated_response_path",
    )
    @classmethod
    def _portable_path(cls, value: str) -> str:
        path = Path(value)
        if path.is_absolute() or "\\" in value or ".." in path.parts:
            raise ValueError("AI-first paths must be portable and relative")
        return path.as_posix()


class _Phase03AIFirstIdentity(_StrictModel):
    format_version: Literal["1.2.0"] = PHASE03_AI_FIRST_FORMAT_VERSION
    pipeline_run_id: NonEmpty
    ai_run_id: NonEmpty
    provider: Literal["openai", "anthropic"]
    model: NonEmpty
    reasoning_effort: NonEmpty | None
    reasoning_mode: NonEmpty | None
    text_verbosity: NonEmpty | None
    store_response: bool | None
    approved_by: NonEmpty
    approval_note: NonEmpty
    created_at: datetime
    tasks: tuple[Phase03AITaskRecord, Phase03AITaskRecord, Phase03AITaskRecord]
    draft_gpkg_path: NonEmpty
    draft_gpkg_sha256: Sha256
    draft_qgz_path: NonEmpty
    draft_qgz_sha256: Sha256
    review_package_path: NonEmpty
    review_package_id: Sha256
    integrated_project_path: NonEmpty
    integrated_project_sha256: Sha256

    @field_validator("created_at")
    @classmethod
    def _aware_time(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("AI-first creation time must be timezone-aware")
        return value

    @field_validator(
        "draft_gpkg_path",
        "draft_qgz_path",
        "review_package_path",
        "integrated_project_path",
    )
    @classmethod
    def _portable_output_path(cls, value: str) -> str:
        path = Path(value)
        if path.is_absolute() or "\\" in value or ".." in path.parts:
            raise ValueError("AI-first output paths must be portable and relative")
        return path.as_posix()

    @model_validator(mode="after")
    def _exact_tasks(self) -> _Phase03AIFirstIdentity:
        validate_run_id(self.pipeline_run_id)
        validate_run_id(self.ai_run_id)
        if self.pipeline_run_id == self.ai_run_id:
            raise ValueError("AI execution requires a distinct retry-safe attempt identity")
        if tuple(item.task_type for item in self.tasks) != (
            TaskType.LEGEND_EXTRACTION.value,
            TaskType.GEOLOGICAL_FEATURE_PROPOSAL.value,
            TaskType.FEATURE_CRITIQUE.value,
        ):
            raise ValueError(
                "AI-first Phase 03 requires legend extraction, feature proposal, then critique"
            )
        return self


class Phase03AIFirstManifest(_Phase03AIFirstIdentity):
    session_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> Phase03AIFirstManifest:
        identity = _Phase03AIFirstIdentity.model_validate(
            self.model_dump(mode="python", exclude={"session_id"})
        )
        if self.session_id != sha256_value(identity):
            raise ValueError("AI-first Phase 03 session identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> Phase03AIFirstManifest:
        identity = _Phase03AIFirstIdentity.model_validate(values)
        return cls(**identity.model_dump(mode="python"), session_id=sha256_value(identity))


def _execute_task(
    *,
    source: Path,
    snapshot_root: Path,
    roots: StorageRoots,
    ai_run_id: str,
    ai: AIConfig,
    target_crs: str,
    task_type: TaskType,
    tile_parameters: TileParameters,
    estimated_cost: Decimal,
    approved_by: str,
    approval_note: str,
    provider: AIProvider | None,
    context_parameters: tuple[NamedJSONValue, ...] = (),
    subject: ArtifactSubjectIdentity | None = None,
) -> tuple[
    Phase03AITaskRecord,
    Path,
    RequestPackageManifest,
    Path,
    ValidatedResponseRecord,
]:
    package_directory, package = prepare_request_package(
        source,
        roots=roots,
        run_id=ai_run_id,
        task_type=task_type,
        target_crs=target_crs,
        provider=ai.provider.value,
        model=ai.provider_model,
        reasoning_effort=(ai.reasoning_effort.value if ai.reasoning_effort is not None else None),
        reasoning_mode=(ai.reasoning_mode.value if ai.reasoning_mode is not None else None),
        text_verbosity=(ai.text_verbosity.value if ai.text_verbosity is not None else None),
        store_response=ai.store_responses,
        context_parameters=context_parameters,
        tile_parameters=tile_parameters,
        estimated_cost_usd=estimated_cost,
        phase_id="03",
        subject=subject,
    )
    approve_request_package_egress(
        package_directory,
        roots=roots,
        approved_by=approved_by.strip(),
        note=approval_note.strip(),
    )
    response_path = execute_request_package(
        package_directory,
        config=ai,
        roots=roots,
        provider=provider,
    )
    validated_path, validated = ingest_saved_response(
        package_directory,
        response_path,
        roots=roots,
    )
    task_name = cast(
        Literal["legend_extraction", "geological_feature_proposal", "feature_critique"],
        task_type.value,
    )
    record = Phase03AITaskRecord(
        task_type=task_name,
        source_relative_path=source.relative_to(snapshot_root).as_posix(),
        source_sha256=package.source.sha256,
        request_package_path=package_directory.relative_to(
            roots.run_directory(ai_run_id)
        ).as_posix(),
        request_fingerprint=package.request_fingerprint,
        response_path=response_path.relative_to(roots.run_directory(ai_run_id)).as_posix(),
        response_sha256=sha256_file(response_path),
        validated_response_path=validated_path.relative_to(
            roots.run_directory(ai_run_id)
        ).as_posix(),
        validated_response_sha256=sha256_file(validated_path),
        response_id=validated.response_id,
        input_tokens=validated.usage.input_tokens,
        output_tokens=validated.usage.output_tokens,
    )
    return record, package_directory, package, validated_path, validated


def run_phase03_ai_first(
    config: ProjectConfig,
    *,
    pipeline_run_id: str,
    approved_by: str,
    approval_note: str,
    ai_run_id: str | None = None,
    provider: AIProvider | None = None,
) -> tuple[Path, Phase03AIFirstManifest]:
    """Execute the configured legend and feature tasks and build one review workspace."""

    ai = config.ai
    workflow = ai.phase03_workflow
    if not ai.enabled or ai.profile is not ExecutionProfile.AI_FIRST:
        raise Phase03AIFirstError("project configuration does not enable AI-first execution")
    if workflow is None:
        raise Phase03AIFirstError("AI-first Phase 03 sources are not configured")
    if not approved_by.strip() or not approval_note.strip():
        raise Phase03AIFirstError("AI-first execution requires a named egress approver and note")

    roots = StorageRoots.from_environment(
        raw_root=config.raw_root, project_root=config.project_root
    )
    pipeline_run_id = validate_run_id(pipeline_run_id)
    ai_run_id = validate_run_id(ai_run_id or generate_run_id())
    if pipeline_run_id == ai_run_id:
        raise Phase03AIFirstError("AI attempt ID must differ from the pipeline run ID")
    pipeline_run_directory = roots.run_directory(pipeline_run_id)
    ai_run_directory = roots.run_directory(ai_run_id)
    phase03 = resolve_source_phase(
        config.runs_root,
        "03",
        pipeline_run_id,
        require_advance=False,
        require_qaqc_passed=True,
    )
    existing_evidence = _phase03_evidence_path(
        phase03,
        run_directory=pipeline_run_directory,
    )
    snapshot_root = roots.require_snapshot_root()
    legend_source = roots.assert_snapshot_source(snapshot_root / workflow.legend_source)
    feature_source_path = roots.assert_snapshot_source(snapshot_root / workflow.feature_source)
    legend_tiles = TileParameters(
        width=workflow.legend_tile_size,
        height=workflow.legend_tile_size,
        overlap=workflow.legend_overlap,
    )
    feature_tiles = TileParameters(
        width=workflow.feature_tile_size,
        height=workflow.feature_tile_size,
        overlap=workflow.feature_overlap,
    )

    (
        legend_record,
        _legend_directory,
        _legend_package,
        legend_validated_path,
        legend_validated,
    ) = _execute_task(
        source=legend_source,
        snapshot_root=snapshot_root,
        roots=roots,
        ai_run_id=ai_run_id,
        ai=ai,
        target_crs=config.crs.target_authority,
        task_type=TaskType.LEGEND_EXTRACTION,
        tile_parameters=legend_tiles,
        estimated_cost=workflow.legend_estimated_cost_usd,
        approved_by=approved_by,
        approval_note=approval_note,
        provider=provider,
    )
    legend_context = NamedJSONValue(
        name="validated_legend",
        value=CanonicalJSONValue.from_value(
            {
                "request_fingerprint": legend_validated.request_fingerprint,
                "validated_response_sha256": sha256_file(legend_validated_path),
                "payload": legend_validated.payload.to_python(),
            }
        ),
    )
    (
        feature_record,
        feature_package_directory,
        feature_package,
        feature_validated_path,
        feature_validated,
    ) = _execute_task(
        source=feature_source_path,
        snapshot_root=snapshot_root,
        roots=roots,
        ai_run_id=ai_run_id,
        ai=ai,
        target_crs=config.crs.target_authority,
        task_type=TaskType.GEOLOGICAL_FEATURE_PROPOSAL,
        tile_parameters=feature_tiles,
        estimated_cost=workflow.feature_estimated_cost_usd,
        approved_by=approved_by,
        approval_note=approval_note,
        provider=provider,
        context_parameters=(legend_context,),
    )
    feature_subject = ArtifactSubjectIdentity(
        artifact_id=f"feature-proposals-{feature_validated.request_fingerprint[:24]}",
        artifact_version=1,
        content_sha256=sha256_file(feature_validated_path),
        generator_job_id=feature_validated.job_id,
    )
    proposal_context = NamedJSONValue(
        name="validated_feature_proposals",
        value=CanonicalJSONValue.from_value(
            {
                "request_fingerprint": feature_validated.request_fingerprint,
                "validated_response_sha256": sha256_file(feature_validated_path),
                "payload": feature_validated.payload.to_python(),
            }
        ),
    )
    (
        critique_record,
        _critique_directory,
        _critique_package,
        _critique_path,
        _critique_validated,
    ) = _execute_task(
        source=feature_source_path,
        snapshot_root=snapshot_root,
        roots=roots,
        ai_run_id=ai_run_id,
        ai=ai,
        target_crs=config.crs.target_authority,
        task_type=TaskType.FEATURE_CRITIQUE,
        tile_parameters=feature_tiles,
        estimated_cost=workflow.critique_estimated_cost_usd,
        approved_by=approved_by,
        approval_note=approval_note,
        provider=provider,
        context_parameters=(proposal_context,),
        subject=feature_subject,
    )
    task_records = (legend_record, feature_record, critique_record)
    draft_gpkg = process_validated_response(
        feature_package_directory,
        feature_validated_path,
        roots=roots,
        expected_target_crs=config.crs.target_authority,
    )
    feature_source = verify_package_source(feature_package, roots=roots)
    draft_qgz = write_ai_draft_qgz(
        draft_gpkg.with_suffix(".qgz"),
        gpkg=draft_gpkg,
        source_raster=feature_source,
        epsg=config.target_epsg,
        roots=roots,
        run_id=ai_run_id,
    )
    review_package = (
        ai_run_directory / "phase03-review" / f"ai-first-{sha256_file(feature_source)[:16]}"
    )
    review_manifest = import_ai_draft_review_package(
        draft_gpkg,
        review_package,
        roots=roots,
        run_id=ai_run_id,
        expected_target_crs=config.crs.target_authority,
        existing_evidence=existing_evidence,
    )
    integrated_project = (
        ai_run_directory / "phase03-review" / "Buduunkhad_Integrated_Phase03_Review.qgz"
    )
    build_integrated_phase03_review_project(
        runs_root=config.runs_root,
        pipeline_run_id=pipeline_run_id,
        ai_run_id=ai_run_id,
        review_packages=(review_package,),
        output=integrated_project,
        roots=roots,
        target_epsg=config.target_epsg,
    )
    manifest = Phase03AIFirstManifest.create(
        pipeline_run_id=pipeline_run_id,
        ai_run_id=ai_run_id,
        provider=ai.provider.value,
        model=ai.provider_model,
        reasoning_effort=ai.reasoning_effort.value if ai.reasoning_effort is not None else None,
        reasoning_mode=ai.reasoning_mode.value if ai.reasoning_mode is not None else None,
        text_verbosity=ai.text_verbosity.value if ai.text_verbosity is not None else None,
        store_response=ai.store_responses,
        approved_by=approved_by.strip(),
        approval_note=approval_note.strip(),
        created_at=datetime.now(UTC),
        tasks=tuple(task_records),
        draft_gpkg_path=draft_gpkg.relative_to(ai_run_directory).as_posix(),
        draft_gpkg_sha256=sha256_file(draft_gpkg),
        draft_qgz_path=draft_qgz.relative_to(ai_run_directory).as_posix(),
        draft_qgz_sha256=sha256_file(draft_qgz),
        review_package_path=review_package.relative_to(ai_run_directory).as_posix(),
        review_package_id=review_manifest.package_id,
        integrated_project_path=integrated_project.relative_to(ai_run_directory).as_posix(),
        integrated_project_sha256=sha256_file(integrated_project),
    )
    destination = roots.assert_writable(
        ai_run_directory / "ai" / "phases" / "03" / PHASE03_AI_FIRST_MANIFEST,
        run_id=ai_run_id,
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise Phase03AIFirstError("AI-first Phase 03 manifest already exists")
    destination.write_text(
        manifest.model_dump_json(indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return destination, manifest


def load_phase03_ai_first_manifest(
    path: Path,
    *,
    roots: StorageRoots,
) -> Phase03AIFirstManifest:
    try:
        safe = roots.assert_run_artifact(path)
        data = json.loads(safe.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        manifest = Phase03AIFirstManifest.model_validate(data)
        run_directory = roots.run_directory(manifest.ai_run_id)
        _verify_manifest_files(manifest, run_directory=run_directory)
    except (OSError, UnicodeError, ValueError) as exc:
        raise Phase03AIFirstError("AI-first Phase 03 manifest is invalid") from exc
    return manifest


def _phase03_evidence_path(phase03, *, run_directory: Path) -> Path:
    matches = [
        run_directory / artifact.path
        for artifact in phase03.output_artifacts
        if Path(artifact.path).name.endswith("Geological_Evidence_Layers_v01.gpkg")
    ]
    if len(matches) != 1 or not matches[0].is_file():
        raise Phase03AIFirstError("sealed Phase 03 evidence GeoPackage is unavailable or ambiguous")
    return matches[0]


def _verify_manifest_files(manifest: Phase03AIFirstManifest, *, run_directory: Path) -> None:
    expected = {
        manifest.draft_gpkg_path: manifest.draft_gpkg_sha256,
        manifest.draft_qgz_path: manifest.draft_qgz_sha256,
        manifest.integrated_project_path: manifest.integrated_project_sha256,
    }
    for task in manifest.tasks:
        expected[task.response_path] = task.response_sha256
        expected[task.validated_response_path] = task.validated_response_sha256
    for relative, digest in expected.items():
        path = (run_directory / relative).resolve(strict=True)
        if not path.is_relative_to(run_directory.resolve()) or sha256_file(path) != digest:
            raise Phase03AIFirstError("AI-first Phase 03 artifact bytes changed")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result
