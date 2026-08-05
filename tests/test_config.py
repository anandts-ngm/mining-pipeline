"""Tests for config + register loading and validation."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from buduunkhad.config import (
    OUTPUT_ROOT_ENV,
    PIPELINE_DRIVE_ROOT_ENV,
    PIPELINE_OUTPUTS_ROOT_ENV,
    PIPELINE_WORK_ROOT_ENV,
    PROJECT_ROOT_ENV,
    RAW_ROOT_ENV,
    RESULTS_MIRROR_ROOT_ENV,
    RESULTS_ROOT_ENV,
    RESULTS_UPLOAD_ROOT_ENV,
    WORK_ROOT_ENV,
    ProjectMeta,
)
from buduunkhad.core.paths import PHASE_DIRS


def test_config_loads(project):
    config, register, _tmp = project
    assert config.project.project_code == "XV-023222"
    assert config.project.license_code == "L23222"
    assert config.project.storage_slug == "buduunkhad"
    assert config.target_epsg == 32647
    assert config.data_prefix == "XV023222_Buduunkhad"
    assert config.register_prefix == "XV-023222_Buduunkhad"
    assert config.boundary.input_no == 8
    assert config.boundary.buffers_m == [500, 1000, 5000, 10000, 20000, 25000]


def test_config_rejects_unknown_top_level_and_nested_keys(project):
    config, _register, _tmp = project
    value = config.model_dump(mode="python")
    value["unexpected_section"] = {}
    with pytest.raises(ValidationError, match="unexpected_section"):
        type(config).model_validate(value)

    value = config.model_dump(mode="python")
    value["boundary"]["buffers_metres"] = [500]
    with pytest.raises(ValidationError, match="buffers_metres"):
        type(config).model_validate(value)


def test_register_is_complete(project):
    _config, register, _tmp = project
    # 78 methodology inputs + the SAS hand-interpreted 1:25k scan reconciled from
    # the real archive = 79, numbered contiguously from 1.
    assert len(register) == 79
    assert sorted(r.no for r in register) == list(range(1, 80))


def test_register_groups_match(project):
    config, register, _tmp = project
    from collections import Counter

    counts = Counter(r.evidence_group for r in register)
    for group in config.evidence_groups:
        assert counts[group.name] == group.count


def test_register_groups_cross_validation(project):
    from buduunkhad.config import _validate_register_groups

    config, register, _tmp = project
    _validate_register_groups(register, config.evidence_groups)  # real data agrees -> no raise
    with pytest.raises(ValueError):
        # one row short -> a per-group count no longer matches project.yaml
        _validate_register_groups(register[:-1], config.evidence_groups)


def _write_register(path: Path, rows: list[str]) -> None:
    header = "no,evidence_group,filename,file_type,primary_phase,methodology_action,is_sidecar,parent_file"
    path.write_text("\n".join([header, *rows]) + "\n", encoding="utf-8")


def test_register_rejects_duplicate_filename(tmp_path):
    from buduunkhad.config import load_register

    reg = tmp_path / "r.csv"
    _write_register(reg, ["1,G,dup.tif,raster,02,,,", "2,G,dup.tif,raster,02,,,"])
    with pytest.raises(ValueError):
        load_register(reg)


def test_manifest_rejects_duplicate_filename(tmp_path):
    from buduunkhad.core.ingest import load_manifest

    m = tmp_path / "m.csv"
    m.write_text(
        "no,evidence_group,filename,file_type,is_sidecar,parent_file,"
        "drive_file_id,drive_size_bytes,drive_theme_folder,match_status\n"
        "1,G,dup.jpg,image_scan,false,,ID1,10,T,matched\n"
        "2,G,dup.jpg,image_scan,false,,ID2,20,T,matched\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_manifest(m)


def test_register_sidecar_parents_exist(project):
    _config, register, _tmp = project
    names = {r.filename for r in register}
    for r in register:
        if r.is_sidecar and r.parent_file:
            assert r.parent_file in names


def test_master_gpkg_layers(project):
    config, _register, _tmp = project
    names = {layer.name for layer in config.master_gpkg_layers}
    assert "license_boundary" in names
    assert "pXRF_reading_table" in names
    assert len(config.master_gpkg_layers) == 13
    # exactly one aspatial layer
    aspatial = [layer for layer in config.master_gpkg_layers if not layer.is_spatial]
    assert [layer.name for layer in aspatial] == ["pXRF_reading_table"]


def test_raw_root_env_override(project, monkeypatch):
    config, _register, _tmp = project
    # default: resolves under the project base dir
    assert config.raw_root.name == "00_Raw_Files_Archive"
    # override: a per-machine path (e.g. a Drive-for-Desktop folder) wins
    target = Path.home() / "drive_stub" / "0. Raw Data"
    monkeypatch.setenv(RAW_ROOT_ENV, str(target))
    assert config.raw_root == target


def test_work_root_env_override_places_runs_below_work_root(project, monkeypatch):
    config, _register, tmp_path = project
    target = tmp_path / "protected-work"
    monkeypatch.setenv(WORK_ROOT_ENV, str(target))

    assert config.runs_root == target / "runs"
    assert config.evidence_root == target / "evidence-authority"
    assert config.results_root == target.parent / "results"


def test_project_root_defines_standard_local_layout(project, monkeypatch):
    config, _register, tmp_path = project
    root = tmp_path / "buduunkhad-project"
    monkeypatch.setenv(PROJECT_ROOT_ENV, str(root))
    for name in (RAW_ROOT_ENV, OUTPUT_ROOT_ENV, WORK_ROOT_ENV, RESULTS_ROOT_ENV):
        monkeypatch.delenv(name, raising=False)

    assert config.raw_root == root / "raw"
    assert config.output_root == root / "current"
    assert config.runs_root == root / "work" / "runs"
    assert config.evidence_root == root / "work" / "evidence-authority"
    assert config.results_root == root / "results"


def test_specific_roots_override_standard_project_layout(project, monkeypatch):
    config, _register, tmp_path = project
    monkeypatch.setenv(PROJECT_ROOT_ENV, str(tmp_path / "project"))
    monkeypatch.setenv(RAW_ROOT_ENV, str(tmp_path / "specific-raw"))
    monkeypatch.setenv(OUTPUT_ROOT_ENV, str(tmp_path / "specific-current"))
    monkeypatch.setenv(WORK_ROOT_ENV, str(tmp_path / "specific-work"))
    monkeypatch.setenv(RESULTS_ROOT_ENV, str(tmp_path / "specific-results"))
    monkeypatch.setenv(RESULTS_MIRROR_ROOT_ENV, str(tmp_path / "local-results"))
    monkeypatch.setenv(RESULTS_UPLOAD_ROOT_ENV, str(tmp_path / "drive-results"))

    assert config.raw_root == tmp_path / "specific-raw"
    assert config.output_root == tmp_path / "specific-current"
    assert config.runs_root == tmp_path / "specific-work" / "runs"
    assert config.evidence_root == tmp_path / "specific-work" / "evidence-authority"
    assert config.results_root == tmp_path / "specific-results"
    assert config.results_mirror_root == tmp_path / "local-results"
    assert config.results_upload_root == tmp_path / "drive-results"


def test_generic_bases_namespace_storage_by_project(project, monkeypatch):
    config, _register, tmp_path = project
    work_base = tmp_path / "pipeline-work"
    outputs_base = tmp_path / "pipeline-outputs"
    drive_base = tmp_path / "drive"
    monkeypatch.setenv(PIPELINE_WORK_ROOT_ENV, str(work_base))
    monkeypatch.setenv(PIPELINE_OUTPUTS_ROOT_ENV, str(outputs_base))
    monkeypatch.setenv(PIPELINE_DRIVE_ROOT_ENV, str(drive_base))

    assert config.project_root == work_base / "buduunkhad"
    assert config.raw_root == work_base / "buduunkhad" / "raw"
    assert config.runs_root == work_base / "buduunkhad" / "work" / "runs"
    assert config.results_mirror_root == outputs_base
    assert config.results_upload_root == drive_base


def test_generic_work_base_isolates_multiple_exploration_areas(project, monkeypatch):
    config, _register, tmp_path = project
    work_base = tmp_path / "pipeline-work"
    monkeypatch.setenv(PIPELINE_WORK_ROOT_ENV, str(work_base))
    second = config.model_copy(
        update={
            "project": ProjectMeta(
                name="Nergui Undur",
                slug="nergui-undur",
                project_code="EXAMPLE-002",
                license_code="EXAMPLE-LICENCE",
                data_prefix_code="EXAMPLE002",
            )
        }
    )

    assert config.project_root == work_base / "buduunkhad"
    assert second.project_root == work_base / "nergui-undur"
    assert config.runs_root != second.runs_root
    assert config.raw_root != second.raw_root


def test_buduunkhad_specific_settings_win_over_generic_bases(project, monkeypatch):
    config, _register, tmp_path = project
    legacy_project = tmp_path / "legacy-project"
    legacy_mirror = tmp_path / "legacy-mirror"
    legacy_drive = tmp_path / "legacy-drive"
    monkeypatch.setenv(PIPELINE_WORK_ROOT_ENV, str(tmp_path / "generic-work"))
    monkeypatch.setenv(PIPELINE_OUTPUTS_ROOT_ENV, str(tmp_path / "generic-outputs"))
    monkeypatch.setenv(PIPELINE_DRIVE_ROOT_ENV, str(tmp_path / "generic-drive"))
    monkeypatch.setenv(PROJECT_ROOT_ENV, str(legacy_project))
    monkeypatch.setenv(RESULTS_MIRROR_ROOT_ENV, str(legacy_mirror))
    monkeypatch.setenv(RESULTS_UPLOAD_ROOT_ENV, str(legacy_drive))

    assert config.project_root == legacy_project
    assert config.results_mirror_root == legacy_mirror
    assert config.results_upload_root == legacy_drive


def test_phase_dirs_cover_workflow():
    assert PHASE_DIRS["00"] == "00_Raw_Files_Archive"
    assert PHASE_DIRS["01"] == "01_Phase_1_Data_Audit_and_Master_GIS_Setup"
    assert PHASE_DIRS["99"] == "99_Final_Deliverables"
    assert len(PHASE_DIRS) == 13
