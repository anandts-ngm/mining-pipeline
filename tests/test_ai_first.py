from __future__ import annotations

import json
import os
import shutil
import tempfile
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pytest
import rasterio
from PIL import Image
from rasterio.transform import from_origin

from buduunkhad.ai.contracts import AIUsage, TaskType
from buduunkhad.ai.providers import ProviderCall, ProviderExecutionResult
from buduunkhad.config import AIPhase03SourceConfig, load_config
from buduunkhad.geospatial_ai.ai_first import (
    Phase03AIFirstError,
    load_phase03_ai_batch_manifest,
    load_phase03_ai_first_manifest,
    run_phase03_ai_first,
    run_phase03_ai_first_batch,
)
from buduunkhad.geospatial_ai.execution import LiveExecutionError
from buduunkhad.geospatial_ai.path_safety import StorageRoots
from buduunkhad.geospatial_ai.snapshots import import_phase03_snapshot_source
from buduunkhad.pipeline import run_pipeline


class _Phase03Provider:
    name = "openai"

    def __init__(self, *, feature_legend_code: str = "Q") -> None:
        self.calls: list[ProviderCall] = []
        self.feature_legend_code = feature_legend_code

    def execute(self, call: ProviderCall) -> ProviderExecutionResult:
        self.calls.append(call)
        context = json.loads(call.user_prompt.rsplit("REQUEST_CONTEXT_JSON\n", 1)[1])
        tile = context["tiles"][0]
        source_reference = {
            "asset_id": tile["source_asset_id"],
            "sha256": tile["source_sha256"],
            "locators": [
                {
                    "kind": "raster_tile",
                    "tile_id": tile["tile_id"],
                    "x_offset": tile["x_offset"],
                    "y_offset": tile["y_offset"],
                    "width": tile["width"],
                    "height": tile["height"],
                }
            ],
        }
        if call.task_type is TaskType.LEGEND_EXTRACTION:
            payload = {
                "items": [
                    {
                        "legend_code": "Q",
                        "label": "Synthetic geological unit",
                        "description": "Offline integration-test legend entry.",
                        "color": "#c8b38a",
                        "source_references": [source_reference],
                        "confidence": 0.9,
                        "confidence_components": [
                            {
                                "name": "visibility",
                                "score": 0.9,
                                "rationale": "The synthetic symbol is unobstructed.",
                            }
                        ],
                        "limitations": ["Synthetic test evidence only."],
                    }
                ],
                "limitations": ["No live provider was called."],
            }
        elif call.task_type is TaskType.GEOLOGICAL_FEATURE_PROPOSAL:
            payload = {
                "proposals": [
                    {
                        "feature_id": "synthetic-geology-unit-1",
                        "layer": "geology_units",
                        "feature_type": "geology-unit",
                        "legend_code": self.feature_legend_code,
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [1.0, 1.0],
                                    [6.0, 1.0],
                                    [6.0, 6.0],
                                    [1.0, 6.0],
                                    [1.0, 1.0],
                                ]
                            ],
                        },
                        "geometry_tile_id": tile["tile_id"],
                        "attributes": [],
                        "confidence": 0.87,
                        "confidence_components": [
                            {
                                "name": "closure",
                                "score": 0.87,
                                "rationale": "The synthetic polygon ring is closed.",
                            }
                        ],
                        "source_references": [source_reference],
                        "evidence_observations": ["A closed synthetic boundary is visible."],
                        "limitations": ["Synthetic test geometry only."],
                        "risk_level": "MEDIUM",
                        "review_status": "AI_DRAFT",
                    }
                ],
                "limitations": ["No live provider was called."],
            }
        else:
            payload = {
                "critiques": [
                    {
                        "feature_id": "synthetic-geology-unit-1",
                        "verdict": "ACCEPT_FOR_VALIDATION",
                        "findings": ["The synthetic proposal is source-linked and valid."],
                        "confidence_components": [
                            {
                                "name": "source_linkage",
                                "score": 0.9,
                                "rationale": "The proposal cites the approved synthetic tile.",
                            }
                        ],
                        "source_references": [source_reference],
                        "limitations": ["Synthetic test critique only."],
                    }
                ],
                "limitations": ["No live provider was called."],
            }
        return ProviderExecutionResult.from_payload(
            provider="openai",
            model=call.model,
            response_id=f"offline-{call.task_type.value}",
            created_at=datetime.now(UTC),
            payload=payload,
            usage=AIUsage(input_tokens=20, output_tokens=10),
        )


