"""Post-flight Phase 05 intake, raster QA and bounded terrain processing.

The acquired campaign is much larger than an ordinary phase workspace.  This module therefore
reads source files in place, records their metadata, and writes only curated derivatives.  It
never copies the raw photo/LiDAR tree into a run directory.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import struct
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from shapely.geometry import box

from buduunkhad.core import dem, raster_writers

_BLOCK = re.compile(r"^B(\d+)(?:_|$)", re.IGNORECASE)
_BLOCK_IN_FILE = re.compile(r"(?:^|[_-])B(\d+)(?:[_-]|\.|$)", re.IGNORECASE)
_IGNORED_NAMES = {"desktop.ini", "thumbs.db"}


class Phase05DataError(RuntimeError):
    """The configured acquired campaign cannot produce a truthful Phase 05 result."""


@dataclass(frozen=True)
class Phase05Layout:
    root: Path
    processed: Path
    original_exports: Path
    colour_orthos: Path | None
    final_dem_directory: Path
    control: Path | None
    daily_reports: Path | None


@dataclass(frozen=True)
class RasterMetadata:
    path: Path
    relative_path: str
    size_bytes: int
    epsg: int | None
    width: int
    height: int
    band_count: int
    dtype: str
    nodata: float | int | None
    x_resolution: float
    y_resolution: float
    bounds: tuple[float, float, float, float]
    open_status: Literal["pass", "fail"]
    error: str = ""

    @property
    def geometry(self):
        return box(*self.bounds) if self.open_status == "pass" else None


@dataclass(frozen=True)
class LasMetadata:
    path: Path
    relative_path: str
    size_bytes: int
    version: str | None
    point_format: int | None
    point_count: int | None
    bounds: tuple[float, float, float, float, float, float] | None
    crs_authority: str | None
    open_status: Literal["pass", "fail"]
    error: str = ""


@dataclass(frozen=True)
class DroneBlock:
    block_number: int
    block_id: str
    sensor: Literal["L2", "L3", "unknown"]
    source_directory: Path
    dem: RasterMetadata | None
    dsm: RasterMetadata | None
    dom: RasterMetadata | None
    colour_ortho: RasterMetadata | None
    point_cloud: LasMetadata | None
    quality_report: Path | None

    @property
    def preferred_ortho(self) -> RasterMetadata | None:
        return self.colour_ortho or self.dom

    @property
    def complete_core_products(self) -> bool:
        return all(value is not None for value in (self.dem, self.dsm, self.dom))


@dataclass(frozen=True)
class DroneSurvey:
    layout: Phase05Layout
    blocks: tuple[DroneBlock, ...]
    final_dem: RasterMetadata
    control_files: tuple[Path, ...]
    daily_report_files: tuple[Path, ...]


def resolve_layout(root: Path) -> Phase05Layout:
    """Resolve the existing numbered campaign tree without depending on exact spacing."""

    root = Path(root).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise Phase05DataError(f"Phase 05 source root is not a directory: {root}")
    processed = _numbered_child(root, 2) or root
    original = _prefix_child(processed, "01_")
    final_dem = _prefix_child(processed, "03_")
    if original is None or final_dem is None:
        raise Phase05DataError(
            "Phase 05 processed data must contain 01_* original exports and 03_* final DEM"
        )
    return Phase05Layout(
        root=root,
        processed=processed,
        original_exports=original,
        colour_orthos=_prefix_child(processed, "02_"),
        final_dem_directory=final_dem,
        control=_numbered_child(root, 4),
        daily_reports=_numbered_child(root, 5),
    )


def source_tree_identity(root: Path) -> str:
    """Hash the campaign's path/size/mtime inventory without streaming hundreds of GB."""

    layout = resolve_layout(root)
    roots = [layout.processed, layout.control, layout.daily_reports]
    records: list[dict[str, object]] = []
    for selected in roots:
        if selected is None:
            continue
        for path in sorted(selected.rglob("*"), key=lambda item: item.as_posix().casefold()):
            if not path.is_file() or path.name.casefold() in _IGNORED_NAMES:
                continue
            stat = path.stat()
            records.append(
                {
                    "path": path.relative_to(layout.root).as_posix(),
                    "size_bytes": stat.st_size,
                    "mtime_ns": stat.st_mtime_ns,
                }
            )
    payload = json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_source_separation(root: Path, *writable_roots: Path) -> None:
    """Ensure the read-only campaign cannot be nested inside a pipeline write root."""

    source = Path(root).expanduser().resolve(strict=True)
    for value in writable_roots:
        writable = Path(value).expanduser().resolve(strict=False)
        if source == writable or source in writable.parents or writable in source.parents:
            raise Phase05DataError(
                f"Phase 05 source and writable root must not overlap: {source} ; {writable}"
            )


