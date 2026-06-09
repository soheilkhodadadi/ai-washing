# Coauthor Runbook

This runbook is the first-day path for working on AI Washing without relying on Soheil's older `semantic-patterns` workspace.

## 1. Clone The Code Repository

Clone the private GitHub repository into a normal local folder, not into Dropbox or OneDrive:

```bash
git clone git@github.com:soheilkhodadadi/ai-washing.git
cd ai-washing
```

If SSH is not configured, use the HTTPS private-repo URL from GitHub.

## 2. Create The Python Environment

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

The repository pins the direct runtime dependencies used for the v4.3 reproduction gate. Avoid upgrading packages during reproduction checks unless the goal is explicitly to test environment drift.

## 3. Set The Path Contract

```bash
export AIW_REPO_ROOT="$PWD"
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
export AIW_OUTPUT_ROOT="$PWD/outputs/reproduced"
export AIW_PAPER_ROOT="$PWD/outputs/paper_exports"
```

`AIW_DATA_ROOT` should point to a local mirror of the private Dropbox/OneDrive data folder. The Git repository should remain outside the synced data folder.

## 4. Run Non-Private Validation

```bash
make validate
make path-leak-scan
make import-smoke
make smoke-fixture
make git-hygiene
```

These checks should pass even without private data.

## 5. Validate The Private Data Mirror

```bash
make check-private-data
```

Expected current result: every table-rerun `required_current` and `support_only` input is present, including `external/execucomp/execucomp_ceo_anncomp_2015_2024.parquet`.

## 6. Reproduce Selected v4.3 Tables

Start with the selected gate:

```bash
make reproduce-selected
make TABLE_ID=T16 reproduce-table
make compare-selected-reproduction
```

The selected v4.3 gate covers `T00`, `T16`, `T17`, `T09`, and `T30`. CSV exact matching is the numerical reproduction criterion; TeX wrapper differences can reflect manuscript notes, captions, or layout wrappers.

## 7. Expand To Full Tables

Dry-run the full table surface first:

```bash
make reproduce-all-tables-dry-run
```

Then run batches deliberately:

```bash
PYTHONPATH=src python scripts/reproduce_assets.py --batch remaining-main
PYTHONPATH=src python scripts/reproduce_assets.py --batch appendix
make reproduction-status
```

Do not treat figures as required reruns unless they are explicitly promoted from frozen manuscript assets to regenerable outputs.

## 8. Git Rules

- Commit code, docs, manifests, fixtures, and sanitized status ledgers.
- Do not commit raw/private data, parquet outputs, WRDS/CRSP inputs, archives, `.venv`, or generated outputs under `outputs/`.
- Work on a short branch for changes, then merge or open a pull request.

Example:

```bash
git checkout -b table-20-cleanup
make check-private-data
make TABLE_ID=T20 reproduce-table
git status --short
```

If a table changes numerically, document whether the difference is expected before committing any manuscript-facing update.