class _FailingProvider:
    name = "openai"

    def execute(self, call: ProviderCall) -> ProviderExecutionResult:
        del call
        raise RuntimeError("synthetic provider outage")


def _write_ai_sources(config, *, roots: StorageRoots) -> None:
    workflow = config.ai.phase03_workflow
    assert workflow is not None
    snapshot_root = roots.require_snapshot_root()
    for index, source in enumerate(workflow.configured_sources):
        legend = snapshot_root / source.legend_source
        legend.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(np.full((512, 512, 3), 128 + index, dtype=np.uint8)).save(legend)

        feature = snapshot_root / source.feature_source
        imported = source.feature_source.startswith("phase03-imported-sources/")
        write_target = (
            snapshot_root.parent / "source-fixtures" / source.source_id / feature.name
            if imported
            else feature
        )
        write_target.parent.mkdir(parents=True, exist_ok=True)
        data = np.arange(512 * 512, dtype=np.uint8).reshape(512, 512) + index
        with rasterio.open(
            write_target,
            "w",
            driver="GTiff",
            width=512,
            height=512,
            count=1,
            dtype="uint8",
            crs=config.crs.target_authority,
            transform=from_origin(500_000, 5_200_000, 10, 10),
        ) as dataset:
            dataset.write(data, 1)
        if imported:
            imported_path, _authority = import_phase03_snapshot_source(
                write_target,
                source_id=source.source_id,
                role="georeferenced-map",
                imported_by="Synthetic Test Operator",
                import_reason="Build an immutable synthetic Phase 03 source fixture.",
                roots=roots,
            )
            assert imported_path == feature


