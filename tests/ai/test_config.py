import hashlib
import json
from decimal import Decimal
from pathlib import Path

import pytest
from pydantic import ValidationError

from buduunkhad.config import (
    AIConfig,
    AIPhase03SourceConfig,
    AIPhase03WorkflowConfig,
    AIProviderSelection,
    ExecutionProfile,
    ProjectConfig,
    ReasoningEffort,
    ReasoningMode,
    TextVerbosity,
    load_ai_config,
    load_config,
)


def test_unchanged_project_yaml_loads_with_offline_legacy_defaults() -> None:
    config = load_config(Path("config/project.yaml"))
    assert config.ai.profile is ExecutionProfile.LEGACY
    assert config.ai.enabled is False
    assert config.ai.provider is AIProviderSelection.DISABLED
    assert config.ai.reasoning_effort is None
    assert config.ai.external_data_allowed is False
    assert config.ai.max_cost_per_run_usd == Decimal("0")
    assert config.ai.max_requests_per_run == 1
    assert config.ai.max_input_images_per_request == 32
    assert config.ai.max_input_bytes_per_request == 100_000_000
    assert config.ai.max_output_tokens == 4096
    assert config.ai.concurrency == 1


def test_standalone_openai_profile_is_explicit_and_does_not_change_default() -> None:
    ai = load_ai_config(Path("config/ai.openai.yaml"))
    config = load_config(
        Path("config/project.yaml"),
        ai_config_path=Path("config/ai.openai.yaml"),
    )

    assert ai.profile is ExecutionProfile.AI_FIRST
    assert ai.enabled is True
    assert ai.provider is AIProviderSelection.OPENAI
    assert ai.provider_model == "gpt-5.6-terra"
    assert ai.reasoning_effort is ReasoningEffort.MAX
    assert ai.reasoning_mode is ReasoningMode.PRO
    assert ai.text_verbosity is TextVerbosity.MEDIUM
    assert ai.store_responses is False
    assert ai.external_data_allowed is True
    assert ai.request_timeout_seconds == 3600
    assert ai.max_output_tokens == 32768
    assert ai.max_requests_per_run == 4
    assert ai.max_input_images_per_request == 24
    assert ai.max_input_bytes_per_request == 100_000_000
    assert ai.max_cost_per_run_usd == Decimal("20.00")
    assert ai.phase03_workflow is not None
    assert ai.phase03_workflow.legend_tile_size == 4096
    assert ai.phase03_workflow.feature_tile_size == 1536
    assert ai.phase03_workflow.critique_estimated_cost_usd == Decimal("4.00")
    assert tuple(item.source_id for item in ai.phase03_workflow.configured_sources) == (
        "regional-geology-1987-200k",
        "detailed-geology-2013-50k",
        "regional-metallogeny-2020-500k",
        "mineral-distribution-2013-100k",
        "prospectivity-2013-50k",
        "source-materials-2013-50k",
    )
    assert config.ai == ai
    assert load_config(Path("config/project.yaml")).ai.profile is ExecutionProfile.LEGACY


def test_phase03_ai_workflow_supports_explicit_unique_source_batches() -> None:
    workflow = AIPhase03WorkflowConfig(
        sources=(
            AIPhase03SourceConfig(
                source_id="regional-200k",
                legend_source="phase03/legend-200k.png",
                feature_source="phase03/geology-200k.tif",
            ),
            AIPhase03SourceConfig(
                source_id="local-50k",
                legend_source="phase03/legend-50k.png",
                feature_source="phase03/geology-50k.tif",
            ),
        )
    )

    assert tuple(item.source_id for item in workflow.configured_sources) == (
        "regional-200k",
        "local-50k",
    )
    assert workflow.source("local-50k").feature_source.endswith("geology-50k.tif")
    with pytest.raises(ValueError, match="explicit source ID"):
        workflow.source()

    with pytest.raises(ValidationError, match="source IDs must be unique"):
        AIPhase03WorkflowConfig(
            sources=(
                AIPhase03SourceConfig(
                    source_id="duplicate",
                    legend_source="phase03/legend-a.png",
                    feature_source="phase03/map-a.tif",
                ),
                AIPhase03SourceConfig(
                    source_id="duplicate",
                    legend_source="phase03/legend-b.png",
                    feature_source="phase03/map-b.tif",
                ),
            )
        )


