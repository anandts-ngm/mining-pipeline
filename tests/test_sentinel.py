from __future__ import annotations

import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import geopandas as gpd
import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin
from shapely.geometry import box

from buduunkhad.core import raster_writers, sentinel


def _write_band(path: Path, value: int, *, scl: bool = False) -> Path:
    data = np.full((12, 12), value, dtype="uint16" if not scl else "uint8")
    if scl:
        data[3, 3] = 9
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        width=12,
        height=12,
        count=1,
        dtype=data.dtype,
        crs="EPSG:32647",
        transform=from_origin(300000, 5100000, 10, 10),
        nodata=0,
    ) as dataset:
        dataset.write(data, 1)
    return path


def _safe_zip(tmp_path: Path, *, omit: str | None = None) -> Path:
    archive = tmp_path / "synthetic.SAFE.zip"
    values = {
        "B02": 2000,
        "B03": 2500,
        "B04": 2000,
        "B05": 2400,
        "B06": 2600,
        "B07": 2800,
        "B08": 4000,
        "B8A": 3600,
        "B11": 3000,
        "B12": 2500,
        "SCL": 4,
    }
    metadata = """<?xml version="1.0" encoding="UTF-8"?>
    <Level2A_User_Product>
      <BOA_QUANTIFICATION_VALUE>10000</BOA_QUANTIFICATION_VALUE>
      <BOA_ADD_OFFSET_VALUES_LIST>
        {offsets}
      </BOA_ADD_OFFSET_VALUES_LIST>
    </Level2A_User_Product>
    """.format(
        offsets="\n".join(
            f'<BOA_ADD_OFFSET band_id="{band_id}">-1000</BOA_ADD_OFFSET>' for band_id in range(13)
        )
    )
    with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
        bundle.writestr("SYNTHETIC.SAFE/MTD_MSIL2A.xml", metadata)
        for band, value in values.items():
            if band == omit:
                continue
            resolution = "10m" if band in {"B02", "B03", "B04", "B08"} else "20m"
            source = _write_band(tmp_path / f"{band}.tif", value, scl=band == "SCL")
            bundle.write(
                source,
                f"SYNTHETIC.SAFE/GRANULE/G/IMG_DATA/R{resolution}/SYN_{band}_{resolution}.tif",
            )
    return archive


def test_safe_archive_requires_every_band(tmp_path: Path) -> None:
    archive = _safe_zip(tmp_path, omit="B12")
    with pytest.raises(sentinel.SentinelProcessingError, match="B12"):
        sentinel.inspect_safe_archive(archive)


def test_safe_source_resolution_is_path_and_hash_bound(tmp_path: Path) -> None:
    archive = _safe_zip(tmp_path)
    phase00 = tmp_path / "phase00"
    target = phase00 / "08_Supplementary_Source_Documents" / archive.name
    target.parent.mkdir(parents=True)
    target.write_bytes(archive.read_bytes())
    expected_hash = hashlib.sha256(target.read_bytes()).hexdigest()

    assert (
        sentinel.resolve_safe_archive(
            phase00,
            f"08_Supplementary_Source_Documents/{archive.name}",
            expected_sha256=expected_hash,
            expected_size_bytes=target.stat().st_size,
        )
        == target.resolve()
    )
    with pytest.raises(sentinel.SentinelProcessingError, match="SHA-256"):
        sentinel.resolve_safe_archive(
            phase00,
            f"08_Supplementary_Source_Documents/{archive.name}",
            expected_sha256="0" * 64,
            expected_size_bytes=target.stat().st_size,
        )


def test_safe_archive_produces_complete_cog_set_and_record(tmp_path: Path) -> None:
    archive = _safe_zip(tmp_path)
    source = sentinel.inspect_safe_archive(archive)
    assert source.quantification_value == 10000
    assert source.additive_offsets["B08"] == -1000
    assert set(source.band_members) == set(sentinel.REQUIRED_BANDS)

    aoi = gpd.GeoDataFrame(  # ty: ignore[no-matching-overload]
        {"name": ["AOI"]},
        geometry=[box(300000, 5099880, 300120, 5100000)],
        crs="EPSG:32647",
    )
    outputs = {key: tmp_path / "out" / f"{key}.tif" for key in sentinel.PRODUCT_KEYS}
    record_path = tmp_path / "out" / "sentinel-record.json"
    result = sentinel.process_safe_archive(
        archive,
        aoi,
        outputs,
        record_path,
        source_run_id="source-run",
        processing_run_id="processing-run",
        target_epsg=32647,
    )

    assert result.record.valid_pixel_count == 144
    assert len(result.outputs) == len(sentinel.PRODUCT_KEYS)
    assert sentinel.load_processing_record(record_path) == result.record
    for path in result.outputs:
        assert raster_writers.is_cog(path)

    with rasterio.open(outputs["NDVI"]) as dataset:
        ndvi = dataset.read(1)
        assert ndvi[0, 0] == pytest.approx(0.5)
        assert dataset.crs.to_epsg() == 32647
        assert dataset.nodata == -9999.0
    with rasterio.open(outputs["NaturalRGB"]) as dataset:
        assert dataset.count == 3
        assert dataset.descriptions == ("Red B04", "Green B03", "Blue B02")
    with rasterio.open(outputs["CloudShadowMask"]) as dataset:
        mask = dataset.read(1)
        assert mask[3, 3] == 1
        assert dataset.nodata == 255
