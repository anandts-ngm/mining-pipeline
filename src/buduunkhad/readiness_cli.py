"""Offline commands for measured readiness evidence and separate human attestations."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import typer

readiness_app = typer.Typer(
    add_completion=False,
    help="Create and resolve exact-source operational readiness records.",
    no_args_is_help=True,
)


def _abort(exc: Exception) -> None:
    typer.secho(str(exc), fg="red", err=True)
    raise typer.Exit(2) from exc


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


@readiness_app.command("boundary-attest")
def boundary_attest(
    record: Path = typer.Option(..., "--record", exists=True, dir_okay=False),
    reviewer: str = typer.Option(..., "--reviewer"),
    role: str = typer.Option(..., "--role"),
    authorization_id: str = typer.Option(..., "--authorization-id"),
    reviewed_at: str = typer.Option(..., "--reviewed-at"),
    decision: str = typer.Option(..., "--decision"),
    rationale: str = typer.Option(..., "--rationale"),
    limitation: list[str] | None = typer.Option(None, "--limitation"),
    output: Path = typer.Option(..., "--output", dir_okay=False),
) -> None:
    """Record one named review of an exact Phase 01 boundary validation."""

    from buduunkhad.core.boundary_validation import (
        BoundaryReviewDecision,
        BoundaryReviewerRole,
        create_boundary_review,
        write_boundary_authority_record,
    )

    try:
        attestation = create_boundary_review(
            record,
            reviewer=reviewer,
            reviewer_role=BoundaryReviewerRole(role),
            reviewer_authorization_id=authorization_id,
            reviewed_at=datetime.fromisoformat(reviewed_at.replace("Z", "+00:00")),
            decision=BoundaryReviewDecision(decision),
            rationale=rationale,
            limitations=tuple(limitation or ()),
        )
        write_boundary_authority_record(attestation, output)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Boundary review attestation: {output}")
    typer.echo(f"Attestation ID: {attestation.attestation_id}")


@readiness_app.command("boundary-resolve")
def boundary_resolve(
    record: Path = typer.Option(..., "--record", exists=True, dir_okay=False),
    source_phase_root: Path = typer.Option(
        ..., "--source-phase-root", exists=True, file_okay=False
    ),
    phase_root: Path = typer.Option(..., "--phase-root", exists=True, file_okay=False),
    attestation: list[Path] = typer.Option(
        ...,
        "--attestation",
        exists=True,
        dir_okay=False,
        help="Exactly two attestations: data custodian and qualified geospatial reviewer.",
    ),
    output: Path = typer.Option(..., "--output", dir_okay=False),
) -> None:
    """Resolve the two exact boundary reviews after revalidating all measured bytes."""

    from buduunkhad.core.boundary_validation import (
        resolve_boundary_acceptance,
        write_boundary_authority_record,
    )

    try:
        acceptance = resolve_boundary_acceptance(
            record,
            source_phase_root=source_phase_root,
            phase_root=phase_root,
            attestation_paths=tuple(attestation),
        )
        write_boundary_authority_record(acceptance, output)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Accepted boundary record: {output}")
    typer.echo(f"Acceptance ID: {acceptance.acceptance_id}")


@readiness_app.command("georef-record")
def georef_record(
    processing_run: str = typer.Option(..., "--processing-run"),
    source_run: str = typer.Option(..., "--source-run"),
    source_root: Path = typer.Option(..., "--source-root", exists=True, file_okay=False),
    source: Path = typer.Option(..., "--source", exists=True, dir_okay=False),
    derivative_root: Path = typer.Option(..., "--derivative-root", exists=True, file_okay=False),
    derivative: Path = typer.Option(..., "--derivative", exists=True, dir_okay=False),
    gcps: Path = typer.Option(..., "--gcps", exists=True, dir_okay=False),
    target_epsg: int = typer.Option(..., "--target-epsg", min=1),
    transformation: str = typer.Option(..., "--transformation"),
    resampling: str = typer.Option(..., "--resampling"),
    proposed_source_crs: str | None = typer.Option(None, "--proposed-source-crs"),
    source_crs_evidence: list[str] | None = typer.Option(None, "--source-crs-evidence"),
    distribution_finding: list[str] = typer.Option(..., "--distribution-finding"),
    limitation: list[str] = typer.Option(..., "--limitation"),
    output: Path = typer.Option(..., "--output", dir_okay=False),
) -> None:
    """Bind GCP/residual measurements to exact source and derivative bytes."""

    from buduunkhad.core.georeference import (
        GcpMeasurement,
        create_georeference_record,
        write_georeference_record,
    )

    try:
        data = json.loads(
            gcps.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
        )
        if not isinstance(data, list):
            raise ValueError("GCP input must be a JSON array")
        measurements = tuple(GcpMeasurement.model_validate(item) for item in data)
        record = create_georeference_record(
            processing_run_id=processing_run,
            source_run_id=source_run,
            source_root=source_root,
            source_path=source,
            derivative_root=derivative_root,
            derivative_path=derivative,
            proposed_source_crs=proposed_source_crs,
            source_crs_evidence=tuple(source_crs_evidence or ()),
            target_epsg=target_epsg,
            transformation=transformation,
            resampling=resampling,
            gcps=measurements,
            spatial_distribution_findings=tuple(distribution_finding),
            limitations=tuple(limitation),
        )
        write_georeference_record(record, output)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Georeference measurement record: {output}")
    typer.echo(f"Status: {record.status.value}; record ID: {record.record_id}")
    typer.echo("No scientific or reviewer acceptance was created.")


@readiness_app.command("georef-attest")
def georef_attest(
    record: Path = typer.Option(..., "--record", exists=True, dir_okay=False),
    reviewer: str = typer.Option(..., "--reviewer"),
    role: str = typer.Option(..., "--role"),
    authorization_id: str = typer.Option(..., "--authorization-id"),
    reviewed_at: str = typer.Option(..., "--reviewed-at"),
    decision: str = typer.Option(..., "--decision"),
    rationale: str = typer.Option(..., "--rationale"),
    visual_finding: list[str] = typer.Option(..., "--visual-finding"),
    limitation: list[str] | None = typer.Option(None, "--limitation"),
    output: Path = typer.Option(..., "--output", dir_okay=False),
) -> None:
    """Record one named review of an exact georeference measurement record."""

    from buduunkhad.core.georeference import (
        GeoreferenceReviewDecision,
        GeoreferenceReviewerRole,
        create_georeference_review,
        write_georeference_record,
    )

    try:
        attestation = create_georeference_review(
            record,
            reviewer=reviewer,
            reviewer_role=GeoreferenceReviewerRole(role),
            reviewer_authorization_id=authorization_id,
            reviewed_at=datetime.fromisoformat(reviewed_at.replace("Z", "+00:00")),
            decision=GeoreferenceReviewDecision(decision),
            rationale=rationale,
            visual_alignment_findings=tuple(visual_finding),
            limitations=tuple(limitation or ()),
        )
        write_georeference_record(attestation, output)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Georeference review attestation: {output}")
    typer.echo(f"Attestation ID: {attestation.attestation_id}")


@readiness_app.command("georef-resolve")
def georef_resolve(
    record: Path = typer.Option(..., "--record", exists=True, dir_okay=False),
    source_root: Path = typer.Option(..., "--source-root", exists=True, file_okay=False),
    derivative_root: Path = typer.Option(..., "--derivative-root", exists=True, file_okay=False),
    attestation: list[Path] = typer.Option(
        ...,
        "--attestation",
        exists=True,
        dir_okay=False,
        help="Exactly two attestations: geospatial reviewer and project geologist.",
    ),
    output: Path = typer.Option(..., "--output", dir_okay=False),
) -> None:
    """Resolve exact accepted reviews without granting any broader scientific authority."""

    from buduunkhad.core.georeference import (
        resolve_georeference_acceptance,
        write_georeference_record,
    )

    try:
        acceptance = resolve_georeference_acceptance(
            record,
            source_root=source_root,
            derivative_root=derivative_root,
            attestation_paths=tuple(attestation),
        )
        write_georeference_record(acceptance, output)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Accepted georeference record: {output}")
    typer.echo(f"Acceptance ID: {acceptance.acceptance_id}")


@readiness_app.command("deposit-model-assessment")
def deposit_model_assessment(
    phase03_run: str = typer.Option(..., "--phase03-run"),
    candidate_model: str = typer.Option(..., "--candidate-model"),
    evidence_manifest: list[str] = typer.Option(..., "--evidence-manifest"),
    evidence_groups: Path = typer.Option(..., "--evidence-groups", exists=True, dir_okay=False),
    missing_evidence: list[str] | None = typer.Option(None, "--missing-evidence"),
    confidence_basis: str = typer.Option(..., "--confidence-basis"),
    limitation: list[str] = typer.Option(..., "--limitation"),
    recommended_validation: list[str] = typer.Option(..., "--recommended-validation"),
    draft_score: float | None = typer.Option(None, "--draft-score", min=0, max=100),
    proposing_job_id: str | None = typer.Option(None, "--proposing-job-id"),
    proposing_response_id: str | None = typer.Option(None, "--proposing-response-id"),
    output: Path = typer.Option(..., "--output", dir_okay=False),
    config: Path = typer.Option("config/project.yaml", "--config", "-c"),
) -> None:
    """Create a structured 03A proposal from exact accepted evidence manifests."""

    from buduunkhad.config import load_config
    from buduunkhad.core.evidence_manifest import EvidenceAuthorityResolver
    from buduunkhad.core.phase03_science import (
        DepositModelEvidenceGroup,
        create_deposit_model_assessment,
        write_phase03_science_record,
    )

    try:
        project = load_config(config)
        data = json.loads(
            evidence_groups.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
        )
        if not isinstance(data, list):
            raise ValueError("evidence groups must be a JSON array")
        groups = tuple(DepositModelEvidenceGroup.model_validate(item) for item in data)
        assessment = create_deposit_model_assessment(
            phase03_run_id=phase03_run,
            resolver=EvidenceAuthorityResolver(
                runs_root=project.runs_root,
                evidence_root=project.evidence_root,
                target_epsg=project.target_epsg,
            ),
            evidence_manifest_ids=tuple(evidence_manifest),
            candidate_model=candidate_model,
            evidence_groups=groups,
            missing_evidence=tuple(missing_evidence or ()),
            confidence_basis=confidence_basis,
            limitations=tuple(limitation),
            recommended_validation=tuple(recommended_validation),
            draft_score=draft_score,
            proposing_job_id=proposing_job_id,
            proposing_response_id=proposing_response_id,
        )
        write_phase03_science_record(assessment, output)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Deposit-model assessment: {output}")
    typer.echo(f"Assessment ID: {assessment.assessment_id}")
    typer.echo("This is a structured proposal, not geologist acceptance.")


@readiness_app.command("deposit-model-critique")
def deposit_model_critique(
    assessment: Path = typer.Option(..., "--assessment", exists=True, dir_okay=False),
    critic: str = typer.Option(..., "--critic"),
    origin: str = typer.Option(..., "--origin"),
    critiqued_at: str = typer.Option(..., "--critiqued-at"),
    conclusion: str = typer.Option(..., "--conclusion"),
    finding: list[str] = typer.Option(..., "--finding"),
    critic_authorization_id: str | None = typer.Option(None, "--critic-authorization-id"),
    critique_job_id: str | None = typer.Option(None, "--critique-job-id"),
    critique_response_id: str | None = typer.Option(None, "--critique-response-id"),
    limitation: list[str] | None = typer.Option(None, "--limitation"),
    output: Path = typer.Option(..., "--output", dir_okay=False),
) -> None:
    """Create an independent critique bound to one exact 03A assessment."""

    from buduunkhad.core.phase03_science import (
        CritiqueConclusion,
        CritiqueOrigin,
        create_deposit_model_critique,
        write_phase03_science_record,
    )

    try:
        critique = create_deposit_model_critique(
            assessment,
            critic=critic,
            origin=CritiqueOrigin(origin),
            critic_authorization_id=critic_authorization_id,
            critiqued_at=datetime.fromisoformat(critiqued_at.replace("Z", "+00:00")),
            critique_job_id=critique_job_id,
            critique_response_id=critique_response_id,
            conclusion=CritiqueConclusion(conclusion),
            findings=tuple(finding),
            limitations=tuple(limitation or ()),
        )
        write_phase03_science_record(critique, output)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Deposit-model critique: {output}")
    typer.echo(f"Critique ID: {critique.critique_id}")


@readiness_app.command("deposit-model-review")
def deposit_model_review(
    assessment: Path = typer.Option(..., "--assessment", exists=True, dir_okay=False),
    critique: Path = typer.Option(..., "--critique", exists=True, dir_okay=False),
    reviewer: str = typer.Option(..., "--reviewer"),
    authorization_id: str = typer.Option(..., "--authorization-id"),
    reviewed_at: str = typer.Option(..., "--reviewed-at"),
    decision: str = typer.Option(..., "--decision"),
    accepted_model: str | None = typer.Option(None, "--accepted-model"),
    accepted_confidence: str | None = typer.Option(None, "--accepted-confidence"),
    rationale: str = typer.Option(..., "--rationale"),
    limitation: list[str] | None = typer.Option(None, "--limitation"),
    output: Path = typer.Option(..., "--output", dir_okay=False),
) -> None:
    """Record the project geologist's decision on one exact assessment and critique."""

    from buduunkhad.core.phase03_science import (
        ScientificReviewDecision,
        create_deposit_model_review,
        write_phase03_science_record,
    )

    try:
        review = create_deposit_model_review(
            assessment,
            critique,
            reviewer=reviewer,
            reviewer_authorization_id=authorization_id,
            reviewed_at=datetime.fromisoformat(reviewed_at.replace("Z", "+00:00")),
            decision=ScientificReviewDecision(decision),
            accepted_model=accepted_model,
            accepted_confidence=accepted_confidence,
            rationale=rationale,
            limitations=tuple(limitation or ()),
        )
        write_phase03_science_record(review, output)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Deposit-model geologist review: {output}")
    typer.echo(f"Review ID: {review.review_id}")


