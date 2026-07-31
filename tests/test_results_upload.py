"""Verified transfer of curated results to a synced external folder."""

from __future__ import annotations

from pathlib import Path

import pytest

from buduunkhad.core import results_upload as results_upload_module
from buduunkhad.core.qgis_project import read_qgz_layers
from buduunkhad.core.results_upload import (
    RESULTS_UPLOAD_DIRECTORY_NAME,
    ResultsUploadError,
    upload_results_view,
)
from buduunkhad.core.results_view import materialize_results_view
from buduunkhad.pipeline import run_pipeline


def _create_directory_symlink_or_skip(link: Path, target: Path) -> None:
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"operating system cannot create the required symlink: {exc}")


def test_upload_results_is_complete_portable_and_idempotent(raw_archive):
    config, register, _raw = raw_archive
    run = run_pipeline(config, register, only=["00", "01"], dry_run=False)
    run_dir = config.runs_root / run.run_id
    phase01_qgz = next(
        run_dir / artifact.path
        for artifact in run.phases[1].output_artifacts
        if artifact.path.endswith(".qgz")
    )
    curated = materialize_results_view(
        project_name=config.project.name,
        raw_root=config.raw_root,
        output_root=config.output_root,
        runs_root=config.runs_root,
        results_root=config.base_dir / "results",
        run_id=run.run_id,
        review_project=phase01_qgz,
    )
    upload_root = config.base_dir / "drive-upload"

    first = upload_results_view(curated.root, upload_root)
    (first.destination / "desktop.ini").write_text("Drive shell metadata", encoding="utf-8")
    (first.destination / "01_master_gis" / "desktop.ini").write_text(
        "Drive shell metadata",
        encoding="utf-8",
    )
    repeated = upload_results_view(curated.root, upload_root)

    assert first.created is True
    assert repeated.created is False
    assert repeated.destination == first.destination
    assert repeated.manifest == first.manifest
    assert first.destination.name == RESULTS_UPLOAD_DIRECTORY_NAME
    assert [path.name for path in upload_root.iterdir() if path.is_dir()] == [
        RESULTS_UPLOAD_DIRECTORY_NAME
    ]
    destination_root = first.destination.resolve()
    for qgz in first.destination.rglob("*.qgz"):
        for layer in read_qgz_layers(qgz):
            datasource = Path(layer["datasource"].partition("|")[0])
            resolved = (qgz.parent / datasource).resolve(strict=True)
            resolved.relative_to(destination_root)


def test_upload_results_rejects_changed_existing_destination(raw_archive):
    config, register, _raw = raw_archive
    run = run_pipeline(config, register, only=["00"], dry_run=False)
    curated = materialize_results_view(
        project_name=config.project.name,
        raw_root=config.raw_root,
        output_root=config.output_root,
        runs_root=config.runs_root,
        results_root=config.base_dir / "results",
        run_id=run.run_id,
    )
    uploaded = upload_results_view(curated.root, config.base_dir / "drive-upload")
    changed = next(
        uploaded.destination / record.path
        for record in uploaded.manifest.files
        if record.transformation is None
    )
    changed.write_bytes(changed.read_bytes() + b"changed")

    with pytest.raises(ResultsUploadError, match="uploaded result changed"):
        upload_results_view(curated.root, config.base_dir / "drive-upload")


def test_upload_results_replaces_the_single_current_directory(raw_archive):
    config, register, _raw = raw_archive
    first_run = run_pipeline(config, register, only=["00"], dry_run=False)
    first = materialize_results_view(
        project_name=config.project.name,
        raw_root=config.raw_root,
        output_root=config.output_root,
        runs_root=config.runs_root,
        results_root=config.base_dir / "results-first",
        run_id=first_run.run_id,
    )
    upload_root = config.base_dir / "drive-upload"
    first_upload = upload_results_view(first.root, upload_root)

    second_run = run_pipeline(config, register, only=["00"], dry_run=False)
    second = materialize_results_view(
        project_name=config.project.name,
        raw_root=config.raw_root,
        output_root=config.output_root,
        runs_root=config.runs_root,
        results_root=config.base_dir / "results-second",
        run_id=second_run.run_id,
    )
    second_upload = upload_results_view(second.root, upload_root)

    assert second_upload.created is True
    assert second_upload.destination == first_upload.destination
    assert second_upload.manifest == second.manifest
    assert second_upload.manifest != first_upload.manifest
    assert [path.name for path in upload_root.iterdir() if path.is_dir()] == [
        RESULTS_UPLOAD_DIRECTORY_NAME
    ]


