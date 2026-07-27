"""Measured georeference evidence and two-role acceptance tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from buduunkhad.core.georeference import (
    GcpMeasurement,
    GeoreferenceError,
    GeoreferenceMeasurementStatus,
    GeoreferenceReviewDecision,
    GeoreferenceReviewerRole,
    create_georeference_record,
    create_georeference_review,
    resolve_georeference_acceptance,
    write_georeference_record,
)


def _gcp(identifier: str, residual_x: float, residual_y: float) -> GcpMeasurement:
    return GcpMeasurement(
        gcp_id=identifier,
        source_pixel_x=10.0,
        source_pixel_y=20.0,
        target_x=300000.0,
        target_y=5100000.0,
        residual_x_metres=residual_x,
        residual_y_metres=residual_y,
        residual_metres=(residual_x**2 + residual_y**2) ** 0.5,
        evidence_source="reviewed grid intersection",
    )


def _record(tmp_path):
    source_root = tmp_path / "source"
    derivative_root = tmp_path / "derivative"
    source = source_root / "map.tif"
    derivative = derivative_root / "map_georef.tif"
    source_root.mkdir()
    derivative_root.mkdir()
    source.write_bytes(b"source-map")
    derivative.write_bytes(b"georeferenced-map")
    record = create_georeference_record(
        processing_run_id="processing-run",
        source_run_id="source-run",
        source_root=source_root,
        source_path=source,
        derivative_root=derivative_root,
        derivative_path=derivative,
        proposed_source_crs="EPSG:4326",
        source_crs_evidence=("printed coordinate grid",),
        target_epsg=32647,
        transformation="second-order polynomial",
        resampling="bilinear",
        gcps=(_gcp("GCP-001", 1.0, 2.0), _gcp("GCP-002", 2.0, 2.0)),
        spatial_distribution_findings=("GCPs cover opposite map quadrants.",),
        limitations=("No acceptance threshold was inferred by software.",),
    )
    record_path = write_georeference_record(record, tmp_path / "record.json")
    return source_root, derivative_root, derivative, record, record_path


def test_georeference_record_calculates_residuals_without_approving(tmp_path) -> None:
    _source_root, _derivative_root, _derivative, record, _record_path = _record(tmp_path)
    assert record.status is GeoreferenceMeasurementStatus.MEASURED
    assert record.residual_summary is not None
    assert record.residual_summary.gcp_count == 2
    assert record.residual_summary.maximum_residual_metres == pytest.approx(2**0.5 * 2)
    assert "review" not in type(record).model_fields
    assert "decision" not in type(record).model_fields


def test_two_exact_accepted_roles_resolve_georeference(tmp_path) -> None:
    source_root, derivative_root, _derivative, record, record_path = _record(tmp_path)
    reviews = []
    for role, reviewer in (
        (GeoreferenceReviewerRole.GEOSPATIAL_REVIEWER, "QA Engineer"),
        (GeoreferenceReviewerRole.PROJECT_GEOLOGIST, "Project Geologist"),
    ):
        review = create_georeference_review(
            record_path,
            reviewer=reviewer,
            reviewer_role=role,
            reviewer_authorization_id=f"auth-{role.value}",
            reviewed_at=datetime(2026, 7, 27, 4, 0, tzinfo=UTC),
            decision=GeoreferenceReviewDecision.ACCEPTED,
            rationale="Synthetic acceptance of exact measurements.",
            visual_alignment_findings=("Reference intersections align without visible drift.",),
        )
        reviews.append(write_georeference_record(review, tmp_path / f"{role.value}.json"))

    acceptance = resolve_georeference_acceptance(
        record_path,
        source_root=source_root,
        derivative_root=derivative_root,
        attestation_paths=tuple(reviews),
    )
    assert acceptance.record_id == record.record_id
    assert len(acceptance.accepted_attestation_ids) == 2


def test_duplicate_role_rejection_and_derivative_mutation_fail_closed(tmp_path) -> None:
    source_root, derivative_root, derivative, _measured, record_path = _record(tmp_path)
    review = create_georeference_review(
        record_path,
        reviewer="QA Engineer",
        reviewer_role=GeoreferenceReviewerRole.GEOSPATIAL_REVIEWER,
        reviewer_authorization_id="auth-qa",
        reviewed_at=datetime(2026, 7, 27, 4, 0, tzinfo=UTC),
        decision=GeoreferenceReviewDecision.ACCEPTED,
        rationale="Synthetic acceptance.",
        visual_alignment_findings=("Synthetic visual check.",),
    )
    review_path = write_georeference_record(review, tmp_path / "review.json")
    with pytest.raises(GeoreferenceError, match="both exact reviewer roles"):
        resolve_georeference_acceptance(
            record_path,
            source_root=source_root,
            derivative_root=derivative_root,
            attestation_paths=(review_path, review_path),
        )

    derivative.write_bytes(b"mutated")
    with pytest.raises(GeoreferenceError, match="bytes changed"):
        resolve_georeference_acceptance(
            record_path,
            source_root=source_root,
            derivative_root=derivative_root,
            attestation_paths=(review_path, review_path),
        )


def test_missing_crs_or_gcps_remains_incomplete(tmp_path) -> None:
    source_root = tmp_path / "source"
    derivative_root = tmp_path / "derivative"
    source_root.mkdir()
    derivative_root.mkdir()
    source = source_root / "map.tif"
    derivative = derivative_root / "map_georef.tif"
    source.write_bytes(b"source")
    derivative.write_bytes(b"derivative")
    record = create_georeference_record(
        processing_run_id="processing-run",
        source_run_id="source-run",
        source_root=source_root,
        source_path=source,
        derivative_root=derivative_root,
        derivative_path=derivative,
        proposed_source_crs=None,
        source_crs_evidence=(),
        target_epsg=32647,
        transformation="not selected",
        resampling="not selected",
        gcps=(),
        spatial_distribution_findings=("No GCP distribution can be measured.",),
        limitations=("Source CRS and GCPs remain unresolved.",),
    )
    assert record.status is GeoreferenceMeasurementStatus.INCOMPLETE