@readiness_app.command("phase03-handoff")
def phase03_handoff(
    phase03_run: str = typer.Option(..., "--phase03-run"),
    boundary_acceptance: Path = typer.Option(
        ..., "--boundary-acceptance", exists=True, dir_okay=False
    ),
    georeference_acceptance: list[Path] = typer.Option(
        ..., "--georeference-acceptance", exists=True, dir_okay=False
    ),
    evidence_manifest: list[str] = typer.Option(..., "--evidence-manifest"),
    assessment: Path = typer.Option(..., "--assessment", exists=True, dir_okay=False),
    critique: Path = typer.Option(..., "--critique", exists=True, dir_okay=False),
    review: Path = typer.Option(..., "--review", exists=True, dir_okay=False),
    unresolved_gap: list[str] | None = typer.Option(None, "--unresolved-gap"),
    limitation: list[str] = typer.Option(..., "--limitation"),
    output: Path = typer.Option(..., "--output", dir_okay=False),
    config: Path = typer.Option("config/project.yaml", "--config", "-c"),
) -> None:
    """Resolve a Phase 03 scientific handoff from exact sealed evidence and human reviews."""

    from buduunkhad.config import load_config
    from buduunkhad.core.phase03_science import (
        resolve_phase03_scientific_handoff,
        write_phase03_science_record,
    )

    try:
        project = load_config(config)
        handoff = resolve_phase03_scientific_handoff(
            runs_root=project.runs_root,
            evidence_root=project.evidence_root,
            target_epsg=project.target_epsg,
            phase03_run_id=phase03_run,
            boundary_acceptance_path=boundary_acceptance,
            georeference_acceptance_paths=tuple(georeference_acceptance),
            evidence_manifest_ids=tuple(evidence_manifest),
            assessment_path=assessment,
            critique_path=critique,
            review_path=review,
            unresolved_gaps=tuple(unresolved_gap or ()),
            limitations=tuple(limitation),
        )
        write_phase03_science_record(handoff, output)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Phase 03 scientific handoff: {output}")
    typer.echo(f"Handoff ID: {handoff.handoff_id}")


