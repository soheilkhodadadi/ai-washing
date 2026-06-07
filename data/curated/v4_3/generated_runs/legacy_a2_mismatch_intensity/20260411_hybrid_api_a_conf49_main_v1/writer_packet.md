# Writer Packet

## Metadata
- Test id: `legacy_a2_mismatch_intensity`
- Run id: `20260411_hybrid_api_a_conf49_main_v1`
- Date run: `2026-04-11`
- Script/module path: `semantic_ai_washing.analysis.publication_runs.legacy_a2_mismatch_intensity`
- Annual panel: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`
- Unit of observation: `firm`
- Sample filters: `baseline firm characteristics measured in 2016; intensity outcome aggregated over AI-talking years in the expanded 2016-2025 panel`
- Date range: `baseline covariates in 2016, outcome window 2016-2025`
- N range: `2,680` to `1,331`

## Variable Block
- Dependent variable: `share of AI-talking years flagged as PatentMismatch during 2016-2025`
- Key regressors: `log assets, cash/assets, leverage, R&D/assets, CAPX/assets, ROA, employees (k)`
- Baseline year: `2016`

## Estimation Block
- Fixed effects: `baseline SIC2 industry FE`
- Clustering: `industry level`
- Weighting: `unweighted cross-sectional OLS`

## Result Block
- Multivariate `Leverage`: `0.042`
- Multivariate `CAPX/assets`: `-0.434*`
- Multivariate `R&D/assets`: `-0.078`
- Multivariate N: `1,331`
- One-sentence interpretation: `conditional mismatch intensity is directionally higher for more levered firms and lower for higher-investment firms, but the full-baseline complete-case sample is thin`
- Candidate use: `appendix only`

## Caption Draft
This appendix table reports full-baseline cross-sectional regressions for PatentMismatch intensity on the expanded 2016-2025 panel. The dependent variable is the share of AI-talking years flagged as mismatch, and baseline covariates are measured in 2016. All specifications include baseline industry fixed effects, and standard errors are clustered at the industry level.
