"""Deterministic Sentinel-2 L2A SAFE processing for Phase 02 support products."""

from __future__ import annotations

import hashlib
import json
import math
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal
from zipfile import BadZipFile, ZipFile

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from buduunkhad.core import raster_writers
from buduunkhad.core.run_artifacts import has_symlink_component

SPECTRAL_BANDS = ("B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B11", "B12")
REQUIRED_BANDS = (*SPECTRAL_BANDS, "SCL")
PRODUCT_KEYS = (
    "NaturalRGB",
    "Geology_RGB_B12_B08_B03",
    "FalseColor_B08_B04_B03",
    "LithologyIndex_B11B12_B08B11_B04B03",
    "NDVI",
    "NDWI",
    "VegetationMask",
    "WaterMask",
    "CloudShadowMask",
    "UsablePixelMask",
    "IronOxideIndex_B04B02",
    "FerricIndex_B11B08",
    "ClaySWIRIndex_B11B12",
    "FerrousIndex_B12B08",
    "BrightnessIndex",
)

# Sentinel-2 metadata uses zero-based physical-band identifiers rather than band names.
_BAND_METADATA_IDS = {
    "B02": "1",
    "B03": "2",
    "B04": "3",
    "B05": "4",
    "B06": "5",
    "B07": "6",
    "B08": "7",
    "B8A": "8",
    "B11": "11",
    "B12": "12",
}
_PREFERRED_RESOLUTION = {
    "B02": "10m",
    "B03": "10m",
    "B04": "10m",
    "B08": "10m",
    "B05": "20m",
    "B06": "20m",
    "B07": "20m",
    "B8A": "20m",
    "B11": "20m",
    "B12": "20m",
    "SCL": "20m",
}


class SentinelProcessingError(RuntimeError):
    """Raised when an exact SAFE source cannot produce trustworthy Phase 02 products."""


