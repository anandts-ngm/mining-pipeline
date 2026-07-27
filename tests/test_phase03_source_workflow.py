from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any, cast

import geopandas as gpd
import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin
from shapely.geometry import LineString, box

from buduunkhad.geospatial_ai.path_safety import StorageRoots
from buduunkhad.geospatial_ai.phase03_source_workflow import (
    Phase03SourceWorkflowError,
    load_phase03_overlap_review,
    load_phase03_source_workflow,
    prepare_phase03_source_workflow,
    review_phase03_draft_overlaps,
)
from buduunkhad.geospatial_ai.stitching import (
    OverlapReviewCandidate,
    review_candidate_overlaps,
)
from buduunkhad.geospatial_ai.tiles import TileParameters

TARGET_CRS = "EPSG:32647"


@pytest.fixture
def roots(tmp_path: Path) -> StorageRoots:
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


def _write_raster(path: Path) -> Path:
    data = np.arange(3 * 12 * 12, dtype=np.uint8).reshape(3, 12, 12)
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        width=12,
        height=12,
        count=3,
        dtype="uint8",
        crs=TARGET_CRS,
        transform=from_origin(500_000, 5_200_000, 10, 10),
    ) as dataset:
        dataset.write(data)
    return path


def _write_layer(
    path: Path,
    *,
    layer: str,
    feature_ids: list[str],
    legend_codes: list[str],
    tile_ids: list[list[str]],
    geometries: list[object],
) -> None:
    geo_frame = cast(Any, gpd.GeoDataFrame)
    frame = geo_frame(
        {
            "feature_id": feature_ids,
            "legend_code": legend_codes,
            "tile_ids": [json.dumps(value) for value in tile_ids],
            "confidence": [0.8] * len(feature_ids),
        },
        geometry=geometries,
        crs=TARGET_CRS,
    )
    frame.to_file(path, layer=layer, driver="GPKG")


def test_source_workflow_prepares_exact_legend_and_feature_packages(
    roots: StorageRoots,
) -> None:
    source = _write_raster(roots.require_snapshot_root() / "historical-map.tif")

    path, manifest = prepare_phase03_source_workflow(
        source,
        roots=roots,
        run_id="source-workflow",
        target_crs=TARGET_CRS,
        provider="disabled",
        tile_parameters=TileParameters(width=8, height=8, overlap=2),
        estimated_cost_usd=Decimal("0"),
    )

    assert tuple(item.task_type for item in manifest.tasks) == (
        "legend_extraction",
        "geological_feature_proposal",
    )
    assert load_phase03_source_workflow(path, roots=roots) == manifest

    package = roots.run_directory("source-workflow") / manifest.tasks[0].package_path
    (package / "request-package.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(Phase03SourceWorkflowError, match="package bytes changed"):
        load_phase03_source_workflow(path, roots=roots)


def test_overlap_classification_is_cross_tile_and_never_changes_geometry() -> None:
    original = (
        OverlapReviewCandidate(
            feature_id="a",
            layer_name="geology_units",
            legend_code="Q",
            tile_ids=("tile-a",),
            confidence=0.9,
            geometry=box(0, 0, 10, 10),
        ),
        OverlapReviewCandidate(
            feature_id="b",
            layer_name="geology_units",
            legend_code="Q",
            tile_ids=("tile-b",),
            confidence=0.8,
            geometry=box(0, 0, 10, 10),
        ),
        OverlapReviewCandidate(
            feature_id="c",
            layer_name="alteration_zones",
            legend_code="ARG",
            tile_ids=("tile-c",),
            confidence=0.7,
            geometry=box(0, 0, 10, 10),
        ),
        OverlapReviewCandidate(
            feature_id="d",
            layer_name="faults_structures",
            legend_code="F",
            tile_ids=("tile-d",),
            confidence=0.9,
            geometry=LineString([(0, 20), (10, 20)]),
        ),
        OverlapReviewCandidate(
            feature_id="e",
            layer_name="faults_structures",
            legend_code="F",
            tile_ids=("tile-e",),
            confidence=0.8,
            geometry=LineString([(10.1, 20), (20, 20)]),
        ),
    )
    before = tuple(item.geometry.wkb for item in original)

    result = review_candidate_overlaps(
        original,
        duplicate_overlap_threshold=0.8,
        conflict_overlap_threshold=0.2,
        continuity_tolerance=0.2,
    )

    assert [(item.left_feature_id, item.right_feature_id) for item in result.duplicate_pairs] == [
        ("a", "b")
    ]
    assert {(item.left_feature_id, item.right_feature_id) for item in result.conflict_pairs} == {
        ("a", "c"),
        ("b", "c"),
    }
    assert [(item.left_feature_id, item.right_feature_id) for item in result.continuity_pairs] == [
        ("d", "e")
    ]
    assert tuple(item.geometry.wkb for item in original) == before


def test_overlap_report_is_hash_bound_and_idempotent(roots: StorageRoots) -> None:
    run_id = "overlap-review"
    run = roots.run_directory(run_id, create=True)
    draft = run / "draft.gpkg"
    _write_layer(
        draft,
        layer="geology_units",
        feature_ids=["a", "b"],
        legend_codes=["Q", "Q"],
        tile_ids=[["tile-a"], ["tile-b"]],
        geometries=[box(0, 0, 10, 10), box(0, 0, 10, 10)],
    )
    _write_layer(
        draft,
        layer="faults_structures",
        feature_ids=["c", "d"],
        legend_codes=["F", "F"],
        tile_ids=[["tile-c"], ["tile-d"]],
        geometries=[
            LineString([(0, 20), (10, 20)]),
            LineString([(10.1, 20), (20, 20)]),
        ],
    )
    output = run / "reviews" / "overlap.json"

    first = review_phase03_draft_overlaps(
        draft,
        roots=roots,
        run_id=run_id,
        output=output,
        continuity_tolerance=0.2,
    )
    second = review_phase03_draft_overlaps(
        draft,
        roots=roots,
        run_id=run_id,
        output=output,
        continuity_tolerance=0.2,
    )

    assert first == second == load_phase03_overlap_review(output, roots=roots, run_id=run_id)
    assert first.review_required
    draft.write_bytes(draft.read_bytes() + b"changed")
    with pytest.raises(Phase03SourceWorkflowError, match="draft bytes changed"):
        load_phase03_overlap_review(output, roots=roots, run_id=run_id)
