"""Behavioral compatibility checks for the unchanged Typer CLI."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from click import unstyle
from typer.testing import CliRunner

from buduunkhad.cli import app
from buduunkhad.config import (
    OUTPUT_ROOT_ENV,
    RAW_ROOT_ENV,
    RESULTS_MIRROR_ROOT_ENV,
    RESULTS_UPLOAD_ROOT_ENV,
)
from buduunkhad.core.qaqc import Decision, new_report
from buduunkhad.phases.phase00_archive import Phase00Archive
from buduunkhad.pipeline import RunManifest

runner = CliRunner()


def test_help_lists_stable_core_commands() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for command in (
        "run",
        "list",
        "info",
        "validate",
        "methodology-status",
        "phase00",
        "phase99",
    ):
        assert command in result.stdout


def test_ai_help_is_additive_and_keeps_execution_steps_separate() -> None:
    result = runner.invoke(app, ["ai", "--help"])
    assert result.exit_code == 0
    for command in (
        "snapshot-create",
        "snapshot-verify",
        "prepare",
        "approve-egress",
        "execute",
        "ingest-response",
        "process-response",
        "evaluate",
        "inspect-job",
    ):
        assert command in result.stdout

    phase03 = runner.invoke(app, ["ai", "phase03", "--help"])
    assert phase03.exit_code == 0
    assert "import-ai-draft" in phase03.stdout
    assert "promote-reviewed" in phase03.stdout


def test_list_and_info_preserve_legacy_contract(project) -> None:
    config, _register, work = project
    config_path = work / "config" / "project.yaml"
    listed = runner.invoke(app, ["list"])
    assert listed.exit_code == 0
    assert "Registered phases (00 -> 99)" in listed.stdout
    assert "00  [BUILD]" in listed.stdout
    info = runner.invoke(app, ["info", "--config", str(config_path)])
    assert info.exit_code == 0
    assert config.project.project_code in info.stdout
    assert config.crs.target_authority in info.stdout
    assert "79 inputs" in info.stdout


def test_validate_synthetic_configuration(raw_archive) -> None:
    _config, _register, _raw_root = raw_archive
    config_path = _raw_root.parent.parent / "config" / "project.yaml"
    result = runner.invoke(app, ["validate", "--config", str(config_path)])
    assert result.exit_code == 0
    assert "all 79 raw inputs present" in result.stdout


def test_run_dry_run_uses_legacy_defaults(project) -> None:
    _config, _register, work = project
    config_path = work / "config" / "project.yaml"
    result = runner.invoke(app, ["run", "--config", str(config_path), "--dry-run"])
    assert result.exit_code == 0
    assert "dry_run=True" in result.stdout
    assert "00  dry-run" in result.stdout
    assert "05  dry-run" in result.stdout


def test_run_and_single_phase_help_expose_policy_and_exact_bindings() -> None:
    run_help = runner.invoke(app, ["run", "--help"])
    phase_help = runner.invoke(app, ["phase04", "--help"])
    run_help_text = unstyle(run_help.stdout)
    phase_help_text = unstyle(phase_help.stdout)

    assert run_help.exit_code == phase_help.exit_code == 0
    assert "--input-run" in run_help_text
    assert "--input-run" in phase_help_text
    assert "--phase-mode" in run_help_text
    assert "--execution-mode" in phase_help_text
    assert "--authorization" in run_help_text
    assert "--authorization" in phase_help_text
    assert "Retired" in run_help_text
    assert "--upload-results" in run_help_text


def test_cli_generic_override_fails_closed_without_creating_run(project) -> None:
    config, _register, work = project
    config_path = work / "config" / "project.yaml"
    result = runner.invoke(
        app,
        ["run", "--config", str(config_path), "--dry-run", "--override"],
    )

    assert result.exit_code == 2
    assert "--override is retired" in result.stdout
    assert not config.runs_root.exists()


def test_manual_evidence_registration_requires_actor_and_reason() -> None:
    help_result = runner.invoke(app, ["evidence", "register-run-layer", "--help"])
    help_text = unstyle(help_result.stdout)

    assert help_result.exit_code == 0
    assert "--actor" in help_text
    assert "--reason" in help_text


def test_info_honors_existing_environment_path_overrides(project, monkeypatch) -> None:
    _config, _register, work = project
    config_path = work / "config" / "project.yaml"
    raw_override = Path(work) / "env-raw"
    output_override = Path(work) / "env-output"
    monkeypatch.setenv(RAW_ROOT_ENV, str(raw_override))
    monkeypatch.setenv(OUTPUT_ROOT_ENV, str(output_override))
    result = runner.invoke(app, ["info", "--config", str(config_path)])
    assert result.exit_code == 0
    assert str(raw_override) in result.stdout
    assert str(output_override) in result.stdout


def test_real_run_automatically_uploads_curated_results(raw_archive, monkeypatch) -> None:
    _config, _register, raw_root = raw_archive
    config_path = raw_root.parent.parent / "config" / "project.yaml"
    upload_root = raw_root.parent.parent / "drive-results"
    mirror_root = raw_root.parent.parent / "local-results"
    monkeypatch.setenv(RESULTS_MIRROR_ROOT_ENV, str(mirror_root))
    monkeypatch.setenv(RESULTS_UPLOAD_ROOT_ENV, str(upload_root))

    result = runner.invoke(
        app,
        ["run", "--config", str(config_path), "--only", "00"],
    )

    assert result.exit_code == 0, result.stdout
    assert "local results mirror:" in result.stdout
    assert "Google Drive results:" in result.stdout
    assert [path.name for path in mirror_root.iterdir() if path.is_dir()] == ["Buduunkhad"]
    assert [path.name for path in upload_root.iterdir() if path.is_dir()] == ["Buduunkhad"]
    assert (mirror_root / "Buduunkhad" / "run-summary.json").read_bytes() == (
        upload_root / "Buduunkhad" / "run-summary.json"
    ).read_bytes()


def test_no_upload_still_refreshes_the_local_results_mirror(raw_archive, monkeypatch) -> None:
    _config, _register, raw_root = raw_archive
    config_path = raw_root.parent.parent / "config" / "project.yaml"
    mirror_root = raw_root.parent.parent / "local-results"
    drive_root = raw_root.parent.parent / "drive-results"
    monkeypatch.setenv(RESULTS_MIRROR_ROOT_ENV, str(mirror_root))
    monkeypatch.setenv(RESULTS_UPLOAD_ROOT_ENV, str(drive_root))

    result = runner.invoke(
        app,
        ["run", "--config", str(config_path), "--only", "00", "--no-upload-results"],
    )

    assert result.exit_code == 0, result.stdout
    assert (mirror_root / "Buduunkhad" / "run-summary.json").is_file()
    assert not drive_root.exists()


def test_drive_failure_preserves_the_verified_local_mirror(
    raw_archive,
    monkeypatch,
) -> None:
    from buduunkhad.core import results_upload as results_upload_module
    from buduunkhad.core.results_upload import ResultsUploadError

    _config, _register, raw_root = raw_archive
    config_path = raw_root.parent.parent / "config" / "project.yaml"
    mirror_root = raw_root.parent.parent / "local-results"
    drive_root = raw_root.parent.parent / "drive-results"
    monkeypatch.setenv(RESULTS_MIRROR_ROOT_ENV, str(mirror_root))
    monkeypatch.setenv(RESULTS_UPLOAD_ROOT_ENV, str(drive_root))
    real_upload = results_upload_module.upload_results_view

    def fail_drive(source, destination, **kwargs):
        if Path(destination) == drive_root:
            raise ResultsUploadError("synthetic Drive outage")
        return real_upload(source, destination, **kwargs)

    monkeypatch.setattr(results_upload_module, "upload_results_view", fail_drive)
    result = runner.invoke(
        app,
        ["run", "--config", str(config_path), "--only", "00"],
    )

    assert result.exit_code == 2
    assert "local mirror remains verified" in result.output
    assert "synthetic Drive outage" in result.output
    assert (mirror_root / "Buduunkhad" / "run-summary.json").is_file()


def test_failed_run_exit_and_message_do_not_depend_on_upload_root(
    raw_archive,
    monkeypatch,
) -> None:
    _config, _register, raw_root = raw_archive
    config_path = raw_root.parent.parent / "config" / "project.yaml"
    upload_root = raw_root.parent.parent / "drive-results"

    def failed_qaqc(self, ctx):  # noqa: ARG001
        report = new_report("00", "Raw Files Archive")
        report.add("Archive acceptance", "Synthetic failure", decision=Decision.FAIL)
        return report

    monkeypatch.setattr(Phase00Archive, "qaqc", failed_qaqc)
    without_upload = runner.invoke(
        app,
        ["run", "--config", str(config_path), "--only", "00"],
    )
    monkeypatch.setenv(RESULTS_UPLOAD_ROOT_ENV, str(upload_root))
    with_upload = runner.invoke(
        app,
        ["run", "--config", str(config_path), "--only", "00"],
    )

    for result in (without_upload, with_upload):
        assert result.exit_code == 2
        assert "Run failed: Phase 00 QA/QC failed before artifact sealing" in result.output
        assert "Pipeline succeeded" not in result.output
        assert "automatic results upload failed" not in result.output.casefold()
    assert not upload_root.exists()


def test_controlled_gate_stop_still_curates_results(project, monkeypatch) -> None:
    _config, _register, work = project
    config_path = work / "config" / "project.yaml"
    upload_root = work / "drive-results"
    monkeypatch.setenv(RESULTS_UPLOAD_ROOT_ENV, str(upload_root))
    manifest = RunManifest(
        run_id="controlled-gate-stop",
        started_at="2026-07-31T00:00:00+00:00",
        dry_run=False,
        override=False,
        selected_phases=["03"],
        stopped_at="03",
    )
    calls: list[tuple[str, bool]] = []

    def fake_curate(cfg, *, run_id, upload, **kwargs):  # noqa: ARG001
        calls.append((run_id, upload))
        return SimpleNamespace(root=work / "results" / "latest"), None, None

    monkeypatch.setattr("buduunkhad.cli.run_pipeline", lambda *args, **kwargs: manifest)
    monkeypatch.setattr("buduunkhad.cli._curate_and_upload_results", fake_curate)

    result = runner.invoke(app, ["run", "--config", str(config_path), "--only", "03"])

    assert result.exit_code == 0, result.output
    assert "Stopped at phase 03" in result.output
    assert "Curated results:" in result.output
    assert calls == [(manifest.run_id, True)]
