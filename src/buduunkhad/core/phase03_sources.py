"""Exact Phase 03 source traceability over sealed Phase 00 working copies."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from buduunkhad.ai.fingerprint import sha256_value
from buduunkhad.config import InputRecord
from buduunkhad.core.run_artifacts import (
    ArtifactSealError,
    require_regular_file_under,
    sha256_file,
)

PHASE03_SOURCE_TRACE_FORMAT_VERSION = "1.0.0"
PHASE03_SOURCE_TRACE_COMPONENT = "buduunkhad.phase03.source-traceability-v1"
PHASE03_INPUT_NUMBERS = (*range(1, 9), *range(53, 73))

Sha256 = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
NonEmpty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Phase03SourceTraceError(RuntimeError):
    """The exact Phase 03 source set cannot be established safely."""


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, revalidate_instances="always")

    @classmethod
    def model_construct(
        cls,
        _fields_set: set[str] | None = None,
        **values: object,
    ) -> Self:
        del _fields_set, values
        raise TypeError("model_construct is unsupported; use validated construction")


class Phase03SourceBinding(_StrictModel):
    input_no: int = Field(ge=1)
    evidence_group: NonEmpty
    filename: NonEmpty
    file_type: NonEmpty
    methodology_action: str
    source_phase_id: Literal["00"] = "00"
    source_run_id: NonEmpty
    source_relative_path: NonEmpty
    source_sha256: Sha256
    source_size_bytes: int = Field(ge=0)

    @model_validator(mode="after")
    def _portable_identity(self) -> Phase03SourceBinding:
        path = Path(self.source_relative_path)
        if path.is_absolute() or "\\" in self.source_relative_path or ".." in path.parts:
            raise ValueError("Phase 03 source paths must be portable and relative")
        if path.as_posix() != self.source_relative_path:
            raise ValueError("Phase 03 source paths must use canonical POSIX separators")
        return self


class _Phase03SourceTraceIdentity(_StrictModel):
    format_version: Literal["1.0.0"] = PHASE03_SOURCE_TRACE_FORMAT_VERSION
    phase03_run_id: NonEmpty
    phase00_source_run_id: NonEmpty
    records: tuple[Phase03SourceBinding, ...] = Field(min_length=len(PHASE03_INPUT_NUMBERS))
    component: Literal["buduunkhad.phase03.source-traceability-v1"] = PHASE03_SOURCE_TRACE_COMPONENT

    @model_validator(mode="after")
    def _exact_registered_set(self) -> _Phase03SourceTraceIdentity:
        numbers = tuple(item.input_no for item in self.records)
        if numbers != PHASE03_INPUT_NUMBERS:
            raise ValueError("Phase 03 traceability must bind exact inputs 1-8 and 53-72")
        if any(item.source_run_id != self.phase00_source_run_id for item in self.records):
            raise ValueError("Phase 03 source records must bind one exact Phase 00 source run")
        return self


class Phase03SourceTraceability(_Phase03SourceTraceIdentity):
    traceability_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> Phase03SourceTraceability:
        identity = _Phase03SourceTraceIdentity.model_validate(
            self.model_dump(mode="python", exclude={"traceability_id"})
        )
        if self.traceability_id != sha256_value(identity):
            raise ValueError("Phase 03 source-traceability identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> Phase03SourceTraceability:
        identity = _Phase03SourceTraceIdentity.model_validate(values)
        return cls(
            **identity.model_dump(mode="python"),
            traceability_id=sha256_value(identity),
        )


def create_phase03_source_traceability(
    *,
    phase03_run_id: str,
    phase00_source_run_id: str,
    phase00_root: Path,
    records: list[InputRecord] | tuple[InputRecord, ...],
) -> Phase03SourceTraceability:
    """Bind the methodology's exact source set to immutable Phase 00 bytes."""

    by_number = {record.no: record for record in records}
    if set(by_number) != set(PHASE03_INPUT_NUMBERS) or len(by_number) != len(records):
        raise Phase03SourceTraceError("Phase 03 source records are incomplete or duplicated")
    root = Path(phase00_root).absolute().resolve()
    bindings: list[Phase03SourceBinding] = []
    for input_no in PHASE03_INPUT_NUMBERS:
        record = by_number[input_no]
        relative = Path(record.evidence_group) / record.filename
        try:
            source = require_regular_file_under(
                root,
                root / relative,
                description=f"Phase 03 input #{input_no}",
            )
        except (ArtifactSealError, OSError, ValueError) as exc:
            raise Phase03SourceTraceError(
                f"Phase 03 input #{input_no} is missing or unsafe: {record.filename}"
            ) from exc
        bindings.append(
            Phase03SourceBinding(
                input_no=input_no,
                evidence_group=record.evidence_group,
                filename=record.filename,
                file_type=record.file_type,
                methodology_action=record.methodology_action,
                source_run_id=phase00_source_run_id,
                source_relative_path=relative.as_posix(),
                source_sha256=sha256_file(source),
                source_size_bytes=source.stat().st_size,
            )
        )
    return Phase03SourceTraceability.create(
        phase03_run_id=phase03_run_id,
        phase00_source_run_id=phase00_source_run_id,
        records=tuple(bindings),
    )


def write_phase03_source_traceability(
    record: Phase03SourceTraceability,
    path: Path,
) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = record.model_dump_json(indent=2) + "\n"
    if target.exists() and target.read_text(encoding="utf-8") != payload:
        raise Phase03SourceTraceError("Phase 03 source-traceability record already differs")
    target.write_text(payload, encoding="utf-8", newline="\n")
    return target


def load_phase03_source_traceability(path: Path) -> Phase03SourceTraceability:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        return Phase03SourceTraceability.model_validate(data)
    except (OSError, UnicodeError, ValueError) as exc:
        raise Phase03SourceTraceError("Phase 03 source-traceability record is invalid") from exc


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result