def inspect_survey(root: Path, *, target_epsg: int) -> DroneSurvey:
    """Inspect all B-numbered processed blocks and the final DEM using header-only reads."""

    layout = resolve_layout(root)
    colour = _colour_ortho_index(layout.colour_orthos)
    block_dirs: dict[int, Path] = {}
    for path in layout.original_exports.iterdir():
        match = _BLOCK.match(path.name) if path.is_dir() else None
        if match is not None:
            number = int(match.group(1))
            if number in block_dirs:
                raise Phase05DataError(f"duplicate processed block B{number}: {path}")
            block_dirs[number] = path
    if not block_dirs:
        raise Phase05DataError("Phase 05 processed export contains no B-numbered blocks")

    blocks: list[DroneBlock] = []
    for number, directory in sorted(block_dirs.items()):
        files = tuple(
            item
            for item in directory.rglob("*")
            if item.is_file() and item.name.casefold() not in _IGNORED_NAMES
        )
        report = _one_optional(
            files, lambda path: path.suffix.casefold() == ".pdf", "report", number
        )
        sensor = _sensor_from_report(report)
        dem_path = _one_optional(
            files, lambda path: path.name.casefold() == "dem.tif", "DEM", number
        )
        dsm_path = _one_optional(
            files, lambda path: path.name.casefold() == "dsm.tif", "DSM", number
        )
        dom_path = _one_optional(
            files, lambda path: path.name.casefold() == "dom.tif", "DOM", number
        )
        las_path = _one_optional(
            files,
            lambda path: path.suffix.casefold() in {".las", ".laz"},
            "point cloud",
            number,
        )
        blocks.append(
            DroneBlock(
                block_number=number,
                block_id=f"B{number}",
                sensor=sensor,
                source_directory=directory,
                dem=inspect_raster(dem_path, layout.root) if dem_path else None,
                dsm=inspect_raster(dsm_path, layout.root) if dsm_path else None,
                dom=inspect_raster(dom_path, layout.root) if dom_path else None,
                colour_ortho=(
                    inspect_raster(colour[number], layout.root) if number in colour else None
                ),
                point_cloud=inspect_las(las_path, layout.root) if las_path else None,
                quality_report=report,
            )
        )

    final_candidates = sorted(layout.final_dem_directory.rglob("*.tif"))
    if len(final_candidates) != 1:
        raise Phase05DataError(
            "Phase 05 final DEM directory must contain exactly one GeoTIFF "
            f"(found {len(final_candidates)})"
        )
    final_dem = inspect_raster(final_candidates[0], layout.root)
    if final_dem.open_status != "pass" or final_dem.epsg != target_epsg:
        raise Phase05DataError(
            f"Phase 05 final DEM must open in EPSG:{target_epsg}: {final_dem.error or final_dem.epsg}"
        )
    return DroneSurvey(
        layout=layout,
        blocks=tuple(blocks),
        final_dem=final_dem,
        control_files=_files_below(layout.control),
        daily_report_files=_files_below(layout.daily_reports),
    )


