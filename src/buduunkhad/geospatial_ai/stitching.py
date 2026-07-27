"""Deterministic overlap de-duplication for tiled draft features."""

from __future__ import annotations

from dataclasses import dataclass

from shapely.geometry.base import BaseGeometry


@dataclass(frozen=True, slots=True)
class StitchCandidate:
    feature_id: str
    confidence: float
    geometry: BaseGeometry


@dataclass(frozen=True, slots=True)
class StitchResult:
    kept: tuple[StitchCandidate, ...]
    duplicate_feature_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OverlapReviewCandidate:
    feature_id: str
    layer_name: str
    legend_code: str
    tile_ids: tuple[str, ...]
    confidence: float
    geometry: BaseGeometry


@dataclass(frozen=True, slots=True)
class OverlapReviewPair:
    left_feature_id: str
    right_feature_id: str
    reason: str
    overlap_ratio: float
    endpoint_distance: float | None = None


@dataclass(frozen=True, slots=True)
class OverlapReviewResult:
    duplicate_pairs: tuple[OverlapReviewPair, ...]
    conflict_pairs: tuple[OverlapReviewPair, ...]
    continuity_pairs: tuple[OverlapReviewPair, ...]


def deduplicate_candidates(
    candidates: tuple[StitchCandidate, ...],
    *,
    overlap_threshold: float,
) -> StitchResult:
    if not 0 < overlap_threshold <= 1:
        raise ValueError("overlap threshold must be greater than zero and at most one")
    ordered = sorted(candidates, key=lambda value: (-value.confidence, value.feature_id))
    kept: list[StitchCandidate] = []
    duplicates: list[str] = []
    for candidate in ordered:
        if any(_overlap(candidate.geometry, prior.geometry) >= overlap_threshold for prior in kept):
            duplicates.append(candidate.feature_id)
        else:
            kept.append(candidate)
    return StitchResult(kept=tuple(kept), duplicate_feature_ids=tuple(sorted(duplicates)))


def review_candidate_overlaps(
    candidates: tuple[OverlapReviewCandidate, ...],
    *,
    duplicate_overlap_threshold: float = 0.8,
    conflict_overlap_threshold: float = 0.2,
    continuity_tolerance: float = 0.0,
) -> OverlapReviewResult:
    """Classify overlap relationships without changing or joining proposal geometry."""

    if not 0 < conflict_overlap_threshold <= duplicate_overlap_threshold <= 1:
        raise ValueError("overlap thresholds must satisfy 0 < conflict <= duplicate <= 1")
    if continuity_tolerance < 0:
        raise ValueError("continuity tolerance cannot be negative")
    ordered = tuple(sorted(candidates, key=lambda item: item.feature_id))
    if len({item.feature_id for item in ordered}) != len(ordered):
        raise ValueError("overlap-review feature identities must be unique")
    for item in ordered:
        if (
            not item.feature_id.strip()
            or not item.layer_name.strip()
            or not item.tile_ids
            or tuple(sorted(set(item.tile_ids))) != item.tile_ids
            or not 0 <= item.confidence <= 1
            or item.geometry.is_empty
            or not item.geometry.is_valid
        ):
            raise ValueError(f"overlap-review candidate is invalid: {item.feature_id!r}")

    duplicates: list[OverlapReviewPair] = []
    conflicts: list[OverlapReviewPair] = []
    continuity: list[OverlapReviewPair] = []
    for index, left in enumerate(ordered):
        for right in ordered[index + 1 :]:
            # A pair with identical tile provenance is not a stitching boundary. It remains
            # available to the ordinary within-response validation and human review workflow.
            if left.tile_ids == right.tile_ids:
                continue
            ratio = _overlap(left.geometry, right.geometry)
            same_class = (
                left.layer_name == right.layer_name and left.legend_code == right.legend_code
            )
            if ratio >= duplicate_overlap_threshold and same_class:
                duplicates.append(
                    _pair(left, right, reason="same-class-overlap", overlap_ratio=ratio)
                )
                continue
            if ratio >= conflict_overlap_threshold and not same_class:
                conflicts.append(
                    _pair(left, right, reason="conflicting-class-overlap", overlap_ratio=ratio)
                )
                continue
            if (
                continuity_tolerance > 0
                and same_class
                and left.geometry.geom_type in {"LineString", "MultiLineString"}
                and right.geometry.geom_type in {"LineString", "MultiLineString"}
            ):
                distance = _endpoint_distance(left.geometry, right.geometry)
                if distance <= continuity_tolerance:
                    continuity.append(
                        _pair(
                            left,
                            right,
                            reason="possible-line-continuity",
                            overlap_ratio=ratio,
                            endpoint_distance=distance,
                        )
                    )

    def pair_key(item: OverlapReviewPair) -> tuple[str, str]:
        return item.left_feature_id, item.right_feature_id

    return OverlapReviewResult(
        duplicate_pairs=tuple(sorted(duplicates, key=pair_key)),
        conflict_pairs=tuple(sorted(conflicts, key=pair_key)),
        continuity_pairs=tuple(sorted(continuity, key=pair_key)),
    )


def _pair(
    left: OverlapReviewCandidate,
    right: OverlapReviewCandidate,
    *,
    reason: str,
    overlap_ratio: float,
    endpoint_distance: float | None = None,
) -> OverlapReviewPair:
    return OverlapReviewPair(
        left_feature_id=left.feature_id,
        right_feature_id=right.feature_id,
        reason=reason,
        overlap_ratio=overlap_ratio,
        endpoint_distance=endpoint_distance,
    )


def _overlap(left: BaseGeometry, right: BaseGeometry) -> float:
    if left.equals(right):
        return 1.0
    if left.area > 0 and right.area > 0:
        union = left.union(right).area
        return float(left.intersection(right).area / union) if union else 0.0
    denominator = max(left.length, right.length)
    return float(left.intersection(right).length / denominator) if denominator else 0.0


def _endpoint_distance(left: BaseGeometry, right: BaseGeometry) -> float:
    left_boundary = left.boundary
    right_boundary = right.boundary
    return float(left_boundary.distance(right_boundary))
