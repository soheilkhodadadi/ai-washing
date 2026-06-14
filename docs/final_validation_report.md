# Final Validation Report

Generated: 2026-06-14

This report summarizes the current validation state for the coauthor workstation. It distinguishes the Git-tracked code/docs package from the external private data room and preserves v4.3 as the numerical reproduction target.

## Commands Run In This Pass

```bash
make portfolio-demo
make portfolio-demo-check
make dashboard-check
make package-surface-audit
.venv/bin/python -m pytest -q
make coauthor-preflight
AIW_DATA_ROOT=/path/to/ai-washing-private-data make check-private-data validate-data-room
AIW_DATA_ROOT=/path/to/ai-washing-private-data make validate-sec-source validate-wrds-data validate-patent-data
AIW_DATA_ROOT=/path/to/ai-washing-private-data make audit-artifact-coverage
make reproduction-status figure-reproduction-status c7-format-delta
git diff --check
```

## Results

- Portfolio-safe static overview: passed; generated `outputs/portfolio_demo/index.html` and passed leakage/content checks.
- Static dashboard: passed; 26 paper assets, 16 data products, and 4 extension lanes are represented.
- Package surface audit: passed with 0 stop-the-line tracked leakage issues.
- Pytest suite: passed, 68 tests.
- Coauthor preflight: passed. The environment doctor used the repo-local Python at `.venv/bin/python`, confirmed pinned package versions, package imports, Docker CLI availability, capsule validation, path-leak scan, import smoke test, fixture pipeline, and Git hygiene.
- Capsule validation: passed with 24 table assets, 2 figures, and 47 dependency rows.
- Private data dependency check: passed with 15/15 unique logical paths present and no missing required inputs.
- Coauthor data-room validation: passed with 35 present rows and 2 documented future-extension rows: `seo_offering_terms` and `job_postings`.
- SEC source validation: passed with 7/7 manifest rows present.
- WRDS/market validation: passed with 16/16 manifest rows present.
- Patent data validation: passed with 29/29 manifest rows present.
- Artifact coverage audit: passed with 20 promoted coverage rows and 2 documented not-promoted candidates.
- Reproduction status refresh: 23 table CSV exact matches, 1 C7 format-only CSV delta, and 2 frozen/candidate figure evidence rows.
- Figure evidence refresh: both figure-series CSV evidence files match exactly; generated PDFs remain candidate evidence while frozen manuscript PDFs remain canonical.
- C7 explanation refresh: 16 numeric-string cells differ only at floating-point representation scale, maximum absolute numeric delta is below `1e-10`, and TeX output is byte-identical.
- Whitespace check: `git diff --check` passed.

## Current Release Boundary

- v4.3 remains the frozen computational reference.
- v5.0 editorial source is preserved under `paper/v5_0_editorial_source/` as the presentation benchmark for wording, captions, appendix wrappers, and table notes.
- The v5.0 source is not a numerical freeze unless a later release explicitly promotes it.

## Current Non-Blockers

- Full raw SEC and PatentsView corpora are not committed to Git. Representative source samples, source links, extracted sentences, classifier outputs, patent artifacts, and validation reports are staged or documented for coauthor audit. Full raw mirrors can be added to the private data room if coauthors request bottom-up rebuilds.
- The event/market-return lane remains 2016-2024 because the staged CRSP return extracts stop at 2024-12-31. The annual NLP/patent lane covers 2016-2025.
- Strong washing-pays tests using actual SEO/offering terms are future-data work. The current workstation includes the v4.3 Test 30 share-growth proxy and a schema checker for future SEO/offering-term data.
- Job postings remain a future optional extension.

## Share Readiness Verdict

The package is ready for private coauthor circulation as a two-part workstation: the GitHub repository plus the external private data room. Before formal journal deposit, rerun the same validation sequence and decide whether to promote a new numerical release beyond v4.3.
