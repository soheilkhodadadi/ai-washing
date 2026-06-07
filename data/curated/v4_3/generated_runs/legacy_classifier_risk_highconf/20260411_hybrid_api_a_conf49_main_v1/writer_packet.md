# Writer Packet

## Metadata
- Test id: `legacy_classifier_risk_highconf`
- Run id: `20260411_hybrid_api_a_conf49_main_v1`
- Date run: `2026-04-11`
- Script/module path: `semantic_ai_washing.analysis.publication_runs.legacy_classifier_risk_highconf`
- Annual panel: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`
- Filing measure input: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/interim/market/filing_ai_measures_hybrid_api_a_conf49_v1.csv`
- High-confidence rule: `keep firm-years with api_a_sentence_count == 0 in the filing-year aggregate`
- Underlying selective-defer trigger: `local_confidence < 0.49` sent rows to API-A under the conf49 policy

## Sample Block
- Panel rows retained: `7,287` of `50,840`
- AI-talking rows retained: `7,287` of `13,777`
- Unit of observation: `firm-year`

## Table C1
- Purpose: `composition timing robustness on all-local firm-years`
- Actionable t+1 coefficient: `0.035`
- Speculative-only t+1 coefficient: `-0.076`

## Table C2
- Purpose: `main mismatch regression on all-local firm-years`
- First-spec `A/S ratio`: `0.085*`
- First-spec `A/S ratio × PatentMismatch`: `-0.065`

## Interpretation
- If the main signs survive on this all-local subset, the core disclosure-to-patent patterns are not being mechanically driven by low-confidence/API-routed sentence years.
- Candidate use: `appendix robustness block required by Rubric 2.0`