def inspect_raster(path: Path, root: Path) -> RasterMetadata:
    import rasterio

    path = Path(path)
    relative = path.relative_to(root).as_posix()
    size = path.stat().st_size
    try:
        with rasterio.open(path) as dataset:
            bounds = dataset.bounds
            nodata = dataset.nodata
            return RasterMetadata(
                path=path,
                relative_path=relative,
                size_bytes=size,
                epsg=dataset.crs.to_epsg() if dataset.crs is not None else None,
                width=dataset.width,
                height=dataset.height,
                band_count=dataset.count,
                dtype=dataset.dtypes[0],
                nodata=nodata if nodata is None or math.isfinite(float(nodata)) else None,
                x_resolution=abs(float(dataset.res[0])),
                y_resolution=abs(float(dataset.res[1])),
                bounds=(
                    float(bounds.left),
                    float(bounds.bottom),
                    float(bounds.right),
                    float(bounds.top),
                ),
                open_status="pass",
            )
    except Exception as exc:  # noqa: BLE001 - the failure is retained in the survey register
        return RasterMetadata(
            path=path,
            relative_path=relative,
            size_bytes=size,
            epsg=None,
            width=0,
            height=0,
            band_count=0,
            dtype="",
            nodata=None,
            x_resolution=0,
            y_resolution=0,
            bounds=(0, 0, 0, 0),
            open_status="fail",
            error=f"{type(exc).__name__}: {exc}",
        )


def inspect_las(path: Path, root: Path) -> LasMetadata:
    """Read standard LAS header fields and an optional WKT VLR without loading points."""

    path = Path(path)
    relative = path.relative_to(root).as_posix()
    size = path.stat().st_size
    try:
        with path.open("rb") as stream:
            header = stream.read(375)
            if len(header) < 227 or header[:4] != b"LASF":
                raise ValueError("not a LAS file or header is truncated")
            version = f"{header[24]}.{header[25]}"
            header_size = struct.unpack_from("<H", header, 94)[0]
            point_offset = struct.unpack_from("<I", header, 96)[0]
            vlr_count = struct.unpack_from("<I", header, 100)[0]
            point_format = header[104] & 0x3F
            legacy_count = struct.unpack_from("<I", header, 107)[0]
            point_count = legacy_count
            if version == "1.4" and len(header) >= 255:
                extended = struct.unpack_from("<Q", header, 247)[0]
                point_count = extended or legacy_count
            max_x, min_x, max_y, min_y, max_z, min_z = struct.unpack_from("<6d", header, 179)
            crs_authority: str | None = None
            if point_offset <= 16 * 1024 * 1024 and header_size <= point_offset:
                stream.seek(header_size)
                for _ in range(vlr_count):
                    vlr = stream.read(54)
                    if len(vlr) != 54:
                        break
                    record_id = struct.unpack_from("<H", vlr, 18)[0]
                    payload_size = struct.unpack_from("<H", vlr, 20)[0]
                    payload = stream.read(payload_size)
                    if record_id == 2112:
                        from pyproj import CRS

                        text = payload.rstrip(b"\x00").decode("utf-8", errors="strict")
                        authority = CRS.from_wkt(text).to_authority()
                        if authority is not None:
                            crs_authority = f"{authority[0]}:{authority[1]}"
            return LasMetadata(
                path=path,
                relative_path=relative,
                size_bytes=size,
                version=version,
                point_format=point_format,
                point_count=point_count,
                bounds=(min_x, min_y, min_z, max_x, max_y, max_z),
                crs_authority=crs_authority,
                open_status="pass",
            )
    except Exception as exc:  # noqa: BLE001 - the failure is retained in the survey register
        return LasMetadata(
            path=path,
            relative_path=relative,
            size_bytes=size,
            version=None,
            point_format=None,
            point_count=None,
            bounds=None,
            crs_authority=None,
            open_status="fail",
            error=f"{type(exc).__name__}: {exc}",
        )


