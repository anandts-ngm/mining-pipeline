"""Immutable snapshot inventory creation and verification."""

from __future__ import annotations

import json
import math
import os
import re
import shutil
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from buduunkhad.ai.contracts import require_aware_datetime
from buduunkhad.ai.fingerprint import sha256_file, sha256_value
from buduunkhad.core.run_artifacts import has_symlink_component
from buduunkhad.geospatial_ai.path_safety import PathSafetyError, StorageRoots

SourceRootId = Literal["raw", "snapshot"]
SnapshotImportRole = Literal["legend", "georeferenced-map"]
_SIDECARS = (".tfw", ".jgw", ".pgw", ".wld", ".aux.xml", ".ovr", ".rpc", ".eph")
_IMPORT_DIRECTORY = "phase03-imported-sources"
_IMPORT_AUTHORITY = "snapshot-import.json"
_LEGEND_SUFFIXES = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".pdf"}
_MAP_SUFFIXES = {".tif", ".tiff"}
Sha256 = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
NonEmpty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class SnapshotEntry(BaseModel):
    model_config = ConfigDict(frozen=True)

    relative_path: str
    size: int = Field(ge=0)
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    bundle_parent: str | None = None
    sidecar_kind: str | None = None


class SnapshotManifest(BaseModel):
    model_config = ConfigDict(frozen=True)

    format_version: Literal["1.0.0"] = "1.0.0"
    source_root_id: SourceRootId
    created_at: datetime
    entries: tuple[SnapshotEntry, ...]

    @field_validator("created_at")
    @classmethod
    def _aware_creation_time(cls, value: datetime) -> datetime:
        return require_aware_datetime(value, "created_at")


class SnapshotVerification(BaseModel):
    model_config = ConfigDict(frozen=True)

    valid: bool
    missing: tuple[str, ...]
    changed: tuple[str, ...]
    unexpected: tuple[str, ...]