def test_standalone_ai_profile_rejects_project_fields_and_credentials(tmp_path: Path) -> None:
    invalid = tmp_path / "ai.yaml"
    invalid.write_text(
        "ai:\n"
        "  profile: ai-first\n"
        "  enabled: true\n"
        "  provider: openai\n"
        "  provider_model: synthetic-model\n"
        "  reasoning_effort: high\n"
        "  external_data_allowed: true\n"
        "  source_egress_policy: require-explicit-approval\n"
        "project:\n"
        "  name: forbidden\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="exactly one top-level"):
        load_ai_config(invalid)

    invalid.write_text("ai:\n  embedded_credential: placeholder\n", encoding="utf-8")
    with pytest.raises(ValidationError, match="Extra inputs"):
        load_ai_config(invalid)


def test_legacy_serialization_shape_excludes_ai_by_default() -> None:
    config = load_config(Path("config/project.yaml"))
    snapshot_path = Path("tests/fixtures/legacy_project_config.json")
    expected = json.loads(snapshot_path.read_text(encoding="utf-8"))
    python_dump = _normalize_legacy_dump(config.model_dump())
    json_dump = _normalize_legacy_dump(json.loads(config.model_dump_json()))
    assert python_dump == expected
    assert json_dump == expected
    exact_snapshot = (
        Path("tests/fixtures/legacy_project_config_dump.json").read_text(encoding="utf-8").strip()
    )
    normalized_json_text = json.dumps(
        json_dump,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    assert normalized_json_text == exact_snapshot
    ai_v1 = config.model_dump(context={"config_serialization_version": "ai-v1"})
    assert ai_v1["ai"]["profile"] == "legacy"


def test_project_yaml_bytes_remain_at_the_legacy_baseline() -> None:
    content = Path("config/project.yaml").read_bytes()
    assert hashlib.sha256(content).hexdigest() == (
        "7d4796c895db32e1f3e5e637379dc0126673e4e0fd4595372ad02c4cd9200296"
    )


def test_hybrid_configuration_is_optional_and_typed() -> None:
    config = load_config(Path("config/project.yaml"))
    hybrid = config.ai.model_copy(
        update={
            "profile": ExecutionProfile.HYBRID,
            "enabled": True,
            "provider": AIProviderSelection.OPENAI,
            "provider_model": "synthetic-model",
            "reasoning_effort": ReasoningEffort.HIGH,
            "external_data_allowed": True,
            "source_egress_policy": "require-explicit-approval",
            "max_cost_per_run_usd": Decimal("1"),
        }
    )
    assert hybrid.profile is ExecutionProfile.HYBRID
    assert hybrid.external_data_allowed is True
    assert hybrid.provider is AIProviderSelection.OPENAI
    assert hybrid.reasoning_effort is ReasoningEffort.HIGH


def test_enabled_openai_requires_explicit_reasoning_effort() -> None:
    with pytest.raises(ValidationError, match="explicit reasoning_effort"):
        AIConfig(
            profile=ExecutionProfile.HYBRID,
            enabled=True,
            provider=AIProviderSelection.OPENAI,
            provider_model="synthetic-model",
            external_data_allowed=True,
            source_egress_policy="require-explicit-approval",
            max_cost_per_run_usd=Decimal("1"),
        )


def test_ai_config_copy_and_reload_paths_revalidate_security_fields() -> None:
    ai = load_config(Path("config/project.yaml")).ai
    for operation in (
        lambda: ai.model_copy(update={"concurrency": 0}),
        lambda: ai.copy(update={"concurrency": 0}),
        lambda: type(ai).model_validate(ai.model_dump() | {"concurrency": 0}),
        lambda: type(ai).model_validate_json(
            json.dumps(ai.model_dump(mode="json") | {"concurrency": 0})
        ),
    ):
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            operation()


@pytest.mark.parametrize(
    ("update", "message"),
    [
        ({"enabled": True}, "legacy execution"),
        ({"external_data_allowed": True}, "legacy execution"),
        ({"provider": AIProviderSelection.OPENAI}, "legacy execution"),
        (
            {
                "review_policy": {
                    "require_named_reviewer": False,
                    "high_risk_requires_geologist": True,
                    "production_geometry_requires_approval": True,
                }
            },
            "safeguards",
        ),
    ],
)
def test_project_config_revalidates_security_sensitive_ai_updates_on_every_public_path(
    update: dict[str, object],
    message: str,
) -> None:
    config = load_config(Path("config/project.yaml"))
    ai_values = config.ai.model_dump(mode="python") | update
    project_values = config.model_dump(
        mode="python", context={"config_serialization_version": "ai-v1"}
    )
    project_values["ai"] = ai_values
    json_values = config.model_dump(mode="json", context={"config_serialization_version": "ai-v1"})
    json_values["ai"] = AIConfig.model_validate(config.ai).model_dump(mode="json") | update
    operations = (
        lambda: config.model_copy(update={"ai": ai_values}),
        lambda: config.copy(update={"ai": ai_values}),
        lambda: ProjectConfig.model_validate(project_values),
        lambda: ProjectConfig.model_validate_json(json.dumps(json_values)),
    )
    for operation in operations:
        with pytest.raises(ValidationError, match=message):
            operation()


def test_project_config_unvalidated_construction_apis_fail_explicitly() -> None:
    with pytest.raises(TypeError, match="model_construct"):
        ProjectConfig.model_construct()
    with pytest.raises(TypeError, match="construct"):
        ProjectConfig.construct()


def test_project_config_revalidates_tampered_existing_nested_ai_instance() -> None:
    config = load_config(Path("config/project.yaml")).model_copy()
    tampered_ai = config.ai.model_copy()
    object.__setattr__(tampered_ai, "external_data_allowed", True)
    object.__setattr__(config, "ai", tampered_ai)
    with pytest.raises(ValidationError, match="legacy execution"):
        ProjectConfig.model_validate(config)


def test_only_live_provider_choices_are_user_configurable() -> None:
    assert {item.value for item in AIProviderSelection} == {
        "disabled",
        "openai",
        "anthropic",
    }


def test_unknown_ai_serialization_version_fails() -> None:
    config = load_config(Path("config/project.yaml"))
    with pytest.raises(ValueError, match="unsupported config serialization version"):
        config.model_dump(context={"config_serialization_version": "ai-v2"})


def _normalize_legacy_dump(value: object) -> object:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, dict):
        result = {key: _normalize_legacy_dump(item) for key, item in value.items()}
        if "base_dir" in result:
            result["base_dir"] = "__REPOSITORY_ROOT__"
        return result
    if isinstance(value, list):
        return [_normalize_legacy_dump(item) for item in value]
    if isinstance(value, str):
        return value.replace("\\", "/")
    return value
