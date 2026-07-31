Buduunkhad exploration pipeline
===============================

What this is
------------
A config-driven Python geospatial pipeline implementing the automatable parts
of the Buduunkhad exploration workflow methodology (phases 00-99), plus an
offline, keyless AI-to-QGIS interpretation slice with human review and
promotion controls. Project identity, licence, deliverable CRS, buffers, and
the registered raw-input inventory are defined by config/project.yaml and the
registered input manifests (config/input_register.csv, config/raw_manifest.csv).

Installation
------------
Python 3.11 or 3.12. From the repository root:

    pip install -e .            (runtime)
    pip install -e .[dev]       (development: ruff, ty, pytest)

Optional extras: [dem] (terrain/hydrology tooling), [openai] / [anthropic]
(live provider adapters; never required for tests or offline work).

Default behavior
----------------
The default execution profile is "legacy": fully offline, AI disabled, no
network access, no provider SDK imports, and no external data egress. Dry runs
(`run --dry-run`) require no raw data. Live provider execution is opt-in and
requires explicit non-legacy configuration, egress approval, and credentials
supplied only at execution time.

Command-line entry points
-------------------------
    buduunkhad list | info | validate | methodology-status | run | results | publish | backup-raw
    buduunkhad ai snapshot-create | snapshot-verify | prepare | approve-egress
                  | execute | ingest-response | process-response | evaluate
                  | inspect-job
    buduunkhad ai phase03 prepare-source | import-ai-draft | review-overlaps
                         | build-run-review | promote-reviewed

Where things live
-----------------
- Agent permissions, safety and implemented-state summary: AGENTS.md (the only
  tracked Markdown file).
- Methodology authority, append-only decisions and operational readiness:
  config/methodology/ (versioned YAML contracts).
- Reviewed methodology source mirrors: docs/methodology/. Each approved
  document exception is bound to an exact repository path, SHA-256, byte size
  and verified snapshot identity by the authority and repository-policy contracts.
- External methodology remains reachable read-only through the
  BUDUUNKHAD_WORKFLOW_DOCS_ROOT environment root for source reconciliation.
- Set BUDUUNKHAD_PROJECT_ROOT once to use the standard local `raw`, `snapshots`,
  `work`, `current`, `results`, `evaluation`, and `publish` folders. More specific
  root variables remain available for non-standard deployments.
- Raw geological data and production outputs are external to Git. The raw archive
  is immutable and checksum-verified. Complete sealed internals stay under
  `work/runs`; `current` is a compatibility view; `buduunkhad results --run-id ID`
  atomically creates the small operator-facing `results/latest` view from declared
  outputs only. Repeat `--review-package` and supply `--review-project` when the
  portable view should include verified Phase 03 AI review data. External
  publication remains a separate deliberate operation.

Implemented phase boundary
--------------------------
Phases 00-04 have substantial deterministic implementations. Phase 03 remains
scientifically incomplete. Phase 04 remains a legacy comparator inside the ordered
pipeline, while a separate prospect-polygon implementation remains inactive until the exact Phase 03 handoff,
reference-set calibration and required human reviews exist. The comparator cannot run
against a valid real predecessor until the blocking Phase 03 scientific handoff is
accepted; dry-run scaffolding does not establish readiness. Phases 05-11 and 99 are
registered stubs (scaffolding and templates only). The optional Phase 03 AI handoff
promotes explicitly human-reviewed proposals into standalone accepted evidence;
accepted evidence is support material and is not scientific (geologist) approval.
The build-run-review command creates one portable QGIS view over sealed Phase 01–03
outputs and validated AI review packages while preserving those provenance boundaries.
