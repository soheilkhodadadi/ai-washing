# Current State And Roadmap

Generated: 2026-06-08

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
- Private data staging: 14 of 15 unique logical paths staged locally. The remaining item is `data/external/execucomp_or_private_db`, marked as a future extension for Test 25.

## Main Risks To Control

- Workspace confusion: this chat's default shell still points to `semantic-patterns`; future execution must use the `ai-washing` repo explicitly or start a new Codex workspace there.
- Private data leakage: WRDS/CRSP, derived panels, labels, archives, and generated outputs must stay outside Git.
- Environment drift: exact reproduction requires pinned dependency versions, not latest `pip` versions.
- Manuscript wrapper deltas: many v4.3 manuscript TeX files differ from generated TeX because of captions, notes, resizing, or manual manuscript wrappers. Numeric CSV evidence should be treated separately from manuscript-facing TeX wrappers.
- Full-table uncertainty: selected reproduction has passed, but the remaining 19 table assets and 2 figures still need full expansion or explicit frozen-asset treatment.

## Roadmap To Complete Coauthor-Ready Workstation

### Phase 3A: Fresh Clone Smoke Test

Status: initial pass on 2026-06-08. Keep this as a repeated gate after major code/data-manifest changes.

Goal: prove a new machine can clone the private repo and validate the code/docs without private data.

Tasks:

- Clone `soheilkhodadadi/ai-washing` into a temporary clean folder.
- Create `.venv`, install `pip install -e .`, and confirm pinned versions.
- Run `make validate`, `make path-leak-scan`, `make import-smoke`, `make smoke-fixture`, and `make git-hygiene`.
- Confirm `make reproduce-selected` reports private-data paths clearly when `AIW_DATA_ROOT` is absent.

Gate: fresh clone can pass all non-private validation and fails gracefully for private reruns. Initial gate passed; rerun after Phase 3B/3C changes.

### Phase 3B: Private Data Mirror Contract

Goal: make Kuntara's data setup mechanical.

Tasks:

- Add a private-data package checklist under the external data root.
- Confirm each expected path in `manifests/data_dependency_manifest.csv` maps cleanly from `data/...` to `$AIW_DATA_ROOT/...`.
- Write a coauthor-facing private-data README that explains where to put the shared Dropbox/OneDrive folder and how to set `AIW_DATA_ROOT`.
- Keep checksum reports outside Git unless paths/data are sanitized.

Gate: a collaborator can stage or mirror private data without guessing folder names.

### Phase 3C: Full Table Expansion

Goal: move from selected reproduction to every v4.3 table/figure asset.

Tasks:

- Run each crosswalk table one by one through `scripts/run_publication_table.py` where supported.
- For each asset, classify output as `csv_exact_match`, `format_only_delta`, `content_delta`, `blocked_private_input`, `frozen_asset_only`, or `not_regenerated_by_design`.
- Update `docs/full_reproduction_status.md` after each batch.
- For Test 25, decide whether to stage the private ExecuComp/database artifact, preserve frozen generated evidence only, or mark as future extension.

Gate: every v4.3 table/figure has a table-level reproduction status with no unexplained numerical difference.

### Phase 3D: Coauthor Runbook And First Issue Queue

Goal: make collaboration easy once Kuntara starts testing or adding models.

Tasks:

- Add `docs/coauthor_runbook.md` with exact first-day commands.
- Add `docs/issue_queue.md` for known next work: Test 25 dependency, wrapper deltas, figure regeneration, full-table expansion.
- Add one or two example Git workflows: new branch, run table, commit code-only changes, never commit data.

Gate: coauthors can start from the README without needing the old `semantic-patterns` repository.

### Phase 3E: Containerization Or Devcontainer

Goal: reduce environment variation after the full table surface is clearer.

Tasks:

- Add Docker/devcontainer only after full-table expansion stabilizes.
- Bind-mount external `AIW_DATA_ROOT`; do not bundle private data into the image.
- Run non-private validation and selected private reproduction inside the container.

Gate: fresh clone plus mounted private data can reproduce selected tables in the container.

## Recommended Immediate Next Move

Start with Phase 3B. The fresh-clone non-private gate has passed; the next practical bottleneck is making the private data mirror contract mechanical enough that Kuntara can stage data without guessing folder names or relying on Soheil's machine.
