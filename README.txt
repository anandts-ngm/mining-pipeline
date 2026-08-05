Buduunkhad exploration pipeline
===============================

What this is
------------
An AI-first, AI-native mineral-exploration engine that turns registered real-world
inputs into reproducible GIS, raster, geological-evidence and prospect-ranking
outputs. OpenAI performs the interpretation-heavy work; deterministic geospatial
code performs transformations, measurements, validation, lineage and packaging.
The engine also remains fully executable offline for deterministic processing,
testing and recovery. Project identity, licence, deliverable CRS, buffers and the
registered raw-input inventory are defined by config/project.yaml and the registered
input manifests (config/input_register.csv, config/raw_manifest.csv).

AI outputs are functional project artifacts, not demonstrations or placeholders.
Their recorded lifecycle states distinguish machine conclusions from independent
scientific approval; no label changes the underlying bytes, geometry or usefulness.

Installation
------------
Python 3.11 or 3.12. From the repository root:

    pip install -e .            (runtime)
    pip install -e .[dev]       (development: ruff, ty, pytest)

Optional extras: [dem] (terrain/hydrology tooling), [openai] / [anthropic]
(live provider adapters; never required for tests or offline work).

Operating behavior
------------------
The Buduunkhad command-line workflow automatically loads config/ai.openai.yaml as
its AI-first profile. A real run includes live interpretation when `run --ai` is
selected; without that flag, the same engine runs its deterministic phases offline.
The base project.yaml and library API remain keyless and offline so tests, recovery
and non-Buduunkhad projects never send data implicitly. Dry runs (`run --dry-run`)
require no raw data. Live provider execution requires
`run --ai --ai-approved-by "NAME" --ai-source SOURCE_ID`, package-level egress
approval and credentials supplied only at execution time.
Profiles with several Phase 03 maps require each intended `--ai-source`; the CLI
does not infer approval to send the whole source catalog.
The repository-local `.env` may contain only `OPENAI_API_KEY` or
`ANTHROPIC_API_KEY`; path roots, reviewer identities, and standing approvals are
rejected there.

Command-line entry points
-------------------------
    buduunkhad list | info | validate | methodology-status | run | results | publish | backup-raw
    buduunkhad ai snapshot-create | snapshot-verify | prepare | approve-egress
                  | execute | ingest-response | process-response | evaluate
                  | inspect-job
    buduunkhad ai phase03 import-snapshot-source | prepare-source | run-ai-first
                         | import-ai-draft | review-overlaps | build-run-review
                         | promote-reviewed

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
  `work`, `current`, `results`, `evaluation`, and `publish` folders. For a shared
  multi-area installation, set MINING_PIPELINE_WORK_ROOT instead; each project is
  isolated beneath its validated `project.slug`. Existing project-specific root
  variables continue to take precedence.
- Raw geological data and production outputs are external to Git. The raw archive
  is immutable and checksum-verified. Complete sealed internals stay under
  `work/runs`; `current` is a compatibility view; `buduunkhad results --run-id ID`
  atomically creates the small operator-facing `results/latest` view from declared
  outputs only. Repeat `--review-package` and supply `--review-project` when the
  portable view should include verified Phase 03 AI review data. Set
  MINING_PIPELINE_OUTPUTS_ROOT (or BUDUUNKHAD_RESULTS_MIRROR_ROOT) for a stable
  verified local team view, and MINING_PIPELINE_DRIVE_ROOT (or
  BUDUUNKHAD_RESULTS_UPLOAD_ROOT) for the matching Google Drive parent. Each area
  receives one human-readable directory derived from its manifest-bound project
  name. The Drive copy is made from the verified local mirror when both are
  configured; both retain identical hashes and `view_id`. Use
  `--no-upload-results` or `--no-upload` to skip only the Drive copy. Sealed run
  history remains under `work/runs`; external publication is separate.

Implemented phase boundary
--------------------------
Phases 00-04 have substantial automated implementations. They produce real,
sealed outputs from real inputs. Phase 03 combines
deterministic evidence assembly with AI legend extraction, geological-feature
proposals, critique and QGIS review packages. Phase 04 produces a fixed 250 m
evidence-grid candidate ranking that converts available evidence into prospect
polygons and A/B/C/D scores. Missing criteria remain explicit and score zero.
The prior `legacy-comparator` execution mode is retained only for regression
compatibility.

Optional specialist reviews may improve Phase 03 georeferencing, evidence and 03A
conclusions, but review-only pending rows do not stop automated Phase 00-04 output
generation. The separate reviewed prospect-polygon implementation remains available
when external reviewed polygons and scorecards are supplied. Neither automated nor
reviewed outputs are proof of ore, grade, resource or economics. Phases 05-11 and 99
remain registered stubs. The build-run-review
command creates one portable QGIS view over sealed Phase 01–03 outputs and validated
AI review packages while preserving exact source and model lineage.
