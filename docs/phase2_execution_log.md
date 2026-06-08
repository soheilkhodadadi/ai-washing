# Phase 2 Execution Log

## 2026-06-07: Phase 2A/2B Bootstrap

Goal: convert the v4.3 research capsule into a clean local Git-tracked workstation while keeping private/large data outside Git.

Actions completed:

- Created the first local Git-tracked workstation.
- Created an external private data root for full/private inputs.
- Added conservative `.gitignore` rules for generated outputs, caches, archives, and private/licensed binary data.
- Added quickstart documentation using explicit environment variables.
- Added Git hygiene validation before the first local commit.

Validation commands:

```bash
make validate
make path-leak-scan
make import-smoke
make smoke-fixture
make compare-tables
make reproduce-selected
make git-hygiene
```

Current known blocker: full numerical reproduction requires private inputs listed in `manifests/data_dependency_manifest.csv`.

## 2026-06-07: Phase 2C Private Data Staging

Targeted search roots:

- `/Users/soheilkhodadadi/DataWork`
- `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns`

Result:

- Found and staged all current/support missing inputs into `/Users/soheilkhodadadi/DataWork/ai-washing-private-data`.
- Deferred only `data/external/execucomp_or_private_db`, which is marked `future_extension`.
- Moved copied binary/archive artifacts out of the Git workstation and into the private data root.
- Wrote private checksum and copy logs outside Git.

Private reports:

```text
$AIW_DATA_ROOT/private_data_checksum_report.csv
$AIW_DATA_ROOT/private_data_staging_copy_log.csv
```

Path contract correction: `AIW_DATA_ROOT` is the equivalent of repository `data/`, so files are staged without the leading manifest `data/` prefix. Example: `data/processed/panel/file.parquet` becomes `$AIW_DATA_ROOT/processed/panel/file.parquet`.

## 2026-06-07: Phase 2D Selected Table Reproduction

Selected targets run: `T16`, `T17`, `T30`, `T00`, and `T09`.

Result:

- All five selected scripts completed using `AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data`.
- Fresh reproduced CSV outputs are exact SHA-256 matches to the frozen v4.3 generated CSV evidence for all five targets.
- TeX outputs are exact only for `T00`; `T16`, `T17`, `T30`, and `T09` have TeX content deltas, treated as wrapper/export-level differences because their CSV payloads are exact matches.
- Generated outputs remain untracked under `outputs/`.

Reports:

```text
docs/selected_reproduction_comparison.csv
docs/selected_reproduction_status.md
docs/full_reproduction_status.md
```

## 2026-06-08: Canonical Workstation Reframe

Goal: rename the project from a one-time v4.3 handoff to the permanent AI Washing research workstation.

Actions completed:

- Renamed the local repository to `/Users/soheilkhodadadi/DataWork/ai-washing`.
- Renamed the private data root to `/Users/soheilkhodadadi/DataWork/ai-washing-private-data`.
- Added collaboration and data-management docs.
- Added `AGENTS.md` and `.env.example` for future Codex/coauthor work.
- Preserved v4.3 as a release target rather than embedding it in the repository name.

## 2026-06-08: Environment Pinning Check

A fresh unpinned `.venv` initially installed `pandas 3.0.3`, `numpy 2.4.6`, and `pyarrow 24.0.0`. The selected rerun still passed structurally, but `T09` produced tiny floating-point/string representation deltas at the CSV hash level. The workstation now pins the direct runtime dependencies to the v4.3-validated stack, including `pandas==2.2.3`, `numpy==1.26.4`, and `pyarrow==23.0.1`; rerunning `T09` restored exact CSV matching.
