"""Exact-source ASTER readiness contract tests."""

from __future__ import annotations

import json

import numpy as np
import pytest
import rasterio
from pydantic import ValidationError
from rasterio.transform import from_origin

from buduunkhad.ai.fingerprint import sha256_value
from buduunkhad.core.aster_readiness import (
    AsterFileIdentity,
    AsterRasterValidation,
    AsterReadinessError,
    AsterReadinessRecord,
    AsterReadinessStatus,
    AsterSubdatasetInspection,
    load_aster_readiness_record,
    validate_aster_readiness,
    verify_aster_readiness_files,
    write_aster_readiness_record,
)
from buduunkhad.core.run_artifacts import sha256_file


def _identity(root, path) -> AsterFileIdentity:
    return AsterFileIdentity(
        path=path.relative_to(root).as_posix(),
        sha256=sha256_file(path),
        size_bytes=path.stat().st_size,
    )


def test_unavailable_record_still_binds_exact_hdf_bytes(tmp_path) -> None:
    source_root = tmp_path / "source"
    phase_root = tmp_path / "phase02"
    source = source_root / "ASTER" / "scene.hdf"
    source.parent.mkdir(parents=True)
    phase_root.mkdir()
    source.write_bytes(b"synthetic-hdf")

    record = validate_aster_readiness(
        source_run_id="source-run",
        processing_run_id="processing-run",
        source_phase_root=source_root,
        source_path=source,
        phase_root=phase_root,
        target_epsg=32647,
        gdalwarp=None,
    )

    assert record.status is AsterReadinessStatus.UNAVAILABLE
    assert record.source.sha256 == sha256_file(source)
    assert not record.source_opened
    assert "HDF4-capable gdalinfo is unavailable." in record.findings
    path = write_aster_readiness_record(record, phase_root / "readiness.json")
    assert load_aster_readiness_record(path) == record
    verify_aster_readiness_files(
        record,
        source_phase_root=source_root,
        phase_root=phase_root,
    )


def test_ready_record_requires_subdatasets_geolocation_and_valid_output(tmp_path) -> None:
    source_root = tmp_path / "source"
    phase_root = tmp_path / "phase02"
    source = source_root / "ASTER" / "scene.hdf"
    output = phase_root / "output.tif"
    source.parent.mkdir(parents=True)
    phase_root.mkdir()
    source.write_bytes(b"synthetic-hdf")
    with rasterio.open(
        output,
        "w",
        driver="GTiff",
        height=4,
        width=4,
        count=1,
        dtype="float32",
        crs="EPSG:32647",
        transform=from_origin(300000, 5100000, 30, 30),
        nodata=-9999.0,
    ) as dataset:
        dataset.write(np.ones((4, 4), dtype="float32"), 1)

    required = ("SWIR_Swath:ImageData4", "VNIR_Swath:ImageData1")
    inspections = tuple(
        AsterSubdatasetInspection(
            logical_name=name,
            description=f"HDF4_EOS:<source>:{name}",
            width=4,
            height=4,
            band_types=("UInt16",),
            geolocation_evidence=("gcps",),
        )
        for name in required
    )
    output_validation = AsterRasterValidation(
        artifact=_identity(phase_root, output),
        epsg=32647,
        width=4,
        height=4,
        band_count=1,
        nodata_values=(-9999.0,),
        finite_pixel_count=16,
    )
    record = AsterReadinessRecord.create(
        source_run_id="source-run",
        processing_run_id="processing-run",
        source=_identity(source_root, source),
        target_epsg=32647,
        gdal_version="GDAL synthetic",
        source_opened=True,
        subdatasets=inspections,
        required_logical_subdatasets=required,
        required_subdatasets_present=True,
        geolocation_evidence_complete=True,
        reprojection_test_passed=True,
        outputs=(output_validation,),
        status=AsterReadinessStatus.READY,
        findings=("Exact-source ASTER technical readiness checks passed.",),
        limitations=("Technical readiness is not geological approval.",),
    )
    assert record.status is AsterReadinessStatus.READY

    changed = record.model_dump(mode="python")
    changed["status"] = AsterReadinessStatus.UNAVAILABLE
    changed["readiness_id"] = sha256_value(
        {key: value for key, value in changed.items() if key != "readiness_id"}
    )
    with pytest.raises(ValidationError, match="status does not match"):
        AsterReadinessRecord.model_validate(changed)


def test_readiness_file_mutation_and_duplicate_json_keys_fail_closed(tmp_path) -> None:
    source_root = tmp_path / "source"
    phase_root = tmp_path / "phase02"
    source = source_root / "ASTER" / "scene.hdf"
    source.parent.mkdir(parents=True)
    phase_root.mkdir()
    source.write_bytes(b"synthetic-hdf")
    record = validate_aster_readiness(
        source_run_id="source-run",
        processing_run_id="processing-run",
        source_phase_root=source_root,
        source_path=source,
        phase_root=phase_root,
        target_epsg=32647,
        gdalwarp=None,
    )
    source.write_bytes(b"changed")
    with pytest.raises(AsterReadinessError, match="bytes changed"):
        verify_aster_readiness_files(
            record,
            source_phase_root=source_root,
            phase_root=phase_root,
        )

    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text(
        json.dumps(record.model_dump(mode="json")).replace(
            '{"format_version":', '{"format_version":"1.0.0","format_version":', 1
        ),
        encoding="utf-8",
    )
    with pytest.raises(AsterReadinessError, match="record is invalid"):
        load_aster_readiness_record(duplicate)
