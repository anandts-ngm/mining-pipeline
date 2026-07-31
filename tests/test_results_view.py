"""Curated operator results assembled from exact sealed run outputs."""

from __future__ import annotations

from pathlib import Path

import pytest

from buduunkhad.core.qgis_project import read_qgz_layers
from buduunkhad.core.results_view import (
    RESULTS_SUMMARY_NAME,
    ResultsViewError,
    materialize_results_view,
)
from buduunkhad.pipeline import run_pipeline


def test_results_view_curates_declared_outputs_and_is_idempotent(raw_archive):
    config, register, _raw = raw_archive
    run = run_pipeline(
        config,
        register,
        only=["00", "01"],
        dry_run=False,
    )
    run_dir = config.runs_root / run.run_id
    (run_dir / "unrelated-scratch.tmp").write_text("omit me", encoding="utf-8")
    phase01_qgz = next(
        run_dir / artifact.path
        for artifact in run.phases[1].output_artifacts
        if artifact.path.endswith(".qgz")
    )

    result = materialize_results_view(
        project_name=config.project.name,
        raw_root=config.raw_root,
        output_root=config.output_root,
        runs_root=config.runs_root,
        results_root=config.base_dir / "operator-results",
        run_id=run.run_id,
        review_project=phase01_qgz,
    )

    assert result.created is True
    assert [phase.phase_id for phase in result.manifest.phases] == ["00", "01"]
    assert {path.name for path in result.root.iterdir()} == {
        "00_inventory",
        "01_master_gis",
        "Buduunkhad.qgz",
        RESULTS_SUMMARY_NAME,
    }
    assert not any("Working" in part for path in result.root.rglob("*") for part in path.parts)
    assert not any(path.name == "unrelated-scratch.tmp" for path in result.root.rglob("*"))
    assert {
        path.parent.name
        for path in result.root.rglob("*")
        if path.is_file() and path.name != RESULTS_SUMMARY_NAME
    } <= {"data", "projects", "reports", "latest"}

    for qgz in result.root.rglob("*.qgz"):
        for layer in read_qgz_layers(qgz):
            datasource = Path(layer["datasource"].partition("|")[0])
            assert (qgz.parent / datasource).resolve(strict=True).is_file()

    repeated = materialize_results_view(
        project_name=config.project.name,
        raw_root=config.raw_root,
        output_root=config.output_root,
        runs_root=config.runs_root,
        results_root=config.base_dir / "operator-results",
        run_id=run.run_id,
        review_project=phase01_qgz,
    )
    assert repeated.created is False
    assert repeated.manifest == result.manifest


def test_results_view_detects_mutation_of_existing_view(raw_archive):
    config, register, _raw = raw_archive
    run = run_pipeline(config, register, only=["00"], dry_run=False)

    def materialize():
        return materialize_results_view(
            project_name=config.project.name,
            raw_root=config.raw_root,
            output_root=config.output_root,
            runs_root=config.runs_root,
            results_root=config.base_dir / "operator-results",
            run_id=run.run_id,
        )

    result = materialize()
    changed = next(
        result.root / record.path
        for record in result.manifest.files
        if record.transformation is None
    )
    changed.write_bytes(changed.read_bytes() + b"changed")

    with pytest.raises(ResultsViewError, match="curated result changed"):
        materialize()


def test_results_root_overlap_is_rejected_before_creation(raw_archive):
    config, _register, raw = raw_archive
    config.runs_root.mkdir(parents=True, exist_ok=True)
    unsafe = raw / "results"

    with pytest.raises(ResultsViewError, match="must not overlap"):
        materialize_results_view(
            project_name=config.project.name,
            raw_root=raw,
            output_root=config.output_root,
            runs_root=config.runs_root,
            results_root=unsafe,
            run_id="019fb1c0-742b-7eb6-bd4a-105cb840e9bd",
        )
    assert not unsafe.exists()
