from __future__ import annotations

import csv
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import geopandas as gpd
import pytest
from shapely.geometry import LineString, Point, box

from buduunkhad.ai.fingerprint import sha256_file
from buduunkhad.core.evidence_manifest import (
    EvidenceExecutionMode,
    EvidenceLifecycleState,
    EvidenceManifestBinding,
    EvidenceOrigin,
    EvidenceRecord,
    EvidenceRole,
    EvidenceSourceKind,
    ResolvedEvidence,
)
from buduunkhad.core.execution_policy import ExecutionMode
from buduunkhad.core.phase03_science import (
    GeoreferenceAcceptanceBinding,
    Phase03ScientificHandoff,
    ScientificRecordBinding,
    write_phase03_science_record,
)
from buduunkhad.core.phase04_authoritative import (
    CriterionScore,
    Phase04ActivationDecision,
    Phase04ActivationRole,
    Phase04AuthoritativeError,
    ProspectScore,
    create_phase04_activation_candidate,
    create_phase04_activation_review,
    create_phase04_scorecard,
    load_phase04_result,
    resolve_phase04_activation,
    run_phase04_authoritative,
    verify_phase04_result,
    write_phase04_record,
)
from buduunkhad.core.run_storage import ResolvedSourcePhase, SourcePhaseBinding
from buduunkhad.geospatial_ai.path_safety import StorageRoots

TARGET_EPSG = 32647


def _roots(tmp_path: Path) -> StorageRoots:
    paths = {
        name: tmp_path / name for name in ("raw", "workflow", "snapshot", "work", "eval", "publish")
    }
    for path in paths.values():
        path.mkdir()
    return StorageRoots(
        raw_root=paths["raw"],
        workflow_docs_root=paths["workflow"],
        snapshot_root=paths["snapshot"],
        work_root=paths["work"],
        eval_root=paths["eval"],
        publish_root=paths["publish"],
    )


def _evidence(tmp_path: Path) -> tuple[ResolvedEvidence, ...]:
    tmp_path.mkdir(parents=True, exist_ok=True)
    definitions = (
        (
            "EV-GEOLOGY",
            "geology_units_50k_polygon",
            "geology_units_50k_polygon",
            EvidenceRole.GEOLOGY,
            [box(0, 0, 100, 100)],
        ),
        (
            "EV-STRUCTURE",
            "faults_structures_line",
            "faults_structures_line",
            EvidenceRole.STRUCTURE,
            [LineString([(0, 50), (200, 50)])],
        ),
        (
            "EV-OCCURRENCE",
            "mineral_occurrences_point",
            "mineral_occurrences_point",
            EvidenceRole.OCCURRENCE,
            [Point(25, 25)],
        ),
        (
            "EV-ALTERATION",
            "ai_accepted_alteration_zones_polygon",
            None,
            EvidenceRole.ALTERATION_SUPPORT,
            [box(10, 10, 90, 90)],
        ),
    )
    result = []
    for evidence_id, layer, target, role, geometry in definitions:
        artifact = tmp_path / f"{evidence_id}.gpkg"
        geo_frame = cast(Any, gpd.GeoDataFrame)
        geo_frame(
            {"source_id": [evidence_id]},
            geometry=geometry,
            crs=f"EPSG:{TARGET_EPSG}",
        ).to_file(artifact, layer=layer, driver="GPKG")
        record = EvidenceRecord(
            evidence_id=evidence_id,
            source_kind=EvidenceSourceKind.PHASE03_PROMOTION,
            source_run_id="phase03-run",
            source_authority_path=f"accepted/{evidence_id}.promotion-ledger.jsonl",
            source_authority_sha256="b" * 64,
            source_record_id=f"audit-{evidence_id}",
            artifact_path=f"accepted/{evidence_id}.gpkg",
            artifact_sha256=sha256_file(artifact),
            artifact_size_bytes=artifact.stat().st_size,
            layer_name=layer,
            target_layer_name=target,
            evidence_role=role,
            origin=EvidenceOrigin.PHASE03_AI_HANDOFF,
            lifecycle_state=EvidenceLifecycleState.ACCEPTED_EVIDENCE,
            review_record_id=f"audit-{evidence_id}",
            reviewers=("Project Geologist",),
            reviewed_at=datetime(2026, 7, 27, 7, 0, tzinfo=UTC),
            eligible_phases=("03",),
            eligible_modes=(EvidenceExecutionMode.SUPPORT_EVIDENCE,),
            authoritative_for_phase04=False,
            limitations=("Accepted Phase 03 evidence.",),
        )
        result.append(
            ResolvedEvidence(
                manifest_id="a" * 64,
                manifest_sha256="c" * 64,
                catalog_entry_id="d" * 64,
                record=record,
                artifact=artifact,
            )
        )
    return tuple(sorted(result, key=lambda item: item.record.evidence_id))


