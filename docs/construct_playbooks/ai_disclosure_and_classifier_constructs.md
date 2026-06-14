# AI Disclosure And Classifier Constructs

## Purpose

This layer turns SEC filing text into AI disclosure measures. It separates concrete AI deployment language from speculative or irrelevant AI references, then aggregates sentence-level classifications into filing-year and firm-year measures.

## Source Artifacts

- Final classifier output: `data/processed/classifications/classifications_shadow_hybrid_api_a_conf49_v1`
- Extracted sentence support: `data/processed/sec/sentences_clean` and `data/processed/sec/sentences_clean_refresh_2025_v1`
- Label and validation files: `data/labels/`, `data/validation/held_out_v4/`, and `data/reports/evaluation/`
- Source policy and audit notes: `docs/sec_raw_source_policy.md` and `docs/sec_extraction_classification_audit.md`

## v4.3 Definitions

- AI-related sentence: a sentence extracted from cleaned 10-X text by the AI keyword/sentence extraction layer.
- Actionable AI language: concrete deployment, product, workflow, model, or internal-use language.
- Speculative AI language: aspirational or forward-looking AI language with limited operational detail.
- Irrelevant AI language: generic or tangential AI references that should not be treated as the firm's own capability.
- AI Focus and related composition variables: filing/firm-year aggregates built from final classifier outputs.

## Owning Scripts And Tables

- Measurement table: `semantic_ai_washing.analysis.publication_runs.legacy_b1_measurement_audit` (`A1`)
- High-confidence classifier-risk checks: `semantic_ai_washing.analysis.publication_runs.legacy_classifier_risk_highconf` (`A3`, `A4`)
- Summary table: `semantic_ai_washing.analysis.publication_runs.legacy_r1_summary_stats` (`T00`)

## Validation Checks

- `make validate-sec-source`
- `make textual-construct-audit`
- `make TABLE_ID=A1 reproduce-table`
- `make TABLE_ID=A3 reproduce-table`
- `make TABLE_ID=A4 reproduce-table`

## Known Limitations

Short acronyms such as `AI` and `ML` can be ambiguous in text. v4.3 uses the current classifier and validation layer; a future robustness round should add a reviewer-labeled disambiguation layer for short-acronym-only hits and borderline cases.

## Safe Update Path

1. Create a new classifier/output version; do not overwrite the v4.3 classifier folder.
2. Run held-out and stratified validation before aggregation.
3. Rebuild filing-level and annual measures under a new versioned panel path.
4. Update the data product catalog and table workbench only after numerical differences are understood.

## Likely Coauthor Or Referee Questions

- Are AI-related sentences truly about artificial intelligence rather than unrelated acronyms?
- Does the classifier preserve precision in high-stakes constructs such as PatentMismatch?
- Do results survive high-confidence or reviewer-labeled subsets?
