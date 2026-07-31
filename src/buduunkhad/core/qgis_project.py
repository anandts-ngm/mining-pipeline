"""Deterministic layered QGIS project (.qgz) generation — no PyQGIS required.

A .qgz is a zip archive holding a .qgs project XML. QGIS re-reads every layer from
its datasource on open, so a project file only needs: the project CRS, one
``<maplayer>`` entry per layer (OGR datasource + layer name), a matching
``<layer-tree-layer>`` in the layer tree (top-to-bottom render order), and an
optional embedded renderer for deterministic symbology. Datasource paths are
written *relative to the project file* so the whole output tree stays portable
(local folder, Drive copy, another machine).

This is Tier-1 deterministic work per the methodology: the master doc (§01) and the
Phase-2 basemap guide both deliver *layered* .qgz projects. Symbology defaults here
are a machine draft — cartographic refinement stays with the geologist.
"""

from __future__ import annotations

import math
import os
import zipfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET

#: config geometry vocab -> QGIS maplayer ``geometry`` attribute
GEOMETRY_ATTR = {
    "Point": "Point",
    "LineString": "Line",
    "MultiLineString": "Line",
    "Polygon": "Polygon",
    "MultiPolygon": "Polygon",
    "None": "No geometry",
    "Raster": "Raster",
}


@dataclass(frozen=True)
class QgzLayer:
    """One vector layer entry in the generated project.

    ``source`` is the OGR datasource string relative to the .qgz location, e.g.
    ``../06_Master_GeoPackage_Schema/Master.gpkg|layername=license_boundary``.
    ``geometry`` uses the config vocabulary (keys of :data:`GEOMETRY_ATTR`).
    ``symbol`` is an optional ("fill"|"line", properties) pair for a deterministic
    single-symbol renderer; layers without one get QGIS defaults on open. ``subset_string``
    provides an ordinary QGIS layer filter, ``epsg`` may override the project CRS for a
    source layer such as a georeferenced review preview, and ``read_only`` prevents ordinary
    edits through the generated project. Read-only project metadata remains defense in depth;
    callers must still validate source bytes before consuming them.
    """

    name: str
    source: str
    geometry: str
    symbol: tuple[str, dict[str, str]] | None = None
    visible: bool = True
    group: str = "Layers"
    provider: str = "ogr"
    subset_string: str | None = None
    epsg: int | None = None
    read_only: bool = False


@dataclass(frozen=True)
class QgzExtent:
    """Finite project-canvas bounds in the project CRS."""

    xmin: float
    ymin: float
    xmax: float
    ymax: float

    def __post_init__(self) -> None:
        values = (self.xmin, self.ymin, self.xmax, self.ymax)
        if not all(math.isfinite(value) for value in values):
            raise ValueError("QGIS project extent must contain only finite coordinates")
        if self.xmax <= self.xmin or self.ymax <= self.ymin:
            raise ValueError("QGIS project extent must have positive width and height")


def polygon_outline(color_rgba: str, width_mm: float, *, dash: bool = False):
    """A no-fill polygon outline symbol spec (color as 'r,g,b,a')."""
    return (
        "fill",
        {
            "color": "255,255,255,0",
            "style": "no",
            "outline_color": color_rgba,
            "outline_style": "dash" if dash else "solid",
            "outline_width": str(width_mm),
            "outline_width_unit": "MM",
            "joinstyle": "bevel",
        },
    )


def line_symbol(color_rgba: str, width_mm: float, *, dash: bool = False):
    """A simple line symbol spec (color as 'r,g,b,a')."""
    return (
        "line",
        {
            "line_color": color_rgba,
            "line_style": "dash" if dash else "solid",
            "line_width": str(width_mm),
            "line_width_unit": "MM",
            "joinstyle": "bevel",
            "capstyle": "square",
        },
    )


def point_symbol(color_rgba: str, size_mm: float):
    """A simple deterministic circle marker symbol."""
    return (
        "marker",
        {
            "color": color_rgba,
            "name": "circle",
            "outline_color": "0,0,0,255",
            "outline_width": "0.2",
            "size": str(size_mm),
            "size_unit": "MM",
        },
    )


def _layer_id(name: str) -> str:
    """Deterministic QGIS layer id (uuid-free so re-runs produce identical XML)."""
    return f"{name}_buduunkhad"


def _srs_element(epsg: int) -> ET.Element:
    """Full spatialrefsys block - QGIS needs the WKT/proj4 definition to reconstruct
    the CRS on load (authid alone reads back as an invalid/empty CRS)."""
    from pyproj import CRS as PyCRS

    crs = PyCRS.from_epsg(epsg)
    srs = ET.Element("spatialrefsys", {"nativeFormat": "Wkt"})
    ET.SubElement(srs, "wkt").text = crs.to_wkt()
    ET.SubElement(srs, "proj4").text = crs.to_proj4()
    ET.SubElement(srs, "srid").text = str(epsg)
    ET.SubElement(srs, "authid").text = f"EPSG:{epsg}"
    ET.SubElement(srs, "description").text = crs.name
    ET.SubElement(srs, "geographicflag").text = "true" if crs.is_geographic else "false"
    return srs


