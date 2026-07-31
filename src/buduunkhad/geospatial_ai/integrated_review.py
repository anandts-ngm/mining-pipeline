"""One portable QGIS view over sealed pipeline results and Phase 03 AI review layers."""

from __future__ import annotations

import math
import os
from pathlib import Path

import fiona
import rasterio
from pyproj import CRS, Transformer

from buduunkhad.core.qgis_project import (
    QgzExtent,
    QgzLayer,
    line_symbol,
    point_symbol,
    polygon_outline,
    write_layered_qgz,
)
from buduunkhad.core.run_storage import ResolvedSourcePhase, resolve_source_phase
from buduunkhad.geospatial_ai.path_safety import StorageRoots
from buduunkhad.geospatial_ai.phase03_handoff import (
    REVIEW_GPKG_NAME,
    ReviewPackageManifest,
    verify_review_package,
)
from buduunkhad.geospatial_ai.schemas import DraftLayerName

_TARGET_EPSG = 32647
_RASTER_SUFFIXES = frozenset({".tif", ".tiff"})
_VECTOR_SUFFIXES = frozenset({".gpkg"})

_DRAFT_GEOMETRY: dict[DraftLayerName, str] = {
    DraftLayerName.GEOLOGY_UNITS: "Polygon",
    DraftLayerName.FAULTS_STRUCTURES: "LineString",
    DraftLayerName.INTRUSIVE_CONTACTS: "LineString",
    DraftLayerName.DYKES_VEINS: "LineString",
    DraftLayerName.MINERAL_OCCURRENCES: "Point",
    DraftLayerName.ALTERATION_ZONES: "Polygon",
    DraftLayerName.PROSPECT_PROPOSALS: "Polygon",
}


def build_integrated_phase03_review_project(
    *,
    runs_root: Path,
    pipeline_run_id: str,
    ai_run_id: str,
    review_packages: tuple[Path, ...],
    output: Path,
    roots: StorageRoots,
    target_epsg: int,
) -> Path:
    """Create one QGIS workspace without weakening either run's provenance boundary."""

    if target_epsg != _TARGET_EPSG:
        raise ValueError("integrated Phase 03 review requires EPSG:32647")
    if not review_packages:
        raise ValueError("at least one Phase 03 AI review package is required")
    project = roots.assert_writable(output, run_id=ai_run_id)
    if project.suffix.casefold() != ".qgz":
        raise ValueError("integrated Phase 03 review output must be a .qgz file")

    phases = tuple(
        resolve_source_phase(
            runs_root,
            phase_id,
            pipeline_run_id,
            require_advance=False,
            require_qaqc_passed=True,
        )
        for phase_id in ("01", "02", "03")
    )
    packages = tuple(
        _verified_review_package(path, roots=roots, ai_run_id=ai_run_id) for path in review_packages
    )

    layers: list[QgzLayer] = []
    extent_candidates: list[tuple[float, float, float, float]] = []
    for phase in phases:
        phase_layers, phase_extents = _pipeline_phase_layers(
            phase,
            project=project,
            target_epsg=target_epsg,
        )
        layers.extend(phase_layers)
        if phase.binding.phase_id == "01":
            extent_candidates.extend(phase_extents)
    for package_path, manifest in zip(review_packages, packages, strict=True):
        layers.extend(
            _review_package_layers(
                package_path.resolve(),
                manifest=manifest,
                project=project,
            )
        )

    extent = _combined_extent(extent_candidates)
    return write_layered_qgz(
        project,
        epsg=target_epsg,
        title=f"Buduunkhad {pipeline_run_id} Phase 03 Integrated Review",
        layers=layers,
        initial_extent=extent,
    )


def _verified_review_package(
    path: Path,
    *,
    roots: StorageRoots,
    ai_run_id: str,
) -> ReviewPackageManifest:
    manifest = verify_review_package(path, roots=roots)
    if manifest.run_id != ai_run_id:
        raise ValueError(f"review package belongs to AI run {manifest.run_id}, not {ai_run_id}")
    return manifest


