"""Verified transfer of curated results to a synced external folder."""

from __future__ import annotations

from pathlib import Path

import pytest

from buduunkhad.core.qgis_project import read_qgz_layers
from buduunkhad.core.results_upload import ResultsUploadError, upload_results_view
from buduunkhad.core.results_view import materialize_results_view
from buduunkhad.pipeline import run_pipeline


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
    assert first.destination.name == (
        f"Buduunkhad_Results_{run.run_id}_{curated.manifest.view_id[:12]}"
    )
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