def _handoff(path: Path, evidence: tuple[ResolvedEvidence, ...]) -> Phase03ScientificHandoff:
    source = SourcePhaseBinding(
        phase_id="03",
        source_run_id="phase03-run",
        source_manifest_sha256="e" * 64,
        source_phase_sha256="f" * 64,
    )
    handoff = Phase03ScientificHandoff.create(
        phase03_source=source,
        boundary_acceptance=ScientificRecordBinding(
            record_id="1" * 64,
            file_sha256="2" * 64,
        ),
        georeference_acceptances=(
            GeoreferenceAcceptanceBinding(
                acceptance_id="3" * 64,
                acceptance_file_sha256="4" * 64,
                source_sha256="5" * 64,
                derivative_sha256="6" * 64,
            ),
        ),
        evidence_manifest_bindings=(
            EvidenceManifestBinding(
                manifest_id="a" * 64,
                manifest_sha256="c" * 64,
                catalog_entry_id="d" * 64,
            ),
        ),
        accepted_evidence_ids=tuple(item.record.evidence_id for item in evidence),
        accepted_evidence_roles=tuple(
            sorted({item.record.evidence_role for item in evidence}, key=lambda item: item.value)
        ),
        deposit_model_assessment=ScientificRecordBinding(
            record_id="7" * 64,
            file_sha256="8" * 64,
        ),
        deposit_model_critique=ScientificRecordBinding(
            record_id="9" * 64,
            file_sha256="a" * 64,
        ),
        deposit_model_review=ScientificRecordBinding(
            record_id="b" * 64,
            file_sha256="c" * 64,
        ),
        unresolved_gaps=("Field confirmation",),
        limitations=("Desktop support evidence only.",),
        handed_off_by="Project Geologist",
        handoff_authorization_id="geologist-authorization",
        handed_off_at=datetime(2026, 7, 27, 8, 0, tzinfo=UTC),
        decision="accepted-for-phase04-input",
    )
    write_phase03_science_record(handoff, path)
    return handoff


def _criterion_scores(
    handoff: Phase03ScientificHandoff,
    *,
    strong: bool,
) -> tuple[CriterionScore, ...]:
    values = {
        "geology": (20 if strong else 15, ("EV-GEOLOGY",)),
        "occurrence": (15 if strong else 10, ("EV-OCCURRENCE",)),
        "geochemistry": (0, ()),
        "remote_sensing": (15 if strong else 10, ("EV-ALTERATION",)),
        "structure": (10 if strong else 8, ("EV-STRUCTURE",)),
        "deposit_model_fit": (
            10 if strong else 7,
            (handoff.deposit_model_assessment.record_id,),
        ),
        "access": (0, ()),
        "confidence": (5, (handoff.handoff_id,)),
    }
    return tuple(
        CriterionScore(
            criterion_id=criterion,
            awarded_points=values[criterion][0],
            rationale=f"Human judgment for {criterion}.",
            evidence_ids=values[criterion][1],
            data_gap=values[criterion][0] == 0,
        )
        for criterion in values
    )


def _score(
    prospect_id: str,
    handoff: Phase03ScientificHandoff,
    *,
    strong: bool,
) -> ProspectScore:
    return ProspectScore(
        prospect_id=prospect_id,
        scores=_criterion_scores(handoff, strong=strong),
        dominant_deposit_model="Porphyry Cu-Au",
        model_confidence="preliminary-moderate",
        missing_model_evidence=("Field confirmation",),
        validation_priority="high" if strong else "medium",
        confidence="moderate",
        limitations=("Desktop ranking is not proof of mineralization.",),
        data_gaps=("Access evidence unavailable", "Geochemistry evidence unavailable"),
        next_action="Qualified expert review and field validation.",
    )


def test_positive_score_requires_exact_evidence_identity() -> None:
    with pytest.raises(ValueError, match="positive criterion"):
        CriterionScore(
            criterion_id="geology",
            awarded_points=5,
            rationale="Unsupported.",
            evidence_ids=(),
            data_gap=False,
        )


