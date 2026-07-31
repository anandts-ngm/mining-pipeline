"""Atomic, human-facing results assembled from one exact sealed pipeline run."""

from __future__ import annotations

import json
import os
import shutil
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Annotated, Literal, Self, cast

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from buduunkhad.ai.fingerprint import sha256_file, sha256_value
from buduunkhad.core.execution_policy import ExecutionMode
from buduunkhad.core.qgis_project import copy_qgz_rebased
from buduunkhad.core.run_artifacts import (
    ArtifactSealError,
    canonical_relative_path,
    has_symlink_component,
    require_regular_file_under,
)
from buduunkhad.core.run_storage import (
    RUN_LAYOUT_VERSION,
    SUPPORTED_RUN_MANIFEST_FORMAT_VERSIONS,
    ResolvedSourcePhase,
    RunStorageError,
    resolve_source_phase,
    validate_run_id,
)

RESULTS_VIEW_FORMAT_VERSION = "1.1.0"
RESULTS_SUMMARY_NAME = "run-summary.json"
RESULTS_LATEST_NAME = "latest"
RESULTS_PHASE_DIRS = {
    "00": "00_inventory",
    "01": "01_master_gis",
    "02": "02_remote_sensing",
    "03": "03_geology",
    "04": "04_prospects",
}
_DATA_SUFFIXES = frozenset({".gpkg", ".tif"})
_PROJECT_SUFFIXES = frozenset({".qgz"})

Sha256 = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
NonEmpty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class ResultsViewError(RuntimeError):
    """A curated results view cannot be assembled without losing provenance."""


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


class ResultsFile(_StrictModel):
    phase_id: str | None
    origin: Literal["pipeline-output", "review-package", "integrated-project"]
    path: str
    sha256: Sha256
    size_bytes: int = Field(ge=0)
    source_path: NonEmpty
    source_sha256: Sha256
    source_size_bytes: int = Field(ge=0)
    transformation: Literal["qgz-rebase-v1"] | None = None

    @field_validator("phase_id")
    @classmethod
    def _known_phase(cls, value: str | None) -> str | None:
        if value is not None and value not in RESULTS_PHASE_DIRS:
            raise ValueError("results file phase is outside Phase 00-04")
        return value

    @field_validator("path", "source_path")
    @classmethod
    def _portable_path(cls, value: str) -> str:
        return canonical_relative_path(value)

    @model_validator(mode="after")
    def _coherent_origin(self) -> ResultsFile:
        if (self.phase_id is None) != (self.origin == "integrated-project"):
            raise ValueError("only the integrated project may omit a phase identity")
        return self


class ResultsPhase(_StrictModel):
    phase_id: str
    source_run_id: NonEmpty
    execution_mode: ExecutionMode
    gate_status: Literal["go", "no-go", "blocked"]
    gate_provisional: bool
    human_review_or_qaqc_pending: bool
    output_count: int = Field(ge=1)

    @field_validator("phase_id")
    @classmethod
    def _known_phase(cls, value: str) -> str:
        if value not in RESULTS_PHASE_DIRS:
            raise ValueError("results phase is outside Phase 00-04")
        return value


class _ResultsViewIdentity(_StrictModel):
    format_version: Literal["1.1.0"] = RESULTS_VIEW_FORMAT_VERSION
    project_name: NonEmpty
    source_run_id: NonEmpty
    source_run_manifest_sha256: Sha256
    source_finished_at: datetime
    phases: tuple[ResultsPhase, ...] = Field(min_length=1)
    files: tuple[ResultsFile, ...] = Field(min_length=1)
    review_project_source_sha256: Sha256 | None = None
    review_package_ids: tuple[Sha256, ...] = ()

    @model_validator(mode="after")
    def _coherent_view(self) -> _ResultsViewIdentity:
        validate_run_id(self.source_run_id)
        if self.source_finished_at.tzinfo is None or self.source_finished_at.utcoffset() is None:
            raise ValueError("results source completion time must be timezone-aware")
        phase_ids = tuple(item.phase_id for item in self.phases)
        if phase_ids != tuple(sorted(set(phase_ids))):
            raise ValueError("results phases must be unique and ordered")
        paths = tuple(item.path for item in self.files)
        if paths != tuple(sorted(set(paths))):
            raise ValueError("results file paths must be unique and ordered")
        counts = {
            phase.phase_id: sum(file.phase_id == phase.phase_id for file in self.files)
            for phase in self.phases
        }
        if any(phase.output_count != counts[phase.phase_id] for phase in self.phases):
            raise ValueError("results phase output count is inconsistent")
        has_review = any(file.phase_id is None for file in self.files)
        if has_review != (self.review_project_source_sha256 is not None):
            raise ValueError("results review-project identity is incomplete")
        if self.review_package_ids != tuple(sorted(set(self.review_package_ids))):
            raise ValueError("results review-package identities must be unique and ordered")
        has_package_files = any(file.origin == "review-package" for file in self.files)
        if has_package_files != bool(self.review_package_ids):
            raise ValueError("results review-package inventory is incomplete")
        return self


