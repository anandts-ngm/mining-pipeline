"""Standard project-root expansion for protected and writable AI storage."""

from __future__ import annotations

from buduunkhad.config import PROJECT_ROOT_ENV
from buduunkhad.geospatial_ai.path_safety import (
    EVAL_ROOT_ENV,
    PUBLISH_ROOT_ENV,
    SNAPSHOT_ROOT_ENV,
    WORK_ROOT_ENV,
    StorageRoots,
)


def test_storage_roots_derive_from_single_project_root(tmp_path, monkeypatch):
    project_root = tmp_path / "project"
    monkeypatch.setenv(PROJECT_ROOT_ENV, str(project_root))
    for name in (SNAPSHOT_ROOT_ENV, WORK_ROOT_ENV, EVAL_ROOT_ENV, PUBLISH_ROOT_ENV):
        monkeypatch.delenv(name, raising=False)

    roots = StorageRoots.from_environment(raw_root=project_root / "raw")

    assert roots.snapshot_root == (project_root / "snapshots").resolve()
    assert roots.work_root == (project_root / "work").resolve()
    assert roots.eval_root == (project_root / "evaluation").resolve()
    assert roots.publish_root == (project_root / "publish").resolve()


def test_specific_storage_root_wins_over_project_root(tmp_path, monkeypatch):
    project_root = tmp_path / "project"
    specific_work = tmp_path / "specific-work"
    monkeypatch.setenv(PROJECT_ROOT_ENV, str(project_root))
    monkeypatch.setenv(WORK_ROOT_ENV, str(specific_work))

    roots = StorageRoots.from_environment(raw_root=project_root / "raw")

    assert roots.work_root == specific_work.resolve()
    assert roots.snapshot_root == (project_root / "snapshots").resolve()
