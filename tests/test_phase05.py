from __future__ import annotations

import struct
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.transform import from_origin
from shapely.geometry import box

from buduunkhad.core import phase05_drone, vector_io
from buduunkhad.core.execution_policy import ExecutionMode, resolve_execution_policy
from buduunkhad.core.qaqc import Decision
from buduunkhad.phases.base import RunContext
from buduunkhad.phases.phase05_drone_lidar import Phase05DroneLidar


def _raster(path: Path, *, x: float, bands: int = 1, dtype: str = "float32") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = np.arange(36, dtype=dtype).reshape(6, 6)
    profile = {
        "driver": "GTiff",
        "height": 6,
        "width": 6,
        "count": bands,
        "dtype": dtype,
        "crs": "EPSG:32647",
        "transform": from_origin(x, 5_096_000, 1, 1),
        "nodata": -9999 if dtype == "float32" else 0,
    }
    with rasterio.open(path, "w", **profile) as target:
        for band in range(1, bands + 1):
            target.write(data, band)
    return path


def _las(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = bytearray(227)
    header[:4] = b"LASF"
    header[24:26] = bytes((1, 2))
    struct.pack_into("<H", header, 94, 227)
    struct.pack_into("<I", header, 96, 227)
    struct.pack_into("<I", header, 100, 0)
    header[104] = 3
    struct.pack_into("<H", header, 105, 34)
    struct.pack_into("<I", header, 107, 10)
    struct.pack_into("<3d", header, 131, 0.01, 0.01, 0.01)
    struct.pack_into("<3d", header, 155, 0, 0, 0)
    struct.pack_into("<6d", header, 179, 314_006, 314_000, 5_096_000, 5_095_994, 1200, 1100)
    path.write_bytes(header)
    return path


def _campaign(root: Path) -> Path:
    original = root / "2. Processed" / "01_DJI_TERRA_ORIGINAL_EXPORT_DO_NOT_EDIT"
    colours = root / "2. Processed" / "02_METASHAPE_ORTHO_COLOR_CORRECTED"
    final = root / "2. Processed" / "03_DEM_MOSAIC_FINAL"
    for number in range(1, 80):
        block = original / f"B{number}_export"
        x = 314_000 + number * 10
        _raster(block / "dem.tif", x=x)
        _raster(block / "dsm.tif", x=x)
        _raster(block / "dom.tif", x=x, bands=4, dtype="uint8")
        (block / f"B{number}_{'L3' if number <= 4 else 'L2'}_report.pdf").write_bytes(
            b"%PDF synthetic"
        )
        if number != 69:
            _las(block / "cloud_merged.las")
    _raster(colours / "Ortho_B1.tif", x=314_010, bands=4, dtype="uint8")
    _raster(final / "BUDUUNKHAD_FULL_AREA_DEM_MOSAIC_FINAL.tif", x=314_000)
    control = root / "4. Conrol point"
    control.mkdir(parents=True)
    (control / "control-certificate.pdf").write_bytes(b"%PDF control")
    reports = root / "5.Daily_report"
    reports.mkdir(parents=True)
    (reports / "daily-01.pdf").write_bytes(b"%PDF daily")
    return root


def _phase04_output(config) -> None:
    path = config.output_root / "04_Phase_4_Preliminary_Prospect_Delineation_and_Ranking"
    target = path / "prospects.gpkg"
    prospects = gpd.GeoDataFrame(  # ty: ignore[no-matching-overload]
        [
            {
                "candidate_id": "P-001",
                "prospect_class": "C",
                "geometry": box(314_000, 5_095_990, 314_100, 5_096_010),
            }
        ],
        geometry="geometry",
        crs="EPSG:32647",
    )
    vector_io.write_layer(prospects, target, layer="prospect_candidate_areas")


def test_phase05_postflight_slice_produces_real_outputs(project, monkeypatch):
    config, register, work = project
    campaign = _campaign(work / "campaign")
    monkeypatch.setenv("BUDUUNKHAD_PHASE05_SOURCE_ROOT", str(campaign))
    _phase04_output(config)
    phase = Phase05DroneLidar()
    ctx = RunContext(config=config, register=register, run_id="phase05-test")

    phase.prepare(ctx)
    result = phase.run(ctx)
    report = phase.qaqc(ctx)

    assert result.status == "ok"
    assert len(result.outputs) == 10
    assert all(path.is_file() for path in result.outputs)
    assert not report.has_failures
    assert all(item.decision in {Decision.PASS, Decision.NA} for item in report.items)
    source = phase05_drone.inspect_survey(campaign, target_epsg=32647)
    assert len(source.blocks) == 79
    assert sum(block.point_cloud is None for block in source.blocks) == 1
    interpretation = next(path for path in result.outputs if "Structure_Outcrop" in path.name)
    assert {
        "drone_block_coverage",
        "structure_interpretation_line",
        "outcrop_interpretation_polygon",
        "field_observation_point",
        "sample_planning_point",
        "phase04_prospect_candidates",
    } <= set(vector_io.list_gpkg_layers(interpretation))

    project_path = next(path for path in result.outputs if path.suffix == ".qgz")
    with zipfile.ZipFile(project_path) as archive:
        member = next(name for name in archive.namelist() if name.endswith(".qgs"))
        xml = ET.fromstring(archive.read(member))
    generator = xml.find("./mapViewDocks3D/view/qgis3d/terrain/generator")
    assert generator is not None
    assert generator.get("layer") == "Drone DTM_buduunkhad"


def test_phase05_source_identity_detects_metadata_change(project):
    _config, _register, work = project
    campaign = _campaign(work / "campaign")
    before = phase05_drone.source_tree_identity(campaign)
    report = campaign / "5.Daily_report" / "daily-01.pdf"
    report.write_bytes(report.read_bytes() + b"changed")
    assert phase05_drone.source_tree_identity(campaign) != before


def test_phase05_is_an_automated_real_execution_mode():
    binding = resolve_execution_policy(["05"], dry_run=False)
    assert binding.phase_modes[0].execution_mode is ExecutionMode.AUTOMATED
