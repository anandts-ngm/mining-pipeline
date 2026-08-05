from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from buduunkhad.core import kompsat


def _bundle(root: Path) -> dict[str, Path]:
    images: dict[str, Path] = {}
    for index, role in enumerate(kompsat.KOMPSAT_ROLES, start=1):
        image = root / "03_KOMPSAT2_MSC_L1G" / f"asset-{index}.tif"
        image.parent.mkdir(parents=True, exist_ok=True)
        image.write_bytes(f"image-{role}".encode())
        for suffix in kompsat.REQUIRED_SIDECARS:
            image.with_suffix(suffix).write_bytes(f"{role}-{suffix}".encode())
        images[role] = image
    return images


def test_kompsat_inventory_hashes_exact_bundle_without_opening_images(tmp_path: Path) -> None:
    root = tmp_path / "phase00"
    images = _bundle(root)
    record_path = tmp_path / "inventory.json"
    record = kompsat.inventory_bundle(
        root,
        images,
        record_path,
        source_run_id="source-run",
        processing_run_id="processing-run",
    )

    assert record.inventory_complete
    assert not record.image_content_opened
    assert record.processing_status == "excluded-meth-ready-002"
    assert tuple(asset.role for asset in record.assets) == kompsat.KOMPSAT_ROLES
    assert all(len(asset.sidecars) == 3 for asset in record.assets)
    assert kompsat.load_inventory_record(record_path) == record


def test_kompsat_inventory_fails_when_a_sidecar_is_missing(tmp_path: Path) -> None:
    root = tmp_path / "phase00"
    images = _bundle(root)
    images["RED"].with_suffix(".rpc").unlink()

    with pytest.raises(kompsat.KompsatInventoryError, match="inventory failed"):
        kompsat.inventory_bundle(
            root,
            images,
            tmp_path / "inventory.json",
            source_run_id="source-run",
            processing_run_id="processing-run",
        )


def test_brovey_rgb_is_aligned_bounded_and_preserves_invalid_pixels() -> None:
    rgb = np.array(
        [
            [[10, 0], [30, 20]],
            [[20, 0], [30, 20]],
            [[30, 0], [30, 20]],
        ],
        dtype="uint16",
    )
    pan = np.array([[40, 50], [30, 0]], dtype="uint16")

    result = kompsat.brovey_rgb(rgb, pan)

    assert result.dtype == np.uint16
    assert result.shape == rgb.shape
    assert result[:, 0, 0].tolist() == [20, 40, 60]
    assert result[:, 0, 1].tolist() == [0, 0, 0]
    assert result[:, 1, 0].tolist() == [30, 30, 30]
    assert result[:, 1, 1].tolist() == [0, 0, 0]


def test_aoi_mask_reads_and_updates_a_writable_rpc_target(tmp_path: Path) -> None:
    import rasterio
    from rasterio.transform import from_origin
    from shapely.geometry import box

    path = tmp_path / "rpc-target.tif"
    profile = {
        "driver": "GTiff",
        "width": 4,
        "height": 4,
        "count": 1,
        "dtype": "uint16",
        "crs": "EPSG:32647",
        "transform": from_origin(0, 4, 1, 1),
        "nodata": 0,
        "tiled": True,
        "blockxsize": 16,
        "blockysize": 16,
    }
    with rasterio.open(path, "w+", **profile) as dataset:
        dataset.write(np.ones((4, 4), dtype="uint16"), 1)
        kompsat._mask_outside_geometry(dataset, box(0, 0, 2, 4))

    with rasterio.open(path) as dataset:
        values = dataset.read(1)
    assert np.all(values[:, :2] == 1)
    assert np.all(values[:, 2:] == 0)


def test_kompsat_processing_record_forbids_external_distribution() -> None:
    source = kompsat.KompsatSourceInspection(
        role="PAN",
        identity=kompsat.KompsatFileIdentity(path="pan.tif", sha256="a" * 64, size_bytes=1),
        source_epsg=32647,
        width=1,
        height=1,
        resolution_m=1,
        dtype="uint16",
        rpc_present=True,
        image_level="L1G",
        product_level="RPC",
        source_dem_record="NULL",
        source_licence_record="NULL",
    )
    sources = tuple(
        source.model_copy(
            update={
                "role": role,
                "identity": source.identity.model_copy(update={"path": f"{role}.tif"}),
                "resolution_m": 1 if role == "PAN" else 4,
            }
        )
        for role in kompsat.KOMPSAT_ROLES
    )
    outputs = tuple(
        kompsat.KompsatOutputIdentity(
            product_id=product,
            identity=kompsat.KompsatFileIdentity(
                path=f"{product}.tif", sha256="b" * 64, size_bytes=1
            ),
            media_type="image/tiff; application=geotiff",
            target_epsg=32647,
            width=1,
            height=1,
            resolution_m=1,
            band_count=1,
            dtype="uint16",
            cog_valid=True,
        )
        for product in kompsat.PROCESSING_PRODUCTS
    ) + (
        kompsat.KompsatOutputIdentity(
            product_id="interpretation",
            identity=kompsat.KompsatFileIdentity(
                path="interpretation.gpkg", sha256="c" * 64, size_bytes=1
            ),
            media_type="application/geopackage+sqlite3",
            target_epsg=32647,
            layer_names=("lineament_interpretation_line",),
        ),
    )
    record = kompsat.KompsatProcessingRecord(
        source_run_id="source",
        processing_run_id="run",
        source_assets=sources,
        rpc_dem=kompsat.KompsatFileIdentity(path="dem.tif", sha256="d" * 64, size_bytes=1),
        target_epsg=32647,
        clip_buffer_m=1000,
        pan_resolution_m=1,
        multispectral_resolution_m=4,
        multispectral_band_order=kompsat.MS_BAND_ORDER,
        outputs=outputs,
        ndvi_min=-0.5,
        ndvi_max=0.5,
        lineament_feature_count=0,
        licence_record_present=False,
        limitation="local only",
    )
    assert not record.external_egress_allowed
    payload = record.model_dump(mode="json")
    payload["external_egress_allowed"] = True
    with pytest.raises(ValueError, match="external KOMPSAT distribution"):
        kompsat.KompsatProcessingRecord.model_validate(payload)
