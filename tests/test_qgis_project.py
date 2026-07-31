"""core.qgis_project — deterministic layered .qgz generation."""

from __future__ import annotations

import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from buduunkhad.core.qgis_project import (
    QgzExtent,
    QgzLayer,
    copy_qgz_rebased,
    line_symbol,
    polygon_outline,
    read_qgz_layers,
    write_layered_qgz,
)


def _layers() -> list[QgzLayer]:
    return [
        QgzLayer(
            name="License Boundary (L23222)",
            source="../05_KMZ_KML_to_GPKG/boundary.gpkg|layername=license_boundary",
            geometry="MultiPolygon",
            symbol=polygon_outline("227,26,28,255", 0.8),
        ),
        QgzLayer(
            name="faults_structures_line",
            source="../06_Master_GeoPackage_Schema/master.gpkg|layername=faults_structures_line",
            geometry="LineString",
            symbol=line_symbol("0,0,0,255", 0.4, dash=True),
        ),
        QgzLayer(
            name="pXRF_reading_table",
            source="../06_Master_GeoPackage_Schema/master.gpkg|layername=pXRF_reading_table",
            geometry="None",
            visible=False,
        ),
    ]


def test_write_layered_qgz_roundtrip(tmp_path):
    qgz = write_layered_qgz(
        tmp_path / "project.qgz", epsg=32647, title="Test Master", layers=_layers()
    )
    entries = read_qgz_layers(qgz)
    assert [e["name"] for e in entries] == [
        "License Boundary (L23222)",
        "faults_structures_line",
        "pXRF_reading_table",
    ]
    assert len({e["id"] for e in entries}) == 3  # unique, deterministic ids
    assert entries[0]["geometry"] == "Polygon"
    assert entries[1]["geometry"] == "Line"
    assert entries[2]["geometry"] == "No geometry"
    assert all("|layername=" in e["datasource"] for e in entries)


def test_qgz_tree_projectlayers_and_order_consistent(tmp_path):
    extent = QgzExtent(296_000, 5_030_000, 313_000, 5_053_000)
    qgz = write_layered_qgz(
        tmp_path / "p.qgz",
        epsg=32647,
        title="T",
        layers=_layers(),
        initial_extent=extent,
    )
    with zipfile.ZipFile(qgz) as zf:
        root = ET.fromstring(zf.read(next(n for n in zf.namelist() if n.endswith(".qgs"))))

    assert root.find("projectCrs/spatialrefsys/authid") is not None
    assert root.findtext("projectCrs/spatialrefsys/authid") == "EPSG:32647"
    assert root.findtext("mapcanvas/extent/xmin") == "296000"
    assert root.findtext("mapcanvas/extent/ymin") == "5030000"
    assert root.findtext("mapcanvas/extent/xmax") == "313000"
    assert root.findtext("mapcanvas/extent/ymax") == "5053000"
    assert root.findtext("mapcanvas/destinationsrs/spatialrefsys/authid") == "EPSG:32647"

    tree_ids = [n.get("id") for n in root.iter("layer-tree-layer")]
    maplayer_ids = [ml.findtext("id") for ml in root.iter("maplayer")]
    order_ids = [n.get("id") for n in root.find("layerorder").iter("layer")]  # ty: ignore[unresolved-attribute]
    assert tree_ids == maplayer_ids == order_ids

    # visibility flag round-trips into the tree
    checked = {n.get("name"): n.get("checked") for n in root.iter("layer-tree-layer")}
    assert checked["pXRF_reading_table"] == "Qt::Unchecked"
    assert checked["faults_structures_line"] == "Qt::Checked"

    # symbology embedded for the styled layers only
    renderers = [ml.find("renderer-v2") for ml in root.iter("maplayer")]
    assert renderers[0] is not None and renderers[1] is not None
    assert renderers[2] is None


def test_qgz_extent_rejects_non_finite_or_inverted_values():
    with pytest.raises(ValueError, match="finite"):
        QgzExtent(float("nan"), 0, 1, 1)
    with pytest.raises(ValueError, match="positive width"):
        QgzExtent(1, 0, 1, 1)


def test_write_layered_qgz_is_deterministic(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    a = write_layered_qgz(first / "project.qgz", epsg=32647, title="T", layers=_layers())
    b = write_layered_qgz(second / "project.qgz", epsg=32647, title="T", layers=_layers())
    with zipfile.ZipFile(a) as za, zipfile.ZipFile(b) as zb:
        xa = za.read(next(n for n in za.namelist() if n.endswith(".qgs")))
        xb = zb.read(next(n for n in zb.namelist() if n.endswith(".qgs")))
    assert xa == xb
    assert a.read_bytes() == b.read_bytes()


def test_copy_qgz_rebased_preserves_and_relocates_datasources(tmp_path):
    source_data = tmp_path / "sealed" / "data.gpkg"
    source_data.parent.mkdir()
    source_data.write_bytes(b"sealed-data")
    source_project = write_layered_qgz(
        tmp_path / "sealed" / "project.qgz",
        epsg=32647,
        title="Source",
        layers=[
            QgzLayer(
                name="Evidence",
                source="data.gpkg|layername=evidence",
                geometry="Polygon",
            )
        ],
    )
    copied_data = tmp_path / "results" / "data" / "data.gpkg"
    copied_data.parent.mkdir(parents=True)
    copied_data.write_bytes(source_data.read_bytes())
    first = copy_qgz_rebased(
        source_project,
        tmp_path / "results" / "projects" / "project.qgz",
        copied_sources={source_data: copied_data},
    )
    second = copy_qgz_rebased(
        source_project,
        tmp_path / "results-2" / "projects" / "project.qgz",
        copied_sources={source_data: tmp_path / "results-2" / "data" / "data.gpkg"},
    )

    first_source = read_qgz_layers(first)[0]["datasource"].partition("|")[0]
    assert (first.parent / Path(first_source)).resolve() == copied_data.resolve()
    with zipfile.ZipFile(first) as archive:
        first_xml = archive.read(next(name for name in archive.namelist() if name.endswith(".qgs")))
    with zipfile.ZipFile(second) as archive:
        second_xml = archive.read(
            next(name for name in archive.namelist() if name.endswith(".qgs"))
        )
    assert first_xml == second_xml


def test_copy_qgz_rebased_fails_when_datasource_is_missing(tmp_path):
    source_project = write_layered_qgz(
        tmp_path / "source.qgz",
        epsg=32647,
        title="Source",
        layers=[
            QgzLayer(
                name="Missing",
                source="missing.gpkg|layername=missing",
                geometry="Polygon",
            )
        ],
    )

    with pytest.raises(FileNotFoundError):
        copy_qgz_rebased(source_project, tmp_path / "results" / "project.qgz")


def test_copy_qgz_rebased_can_require_every_datasource_to_be_curated(tmp_path):
    source_data = tmp_path / "source.gpkg"
    source_data.write_bytes(b"source")
    source_project = write_layered_qgz(
        tmp_path / "source.qgz",
        epsg=32647,
        title="Source",
        layers=[
            QgzLayer(
                name="Source",
                source="source.gpkg|layername=source",
                geometry="Polygon",
            )
        ],
    )

    with pytest.raises(ValueError, match="has no curated copy"):
        copy_qgz_rebased(
            source_project,
            tmp_path / "results" / "project.qgz",
            require_mapped_sources=True,
        )
