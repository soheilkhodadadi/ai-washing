# AI Washing v4.3 Handoff Workstation

This repository is the local Git-tracked handoff workstation for **AI Washing v4.3**. It freezes v4.3 as the computational reference target and keeps the original `semantic-patterns` repository as provenance only.

The package is intentionally curated. It is not a wholesale copy of the original research repository, and it does not track private or licensed data.

## What is tracked

- `paper/v4_3_source/`: frozen v4.3 LaTeX source and manuscript table/figure inputs.
- `paper/ai_washing_v4.3.pdf`: frozen v4.3 manuscript PDF.
- `manifests/`: table/script/data/artifact lineage files.
- `data/curated/v4_3/generated_runs/`: small generated run evidence where safe to track.
- `data/fixtures/`: tiny non-sensitive fixture data for smoke tests.
- `src/semantic_ai_washing/`: minimal source closure needed by mapped publication scripts.
- `src/semantic_ai_washing_min/`: capsule-specific fixture and validation utilities.
- `scripts/`: validation, comparison, hygiene, and reproduction wrappers.

## What is private or untracked

Private, licensed, large, or machine-local data are deliberately excluded from Git. This includes raw SEC/WRDS data, derived full-rerun panels, label/evaluation parquet files, archives, and generated outputs.

Use this external data root for Phase 2 staging:

```bash
export AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-v43-private-data
```

The expected private input paths are listed in `manifests/data_dependency_manifest.csv` and summarized in `docs/private_data_staging_map.md`.

## Environment contract

The workstation uses four explicit path variables:

```bash
export AIW_REPO_ROOT="$PWD"
export AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-v43-private-data
export AIW_OUTPUT_ROOT="$PWD/outputs/reproduced"
export AIW_PAPER_ROOT="$PWD/outputs/paper_exports"
```

If the variables are unset, the local scripts default to repository-local paths where possible. Full table reruns still require `AIW_DATA_ROOT` to contain the private inputs.

## Quick validation

Use the Python environment from the source repository until this workstation receives its own pinned environment:

```bash
cd /Users/soheilkhodadadi/DataWork/ai-washing-v43-handoff
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python validate
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python path-leak-scan
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python import-smoke
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python smoke-fixture
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python git-hygiene
```

## Comparison and rerun preflight

```bash
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python compare-tables
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python reproduce-selected
```

`reproduce-selected` is a dry-run preflight for `T00`, `T16`, `T17`, `T09`, and `T30`. It reports missing private inputs without failing the workstation.

## Full table reruns

After private inputs are staged under `AIW_DATA_ROOT`, run one table at a time:

```bash
export AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-v43-private-data
export AIW_OUTPUT_ROOT="$PWD/outputs/reproduced"
export AIW_PAPER_ROOT="$PWD/outputs/paper_exports"
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python TABLE_ID=T16 reproduce-table
```

Recommended first rerun targets: `T00`, `T16`, `T17`, `T09`, and `T30`.

## Current status

Phase 2A-2D establish this repository as a clean local workstation, stage the current/support private inputs outside Git, and verify selected-table numerical reproduction. Full-table expansion remains pending.