def test_ai_first_phase03_attaches_review_outputs_to_exact_pipeline_run(
    raw_archive, monkeypatch, request
) -> None:
    legacy_config, register, _raw_root = raw_archive
    config = load_config(
        legacy_config.base_dir / "config" / "project.yaml",
        ai_config_path=Path("config/ai.openai.yaml"),
    )
    short_base = (
        Path(config.base_dir.anchor) / ".bkt_ai"
        if os.name == "nt"
        else Path(tempfile.gettempdir()) / ".bkt_ai"
    )
    work_root = short_base / f"w-{config.base_dir.name}"
    snapshot_root = short_base / f"s-{config.base_dir.name}"
    output_root = short_base / f"o-{config.base_dir.name}"
    request.addfinalizer(lambda: shutil.rmtree(work_root, ignore_errors=True))
    request.addfinalizer(lambda: shutil.rmtree(snapshot_root, ignore_errors=True))
    request.addfinalizer(lambda: shutil.rmtree(output_root, ignore_errors=True))
    monkeypatch.setenv("BUDUUNKHAD_WORK_ROOT", str(work_root))
    monkeypatch.setenv("BUDUUNKHAD_SNAPSHOT_ROOT", str(snapshot_root))
    monkeypatch.setenv("BUDUUNKHAD_OUTPUT_ROOT", str(output_root))
    roots = StorageRoots.from_environment(
        raw_root=config.raw_root,
        project_root=config.project_root,
    )
    _write_ai_sources(config, roots=roots)
    pipeline_manifest = run_pipeline(config, register, from_="00", to="03")
    assert pipeline_manifest.error == "", repr(pipeline_manifest)
    assert pipeline_manifest.stopped_at == "03"

    existing_runs = {item.name for item in config.runs_root.iterdir() if item.is_dir()}
    workflow = config.ai.phase03_workflow
    assert workflow is not None
    source_id = workflow.configured_sources[0].source_id
    small_tiles = workflow.model_copy(
        update={
            "legend_tile_size": 256,
            "legend_overlap": 0,
            "feature_tile_size": 256,
            "feature_overlap": 0,
        }
    )
    bounded_ai = config.ai.model_copy(
        update={
            "phase03_workflow": small_tiles,
            "max_input_images_per_request": 1,
        }
    )
    bounded_config = config.model_copy(update={"ai": bounded_ai})
    bounded_provider = _Phase03Provider()
    with pytest.raises(Phase03AIFirstError, match="needs 4 images"):
        run_phase03_ai_first(
            bounded_config,
            pipeline_run_id=pipeline_manifest.run_id,
            approved_by="Synthetic Test Approver",
            approval_note="Reject an oversized source before egress.",
            provider=bounded_provider,
            source_id=source_id,
        )
    assert bounded_provider.calls == []
    assert {item.name for item in config.runs_root.iterdir() if item.is_dir()} == existing_runs

    with pytest.raises(LiveExecutionError, match="live provider execution failed"):
        run_phase03_ai_first(
            config,
            pipeline_run_id=pipeline_manifest.run_id,
            approved_by="Synthetic Test Approver",
            approval_note="Offline synthetic failure attempt.",
            provider=_FailingProvider(),
            source_id=source_id,
        )
    failed_attempts = {
        item.name for item in config.runs_root.iterdir() if item.is_dir()
    } - existing_runs
    assert len(failed_attempts) == 1

    provider = _Phase03Provider()
    path, manifest = run_phase03_ai_first(
        config,
        pipeline_run_id=pipeline_manifest.run_id,
        approved_by="Synthetic Test Approver",
        approval_note="Offline synthetic integration test.",
        provider=provider,
        source_id=source_id,
    )

    assert [call.task_type for call in provider.calls] == [
        TaskType.LEGEND_EXTRACTION,
        TaskType.GEOLOGICAL_FEATURE_PROPOSAL,
        TaskType.FEATURE_CRITIQUE,
    ]
    feature_call = provider.calls[1]
    feature_context = json.loads(feature_call.user_prompt.rsplit("REQUEST_CONTEXT_JSON\n", 1)[1])
    feature_parameters = {
        item["name"]: item["value"]
        for item in feature_context["request"]["interpretation_parameters"]
    }
    assert "validated_legend" in feature_parameters
    critique_call = provider.calls[2]
    critique_context = json.loads(critique_call.user_prompt.rsplit("REQUEST_CONTEXT_JSON\n", 1)[1])
    critique_parameters = {
        item["name"]: item["value"]
        for item in critique_context["request"]["interpretation_parameters"]
    }
    assert "validated_feature_proposals" in critique_parameters
    assert manifest.pipeline_run_id == pipeline_manifest.run_id
    assert manifest.ai_run_id != pipeline_manifest.run_id
    assert manifest.ai_run_id not in failed_attempts
    assert tuple(task.task_type for task in manifest.tasks) == (
        "legend_extraction",
        "geological_feature_proposal",
        "feature_critique",
    )
    run_directory = config.runs_root / manifest.ai_run_id
    assert (run_directory / manifest.draft_gpkg_path).is_file()
    assert (run_directory / manifest.draft_qgz_path).is_file()
    assert (run_directory / manifest.review_package_path).is_dir()
    assert (run_directory / manifest.integrated_project_path).is_file()

    assert load_phase03_ai_first_manifest(path, roots=roots) == manifest

    unknown = _Phase03Provider(feature_legend_code="UNLISTED")
    with pytest.raises(Phase03AIFirstError, match="absent from the exact extracted legend"):
        run_phase03_ai_first(
            config,
            pipeline_run_id=pipeline_manifest.run_id,
            approved_by="Synthetic Test Approver",
            approval_note="Offline unknown-legend regression test.",
            provider=unknown,
            source_id=source_id,
        )
    assert [call.task_type for call in unknown.calls] == [
        TaskType.LEGEND_EXTRACTION,
        TaskType.GEOLOGICAL_FEATURE_PROPOSAL,
    ]


