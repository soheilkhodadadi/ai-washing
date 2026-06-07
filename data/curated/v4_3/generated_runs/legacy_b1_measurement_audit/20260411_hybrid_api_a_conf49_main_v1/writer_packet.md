# Writer Packet

## Metadata
- Test id: `legacy_b1_measurement_audit`
- Run id: `20260411_hybrid_api_a_conf49_main_v1`
- Date run: `2026-04-11`
- Script/module path: `semantic_ai_washing.analysis.publication_runs.legacy_b1_measurement_audit`

## Source Artifacts
- Label base: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/labels/v1/labels_master.parquet`
- Leakage-safe training pool: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/labels/v2/labels_master_boundary_revised_v1_excluding_heldout_v4.parquet`
- Heldout-v4 benchmark: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/validation/held_out_v4/held_out_sentences_v4.csv`
- IRR rerun report: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/reports/labels/irr_boundary_revised_v3_rerun_report.json`
- Hybrid evaluation report: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/reports/evaluation/selective_defer_heldout_v4_hybrid_api_upgrade_v2.json`
- Scored benchmark used by the hybrid evaluation: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/validation/held_out_v4/held_out_sentences_v4_hybrid_api_upgrade_v2_scored.csv`

## Main Numbers
- Adjudicated sentence base: `551` rows
- Leakage-safe training/calibration pool: `431` rows
- Heldout-v4 benchmark: `120` rows
- Human-human IRR rerun: kappa `0.850`, `12` resolved disagreements
- Selected hybrid policy `api_a_conf_or_margin`: accuracy `85.0%`, macro-F1 `83.6%`, binary relevance `91.7%`, A/S `86.5%`

## Caption Draft
This appendix table summarizes the measurement audit underlying the disclosure-classification layer. It reports the size of the adjudicated sentence base, the leakage-safe training pool used for model calibration, the current adjudicated heldout-v4 benchmark, the human-human IRR rerun, and the heldout-v4 evaluation of the selected hybrid policy. The final deployment posture uses targeted API-A deferral on low-confidence rows and improves materially over the local-only baseline.
