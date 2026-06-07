# Phase 2 Execution Log

## 2026-06-07: Phase 2A/2B Bootstrap

Goal: convert the v4.3 handoff capsule into a clean local Git-tracked workstation while keeping private/large data outside Git.

Actions planned for this bootstrap:

- Copy the Phase 1 capsule into `/Users/soheilkhodadadi/DataWork/ai-washing-v43-handoff`.
- Create `/Users/soheilkhodadadi/DataWork/ai-washing-v43-private-data` as the external private data root.
- Add conservative `.gitignore` rules for generated outputs, caches, archives, and private/licensed binary data.
- Update quickstart documentation to use the new workstation path and explicit environment variables.
- Add Git hygiene validation before the first local commit.

Validation commands for this bootstrap:

```bash
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python validate
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python path-leak-scan
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python import-smoke
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python smoke-fixture
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python compare-tables
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python reproduce-selected
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python git-hygiene
```

Current known blocker: full numerical reproduction requires private inputs listed in `manifests/data_dependency_manifest.csv`.

## 2026-06-07: Phase 2C Private Data Staging

Targeted search roots:

- `/Users/soheilkhodadadi/DataWork`
- `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns`

Result:

- Found and staged all current/support missing inputs into `/Users/soheilkhodadadi/DataWork/ai-washing-v43-private-data`.
- Deferred only `data/external/execucomp_or_private_db`, which is marked `future_extension`.
- Moved copied binary/archive artifacts out of the Git workstation and into the private data root.
- Wrote private checksum and copy logs outside Git.

Private reports:

```text
/Users/soheilkhodadadi/DataWork/ai-washing-v43-private-data/private_data_checksum_report.csv
/Users/soheilkhodadadi/DataWork/ai-washing-v43-private-data/private_data_staging_copy_log.csv
```
Path contract correction: `AIW_DATA_ROOT` is the equivalent of repository `data/`, so files are staged without the leading manifest `data/` prefix. Example: `data/processed/panel/file.parquet` becomes `$AIW_DATA_ROOT/processed/panel/file.parquet`.

## 2026-06-07: Phase 2D Selected Table Reproduction

Selected targets run: `T16`, `T17`, `T30`, `T00`, and `T09`.

Result:

- All five selected scripts completed using `AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-v43-private-data`.
- Fresh reproduced CSV outputs are exact SHA-256 matches to the frozen v4.3 generated CSV evidence for all five targets.
- TeX outputs are exact only for `T00`; `T16`, `T17`, `T30`, and `T09` have TeX content deltas, treated as wrapper/export-level differences because their CSV payloads are exact matches.
- Generated outputs remain untracked under `outputs/`.

Reports:

```text
docs/selected_reproduction_comparison.csv
docs/selected_reproduction_status.md
docs/full_reproduction_status.md
```
