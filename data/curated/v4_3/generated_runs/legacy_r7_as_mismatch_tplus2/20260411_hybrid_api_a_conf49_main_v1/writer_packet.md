# Writer Packet

## Metadata
- Test id: `legacy_r7_as_mismatch_tplus2`
- Run id: `20260411_hybrid_api_a_conf49_main_v1`
- Date run: `2026-04-11`
- Script/module path: `semantic_ai_washing.analysis.publication_runs.legacy_r7_as_mismatch_tplus2`
- Annual panel: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`
- Unit of observation: `firm-year`
- Sample filters: `expanded ever-speaker annual panel, 2016-2025; column-specific non-financial / non-utility trims vary by specification`
- Date range: `2016-2025 disclosures with patent lead outcome at t+2`
- N range: `14,968` to `13,737`

## Variable Block
- Dependent variable: `log(1 + AI patents at t+2)`
- Key regressors: `A/S ratio` and `A/S ratio × PatentMismatch`
- Control set: `log assets, leverage, cash/assets, R&D/assets, CAPX/assets, ROA, sales growth, employees`
- Transformations: `patent outcome logged as log(1+x); ratio entered in levels`

## Estimation Block
- Fixed effects: `firm + year FE, industry×year FE, plus trimmed variants across columns`
- Clustering: `firm level`
- Weighting: `unweighted OLS`

## Result Block
- First-spec `A/S ratio`: `0.021**`
- First-spec `A/S ratio × PatentMismatch`: `-0.008`
- One-sentence interpretation: `the strong mismatch penalty fades by t+2, so the credibility signal is sharpest in the near-term patent realization window`
- Candidate use: `appendix / supporting validation table`

## Caption Draft
This table reports the methodology-aligned AI-washing specification on the expanded 2016-2025 ever-speaker annual panel using the longer-horizon outcome log(1 + AI patents) at t+2. Rows report the A/S ratio and its interaction with PatentMismatch, while columns vary the fixed-effects structure and sample trim. Controls are lagged firm characteristics, and standard errors are clustered at the firm level.
