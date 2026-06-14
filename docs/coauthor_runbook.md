# Coauthor Runbook

This runbook is the first-day path for working on AI Washing without relying on the older `semantic-patterns` workspace.

## 0. Understand The Paper Workstation

Before running or modifying tables, open these two files:

```text
docs/empirical_workstation.md
docs/paper_table_workbench.md
docs/panel_and_data_catalog.md
docs/construct_playbooks/README.md
```

The empirical workstation guide explains how SEC text, classifier outputs, patent data, WRDS/market data, and annual/event panels fit together. The paper table workbench maps each v4.3 manuscript table and figure to its empirical question, data product, script module, rerun command, and safe modification path. The panel/data catalog explains the private data products, and the construct playbooks explain how to update central variables without disturbing v4.3 evidence.

If the goal is to revise a specific table, start from the workbench rather than searching through scripts by filename.

## 1. Clone The Code Repository

Clone the private GitHub repository into a normal local folder, not into Dropbox or OneDrive:

```bash
git clone git@github.com:soheilkhodadadi/ai-washing.git
cd ai-washing
```

If SSH is not configured, use the HTTPS private-repo URL from GitHub.

## 2. Choose The Runtime Path

The easiest path is Docker:

```bash
make docker-build
make docker-preflight
```

Use native Python if you plan to edit code directly:

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
make doctor
make coauthor-preflight
```

`make coauthor-preflight` is the shortest first-day command. It runs the environment doctor, manifest validation, path leakage scan, import smoke test, fixture smoke test, and Git hygiene check.

The same checks can be run individually:

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
make validate-data-room
make validate-wrds-data
make validate-sec-source
make audit-artifact-coverage
```

Docker equivalent:

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make docker-private-check
```

Expected current result: every table-rerun `required_current` and `support_only` input is present, including `external/execucomp/execucomp_ceo_anncomp_2015_2024.parquet`.

The artifact coverage audit is deliberately lane-specific. Annual NLP/patent artifacts should cover 2016-2025, but event/market-return artifacts should cover 2016-2024 for v4.3 because the staged CRSP/event-return files stop at 2024-12-31. Do not replace the v4.3 event panel with a 2016-2025 filing spine unless a future release explicitly promotes a new return-event panel.

## 6. Validate The SEC Source / NLP Audit Layer

The full raw SEC corpus is not bundled by default. The private mirror instead includes representative raw/full-submission samples, representative Notre Dame Stage-One cleaned samples, public source links, extracted AI sentence outputs, and final hybrid classifier outputs.

```bash
make validate-sec-source
```

Then read:

```text
docs/sec_raw_source_policy.md
docs/sec_extraction_classification_audit.md
```

The validator should confirm 5 representative full-submission samples, 4 Stage-One 2025 samples, 106,977 extracted AI sentences for 2016-2024, 40,902 extracted AI sentences for 2025, and 147,879 final hybrid classified AI sentences for 2016-2025. If a coauthor wants a full raw rebuild, stage the corpus under a new private raw-source folder and add it to the manifest; do not put raw SEC text in Git.


## 7. Validate The WRDS / CRSP / Compustat Layer

The coauthor request includes the CRSP and Compustat merges, not only final panel variables. After the private mirror is mounted, run:

```bash
make validate-wrds-data
```

Then read:

```text
docs/wrds_crsp_compustat_method_note.md
docs/wrds_source_inventory.md
```

The validator should report all 16 WRDS manifest rows present. The key interpretation rule is that the filing spine and annual WRDS backbone extend through 2025, but the v4.3 event-return lane stops in 2024 because the staged CRSP return extracts stop at 2024-12-31.

## 8. Inspect The Patent Evidence Pack

Patent matching is the key construct-audit layer. After the private mirror is mounted, run:

```bash
make patent-example-audit
make validate-patent-data
```

If the private data mirror is mounted read-only, write the refreshed audit sample to `outputs/` instead:

```bash
make PATENT_AUDIT_OUTPUT="$PWD/outputs/patent_audit_examples.csv" patent-example-audit
make validate-patent-data
```

Then read the method notes:

```text
docs/patent_mismatch_method_note.md
docs/patent_matching_validation.md
docs/patent_source_inventory.md
docs/patent_fuzzy_sensitivity_note.md
```

The generated private audit sample is:

```text
$AIW_DATA_ROOT/reports/patents/patent_audit_examples.csv
```

It contains a small balanced sample of actual matched grant and pregrant AI patent/application examples.

## 9. Reproduce Selected v4.3 Tables

Start with the selected gate:

```bash
make reproduce-selected
make TABLE_ID=T16 reproduce-table
make compare-selected-reproduction
```

The selected v4.3 gate covers `T00`, `T16`, `T17`, `T09`, and `T30`. CSV exact matching is the numerical reproduction criterion; TeX wrapper differences can reflect manuscript notes, captions, or layout wrappers.

## 10. Expand To Full Tables

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

## 10A. Regenerate Figure Evidence Without Replacing Frozen Figures

The v4.3 manuscript figure PDFs remain frozen canonical assets. The workstation can still regenerate figure-series evidence and candidate PDFs for audit:

```bash
make reproduce-figures
make figure-reproduction-status
```

Read:

```text
docs/figure_reproduction_status.md
```

Current expected status: figure-series CSV evidence for `F1` and `FC1` matches the frozen v4.3 exports exactly, while generated PDFs are documented as layout/hash deltas relative to the frozen manuscript PDFs.

## 10B. Inspect The C7 Format-Only Delta

The full table ledger has one known format-only CSV delta in `C7`. Refresh the cell-level explanation with:

```bash
make c7-format-delta
```

Read:

```text
docs/c7_format_delta_explanation.md
docs/c7_format_delta_cells.csv
```

Current expected status: 16 numeric-string cells differ only at floating-point representation depth, all within `1e-10`, and the generated TeX file is an exact match.


## 11. Export A Table Workbench Bundle

For a table-specific inspection folder, run:

```bash
make workbench-index
make export-table-workbench TABLE_ID=T30
```

The bundle is written under ignored `outputs/workbench/T30/` and includes a short README, input-artifact notes, the rerun command, frozen reference outputs where available, generated public outputs where available, and safe-modification notes. It does not copy private panels or licensed data.

To rerun the table first and then refresh the bundle:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make export-table-workbench TABLE_ID=T30 RERUN=1
```

## 12. Run Extension Starters

After the v4.3 reproduction and construct-audit checks pass, coauthors can start from the extension layer without changing the frozen v4.3 evidence.

Inspect the registered extension lanes:

```bash
make extension-info EXTENSION=builder_hides
make extension-info EXTENSION=washing_pays_proxy
```

Run builder-hides first-pass screens:

```bash
make extension-builder-hides
make extension-builder-hides-ai-talk-only
```

Run the washing-pays proxy screen:

```bash
make extension-washing-pays-proxy
```

Then read:

```text
docs/extensions/README.md
docs/extensions/builder_hides_first_pass.md
docs/extensions/washing_pays_proxy_first_pass.md
docs/extensions/washing_pays_data_requirements.md
```

The builder-hides scripts use the staged annual panel and write ignored outputs under `outputs/extensions/`. The washing-pays proxy uses Test 30's CRSP share-growth logic and is not an SEO/offering-terms test. Use `templates/seo_offering_terms_schema.csv` before building the stronger financing-terms extension.

## 13. Git Rules

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
