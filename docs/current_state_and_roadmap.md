# Current State And Roadmap

Generated: 2026-06-09

## Current State

- Canonical local repository: `/Users/soheilkhodadadi/DataWork/ai-washing`.
- Canonical private data root: `/Users/soheilkhodadadi/DataWork/ai-washing-private-data`.
- Private GitHub repository: `https://github.com/soheilkhodadadi/ai-washing`.
- Git branch: `main`, clean and tracking `origin/main`.
- Release tags: `v4.3-defense-freeze` and `phase2-selected-repro-passed`.
- Tracked repository size is small; local bulk comes from ignored `.venv`, ignored reproduced outputs, and the external private data root.
- The current Codex chat/process still opens from the older `semantic-patterns` workspace. That is a UI/workspace-root issue, not a Git issue. Future AI Washing work should open `/Users/soheilkhodadadi/DataWork/ai-washing` as the workspace or explicitly run commands from that path.

## What Is Already Working

- `README.md` now exists for GitHub's landing page and points to the full quickstart.
- Fresh-clone smoke test passed from GitHub in `/tmp/aiw-fresh-clone-59obuX/ai-washing`: pinned versions installed, non-private validation passed, and missing private-data reruns reported clear staging paths.
- `README_START_HERE.md`, `AGENTS.md`, `.env.example`, `requirements-lock.txt`, and collaboration/data-management docs are present.
- The direct runtime dependencies are pinned to the v4.3-validated environment. This matters because an unpinned fresh install caused a tiny `T09` CSV representation delta under newer `pandas`/`numpy`; pinning restored exact matching.
- Core validation passes:
  - `make validate`
  - `make path-leak-scan`
  - `make import-smoke`
  - `make smoke-fixture`
  - `make git-hygiene`
- Selected v4.3 reruns pass for `T00`, `T16`, `T17`, `T09`, and `T30`; fresh CSV outputs exactly match frozen v4.3 generated evidence.

## Current Manifest Snapshot

- Manuscript crosswalk: 26 mapped assets, including 24 tables and 2 figures.
- v4.3 manuscript asset inventory: 31 rows.
- Source closure: 34 modules.
- Data dependency manifest: 44 rows and 15 unique logical private/support paths.
- Private data staging: 15 of 15 unique logical paths staged locally after promoting Test 25 to a private ExecuComp-cache dependency.
- Coauthor data-room manifest: broader full-data contract for cleaned panels, classifier outputs, sentence extracts, patent lineage, CRSP/Compustat merge inputs, raw/near-raw samples, source links, and extension data.
- Artifact provenance audit: lane-specific v4.3 coverage gate with 22 tracked artifacts. Current expected state is 20 promoted artifacts passing coverage and 2 documented not-promoted candidates.
- v4.3 lane coverage is explicit: annual NLP/patent artifacts cover 2016-2025; event/market-return artifacts cover 2016-2024 because staged CRSP/event-return inputs stop at 2024-12-31.

## Main Risks To Control

- Workspace confusion: this chat's default shell still points to `semantic-patterns`; future execution must use the `ai-washing` repo explicitly or start a new Codex workspace there.
- Private data leakage: WRDS/CRSP, derived panels, labels, archives, and generated outputs must stay outside Git.
- Environment drift: exact reproduction requires pinned dependency versions, not latest `pip` versions.
- Manuscript wrapper deltas: many v4.3 manuscript TeX files differ from generated TeX because of captions, notes, resizing, or manual manuscript wrappers. Numeric CSV evidence should be treated separately from manuscript-facing TeX wrappers.
- Full-table uncertainty: selected reproduction has passed, Phase 3C produced a batch reproduction ledger, and Phase 3D closes the T25 input-policy gap. Broader raw/intermediate data-room artifacts still need staging for bottom-up rebuilds and extensions.
- Artifact substitution risk: newer-looking 2016-2025 filing-spine files must not be silently substituted for the 2016-2024 v4.3 event-return panel. Use `make audit-artifact-coverage` before promoting private artifacts.

## Roadmap To Complete Coauthor-Ready Workstation

### Phase 3A: Fresh Clone Smoke Test

Status: initial pass on 2026-06-08. Rerun after Phase 3D/3E changes before release.

Goal: prove a new machine can clone the private repo and validate the code/docs without private data.

Tasks:

- Clone `soheilkhodadadi/ai-washing` into a temporary clean folder.
- Create `.venv`, install `pip install -e .`, and confirm pinned versions.
- Run `make validate`, `make path-leak-scan`, `make import-smoke`, `make smoke-fixture`, and `make git-hygiene`.
- Confirm `make reproduce-selected` reports private-data paths clearly when `AIW_DATA_ROOT` is absent.

Gate: fresh clone can pass all non-private validation and fails gracefully for private reruns. Initial gate passed; rerun after Phase 3B/3C changes.

### Phase 3B: Private Data Mirror Contract

Status: implemented as a mechanical gate.