def _pipeline_phase_layers(
    phase: ResolvedSourcePhase,
    *,
    project: Path,
    target_epsg: int,
) -> tuple[list[QgzLayer], list[tuple[float, float, float, float]]]:
    phase_id = phase.binding.phase_id
    group = f"Phase {phase_id} Sealed Outputs"
    layers: list[QgzLayer] = []
    extents: list[tuple[float, float, float, float]] = []
    run_directory = phase.phase_dir.parents[1]
    for artifact in phase.output_artifacts:
        path = run_directory / artifact.path
        suffix = path.suffix.casefold()
        if suffix in _RASTER_SUFFIXES:
            epsg, bounds = _raster_metadata(path, target_epsg=target_epsg)
            layers.append(
                QgzLayer(
                    name=f"P{phase_id} {path.stem}",
                    source=_relative(project.parent, path),
                    geometry="Raster",
                    visible=False,
                    group=group,
                    provider="gdal",
                    epsg=epsg,
                    read_only=True,
                )
            )
            extents.append(bounds)
        elif suffix in _VECTOR_SUFFIXES:
            vector_layers, vector_extents = _vector_layers(
                path,
                display_prefix=f"P{phase_id}",
                group=group,
                project=project,
                target_epsg=target_epsg,
            )
            layers.extend(vector_layers)
            extents.extend(vector_extents)
    return layers, extents


def _vector_layers(
    path: Path,
    *,
    display_prefix: str,
    group: str,
    project: Path,
    target_epsg: int,
) -> tuple[list[QgzLayer], list[tuple[float, float, float, float]]]:
    layers: list[QgzLayer] = []
    extents: list[tuple[float, float, float, float]] = []
    relative = _relative(project.parent, path)
    for layer_name in fiona.listlayers(path):
        with fiona.open(path, layer=layer_name) as collection:
            geometry = _qgis_geometry(collection.schema.get("geometry"))
            epsg = target_epsg if geometry == "None" else _collection_epsg(collection)
            bounds = (
                _target_bounds(collection.bounds, epsg=epsg, target_epsg=target_epsg)
                if geometry != "None" and len(collection) > 0
                else None
            )
        layers.append(
            QgzLayer(
                name=f"{display_prefix} {layer_name}",
                source=f"{relative}|layername={layer_name}",
                geometry=geometry,
                symbol=_default_style(geometry),
                visible=_default_pipeline_visibility(layer_name),
                group=group,
                provider="ogr",
                epsg=epsg,
                read_only=True,
            )
        )
        if bounds is not None:
            extents.append(bounds)
    return layers, extents


def _review_package_layers(
    package_path: Path,
    *,
    manifest: ReviewPackageManifest,
    project: Path,
) -> list[QgzLayer]:
    package_label = manifest.source_asset_id[:12]
    layers: list[QgzLayer] = []
    for index, (relative, _digest) in enumerate(manifest.source_preview_files):
        preview = package_path / relative
        if preview.suffix.casefold() != ".png":
            continue
        epsg = _preview_epsg(preview)
        layers.append(
            QgzLayer(
                name=f"AI Source {package_label} {index + 1}",
                source=_relative(project.parent, preview),
                geometry="Raster",
                visible=index == 0,
                group=f"AI Source {package_label}",
                provider="gdal",
                epsg=epsg,
                read_only=True,
            )
        )

    review_gpkg = package_path / REVIEW_GPKG_NAME
    relative_gpkg = _relative(project.parent, review_gpkg)
    review_group = f"AI Review {package_label}"
    for layer in DraftLayerName:
        geometry = _DRAFT_GEOMETRY[layer]
        layers.extend(
            (
                QgzLayer(
                    name=f"AI Pending {package_label} {layer.value}",
                    source=f"{relative_gpkg}|layername=review_{layer.value}",
                    geometry=geometry,
                    symbol=_review_style(geometry, "pending"),
                    visible=True,
                    group=review_group,
                    provider="ogr",
                    subset_string="\"review_decision\" = 'pending'",
                ),
                QgzLayer(
                    name=f"AI Original {package_label} {layer.value}",
                    source=f"{relative_gpkg}|layername=original_{layer.value}",
                    geometry=geometry,
                    symbol=_review_style(geometry, "original"),
                    visible=False,
                    group=review_group,
                    provider="ogr",
                    read_only=True,
                ),
                QgzLayer(
                    name=f"AI Accepted {package_label} {layer.value}",
                    source=f"{relative_gpkg}|layername=review_{layer.value}",
                    geometry=geometry,
                    symbol=_review_style(geometry, "accepted"),
                    visible=False,
                    group=review_group,
                    provider="ogr",
                    subset_string="\"review_decision\" IN ('accepted','accepted_with_edits')",
                ),
                QgzLayer(
                    name=f"AI Rejected {package_label} {layer.value}",
                    source=f"{relative_gpkg}|layername=review_{layer.value}",
                    geometry=geometry,
                    symbol=_review_style(geometry, "rejected"),
                    visible=False,
                    group=review_group,
                    provider="ogr",
                    subset_string="\"review_decision\" = 'rejected'",
                ),
            )
        )
    layers.append(
        QgzLayer(
            name=f"AI Validation {package_label}",
            source=f"{relative_gpkg}|layername=validation_findings",
            geometry="Point",
            symbol=point_symbol("255,0,255,255", 2.5),
            visible=True,
            group=review_group,
            provider="ogr",
            read_only=True,
        )
    )
    return layers


