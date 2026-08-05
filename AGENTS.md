# AGENTS.md — Mining pipeline instructions

## Mission

This repository is an AI-first mining-exploration engine. Its priority is functional execution:
take the configured real inputs, run Phases 00–04, and produce complete, usable phase outputs for
local inspection and team delivery. Prefer working results over additional governance machinery,
planning documents, or placeholder artifacts.

Use the byte-bound master methodology registered in `config/methodology/authority.yaml` as the
workflow authority. Use the individual phase documents to add compatible operational detail. If
they conflict, follow the master. Keep durable machine-readable decisions in the existing YAML,
JSON, CSV, or Python contracts; `AGENTS.md` remains the only tracked Markdown file.

## Autonomy

Agents have full authority to complete the user's scoped repository work end to end. This includes
editing code and configuration, refactoring, testing, building, running Phases 00–04, using locally
configured tools and provider credentials, producing outputs, maintaining local result mirrors,
and synchronizing configured team deliverables. Do not repeatedly ask for permission for normal,
in-scope implementation or execution steps.

Keep credentials out of tracked files and generated outputs. Preserve raw inputs unchanged and
process working copies. Preserve unrelated user work. Do not perform unrelated destructive actions.

## Execution policy

- Phases 00–04 are output-producing workflows, not documentation exercises. Implement and execute
  every functional step that can be supported by the available inputs and tools.
- AI is part of the main workflow wherever interpretation, inspection, extraction, comparison, or
  ranking materially improves the result. Deterministic code should handle file operations,
  transforms, measurements, validation, and packaging.
- Do not stop an otherwise executable Phase 00–04 run because an output is described as
  provisional, pending review, support evidence, or a legacy comparator. Skip those blocking
  distinctions and continue to produce the best real result available.
- Reviewer-dependent Phase 00–04 steps are considered reviewed and accepted under the project
  owner's direction. Do not require another attestation merely to execute the pipeline. Record the
  decision as owner-approved or automated where metadata is required; never invent a person's
  identity, signature, timestamp, measurement, or source data.
- Missing functional input data must remain explicit. Use available evidence and AI to derive what
  can genuinely be derived, but do not fabricate an unavailable raster, map observation,
  coordinate, assay, or geological fact.
- Phase 04 should produce actual prospect candidates and rankings from Phase 03 evidence. The
  existing grid comparator may remain as a diagnostic, but it must not replace the functional
  prospect workflow.
- Phase 05 remains parked until its real survey inputs are supplied. Do not let Phase 05 prevent
  completion of Phases 00–04.
- Keep outputs simple: complete run artifacts stay in the run workspace; curated phase deliverables
  go to the local results mirror and the configured Google Drive destination.

## Engineering rules

- All significant changes must be tested. Add or update focused tests for semantic changes when existing coverage does not already establish the intended behavior.

- Before writing significant amounts of new code, look for existing utilities or mechanisms that could solve the problem. Avoid expanding the task to unrelated issues, but do not confuse keeping the task focused with minimizing the size of the implementation. Prefer addressing the underlying architectural problem over adding a localized workaround, even when doing so requires a substantial refactor or rearchitecture. Ask the user for guidance if in doubt about whether to attempt a larger refactor or not.

- Don't use comments to narrate code, but do use them to explain invariants and why something unusual was done a particular way. Make sure that a comment will make sense to somebody who's reading the code for the first time. Prefer plain language, avoid jargon, and don't be afraid to be more verbose if it's necessary to explain something well.

- Prefer typed, cohesive changes and reuse existing phase, GIS, AI, run-storage, and results-delivery
  mechanisms before adding new systems.
- Fail clearly on corrupt inputs, unsafe paths, invalid geometry, broken provider responses, or
  outputs that cannot be verified. A clear functional data gap may reduce a result's confidence but
  should not stop unrelated products.
- Keep generated GIS data, rasters, databases, logs, provider responses, secrets, and production
  outputs outside Git. Small intentional synthetic test fixtures are allowed.
- Preserve Python 3.11 and 3.12 compatibility. Use Ruff for linting and formatting and ty for static
  type checking.

## Completion

For significant work, run focused tests and then the relevant repository checks:

```text
ruff check .
ruff format --check .
ty check
pytest -q
python -m build --wheel --no-isolation
git diff --check
```

Report the outputs produced, tests run, real functional data still missing, and whether a live AI
provider or external destination was used.
