"""Local GIS evidence intake remains immutable, explicit, and phase-scoped."""

from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd
import pytest
from pydantic import ValidationError
from shapely.geometry import LineString, Polygon

from buduunkhad.core.evidence_manifest import (
    EvidenceAuthorityResolver,
    EvidenceExecutionMode,
    EvidenceManifestError,
    EvidenceOrigin,
    EvidenceRole,
    EvidenceSourceKind,
)
from buduunkhad.core.local_evidence_intake import register_local_evidence


def _resolver(tmp_path: Path) -> EvidenceAuthorityResolver:
    return EvidenceAuthorityResolver(
        runs_root=tmp_path / "runs",
        evidence_root=tmp_path / "evidence",
        target_epsg=32647,
    )


def test_local_geopackage_is_copied_and_resolved_by_exact_layer(tmp_path: Path) -> None:
    source = tmp_path / "manual.gpkg"
    gpd.GeoDataFrame(  # ty: ignore[no-matching-overload]
        {"class": ["anomaly"], "geometry": [Polygon([(0, 0), (10, 0), (10, 10), (0, 0)])]},
        crs="EPSG:32647",
    ).to_file(source, layer="geochem", driver="GPKG")

    manifest = register_local_evidence(
        runs_root=tmp_path / "runs",
        evidence_root=tmp_path / "evidence",
        target_epsg=32647,
        source_path=source,
        source_layer="geochem",
        evidence_role=EvidenceRole.GEOCHEMICAL_ANOMALY,
        origin=EvidenceOrigin.HUMAN_DIGITIZED,
        eligible_phases=("04",),
        eligible_modes=(EvidenceExecutionMode.LEGACY_COMPARATOR,),
        registered_by="QA Engineer",
        registration_reason="Use the inspected manual anomaly layer in the comparator.",
        limitations=("Historical anomaly interpretation; use with caution.",),
    )
    selected = _resolver(tmp_path).resolve_selected([manifest.manifest_id])

    assert len(selected) == 1
    assert selected[0].record.source_kind is EvidenceSourceKind.LOCAL_INTAKE
    assert selected[0].record.evidence_role is EvidenceRole.GEOCHEMICAL_ANOMALY
    assert selected[0].artifact != source.resolve()
    assert selected[0].artifact.read_bytes() == source.read_bytes()
    assert selected[0].record.eligible_phases == ("04",)


def test_local_shapefile_bundle_is_preserved_and_converted(tmp_path: Path) -> None:
    source = tmp_path / "geology.shp"
    gpd.GeoDataFrame(  # ty: ignore[no-matching-overload]
        {"unit": ["intrusive"], "geometry": [Polygon([(0, 0), (5, 0), (5, 5), (0, 0)])]},
        crs="EPSG:32647",
    ).to_file(source)

    manifest = register_local_evidence(
        runs_root=tmp_path / "runs",
        evidence_root=tmp_path / "evidence",
        target_epsg=32647,
        source_path=source,
        source_layer=None,
        evidence_role=EvidenceRole.GEOLOGY,
        origin=EvidenceOrigin.HUMAN_DIGITIZED,
        eligible_phases=("03",),
        eligible_modes=(EvidenceExecutionMode.SUPPORT_EVIDENCE,),
        target_layer_name="geology_units_50k_polygon",
        registered_by="QA Engineer",
        registration_reason="Preserve the existing human-digitized geology layer.",
    )
    selected = _resolver(tmp_path).resolve_selected([manifest.manifest_id])
    authority_path = tmp_path / "evidence" / selected[0].record.source_authority_path
    authority = json.loads(authority_path.read_text(encoding="utf-8"))

    assert selected[0].record.layer_name == "evidence"
    assert selected[0].artifact.suffix == ".gpkg"
    assert len(gpd.read_file(selected[0].artifact, layer="evidence")) == 1
    assert authority["source_format"] == "shapefile"
    assert authority["conversion"] == "shapefile-to-gpkg-v1"
    assert {Path(item["relative_path"]).suffix for item in authority["source_files"]} >= {
        ".shp",
        ".shx",
        ".dbf",
        ".prj",
    }


def test_local_intake_detects_copied_source_mutation(tmp_path: Path) -> None:
    source = tmp_path / "manual.gpkg"
    gpd.GeoDataFrame(  # ty: ignore[no-matching-overload]
        {"geometry": [LineString([(0, 0), (1, 1)])]}, crs="EPSG:32647"
    ).to_file(source, layer="faults", driver="GPKG")
    manifest = register_local_evidence(
        runs_root=tmp_path / "runs",
        evidence_root=tmp_path / "evidence",
        target_epsg=32647,
        source_path=source,
        source_layer="faults",
        evidence_role=EvidenceRole.STRUCTURE,
        origin=EvidenceOrigin.HUMAN_DIGITIZED,
        eligible_phases=("03",),
        eligible_modes=(EvidenceExecutionMode.SUPPORT_EVIDENCE,),
        target_layer_name="faults_structures_line",
        registered_by="QA Engineer",
        registration_reason="Regression fixture.",
    )
    record = manifest.records[0]
    authority = json.loads(
        (tmp_path / "evidence" / record.source_authority_path).read_text(encoding="utf-8")
    )
    copied_source = tmp_path / "evidence" / authority["source_files"][0]["relative_path"]
    copied_source.write_bytes(copied_source.read_bytes() + b"changed")

    with pytest.raises(EvidenceManifestError, match="source bytes changed"):
        _resolver(tmp_path).resolve_selected([manifest.manifest_id])


def test_local_intake_cannot_grant_unimplemented_phase04_role(tmp_path: Path) -> None:
    source = tmp_path / "manual.gpkg"
    gpd.GeoDataFrame(  # ty: ignore[no-matching-overload]
        {"geometry": [Polygon([(0, 0), (1, 0), (1, 1), (0, 0)])]}, crs="EPSG:32647"
    ).to_file(source, layer="geology", driver="GPKG")

    with pytest.raises(ValidationError, match="accepts only implemented manifest roles"):
        register_local_evidence(
            runs_root=tmp_path / "runs",
            evidence_root=tmp_path / "evidence",
            target_epsg=32647,
            source_path=source,
            source_layer="geology",
            evidence_role=EvidenceRole.GEOLOGY,
            origin=EvidenceOrigin.HUMAN_DIGITIZED,
            eligible_phases=("04",),
            eligible_modes=(EvidenceExecutionMode.LEGACY_COMPARATOR,),
            registered_by="QA Engineer",
            registration_reason="Invalid role regression fixture.",
        )
