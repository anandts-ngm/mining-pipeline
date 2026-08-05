"""Strict loading for machine-local CLI environment values."""

from __future__ import annotations

import os
import re
from pathlib import Path

_ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_MAX_ENV_BYTES = 64 * 1024
_ALLOWED_NAMES = frozenset({"OPENAI_API_KEY", "ANTHROPIC_API_KEY"})


class LocalEnvError(RuntimeError):
    """A machine-local environment file is unsafe or malformed."""


def load_repository_env(config_path: Path | str) -> Path | None:
    """Load ``<project-root>/.env`` without evaluating or overriding process state."""

    config = Path(config_path).expanduser().resolve(strict=True)
    path = config.parent.parent / ".env"
    if not path.exists():
        return None
    if path.is_symlink() or not path.is_file():
        raise LocalEnvError("repository .env must be a regular, non-symlink file")
    try:
        if path.stat().st_size > _MAX_ENV_BYTES:
            raise LocalEnvError("repository .env exceeds the 64 KiB safety limit")
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise LocalEnvError("repository .env cannot be read safely") from exc

    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        name, separator, raw_value = line.partition("=")
        name = name.strip()
        if separator != "=" or not _ENV_NAME.fullmatch(name):
            raise LocalEnvError(f"repository .env line {line_number} is malformed")
        if name not in _ALLOWED_NAMES:
            raise LocalEnvError(
                f"repository .env variable {name} is unsupported; only provider credentials belong here"
            )
        if name in values:
            raise LocalEnvError(f"repository .env repeats {name}")
        values[name] = _parse_value(raw_value, line_number=line_number)

    _validate_provider_keys(values)
    for name, value in values.items():
        if name not in os.environ and value:
            os.environ[name] = value
    return path


def _parse_value(raw_value: str, *, line_number: int) -> str:
    value = raw_value.strip()
    if not value:
        return ""
    if value[0] in {'"', "'"}:
        if len(value) < 2 or value[-1] != value[0]:
            raise LocalEnvError(f"repository .env line {line_number} has unmatched quotes")
        return value[1:-1]
    if any(character.isspace() for character in value):
        raise LocalEnvError(f"repository .env line {line_number} has an unquoted whitespace value")
    return value


def _validate_provider_keys(values: dict[str, str]) -> None:
    openai_key = values.get("OPENAI_API_KEY")
    if openai_key and (
        not openai_key.startswith("sk-") or any(character.isspace() for character in openai_key)
    ):
        raise LocalEnvError("OPENAI_API_KEY in repository .env is malformed")
    anthropic_key = values.get("ANTHROPIC_API_KEY")
    if anthropic_key and any(character.isspace() for character in anthropic_key):
        raise LocalEnvError("ANTHROPIC_API_KEY in repository .env is malformed")