@readiness_app.command("phase04-activation-candidate")
def phase04_activation_candidate(
    handoff: Path = typer.Option(..., "--handoff", exists=True, dir_okay=False),
    reference_root: Path = typer.Option(..., "--reference-root", exists=True, file_okay=False),
    reference_set: Path = typer.Option(..., "--reference-set", exists=True, dir_okay=False),
    calibration_report: Path = typer.Option(
        ..., "--calibration-report", exists=True, dir_okay=False
    ),
    limitation: list[str] = typer.Option(..., "--limitation"),
    output: Path = typer.Option(..., "--output", dir_okay=False),
) -> None:
    """Bind one Phase 03 handoff to an exact reference set and calibration report."""

    from buduunkhad.core.phase04_authoritative import (
        create_phase04_activation_candidate,
        write_phase04_record,
    )

    try:
        candidate = create_phase04_activation_candidate(
            handoff,
            reference_root=reference_root,
            reference_set_path=reference_set,
            calibration_report_path=calibration_report,
            limitations=tuple(limitation),
        )
        write_phase04_record(candidate, output)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Phase 04 activation candidate: {output}")
    typer.echo(f"Candidate ID: {candidate.candidate_id}")
    typer.echo("Activation still requires methodology-owner and project-geologist reviews.")


@readiness_app.command("phase04-activation-attest")
def phase04_activation_attest(
    candidate: Path = typer.Option(..., "--candidate", exists=True, dir_okay=False),
    reviewer: str = typer.Option(..., "--reviewer"),
    role: str = typer.Option(..., "--role"),
    authorization_id: str = typer.Option(..., "--authorization-id"),
    reviewed_at: str = typer.Option(..., "--reviewed-at"),
    decision: str = typer.Option(..., "--decision"),
    rationale: str = typer.Option(..., "--rationale"),
    limitation: list[str] | None = typer.Option(None, "--limitation"),
    output: Path = typer.Option(..., "--output", dir_okay=False),
) -> None:
    """Review one exact Phase 04 calibration/activation candidate."""

    from buduunkhad.core.phase04_authoritative import (
        Phase04ActivationDecision,
        Phase04ActivationRole,
        create_phase04_activation_review,
        write_phase04_record,
    )

    try:
        review = create_phase04_activation_review(
            candidate,
            reviewer=reviewer,
            reviewer_role=Phase04ActivationRole(role),
            reviewer_authorization_id=authorization_id,
            reviewed_at=datetime.fromisoformat(reviewed_at.replace("Z", "+00:00")),
            decision=Phase04ActivationDecision(decision),
            rationale=rationale,
            limitations=tuple(limitation or ()),
        )
        write_phase04_record(review, output)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Phase 04 activation review: {output}")
    typer.echo(f"Review ID: {review.review_id}")


