"""Verified upload of one curated results view to an external synced folder."""

from __future__ import annotations

import os
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path

from buduunkhad.ai.fingerprint import sha256_file
from buduunkhad.core.results_view import (
    RESULTS_SUMMARY_NAME,
    ResultsViewError,
    ResultsViewManifest,
    verify_results_view,
)
from buduunkhad.core.run_artifacts import (
    ArtifactSealError,
    has_symlink_component,
    require_regular_file_under,
)


class ResultsUploadError(RuntimeError):
    """A curated results view could not be copied without changing its identity."""


@dataclass(frozen=True)
class ResultsUploadResult:
    destination: Path
    manifest: ResultsViewManifest
    created: bool


def upload_results_view(
    results_view: Path,
    upload_root: Path,
    *,
    protected_roots: tuple[Path, ...] = (),
) -> ResultsUploadResult:
    """Copy one exact curated view into a versioned external destination."""

    source = _existing_root(results_view, "curated results view")
    destination_candidate = Path(upload_root).absolute().resolve(strict=False)
    _reject_overlap(source, destination_candidate)
    for protected in protected_roots:
        _reject_overlap(protected.resolve(strict=False), destination_candidate)
    destination_root = _external_root(destination_candidate)
    try:
        manifest = verify_results_view(source)
    except ResultsViewError as exc:
        raise ResultsUploadError(str(exc)) from exc
    name = f"Buduunkhad_Results_{manifest.source_run_id}_{manifest.view_id[:12]}"
    destination = destination_root / name
    if destination.exists():
        try:
            _verify_uploaded(destination, manifest)
        except (OSError, ResultsViewError, ValueError) as exc:
            raise ResultsUploadError(str(exc)) from exc
        return ResultsUploadResult(
            destination=destination,
            manifest=manifest,
            created=False,
        )

    # Keep the temporary component short because Windows still applies MAX_PATH to
    # some copy operations even when the final Drive folder is within the limit.
    staging = destination_root / f".u-{uuid.uuid4().hex[:8]}"
    staging.mkdir()
    try:
        for record in manifest.files:
            source_file = require_regular_file_under(
                source,
                source / Path(record.path),
                description="curated upload source",
            )
            target = staging / Path(record.path)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, target)
            if target.stat().st_size != record.size_bytes or sha256_file(target) != record.sha256:
                raise ResultsUploadError(f"uploaded file differs from source: {record.path}")
        summary_source = require_regular_file_under(
            source,
            source / RESULTS_SUMMARY_NAME,
            description="curated results summary",
        )
        shutil.copy2(summary_source, staging / RESULTS_SUMMARY_NAME)
        _verify_uploaded(staging, manifest)
        os.replace(staging, destination)
        _verify_uploaded(destination, manifest)
        return ResultsUploadResult(
            destination=destination,
            manifest=manifest,
            created=True,
        )
    except (ArtifactSealError, OSError, ResultsViewError, ValueError) as exc:
        if isinstance(exc, ResultsUploadError):
            raise
        raise ResultsUploadError(str(exc)) from exc
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def _verify_uploaded(root: Path, expected_manifest: ResultsViewManifest) -> None:
    summary = require_regular_file_under(
        root,
        root / RESULTS_SUMMARY_NAME,
        description="uploaded results summary",
    )
    try:
        manifest = ResultsViewManifest.model_validate_json(summary.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise ResultsUploadError("uploaded results summary is invalid") from exc
    if manifest != expected_manifest:
        raise ResultsUploadError("uploaded results identity differs from the curated source")
    expected = {record.path for record in manifest.files} | {RESULTS_SUMMARY_NAME}
    observed: set[str] = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ResultsUploadError(f"uploaded results contain a symlink: {path}")
        if path.is_file() and path.name.casefold() != "desktop.ini":
            observed.add(path.relative_to(root).as_posix())
    if observed != expected:
        raise ResultsUploadError(
            "uploaded results file inventory changed "
            f"(added={sorted(observed - expected)}, missing={sorted(expected - observed)})"
        )
    for record in manifest.files:
        path = require_regular_file_under(
            root,
            root / Path(record.path),
            description="uploaded result",
        )
        if path.stat().st_size != record.size_bytes or sha256_file(path) != record.sha256:
            raise ResultsUploadError(f"uploaded result changed: {record.path}")


def _existing_root(path: Path, description: str) -> Path:
    candidate = Path(path).absolute()
    if has_symlink_component(candidate):
        raise ResultsUploadError(f"{description} must not use a symlink: {candidate}")
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise ResultsUploadError(f"{description} does not exist: {candidate}") from exc
    if not resolved.is_dir():
        raise ResultsUploadError(f"{description} is not a directory: {resolved}")
    return resolved


def _external_root(path: Path) -> Path:
    candidate = Path(path).absolute()
    if has_symlink_component(candidate):
        raise ResultsUploadError(f"results upload root must not use a symlink: {candidate}")
    try:
        candidate.mkdir(parents=True, exist_ok=True)
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise ResultsUploadError(f"results upload root is unavailable: {candidate}") from exc
    if not resolved.is_dir():
        raise ResultsUploadError(f"results upload root is not a directory: {resolved}")
    return resolved


def _reject_overlap(source: Path, destination: Path) -> None:
    if source == destination or source in destination.parents or destination in source.parents:
        raise ResultsUploadError(
            f"curated results and upload roots must not overlap: {source} ; {destination}"
        )
