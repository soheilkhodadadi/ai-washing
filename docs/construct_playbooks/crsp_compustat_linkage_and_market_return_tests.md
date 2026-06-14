# CRSP/Compustat Linkage And Market-Return Tests

## Purpose

This layer connects SEC filings and firm-years to accounting controls, CRSP returns, market features, and factor-return tests.

## Source Artifacts

- Compustat extract: `data/interim/accounting/wrds_comp_funda_full_sample_v1.parquet`
- CRSP monthly/index/daily files: `data/interim/market/`
- Linkage files and unmatched diagnostics: `data/interim/linking/` and `data/reports/wrds/`
- Factor inputs: `data/curated/v4_3/factor_inputs`

## v4.3 Definitions

The annual lane covers 2016-2025. The event/market-return lane covers 2016-2024 because staged CRSP return data stop at 2024-12-31. Do not treat the missing 2025 event-return panel as an error in v4.3.

## Owning Scripts And Tables

- Factor alpha: `test_09_factor_adjusted_alpha` (`T09`)
- Size heterogeneity: `test_05_size_heterogeneity` (`C4`)
- Return controls: `test_12_predictive_return_controls` (`C6`)
- Matched AI-talking sample: `test_15_matched_ai_talking_sample` (`C7`)

## Validation Checks

- `make validate-wrds-data`
- `make TABLE_ID=T09 reproduce-table`
- `make TABLE_ID=C6 reproduce-table`
- `make c7-format-delta`

## Known Limitations

The event/market lane cannot include 2025 filing returns without a CRSP refresh. Appendix Table C7 has a documented numeric-string format-only CSV delta; the generated TeX is exact.

## Safe Update Path

1. Refresh WRDS/CRSP data only with local credentials outside Git.
2. Rebuild bridge files and unmatched diagnostics.
3. Validate row counts and date coverage before rerunning return tests.
4. Stage any 2025 event-return expansion as a v5+ lane.

## Likely Coauthor Or Referee Questions

- Are return tests sensitive to CRSP link quality and unmatched filings?
- Do factor results survive alternative horizons or weighting?
- Are 2025 annual observations incorrectly entering return-event tests?