class SnapshotImportFile(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    relative_path: NonEmpty
    sha256: Sha256
    size_bytes: int = Field(ge=0)

    @field_validator("relative_path")
    @classmethod
    def _portable_path(cls, value: str) -> str:
        path = Path(value)
        if path.is_absolute() or "\\" in value or ".." in path.parts:
            raise ValueError("snapshot import paths must be portable and relative")
        return path.as_posix()


class _SnapshotImportIdentity(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    format_version: Literal["1.0.0"] = "1.0.0"
    source_id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,63}$")
    role: SnapshotImportRole
    created_at: datetime
    imported_by: NonEmpty
    import_reason: NonEmpty
    original_filename: NonEmpty
    original_sha256: Sha256
    original_size_bytes: int = Field(ge=1)
    files: tuple[SnapshotImportFile, ...] = Field(min_length=1)
    primary_relative_path: NonEmpty
    raster_crs: NonEmpty | None = None
    raster_width: int | None = Field(default=None, ge=1)
    raster_height: int | None = Field(default=None, ge=1)
    raster_band_count: int | None = Field(default=None, ge=1)

    @field_validator("created_at")
    @classmethod
    def _aware_creation_time(cls, value: datetime) -> datetime:
        return require_aware_datetime(value, "created_at")

    @field_validator("primary_relative_path")
    @classmethod
    def _portable_primary_path(cls, value: str) -> str:
        path = Path(value)
        if path.is_absolute() or "\\" in value or ".." in path.parts:
            raise ValueError("snapshot import primary path must be portable and relative")
        return path.as_posix()

    @model_validator(mode="after")
    def _coherent_import(self) -> _SnapshotImportIdentity:
        prefix = f"{_IMPORT_DIRECTORY}/{self.source_id}/"
        paths = tuple(item.relative_path for item in self.files)
        if paths != tuple(sorted(paths)) or len(paths) != len(set(paths)):
            raise ValueError("snapshot import files must be unique and sorted")
        if any(not path.startswith(prefix) for path in paths):
            raise ValueError("snapshot import file path does not match its source identity")
        if self.primary_relative_path not in paths:
            raise ValueError("snapshot import primary file is absent from its file inventory")
        raster_values = (
            self.raster_crs,
            self.raster_width,
            self.raster_height,
            self.raster_band_count,
        )
        if self.role == "georeferenced-map" and any(value is None for value in raster_values):
            raise ValueError("georeferenced map imports require complete raster metadata")
        if self.role == "legend" and any(value is not None for value in raster_values):
            raise ValueError("legend imports must not claim georeferencing metadata")
        return self


class SnapshotImportAuthority(_SnapshotImportIdentity):
    authority_id: Sha256

    @model_validator(mode="after")
    def _sealed_identity(self) -> SnapshotImportAuthority:
        identity = _SnapshotImportIdentity.model_validate(
            self.model_dump(mode="python", exclude={"authority_id"})
        )
        if self.authority_id != sha256_value(identity):
            raise ValueError("snapshot import identity is invalid")
        return self

    @classmethod
    def create(cls, **values: object) -> SnapshotImportAuthority:
        identity = _SnapshotImportIdentity.model_validate(values)
        return cls(**identity.model_dump(mode="python"), authority_id=sha256_value(identity))


def import_phase03_snapshot_source(
    source_path: Path,
    *,
    source_id: str,
    role: SnapshotImportRole,
    imported_by: str,
    import_reason: str,
    roots: StorageRoots,
    now: datetime | None = None,
) -> tuple[Path, SnapshotImportAuthority]:
    """Copy one exact local source into the immutable Phase 03 snapshot namespace."""

    if re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", source_id) is None:
        raise PathSafetyError("Phase 03 snapshot source ID is invalid")
    if not imported_by.strip() or not import_reason.strip():
        raise PathSafetyError("snapshot import requires a named actor and non-empty reason")
    source = Path(source_path).absolute()
    if has_symlink_component(source) or not source.is_file():
        raise PathSafetyError("Phase 03 snapshot source must be a regular non-symlink file")
    snapshot_root = roots.require_snapshot_root()
    source_resolved = source.resolve(strict=True)
    if source_resolved == snapshot_root or snapshot_root in source_resolved.parents:
        raise PathSafetyError("Phase 03 snapshot import source must be outside the snapshot root")
    suffix = source.suffix.casefold()
    allowed = _MAP_SUFFIXES if role == "georeferenced-map" else _LEGEND_SUFFIXES
    if suffix not in allowed:
        raise PathSafetyError(f"unsupported {role} snapshot source suffix: {source.suffix}")

    destination = snapshot_root / _IMPORT_DIRECTORY / source_id
    temporary = destination.parent / f".{source_id}.{uuid.uuid4().hex}.tmp"
    primary_relative = (Path(_IMPORT_DIRECTORY) / source_id / "source" / source.name).as_posix()
    source_hash = sha256_file(source)
    source_size = source.stat().st_size
    if destination.exists():
        authority = load_snapshot_import_authority(destination / _IMPORT_AUTHORITY, roots=roots)
        if (
            authority.source_id != source_id
            or authority.role != role
            or authority.original_filename != source.name
            or authority.original_sha256 != source_hash
            or authority.original_size_bytes != source_size
        ):
            raise PathSafetyError("snapshot source ID already names different immutable bytes")
        return snapshot_root / authority.primary_relative_path, authority

    raster_metadata = _validate_import_source(source, role=role)
    components = _source_components(source)
    try:
        (temporary / "source").mkdir(parents=True)
        records: list[SnapshotImportFile] = []
        for component in components:
            target = temporary / "source" / component.name
            shutil.copyfile(component, target)
            relative = (Path(_IMPORT_DIRECTORY) / source_id / "source" / component.name).as_posix()
            records.append(
                SnapshotImportFile(
                    relative_path=relative,
                    sha256=sha256_file(target),
                    size_bytes=target.stat().st_size,
                )
            )
        copied_primary = temporary / "source" / source.name
        if (
            sha256_file(copied_primary) != source_hash
            or copied_primary.stat().st_size != source_size
        ):
            raise PathSafetyError("snapshot source copy differs from its original bytes")
        _validate_import_source(copied_primary, role=role)
        authority = SnapshotImportAuthority.create(
            source_id=source_id,
            role=role,
            created_at=now or datetime.now(UTC),
            imported_by=imported_by,
            import_reason=import_reason,
            original_filename=source.name,
            original_sha256=source_hash,
            original_size_bytes=source_size,
            files=tuple(sorted(records, key=lambda item: item.relative_path)),
            primary_relative_path=primary_relative,
            raster_crs=raster_metadata[0],
            raster_width=raster_metadata[1],
            raster_height=raster_metadata[2],
            raster_band_count=raster_metadata[3],
        )
        (temporary / _IMPORT_AUTHORITY).write_text(
            authority.model_dump_json(indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        os.replace(temporary, destination)
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise
    return snapshot_root / authority.primary_relative_path, authority


def load_snapshot_import_authority(
    path: Path,
    *,
    roots: StorageRoots,
) -> SnapshotImportAuthority:
    """Revalidate one imported snapshot package and every copied byte."""

    snapshot_root = roots.require_snapshot_root()
    authority_path = Path(path).resolve(strict=True)
    if not authority_path.is_relative_to(snapshot_root) or has_symlink_component(authority_path):
        raise PathSafetyError("snapshot import authority escapes the configured snapshot root")
    try:
        authority = SnapshotImportAuthority.model_validate(
            json.loads(authority_path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        )
    except (OSError, UnicodeError, ValueError) as exc:
        raise PathSafetyError("snapshot import authority is unreadable or invalid") from exc
    expected_authority = (
        snapshot_root / _IMPORT_DIRECTORY / authority.source_id / _IMPORT_AUTHORITY
    ).resolve()
    if authority_path != expected_authority:
        raise PathSafetyError("snapshot import authority path does not match its identity")
    for item in authority.files:
        candidate = (snapshot_root / item.relative_path).resolve(strict=True)
        if (
            not candidate.is_relative_to(snapshot_root)
            or has_symlink_component(candidate)
            or not candidate.is_file()
            or candidate.stat().st_size != item.size_bytes
            or sha256_file(candidate) != item.sha256
        ):
            raise PathSafetyError("snapshot import file bytes changed")
    primary = snapshot_root / authority.primary_relative_path
    if (
        primary.stat().st_size != authority.original_size_bytes
        or sha256_file(primary) != authority.original_sha256
    ):
        raise PathSafetyError("snapshot import primary source bytes changed")
    metadata = _validate_import_source(primary, role=authority.role)
    if metadata != (
        authority.raster_crs,
        authority.raster_width,
        authority.raster_height,
        authority.raster_band_count,
    ):
        raise PathSafetyError("snapshot import raster metadata changed")
    return authority


def verify_phase03_snapshot_source(path: Path, *, roots: StorageRoots) -> None:
    """Revalidate imported sources; registered raw-source snapshots use their Phase 00 identity."""

    source = roots.assert_snapshot_source(path)
    snapshot_root = roots.require_snapshot_root()
    relative = source.relative_to(snapshot_root)
    if not relative.parts or relative.parts[0] != _IMPORT_DIRECTORY:
        return
    if len(relative.parts) < 4 or relative.parts[2] != "source":
        raise PathSafetyError("configured Phase 03 imported source path is invalid")
    authority = load_snapshot_import_authority(
        snapshot_root / _IMPORT_DIRECTORY / relative.parts[1] / _IMPORT_AUTHORITY,
        roots=roots,
    )
    if relative.as_posix() != authority.primary_relative_path:
        raise PathSafetyError("configured Phase 03 source is not the imported primary file")


def _validate_import_source(
    source: Path,
    *,
    role: SnapshotImportRole,
) -> tuple[str | None, int | None, int | None, int | None]:
    if role == "legend":
        if source.stat().st_size == 0:
            raise PathSafetyError("legend snapshot source is empty")
        return None, None, None, None
    try:
        import rasterio

        with rasterio.open(source) as dataset:
            if dataset.crs is None:
                raise PathSafetyError("Phase 03 map must have explicit CRS evidence")
            if dataset.width < 1 or dataset.height < 1 or dataset.count < 1:
                raise PathSafetyError("Phase 03 map has invalid raster dimensions")
            if dataset.transform.is_identity:
                raise PathSafetyError("Phase 03 map lacks a non-identity spatial transform")
            bounds = tuple(float(value) for value in dataset.bounds)
            if not all(math.isfinite(value) for value in bounds):
                raise PathSafetyError("Phase 03 map has non-finite spatial bounds")
            return dataset.crs.to_string(), dataset.width, dataset.height, dataset.count
    except PathSafetyError:
        raise
    except (OSError, TypeError, ValueError) as exc:
        raise PathSafetyError("Phase 03 map cannot be opened as a georeferenced raster") from exc


def _source_components(source: Path) -> tuple[Path, ...]:
    candidates = {source}
    for suffix in _SIDECARS:
        by_name = source.with_name(source.name + suffix)
        by_stem = source.with_suffix(suffix)
        if by_name.is_file():
            candidates.add(by_name)
        if by_stem.is_file():
            candidates.add(by_stem)
    result = tuple(sorted(candidates, key=lambda item: item.name.casefold()))
    if any(has_symlink_component(item) for item in result):
        raise PathSafetyError("Phase 03 snapshot source bundle must not contain symlinks")
    return result


def create_snapshot_manifest(
    source_root: Path,
    manifest_path: Path,
    *,
    source_root_id: SourceRootId,
    roots: StorageRoots,
    run_id: str,
    now: datetime | None = None,
) -> SnapshotManifest:
    source = _authorized_source_root(source_root, source_root_id=source_root_id, roots=roots)
    destination = roots.assert_writable(manifest_path, run_id=run_id)
    if destination.exists():
        raise PathSafetyError("snapshot manifests are immutable and cannot be overwritten")
    files = _inventory_files(source)
    relatives = {path.relative_to(source).as_posix(): path for path in files}
    entries = tuple(_entry(path, source=source, relatives=relatives) for path in files)
    manifest = SnapshotManifest(
        source_root_id=source_root_id,
        created_at=now or datetime.now(UTC),
        entries=entries,
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(manifest.model_dump_json(indent=2), encoding="utf-8", newline="\n")
    return manifest


def verify_snapshot_manifest(
    source_root: Path,
    manifest_path: Path,
    *,
    source_root_id: SourceRootId,
    roots: StorageRoots,
) -> SnapshotVerification:
    source = _authorized_source_root(source_root, source_root_id=source_root_id, roots=roots)
    try:
        manifest = SnapshotManifest.model_validate(
            json.loads(
                manifest_path.read_text(encoding="utf-8"),
                object_pairs_hook=_unique_object,
            )
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise PathSafetyError("snapshot manifest is unreadable or invalid") from exc
    if manifest.source_root_id != source_root_id:
        raise PathSafetyError("snapshot manifest source-root identity mismatch")
    expected = {entry.relative_path: entry for entry in manifest.entries}
    actual_paths = _inventory_files(source)
    actual = {path.relative_to(source).as_posix(): path for path in actual_paths}
    missing = tuple(sorted(set(expected) - set(actual)))
    unexpected = tuple(sorted(set(actual) - set(expected)))
    changed = tuple(
        sorted(
            relative
            for relative in set(expected) & set(actual)
            if actual[relative].stat().st_size != expected[relative].size
            or sha256_file(actual[relative]) != expected[relative].sha256
        )
    )
    return SnapshotVerification(
        valid=not missing and not changed and not unexpected,
        missing=missing,
        changed=changed,
        unexpected=unexpected,
    )


def _authorized_source_root(
    source_root: Path,
    *,
    source_root_id: SourceRootId,
    roots: StorageRoots,
) -> Path:
    if source_root_id not in ("raw", "snapshot"):
        raise PathSafetyError(
            "snapshot creation and verification are limited to raw or immutable snapshot roots; "
            "workflow documents must not be bulk-read"
        )
    source = source_root.expanduser().resolve(strict=True)
    expected = {
        "raw": roots.raw_root,
        "snapshot": roots.snapshot_root,
    }[source_root_id]
    if expected is None or source != expected:
        raise PathSafetyError("snapshot source root does not match its configured identity")
    return source


def _entry(path: Path, *, source: Path, relatives: dict[str, Path]) -> SnapshotEntry:
    relative = path.relative_to(source).as_posix()
    lower = relative.casefold()
    suffix = next((value for value in _SIDECARS if lower.endswith(value)), None)
    parent = _bundle_parent(relative, relatives, suffix) if suffix else None
    return SnapshotEntry(
        relative_path=relative,
        size=path.stat().st_size,
        sha256=sha256_file(path),
        bundle_parent=parent,
        sidecar_kind=suffix,
    )


def _bundle_parent(relative: str, relatives: dict[str, Path], suffix: str) -> str | None:
    base = relative[: -len(suffix)]
    candidates = (base, base + ".tif", base + ".tiff", base + ".jpg", base + ".png")
    return next((candidate for candidate in candidates if candidate in relatives), None)


def _path_key(path: Path) -> str:
    return path.as_posix().casefold()


def _inventory_files(source: Path) -> tuple[Path, ...]:
    entries = tuple(sorted(source.rglob("*"), key=_path_key))
    symlinks = tuple(path.relative_to(source).as_posix() for path in entries if path.is_symlink())
    if symlinks:
        raise PathSafetyError(f"snapshot roots cannot contain symlinks: {symlinks[0]}")
    return tuple(path for path in entries if path.is_file())


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate snapshot-manifest key: {key}")
        value[key] = item
    return value