def test_phase04_activation_and_output_path_are_review_bound(
    tmp_path: Path,
    monkeypatch,
) -> None:
    roots = _roots(tmp_path)
    run_id = "phase04-run"
    run = roots.run_directory(run_id, create=True)
    evidence = _evidence(tmp_path / "accepted-evidence")
    handoff_path = run / "phase03-handoff.json"
    handoff = _handoff(handoff_path, evidence)

    reference_root = roots.require_eval_root()
    reference_set = reference_root / "reference.gpkg"
    calibration = reference_root / "calibration.json"
    reference_set.write_bytes(b"owner-approved reference bytes")
    calibration.write_text('{"calibrated":true}\n', encoding="utf-8")
    candidate = create_phase04_activation_candidate(
        handoff_path,
        reference_root=reference_root,
        reference_set_path=reference_set,
        calibration_report_path=calibration,
        limitations=("Calibration applies only to the bound reference set.",),
    )
    candidate_path = run / "phase04-activation-candidate.json"
    write_phase04_record(candidate, candidate_path)
    review_paths = []
    for role, reviewer in (
        (Phase04ActivationRole.METHODOLOGY_OWNER, "Methodology Owner"),
        (Phase04ActivationRole.PROJECT_GEOLOGIST, "Project Geologist"),
    ):
        review = create_phase04_activation_review(
            candidate_path,
            reviewer=reviewer,
            reviewer_role=role,
            reviewer_authorization_id=f"authorization-{role.value}",
            reviewed_at=datetime(2026, 7, 27, 9, 0, tzinfo=UTC),
            decision=Phase04ActivationDecision.ACCEPTED,
            rationale="Accepted the exact implementation calibration.",
        )
        review_path = run / f"activation-{role.value}.json"
        write_phase04_record(review, review_path)
        review_paths.append(review_path)
    activation = resolve_phase04_activation(
        candidate_path,
        handoff_path=handoff_path,
        reference_root=reference_root,
        review_paths=tuple(review_paths),
    )
    activation_path = run / "phase04-activation.json"
    write_phase04_record(activation, activation_path)

    prospects_path = run / "reviewed-prospects.gpkg"
    geo_frame = cast(Any, gpd.GeoDataFrame)
    geo_frame(
        {"prospect_id": ["P-001", "P-002"]},
        geometry=[box(0, 0, 100, 100), box(110, 0, 210, 100)],
        crs=f"EPSG:{TARGET_EPSG}",
    ).to_file(prospects_path, layer="reviewed_prospects", driver="GPKG")
    scorecard = create_phase04_scorecard(
        prospects_path,
        prospect_layer="reviewed_prospects",
        reviewer="Project Geologist",
        reviewer_authorization_id="geologist-authorization",
        reviewed_at=datetime(2026, 7, 27, 10, 0, tzinfo=UTC),
        scores=(
            _score("P-001", handoff, strong=True),
            _score("P-002", handoff, strong=False),
        ),
        limitations=("Scores are human judgments over exact reviewed geometry.",),
    )
    scorecard_path = run / "phase04-scorecard.json"
    write_phase04_record(scorecard, scorecard_path)

    source = ResolvedSourcePhase(
        binding=handoff.phase03_source,
        phase_dir=tmp_path / "source-phase03",
        output_artifacts=(),
        sealed_files=(),
        gate_status="blocked",
        gate_provisional=False,
        execution_mode=ExecutionMode.SUPPORT_EVIDENCE,
    )
    monkeypatch.setattr(
        "buduunkhad.core.phase04_authoritative.resolve_source_phase",
        lambda *args, **kwargs: source,
    )
    monkeypatch.setattr(
        "buduunkhad.core.phase04_authoritative.EvidenceAuthorityResolver.resolve_selected",
        lambda self, manifest_ids: evidence,
    )
    runs_root = tmp_path / "pipeline-runs"
    evidence_root = tmp_path / "evidence-authority"
    runs_root.mkdir()
    evidence_root.mkdir()

    output, result = run_phase04_authoritative(
        roots=roots,
        run_id=run_id,
        runs_root=runs_root,
        evidence_root=evidence_root,
        target_epsg=TARGET_EPSG,
        handoff_path=handoff_path,
        activation_path=activation_path,
        activation_candidate_path=candidate_path,
        activation_reference_root=reference_root,
        prospect_path=prospects_path,
        prospect_layer="reviewed_prospects",
        scorecard_path=scorecard_path,
        evidence_manifest_ids=("a" * 64,),
    )

    assert result.prospect_count == 2
    assert dict(result.class_counts) == {"A": 1, "B": 1, "C": 0, "D": 0}
    with (output / "prospect_measurements.csv").open(encoding="utf-8", newline="") as stream:
        measurements = list(csv.DictReader(stream))
    assert measurements[0]["geology_feature_count"] == "1"
    assert measurements[0]["occurrence_point_count"] == "1"
    ranked = gpd.read_file(output / "ranked_prospects.gpkg", layer="authoritative_prospects")
    assert list(ranked["prospect_id"]) == ["P-001", "P-002"]
    assert list(ranked["total_score"]) == [75, 55]
    assert load_phase04_result(output / "phase04_authoritative_result.json") == result

    second_output, second = run_phase04_authoritative(
        roots=roots,
        run_id=run_id,
        runs_root=runs_root,
        evidence_root=evidence_root,
        target_epsg=TARGET_EPSG,
        handoff_path=handoff_path,
        activation_path=activation_path,
        activation_candidate_path=candidate_path,
        activation_reference_root=reference_root,
        prospect_path=prospects_path,
        prospect_layer="reviewed_prospects",
        scorecard_path=scorecard_path,
        evidence_manifest_ids=("a" * 64,),
    )
    assert (second_output, second) == (output, result)

    ranked_path = output / "ranked_prospects.gpkg"
    ranked_path.write_bytes(ranked_path.read_bytes() + b"changed")
    with pytest.raises(Phase04AuthoritativeError, match="file bytes changed"):
        verify_phase04_result(
            result,
            result_directory=output,
            handoff_path=handoff_path,
            activation_path=activation_path,
            prospect_path=prospects_path,
            scorecard_path=scorecard_path,
        )