def test_upload_results_restores_previous_directory_when_replacement_fails(
    raw_archive,
    monkeypatch,
):
    config, register, _raw = raw_archive
    first_run = run_pipeline(config, register, only=["00"], dry_run=False)
    first = materialize_results_view(
        project_name=config.project.name,
        raw_root=config.raw_root,
        output_root=config.output_root,
        runs_root=config.runs_root,
        results_root=config.base_dir / "results-first",
        run_id=first_run.run_id,
    )
    upload_root = config.base_dir / "drive-upload"
    original = upload_results_view(first.root, upload_root)
    second_run = run_pipeline(config, register, only=["00"], dry_run=False)
    second = materialize_results_view(
        project_name=config.project.name,
        raw_root=config.raw_root,
        output_root=config.output_root,
        runs_root=config.runs_root,
        results_root=config.base_dir / "results-second",
        run_id=second_run.run_id,
    )
    real_replace = results_upload_module.os.replace

    def fail_install(source, destination):
        if Path(source).name.startswith(".u-") and Path(destination).name == "Buduunkhad":
            raise OSError("synthetic install failure")
        return real_replace(source, destination)

    monkeypatch.setattr(results_upload_module.os, "replace", fail_install)
    with pytest.raises(ResultsUploadError, match="synthetic install failure"):
        upload_results_view(second.root, upload_root)

    restored = upload_results_view(first.root, upload_root)
    assert restored.created is False
    assert restored.destination == original.destination
    assert restored.manifest == original.manifest
    assert not any(path.name.startswith((".u-", ".b-")) for path in upload_root.iterdir())


def test_upload_results_rejects_protected_destination(raw_archive):
    config, register, _raw = raw_archive
    run = run_pipeline(config, register, only=["00"], dry_run=False)
    curated = materialize_results_view(
        project_name=config.project.name,
        raw_root=config.raw_root,
        output_root=config.output_root,
        runs_root=config.runs_root,
        results_root=config.base_dir / "results",
        run_id=run.run_id,
    )

    with pytest.raises(ResultsUploadError, match="must not overlap"):
        upload_results_view(
            curated.root,
            config.raw_root,
            protected_roots=(config.raw_root,),
        )
    nested_destination = curated.root / "unexpected-upload"
    with pytest.raises(ResultsUploadError, match="must not overlap"):
        upload_results_view(curated.root, nested_destination)
    assert not nested_destination.exists()


def test_upload_results_rejects_symlinked_external_roots(raw_archive):
    config, register, _raw = raw_archive
    run = run_pipeline(config, register, only=["00"], dry_run=False)
    curated = materialize_results_view(
        project_name=config.project.name,
        raw_root=config.raw_root,
        output_root=config.output_root,
        runs_root=config.runs_root,
        results_root=config.base_dir / "results",
        run_id=run.run_id,
    )
    external = config.base_dir / "external"
    external.mkdir()
    upload_link = config.base_dir / "upload-link"
    protected_link = config.base_dir / "protected-link"
    _create_directory_symlink_or_skip(upload_link, external)
    _create_directory_symlink_or_skip(protected_link, config.raw_root)

    with pytest.raises(ResultsUploadError, match="upload root must not use a symlink"):
        upload_results_view(curated.root, upload_link)
    with pytest.raises(ResultsUploadError, match="protected root must not use a symlink"):
        upload_results_view(
            curated.root,
            external,
            protected_roots=(protected_link,),
        )


def test_upload_results_namespaces_another_exploration_area(raw_archive):
    config, register, _raw = raw_archive
    run = run_pipeline(config, register, only=["00"], dry_run=False)
    curated = materialize_results_view(
        project_name="Nergui Undur",
        raw_root=config.raw_root,
        output_root=config.output_root,
        runs_root=config.runs_root,
        results_root=config.base_dir / "results",
        run_id=run.run_id,
    )

    uploaded = upload_results_view(curated.root, config.base_dir / "multi-project-results")

    assert uploaded.destination.name == "Nergui Undur"
    assert uploaded.manifest.project_name == "Nergui Undur"


def test_verified_local_mirror_can_feed_the_drive_copy(raw_archive):
    config, register, _raw = raw_archive
    run = run_pipeline(config, register, only=["00"], dry_run=False)
    curated = materialize_results_view(
        project_name=config.project.name,
        raw_root=config.raw_root,
        output_root=config.output_root,
        runs_root=config.runs_root,
        results_root=config.base_dir / "results",
        run_id=run.run_id,
    )
    mirrored = upload_results_view(curated.root, config.base_dir / "local-results")
    (mirrored.destination / "desktop.ini").write_text("Windows shell metadata", encoding="utf-8")

    uploaded = upload_results_view(mirrored.destination, config.base_dir / "drive-results")

    assert uploaded.manifest == mirrored.manifest
    assert uploaded.destination.name == config.project.name


def test_upload_results_rejects_unsafe_project_directory_name(raw_archive):
    config, register, _raw = raw_archive
    run = run_pipeline(config, register, only=["00"], dry_run=False)
    curated = materialize_results_view(
        project_name="../another-project",
        raw_root=config.raw_root,
        output_root=config.output_root,
        runs_root=config.runs_root,
        results_root=config.base_dir / "results",
        run_id=run.run_id,
    )

    upload_root = config.base_dir / "multi-project-results"
    with pytest.raises(ResultsUploadError, match="safe directory name"):
        upload_results_view(curated.root, upload_root)
    assert not upload_root.exists()