class SentinelOutputIdentity(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    product: str
    path: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    size_bytes: int = Field(ge=1)
    band_count: int = Field(ge=1)
    dtype: str
    finite_pixels: int = Field(ge=0)


class SentinelProcessingRecord(BaseModel):
    """Machine-readable identity and validation record for one exact SAFE archive."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    format_version: Literal["1.0.0"] = "1.0.0"
    source_run_id: str
    processing_run_id: str
    source_path: str
    source_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_size_bytes: int = Field(ge=1)
    metadata_member: str
    band_members: dict[str, str]
    quantification_value: float = Field(gt=0)
    additive_offsets: dict[str, float]
    target_epsg: int = Field(gt=0)
    target_resolution_m: float = Field(gt=0)
    clip_buffer_m: int = Field(ge=0)
    valid_pixel_count: int = Field(ge=0)
    outputs: tuple[SentinelOutputIdentity, ...]
    validation_status: str = "Support evidence only"
    limitation: str = "Not ore proof; requires field/lab validation"

    @field_validator("source_run_id", "processing_run_id", "source_path", "metadata_member")
    @classmethod
    def _non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Sentinel identity fields must be non-empty")
        return value

    @model_validator(mode="after")
    def _complete_source_and_outputs(self) -> SentinelProcessingRecord:
        if set(self.band_members) != set(REQUIRED_BANDS):
            raise ValueError("Sentinel record must bind every required spectral/SCL member")
        if set(self.additive_offsets) != set(SPECTRAL_BANDS):
            raise ValueError("Sentinel record must bind every spectral additive offset")
        if not self.outputs:
            raise ValueError("Sentinel record must bind at least one output")
        if len({item.product for item in self.outputs}) != len(self.outputs):
            raise ValueError("Sentinel output product names must be unique")
        return self


@dataclass(frozen=True)
class SentinelSafeSource:
    archive: Path
    metadata_member: str
    band_members: Mapping[str, str]
    quantification_value: float
    additive_offsets: Mapping[str, float]


@dataclass(frozen=True)
class SentinelProcessingResult:
    record: SentinelProcessingRecord
    record_path: Path
    outputs: tuple[Path, ...]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tag_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _select_member(names: Sequence[str], band: str) -> str:
    resolution = _PREFERRED_RESOLUTION[band]
    candidates = [
        name
        for name in names
        if Path(name).suffix.casefold() in {".jp2", ".tif", ".tiff"}
        and (f"_{band}_{resolution}." in name or f"_{band}." in name)
    ]
    preferred = [name for name in candidates if f"_{band}_{resolution}." in name]
    chosen = preferred or candidates
    if len(chosen) != 1:
        raise SentinelProcessingError(
            f"SAFE archive must contain exactly one preferred {band} {resolution} image; "
            f"found {len(chosen)}"
        )
    return chosen[0]


def inspect_safe_archive(path: Path) -> SentinelSafeSource:
    """Resolve exact L2A band members and radiometric scale/offset metadata."""

    from xml.etree import ElementTree as ET

    archive = Path(path).resolve()
    if not archive.is_file() or archive.suffix.casefold() != ".zip":
        raise SentinelProcessingError(f"Sentinel SAFE archive is missing: {path}")
    try:
        with ZipFile(archive) as bundle:
            names = tuple(bundle.namelist())
            metadata = tuple(name for name in names if name.endswith("/MTD_MSIL2A.xml"))
            if len(metadata) != 1:
                raise SentinelProcessingError(
                    f"SAFE archive must contain one MTD_MSIL2A.xml; found {len(metadata)}"
                )
            root = ET.fromstring(bundle.read(metadata[0]))
            quantification: float | None = None
            offsets_by_id: dict[str, float] = {}
            for element in root.iter():
                tag = _tag_name(element.tag)
                text = (element.text or "").strip()
                if tag == "BOA_QUANTIFICATION_VALUE" and text:
                    quantification = float(text)
                elif tag == "BOA_ADD_OFFSET" and text:
                    band_id = element.attrib.get("band_id")
                    if band_id is not None:
                        offsets_by_id[band_id] = float(text)
            if quantification is None or not math.isfinite(quantification) or quantification <= 0:
                raise SentinelProcessingError("SAFE BOA quantification value is missing or invalid")
            offsets = {
                band: offsets_by_id.get(metadata_id, 0.0)
                for band, metadata_id in _BAND_METADATA_IDS.items()
            }
            members = {band: _select_member(names, band) for band in REQUIRED_BANDS}
            selected = (*metadata, *members.values())
            if any(
                not name or "\\" in name or Path(name).is_absolute() or ".." in Path(name).parts
                for name in selected
            ):
                raise SentinelProcessingError(
                    "SAFE selected members must be canonical archive paths"
                )
    except (BadZipFile, OSError, ValueError, ET.ParseError) as exc:
        if isinstance(exc, SentinelProcessingError):
            raise
        raise SentinelProcessingError(f"Sentinel SAFE inspection failed: {exc}") from exc
    return SentinelSafeSource(
        archive=archive,
        metadata_member=metadata[0],
        band_members=members,
        quantification_value=quantification,
        additive_offsets=offsets,
    )


def discover_safe_archives(phase00_root: Path) -> tuple[Path, ...]:
    """List potential SAFE sources for inventory only; discovery never grants authority."""

    return tuple(sorted(Path(phase00_root).rglob("*.SAFE.zip")))


def resolve_safe_archive(
    phase00_root: Path,
    relative_path: str,
    *,
    expected_sha256: str,
    expected_size_bytes: int,
) -> Path:
    """Resolve the processing-contract-selected source and revalidate its exact bytes."""

    root = Path(phase00_root).absolute()
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts or "\\" in relative_path:
        raise SentinelProcessingError("Sentinel SAFE source path must be canonical and relative")
    candidate = root / relative
    if has_symlink_component(root) or has_symlink_component(candidate):
        raise SentinelProcessingError("Sentinel SAFE source must not use symlinks")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root.resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise SentinelProcessingError("Sentinel SAFE source escapes or is missing") from exc
    if not resolved.is_file():
        raise SentinelProcessingError("Sentinel SAFE source is not a regular file")
    if resolved.stat().st_size != expected_size_bytes:
        raise SentinelProcessingError(
            "Sentinel SAFE source size differs from the processing contract"
        )
    if _sha256(resolved) != expected_sha256:
        raise SentinelProcessingError(
            "Sentinel SAFE source SHA-256 differs from the processing contract"
        )
    return resolved


def _vsi_zip_path(archive: Path, member: str) -> str:
    return f"/vsizip/{archive.as_posix()}/{member}"


def _target_grid(aoi, *, target_epsg: int, resolution_m: float):
    from affine import Affine

    projected = aoi.to_crs(epsg=target_epsg)
    left, bottom, right, top = projected.total_bounds
    left = math.floor(left / resolution_m) * resolution_m
    bottom = math.floor(bottom / resolution_m) * resolution_m
    right = math.ceil(right / resolution_m) * resolution_m
    top = math.ceil(top / resolution_m) * resolution_m
    width = int(round((right - left) / resolution_m))
    height = int(round((top - bottom) / resolution_m))
    if width <= 0 or height <= 0:
        raise SentinelProcessingError("Sentinel target AOI has an empty extent")
    return projected, Affine(resolution_m, 0, left, 0, -resolution_m, top), width, height


def _read_aligned(
    source: SentinelSafeSource,
    aoi,
    *,
    target_epsg: int,
    resolution_m: float,
):
    import numpy as np
    import rasterio
    from rasterio.enums import Resampling
    from rasterio.features import geometry_mask
    from rasterio.warp import reproject
    from shapely.geometry import mapping

    projected, transform, width, height = _target_grid(
        aoi, target_epsg=target_epsg, resolution_m=resolution_m
    )
    shapes = [mapping(geometry) for geometry in projected.geometry if geometry is not None]
    inside = geometry_mask(shapes, out_shape=(height, width), transform=transform, invert=True)
    arrays: dict[str, object] = {}
    for band in REQUIRED_BANDS:
        categorical = band == "SCL"
        destination = np.full(
            (height, width),
            255 if categorical else np.nan,
            dtype="uint8" if categorical else "float32",
        )
        member = _vsi_zip_path(source.archive, source.band_members[band])
        with rasterio.open(member) as dataset:
            reproject(
                source=rasterio.band(dataset, 1),
                destination=destination,
                src_transform=dataset.transform,
                src_crs=dataset.crs,
                src_nodata=0,
                dst_transform=transform,
                dst_crs=f"EPSG:{target_epsg}",
                dst_nodata=255 if categorical else np.nan,
                resampling=Resampling.nearest if categorical else Resampling.bilinear,
                num_threads=2,
            )
        if categorical:
            destination[~inside] = 255
        else:
            raw_valid = np.isfinite(destination) & inside
            destination[raw_valid] = (
                destination[raw_valid] + source.additive_offsets[band]
            ) / source.quantification_value
            destination[~raw_valid] = np.nan
        arrays[band] = destination
    return arrays, transform, inside


def _safe_ratio(numerator, denominator):
    import numpy as np

    out = np.full(numerator.shape, np.nan, dtype="float32")
    valid = np.isfinite(numerator) & np.isfinite(denominator) & (np.abs(denominator) > 1e-6)
    out[valid] = numerator[valid] / denominator[valid]
    return out


def _normalized_difference(first, second):
    return _safe_ratio(first - second, first + second)


def _build_products(arrays: Mapping[str, Any], inside):
    import numpy as np

    b02, b03, b04 = arrays["B02"], arrays["B03"], arrays["B04"]
    b08, b11, b12 = arrays["B08"], arrays["B11"], arrays["B12"]
    scl = arrays["SCL"]
    ndvi = _normalized_difference(b08, b04)
    ndwi = _normalized_difference(b03, b08)
    valid = inside & np.isfinite(ndvi) & np.isfinite(ndwi) & (scl != 0) & (scl != 255)
    cloud_shadow = valid & np.isin(scl, (1, 3, 8, 9, 10, 11))
    vegetation = valid & (ndvi > 0.3)
    water = valid & ((ndwi > 0.2) | (scl == 6))
    usable = valid & ~cloud_shadow & ~vegetation & ~water

    def binary(mask):
        result = np.full(mask.shape, np.nan, dtype="float32")
        result[valid] = mask[valid].astype("float32")
        return result

    products: dict[str, tuple[object, tuple[str, ...], bool]] = {
        "NaturalRGB": (np.stack((b04, b03, b02)), ("Red B04", "Green B03", "Blue B02"), False),
        "Geology_RGB_B12_B08_B03": (
            np.stack((b12, b08, b03)),
            ("SWIR B12", "NIR B08", "Green B03"),
            False,
        ),
        "FalseColor_B08_B04_B03": (
            np.stack((b08, b04, b03)),
            ("NIR B08", "Red B04", "Green B03"),
            False,
        ),
        "LithologyIndex_B11B12_B08B11_B04B03": (
            np.stack((_safe_ratio(b11, b12), _safe_ratio(b08, b11), _safe_ratio(b04, b03))),
            ("B11/B12", "B08/B11", "B04/B03"),
            False,
        ),
        "NDVI": (ndvi, ("NDVI",), False),
        "NDWI": (ndwi, ("NDWI",), False),
        "VegetationMask": (binary(vegetation), ("NDVI > 0.3",), True),
        "WaterMask": (binary(water), ("NDWI > 0.2 or SCL water",), True),
        "CloudShadowMask": (
            binary(cloud_shadow),
            ("SCL cloud/shadow/cirrus/snow",),
            True,
        ),
        "UsablePixelMask": (binary(usable), ("Usable support pixel",), True),
        "IronOxideIndex_B04B02": (_safe_ratio(b04, b02), ("B04/B02",), False),
        "FerricIndex_B11B08": (_safe_ratio(b11, b08), ("B11/B08",), False),
        "ClaySWIRIndex_B11B12": (_safe_ratio(b11, b12), ("B11/B12",), False),
        "FerrousIndex_B12B08": (_safe_ratio(b12, b08), ("B12/B08",), False),
        "BrightnessIndex": ((b02 + b03 + b04) / 3.0, ("Mean B02/B03/B04",), False),
    }
    if tuple(products) != PRODUCT_KEYS:
        raise AssertionError("Sentinel product declaration drifted from PRODUCT_KEYS")
    return products, int(valid.sum())


def _write_product(
    path: Path, array, descriptions: Sequence[str], *, binary: bool, transform, epsg: int
):
    import numpy as np
    import rasterio

    data = array if array.ndim == 3 else array[np.newaxis, ...]
    dtype = "uint8" if binary else "float32"
    nodata = 255 if binary else -9999.0
    if binary:
        valid = np.isfinite(data)
        encoded = np.full(data.shape, nodata, dtype="uint8")
        encoded[valid] = data[valid].astype("uint8")
    else:
        encoded = data.astype(dtype, copy=True)
        encoded[~np.isfinite(encoded)] = nodata
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="sentinel_") as tmp:
        plain = Path(tmp) / "product.tif"
        profile = {
            "driver": "GTiff",
            "height": encoded.shape[1],
            "width": encoded.shape[2],
            "count": encoded.shape[0],
            "dtype": dtype,
            "crs": f"EPSG:{epsg}",
            "transform": transform,
            "nodata": nodata,
            "compress": "DEFLATE",
            "tiled": True,
        }
        with rasterio.open(plain, "w", **profile) as dataset:
            dataset.write(encoded)
            for index, description in enumerate(descriptions, start=1):
                dataset.set_band_description(index, description)
            dataset.update_tags(
                validation_status="Support evidence only",
                limitation="Not ore proof; requires field/lab validation",
            )
        raster_writers.write_cog(
            plain,
            path,
            compress="DEFLATE",
            predictor=raster_writers.predictor_for(dtype),
            overview_resampling="NEAREST" if binary else "AVERAGE",
        )


def process_safe_archive(
    source_path: Path,
    aoi,
    output_paths: Mapping[str, Path],
    record_path: Path,
    *,
    source_run_id: str,
    processing_run_id: str,
    target_epsg: int,
    target_resolution_m: float = 10.0,
    clip_buffer_m: int = 1000,
) -> SentinelProcessingResult:
    """Generate the complete deterministic Sentinel support-product set from one SAFE ZIP."""

    import numpy as np
    import rasterio

    source = inspect_safe_archive(source_path)
    arrays, transform, inside = _read_aligned(
        source, aoi, target_epsg=target_epsg, resolution_m=target_resolution_m
    )
    products, valid_pixels = _build_products(arrays, inside)
    if set(output_paths) != set(products):
        missing = sorted(set(products) - set(output_paths))
        extra = sorted(set(output_paths) - set(products))
        raise SentinelProcessingError(
            f"Sentinel output path contract mismatch; missing={missing}, extra={extra}"
        )
    resolved_outputs = [Path(path).absolute() for path in output_paths.values()]
    if len(set(resolved_outputs)) != len(resolved_outputs):
        raise SentinelProcessingError("Sentinel output paths must be unique")
    written: list[Path] = []
    identities: list[SentinelOutputIdentity] = []
    for product, (array, descriptions, binary) in products.items():
        path = Path(output_paths[product])
        _write_product(
            path,
            array,
            descriptions,
            binary=binary,
            transform=transform,
            epsg=target_epsg,
        )
        written.append(path)
        with rasterio.open(path) as dataset:
            finite_pixels = int(
                np.count_nonzero(dataset.read(1) != dataset.nodata)
                if dataset.nodata is not None
                else dataset.width * dataset.height
            )
            identities.append(
                SentinelOutputIdentity(
                    product=product,
                    path=path.name,
                    sha256=_sha256(path),
                    size_bytes=path.stat().st_size,
                    band_count=dataset.count,
                    dtype=dataset.dtypes[0],
                    finite_pixels=finite_pixels,
                )
            )
    record = SentinelProcessingRecord(
        source_run_id=source_run_id,
        processing_run_id=processing_run_id,
        source_path=Path(source_path).name,
        source_sha256=_sha256(Path(source_path)),
        source_size_bytes=Path(source_path).stat().st_size,
        metadata_member=source.metadata_member,
        band_members=dict(source.band_members),
        quantification_value=source.quantification_value,
        additive_offsets=dict(source.additive_offsets),
        target_epsg=target_epsg,
        target_resolution_m=target_resolution_m,
        clip_buffer_m=clip_buffer_m,
        valid_pixel_count=valid_pixels,
        outputs=tuple(identities),
    )
    target = Path(record_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(record.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return SentinelProcessingResult(record=record, record_path=target, outputs=tuple(written))


def load_processing_record(path: Path) -> SentinelProcessingRecord:
    return SentinelProcessingRecord.model_validate_json(Path(path).read_text(encoding="utf-8"))
