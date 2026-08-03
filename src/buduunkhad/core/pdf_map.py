"""Small deterministic PDF maps for sealed phase handoff packages.

The production environment does not require PyQGIS, matplotlib, or ReportLab.  This module writes
simple vector PDF maps directly so required review maps remain available in the base installation.
It renders only geometry already accepted by the caller; it never discovers or interprets evidence.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

from shapely.geometry import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from shapely.geometry.base import BaseGeometry

RGB = tuple[float, float, float]


@dataclass(frozen=True)
class MapLayer:
    """One caller-selected geometry set and its display-only map style."""

    name: str
    geometries: tuple[BaseGeometry, ...]
    stroke: RGB
    fill: RGB | None = None
    line_width: float = 1.0
    dashed: bool = False


@dataclass(frozen=True)
class MapLabel:
    x: float
    y: float
    text: str


def write_map_pdf(
    path: Path,
    *,
    title: str,
    subtitle: str,
    crs_label: str,
    run_id: str,
    layers: tuple[MapLayer, ...],
    labels: tuple[MapLabel, ...] = (),
    notes: tuple[str, ...] = (),
    footer: str,
    empty_message: str = "No spatial geometry was available for this map.",
) -> Path:
    """Write one landscape vector map without optional rendering dependencies."""

    _validate_layers(layers)
    usable = tuple(
        geometry for layer in layers for geometry in layer.geometries if _usable_geometry(geometry)
    )
    if not usable:
        return write_text_pdf(
            path,
            [title, subtitle, empty_message, crs_label, f"Run: {run_id}", *notes, footer],
        )

    page_width, page_height = 842.0, 595.0
    map_left, map_bottom, map_width, map_height = 48.0, 70.0, 590.0, 455.0
    xmin, ymin, xmax, ymax = _combined_bounds(usable)
    span_x, span_y = xmax - xmin, ymax - ymin
    base_span = max(span_x, span_y, 1.0)
    padding = base_span * 0.025
    if span_x <= 0:
        xmin -= padding
        xmax += padding
    else:
        xmin -= padding
        xmax += padding
    if span_y <= 0:
        ymin -= padding
        ymax += padding
    else:
        ymin -= padding
        ymax += padding
    span_x, span_y = xmax - xmin, ymax - ymin
    scale = min(map_width / span_x, map_height / span_y)
    draw_width, draw_height = span_x * scale, span_y * scale
    draw_left = map_left + (map_width - draw_width) / 2
    draw_bottom = map_bottom + (map_height - draw_height) / 2

    def transform(x: float, y: float) -> tuple[float, float]:
        return draw_left + (x - xmin) * scale, draw_bottom + (y - ymin) * scale

    content = [
        "1 1 1 rg",
        f"0 0 {page_width:.2f} {page_height:.2f} re f",
        "1 J 1 j",
        "0.97 0.97 0.97 rg",
        f"{map_left:.2f} {map_bottom:.2f} {map_width:.2f} {map_height:.2f} re f",
        "q",
        f"{map_left:.2f} {map_bottom:.2f} {map_width:.2f} {map_height:.2f} re W n",
    ]
    grid_interval = _nice_distance(max(span_x, span_y) / 6)
    content.extend(_grid_commands(xmin, ymin, xmax, ymax, grid_interval, transform))
    simplify_tolerance = max(span_x, span_y) / 3000
    for layer in layers:
        if not any(_usable_geometry(geometry) for geometry in layer.geometries):
            continue
        content.extend(_style_commands(layer))
        for geometry in layer.geometries:
            if not _usable_geometry(geometry):
                continue
            rendered = geometry.simplify(simplify_tolerance, preserve_topology=True)
            content.extend(_geometry_commands(rendered, transform, fill=layer.fill is not None))
    for label in labels:
        if not all(math.isfinite(value) for value in (label.x, label.y)):
            continue
        if xmin <= label.x <= xmax and ymin <= label.y <= ymax:
            x, y = transform(label.x, label.y)
            content.append(pdf_text(x + 3, y + 3, label.text, 6))
    content.extend(["Q", "0 0 0 RG", "0 0 0 rg", "0.8 w"])
    content.append(f"{map_left:.2f} {map_bottom:.2f} {map_width:.2f} {map_height:.2f} re S")
    content.extend(
        _coordinate_labels(
            xmin,
            ymin,
            xmax,
            ymax,
            grid_interval,
            transform,
            map_left,
            map_bottom,
            map_width,
            map_height,
        )
    )
    content.extend(_scale_bar(map_left + 20, map_bottom + 18, max(span_x, span_y), scale))
    content.extend(_north_arrow(785, 485))
    content.extend(
        [
            pdf_text(48, 560, title, 18),
            pdf_text(48, 542, subtitle, 9),
            pdf_text(664, 455, "Legend", 12),
        ]
    )
    legend_y = 432.0
    for layer in layers:
        if not any(_usable_geometry(geometry) for geometry in layer.geometries):
            continue
        content.extend(_legend_commands(layer, 664, legend_y))
        legend_y -= 22
    content.extend(
        [
            pdf_text(664, legend_y - 6, "Coordinate reference", 10),
            pdf_text(664, legend_y - 22, crs_label, 8),
            pdf_text(664, legend_y - 50, "Run identity", 10),
            pdf_text(664, legend_y - 66, run_id, 7),
        ]
    )
    note_y = legend_y - 96
    for note in notes:
        for line in _wrap_text(note, width=31):
            content.append(pdf_text(664, note_y, line, 6))
            note_y -= 9
    content.append(pdf_text(48, 30, footer, 8))
    return write_pdf_stream(
        path,
        "\n".join(content).encode("ascii", errors="replace"),
        page_width=page_width,
        page_height=page_height,
    )


def write_text_pdf(path: Path, lines: Iterable[str]) -> Path:
    commands = ["BT", "/F1 12 Tf", "72 760 Td"]
    for index, line in enumerate(lines):
        if index:
            commands.append("0 -20 Td")
        commands.append(f"({_escape_text(line)}) Tj")
    commands.append("ET")
    return write_pdf_stream(
        path,
        "\n".join(commands).encode("ascii", errors="replace"),
        page_width=612,
        page_height=792,
    )


def pdf_text(x: float, y: float, text: str, size: float) -> str:
    return f"BT /F1 {size:g} Tf {x:.2f} {y:.2f} Td ({_escape_text(text)}) Tj ET"


def write_pdf_stream(
    path: Path,
    stream: bytes,
    *,
    page_width: float,
    page_height: float,
) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_width:g} {page_height:g}] ".encode()
            + b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        ),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length "
        + str(len(stream)).encode("ascii")
        + b" >>\nstream\n"
        + stream
        + b"\nendstream",
    ]
    chunks = [b"%PDF-1.4\n"]
    offsets: list[int] = []
    for index, obj in enumerate(objects, start=1):
        offsets.append(sum(len(chunk) for chunk in chunks))
        chunks.extend((f"{index} 0 obj\n".encode("ascii"), obj, b"\nendobj\n"))
    xref_offset = sum(len(chunk) for chunk in chunks)
    chunks.extend(
        (
            f"xref\n0 {len(objects) + 1}\n".encode("ascii"),
            b"0000000000 65535 f \n",
        )
    )
    chunks.extend(f"{offset:010d} 00000 n \n".encode("ascii") for offset in offsets)
    chunks.append(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )
    path.write_bytes(b"".join(chunks))
    return path


def _validate_layers(layers: tuple[MapLayer, ...]) -> None:
    if len({layer.name for layer in layers}) != len(layers):
        raise ValueError("map layer names must be unique")
    for layer in layers:
        if not layer.name.strip():
            raise ValueError("map layer name must not be empty")
        if layer.line_width <= 0 or not math.isfinite(layer.line_width):
            raise ValueError("map layer line width must be positive")
        for colour in (layer.stroke, layer.fill):
            if colour is not None and (
                len(colour) != 3
                or not all(math.isfinite(value) and 0 <= value <= 1 for value in colour)
            ):
                raise ValueError("map colours must contain three values between zero and one")


def _usable_geometry(geometry: BaseGeometry) -> bool:
    return (
        isinstance(geometry, BaseGeometry)
        and not geometry.is_empty
        and all(math.isfinite(value) for value in geometry.bounds)
    )


def _combined_bounds(geometries: tuple[BaseGeometry, ...]) -> tuple[float, float, float, float]:
    bounds = [geometry.bounds for geometry in geometries]
    return (
        min(value[0] for value in bounds),
        min(value[1] for value in bounds),
        max(value[2] for value in bounds),
        max(value[3] for value in bounds),
    )


def _style_commands(layer: MapLayer) -> list[str]:
    stroke = " ".join(f"{value:g}" for value in layer.stroke)
    commands = [f"{stroke} RG", f"{layer.line_width:g} w"]
    if layer.fill is not None:
        commands.append(" ".join(f"{value:g}" for value in layer.fill) + " rg")
    commands.append("[4 3] 0 d" if layer.dashed else "[] 0 d")
    return commands


def _geometry_commands(
    geometry: BaseGeometry,
    transform,
    *,
    fill: bool,
) -> list[str]:
    if isinstance(geometry, Polygon):
        commands: list[str] = []
        for ring in (geometry.exterior, *geometry.interiors):
            coordinates = list(ring.coords)
            if not coordinates:
                continue
            x, y = transform(float(coordinates[0][0]), float(coordinates[0][1]))
            commands.append(f"{x:.2f} {y:.2f} m")
            for coordinate in coordinates[1:]:
                x, y = transform(float(coordinate[0]), float(coordinate[1]))
                commands.append(f"{x:.2f} {y:.2f} l")
            commands.append("h")
        commands.append("B*" if fill else "S")
        return commands
    if isinstance(geometry, LineString):
        coordinates = list(geometry.coords)
        if not coordinates:
            return []
        x, y = transform(float(coordinates[0][0]), float(coordinates[0][1]))
        commands = [f"{x:.2f} {y:.2f} m"]
        for coordinate in coordinates[1:]:
            x, y = transform(float(coordinate[0]), float(coordinate[1]))
            commands.append(f"{x:.2f} {y:.2f} l")
        commands.append("S")
        return commands
    if isinstance(geometry, Point):
        x, y = transform(float(geometry.x), float(geometry.y))
        return [f"{x - 2:.2f} {y - 2:.2f} 4 4 re B"]
    if isinstance(
        geometry,
        (MultiPolygon, MultiLineString, MultiPoint, GeometryCollection),
    ):
        return [
            command
            for part in geometry.geoms
            for command in _geometry_commands(part, transform, fill=fill)
        ]
    return []


def _nice_distance(value: float) -> float:
    if not math.isfinite(value) or value <= 0:
        raise ValueError("map grid distance must be positive")
    exponent = math.floor(math.log10(value))
    fraction = value / (10**exponent)
    nice = 1.0 if fraction < 1.5 else 2.0 if fraction < 3.5 else 5.0 if fraction < 7.5 else 10.0
    return nice * (10**exponent)


def _grid_values(minimum: float, maximum: float, interval: float) -> Iterator[float]:
    current = math.ceil(minimum / interval) * interval
    while current <= maximum:
        yield current
        current += interval


def _grid_commands(xmin, ymin, xmax, ymax, interval, transform) -> list[str]:
    commands = ["0.84 0.84 0.84 RG", "0.35 w"]
    for value in _grid_values(xmin, xmax, interval):
        x1, y1 = transform(value, ymin)
        x2, y2 = transform(value, ymax)
        commands.append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")
    for value in _grid_values(ymin, ymax, interval):
        x1, y1 = transform(xmin, value)
        x2, y2 = transform(xmax, value)
        commands.append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")
    return commands


def _coordinate_labels(
    xmin,
    ymin,
    xmax,
    ymax,
    interval,
    transform,
    map_left,
    map_bottom,
    map_width,
    map_height,
) -> list[str]:
    commands: list[str] = []
    for value in _grid_values(xmin, xmax, interval):
        x, _ = transform(value, ymin)
        if map_left <= x <= map_left + map_width:
            commands.append(pdf_text(x - 14, map_bottom - 12, f"{value:.0f} E", 6))
    for value in _grid_values(ymin, ymax, interval):
        _, y = transform(xmin, value)
        if map_bottom <= y <= map_bottom + map_height:
            commands.append(pdf_text(map_left + 3, y + 2, f"{value:.0f} N", 6))
    return commands


def _scale_bar(x: float, y: float, map_span: float, scale: float) -> list[str]:
    distance = _nice_distance(map_span / 5)
    width = distance * scale
    segment_width = width / 4
    commands = ["0 0 0 RG", "0.5 w"]
    for index in range(4):
        fill = "0 0 0 rg" if index % 2 == 0 else "1 1 1 rg"
        commands.append(
            f"{fill} {x + index * segment_width:.2f} {y:.2f} {segment_width:.2f} 7 re B"
        )
    commands.extend(
        (
            pdf_text(x, y - 10, "0", 6),
            pdf_text(x + width - 10, y - 10, _format_distance(distance), 6),
        )
    )
    return commands


def _north_arrow(x: float, y: float) -> list[str]:
    return [
        pdf_text(x - 4, y + 34, "N", 12),
        "0 0 0 rg 0 0 0 RG",
        f"{x:.2f} {y + 28:.2f} m {x - 7:.2f} {y:.2f} l {x:.2f} {y + 7:.2f} l "
        f"{x + 7:.2f} {y:.2f} l h f",
    ]


def _legend_commands(layer: MapLayer, x: float, y: float) -> list[str]:
    commands = _style_commands(layer)
    if layer.fill is None:
        commands.append(f"{x:.2f} {y:.2f} m {x + 38:.2f} {y:.2f} l S")
    else:
        commands.append(f"{x:.2f} {y - 5:.2f} 38 10 re B")
    commands.append(pdf_text(x + 48, y - 4, layer.name, 8))
    return commands


def _format_distance(distance_metres: float) -> str:
    if distance_metres >= 1000:
        return f"{distance_metres / 1000:g} km"
    return f"{distance_metres:g} m"


def _wrap_text(text: str, *, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines or [""]


def _escape_text(text: str) -> str:
    return str(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
