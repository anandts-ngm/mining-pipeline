"""Deterministic tile-pixel to source/world coordinate conversion."""

from __future__ import annotations

import math
from itertools import pairwise
from typing import cast

from pyproj import CRS, Transformer
from shapely.geometry import LineString, Point, Polygon
from shapely.geometry.base import BaseGeometry

from buduunkhad.ai.contracts import PixelGeometry, PixelLineString, PixelPoint, PixelPolygon
from buduunkhad.geospatial_ai.manifests import SourceAssetRecord, TileRecord

_SOURCE_EXTENT_EDGE_SEGMENTS = 256
_GEOMETRY_EDGE_SEGMENTS = 256


class PixelWorldError(ValueError):
    """Pixel geometry cannot be transformed without ambiguity or clamping."""


def tile_pixel_to_world(
    x: float,
    y: float,
    *,
    tile: TileRecord,
    source: SourceAssetRecord,
) -> tuple[float, float]:
    return _tile_pixel_to_world(
        x,
        y,
        tile=tile,
        source=source,
        transformer=_source_to_target_transformer(source),
    )


def _tile_pixel_to_world(
    x: float,
    y: float,
    *,
    tile: TileRecord,
    source: SourceAssetRecord,
    transformer: Transformer | None,
) -> tuple[float, float]:
    if not math.isfinite(x) or not math.isfinite(y):
        raise PixelWorldError("pixel coordinate is non-finite")
    if not (0 <= x <= tile.width and 0 <= y <= tile.height):
        raise PixelWorldError("pixel coordinate lies outside its source tile")
    source_x = tile.x_offset + x
    source_y = tile.y_offset + y
    if not (0 <= source_x <= source.width and 0 <= source_y <= source.height):
        raise PixelWorldError("pixel coordinate lies outside the source raster")
    affine = source.affine
    determinant = affine.a * affine.e - affine.b * affine.d
    if not math.isfinite(determinant) or determinant == 0:
        raise PixelWorldError("source affine transform is singular or unsafe")
    map_x = affine.a * source_x + affine.b * source_y + affine.c
    map_y = affine.d * source_x + affine.e * source_y + affine.f
    if not math.isfinite(map_x) or not math.isfinite(map_y):
        raise PixelWorldError("source affine transform produced non-finite coordinates")
    try:
        if transformer is None:
            world_x, world_y = map_x, map_y
        else:
            world_x, world_y = transformer.transform(map_x, map_y, errcheck=True)
    except Exception as exc:
        raise PixelWorldError("CRS transformation failed") from exc
    if not math.isfinite(world_x) or not math.isfinite(world_y):
        raise PixelWorldError("CRS transformation produced non-finite coordinates")
    return float(world_x), float(world_y)


def _source_to_target_transformer(source: SourceAssetRecord) -> Transformer | None:
    if source.source_crs is None:
        raise PixelWorldError("source raster has no CRS")
    try:
        source_crs = CRS.from_user_input(source.source_crs)
        target_crs = CRS.from_user_input(source.target_crs)
        if source_crs == target_crs:
            return None
        return Transformer.from_crs(source_crs, target_crs, always_xy=True)
    except Exception as exc:
        raise PixelWorldError("source or target CRS is unsupported") from exc


def transform_pixel_geometry(
    geometry: PixelGeometry,
    *,
    tile: TileRecord,
    source: SourceAssetRecord,
) -> BaseGeometry:
    transformer = _source_to_target_transformer(source)

    def convert(point: tuple[float, float]) -> tuple[float, float]:
        return _tile_pixel_to_world(
            point[0],
            point[1],
            tile=tile,
            source=source,
            transformer=transformer,
        )

    maximum_step = max(source.width, source.height) / _GEOMETRY_EDGE_SEGMENTS

    def transformed_path(
        points: tuple[tuple[float, float], ...],
    ) -> tuple[tuple[float, float], ...]:
        pixel_points = (
            _densify_pixel_path(points, maximum_step=maximum_step)
            if transformer is not None
            else points
        )
        return tuple(convert(point) for point in pixel_points)

    if isinstance(geometry, PixelPoint):
        return Point(convert(geometry.coordinates))
    if isinstance(geometry, PixelLineString):
        coordinates = transformed_path(geometry.coordinates)
        if len(set(coordinates)) < 2:
            raise PixelWorldError("line geometry is degenerate after transformation")
        return LineString(coordinates)
    if isinstance(geometry, PixelPolygon):
        rings = tuple(transformed_path(ring) for ring in geometry.coordinates)
        if any(len(set(ring[:-1])) < 3 for ring in rings):
            raise PixelWorldError("polygon geometry is degenerate after transformation")
        return Polygon(rings[0], holes=rings[1:])
    raise PixelWorldError(f"unsupported pixel geometry: {type(geometry).__name__}")


def _densify_pixel_path(
    points: tuple[tuple[float, float], ...],
    *,
    maximum_step: float,
) -> tuple[tuple[float, float], ...]:
    densified: list[tuple[float, float]] = []
    for start, end in pairwise(points):
        delta_x = end[0] - start[0]
        delta_y = end[1] - start[1]
        segment_count = max(
            1,
            math.ceil(max(abs(delta_x), abs(delta_y)) / maximum_step),
        )
        densified.extend(
            (
                start[0] + delta_x * index / segment_count,
                start[1] + delta_y * index / segment_count,
            )
            for index in range(segment_count)
        )
    densified.append(points[-1])
    return tuple(densified)


def transformed_source_extent(source: SourceAssetRecord) -> Polygon:
    """Return the target-CRS footprint of the complete source raster."""

    synthetic = TileRecord(
        tile_id="source-extent",
        source_asset_id=source.asset_id,
        source_sha256=source.sha256,
        band_identity="extent",
        x_offset=0,
        y_offset=0,
        width=source.width,
        height=source.height,
        overlap=0,
        image_relative_path="extent",
        image_sha256="0" * 64,
        valid_fraction=1,
    )
    transformer = _source_to_target_transformer(source)

    def convert(x: float, y: float) -> tuple[float, float]:
        return _tile_pixel_to_world(
            x,
            y,
            tile=synthetic,
            source=source,
            transformer=transformer,
        )

    if transformer is None:
        ring = (
            convert(0, 0),
            convert(source.width, 0),
            convert(source.width, source.height),
            convert(0, source.height),
            convert(0, 0),
        )
        return Polygon(ring)

    # Reprojected raster edges are curves in the target CRS. Four transformed corners can
    # exclude valid points on those curves, so approximate every edge and add only a
    # scale-relative numerical envelope around the approximation.
    segments = _SOURCE_EXTENT_EDGE_SEGMENTS
    top = tuple(
        convert(
            source.width * index / segments,
            0,
        )
        for index in range(segments + 1)
    )
    right = tuple(
        convert(
            source.width,
            source.height * index / segments,
        )
        for index in range(1, segments + 1)
    )
    bottom = tuple(
        convert(
            source.width * (segments - index) / segments,
            source.height,
        )
        for index in range(1, segments + 1)
    )
    left = tuple(
        convert(
            0,
            source.height * (segments - index) / segments,
        )
        for index in range(1, segments + 1)
    )
    footprint = Polygon(top + right + bottom + left)
    min_x, min_y, max_x, max_y = footprint.bounds
    numerical_tolerance = max(max_x - min_x, max_y - min_y, 1.0) * 1e-8
    return cast(Polygon, footprint.buffer(numerical_tolerance))