def _preview_epsg(path: Path) -> int:
    projection = path.with_suffix(".prj")
    if not projection.is_file():
        raise ValueError(f"review preview has no projection sidecar: {path}")
    try:
        epsg = CRS.from_wkt(projection.read_text(encoding="utf-8")).to_epsg()
    except (OSError, UnicodeError, ValueError) as exc:
        raise ValueError(f"review preview projection is invalid: {projection}") from exc
    if epsg is None:
        raise ValueError(f"review preview projection has no EPSG identity: {projection}")
    return epsg


def _raster_metadata(
    path: Path,
    *,
    target_epsg: int,
) -> tuple[int, tuple[float, float, float, float]]:
    with rasterio.open(path) as dataset:
        if dataset.crs is None:
            raise ValueError(f"review raster has no CRS: {path}")
        epsg = dataset.crs.to_epsg()
        if epsg is None:
            raise ValueError(f"review raster CRS has no EPSG identity: {path}")
        bounds = _target_bounds(dataset.bounds, epsg=epsg, target_epsg=target_epsg)
    if bounds is None:
        raise ValueError(f"review raster has an empty or invalid extent: {path}")
    return epsg, bounds


def _collection_epsg(collection: fiona.Collection) -> int:
    if not collection.crs:
        raise ValueError(f"review vector layer has no CRS: {collection.name}")
    epsg = CRS.from_user_input(collection.crs).to_epsg()
    if epsg is None:
        raise ValueError(f"review vector layer CRS has no EPSG identity: {collection.name}")
    return epsg


def _target_bounds(
    bounds: tuple[float, float, float, float],
    *,
    epsg: int,
    target_epsg: int,
) -> tuple[float, float, float, float] | None:
    xmin, ymin, xmax, ymax = (float(value) for value in bounds)
    if (
        not all(math.isfinite(value) for value in (xmin, ymin, xmax, ymax))
        or xmax <= xmin
        or ymax <= ymin
    ):
        return None
    if epsg == target_epsg:
        return xmin, ymin, xmax, ymax
    transformed = Transformer.from_crs(
        f"EPSG:{epsg}",
        f"EPSG:{target_epsg}",
        always_xy=True,
    ).transform_bounds(xmin, ymin, xmax, ymax)
    if not all(math.isfinite(value) for value in transformed):
        return None
    return transformed


def _combined_extent(
    bounds: list[tuple[float, float, float, float]],
) -> QgzExtent:
    if not bounds:
        raise ValueError("sealed Phase 01 outputs do not provide a usable project extent")
    return QgzExtent(
        xmin=min(item[0] for item in bounds),
        ymin=min(item[1] for item in bounds),
        xmax=max(item[2] for item in bounds),
        ymax=max(item[3] for item in bounds),
    )


def _qgis_geometry(value: str | None) -> str:
    geometry = (value or "").replace("3D ", "")
    if "Point" in geometry:
        return "Point"
    if "LineString" in geometry:
        return "LineString"
    if "Polygon" in geometry:
        return "Polygon"
    if geometry in {"None", "Unknown"}:
        return "None"
    raise ValueError(f"unsupported review vector geometry: {value}")


def _default_pipeline_visibility(layer_name: str) -> bool:
    normalized = layer_name.casefold()
    return normalized in {
        "license_boundary",
        "project_buffers",
        "mineral_occurrences_point",
    }


def _default_style(geometry: str):
    if geometry == "Point":
        return point_symbol("255,215,0,255", 2.5)
    if geometry == "LineString":
        return line_symbol("90,90,90,255", 0.45)
    if geometry == "Polygon":
        return polygon_outline("70,110,160,255", 0.45)
    return None


def _review_style(geometry: str, state: str):
    if state == "accepted":
        color, dash = "0,150,70,255", False
    elif state == "rejected":
        color, dash = "160,160,160,255", True
    elif state == "original":
        color, dash = "40,90,210,255", True
    else:
        color, dash = "230,0,180,255", True
    if geometry == "Point":
        return point_symbol(color, 3.0)
    if geometry == "LineString":
        return line_symbol(color, 0.7, dash=dash)
    return polygon_outline(color, 0.7, dash=dash)


def _relative(base: Path, target: Path) -> str:
    return os.path.relpath(target.resolve(), base.resolve()).replace("\\", "/")