@readiness_app.command("phase04-activation-resolve")
def phase04_activation_resolve(
    candidate: Path = typer.Option(..., "--candidate", exists=True, dir_okay=False),
    handoff: Path = typer.Option(..., "--handoff", exists=True, dir_okay=False),
    reference_root: Path = typer.Option(..., "--reference-root", exists=True, file_okay=False),
    review: list[Path] = typer.Option(
        ...,
        "--review",
        exists=True,
        dir_okay=False,
        help="Exactly two reviews: methodology owner and project geologist.",
    ),
    output: Path = typer.Option(..., "--output", dir_okay=False),
) -> None:
    """Resolve Phase 04 activation after revalidating calibration and both reviews."""

    from buduunkhad.core.phase04_authoritative import (
        resolve_phase04_activation,
        write_phase04_record,
    )

    try:
        activation = resolve_phase04_activation(
            candidate,
            handoff_path=handoff,
            reference_root=reference_root,
            review_paths=tuple(review),
        )
        write_phase04_record(activation, output)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Phase 04 activation: {output}")
    typer.echo(f"Activation ID: {activation.activation_id}")


@readiness_app.command("phase04-scorecard")
def phase04_scorecard(
    prospects: Path = typer.Option(..., "--prospects", exists=True, dir_okay=False),
    prospect_layer: str = typer.Option(..., "--prospect-layer"),
    judgments: Path = typer.Option(..., "--judgments", exists=True, dir_okay=False),
    reviewer: str = typer.Option(..., "--reviewer"),
    authorization_id: str = typer.Option(..., "--authorization-id"),
    reviewed_at: str = typer.Option(..., "--reviewed-at"),
    limitation: list[str] = typer.Option(..., "--limitation"),
    output: Path = typer.Option(..., "--output", dir_okay=False),
) -> None:
    """Bind human-reviewed geometry and ranged score judgments to exact prospect bytes."""

    from buduunkhad.core.phase04_authoritative import (
        ProspectScore,
        create_phase04_scorecard,
        write_phase04_record,
    )

    try:
        data = json.loads(
            judgments.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
        )
        if not isinstance(data, list):
            raise ValueError("Phase 04 judgments must be a JSON array")
        scores = tuple(ProspectScore.model_validate(item) for item in data)
        scorecard = create_phase04_scorecard(
            prospects,
            prospect_layer=prospect_layer,
            reviewer=reviewer,
            reviewer_authorization_id=authorization_id,
            reviewed_at=datetime.fromisoformat(reviewed_at.replace("Z", "+00:00")),
            scores=scores,
            limitations=tuple(limitation),
        )
        write_phase04_record(scorecard, output)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Phase 04 reviewed scorecard: {output}")
    typer.echo(f"Scorecard ID: {scorecard.scorecard_id}")


