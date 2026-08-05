"""Exact KOMPSAT-2 inventory and local deterministic support processing."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from collections.abc import Mapping
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from buduunkhad.core.run_artifacts import ArtifactSealError, require_regular_file_under

KompsatRole = Literal["PAN", "GREEN", "BLUE", "NIR", "RED"]
KOMPSAT_ROLES: tuple[KompsatRole, ...] = ("PAN", "GREEN", "BLUE", "NIR", "RED")
REQUIRED_SIDECARS = (".txt", ".rpc", ".eph")
MS_BAND_ORDER: tuple[KompsatRole, ...] = ("BLUE", "GREEN", "RED", "NIR")
PROCESSING_PRODUCTS = (
    "pan_ortho",
    "ms_ortho_bundle",
    "ms_stack",
    "true_color",
    "false_color",
    "ndvi",
    "pansharpened",
)


class KompsatInventoryError(RuntimeError):
    """Raised when an exact KOMPSAT bundle cannot be inventoried safely."""


class KompsatProcessingError(RuntimeError):
    """Raised when a KOMPSAT source or deterministic derivative fails validation."""


class KompsatFileIdentity(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    path: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    size_bytes: int = Field(ge=1)


class KompsatAssetInventory(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    role: KompsatRole
    image: KompsatFileIdentity
    sidecars: tuple[KompsatFileIdentity, ...]

    @model_validator(mode="after")
    def _sidecars_are_complete(self) -> KompsatAssetInventory:
        if tuple(Path(item.path).suffix.casefold() for item in self.sidecars) != REQUIRED_SIDECARS:
            raise ValueError("KOMPSAT sidecars must be ordered TXT, RPC and EPH")
        return self


class KompsatBundleInventoryRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    format_version: Literal["1.0.0"] = "1.0.0"
    source_run_id: str
    processing_run_id: str
    assets: tuple[KompsatAssetInventory, ...]
    inventory_complete: bool
    image_content_opened: bool = False
    processing_status: Literal["excluded-meth-ready-002"] = "excluded-meth-ready-002"
    validation_status: str = "Inventory evidence only"
    limitation: str = (
        "KOMPSAT imagery was not opened, processed, transmitted or published; exact licence "
        "and technical readiness remain unresolved under METH-READY-002"
    )

    @field_validator("source_run_id", "processing_run_id")
    @classmethod
    def _non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("KOMPSAT run identities must be non-empty")
        return value

    @model_validator(mode="after")
    def _roles_are_exact(self) -> KompsatBundleInventoryRecord:
        if tuple(item.role for item in self.assets) != KOMPSAT_ROLES:
            raise ValueError("KOMPSAT inventory must contain PAN/GREEN/BLUE/NIR/RED in order")
        if not self.inventory_complete:
            raise ValueError("a persisted KOMPSAT inventory record must be complete")
        if self.image_content_opened:
            raise ValueError("METH-READY-002 inventory must not claim image content was opened")
        return self


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _identity(root: Path, path: Path) -> KompsatFileIdentity:
    resolved = require_regular_file_under(root, path, description="KOMPSAT bundle file")
    return KompsatFileIdentity(
        path=resolved.relative_to(Path(root).resolve()).as_posix(),
        sha256=_sha256(resolved),
        size_bytes=resolved.stat().st_size,
    )


def inventory_bundle(
    phase00_root: Path,
    images: Mapping[str, Path],
    record_path: Path,
    *,
    source_run_id: str,
    processing_run_id: str,
) -> KompsatBundleInventoryRecord:
    """Hash the five registered parent images and every required sidecar without opening them."""

    if tuple(images) != KOMPSAT_ROLES:
        raise KompsatInventoryError("KOMPSAT image mapping must be PAN/GREEN/BLUE/NIR/RED")
    root = Path(phase00_root)
    assets: list[KompsatAssetInventory] = []
    try:
        for role, image_path in images.items():
            image = Path(image_path)
            sidecars = tuple(
                _identity(root, image.with_suffix(suffix)) for suffix in REQUIRED_SIDECARS
            )
            assets.append(
                KompsatAssetInventory(
                    role=cast(KompsatRole, role),
                    image=_identity(root, image),
                    sidecars=sidecars,
                )
            )
        record = KompsatBundleInventoryRecord(
            source_run_id=source_run_id,
            processing_run_id=processing_run_id,
            assets=tuple(assets),
            inventory_complete=True,
        )
    except (ArtifactSealError, OSError, ValueError) as exc:
        raise KompsatInventoryError(f"KOMPSAT bundle inventory failed: {exc}") from exc
    target = Path(record_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(record.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return record


def load_inventory_record(path: Path) -> KompsatBundleInventoryRecord:
    return KompsatBundleInventoryRecord.model_validate_json(Path(path).read_text(encoding="utf-8"))


class KompsatSourceInspection(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    role: KompsatRole
    identity: KompsatFileIdentity
    source_epsg: int
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    resolution_m: float = Field(gt=0)
    dtype: str
    rpc_present: bool
    image_level: str
    product_level: str
    source_dem_record: str
    source_licence_record: str


class KompsatOutputIdentity(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    product_id: str
    identity: KompsatFileIdentity
    media_type: Literal["image/tiff; application=geotiff", "application/geopackage+sqlite3"]
    target_epsg: int
    width: int | None = Field(default=None, ge=1)
    height: int | None = Field(default=None, ge=1)
    resolution_m: float | None = Field(default=None, gt=0)
    band_count: int | None = Field(default=None, ge=1)
    dtype: str | None = None
    cog_valid: bool | None = None
    layer_names: tuple[str, ...] = ()


class KompsatProcessingRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    format_version: Literal["1.0.0"] = "1.0.0"
    source_run_id: str
    processing_run_id: str
    authority_basis: Literal["METH-DISC-074"] = "METH-DISC-074"
    processing_status: Literal["completed-local-support-evidence"] = (
        "completed-local-support-evidence"
    )
    source_assets: tuple[KompsatSourceInspection, ...]
    rpc_dem: KompsatFileIdentity
    target_epsg: int
    clip_buffer_m: int = Field(ge=0)
    pan_resolution_m: float = Field(gt=0)
    multispectral_resolution_m: float = Field(gt=0)
    multispectral_band_order: tuple[KompsatRole, ...]
    orthorectification_method: Literal["RPC_DEM"] = "RPC_DEM"
    pansharpen_method: Literal["Brovey-RGB"] = "Brovey-RGB"
    outputs: tuple[KompsatOutputIdentity, ...]
    ndvi_min: float = Field(ge=-1.0, le=1.0)
    ndvi_max: float = Field(ge=-1.0, le=1.0)
    lineament_feature_count: int = Field(ge=0)
    licence_record_present: bool
    external_egress_allowed: bool = False
    external_publication_allowed: bool = False
    limitation: str

    @model_validator(mode="after")
    def _record_is_coherent(self) -> KompsatProcessingRecord:
        if tuple(item.role for item in self.source_assets) != KOMPSAT_ROLES:
            raise ValueError("KOMPSAT processing sources must be PAN/GREEN/BLUE/NIR/RED")
        if self.multispectral_band_order != MS_BAND_ORDER:
            raise ValueError("KOMPSAT multispectral order must be BLUE/GREEN/RED/NIR")
        expected = (*PROCESSING_PRODUCTS, "interpretation")
        if tuple(item.product_id for item in self.outputs) != expected:
            raise ValueError("KOMPSAT processing outputs are incomplete or out of order")
        if any(not item.rpc_present for item in self.source_assets):
            raise ValueError("every processed KOMPSAT source must expose RPC metadata")
        if self.external_egress_allowed or self.external_publication_allowed:
            raise ValueError("METH-DISC-074 does not authorize external KOMPSAT distribution")
        return self


class KompsatProcessingResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", arbitrary_types_allowed=True)

    raster_outputs: tuple[Path, ...]
    interpretation_path: Path
    record_path: Path
    record: KompsatProcessingRecord


def _metadata_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        parts = raw.strip().split(None, 1)
        if len(parts) == 2:
            values[parts[0]] = parts[1].strip()
    return values


def _inspect_source(root: Path, role: KompsatRole, path: Path) -> KompsatSourceInspection:
    import rasterio

    resolved = require_regular_file_under(root, path, description="KOMPSAT source raster")
    metadata_path = require_regular_file_under(
        root, resolved.with_suffix(".txt"), description="KOMPSAT metadata sidecar"
    )
    metadata = _metadata_values(metadata_path)
    with rasterio.open(resolved) as dataset:
        epsg = dataset.crs.to_epsg() if dataset.crs is not None else None
        if epsg is None:
            raise KompsatProcessingError(f"{resolved.name} has no declared EPSG CRS")
        if dataset.count != 1:
            raise KompsatProcessingError(f"{resolved.name} must contain exactly one band")
        if dataset.rpcs is None:
            raise KompsatProcessingError(f"{resolved.name} has no readable RPC metadata")
        if abs(abs(dataset.res[0]) - abs(dataset.res[1])) > 1e-6:
            raise KompsatProcessingError(f"{resolved.name} has non-square pixels")
        return KompsatSourceInspection(
            role=role,
            identity=_identity(root, resolved),
            source_epsg=epsg,
            width=dataset.width,
            height=dataset.height,
            resolution_m=abs(float(dataset.res[0])),
            dtype=dataset.dtypes[0],
            rpc_present=True,
            image_level=metadata.get("AUX_IMAGE_LEVEL", ""),
            product_level=metadata.get("AUX_PRODUCT_LEVEL", ""),
            source_dem_record=metadata.get("CAL_DEM_FILE", ""),
            source_licence_record=metadata.get("LICENCE", ""),
        )


def _aoi_geometry(aoi_gdf: Any, target_epsg: int) -> Any:
    if aoi_gdf is None or len(aoi_gdf) == 0:
        raise KompsatProcessingError("KOMPSAT processing requires a non-empty clip AOI")
    if aoi_gdf.crs is None:
        raise KompsatProcessingError("KOMPSAT clip AOI has no CRS")
    projected = aoi_gdf.to_crs(epsg=target_epsg)
    geometry = (
        projected.geometry.union_all()
        if hasattr(projected.geometry, "union_all")
        else projected.geometry.unary_union
    )
    if geometry.is_empty or not geometry.is_valid:
        raise KompsatProcessingError("KOMPSAT clip AOI is empty or invalid")
    return geometry


def _aligned_grid(geometry: Any, resolution_m: float) -> tuple[Any, int, int]:
    from rasterio.transform import from_origin

    left, bottom, right, top = geometry.bounds
    x_origin = math.floor(left / resolution_m) * resolution_m
    y_origin = math.ceil(top / resolution_m) * resolution_m
    width = math.ceil((right - x_origin) / resolution_m)
    height = math.ceil((y_origin - bottom) / resolution_m)
    return from_origin(x_origin, y_origin, resolution_m, resolution_m), width, height


def _mask_outside_geometry(dataset: Any, geometry: Any) -> None:
    from rasterio.features import geometry_mask
    from rasterio.windows import transform as window_transform
    from shapely.geometry import mapping

    shape = [mapping(geometry)]
    for _, window in dataset.block_windows(1):
        inside = geometry_mask(
            shape,
            out_shape=(int(window.height), int(window.width)),
            transform=window_transform(window, dataset.transform),
            invert=True,
        )
        data = dataset.read(window=window)
        data[:, ~inside] = dataset.nodata
        dataset.write(data, window=window)


def _write_rpc_stack(
    source_paths: tuple[Path, ...],
    destination: Path,
    *,
    dem_path: Path,
    geometry: Any,
    target_epsg: int,
    resolution_m: float,
) -> None:
    import rasterio
    from rasterio.warp import Resampling, reproject

    transform, width, height = _aligned_grid(geometry, resolution_m)
    profile = {
        "driver": "GTiff",
        "width": width,
        "height": height,
        "count": len(source_paths),
        "dtype": "uint16",
        "crs": f"EPSG:{target_epsg}",
        "transform": transform,
        "nodata": 0,
        "tiled": True,
        "blockxsize": 512,
        "blockysize": 512,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(destination, "w+", **profile) as output:
        for output_band, source_path in enumerate(source_paths, start=1):
            with rasterio.open(source_path) as source:
                if source.rpcs is None:
                    raise KompsatProcessingError(f"{source_path.name} has no readable RPC metadata")
                reproject(
                    source=rasterio.band(source, 1),
                    destination=rasterio.band(output, output_band),
                    rpcs=source.rpcs,
                    src_crs=None,
                    src_nodata=0,
                    dst_transform=transform,
                    dst_crs=f"EPSG:{target_epsg}",
                    dst_nodata=0,
                    resampling=Resampling.cubic,
                    num_threads=2,
                    RPC_DEM=str(dem_path),
                )
        _mask_outside_geometry(output, geometry)


def _write_selected_bands(source: Path, destination: Path, bands: tuple[int, ...]) -> None:
    import rasterio

    from buduunkhad.core.raster_writers import predictor_for, write_cog

    with TemporaryDirectory() as tmp:
        plain = Path(tmp) / "selected.tif"
        with rasterio.open(source) as dataset:
            profile = dataset.profile.copy()
            profile.update(driver="GTiff", count=len(bands))
            with rasterio.open(plain, "w", **profile) as output:
                for output_band, source_band in enumerate(bands, start=1):
                    output.write(dataset.read(source_band), output_band)
        write_cog(
            plain,
            destination,
            compress="DEFLATE",
            predictor=predictor_for(profile["dtype"]),
            overview_resampling="AVERAGE",
        )


def _write_ndvi(source: Path, destination: Path) -> tuple[float, float]:
    import numpy as np
    import rasterio

    from buduunkhad.core.raster_writers import write_cog

    minimum = 1.0
    maximum = -1.0
    with TemporaryDirectory() as tmp:
        plain = Path(tmp) / "ndvi.tif"
        with rasterio.open(source) as dataset:
            profile = dataset.profile.copy()
            profile.update(driver="GTiff", count=1, dtype="float32", nodata=-9999.0)
            with rasterio.open(plain, "w", **profile) as output:
                for _, window in dataset.block_windows(1):
                    red = dataset.read(3, window=window).astype("float32")
                    nir = dataset.read(4, window=window).astype("float32")
                    denominator = nir + red
                    valid = (red > 0) & (nir > 0) & (denominator != 0)
                    values = np.full(red.shape, -9999.0, dtype="float32")
                    values[valid] = np.clip(
                        (nir[valid] - red[valid]) / denominator[valid], -1.0, 1.0
                    )
                    if valid.any():
                        minimum = min(minimum, float(values[valid].min()))
                        maximum = max(maximum, float(values[valid].max()))
                    output.write(values, 1, window=window)
        if maximum < minimum:
            raise KompsatProcessingError("KOMPSAT NDVI contains no valid pixels")
        write_cog(
            plain,
            destination,
            compress="DEFLATE",
            predictor="3",
            overview_resampling="AVERAGE",
        )
    return minimum, maximum


def brovey_rgb(rgb: Any, pan: Any) -> Any:
    """Return a Brovey RGB array while preserving invalid zero-valued pixels."""

    import numpy as np

    source = np.asarray(rgb, dtype="float32")
    pan_array = np.asarray(pan, dtype="float32")
    if source.ndim != 3 or source.shape[0] != 3 or source.shape[1:] != pan_array.shape:
        raise ValueError("Brovey input must be three RGB bands aligned to one PAN band")
    denominator = source.sum(axis=0)
    valid = (pan_array > 0) & np.all(source > 0, axis=0) & (denominator > 0)
    result = np.zeros(source.shape, dtype="uint16")
    if valid.any():
        sharpened = source[:, valid] * (3.0 * pan_array[valid] / denominator[valid])
        result[:, valid] = np.clip(sharpened, 0, np.iinfo("uint16").max).astype("uint16")
    return result


def _write_pansharpened(pan_path: Path, multispectral_path: Path, destination: Path) -> None:
    import rasterio
    from rasterio.enums import Resampling
    from rasterio.vrt import WarpedVRT

    from buduunkhad.core.raster_writers import write_cog

    with TemporaryDirectory() as tmp:
        plain = Path(tmp) / "pansharpened.tif"
        with rasterio.open(pan_path) as pan, rasterio.open(multispectral_path) as multispectral:
            profile = pan.profile.copy()
            profile.update(driver="GTiff", count=3, dtype="uint16", nodata=0)
            with (
                WarpedVRT(
                    multispectral,
                    crs=pan.crs,
                    transform=pan.transform,
                    width=pan.width,
                    height=pan.height,
                    resampling=Resampling.cubic,
                    nodata=0,
                ) as aligned,
                rasterio.open(plain, "w", **profile) as output,
            ):
                for _, window in pan.block_windows(1):
                    pan_data = pan.read(1, window=window)
                    rgb = aligned.read((3, 2, 1), window=window)
                    output.write(brovey_rgb(rgb, pan_data), window=window)
        write_cog(
            plain,
            destination,
            compress="DEFLATE",
            predictor="2",
            overview_resampling="AVERAGE",
        )


_INTERPRETATION_PROPERTIES = {
    "feature_id": "str:64",
    "feature_type": "str:64",
    "interpretation_basis": "str:254",
    "source_raw_input_no": "str:16",
    "source_raw_filename": "str:254",
    "processing_phase": "str:8",
    "processing_software": "str:128",
    "processing_action": "str:254",
    "native_crs": "str:64",
    "output_crs": "str:64",
    "confidence": "str:32",
    "validation_status": "str:96",
    "limitation": "str:254",
    "reviewer": "str:128",
    "reviewed_at": "str:32",
}


def _write_interpretation_gpkg(
    pansharpened_path: Path,
    destination: Path,
    *,
    target_epsg: int,
    source_filename: str,
) -> int:
    import fiona
    import numpy as np
    import rasterio
    from affine import Affine
    from pyproj import CRS
    from rasterio.enums import Resampling
    from shapely.geometry import LineString, mapping
    from skimage.feature import canny
    from skimage.transform import probabilistic_hough_line

    with rasterio.open(pansharpened_path) as source:
        output_height = max(1, math.ceil(source.height / 4))
        output_width = max(1, math.ceil(source.width / 4))
        rgb = source.read(
            (1, 2, 3),
            out_shape=(3, output_height, output_width),
            resampling=Resampling.average,
        ).astype("float32")
        transform = source.transform * Affine.scale(
            source.width / output_width, source.height / output_height
        )
    intensity = rgb.mean(axis=0)
    valid = np.all(rgb > 0, axis=0)
    if valid.any():
        low, high = np.percentile(intensity[valid], (2, 98))
        normalized = np.zeros(intensity.shape, dtype="float32")
        normalized[valid] = np.clip(
            (intensity[valid] - low) / max(float(high - low), 1e-6), 0.0, 1.0
        )
        edges = canny(normalized, sigma=2.0)
        edges[~valid] = False
        segments = probabilistic_hough_line(edges, threshold=10, line_length=50, line_gap=5, rng=0)
    else:
        segments = []

    lines: list[LineString] = []
    for (column0, row0), (column1, row1) in segments:
        x0, y0 = cast(tuple[float, float], transform * (column0 + 0.5, row0 + 0.5))
        x1, y1 = cast(tuple[float, float], transform * (column1 + 0.5, row1 + 0.5))
        geometry = LineString(((x0, y0), (x1, y1)))
        if geometry.length >= 200.0:
            lines.append(geometry)
    lines.sort(key=lambda item: tuple(round(value, 3) for value in item.bounds))

    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        destination.unlink()
    crs_wkt = CRS.from_epsg(target_epsg).to_wkt()
    layers = (
        ("lineament_interpretation_line", "LineString"),
        ("outcrop_interpretation_polygon", "Polygon"),
        ("access_track_line", "LineString"),
        ("disturbance_surface_polygon", "Polygon"),
    )
    for layer_name, geometry_type in layers:
        with fiona.open(
            destination,
            "w",
            driver="GPKG",
            layer=layer_name,
            schema={"geometry": geometry_type, "properties": _INTERPRETATION_PROPERTIES},
            crs_wkt=crs_wkt,
        ) as layer:
            if layer_name != "lineament_interpretation_line":
                continue
            for index, geometry in enumerate(lines, start=1):
                layer.write(
                    {
                        "geometry": mapping(geometry),
                        "properties": {
                            "feature_id": f"KOMPSAT-LIN-{index:05d}",
                            "feature_type": "machine-lineament-candidate",
                            "interpretation_basis": "PAN-sharpened RGB Canny and probabilistic Hough",
                            "source_raw_input_no": "24",
                            "source_raw_filename": source_filename,
                            "processing_phase": "02",
                            "processing_software": "buduunkhad/scikit-image",
                            "processing_action": "deterministic image-edge lineament proposal",
                            "native_crs": f"EPSG:{target_epsg}",
                            "output_crs": f"EPSG:{target_epsg}",
                            "confidence": "Needs verification",
                            "validation_status": "Machine draft — requires geologist review",
                            "limitation": "May include roads, drainage, shadows or image artefacts; support evidence only",
                            "reviewer": "",
                            "reviewed_at": "",
                        },
                    }
                )
    return len(lines)


def _output_identity(
    output_root: Path, product_id: str, path: Path, target_epsg: int
) -> KompsatOutputIdentity:
    if path.suffix.casefold() == ".gpkg":
        import fiona

        return KompsatOutputIdentity(
            product_id=product_id,
            identity=_identity(output_root, path),
            media_type="application/geopackage+sqlite3",
            target_epsg=target_epsg,
            layer_names=tuple(fiona.listlayers(path)),
        )

    import rasterio

    from buduunkhad.core.raster_writers import is_cog

    with rasterio.open(path) as dataset:
        epsg = dataset.crs.to_epsg() if dataset.crs is not None else None
        if epsg != target_epsg:
            raise KompsatProcessingError(f"{path.name} has unexpected output CRS {epsg}")
        return KompsatOutputIdentity(
            product_id=product_id,
            identity=_identity(output_root, path),
            media_type="image/tiff; application=geotiff",
            target_epsg=target_epsg,
            width=dataset.width,
            height=dataset.height,
            resolution_m=abs(float(dataset.res[0])),
            band_count=dataset.count,
            dtype=dataset.dtypes[0],
            cog_valid=is_cog(path),
        )


def process_bundle(
    phase00_root: Path,
    images: Mapping[str, Path],
    dem_path: Path,
    aoi_gdf: Any,
    output_root: Path,
    output_paths: Mapping[str, Path],
    interpretation_path: Path,
    record_path: Path,
    *,
    source_run_id: str,
    processing_run_id: str,
    target_epsg: int = 32647,
    clip_buffer_m: int = 1000,
    pan_resolution_m: float = 1.0,
    multispectral_resolution_m: float = 4.0,
    licence_record_present: bool = False,
) -> KompsatProcessingResult:
    """RPC+DEM orthorectify, derive and QA the exact local KOMPSAT bundle."""

    from buduunkhad.core.raster_writers import write_cog

    if tuple(images) != KOMPSAT_ROLES:
        raise KompsatProcessingError("KOMPSAT image mapping must be PAN/GREEN/BLUE/NIR/RED")
    if tuple(output_paths) != PROCESSING_PRODUCTS:
        raise KompsatProcessingError("KOMPSAT output mapping is incomplete or out of order")
    root = Path(phase00_root).resolve()
    outputs_root = Path(output_root).resolve()
    resolved_images = {
        cast(KompsatRole, role): require_regular_file_under(
            root, path, description="KOMPSAT source raster"
        )
        for role, path in images.items()
    }
    resolved_dem = require_regular_file_under(root, dem_path, description="KOMPSAT RPC DEM")
    inspections = tuple(_inspect_source(root, role, path) for role, path in resolved_images.items())
    pan_inspection = inspections[0]
    multispectral = inspections[1:]
    if pan_inspection.resolution_m != pan_resolution_m:
        raise KompsatProcessingError("KOMPSAT PAN resolution does not match the adopted profile")
    if any(item.resolution_m != multispectral_resolution_m for item in multispectral):
        raise KompsatProcessingError("KOMPSAT multispectral resolution does not match profile")
    ms_grid = {(item.width, item.height, item.source_epsg) for item in multispectral}
    if len(ms_grid) != 1:
        raise KompsatProcessingError("KOMPSAT multispectral bands are not co-registered")
    geometry = _aoi_geometry(aoi_gdf, target_epsg)

    try:
        with TemporaryDirectory() as tmp:
            temporary = Path(tmp)
            pan_plain = temporary / "pan-ortho.tif"
            ms_plain = temporary / "ms-ortho.tif"
            _write_rpc_stack(
                (resolved_images["PAN"],),
                pan_plain,
                dem_path=resolved_dem,
                geometry=geometry,
                target_epsg=target_epsg,
                resolution_m=pan_resolution_m,
            )
            _write_rpc_stack(
                tuple(resolved_images[role] for role in MS_BAND_ORDER),
                ms_plain,
                dem_path=resolved_dem,
                geometry=geometry,
                target_epsg=target_epsg,
                resolution_m=multispectral_resolution_m,
            )
            write_cog(
                pan_plain,
                output_paths["pan_ortho"],
                compress="DEFLATE",
                predictor="2",
                overview_resampling="AVERAGE",
            )
            write_cog(
                ms_plain,
                output_paths["ms_ortho_bundle"],
                compress="DEFLATE",
                predictor="2",
                overview_resampling="AVERAGE",
            )
        Path(output_paths["ms_stack"]).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(output_paths["ms_ortho_bundle"], output_paths["ms_stack"])
        _write_selected_bands(output_paths["ms_stack"], output_paths["true_color"], (3, 2, 1))
        _write_selected_bands(output_paths["ms_stack"], output_paths["false_color"], (4, 3, 2))
        ndvi_min, ndvi_max = _write_ndvi(output_paths["ms_stack"], output_paths["ndvi"])
        _write_pansharpened(
            output_paths["pan_ortho"],
            output_paths["ms_stack"],
            output_paths["pansharpened"],
        )
        lineament_count = _write_interpretation_gpkg(
            output_paths["pansharpened"],
            interpretation_path,
            target_epsg=target_epsg,
            source_filename=resolved_images["PAN"].name,
        )
        output_identities = tuple(
            _output_identity(outputs_root, product_id, Path(output_paths[product_id]), target_epsg)
            for product_id in PROCESSING_PRODUCTS
        ) + (_output_identity(outputs_root, "interpretation", interpretation_path, target_epsg),)
        if any(item.cog_valid is False for item in output_identities):
            raise KompsatProcessingError("one or more KOMPSAT raster outputs are not valid COGs")
        record = KompsatProcessingRecord(
            source_run_id=source_run_id,
            processing_run_id=processing_run_id,
            source_assets=inspections,
            rpc_dem=_identity(root, resolved_dem),
            target_epsg=target_epsg,
            clip_buffer_m=clip_buffer_m,
            pan_resolution_m=pan_resolution_m,
            multispectral_resolution_m=multispectral_resolution_m,
            multispectral_band_order=MS_BAND_ORDER,
            outputs=output_identities,
            ndvi_min=ndvi_min,
            ndvi_max=ndvi_max,
            lineament_feature_count=lineament_count,
            licence_record_present=licence_record_present,
            limitation=(
                "Local deterministic support processing authorized by the repository owner. "
                "The registered EULA file remains absent, so external provider egress and "
                "external publication remain disabled. Machine lineaments require geological "
                "review; outcrop, access-track and disturbance layers remain empty rather than "
                "being fabricated."
            ),
        )
    except KompsatProcessingError:
        raise
    except Exception as exc:
        raise KompsatProcessingError(
            f"KOMPSAT processing failed: {type(exc).__name__}: {exc}"
        ) from exc

    target = Path(record_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(record.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return KompsatProcessingResult(
        raster_outputs=tuple(Path(output_paths[item]) for item in PROCESSING_PRODUCTS),
        interpretation_path=Path(interpretation_path),
        record_path=target,
        record=record,
    )


def load_processing_record(path: Path) -> KompsatProcessingRecord:
    return KompsatProcessingRecord.model_validate_json(Path(path).read_text(encoding="utf-8"))
