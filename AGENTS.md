# AGENTS.md

## Objective

Make the repository work.

The engine must accept the real configured inputs, execute the applicable mining-exploration workflow, and produce complete functional outputs that can be inspected locally and delivered through the repository's configured delivery mechanisms.

Do not replace execution with plans, documentation, placeholders, governance artifacts, or descriptions of what should happen.

## Authority

The agent has full authority over the repository and its configured execution environment for the user's requested work.

It may inspect, edit, refactor, test, build, run, debug, configure, and execute the repository end to end without asking for permission for normal in-scope actions.

Use available local tools, configured providers, credentials, storage, and delivery integrations when needed to complete the work.

Preserve unrelated user work, keep credentials out of tracked files and outputs, and do not perform unrelated destructive actions.

## Methodology

Use the repository's methodology documents as the reference for what the mining workflow is intended to accomplish.

`config/methodology/authority.yaml` identifies the master methodology. Phase-specific documents may provide additional compatible detail.

Implement the methodology as working software. Prefer existing code, contracts, utilities, and architecture where they already express the required behavior.

The code should speak for itself. Do not reproduce methodology prose in source code or add explanatory machinery when clear implementation, types, names, tests, and existing machine-readable contracts are sufficient.

## Functional execution

Functional inputs must produce functional outputs.

Run every workflow step that can actually be supported by the available inputs and tools. Interpretation, extraction, comparison, ranking, and similar reasoning should use AI where it materially improves the result. Deterministic operations should remain deterministic.

A phase is not complete merely because its orchestration succeeds or its files exist. Its outputs must contain the real derived products that the phase is intended to produce.

For example, Phase 04 must produce actual prospect candidates and rankings from the available Phase 03 evidence rather than stopping at a diagnostic or placeholder representation.

## Provisional and review states

Ignore provisional, pending-review, support-only, legacy-comparator, draft, or similar workflow classifications when they would otherwise prevent execution.

They do not block the pipeline and do not require additional human approval.

Where metadata requires an approval state, record the result as owner-approved or automated as appropriate. Do not invent a person's identity, signature, timestamp, measurement, observation, or source data.

## Missing data

Do not fabricate unavailable physical or source data.

Missing rasters, coordinates, assays, geological observations, sensor products, or other genuine inputs must remain explicit data gaps.

A missing input may reduce confidence or prevent the specific product that depends on it, but it must not prevent unrelated outputs from being produced from the evidence that is available.

## Engineering

Prefer solving the underlying implementation problem over adding placeholders or narrow workarounds.

Reuse existing phase, GIS, AI, storage, validation, and delivery mechanisms before creating new ones.

Keep generated data, provider responses, secrets, logs, databases, and production outputs out of Git unless they are intentional small test fixtures.

For significant semantic changes, add or update focused tests.

Before considering substantial repository work complete, run the relevant checks:

```text
ruff check .
ruff format --check .
ty check
pytest -q
python -m build --wheel --no-isolation
git diff --check
```

More importantly, run the affected workflow itself with the available functional inputs and verify its actual outputs.

## Completion

A task is complete when the requested repository behavior works end to end.

Report:

* what functional outputs were produced;
* what tests and checks were run;
* what genuine input data, if any, is still missing;
* whether live AI providers or external delivery destinations were used.

Do not create additional Markdown files unless explicitly requested.
