"""Bounded-memory rasterisation and QA of the acquired per-block point clouds.

The campaign delivers one classified cloud per survey block, and the whole set is far too
large to hold in memory: roughly twelve billion points across seventy-eight blocks.  Every
product this module derives is therefore accumulated in a single streaming pass per block.
Decompressing a block is the expensive step, so one pass produces the surface models, the
return-density grid and the classification census together rather than reading three times.

Point data needs ``laspy`` (with ``lazrs`` for the compressed ``.laz`` delivery format), which
is an optional extra.  Header-only inspection does not: :func:`buduunkhad.core.phase05_drone.
inspect_las` parses the public header block, and that block is byte-identical in LAS and LAZ.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import numpy as np

#: ASPRS standard classification for bare-earth returns; the DTM is built from these alone.
GROUND_CLASSIFICATION = 2

#: Points decompressed per chunk. Ten million keeps peak memory near 250 MB while leaving
#: the per-chunk numpy work large enough that Python-level overhead stays negligible.
DEFAULT_CHUNK_SIZE = 10_000_000

_NODATA = -9999.0


class PointCloudError(RuntimeError):
    """A delivered point cloud cannot produce a truthful Phase 05 product."""


def laspy_available() -> bool:
    """Report whether point data can be read at all, without importing at module scope."""

    try:
        import laspy  # noqa: F401
    except ImportError:
        return False
    return True


def require_laspy():
    """Import laspy, converting the optional-dependency failure into a phase-level error."""

    try:
        import laspy
    except ImportError as exc:  # pragma: no cover - exercised only without the extra
        raise PointCloudError(
            "reading point data requires the 'pointcloud' extra: pip install 'buduunkhad[pointcloud]'"
        ) from exc
    return laspy


@dataclass(frozen=True)
class PointCloudGrid:
    """A north-up raster lattice shared by every product derived from the clouds.

    Blocks overlap by design, so each one is rasterised onto a lattice snapped to a common
    origin.  That makes the per-block grids exactly co-registered, which is what lets them be
    mosaicked later without resampling and differenced against the supplied DEM.
    """

    origin_x: float
    origin_y: float  # north (top) edge, matching raster convention
    resolution: float
    width: int
    height: int
    epsg: int

    def __post_init__(self) -> None:
        if self.resolution <= 0:
            raise PointCloudError(f"grid resolution must be positive: {self.resolution}")
        if self.width <= 0 or self.height <= 0:
            raise PointCloudError(f"grid must have positive extent: {self.width}x{self.height}")

    @classmethod
    def covering(
        cls,
        bounds: tuple[float, float, float, float],
        *,
        resolution: float,
        epsg: int,
        snap_x: float = 0.0,
        snap_y: float = 0.0,
    ) -> PointCloudGrid:
        """Build the smallest lattice covering ``bounds`` and aligned to a shared anchor.

        ``snap_x`` / ``snap_y`` name a coordinate the lattice edges must fall on — pass the
        final DEM mosaic's origin so derived surfaces land on the same cells as the existing
        terrain products.
        """

        if resolution <= 0:
            raise PointCloudError(f"grid resolution must be positive: {resolution}")
        min_x, min_y, max_x, max_y = (float(value) for value in bounds)
        if not (max_x > min_x and max_y > min_y):
            raise PointCloudError(f"grid bounds must be non-degenerate: {bounds}")
        left = snap_x + np.floor((min_x - snap_x) / resolution) * resolution
        top = snap_y + np.ceil((max_y - snap_y) / resolution) * resolution
        width = int(np.ceil((max_x - left) / resolution))
        height = int(np.ceil((top - min_y) / resolution))
        return cls(
            origin_x=float(left),
            origin_y=float(top),
            resolution=float(resolution),
            width=max(width, 1),
            height=max(height, 1),
            epsg=epsg,
        )

    @property
    def bounds(self) -> tuple[float, float, float, float]:
        return (
            self.origin_x,
            self.origin_y - self.height * self.resolution,
            self.origin_x + self.width * self.resolution,
            self.origin_y,
        )

    @property
    def cell_count(self) -> int:
        return self.width * self.height

    def transform(self):
        from rasterio.transform import from_origin

        return from_origin(self.origin_x, self.origin_y, self.resolution, self.resolution)

    def flat_indices(self, x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Map coordinates to flat cell indices, returning the in-bounds selection mask.

        Points outside the lattice are reported rather than silently wrapped, because a block
        whose points fall outside its own grid signals a CRS or bounds error upstream.
        """

        col = np.floor((x - self.origin_x) / self.resolution).astype(np.int64)
        row = np.floor((self.origin_y - y) / self.resolution).astype(np.int64)
        inside = (col >= 0) & (col < self.width) & (row >= 0) & (row < self.height)
        return row * self.width + col, inside