@readiness_app.command("phase04-run")
def phase04_run(
    run_id: str = typer.Option(..., "--run-id"),
    handoff: Path = typer.Option(..., "--handoff", exists=True, dir_okay=False),
    activation: Path = typer.Option(..., "--activation", exists=True, dir_okay=False),
    activation_candidate: Path = typer.Option(
        ..., "--activation-candidate", exists=True, dir_okay=False
    ),
    activation_reference_root: Path = typer.Option(
        ..., "--activation-reference-root", exists=True, file_okay=False
    ),
    prospects: Path = typer.Option(..., "--prospects", exists=True, dir_okay=False),
    prospect_layer: str = typer.Option(..., "--prospect-layer"),
    scorecard: Path = typer.Option(..., "--scorecard", exists=True, dir_okay=False),
    evidence_manifest: list[str] = typer.Option(..., "--evidence-manifest"),
    config: Path = typer.Option("config/project.yaml", "--config", "-c"),
) -> None:
    """Produce measured and ranked human-reviewed prospect-polygon outputs."""

    from buduunkhad.config import load_config
    from buduunkhad.core.phase04_authoritative import run_phase04_authoritative
    from buduunkhad.geospatial_ai.path_safety import StorageRoots

    try:
        project = load_config(config)
        output, result = run_phase04_authoritative(
            roots=StorageRoots.from_environment(raw_root=project.raw_root),
            run_id=run_id,
            runs_root=project.runs_root,
            evidence_root=project.evidence_root,
            target_epsg=project.target_epsg,
            handoff_path=handoff,
            activation_path=activation,
            activation_candidate_path=activation_candidate,
            activation_reference_root=activation_reference_root,
            prospect_path=prospects,
            prospect_layer=prospect_layer,
            scorecard_path=scorecard,
            evidence_manifest_ids=tuple(evidence_manifest),
        )
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        _abort(exc)
    typer.echo(f"Phase 04 prospect-polygon outputs: {output}")
    typer.echo(f"Result ID: {result.result_id}")
