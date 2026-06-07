# Writer Packet

## Metadata
- Test id: `legacy_a1_mismatch_determinants_full`
- Run id: `20260411_hybrid_api_a_conf49_main_v1`
- Date run: `2026-04-11`
- Script/module path: `semantic_ai_washing.analysis.publication_runs.legacy_a1_mismatch_determinants_full`
- Annual panel: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`
- Unit of observation: `firm`
- Sample filters: `baseline firm characteristics measured in 2016; mismatch outcome aggregated over expanded 2016-2025 panel`
- Date range: `baseline covariates in 2016, outcome window 2016-2025`
- N range: `2,680` to `1,331`

## Variable Block
- Dependent variable: `indicator for whether a firm records at least one PatentMismatch incident during 2016-2025`
- Key regressors: `log assets, cash/assets, leverage, R&D/assets, CAPX/assets, ROA, employees (k)`
- Baseline year: `2016`

## Estimation Block
- Fixed effects: `baseline SIC2 industry FE`
- Clustering: `industry level`
- Weighting: `unweighted cross-sectional OLS`

## Result Block
- Multivariate `Log assets`: `0.009**`
- Multivariate `ROA`: `-0.001`
- Multivariate `R&D/assets`: `-0.025`
- Multivariate `Leverage`: `0.028`
- Multivariate N: `1,331`
- One-sentence interpretation: `full-baseline determinants are directionally similar to the reduced table but become much noisier once the sample is forced onto the smaller complete-case subset`
- Candidate use: `appendix only`

## Caption Draft
This appendix table reports full-baseline cross-sectional regressions for whether a firm records at least one PatentMismatch incident on the expanded 2016-2025 panel. Baseline covariates are measured in 2016 and include log assets, cash/assets, leverage, R&D/assets, CAPX/assets, ROA, and employees. All specifications include baseline industry fixed effects, and standard errors are clustered at the industry level.