@dataclass(frozen=True)
class PointCloudRasters:
    """The surfaces and coverage grids produced by one streaming pass over a block."""

    grid: PointCloudGrid
    surface: np.ndarray  # DSM: highest return per cell
    terrain: np.ndarray  # DTM: lowest ground-classified return per cell
    return_count: np.ndarray  # returns per cell, all classes
    classification_counts: dict[int, int]
    total_points: int
    points_outside_grid: int

    @property
    def surface_coverage(self) -> float:
        """Fraction of cells carrying at least one return."""

        return float(np.count_nonzero(self.return_count) / self.grid.cell_count)

    @property
    def terrain_coverage(self) -> float:
        """Fraction of cells carrying at least one ground-classified return."""

        return float(np.count_nonzero(self.terrain != _NODATA) / self.grid.cell_count)

    @property
    def ground_point_count(self) -> int:
        return int(self.classification_counts.get(GROUND_CLASSIFICATION, 0))

    @property
    def mean_density_per_m2(self) -> float:
        """Mean returns per square metre over covered cells only.

        Averaging over covered cells rather than the whole lattice keeps the figure
        comparable between blocks whose footprints fill their bounding box differently.
        """

        covered = self.return_count[self.return_count > 0]
        if covered.size == 0:
            return 0.0
        return float(covered.mean() / (self.grid.resolution**2))


