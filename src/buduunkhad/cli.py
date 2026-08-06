"""Typer CLI for the Buduunkhad pipeline.

buduunkhad list                 # show the phase registry
buduunkhad info                 # show project constants
buduunkhad validate             # check raw inputs are present
buduunkhad run --dry-run        # build the full tree + scaffolding (no data)
buduunkhad run --from 00 --to 01
buduunkhad results --run-id ID  # curate declared outputs from one sealed run
buduunkhad phase00 / phase01 / ... --dry-run   # run a single phase
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Literal, cast

import typer

from buduunkhad.ai_cli import ai_app
from buduunkhad.config import ProjectConfig
from buduunkhad.core.evidence_manifest import (
    EvidenceAuthorityResolver,
    EvidenceExecutionMode,
    EvidenceManifestError,
    EvidenceOrigin,
    EvidenceRole,
    register_pipeline_evidence,
)
from buduunkhad.core.execution_policy import (
    ExecutionMode,
    ExecutionPolicyError,
)
from buduunkhad.core.local_evidence_intake import register_local_evidence
from buduunkhad.core.raw_guard import RawIntegrityError
from buduunkhad.core.run_storage import RunStorageError
from buduunkhad.pipeline import (
    PHASE_CLASSES,
    MissingRawDataError,
    PathTooLongError,
    SelectionError,
    build_registry,
    load_project,
    run_pipeline,
    select_phases,
    validate_raw_inputs,
)
from buduunkhad.readiness_cli import readiness_app
from buduunkhad.runtime_env import LocalEnvError, load_repository_env

# Run-start failures that should surface as a clean red message + non-zero exit.
_RUN_ERRORS = (
    MissingRawDataError,
    PathTooLongError,
    RawIntegrityError,
    SelectionError,
    RunStorageError,
    EvidenceManifestError,
    ExecutionPolicyError,
)
_PHASE_COMMAND_ERRORS = (ValueError,) + _RUN_ERRORS

app = typer.Typer(
    add_completion=False,
    help="Buduunkhad / XV-023222 exploration workflow pipeline (phases 00-99).",
    no_args_is_help=True,
)
app.add_typer(ai_app, name="ai")
app.add_typer(readiness_app, name="readiness")
evidence_app = typer.Typer(
    add_completion=False,
    help="Verify immutable evidence authority selected by manifest identity.",
)
app.add_typer(evidence_app, name="evidence")

_CONFIG_OPT = typer.Option("config/project.yaml", "--config", "-c", help="Path to project.yaml.")


def _echo_manifest(manifest, runs_root: Path) -> None:
    typer.echo(f"\nRun {manifest.run_id}  (dry_run={manifest.dry_run})")
    typer.echo("-" * 72)
    for p in manifest.phases:
        gate = p.gate_status or "-"
        if p.gate_provisional:
            gate = f"{gate} (provisional)"
        line = (
            f"  {p.phase_id}  {p.status:<16} mode={p.execution_mode.value:<18} "
            f"gate={gate:<20} {p.name}"
        )
        typer.echo(line)
        if p.gate_provisional and p.gate_reason:
            typer.echo(f"        · {p.gate_reason}")
        if p.error:
            typer.echo(f"        ! {p.error}")
    for w in manifest.warnings:
        typer.secho(f"  ! warning: {w}", fg="yellow")
    if manifest.stopped_at:
        typer.echo(f"\nStopped at phase {manifest.stopped_at}.")
    typer.echo(f"\nManifest: {runs_root / manifest.run_id / 'run_manifest.json'}")
    typer.echo(f"Log:      {runs_root / manifest.run_id / 'logs' / 'run.log'}")


def _curate_and_upload_results(
    cfg: ProjectConfig,
    *,
    run_id: str,
    upload: bool,
    review_project: Path | None = None,
    review_packages: tuple[Path, ...] = (),
):
    from buduunkhad.core.results_upload import ResultsUploadError, upload_results_view
    from buduunkhad.core.results_view import materialize_results_view
    from buduunkhad.geospatial_ai.path_safety import StorageRoots

    roots = StorageRoots.from_environment(raw_root=cfg.raw_root, project_root=cfg.project_root)
    result = materialize_results_view(
        project_name=cfg.project.name,
        raw_root=cfg.raw_root,
        output_root=cfg.output_root,
        runs_root=cfg.runs_root,
        results_root=cfg.results_root,
        run_id=run_id,
        snapshot_root=roots.snapshot_root,
        review_project=review_project,
        review_packages=review_packages,
    )
    protected_roots = (
        cfg.raw_root,
        cfg.output_root,
        cfg.runs_root,
        cfg.evidence_root,
        cfg.results_root,
    ) + ((cfg.phase05_source_root,) if cfg.phase05_source_root is not None else ())
    mirrored = (
        upload_results_view(
            result.root,
            cfg.results_mirror_root,
            protected_roots=protected_roots
            + ((cfg.results_upload_root,) if cfg.results_upload_root is not None else ()),
        )
        if cfg.results_mirror_root is not None
        else None
    )
    try:
        uploaded = (
            upload_results_view(
                mirrored.destination if mirrored is not None else result.root,
                cfg.results_upload_root,
                protected_roots=protected_roots
                + ((cfg.results_mirror_root,) if cfg.results_mirror_root is not None else ()),
            )
            if upload and cfg.results_upload_root is not None
            else None
        )
    except ResultsUploadError as exc:
        if mirrored is not None:
            raise ResultsUploadError(
                f"local mirror remains verified at {mirrored.destination}; "
                f"Drive delivery failed: {exc}"
            ) from exc
        raise
    return result, mirrored, uploaded


@app.command("list")
def list_phases() -> None:
    """List the registered phases in workflow order."""
    typer.echo("Registered phases (00 -> 99):")
    for cls in PHASE_CLASSES:
        built = "BUILD" if cls.mode == "build" else "ORCH "
        typer.echo(f"  {cls.id}  [{built}]  {cls.name}")


@app.command("info")
def info(config: Path = _CONFIG_OPT) -> None:
    """Show project constants and resolved paths."""
    cfg, register = load_project(config)
    typer.echo(
        f"Project:        {cfg.project.name} ({cfg.project.project_code} / {cfg.project.license_code})"
    )
    typer.echo(f"Project slug:   {cfg.project.storage_slug}")
    if cfg.project_root is not None:
        typer.echo(f"Project root:   {cfg.project_root}")
    typer.echo(f"Target CRS:     {cfg.crs.target_name} ({cfg.crs.target_authority})")
    typer.echo(f"Raw root:       {cfg.raw_root}")
    typer.echo(f"Output root:    {cfg.output_root}")
    typer.echo(f"Runs root:      {cfg.runs_root}")
    typer.echo(f"Evidence root:  {cfg.evidence_root}")
    typer.echo(f"Results root:   {cfg.results_root}")
    if cfg.results_mirror_root is not None:
        typer.echo(f"Local mirror:   {cfg.results_mirror_root / cfg.project.name}")
    if cfg.results_upload_root is not None:
        typer.echo(f"Drive target:   {cfg.results_upload_root / cfg.project.name}")
    typer.echo(f"Register:       {cfg.register_path}  ({len(register)} inputs)")
    typer.echo(f"Buffers (m):    {cfg.boundary.buffers_m}")
    typer.echo(f"Master layers:  {len(cfg.master_gpkg_layers)}")


@app.command("validate")
def validate(config: Path = _CONFIG_OPT) -> None:
    """Check that every registered raw input is present under raw_root."""
    cfg, register = load_project(config)

    # Manifest coverage (provenance + size cross-check) when a manifest is configured.
    if cfg.manifest_path and cfg.manifest_path.exists():
        from buduunkhad.core.ingest import coverage, load_manifest

        manifest = load_manifest(cfg.manifest_path)
        cov = coverage(register, manifest, cfg.raw_root)
        typer.echo(
            f"Manifest: {len(manifest)} entries | local present {len(cov.present)}, "
            f"missing {len(cov.missing)}, size-mismatch {len(cov.size_mismatch)}"
        )
        for name, exp, got in cov.size_mismatch[:10]:
            typer.secho(f"  ~ size differs: {name} (manifest {exp}, local {got})", fg="yellow")

    missing = validate_raw_inputs(register, cfg.raw_root)
    if not missing:
        typer.secho(f"OK: all {len(register)} raw inputs present under {cfg.raw_root}", fg="green")
        raise typer.Exit(0)

    # Partition into acknowledged gaps (manifest-flagged absent, e.g. #23 EULA) vs unexpected
    # ones, mirroring run_pipeline: acknowledged -> yellow + exit 0; unexpected -> red + exit 1.
    acknowledged: set[str] = set()
    if cfg.manifest_path and cfg.manifest_path.exists():
        from buduunkhad.core.ingest import acknowledged_absent, load_manifest

        acknowledged = acknowledged_absent(load_manifest(cfg.manifest_path))
    ack = [m for m in missing if m in acknowledged]
    unexpected = [m for m in missing if m not in acknowledged]

    if ack:
        typer.secho(f"{len(ack)} acknowledged data gap(s) (manifest-flagged absent):", fg="yellow")
        for name in ack:
            typer.echo(f"  ~ {name}")
    if unexpected:
        typer.secho(
            f"MISSING {len(unexpected)} / {len(register)} raw inputs under {cfg.raw_root}:",
            fg="red",
        )
        for name in unexpected:
            typer.echo(f"  - {name}")
        raise typer.Exit(1)
    typer.secho(
        f"OK: all raw inputs present or acknowledged-absent under {cfg.raw_root}", fg="green"
    )
    raise typer.Exit(0)


@app.command("methodology-status")
def methodology_status(config: Path = _CONFIG_OPT) -> None:
    """Print master-first operational readiness and registered missing inputs as JSON."""

    from buduunkhad.geospatial_ai.readiness import (
        build_methodology_readiness_report,
        render_methodology_readiness_report,
    )

    cfg, _register = load_project(config)
    if cfg.manifest_path is None:
        typer.secho("Project configuration has no raw manifest path.", fg="red", err=True)
        raise typer.Exit(2)
    try:
        report = build_methodology_readiness_report(cfg.manifest_path)
    except (OSError, ValueError) as exc:
        typer.secho(str(exc), fg="red", err=True)
        raise typer.Exit(2) from exc
    typer.echo(render_methodology_readiness_report(report), nl=False)


@app.command("publish")
def publish_deliverables(
    config: Path = _CONFIG_OPT,
    label: str = typer.Option(
        None, "--label", help="Version label for the published folder (default: timestamp)."
    ),
    supersedes: str | None = typer.Option(
        None,
        "--supersedes",
        help="Publication ID explicitly superseded by this package.",
    ),
    source_run: list[str] | None = typer.Option(
        None,
        "--source-run",
        help="Select an exact source run as PHASE=RUN_ID; repeat for multiple phases.",
    ),
    run_id: str | None = typer.Option(
        None,
        "--run-id",
        help="Publish one exact run-isolated source; required for new v2 run manifests.",
    ),
) -> None:
    """Copy one exact sealed run's deliverables to BUDUUNKHAD_PUBLISH_ROOT.

    New run-isolated manifests require ``--run-id`` and are read from ``runs/<id>/phases`` rather
    than the mutable output compatibility view. Legacy path-only manifests retain the existing
    per-phase selectors for backward compatibility. Raw working copies are always excluded.
    """
    cfg, _register = load_project(config)
    from buduunkhad.geospatial_ai.path_safety import PathSafetyError, StorageRoots

    try:
        publish_root = StorageRoots.from_environment(
            raw_root=cfg.raw_root,
            project_root=cfg.project_root,
        ).require_publish_root()
    except PathSafetyError as exc:
        typer.secho(
            str(exc),
            fg="red",
        )
        raise typer.Exit(2) from exc
    from buduunkhad.core.publish import PublishError
    from buduunkhad.core.publish import publish as do_publish

    label = label or datetime.now().strftime("%Y%m%dT%H%M%S")
    source_runs: dict[str, str] = {}
    for selector in source_run or []:
        phase_id, separator, run_id = selector.partition("=")
        if (
            separator != "="
            or phase_id not in {phase.id for phase in PHASE_CLASSES}
            or not run_id
            or phase_id in source_runs
        ):
            typer.secho(
                "Each --source-run must be a unique registered PHASE=RUN_ID selector.", fg="red"
            )
            raise typer.Exit(2)
        source_runs[phase_id] = run_id
    try:
        result = do_publish(
            cfg.output_root,
            publish_root,
            label,
            runs_root=cfg.runs_root,
            project_config_path=config,
            superseded_publication_id=supersedes,
            source_runs=source_runs,
            run_id=run_id,
        )
    except PublishError as exc:
        typer.secho(str(exc), fg="red")
        raise typer.Exit(2) from exc
    typer.secho(f"Published {len(result.files)} deliverable(s) to:", fg="green")
    typer.echo(f"  {result.dest}")
    typer.echo(f"  (skipped {result.skipped_working_copies} raw working-copy file(s) by design)")
    typer.echo("Share that folder in Google Drive to give teammates access.")


@app.command("results")
def curate_results(
    run_id: str = typer.Option(
        ...,
        "--run-id",
        help="Exact sealed pipeline run to expose in results/latest.",
    ),
    review_project: Path | None = typer.Option(
        None,
        "--review-project",
        help="Optional integrated .qgz under the configured work/runs root.",
    ),
    review_package: list[Path] | None = typer.Option(
        None,
        "--review-package",
        help="Verified Phase 03 AI review package to include; repeat for multiple packages.",
    ),
    upload: bool = typer.Option(
        True,
        "--upload/--no-upload",
        help="Copy the verified local mirror to the configured Drive root.",
    ),
    config: Path = _CONFIG_OPT,
) -> None:
    """Build the small operator-facing results/latest view from declared run outputs."""

    from buduunkhad.core.results_upload import ResultsUploadError
    from buduunkhad.core.results_view import ResultsViewError

    cfg, _register = load_project(config)
    try:
        result, mirrored, uploaded = _curate_and_upload_results(
            cfg,
            run_id=run_id,
            upload=upload,
            review_project=review_project,
            review_packages=tuple(review_package or ()),
        )
    except (ResultsUploadError, ResultsViewError) as exc:
        typer.secho(str(exc), fg="red", err=True)
        raise typer.Exit(2) from exc
    action = "Created" if result.created else "Verified"
    typer.secho(f"{action} curated results:", fg="green")
    typer.echo(f"  {result.root}")
    typer.echo(
        f"  {len(result.manifest.phases)} phase(s), "
        f"{len(result.manifest.files)} declared result file(s)"
    )
    typer.echo(f"  Source run: {result.manifest.source_run_id}")
    if mirrored is not None:
        mirror_action = "Copied" if mirrored.created else "Verified"
        typer.secho(f"{mirror_action} local results mirror:", fg="green")
        typer.echo(f"  {mirrored.destination}")
    if uploaded is not None:
        upload_action = "Copied" if uploaded.created else "Verified"
        typer.secho(f"{upload_action} Google Drive results:", fg="green")
        typer.echo(f"  {uploaded.destination}")


@app.command("backup-raw")
def backup_raw(
    config: Path = _CONFIG_OPT,
    label: str = typer.Option("v01", "--label", help="Version label for the raw backup folder."),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Overwrite an existing backup with this label."
    ),
) -> None:
    """Back up the COMPLETE raw archive to BUDUUNKHAD_PUBLISH_ROOT, checksum-verified.

    Creates ``Raw_Archive_Backup_<label>/`` with the full raw tree under ``0_Raw_Data/`` plus the
    Phase-00 checksum register + integrity artifacts, then re-hashes every file against the
    register. Unlike ``publish`` (deliverables only), this deliberately backs up the raw data so
    teammates have an immutable, verifiable copy separate from the working source. Raw stays
    read-only. Run Phase 00 first — it produces the checksum register.
    """
    from buduunkhad.core import paths
    from buduunkhad.core.publish import PublishError, backup_raw_archive
    from buduunkhad.geospatial_ai.path_safety import PathSafetyError, StorageRoots
    from buduunkhad.pipeline import baseline_checksum_path

    cfg, _register = load_project(config)
    try:
        publish_root = StorageRoots.from_environment(
            raw_root=cfg.raw_root,
            project_root=cfg.project_root,
        ).require_publish_root()
    except PathSafetyError as exc:
        typer.secho(str(exc), fg="red", err=True)
        raise typer.Exit(2) from exc
    register_csv = baseline_checksum_path(cfg)
    p00 = paths.phase_dir(cfg.output_root, "00")
    prefix = cfg.register_prefix
    integrity = [
        p00 / f"{prefix}_79Input_Master_Inventory.xlsx",
        p00 / f"{prefix}_Raw_Data_Integrity_Log.xlsx",
        p00 / f"{prefix}_Source_Data_Readme.docx",
    ]
    try:
        res = backup_raw_archive(
            cfg.raw_root,
            register_csv,
            publish_root,
            label,
            integrity_files=integrity,
            overwrite=overwrite,
        )
    except PublishError as exc:
        typer.secho(str(exc), fg="red")
        raise typer.Exit(1) from exc
    typer.secho(
        f"Raw backup: {res.files} file(s), {res.verified} verified byte-identical.", fg="green"
    )
    typer.echo(f"  {res.dest}")
    typer.echo("Share that folder in Google Drive to give teammates a verified, immutable copy.")


def _parse_input_run_selectors(selectors: list[str] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    known = {phase.id for phase in PHASE_CLASSES}
    for selector in selectors or []:
        phase_id, separator, run_id = selector.partition("=")
        if separator != "=" or phase_id not in known or not run_id or phase_id in result:
            raise SelectionError(
                "Each --input-run must be a unique registered predecessor PHASE=RUN_ID selector."
            )
        result[phase_id] = run_id
    return result


def _parse_phase_mode_selectors(selectors: list[str] | None) -> dict[str, ExecutionMode]:
    result: dict[str, ExecutionMode] = {}
    known = {phase.id for phase in PHASE_CLASSES}
    for selector in selectors or []:
        phase_id, separator, raw_mode = selector.partition("=")
        if separator != "=" or phase_id not in known or not raw_mode or phase_id in result:
            raise SelectionError("Each --phase-mode must be a unique selected PHASE=MODE selector.")
        try:
            result[phase_id] = ExecutionMode(raw_mode)
        except ValueError as exc:
            raise SelectionError(f"Unknown execution mode: {raw_mode}") from exc
    return result


@app.command("run")
def run(
    config: Path = _CONFIG_OPT,
    ai_config: Path | None = typer.Option(
        None,
        "--ai-config",
        exists=True,
        dir_okay=False,
        help="AI profile; defaults to sibling ai.openai.yaml when that file exists.",
    ),
    from_: str = typer.Option(None, "--from", help="First phase id (e.g. 00)."),
    to: str = typer.Option(None, "--to", help="Last phase id (e.g. 01)."),
    only: str = typer.Option(None, "--only", help="Comma-separated phase ids (e.g. 00,01)."),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Build tree + scaffolding; no raw data needed."
    ),
    override: bool = typer.Option(
        False,
        "--override",
        help="Retired: using this flag fails; supply an exact scoped authorization instead.",
    ),
    resume: str | None = typer.Option(
        None,
        "--resume",
        help="Resume one exact run ID after revalidating all execution identities.",
    ),
    evidence_manifest: list[str] | None = typer.Option(
        None,
        "--evidence-manifest",
        help="Select one immutable evidence manifest ID (repeatable).",
    ),
    input_run: list[str] | None = typer.Option(
        None,
        "--input-run",
        help="Bind an external predecessor phase as PHASE=RUN_ID (repeatable).",
    ),
    phase_mode: list[str] | None = typer.Option(
        None,
        "--phase-mode",
        help="Request a phase purpose as PHASE=MODE (repeatable); defaults are conservative.",
    ),
    authorization: list[Path] | None = typer.Option(
        None,
        "--authorization",
        help="Load one immutable scoped execution-authorization JSON file (repeatable).",
    ),
    upload_results: bool = typer.Option(
        True,
        "--upload-results/--no-upload-results",
        help="After a real run, curate and upload outputs when an upload root is configured.",
    ),
    live_ai: bool = typer.Option(
        False,
        "--ai/--offline-ai",
        help="Explicitly execute or skip the configured AI-first Phase 03 provider workflow.",
    ),
    ai_approved_by: str | None = typer.Option(
        None,
        "--ai-approved-by",
        help="Named person authorizing the configured Phase 03 source package egress.",
    ),
    ai_approval_note: str = typer.Option(
        "Run-scoped approval for the configured Phase 03 AI-first source packages.",
        "--ai-approval-note",
        help="Reason recorded in each exact package-level egress approval.",
    ),
    ai_source: list[str] | None = typer.Option(
        None,
        "--ai-source",
        help=(
            "Configured Phase 03 source ID to execute; repeatable. Required when the AI profile "
            "contains multiple sources so a run cannot egress every map accidentally."
        ),
    ),
) -> None:
    """Run deterministic phases and the configured Phase 03 AI-first workflow."""
    try:
        load_repository_env(config)
    except LocalEnvError as exc:
        typer.secho(f"Local environment error: {exc}", fg="red", err=True)
        raise typer.Exit(2) from exc
    resolved_ai_config = ai_config
    if resolved_ai_config is None:
        candidate = config.with_name("ai.openai.yaml")
        if candidate.is_file():
            resolved_ai_config = candidate
    cfg, register = load_project(config, ai_config_path=resolved_ai_config)
    only_list = [s.strip() for s in only.split(",") if s.strip()] if only else None
    try:
        selected = select_phases(build_registry(), from_=from_, to=to, only=only_list)
        ai_selected = (
            not dry_run
            and live_ai
            and cfg.ai.enabled
            and cfg.ai.phase03_workflow is not None
            and any(phase.id == "03" for phase in selected)
        )
        if ai_selected and not (ai_approved_by or "").strip():
            raise SelectionError("AI-first Phase 03 requires --ai-approved-by for this exact run")
        selected_ai_source_ids: tuple[str, ...] = ()
        if ai_selected:
            workflow = cfg.ai.phase03_workflow
            assert workflow is not None
            if ai_source:
                selected_ai_source_ids = tuple(ai_source)
            elif len(workflow.configured_sources) == 1:
                selected_ai_source_ids = (workflow.configured_sources[0].source_id,)
            else:
                raise SelectionError(
                    "AI profile contains multiple Phase 03 sources; select each intended source "
                    "with --ai-source"
                )
            if len(selected_ai_source_ids) != len(set(selected_ai_source_ids)):
                raise SelectionError("--ai-source values must be unique")
            for source_id in selected_ai_source_ids:
                try:
                    workflow.source(source_id)
                except ValueError as exc:
                    raise SelectionError(str(exc)) from exc
        input_runs = _parse_input_run_selectors(input_run)
        phase_modes = _parse_phase_mode_selectors(phase_mode)
        manifest = run_pipeline(
            cfg,
            register,
            from_=from_,
            to=to,
            only=only_list,
            dry_run=dry_run,
            override=override,
            run_id=resume,
            resume=resume is not None,
            evidence_manifest_ids=evidence_manifest,
            input_phase_runs=input_runs,
            phase_modes=phase_modes,
            authorization_paths=authorization,
        )
    except _RUN_ERRORS as exc:
        typer.secho(str(exc), fg="red")
        raise typer.Exit(2) from exc
    _echo_manifest(manifest, cfg.runs_root)
    if manifest.error:
        typer.secho(f"Run failed: {manifest.error}", fg="red", err=True)
        raise typer.Exit(2)
    review_project: Path | None = None
    review_packages: tuple[Path, ...] = ()
    if ai_selected:
        from buduunkhad.geospatial_ai.ai_first import (
            run_phase03_ai_first,
            run_phase03_ai_first_batch,
        )

        try:
            workflow = cfg.ai.phase03_workflow
            assert workflow is not None
            if len(selected_ai_source_ids) == 1:
                ai_manifest_path, ai_manifest = run_phase03_ai_first(
                    cfg,
                    pipeline_run_id=manifest.run_id,
                    approved_by=cast(str, ai_approved_by),
                    approval_note=ai_approval_note,
                    source_id=selected_ai_source_ids[0],
                )
                run_directory = cfg.runs_root / ai_manifest.ai_run_id
                review_project = run_directory / ai_manifest.integrated_project_path
                review_packages = (run_directory / ai_manifest.review_package_path,)
                typer.secho("AI-first Phase 03 completed.", fg="green")
                typer.echo(f"AI attempt: {ai_manifest.ai_run_id}")
                typer.echo(f"AI manifest: {ai_manifest_path}")
                typer.echo(f"Integrated QGIS review: {review_project}")
            else:
                batch_path, batch = run_phase03_ai_first_batch(
                    cfg,
                    pipeline_run_id=manifest.run_id,
                    approved_by=cast(str, ai_approved_by),
                    approval_note=ai_approval_note,
                    source_ids=selected_ai_source_ids,
                )
                review_packages = tuple(
                    cfg.runs_root / item.review_package_path for item in batch.sessions
                )
                typer.secho("AI-first Phase 03 batch completed.", fg="green")
                typer.echo(f"AI batch: {batch.batch_run_id}")
                typer.echo(f"AI batch manifest: {batch_path}")
                for item in batch.sessions:
                    typer.echo(
                        f"{item.source_id} QGIS review: "
                        f"{cfg.runs_root / item.integrated_project_path}"
                    )
        except (OSError, ValueError, RuntimeError) as exc:
            typer.secho(f"AI-first Phase 03 failed: {exc}", fg="red", err=True)
            raise typer.Exit(2) from exc
    elif (
        not dry_run
        and not live_ai
        and cfg.ai.enabled
        and any(phase.id == "03" for phase in selected)
    ):
        typer.secho(
            "AI-first Phase 03 not executed; use --ai for live provider calls.", fg="yellow"
        )
    if not manifest.dry_run and (
        cfg.results_mirror_root is not None or cfg.results_upload_root is not None
    ):
        from buduunkhad.core.results_upload import ResultsUploadError
        from buduunkhad.core.results_view import ResultsViewError

        try:
            results, mirrored, uploaded = _curate_and_upload_results(
                cfg,
                run_id=manifest.run_id,
                upload=upload_results,
                review_project=review_project,
                review_packages=review_packages,
            )
        except (ResultsUploadError, ResultsViewError) as exc:
            typer.secho(f"Automatic results upload failed after the run: {exc}", fg="red")
            raise typer.Exit(2) from exc
        typer.echo(f"Curated results: {results.root}")
        if mirrored is not None:
            mirror_action = "Copied" if mirrored.created else "Verified"
            typer.echo(f"{mirror_action} local results mirror: {mirrored.destination}")
        if uploaded is not None:
            upload_action = "Copied" if uploaded.created else "Verified"
            typer.echo(f"{upload_action} Google Drive results: {uploaded.destination}")


def _make_phase_command(phase_id: str, phase_name: str):
    def _cmd(
        config: Path = _CONFIG_OPT,
        dry_run: bool = typer.Option(
            False, "--dry-run", help="Build scaffolding; no raw data needed."
        ),
        override: bool = typer.Option(
            False,
            "--override",
            help="Retired: using this flag fails; supply an exact scoped authorization instead.",
        ),
        evidence_manifest: list[str] | None = typer.Option(
            None,
            "--evidence-manifest",
            help="Select one immutable evidence manifest ID (repeatable).",
        ),
        input_run: list[str] | None = typer.Option(
            None,
            "--input-run",
            help="Bind an external predecessor phase as PHASE=RUN_ID (repeatable).",
        ),
        execution_mode: str | None = typer.Option(
            None,
            "--execution-mode",
            help="Request the phase execution purpose; otherwise use the conservative default.",
        ),
        authorization: list[Path] | None = typer.Option(
            None,
            "--authorization",
            help="Load one immutable scoped execution-authorization JSON file (repeatable).",
        ),
    ) -> None:
        cfg, register = load_project(config)
        try:
            input_runs = _parse_input_run_selectors(input_run)
            requested_mode = (
                {phase_id: ExecutionMode(execution_mode)} if execution_mode is not None else None
            )
            manifest = run_pipeline(
                cfg,
                register,
                only=[phase_id],
                dry_run=dry_run,
                override=override,
                evidence_manifest_ids=evidence_manifest,
                input_phase_runs=input_runs,
                phase_modes=requested_mode,
                authorization_paths=authorization,
            )
        except _PHASE_COMMAND_ERRORS as exc:
            typer.secho(str(exc), fg="red")
            raise typer.Exit(2) from exc
        _echo_manifest(manifest, cfg.runs_root)

    _cmd.__doc__ = f"Run phase {phase_id} - {phase_name}."
    return _cmd


@evidence_app.command("verify")
def verify_evidence(
    manifest_id: list[str] = typer.Option(
        ...,
        "--manifest-id",
        help="Immutable evidence manifest ID to verify (repeatable).",
    ),
    config: Path = _CONFIG_OPT,
) -> None:
    """Reconcile selected evidence manifests with current source authority and bytes."""

    cfg, _register = load_project(config)
    try:
        resolved = EvidenceAuthorityResolver(
            runs_root=cfg.runs_root,
            evidence_root=cfg.evidence_root,
            target_epsg=cfg.target_epsg,
        ).resolve_selected(manifest_id)
    except EvidenceManifestError as exc:
        typer.secho(str(exc), fg="red")
        raise typer.Exit(2) from exc
    typer.echo(f"Verified {len(manifest_id)} evidence manifest(s), {len(resolved)} record(s).")


@evidence_app.command("register-run-layer")
def register_run_layer_evidence(
    source_run: str = typer.Option(..., "--source-run", help="Exact sealed source run ID."),
    artifact_path: str = typer.Option(
        ..., "--artifact-path", help="Run-relative sealed GeoPackage path."
    ),
    layer_name: str = typer.Option(..., "--layer", help="Exact source GeoPackage layer."),
    role: str = typer.Option(..., "--role", help="Explicit evidence role."),
    phase: list[str] = typer.Option(
        ..., "--phase", help="Eligible phase ID (03 or 04; repeatable)."
    ),
    mode: list[str] = typer.Option(..., "--mode", help="Eligible execution mode (repeatable)."),
    target_layer: str | None = typer.Option(
        None, "--target-layer", help="Exact Phase 03 legacy-schema target layer, when applicable."
    ),
    origin: str = typer.Option(
        EvidenceOrigin.HUMAN_DIGITIZED.value,
        "--origin",
        help="deterministic-pipeline or human-digitized.",
    ),
    evidence_id: str | None = typer.Option(None, "--evidence-id"),
    actor: str = typer.Option(
        ...,
        "--actor",
        help="Identity of the person registering this support-evidence role and eligibility.",
    ),
    reason: str = typer.Option(
        ...,
        "--reason",
        help="Auditable reason for registering this exact support-evidence use.",
    ),
    limitation: list[str] | None = typer.Option(
        None, "--limitation", help="Evidence limitation (repeatable)."
    ),
    config: Path = _CONFIG_OPT,
) -> None:
    """Register one exact sealed run layer as support evidence; never as scientific approval."""

    cfg, _register = load_project(config)
    try:
        if not phase or any(value not in {"03", "04"} for value in phase):
            raise ValueError("eligible phases must contain only 03 or 04")
        eligible_phases = cast(tuple[Literal["03", "04"], ...], tuple(phase))
        manifest = register_pipeline_evidence(
            runs_root=cfg.runs_root,
            evidence_root=cfg.evidence_root,
            target_epsg=cfg.target_epsg,
            source_run_id=source_run,
            artifact_path=artifact_path,
            layer_name=layer_name,
            evidence_role=EvidenceRole(role),
            origin=EvidenceOrigin(origin),
            eligible_phases=eligible_phases,
            eligible_modes=tuple(EvidenceExecutionMode(value) for value in mode),
            target_layer_name=target_layer,
            evidence_id=evidence_id,
            limitations=tuple(limitation or ()),
            registered_by=actor,
            registration_reason=reason,
        )
    except (EvidenceManifestError, ValueError) as exc:
        typer.secho(str(exc), fg="red")
        raise typer.Exit(2) from exc
    typer.echo(f"Registered sealed support evidence: {manifest.manifest_id}")
    typer.echo("This record does not claim scientific approval or Phase 04 authority.")


@evidence_app.command("import-local-layer")
def import_local_layer_evidence(
    source: Path = typer.Option(..., "--source", help="Local GeoPackage or shapefile to copy."),
    layer_name: str | None = typer.Option(
        None, "--layer", help="Exact source layer; required for a multi-layer GeoPackage."
    ),
    role: str = typer.Option(..., "--role", help="Explicit evidence role."),
    phase: list[str] = typer.Option(
        ..., "--phase", help="Eligible phase ID (03 or 04; repeatable)."
    ),
    mode: list[str] = typer.Option(..., "--mode", help="Eligible execution mode (repeatable)."),
    target_layer: str | None = typer.Option(
        None, "--target-layer", help="Exact Phase 03 target layer, when applicable."
    ),
    origin: str = typer.Option(
        EvidenceOrigin.HUMAN_DIGITIZED.value,
        "--origin",
        help="deterministic-pipeline or human-digitized.",
    ),
    evidence_id: str | None = typer.Option(None, "--evidence-id"),
    actor: str = typer.Option(..., "--actor", help="Person registering this local evidence."),
    reason: str = typer.Option(..., "--reason", help="Auditable registration reason."),
    limitation: list[str] | None = typer.Option(
        None, "--limitation", help="Evidence limitation (repeatable)."
    ),
    config: Path = _CONFIG_OPT,
) -> None:
    """Copy one local GIS layer into immutable evidence authority and register it."""

    cfg, _register = load_project(config)
    try:
        if not phase or any(value not in {"03", "04"} for value in phase):
            raise ValueError("eligible phases must contain only 03 or 04")
        eligible_phases = cast(tuple[Literal["03", "04"], ...], tuple(phase))
        manifest = register_local_evidence(
            runs_root=cfg.runs_root,
            evidence_root=cfg.evidence_root,
            target_epsg=cfg.target_epsg,
            source_path=source,
            source_layer=layer_name,
            evidence_role=EvidenceRole(role),
            origin=EvidenceOrigin(origin),
            eligible_phases=eligible_phases,
            eligible_modes=tuple(EvidenceExecutionMode(value) for value in mode),
            target_layer_name=target_layer,
            evidence_id=evidence_id,
            limitations=tuple(limitation or ()),
            registered_by=actor,
            registration_reason=reason,
        )
    except (EvidenceManifestError, ValueError) as exc:
        typer.secho(str(exc), fg="red")
        raise typer.Exit(2) from exc
    typer.echo(f"Registered immutable local support evidence: {manifest.manifest_id}")
    typer.echo("The source was copied; this record does not claim scientific approval.")


# Register one command per phase: phase00, phase01, ... phase99.
for _cls in PHASE_CLASSES:
    app.command(f"phase{_cls.id}")(_make_phase_command(_cls.id, _cls.name))


def main() -> None:  # pragma: no cover - console-script entry
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
