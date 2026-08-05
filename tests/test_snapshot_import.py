"""Phase 03 source imports preserve exact bytes and truthful spatial metadata."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin

from buduunkhad.geospatial_ai.path_safety import PathSafetyError, StorageRoots
from buduunkhad.geospatial_ai.snapshots import (
    import_phase03_snapshot_source,
    load_snapshot_import_authority,
    verify_phase03_snapshot_source,
)


@pytest.fixture
def roots(tmp_path: Path) -> StorageRoots:
    paths = {name: tmp_path / name for name in ("raw", "snapshots", "work")}
    for path in paths.values():
        path.mkdir()
    return StorageRoots(
        raw_root=paths["raw"],
        snapshot_root=paths["snapshots"],
        work_root=paths["work"],
    )


def _raster(path: Path, *, crs: str | None = "EPSG:32647") -> Path:
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        width=4,
        height=3,
        count=1,
        dtype="uint8",
        crs=crs,
        transform=from_origin(300_000, 5_100_000, 10, 10),
    ) as dataset:
        dataset.write(np.ones((1, 3, 4), dtype="uint8"))
    return path


def test_georeferenced_source_import_is_atomic_idempotent_and_revalidated(
    roots: StorageRoots,
    tmp_path: Path,
) -> None:
    source = _raster(tmp_path / "map.tif")
    imported, authority = import_phase03_snapshot_source(
        source,
        source_id="regional-geology-200k",
        role="georeferenced-map",
        imported_by="Synthetic Operator",
        import_reason="Synthetic exact-source intake test.",
        roots=roots,
        now=datetime(2026, 8, 5, tzinfo=UTC),
    )

    assert imported.read_bytes() == source.read_bytes()
    assert authority.raster_crs == "EPSG:32647"
    assert (authority.raster_width, authority.raster_height, authority.raster_band_count) == (
        4,
        3,
        1,
    )
    verify_phase03_snapshot_source(imported, roots=roots)
    repeated, repeated_authority = import_phase03_snapshot_source(
        source,
        source_id="regional-geology-200k",
        role="georeferenced-map",
        imported_by="Another Operator",
        import_reason="The same bytes must resolve idempotently.",
        roots=roots,
    )
    assert repeated == imported
    assert repeated_authority == authority

    imported.write_bytes(imported.read_bytes() + b"changed")
    with pytest.raises(PathSafetyError, match="bytes changed"):
        load_snapshot_import_authority(imported.parents[1] / "snapshot-import.json", roots=roots)


def test_snapshot_import_fails_closed_before_creating_invalid_packages(
    roots: StorageRoots,
    tmp_path: Path,
) -> None:
    source = _raster(tmp_path / "crsless.tif", crs=None)
    with pytest.raises(PathSafetyError, match="explicit CRS"):
        import_phase03_snapshot_source(
            source,
            source_id="crsless-map",
            role="georeferenced-map",
            imported_by="Synthetic Operator",
            import_reason="Reject missing spatial authority.",
            roots=roots,
        )
    assert not (roots.require_snapshot_root() / "phase03-imported-sources").exists()

    with pytest.raises(PathSafetyError, match="source ID"):
        import_phase03_snapshot_source(
            source,
            source_id="../escape",
            role="legend",
            imported_by="Synthetic Operator",
            import_reason="Reject traversal before writing.",
            roots=roots,
        )


def test_legend_import_records_bytes_without_claiming_spatial_metadata(
    roots: StorageRoots,
    tmp_path: Path,
) -> None:
    source = tmp_path / "legend.jpg"
    source.write_bytes(b"synthetic-legend-bytes")
    imported, authority = import_phase03_snapshot_source(
        source,
        source_id="regional-geology-legend",
        role="legend",
        imported_by="Synthetic Operator",
        import_reason="Synthetic legend intake test.",
        roots=roots,
    )
    assert imported.read_bytes() == source.read_bytes()
    assert authority.raster_crs is None
    verify_phase03_snapshot_source(imported, roots=roots)