def iter_point_chunks(
    path: Path, *, chunk_size: int = DEFAULT_CHUNK_SIZE
) -> Iterator[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    """Yield ``(x, y, z, classification)`` arrays for successive chunks of a LAS/LAZ file.

    Scaled coordinates are materialised per chunk; the raw integer arrays are never held for
    the whole file, which is what keeps a nine-gigabyte block inside a few hundred megabytes.
    """

    laspy = require_laspy()
    path = Path(path)
    try:
        with laspy.open(str(path)) as reader:
            for chunk in reader.chunk_iterator(chunk_size):
                yield (
                    np.asarray(chunk.x, dtype="float64"),
                    np.asarray(chunk.y, dtype="float64"),
                    np.asarray(chunk.z, dtype="float64"),
                    np.asarray(chunk.classification, dtype="uint8"),
                )
    except PointCloudError:
        raise
    except Exception as exc:  # noqa: BLE001 - any reader failure is a data-quality result
        raise PointCloudError(f"cannot read point data from {path.name}: {exc}") from exc


def rasterize_point_cloud(
    path: Path,
    *,
    grid: PointCloudGrid,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    ground_classifications: tuple[int, ...] = (GROUND_CLASSIFICATION,),
) -> PointCloudRasters:
    """Derive surface, terrain, density and classification products in one pass.

    The surface model takes the highest return in each cell and the terrain model the lowest
    ground-classified return, which is the conventional pairing: the first follows canopy and
    structures, the second the bare earth beneath them.  Cells with no contributing return keep
    nodata instead of being interpolated, so coverage gaps stay visible downstream.
    """

    cells = grid.cell_count
    surface = np.full(cells, -np.inf, dtype="float64")
    terrain = np.full(cells, np.inf, dtype="float64")
    counts = np.zeros(cells, dtype="int64")
    classification_counts: dict[int, int] = {}
    total_points = 0
    outside = 0
    ground = np.asarray(ground_classifications, dtype="uint8")

    for x, y, z, classification in iter_point_chunks(path, chunk_size=chunk_size):
        total_points += int(x.size)
        flat, inside = grid.flat_indices(x, y)
        outside += int(np.count_nonzero(~inside))

        values, occurrences = np.unique(classification, return_counts=True)
        for value, occurrence in zip(values.tolist(), occurrences.tolist(), strict=True):
            classification_counts[int(value)] = classification_counts.get(int(value), 0) + int(
                occurrence
            )

        if not inside.any():
            continue
        flat_in = flat[inside]
        z_in = z[inside]
        counts += np.bincount(flat_in, minlength=cells)
        np.maximum.at(surface, flat_in, z_in)

        is_ground = np.isin(classification[inside], ground)
        if is_ground.any():
            np.minimum.at(terrain, flat_in[is_ground], z_in[is_ground])

    surface = np.where(np.isfinite(surface), surface, _NODATA)
    terrain = np.where(np.isfinite(terrain), terrain, _NODATA)
    return PointCloudRasters(
        grid=grid,
        surface=surface.reshape(grid.height, grid.width).astype("float32"),
        terrain=terrain.reshape(grid.height, grid.width).astype("float32"),
        return_count=counts.reshape(grid.height, grid.width).astype("int32"),
        classification_counts=dict(sorted(classification_counts.items())),
        total_points=total_points,
        points_outside_grid=outside,
    )


def write_surface_cog(
    array: np.ndarray,
    grid: PointCloudGrid,
    destination: Path,
    *,
    dtype: str = "float32",
    nodata: float | int = _NODATA,
) -> Path:
    """Seal one derived grid as a Cloud-Optimized GeoTIFF on the shared lattice."""

    import tempfile

    import rasterio

    from buduunkhad.core import raster_writers

    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    profile = {
        "driver": "GTiff",
        "height": grid.height,
        "width": grid.width,
        "count": 1,
        "dtype": dtype,
        "crs": f"EPSG:{grid.epsg}",
        "transform": grid.transform(),
        "nodata": nodata,
        "tiled": True,
        "blockxsize": 512,
        "blockysize": 512,
        "compress": "DEFLATE",
    }
    with tempfile.TemporaryDirectory(prefix="p05-cloud-") as temp:
        plain = Path(temp) / "grid.tif"
        with rasterio.open(plain, "w", **profile) as target:
            target.write(array.astype(dtype), 1)
        raster_writers.write_cog(
            plain,
            destination,
            compress="DEFLATE",
            predictor=raster_writers.predictor_for(dtype),
            overview_resampling="AVERAGE" if dtype.startswith("float") else "NEAREST",
        )
    return destination


def baseline_discrepancies(
    rasters: PointCloudRasters,
    *,
    expected_point_count: int | None,
) -> tuple[str, ...]:
    """Compare a converted delivery against the header baseline taken from the originals.

    A LAS-to-LAZ conversion that dropped points, reprojected, or discarded classification is
    otherwise silent, so the point census is checked explicitly rather than assumed.
    """

    problems: list[str] = []
    if expected_point_count is not None and rasters.total_points != expected_point_count:
        problems.append(
            f"point count {rasters.total_points} does not match baseline {expected_point_count}"
        )
    if rasters.points_outside_grid:
        problems.append(f"{rasters.points_outside_grid} point(s) fall outside the block grid")
    if rasters.ground_point_count == 0:
        problems.append("no ground-classified returns; a bare-earth terrain model is not derivable")
    return tuple(problems)
