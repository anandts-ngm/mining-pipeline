from __future__ import annotations

import os
from pathlib import Path

import pytest

from buduunkhad.runtime_env import LocalEnvError, load_repository_env

_OPENAI_KEY_NAME = "OPENAI_" + "API_KEY"
_FILE_KEY = "sk-" + "project-file-" + "value"
_PROCESS_KEY = "sk-" + "explicit-process-" + "value"


def _config(tmp_path: Path) -> Path:
    path = tmp_path / "config" / "project.yaml"
    path.parent.mkdir()
    path.write_text("project: synthetic\n", encoding="utf-8")
    return path


def test_missing_repository_env_is_a_noop(tmp_path: Path) -> None:
    assert load_repository_env(_config(tmp_path)) is None


def test_repository_env_loads_key_without_overriding_process_value(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _config(tmp_path)
    (tmp_path / ".env").write_text(
        f"{_OPENAI_KEY_NAME}={_FILE_KEY}\nBUDUUNKHAD_AI_EGRESS_APPROVER='Anand Tsogtjargal'\n",
        encoding="utf-8",
    )
    monkeypatch.delenv(_OPENAI_KEY_NAME, raising=False)
    monkeypatch.delenv("BUDUUNKHAD_AI_EGRESS_APPROVER", raising=False)

    assert load_repository_env(config) == tmp_path / ".env"
    assert os.environ[_OPENAI_KEY_NAME] == _FILE_KEY
    assert os.environ["BUDUUNKHAD_AI_EGRESS_APPROVER"] == "Anand Tsogtjargal"

    monkeypatch.setenv(_OPENAI_KEY_NAME, _PROCESS_KEY)
    load_repository_env(config)
    assert os.environ[_OPENAI_KEY_NAME] == _PROCESS_KEY


@pytest.mark.parametrize(
    "content",
    [
        f"{_OPENAI_KEY_NAME}=SetEnvironmentVariable(Get-Clipboard)\n",
        f"{_OPENAI_KEY_NAME}=not-a-key\n",
        f"{_OPENAI_KEY_NAME}='unterminated\n",
        f"{_OPENAI_KEY_NAME}=sk-one\n{_OPENAI_KEY_NAME}=sk-two\n",
    ],
)
def test_repository_env_rejects_malformed_values(tmp_path: Path, content: str) -> None:
    config = _config(tmp_path)
    (tmp_path / ".env").write_text(content, encoding="utf-8")
    with pytest.raises(LocalEnvError):
        load_repository_env(config)
