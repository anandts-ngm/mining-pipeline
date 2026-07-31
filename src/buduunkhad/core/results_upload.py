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


RESULTS_UPLOAD_DIRECTORY_NAME = "Buduunkhad"
_WINDOWS_RESERVED_NAMES = {
    "aux",
    "con",
    "nul",
    "prn",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}


def upload_results_view(
    results_view: Path,
    upload_root: Path,
    *,
    protected_roots: tuple[Path, ...] = (),
) -> ResultsUploadResult:
    """Atomically install one exact curated view as the external current result."""

    source = _existing_root(results_view, "curated results view")
    destination_candidate = _comparison_root(upload_root, "results upload root")
    _reject_overlap(source, destination_candidate)
    for protected in protected_roots:
        protected_root = _comparison_root(protected, "protected root")
        _reject_overlap(protected_root, destination_candidate)
    manifest = _verified_source_manifest(source)
    directory_name = _project_directory_name(manifest.project_name)
    destination_root = _external_root(destination_candidate)
    destination = destination_root / directory_name
    if destination.exists():
        try:
            existing = _load_uploaded_manifest(destination)
            _verify_uploaded(destination, existing)
        except (OSError, ResultsViewError, ValueError) as exc:
            raise ResultsUploadError(str(exc)) from exc
        if existing == manifest:
            return ResultsUploadResult(
                destination=destination,
                manifest=manifest,
                created=False,
            )

    # Keep the temporary component short because Windows still applies MAX_PATH to
    # some copy operations even when the final Drive folder is within the limit.
    staging = destination_root / f".u-{uuid.uuid4().hex[:8]}"
    backup = destination_root / f".b-{uuid.uuid4().hex[:8]}"
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
        if destination.exists():
            os.replace(destination, backup)
        try:
            os.replace(staging, destination)
            _verify_uploaded(destination, manifest)
        except Exception:
            if destination.exists():
                shutil.rmtree(destination)
            if backup.exists():
                os.replace(backup, destination)
            raise
        if backup.exists():
            shutil.rmtree(backup)
        return ResultsUploadResult(
            destination=destination,
            manifest=manifest,
            created=True,
        )
    except (ArtifactSealError, OSError, ResultsViewError, ValueError) as exc:
        raise ResultsUploadError(str(exc)) from exc
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def _load_uploaded_manifest(root: Path) -> ResultsViewManifest:
    summary = require_regular_file_under(
        root,
        root / RESULTS_SUMMARY_NAME,
        description="uploaded results summary",
    )
    try:
        return ResultsViewManifest.model_validate_json(summary.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise ResultsUploadError("uploaded results summary is invalid") from exc


def _verified_source_manifest(root: Path) -> ResultsViewManifest:
    try:
        return verify_results_view(root)
    except ResultsViewError as curated_error:
        try:
            manifest = _load_uploaded_manifest(root)
            _verify_uploaded(root, manifest)
        except (ArtifactSealError, OSError, ResultsUploadError, ValueError) as exc:
            raise ResultsUploadError(
                "results source is neither a valid curated view nor a verified mirror "
                f"(curated={curated_error}; mirror={exc})"
            ) from exc
        return manifest


def _verify_uploaded(root: Path, expected_manifest: ResultsViewManifest) -> None:
    manifest = _load_uploaded_manifest(root)
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


def _comparison_root(path: Path, description: str) -> Path:
    candidate = Path(path).absolute()
    if has_symlink_component(candidate):
        raise ResultsUploadError(f"{description} must not use a symlink: {candidate}")
    return candidate.resolve(strict=False)


def _reject_overlap(source: Path, destination: Path) -> None:
    if source == destination or source in destination.parents or destination in source.parents:
        raise ResultsUploadError(
            f"curated results and upload roots must not overlap: {source} ; {destination}"
        )


def _project_directory_name(project_name: str) -> str:
    """Return one safe, human-readable directory component bound to the view manifest."""

    name = project_name.strip()
    if not name or name in {".", ".."} or name != project_name:
        raise ResultsUploadError("results project name is not a safe directory name")
    if len(name) > 100 or name[-1] in {" ", "."}:
        raise ResultsUploadError("results project name is not a safe directory name")
    if any(ord(character) < 32 or character in '<>:"/\\|?*' for character in name):
        raise ResultsUploadError("results project name is not a safe directory name")
    if name.partition(".")[0].casefold() in _WINDOWS_RESERVED_NAMES:
        raise ResultsUploadError("results project name is reserved by Windows")
    return name
