from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import rasterio

from buduunkhad.core import raster_writers
from buduunkhad.core.phase05_pointcloud import (
    GROUND_CLASSIFICATION,
    PointCloudError,
    PointCloudGrid,
    baseline_discrepancies,
    laspy_available,
    rasterize_point_cloud,
    write_surface_cog,
)

pytestmark = pytest.mark.skipif(not laspy_available(), reason="requires the 'pointcloud' extra")

# A 4 x 4 metre lattice at one-metre cells, origin at the north-west corner.
_GRID = PointCloudGrid(origin_x=0.0, origin_y=4.0, resolution=1.0, width=4, height=4, epsg=32647)

# (x, y, z, classification). Two cells receive returns; everything else must stay nodata.
_POINTS = (
    (0.5, 3.5, 10.0, GROUND_CLASSIFICATION),
    (0.5, 3.5, 15.0, 5),  # vegetation above the same cell: raises DSM, must not touch DTM
    (2.5, 1.5, 20.0, GROUND_CLASSIFICATION),
    (2.5, 1.5, 18.0, GROUND_CLASSIFICATION),  # lower ground return wins the DTM
)


def _write_cloud(path: Path, points=_POINTS) -> Path:
    import laspy

    path.parent.mkdir(parents=True, exist_ok=True)
    header = laspy.LasHeader(point_format=3, version="1.2")
    header.offsets = np.zeros(3, dtype="float64")
    header.scales = np.full(3, 0.001, dtype="float64")
    data = laspy.LasData(header)
    data.x = np.array([p[0] for p in points], dtype="float64")
    data.y = np.array([p[1] for p in points], dtype="float64")
    data.z = np.array([p[2] for p in points], dtype="float64")
    data.classification = np.array([p[3] for p in points], dtype="uint8")
    data.write(str(path))
    return path


def test_grid_covering_snaps_to_a_shared_anchor():
    grid = PointCloudGrid.covering(
        (314_307.3, 5_090_786.1, 314_312.9, 5_090_791.4),
        resolution=0.5,
        epsg=32647,
        snap_x=314_672.75,
        snap_y=5_096_902.25,
    )
    # Every edge must land on the anchor lattice so blocks co-register without resampling.
    assert (grid.origin_x - 314_672.75) % 0.5 == pytest.approx(0.0)
    assert (grid.origin_y - 5_096_902.25) % 0.5 == pytest.approx(0.0)
    min_x, min_y, max_x, max_y = grid.bounds
    assert min_x <= 314_307.3 and min_y <= 5_090_786.1
    assert max_x >= 314_312.9 and max_y >= 5_090_791.4


def test_grid_rejects_degenerate_definitions():
    with pytest.raises(PointCloudError):
        PointCloudGrid(origin_x=0, origin_y=0, resolution=0, width=4, height=4, epsg=32647)
    with pytest.raises(PointCloudError):
        PointCloudGrid(origin_x=0, origin_y=0, resolution=1, width=0, height=4, epsg=32647)
    with pytest.raises(PointCloudError):
        PointCloudGrid.covering((10, 10, 10, 20), resolution=1, epsg=32647)


def test_flat_indices_flag_points_outside_the_lattice():
    x = np.array([0.5, 3.5, -1.0, 99.0])
    y = np.array([3.5, 0.5, 3.5, 3.5])
    flat, inside = _GRID.flat_indices(x, y)
    assert inside.tolist() == [True, True, False, False]
    assert flat[0] == 0  # north-west cell
    assert flat[1] == 15  # south-east cell


