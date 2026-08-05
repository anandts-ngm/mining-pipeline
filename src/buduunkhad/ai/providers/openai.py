"""Optional OpenAI vision adapter with lazy SDK and credential loading."""

from __future__ import annotations

import base64
import importlib
import os
from datetime import UTC, datetime
from typing import Protocol, cast

from buduunkhad.ai.contracts import AIUsage
from buduunkhad.ai.providers.base import (
    AIProviderError,
    ProviderCall,
    ProviderCredentialError,
    ProviderDependencyError,
    ProviderExecutionResult,
    ProviderResponseError,
    decode_provider_json,
    provider_execution_error,
)


class OpenAIProvider:
    """Execute an approved request through the optional OpenAI Responses client.

    ``client`` is intentionally injectable so unit tests exercise the complete
    serialization boundary without constructing an SDK client or opening a socket.
    """

    def __init__(self, *, client: object | None = None) -> None:
        self._injected_client = client

    @property
    def name(self) -> str:
        return "openai"

    def execute(self, call: ProviderCall) -> ProviderExecutionResult:
        if call.provider != self.name:
            raise AIProviderError("prepared request provider does not match OpenAI")
        client = cast(
            _OpenAIClient,
            self._injected_client
            if self._injected_client is not None
            else _create_client(call.timeout_seconds),
        )
        content: list[dict[str, object]] = [{"type": "input_text", "text": call.user_prompt}]
        for image in call.images:
            encoded = base64.b64encode(image.data).decode("ascii")
            content.append(
                {
                    "type": "input_text",
                    "text": f"Approved tile {image.tile_id}; image SHA-256 {image.sha256}",
                }
            )
            content.append(
                {
                    "type": "input_image",
                    "image_url": f"data:{image.media_type};base64,{encoded}",
                    "detail": image.detail,
                }
            )
        try:
            reasoning = {
                key: value
                for key, value in (
                    ("effort", call.reasoning_effort),
                    ("mode", call.reasoning_mode),
                )
                if value is not None
            }
            text = {
                "format": {
                    "type": "json_schema",
                    "name": "buduunkhad_geospatial_output",
                    "schema": _strict_output_schema(call.output_schema.to_python()),
                    "strict": True,
                },
                **({"verbosity": call.text_verbosity} if call.text_verbosity is not None else {}),
            }
            response = client.responses.create(
                model=call.model,
                instructions=call.system_prompt,
                input=[{"role": "user", "content": content}],
                text=text,
                max_output_tokens=call.max_output_tokens,
                timeout=call.timeout_seconds,
                **({"reasoning": reasoning} if reasoning else {}),
                **({"store": call.store_response} if call.store_response is not None else {}),
            )
        except Exception as exc:
            raise provider_execution_error(
                "openai",
                exc,
                sensitive_values=(os.environ.get("OPENAI_API_KEY"),),
            ) from None
        response_id = getattr(response, "id", None)
        if not isinstance(response_id, str) or not response_id.strip():
            raise ProviderResponseError("OpenAI response did not contain a response ID")
        output_text = _output_text(response)
        usage = _usage(response)
        return ProviderExecutionResult.from_payload(
            provider="openai",
            model=call.model,
            response_id=response_id,
            created_at=datetime.now(UTC),
            payload=decode_provider_json(output_text),
            usage=usage,
        )


def _create_client(timeout_seconds: float) -> object:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ProviderCredentialError(
            "OPENAI_API_KEY is required only for the optional ai execute command"
        )
    try:
        module = importlib.import_module("openai")
        client_class = module.OpenAI
    except (ImportError, AttributeError) as exc:
        raise ProviderDependencyError(
            "OpenAI execution requires the optional 'openai' project extra"
        ) from exc
    try:
        return client_class(api_key=api_key, timeout=timeout_seconds)
    except Exception as exc:
        raise provider_execution_error(
            "openai",
            exc,
            sensitive_values=(api_key,),
        ) from None


def _usage(response: object) -> AIUsage:
    value = getattr(response, "usage", None)
    input_tokens = getattr(value, "input_tokens", 0) if value is not None else 0
    output_tokens = getattr(value, "output_tokens", 0) if value is not None else 0
    input_details = getattr(value, "input_tokens_details", None) if value is not None else None
    output_details = getattr(value, "output_tokens_details", None) if value is not None else None
    cached_input_tokens = (
        getattr(input_details, "cached_tokens", 0) if input_details is not None else 0
    )
    reasoning_output_tokens = (
        getattr(output_details, "reasoning_tokens", 0) if output_details is not None else 0
    )
    if not all(
        isinstance(item, int)
        for item in (
            input_tokens,
            cached_input_tokens,
            output_tokens,
            reasoning_output_tokens,
        )
    ):
        raise ProviderResponseError("OpenAI response usage is malformed")
    return AIUsage(
        input_tokens=input_tokens,
        cached_input_tokens=cached_input_tokens,
        output_tokens=output_tokens,
        reasoning_output_tokens=reasoning_output_tokens,
        requests=1,
    )


def _output_text(response: object) -> str:
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text
    if getattr(response, "status", None) == "incomplete":
        detail = getattr(response, "incomplete_details", None)
        reason = getattr(detail, "reason", None)
        allowed = {"content_filter", "max_output_tokens"}
        if reason in allowed:
            raise ProviderResponseError(f"OpenAI response was incomplete ({reason})")
        raise ProviderResponseError("OpenAI response was incomplete")
    raise ProviderResponseError("OpenAI response did not contain structured output text")


def _strict_output_schema(value: object) -> dict[str, object]:
    schema = _normalise_schema_node(value)
    if not isinstance(schema, dict):
        raise AIProviderError("OpenAI output schema root must be an object")
    if schema.get("type") != "object":
        raise AIProviderError("OpenAI output schema root must have object type")
    return cast(dict[str, object], schema)


def _normalise_schema_node(value: object) -> object:
    if isinstance(value, list):
        return [_normalise_schema_node(item) for item in value]
    if not isinstance(value, dict):
        return value

    result: dict[str, object] = {}
    discriminator = value.get("discriminator")
    for raw_key, item in value.items():
        if not isinstance(raw_key, str):
            raise AIProviderError("OpenAI output schema keys must be strings")
        key = raw_key
        if key in {"default", "discriminator", "prefixItems"}:
            continue
        if key == "oneOf" and discriminator is not None:
            result["anyOf"] = _normalise_schema_node(item)
            continue
        result[key] = _normalise_schema_node(item)

    prefix_items = value.get("prefixItems")
    if prefix_items is not None:
        normalised_items = _normalise_schema_node(prefix_items)
        if (
            not isinstance(normalised_items, list)
            or not normalised_items
            or any(item != normalised_items[0] for item in normalised_items[1:])
        ):
            raise AIProviderError(
                "OpenAI strict schema cannot represent a heterogeneous fixed-length tuple"
            )
        result["items"] = normalised_items[0]

    properties = result.get("properties")
    if isinstance(properties, dict):
        result["required"] = list(properties)
        result["additionalProperties"] = False
    return result


class _ResponsesEndpoint(Protocol):
    def create(self, **kwargs: object) -> object: ...


class _OpenAIClient(Protocol):
    responses: _ResponsesEndpoint
