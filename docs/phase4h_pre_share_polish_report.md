# Phase 4H Pre-Share Polish Report

Date: 2026-06-10

## Verdict

Phase 4H passes.

The AI Washing workstation is ready for the final OneDrive/GitHub coauthor share after Soheil syncs the private data room. This phase focused on the small, visible issues that create unnecessary coauthor friction: environment checks, figure auditability, the C7 format-only delta, pandas warning cleanup, capital-raising terminology, and a polished one-page share note.

## What Changed

- Added `make doctor` and `make coauthor-preflight` as the first-day environment and code-only validation path.
- Added `docs/coauthor_share_note.md` as a polished email-style note for Thomas/Kuntara.
- Added `docs/onedrive_data_room_checklist.md` as the private data-room upload/share checklist.
- Added figure regeneration support for `F1` and `FC1` through `make reproduce-figures` and `make figure-reproduction-status`.
- Added `docs/figure_reproduction_status.md` and `docs/figure_reproduction_status.csv` to document figure evidence.
- Added `make c7-format-delta`, `docs/c7_format_delta_explanation.md`, and `docs/c7_format_delta_cells.csv` for the one format-only CSV delta.
- Removed the pandas `.fillna` downcasting warning from `test_05_size_heterogeneity.py` and added a focused regression test.
- Clarified that Test 30 is complete for v4.3 as a CRSP `shrout`-growth issue-window proxy. The deferred future item is actual SEO/offering terms, not generic equity issuance.
- Added the missing FC1 figure-run dependencies to the data dependency manifest: event panel, monthly CRSP stock file, and CRSP market index.
- Updated Docker so bind-mounted source imports work without asking coauthors to set `PYTHONPATH` manually.

## Reproduction Status

Full v4.3 table status after rerun:

```text
csv_exact_match: 23
format_only_delta: 1
frozen_asset_only: 2
```

Figure audit status after rerun:

```text
figure_evidence_generated: 2
```

Interpretation:

- All table numerical CSV evidence is reproduced exactly except C7.
- C7 differs only in 16 floating-point string representations, with maximum absolute numeric delta of `4.16333634234433703e-17`, well below the `1e-10` tolerance. Its generated TeX output is exact.
- F1 and FC1 regenerate exact figure-series CSV evidence. Generated PDF/PNG candidates are retained as audit evidence, while frozen v4.3 manuscript figure PDFs remain canonical.

## Validation Run

Local validation passed:

```bash
make PYTHON=.venv/bin/python doctor
make PYTHON=.venv/bin/python coauthor-preflight
.venv/bin/python -m pytest -q
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make PYTHON=.venv/bin/python check-private-data validate-data-room validate-sec-source validate-wrds-data validate-patent-data audit-artifact-coverage
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make PYTHON=.venv/bin/python reproduce-all-tables
make PYTHON=.venv/bin/python reproduction-status
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make PYTHON=.venv/bin/python reproduce-figures
make PYTHON=.venv/bin/python figure-reproduction-status
make PYTHON=.venv/bin/python c7-format-delta
git diff --check
make PYTHON=.venv/bin/python git-hygiene
```

Observed results:

- `doctor`: passed; pinned package versions match.
- `coauthor-preflight`: passed.
- `pytest`: 21 passed; no pandas warning reappeared.
- `check-private-data`: 15 of 15 logical runtime paths present.
- `validate-data-room`: 35 present rows and 2 documented future-extension rows: `seo_offering_terms` and `job_postings`.
- `validate-sec-source`: 7 of 7 rows present.
- `validate-wrds-data`: 16 of 16 rows present.
- `validate-patent-data`: 29 of 29 rows present.
- `audit-artifact-coverage`: 20 `coverage_pass` rows and 2 documented `not_promoted` candidates.
- `git diff --check`: passed after normalizing the crosswalk CSV newline/trailing-whitespace issue.
- `git-hygiene`: passed.

## Docker Rehearsal

Docker image used:

```text
ai-washing-phase4h
```

No-private-data container mode passed the code-only preflight and failed the private-data check only with controlled missing-data messages.

Read-only private-data container mode passed:

```bash
make PYTHON=python coauthor-preflight
make PYTHON=python check-private-data validate-data-room validate-sec-source validate-wrds-data validate-patent-data audit-artifact-coverage
make PYTHON=python reproduce-all-tables
make PYTHON=python reproduction-status
make PYTHON=python reproduce-figures
make PYTHON=python figure-reproduction-status
make PYTHON=python c7-format-delta
PYTHONPATH=src python -m pytest -q
git diff --check
make PYTHON=python git-hygiene
```

This confirms that the private data room can be mounted read-only for reproduction and audit. No script needs to mutate shared private data during normal validation.

## Remaining Non-Blockers

- `seo_offering_terms` is a future-extension data source for the strong washing-pays test: proceeds, offer price, discount, valuation base, offering type, and issue timing.
- `job_postings` remains an optional future-extension source.
- Frozen manuscript PDFs remain canonical for F1 and FC1. The repo now provides regenerable figure-series evidence and candidate outputs, but it does not replace the manuscript PDFs.
- Full raw SEC bulk remains excluded by design. The package includes samples, source links, extracted AI sentences, and final classifier outputs.

## Share Procedure

1. Push this Git state to the private GitHub repository.
2. Confirm OneDrive has fully synced `/Users/soheilkhodadadi/DataWork/ai-washing-private-data` or the chosen private data-room mirror.
3. Share the GitHub repository and OneDrive link with Kuntara/Thomas.
4. Send or adapt `docs/coauthor_share_note.md` as the cover note.
5. Ask coauthors to start with `README_START_HERE.md`, `docs/coauthor_runbook.md`, and `docs/onedrive_data_room_checklist.md`.