Goal: make Kuntara's data setup mechanical.

Implemented artifacts:

- `docs/private_data_contract.md` defines the logical `data/...` to `$AIW_DATA_ROOT/...` mapping.
- `docs/coauthor_runbook.md` gives first-day clone, setup, private data, and selected reproduction commands.
- `docs/workspace_routing.md` explains how this memory-rich global thread can safely route commands to the canonical AI Washing repo.
- `scripts/check_private_data.py` validates the external mirror and fails only for missing required-current inputs.
- `make check-private-data` exposes the validation command.

Gate: current local mirror reports 15/15 unique logical paths present after staging `external/execucomp/execucomp_ceo_anncomp_2015_2024.parquet`.

### Phase 3C: Full Table Expansion

Status: first actual full-table reproduction pass completed.

Goal: move from selected reproduction to every v4.3 table/figure asset.

Implemented artifacts:

- `scripts/reproduce_assets.py` runs or dry-runs crosswalk assets in selected, main, appendix, or all batches.
- `make reproduce-all-tables-dry-run`, `make reproduce-all-tables`, and `make reproduction-status` write `docs/full_reproduction_status.md` and `docs/full_reproduction_status.csv`.
- Figures default to frozen-asset treatment unless explicitly included in the status ledger.

Gate: every v4.3 table/figure has a table-level reproduction status. Current status is 23 CSV exact matches, 1 format-only CSV delta for C7, and 2 frozen figure assets. T25 is now a CSV exact match from the staged ExecuComp cache.

### Phase 3D: Coauthor Runbook And First Issue Queue

Status: implemented for the coauthor-facing handoff layer.

Goal: make collaboration easy once Kuntara starts testing or adding models.

Implemented artifacts:

- `docs/coauthor_data_room.md` defines the broader full-data handoff contract.
- `manifests/coauthor_data_room_manifest.csv` records staged and deferred coauthor artifacts.
- `scripts/validate_data_room.py` and `make validate-data-room` validate row counts, schemas, sizes, and optional hashes.
- `docs/t25_execucomp_policy.md` documents the staged ExecuComp cache and explicit WRDS refresh path.
- `docs/extension_playbook.md` records Kuntara's washing-pays and builder-hides extension lanes.

Gate: coauthors can start from the README without needing the old `semantic-patterns` repository, and the remaining broader data-room gaps are explicit.

### Phase 3F: Artifact Coverage Correction

Status: implemented; validation pending.

Goal: remove ambiguity between March/v3 artifacts, April/v4.3 artifacts, and future-extension candidates.

Implemented artifacts:

- `docs/artifact_coverage_policy.md` defines the canonical lane coverage.
- `manifests/artifact_provenance_audit.csv` records promoted artifacts, excluded candidates, expected row counts, file counts, and year/date coverage.
- `scripts/audit_artifact_coverage.py` validates the private mirror against that manifest.
- `make audit-artifact-coverage` exposes the gate.
- The private data room now stages final hybrid API classifier outputs, local-layered classifier support/provenance, 2016-2024 extracted sentences, 2025 refresh extracted sentences, annual lineage panels, filing spine/WRDS bridge files, representative SEC full-submission samples, representative 2025 Stage-One samples, and source links.

Gate: the audit must pass with annual/NLP/patent artifacts at 2016-2025 and event/market-return artifacts at 2016-2024. No required artifact may have unexplained coverage drift.

### Phase 3E: Containerization Or Devcontainer

Goal: reduce environment variation after the full table surface is clearer.

Tasks:

- Add Docker/devcontainer only after full-table expansion stabilizes.
- Bind-mount external `AIW_DATA_ROOT`; do not bundle private data into the image.
- Run non-private validation and selected private reproduction inside the container.

Gate: fresh clone plus mounted private data can reproduce selected tables in the container.

## Recommended Immediate Next Move

Proceed to Phase 4 using `docs/phase4_coauthor_completeness_roadmap.md` as the controlling roadmap. The highest-return next step is patent closure: stage processed patent counts/examples/diagnostics, port the final patent construction modules, and add the patent method/evidence pack before sharing the coauthor data room.

### Phase 3D Addendum: Full Coauthor Data Room

Status: started.

The table-rerun manifest is intentionally narrower than Kuntara's full-data request. The broader coauthor data-room manifest now tracks raw SEC samples, extracted AI sentences, classifier outputs, patent-match lineage, CRSP/Compustat merge intermediates, and future extension inputs. Items marked `deferred_with_reason` are not v4.3 table-rerun blockers; they are the next staging queue before the handoff is considered complete enough for independent extension work.

### Phase 3E Addendum: Container Surface

Status: initial Dockerfile/devcontainer added; local container validation still remains to be run.

The container installs the pinned Python environment and expects private data to be bind-mounted at `/workspaces/ai-washing-private-data`. Private data are never copied into the image. Container runtime validation remains open because Docker was installed but the local daemon was not running during the Phase 3D/3E pass.
