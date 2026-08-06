from __future__ import annotations

import subprocess
from pathlib import Path

from buduunkhad.repository_policy import APPROVED_METHODOLOGY_DOCUMENTS

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def test_only_agents_and_pinned_methodology_mirrors_are_tracked_markdown() -> None:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    markdown_suffixes = (".md", ".markdown", ".mdown", ".mdwn")
    tracked_markdown = [
        path
        for path in result.stdout.splitlines()
        if path.lower().endswith(markdown_suffixes) and (REPOSITORY_ROOT / path).is_file()
    ]
    # Deriving the allowed mirrors from the policy catalog, rather than naming them here,
    # means a markdown file can only become tracked by first being registered and hash-pinned.
    pinned_markdown = [
        path.as_posix()
        for path in APPROVED_METHODOLOGY_DOCUMENTS
        if path.suffix.casefold() == ".md"
    ]
    allowed = sorted(["AGENTS.md", *pinned_markdown])
    assert sorted(tracked_markdown) == allowed, (
        "Only AGENTS.md and the byte-pinned methodology mirrors may be tracked Markdown; "
        "durable methodology and audit facts belong in versioned machine-readable "
        f"contracts. Found: {sorted(tracked_markdown)}"
    )