@pytest.mark.parametrize("suffix", [".las", ".laz"])
def test_single_pass_derives_surface_terrain_and_census(tmp_path, suffix):
    cloud = _write_cloud(tmp_path / f"cloud{suffix}")

    rasters = rasterize_point_cloud(cloud, grid=_GRID, chunk_size=3)

    assert rasters.total_points == 4
    assert rasters.points_outside_grid == 0
    assert rasters.classification_counts == {GROUND_CLASSIFICATION: 3, 5: 1}

    # The vegetation return lifts the surface but the terrain stays on bare earth.
    assert rasters.surface[0, 0] == pytest.approx(15.0)
    assert rasters.terrain[0, 0] == pytest.approx(10.0)
    # The lower of two ground returns wins the terrain cell.
    assert rasters.surface[2, 2] == pytest.approx(20.0)
    assert rasters.terrain[2, 2] == pytest.approx(18.0)

    # Uncovered cells keep nodata rather than being interpolated.
    assert rasters.surface[1, 1] == pytest.approx(-9999.0)
    assert rasters.terrain[1, 1] == pytest.approx(-9999.0)
    assert rasters.return_count[1, 1] == 0

    assert rasters.return_count[0, 0] == 2
    assert rasters.ground_point_count == 3
    assert rasters.surface_coverage == pytest.approx(2 / 16)
    assert rasters.terrain_coverage == pytest.approx(2 / 16)
    assert rasters.mean_density_per_m2 == pytest.approx(2.0)


def test_chunking_does_not_change_the_result(tmp_path):
    cloud = _write_cloud(tmp_path / "cloud.las")
    whole = rasterize_point_cloud(cloud, grid=_GRID, chunk_size=1_000)
    split = rasterize_point_cloud(cloud, grid=_GRID, chunk_size=1)
    assert np.array_equal(whole.surface, split.surface)
    assert np.array_equal(whole.terrain, split.terrain)
    assert np.array_equal(whole.return_count, split.return_count)
    assert whole.classification_counts == split.classification_counts


def test_points_outside_the_grid_are_counted_not_wrapped(tmp_path):
    points = (*_POINTS, (500.0, 500.0, 1.0, GROUND_CLASSIFICATION))
    cloud = _write_cloud(tmp_path / "stray.las", points)

    rasters = rasterize_point_cloud(cloud, grid=_GRID, chunk_size=2)

    assert rasters.total_points == 5
    assert rasters.points_outside_grid == 1
    assert rasters.return_count.sum() == 4
    assert "1 point(s) fall outside the block grid" in baseline_discrepancies(
        rasters, expected_point_count=5
    )


def test_baseline_discrepancies_detect_a_lossy_conversion(tmp_path):
    cloud = _write_cloud(tmp_path / "cloud.las")
    rasters = rasterize_point_cloud(cloud, grid=_GRID)

    assert baseline_discrepancies(rasters, expected_point_count=4) == ()
    problems = baseline_discrepancies(rasters, expected_point_count=9)
    assert any("does not match baseline 9" in item for item in problems)


def test_a_cloud_without_ground_returns_cannot_yield_a_terrain_model(tmp_path):
    points = tuple((x, y, z, 5) for x, y, z, _ in _POINTS)
    cloud = _write_cloud(tmp_path / "unclassified.las", points)

    rasters = rasterize_point_cloud(cloud, grid=_GRID)

    assert rasters.ground_point_count == 0
    assert (rasters.terrain == -9999.0).all()
    assert any(
        "no ground-classified returns" in item
        for item in baseline_discrepancies(rasters, expected_point_count=4)
    )


def test_unreadable_point_data_fails_clearly(tmp_path):
    broken = tmp_path / "broken.las"
    broken.write_bytes(b"not a point cloud")
    with pytest.raises(PointCloudError, match="cannot read point data"):
        rasterize_point_cloud(broken, grid=_GRID)


def test_derived_grid_is_sealed_as_a_cog_on_the_shared_lattice(tmp_path):
    cloud = _write_cloud(tmp_path / "cloud.las")
    rasters = rasterize_point_cloud(cloud, grid=_GRID)

    out = write_surface_cog(rasters.surface, _GRID, tmp_path / "dsm.tif")

    assert raster_writers.is_cog(out)
    with rasterio.open(out) as dataset:
        assert dataset.crs.to_epsg() == 32647
        assert dataset.nodata == pytest.approx(-9999.0)
        assert (dataset.width, dataset.height) == (_GRID.width, _GRID.height)
        assert tuple(dataset.bounds) == pytest.approx(_GRID.bounds)
        assert dataset.read(1)[0, 0] == pytest.approx(15.0)