def _renderer_element(symbol: tuple[str, dict[str, str]]) -> ET.Element:
    sym_type, props = symbol
    renderer = ET.Element(
        "renderer-v2",
        {"type": "singleSymbol", "forceraster": "0", "symbollevels": "0", "enableorderby": "0"},
    )
    symbols = ET.SubElement(renderer, "symbols")
    sym = ET.SubElement(
        symbols,
        "symbol",
        {"type": sym_type, "name": "0", "alpha": "1", "clip_to_extent": "1", "force_rhr": "0"},
    )
    cls = {"fill": "SimpleFill", "line": "SimpleLine", "marker": "SimpleMarker"}[sym_type]
    layer = ET.SubElement(sym, "layer", {"class": cls, "enabled": "1", "locked": "0", "pass": "0"})
    for k, v in sorted(props.items()):
        ET.SubElement(layer, "prop", {"k": k, "v": v})
    ET.SubElement(renderer, "rotation")
    ET.SubElement(renderer, "sizescale")
    return renderer


def write_layered_qgz(
    path: Path,
    *,
    epsg: int,
    title: str,
    layers: list[QgzLayer],
    initial_extent: QgzExtent | None = None,
    qgis_version: str = "3.34.0",
) -> Path:
    """Write a .qgz whose project contains ``layers`` top-to-bottom in tree order."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    qgis = ET.Element("qgis", {"version": qgis_version, "projectname": title})
    ET.SubElement(qgis, "homePath", {"path": ""})
    ET.SubElement(qgis, "title").text = title
    project_crs = ET.SubElement(qgis, "projectCrs")
    project_crs.append(_srs_element(epsg))
    # QGIS only honours the <projectCrs> node when the legacy ProjectionsEnabled
    # property is set - without it the project opens with an unknown CRS.
    properties = ET.SubElement(qgis, "properties")
    spatial = ET.SubElement(properties, "SpatialRefSys")
    ET.SubElement(spatial, "ProjectionsEnabled", {"type": "int"}).text = "1"
    if initial_extent is not None:
        map_canvas = ET.SubElement(
            qgis,
            "mapcanvas",
            {"name": "theMapCanvas", "annotationsVisible": "1"},
        )
        ET.SubElement(map_canvas, "units").text = "meters"
        extent = ET.SubElement(map_canvas, "extent")
        ET.SubElement(extent, "xmin").text = str(initial_extent.xmin)
        ET.SubElement(extent, "ymin").text = str(initial_extent.ymin)
        ET.SubElement(extent, "xmax").text = str(initial_extent.xmax)
        ET.SubElement(extent, "ymax").text = str(initial_extent.ymax)
        ET.SubElement(map_canvas, "rotation").text = "0"
        destination = ET.SubElement(map_canvas, "destinationsrs")
        destination.append(_srs_element(epsg))

    tree_group = ET.SubElement(qgis, "layer-tree-group")
    project_layers = ET.SubElement(qgis, "projectlayers")
    layer_order = ET.SubElement(qgis, "layerorder")
    groups: dict[str, ET.Element] = {}

    for lyr in layers:
        geometry_attr = GEOMETRY_ATTR[lyr.geometry]
        lid = _layer_id(lyr.name)
        layer_group = groups.get(lyr.group)
        if layer_group is None:
            layer_group = ET.SubElement(
                tree_group,
                "layer-tree-group",
                {"name": lyr.group, "checked": "Qt::Checked", "expanded": "1"},
            )
            groups[lyr.group] = layer_group
        ET.SubElement(
            layer_group,
            "layer-tree-layer",
            {
                "name": lyr.name,
                "id": lid,
                "source": lyr.source,
                "providerKey": lyr.provider,
                "checked": "Qt::Checked" if lyr.visible else "Qt::Unchecked",
                "expanded": "1",
            },
        )
        attributes = {
            "type": "raster" if lyr.provider == "gdal" else "vector",
            "autoRefreshEnabled": "0",
        }
        if lyr.provider != "gdal":
            attributes["geometry"] = geometry_attr
        maplayer = ET.SubElement(project_layers, "maplayer", attributes)
        ET.SubElement(maplayer, "id").text = lid
        ET.SubElement(maplayer, "datasource").text = lyr.source
        ET.SubElement(maplayer, "layername").text = lyr.name
        if lyr.subset_string is not None:
            ET.SubElement(maplayer, "subsetString").text = lyr.subset_string
        ET.SubElement(maplayer, "readOnly").text = "1" if lyr.read_only else "0"
        srs = ET.SubElement(maplayer, "srs")
        srs.append(_srs_element(lyr.epsg or epsg))
        ET.SubElement(maplayer, "provider", {"encoding": "UTF-8"}).text = lyr.provider
        if lyr.symbol is not None and geometry_attr not in {"No geometry", "Raster"}:
            maplayer.append(_renderer_element(lyr.symbol))
        ET.SubElement(layer_order, "layer", {"id": lid})

    ET.indent(qgis)
    qgs_xml = ET.tostring(qgis, encoding="unicode", xml_declaration=True)
    if path.exists():
        path.unlink()
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        member = zipfile.ZipInfo(f"{path.stem}.qgs", date_time=(1980, 1, 1, 0, 0, 0))
        member.compress_type = zipfile.ZIP_DEFLATED
        member.external_attr = 0o600 << 16
        zf.writestr(member, qgs_xml.encode("utf-8"))
    return path


def read_qgz_layers(path: Path) -> list[dict[str, str]]:
    """Parse a .qgz and return its maplayer entries (id / name / datasource / geometry).

    Used by tests and QA to verify tree/projectlayers consistency without QGIS.
    """
    path = Path(path)
    with zipfile.ZipFile(path) as zf:
        qgs_name = next(n for n in zf.namelist() if n.endswith(".qgs"))
        root = ET.fromstring(zf.read(qgs_name))
    out: list[dict[str, str]] = []
    for ml in root.iter("maplayer"):
        out.append(
            {
                "id": ml.findtext("id") or "",
                "name": ml.findtext("layername") or "",
                "datasource": ml.findtext("datasource") or "",
                "geometry": ml.get("geometry") or ("Raster" if ml.get("type") == "raster" else ""),
                "subset": ml.findtext("subsetString") or "",
            }
        )
    return out


def copy_qgz_rebased(
    source: Path,
    target: Path,
    *,
    copied_sources: Mapping[Path, Path] | None = None,
    require_mapped_sources: bool = False,
) -> Path:
    """Copy a generated QGIS project while preserving every datasource relationship.

    A curated view may relocate declared deliverables while leaving large internal or editable
    review artifacts in their run directories. Exact mapped sources follow their curated copies;
    all other sources remain linked to their original bytes using a new relative path.
    """

    source = Path(source).resolve(strict=True)
    target = Path(target)
    if source == target.resolve(strict=False):
        raise ValueError("QGIS project copy target must differ from its source")
    target.parent.mkdir(parents=True, exist_ok=True)
    mappings = {
        Path(original).resolve(strict=True): Path(copied).resolve(strict=False)
        for original, copied in (copied_sources or {}).items()
    }
    try:
        with zipfile.ZipFile(source) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                raise ValueError("QGIS project archive contains duplicate members")
            for name in names:
                member_path = PurePosixPath(name)
                if member_path.is_absolute() or ".." in member_path.parts or "\\" in name:
                    raise ValueError("QGIS project archive contains an unsafe member path")
            qgs_names = [name for name in names if name.casefold().endswith(".qgs")]
            if len(qgs_names) != 1:
                raise ValueError("QGIS project archive must contain exactly one .qgs project")
            qgs_name = qgs_names[0]
            members = {name: archive.read(name) for name in names if not name.endswith("/")}
            root = ET.fromstring(members[qgs_name])
    except (ET.ParseError, KeyError, zipfile.BadZipFile) as exc:
        raise ValueError("QGIS project archive is invalid") from exc

    def rebase(value: str) -> str:
        path_part, separator, layer_part = value.partition("|")
        if not path_part:
            raise ValueError("QGIS project contains an empty datasource")
        original = Path(path_part)
        if not original.is_absolute():
            original = source.parent / original
        resolved = original.resolve(strict=True)
        if not resolved.is_file():
            raise ValueError(f"QGIS datasource is not a regular file: {resolved}")
        if require_mapped_sources and resolved not in mappings:
            raise ValueError(f"QGIS datasource has no curated copy: {resolved}")
        destination = mappings.get(resolved, resolved)
        relative = os.path.relpath(destination, target.parent.resolve()).replace("\\", "/")
        return f"{relative}{separator}{layer_part}"

    for node in root.iter("layer-tree-layer"):
        value = node.get("source")
        if value:
            node.set("source", rebase(value))
    for datasource in root.iter("datasource"):
        if datasource.text:
            datasource.text = rebase(datasource.text)

    ET.indent(root)
    members[qgs_name] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    if target.exists():
        target.unlink()
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, payload in sorted(members.items()):
            member = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            member.compress_type = zipfile.ZIP_DEFLATED
            member.external_attr = 0o600 << 16
            archive.writestr(member, payload)
    return target