def block_rows(survey: DroneSurvey, *, target_epsg: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for block in survey.blocks:
        raster_values = (block.dem, block.dsm, block.dom, block.colour_ortho)
        raster_failures = tuple(
            value.relative_path
            for value in raster_values
            if value is not None and value.open_status == "fail"
        )
        wrong_crs = tuple(
            value.relative_path
            for value in raster_values
            if value is not None and value.open_status == "pass" and value.epsg != target_epsg
        )
        gaps = []
        if not block.complete_core_products:
            gaps.append("missing DEM/DSM/DOM")
        if block.point_cloud is None:
            gaps.append("missing point cloud")
        elif block.point_cloud.open_status == "fail":
            gaps.append("invalid point cloud header")
        if block.quality_report is None:
            gaps.append("missing quality report")
        if raster_failures:
            gaps.append("raster open failure")
        if wrong_crs:
            gaps.append("raster CRS mismatch")
        preferred = block.preferred_ortho
        rows.append(
            {
                "block_id": block.block_id,
                "block_number": block.block_number,
                "sensor": block.sensor,
                "dem_path": block.dem.relative_path if block.dem else "",
                "dsm_path": block.dsm.relative_path if block.dsm else "",
                "dom_path": block.dom.relative_path if block.dom else "",
                "preferred_ortho_path": preferred.relative_path if preferred else "",
                "colour_corrected_ortho": block.colour_ortho is not None,
                "point_cloud_path": block.point_cloud.relative_path if block.point_cloud else "",
                "point_count": block.point_cloud.point_count if block.point_cloud else "",
                "point_cloud_crs": block.point_cloud.crs_authority if block.point_cloud else "",
                "quality_report_path": (
                    block.quality_report.relative_to(survey.layout.root).as_posix()
                    if block.quality_report
                    else ""
                ),
                "core_products_complete": block.complete_core_products,
                "raster_failures": "; ".join(raster_failures),
                "crs_mismatches": "; ".join(wrong_crs),
                "data_gaps": "; ".join(gaps),
                "status": "pass" if not gaps else "data-gap",
            }
        )
    return rows


def coverage_geodataframe(survey: DroneSurvey, *, target_epsg: int):
    import geopandas as gpd

    rows: list[dict[str, Any]] = []
    for block in survey.blocks:
        footprint = block.preferred_ortho or block.dom or block.dsm or block.dem
        if footprint is None or footprint.open_status != "pass" or footprint.epsg != target_epsg:
            continue
        rows.append(
            {
                "block_id": block.block_id,
                "sensor": block.sensor,
                "ortho_src": "colour-corrected" if block.colour_ortho else "DJI Terra DOM",
                "point_cloud": block.point_cloud is not None,
                "data_gap": "" if block.point_cloud is not None else "missing point cloud",
                "geometry": footprint.geometry,
            }
        )
    return gpd.GeoDataFrame(  # ty: ignore[no-matching-overload]
        rows, geometry="geometry", crs=f"EPSG:{target_epsg}"
    )


def write_terrain_products(
    source_dem: Path,
    *,
    dtm_output: Path,
    hillshade_output: Path,
    slope_output: Path,
) -> tuple[Path, Path, Path]:
    """Create a COG DTM plus bounded-memory hillshade and slope COGs."""

    import numpy as np
    import rasterio
    from rasterio.windows import Window

    source_dem = Path(source_dem)
    raster_writers.write_cog(
        source_dem,
        dtm_output,
        compress="DEFLATE",
        predictor="3",
        overview_resampling="AVERAGE",
    )
    with (
        rasterio.open(source_dem) as source,
        tempfile.TemporaryDirectory(prefix="p05-terrain-") as temp,
    ):
        profile = source.profile.copy()
        profile.update(driver="GTiff", count=1, tiled=True, blockxsize=512, blockysize=512)
        plain_hillshade = Path(temp) / "hillshade.tif"
        plain_slope = Path(temp) / "slope.tif"
        hillshade_profile = dict(profile, dtype="uint8", nodata=0, compress="DEFLATE")
        slope_profile = dict(
            profile, dtype="float32", nodata=-9999.0, compress="DEFLATE", predictor=3
        )
        with (
            rasterio.open(plain_hillshade, "w", **hillshade_profile) as hillshade_target,
            rasterio.open(plain_slope, "w", **slope_profile) as slope_target,
        ):
            for _index, window in source.block_windows(1):
                padded = Window(
                    window.col_off - 1,  # ty: ignore[too-many-positional-arguments]
                    window.row_off - 1,
                    window.width + 2,
                    window.height + 2,
                )
                elevation = source.read(1, window=padded, boundless=True, masked=True)
                invalid = np.ma.getmaskarray(elevation)
                values = elevation.astype("float64").filled(np.nan)
                mean = np.nanmean(values)
                values = np.where(np.isnan(values), mean if np.isfinite(mean) else 0.0, values)
                hs = dem.hillshade(values, source.res[0], source.res[1])[1:-1, 1:-1]
                sl = dem.slope_degrees(values, source.res[0], source.res[1])[1:-1, 1:-1]
                invalid_inner = invalid[1:-1, 1:-1]
                hillshade_target.write(
                    np.where(invalid_inner, 0, hs).astype("uint8"), 1, window=window
                )
                slope_target.write(
                    np.where(invalid_inner, -9999.0, sl).astype("float32"), 1, window=window
                )
        raster_writers.write_cog(
            plain_hillshade,
            hillshade_output,
            compress="DEFLATE",
            overview_resampling="AVERAGE",
        )
        raster_writers.write_cog(
            plain_slope,
            slope_output,
            compress="DEFLATE",
            predictor="3",
            overview_resampling="AVERAGE",
        )
    return dtm_output, hillshade_output, slope_output


def _numbered_child(root: Path, number: int) -> Path | None:
    prefix = f"{number}."
    matches = sorted(
        path for path in root.iterdir() if path.is_dir() and path.name.casefold().startswith(prefix)
    )
    if len(matches) > 1:
        raise Phase05DataError(f"multiple Phase 05 directories start with {prefix!r}")
    return matches[0] if matches else None


def _prefix_child(root: Path, prefix: str) -> Path | None:
    matches = sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and path.name.casefold().startswith(prefix.casefold())
    )
    if len(matches) > 1:
        raise Phase05DataError(f"multiple Phase 05 directories start with {prefix!r}")
    return matches[0] if matches else None


def _colour_ortho_index(root: Path | None) -> dict[int, Path]:
    if root is None:
        return {}
    result: dict[int, Path] = {}
    for path in sorted(root.rglob("*.tif")):
        match = _BLOCK_IN_FILE.search(path.name)
        if match is None:
            continue
        number = int(match.group(1))
        if number in result:
            raise Phase05DataError(f"multiple colour-corrected orthos claim B{number}")
        result[number] = path
    return result


def _one_optional(
    files: tuple[Path, ...],
    predicate,
    label: str,
    block_number: int,
) -> Path | None:
    matches = tuple(path for path in files if predicate(path))
    if len(matches) > 1:
        raise Phase05DataError(f"block B{block_number} has multiple {label} files")
    return matches[0] if matches else None


def _sensor_from_report(report: Path | None) -> Literal["L2", "L3", "unknown"]:
    if report is None:
        return "unknown"
    name = report.name.casefold()
    if "l3" in name:
        return "L3"
    if "l2" in name:
        return "L2"
    return "unknown"


def _files_below(root: Path | None) -> tuple[Path, ...]:
    if root is None:
        return ()
    return tuple(
        path
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name.casefold() not in _IGNORED_NAMES
    )