class ResultsViewManifest(_ResultsViewIdentity):
    view_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> ResultsViewManifest:
        identity = _ResultsViewIdentity.model_validate(
            self.model_dump(mode="python", exclude={"view_id"})
        )
        if self.view_id != sha256_value(identity):
            raise ValueError("results view identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> ResultsViewManifest:
        identity = _ResultsViewIdentity.model_validate(values)
        return cls(**identity.model_dump(mode="python"), view_id=sha256_value(identity))


class ResultsViewResult(_StrictModel):
    root: Path
    manifest: ResultsViewManifest
    created: bool


def verify_results_view(root: Path) -> ResultsViewManifest:
    """Revalidate one complete curated-results tree and return its sealed identity."""

    resolved = _resolved_root(root, "curated results view")
    manifest = _load_results_manifest(resolved / RESULTS_SUMMARY_NAME)
    _verify_view(resolved, manifest)
    return manifest


@dataclass(frozen=True)
class _PlannedResult:
    source: Path
    destination: Path
    phase_id: str
    source_path: str
    origin: Literal["pipeline-output", "review-package"]


def materialize_results_view(
    *,
    project_name: str,
    raw_root: Path,
    output_root: Path,
    runs_root: Path,
    results_root: Path,
    run_id: str,
    snapshot_root: Path | None = None,
    review_project: Path | None = None,
    review_packages: tuple[Path, ...] = (),
) -> ResultsViewResult:
    """Create or verify ``results/latest`` from declared outputs of one sealed run."""

    run_id = validate_run_id(run_id)
    raw = _resolved_root(raw_root, "raw root")
    output = _resolved_root(
        output_root,
        "compatibility output root",
        require_existing=False,
    )
    runs = _resolved_root(runs_root, "runs root")
    results = _resolved_root(results_root, "results root", require_existing=False)
    _reject_overlap(
        ("raw root", raw),
        ("compatibility output root", output),
        ("runs root", runs),
        ("results root", results),
    )
    results.mkdir(parents=True, exist_ok=True)
    manifest_path = runs / run_id / "run_manifest.json"
    data = _load_run_manifest(manifest_path, run_id=run_id)
    completed = _completed_phase_ids(data)
    if not completed:
        raise ResultsViewError("source run has no complete Phase 00-04 outputs")

    resolved = tuple(
        resolve_source_phase(
            runs,
            phase_id,
            run_id,
            require_advance=False,
            require_qaqc_passed=True,
        )
        for phase_id in completed
    )
    latest = results / RESULTS_LATEST_NAME
    staging = results / f".{RESULTS_LATEST_NAME}-staging-{uuid.uuid4().hex}"
    backup = results / f".{RESULTS_LATEST_NAME}-previous-{uuid.uuid4().hex}"
    staging.mkdir()
    try:
        plans = list(_artifact_targets(resolved, runs_root=runs, staging=staging))
        package_plans, review_package_ids = _review_package_targets(
            review_packages,
            raw_root=raw,
            runs_root=runs,
            snapshot_root=snapshot_root,
            staging=staging,
        )
        plans.extend(package_plans)
        source_targets = _validate_plans(plans, staging=staging)
        files = _copy_artifacts(plans, staging=staging, source_targets=source_targets)
        review_digest: str | None = None
        if review_project is not None:
            review = _review_project_source(review_project, runs_root=runs)
            review_digest = sha256_file(review)
            destination = staging / "Buduunkhad.qgz"
            copy_qgz_rebased(
                review,
                destination,
                copied_sources=source_targets,
                require_mapped_sources=True,
            )
            if sha256_file(review) != review_digest:
                raise ResultsViewError("integrated review project changed while copying")
            files.append(
                ResultsFile(
                    phase_id=None,
                    origin="integrated-project",
                    path=destination.relative_to(staging).as_posix(),
                    sha256=sha256_file(destination),
                    size_bytes=destination.stat().st_size,
                    source_path=review.relative_to(runs).as_posix(),
                    source_sha256=review_digest,
                    source_size_bytes=review.stat().st_size,
                    transformation="qgz-rebase-v1",
                )
            )
        phase_records = tuple(
            ResultsPhase(
                phase_id=phase.binding.phase_id,
                source_run_id=run_id,
                execution_mode=phase.execution_mode,
                gate_status=cast(
                    Literal["go", "no-go", "blocked"],
                    phase.gate_status,
                ),
                gate_provisional=phase.gate_provisional,
                human_review_or_qaqc_pending=_phase_pending(data, phase.binding.phase_id),
                output_count=sum(item.phase_id == phase.binding.phase_id for item in files),
            )
            for phase in resolved
        )
        manifest = ResultsViewManifest.create(
            project_name=project_name,
            source_run_id=run_id,
            source_run_manifest_sha256=sha256_file(manifest_path),
            source_finished_at=_finished_at(data),
            phases=phase_records,
            files=tuple(sorted(files, key=lambda item: item.path)),
            review_project_source_sha256=review_digest,
            review_package_ids=review_package_ids,
        )
        (staging / RESULTS_SUMMARY_NAME).write_text(
            manifest.model_dump_json(indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        _verify_view(staging, manifest)
        if latest.exists():
            existing = _load_results_manifest(latest / RESULTS_SUMMARY_NAME)
            if existing == manifest:
                _verify_view(latest, existing)
                shutil.rmtree(staging)
                return ResultsViewResult(root=latest, manifest=existing, created=False)
            os.replace(latest, backup)
        try:
            os.replace(staging, latest)
        except Exception:
            if backup.exists() and not latest.exists():
                os.replace(backup, latest)
            raise
        if backup.exists():
            shutil.rmtree(backup)
        return ResultsViewResult(root=latest, manifest=manifest, created=True)
    except (ArtifactSealError, OSError, RunStorageError, ValueError) as exc:
        if isinstance(exc, ResultsViewError):
            raise
        raise ResultsViewError(str(exc)) from exc
    finally:
        if staging.exists():
            shutil.rmtree(staging)
        if backup.exists() and latest.exists():
            shutil.rmtree(backup)


def _artifact_targets(
    phases: tuple[ResolvedSourcePhase, ...],
    *,
    runs_root: Path,
    staging: Path,
) -> tuple[_PlannedResult, ...]:
    plans: list[_PlannedResult] = []
    for phase in phases:
        phase_id = phase.binding.phase_id
        run_directory = runs_root / phase.binding.source_run_id
        for artifact in phase.output_artifacts:
            source = require_regular_file_under(
                run_directory,
                run_directory / Path(artifact.path),
                description="curated results source",
            )
            category = _category(source)
            destination = staging / RESULTS_PHASE_DIRS[phase_id] / category / source.name
            plans.append(
                _PlannedResult(
                    source=source,
                    destination=destination,
                    phase_id=phase_id,
                    source_path=source.relative_to(runs_root).as_posix(),
                    origin="pipeline-output",
                )
            )
    return tuple(plans)


def _review_package_targets(
    package_paths: tuple[Path, ...],
    *,
    raw_root: Path,
    runs_root: Path,
    snapshot_root: Path | None,
    staging: Path,
) -> tuple[tuple[_PlannedResult, ...], tuple[str, ...]]:
    if not package_paths:
        return (), ()
    if snapshot_root is None:
        raise ResultsViewError(
            "snapshot root is required when including a Phase 03 AI review package"
        )

    from buduunkhad.geospatial_ai.path_safety import StorageRoots
    from buduunkhad.geospatial_ai.phase03_handoff import (
        REVIEW_GPKG_NAME,
        REVIEW_MANIFEST_NAME,
        verify_review_package,
    )

    roots = StorageRoots(
        raw_root=raw_root,
        snapshot_root=snapshot_root,
        work_root=runs_root.parent,
    )
    plans: list[_PlannedResult] = []
    package_ids: list[str] = []
    for raw_path in package_paths:
        package_path = _resolved_package_directory(raw_path, runs_root=runs_root)
        manifest = verify_review_package(package_path, roots=roots)
        package_ids.append(manifest.package_id)
        label = manifest.package_id[:16]
        data_root = staging / RESULTS_PHASE_DIRS["03"] / "data" / "ai_review" / label
        report_root = staging / RESULTS_PHASE_DIRS["03"] / "reports" / "ai_review" / label
        package_sources = [
            (
                package_path / REVIEW_GPKG_NAME,
                data_root / REVIEW_GPKG_NAME,
            ),
            *(
                (
                    package_path / relative,
                    data_root / Path(relative),
                )
                for relative, _digest in manifest.source_preview_files
            ),
            (
                package_path / REVIEW_MANIFEST_NAME,
                report_root / REVIEW_MANIFEST_NAME,
            ),
        ]
        for source_path, destination in package_sources:
            source = require_regular_file_under(
                package_path,
                source_path,
                description="curated review-package source",
            )
            plans.append(
                _PlannedResult(
                    source=source,
                    destination=destination,
                    phase_id="03",
                    source_path=source.relative_to(runs_root).as_posix(),
                    origin="review-package",
                )
            )
    if len(package_ids) != len(set(package_ids)):
        raise ResultsViewError("the same review package was selected more than once")
    return tuple(plans), tuple(sorted(package_ids))


def _validate_plans(
    plans: list[_PlannedResult],
    *,
    staging: Path,
) -> dict[Path, Path]:
    sources: dict[Path, Path] = {}
    destinations: set[str] = set()
    for plan in plans:
        relative = canonical_relative_path(plan.destination.relative_to(staging).as_posix())
        if relative in destinations:
            raise ResultsViewError(f"curated results destination collision: {relative}")
        if plan.source in sources:
            raise ResultsViewError(f"curated results source selected more than once: {plan.source}")
        destinations.add(relative)
        sources[plan.source] = plan.destination
    return sources


def _copy_artifacts(
    plans: list[_PlannedResult],
    *,
    staging: Path,
    source_targets: dict[Path, Path],
) -> list[ResultsFile]:
    copied: list[ResultsFile] = []
    for plan in sorted(
        plans,
        key=lambda item: item.destination.as_posix(),
    ):
        source = plan.source
        destination = plan.destination
        source_sha = sha256_file(source)
        source_size = source.stat().st_size
        destination.parent.mkdir(parents=True, exist_ok=True)
        transformation: Literal["qgz-rebase-v1"] | None = None
        if source.suffix.casefold() == ".qgz":
            copy_qgz_rebased(
                source,
                destination,
                copied_sources=source_targets,
                require_mapped_sources=True,
            )
            transformation = "qgz-rebase-v1"
        else:
            shutil.copy2(source, destination)
        if sha256_file(source) != source_sha or source.stat().st_size != source_size:
            raise ResultsViewError(f"source changed while creating results: {source}")
        if transformation is None and (
            sha256_file(destination) != source_sha or destination.stat().st_size != source_size
        ):
            raise ResultsViewError(f"curated result differs from source: {source}")
        copied.append(
            ResultsFile(
                phase_id=plan.phase_id,
                origin=plan.origin,
                path=destination.relative_to(staging).as_posix(),
                sha256=sha256_file(destination),
                size_bytes=destination.stat().st_size,
                source_path=plan.source_path,
                source_sha256=source_sha,
                source_size_bytes=source_size,
                transformation=transformation,
            )
        )
    return copied


def _verify_view(root: Path, manifest: ResultsViewManifest) -> None:
    expected = {item.path for item in manifest.files} | {RESULTS_SUMMARY_NAME}
    observed: set[str] = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ResultsViewError(f"results view contains a symlink: {path}")
        if path.is_file():
            observed.add(path.relative_to(root).as_posix())
    if observed != expected:
        raise ResultsViewError(
            "results view file inventory changed "
            f"(added={sorted(observed - expected)}, missing={sorted(expected - observed)})"
        )
    for record in manifest.files:
        path = require_regular_file_under(
            root,
            root / Path(record.path),
            description="curated result",
        )
        if path.stat().st_size != record.size_bytes or sha256_file(path) != record.sha256:
            raise ResultsViewError(f"curated result changed: {record.path}")


def _review_project_source(path: Path, *, runs_root: Path) -> Path:
    try:
        source = require_regular_file_under(
            runs_root,
            path,
            description="integrated review project",
        )
    except ArtifactSealError as exc:
        raise ResultsViewError(str(exc)) from exc
    if source.suffix.casefold() != ".qgz":
        raise ResultsViewError("integrated review project must be a .qgz file")
    return source


def _resolved_package_directory(path: Path, *, runs_root: Path) -> Path:
    candidate = Path(path).absolute()
    if has_symlink_component(candidate):
        raise ResultsViewError(f"review package must not use a symlink: {candidate}")
    try:
        package = candidate.resolve(strict=True)
        package.relative_to(runs_root)
    except (OSError, ValueError) as exc:
        raise ResultsViewError("review package must be inside the configured runs root") from exc
    if not package.is_dir():
        raise ResultsViewError(f"review package is not a directory: {package}")
    return package


def _load_run_manifest(path: Path, *, run_id: str) -> dict[str, object]:
    try:
        safe = require_regular_file_under(path.parent, path, description="source run manifest")
        data = json.loads(
            safe.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
        )
    except (ArtifactSealError, OSError, UnicodeError, ValueError) as exc:
        raise ResultsViewError("source run manifest is invalid") from exc
    if not isinstance(data, dict):
        raise ResultsViewError("source run manifest root must be an object")
    if (
        data.get("manifest_format_version") not in SUPPORTED_RUN_MANIFEST_FORMAT_VERSIONS
        or data.get("run_layout_version") != RUN_LAYOUT_VERSION
        or data.get("run_id") != run_id
        or data.get("dry_run") is not False
        or data.get("error") != ""
    ):
        raise ResultsViewError("source run is not a complete run-isolated execution")
    _finished_at(data)
    return data


def _completed_phase_ids(data: dict[str, object]) -> tuple[str, ...]:
    raw = data.get("phases")
    if not isinstance(raw, list):
        raise ResultsViewError("source run phase records are invalid")
    result: list[str] = []
    for item in raw:
        if not isinstance(item, dict):
            raise ResultsViewError("source run phase record is invalid")
        phase_id = item.get("phase_id")
        if phase_id in RESULTS_PHASE_DIRS and item.get("status") == "ok":
            output_artifacts = item.get("output_artifacts")
            if not isinstance(output_artifacts, list):
                raise ResultsViewError("source run output artifact inventory is invalid")
            if output_artifacts:
                result.append(str(phase_id))
    if tuple(result) != tuple(sorted(set(result))):
        raise ResultsViewError("source run completed phases are duplicated or unordered")
    return tuple(result)


def _phase_pending(data: dict[str, object], phase_id: str) -> bool:
    phases = data.get("phases")
    assert isinstance(phases, list)
    phase = next(
        item for item in phases if isinstance(item, dict) and item.get("phase_id") == phase_id
    )
    value = phase.get("qaqc_pending")
    if not isinstance(value, bool):
        raise ResultsViewError("source phase pending state is invalid")
    return value


def _finished_at(data: dict[str, object]) -> datetime:
    value = data.get("finished_at")
    if not isinstance(value, str) or not value:
        raise ResultsViewError("source run completion time is missing")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ResultsViewError("source run completion time is invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ResultsViewError("source run completion time must be timezone-aware")
    return parsed


def _category(path: Path) -> str:
    suffix = path.suffix.casefold()
    if suffix in _DATA_SUFFIXES:
        return "data"
    if suffix in _PROJECT_SUFFIXES:
        return "projects"
    return "reports"


def _load_results_manifest(path: Path) -> ResultsViewManifest:
    try:
        data = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
        )
        return ResultsViewManifest.model_validate(data)
    except (OSError, UnicodeError, ValueError) as exc:
        raise ResultsViewError("existing results summary is invalid") from exc


def _resolved_root(
    path: Path,
    description: str,
    *,
    require_existing: bool = True,
) -> Path:
    candidate = Path(path).absolute()
    if has_symlink_component(candidate):
        raise ResultsViewError(f"{description} must not use a symlink: {candidate}")
    try:
        resolved = candidate.resolve(strict=require_existing)
    except OSError as exc:
        raise ResultsViewError(f"{description} does not exist: {candidate}") from exc
    if require_existing and not resolved.is_dir():
        raise ResultsViewError(f"{description} is not a directory: {resolved}")
    if not require_existing and resolved.exists() and not resolved.is_dir():
        raise ResultsViewError(f"{description} is not a directory: {resolved}")
    return resolved


def _reject_overlap(*roots: tuple[str, Path]) -> None:
    for index, (left_name, left) in enumerate(roots):
        for right_name, right in roots[index + 1 :]:
            if left == right or left in right.parents or right in left.parents:
                raise ResultsViewError(
                    f"{left_name} and {right_name} must not overlap: {left} ; {right}"
                )


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result