def test_ai_first_phase03_batch_keeps_each_source_in_a_separate_attempt(
    raw_archive, monkeypatch, request
) -> None:
    legacy_config, register, _raw_root = raw_archive
    config = load_config(
        legacy_config.base_dir / "config" / "project.yaml",
        ai_config_path=Path("config/ai.openai.yaml"),
    )
    workflow = config.ai.phase03_workflow
    assert workflow is not None
    multi_workflow = workflow.model_copy(
        update={
            "legend_source": None,
            "feature_source": None,
            "sources": (
                AIPhase03SourceConfig(
                    source_id="regional-200k",
                    legend_source="phase03/regional-legend.png",
                    feature_source="phase03/regional-geology.tif",
                ),
                AIPhase03SourceConfig(
                    source_id="local-50k",
                    legend_source="phase03/local-legend.png",
                    feature_source="phase03/local-geology.tif",
                ),
            ),
        }
    )
    bounded_ai = config.ai.model_copy(update={"phase03_workflow": multi_workflow})
    bounded_config = config.model_copy(update={"ai": bounded_ai})
    with pytest.raises(Phase03AIFirstError, match="needs 6 requests"):
        run_phase03_ai_first_batch(
            bounded_config,
            pipeline_run_id="synthetic-pipeline-run",
            approved_by="Synthetic Test Approver",
            approval_note="Bounded batch test.",
            provider=_Phase03Provider(),
        )

    ai = bounded_ai.model_copy(update={"max_requests_per_run": 6, "max_cost_per_run_usd": "30.00"})
    config = config.model_copy(update={"ai": ai})
    short_base = (
        Path(config.base_dir.anchor) / ".bkt_ai_batch"
        if os.name == "nt"
        else Path(tempfile.gettempdir()) / ".bkt_ai_batch"
    )
    work_root = short_base / f"w-{config.base_dir.name}"
    snapshot_root = short_base / f"s-{config.base_dir.name}"
    output_root = short_base / f"o-{config.base_dir.name}"
    request.addfinalizer(lambda: shutil.rmtree(work_root, ignore_errors=True))
    request.addfinalizer(lambda: shutil.rmtree(snapshot_root, ignore_errors=True))
    request.addfinalizer(lambda: shutil.rmtree(output_root, ignore_errors=True))
    monkeypatch.setenv("BUDUUNKHAD_WORK_ROOT", str(work_root))
    monkeypatch.setenv("BUDUUNKHAD_SNAPSHOT_ROOT", str(snapshot_root))
    monkeypatch.setenv("BUDUUNKHAD_OUTPUT_ROOT", str(output_root))
    roots = StorageRoots.from_environment(
        raw_root=config.raw_root,
        project_root=config.project_root,
    )
    _write_ai_sources(config, roots=roots)
    pipeline_manifest = run_pipeline(config, register, from_="00", to="03")
    assert pipeline_manifest.error == ""

    rejected_provider = _Phase03Provider()
    with pytest.raises(Phase03AIFirstError, match="must differ"):
        run_phase03_ai_first_batch(
            config,
            pipeline_run_id=pipeline_manifest.run_id,
            batch_run_id=pipeline_manifest.run_id,
            approved_by="Synthetic Test Approver",
            approval_note="Reject a colliding batch identity before egress.",
            provider=rejected_provider,
        )
    assert rejected_provider.calls == []

    provider = _Phase03Provider()
    path, batch = run_phase03_ai_first_batch(
        config,
        pipeline_run_id=pipeline_manifest.run_id,
        approved_by="Synthetic Test Approver",
        approval_note="Offline multi-source integration test.",
        provider=provider,
    )

    assert len(provider.calls) == 6
    assert tuple(item.source_id for item in batch.sessions) == (
        "regional-200k",
        "local-50k",
    )
    assert len({item.ai_run_id for item in batch.sessions}) == 2
    assert all((config.runs_root / item.review_package_path).is_dir() for item in batch.sessions)
    assert load_phase03_ai_batch_manifest(path, roots=roots) == batch
