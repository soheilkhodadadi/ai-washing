# Private Data Staging Map

This file summarizes the private/support inputs required for full AI Washing v4.3 table reruns. `manifests/data_dependency_manifest.csv` records paths with a leading `data/` because those are workstation-relative logical paths. For runtime, `AIW_DATA_ROOT` points to the folder equivalent to repository `data/`, so the leading `data/` is removed.

Recommended external data root:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
```

Soheil's current local mirror is:

```bash
export AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data
```

Example: manifest path `data/processed/panel/file.parquet` should be staged at `$AIW_DATA_ROOT/processed/panel/file.parquet`.

## Status Summary

- Dependency rows: 44
- Unique expected paths: 15
- Unique inputs staged in the current private root: 14/15
- Current Phase 2C result: all `required_current` and `support_only` unique inputs found and staged, except the future-extension ExecuComp/private DB placeholder.

## Unique Inputs

| Manifest path | Runtime path under AIW_DATA_ROOT | Dependency IDs | Classification | Manifest status | Phase 2C local staging | Used by tests | Notes |
|---|---|---|---|---|---|---|---|
| `data/curated/v4_3/comment_letter_event_panel.parquet` | `curated/v4_3/comment_letter_event_panel.parquet` | event_panel | required_current | present | staged_in_private_root | test_20_comment_letter_cleanup | Generated comment-letter event panel from test_19; staged because it is small and required by test_20. |
| `data/curated/v4_3/factor_inputs` | `curated/v4_3/factor_inputs` | factor_root | required_current | present | staged_in_private_root | test_09_factor_adjusted_alpha | Ken French factor cache; can be recreated if internet access and source availability allow. |
| `data/external/execucomp_or_private_db` | `external/execucomp_or_private_db` | execucomp | future_extension | missing_private_input | deferred_no_candidate_found | test_25_exec_incentive_mismatch | Executive compensation data; test_25 currently uses database-backed/private source logic. |
| `data/interim/market/annual_market_features_ever_speaker_2016_2025_hybrid_api_a_conf49_v1.csv` | `interim/market/annual_market_features_ever_speaker_2016_2025_hybrid_api_a_conf49_v1.csv` | market_features | required_current | missing_private_input | staged_in_private_root | legacy_r1_summary_stats | Annual market features merged to firm-year panel. |
| `data/interim/market/filing_ai_measures_hybrid_api_a_conf49_v1.csv` | `interim/market/filing_ai_measures_hybrid_api_a_conf49_v1.csv` | filing_measures | required_current | missing_private_input | staged_in_private_root | legacy_classifier_risk_highconf | Filing-level AI measures used by high-confidence classifier-risk checks. |
| `data/interim/market/filing_event_returns_daily_hybrid_api_a_conf49_v1.parquet` | `interim/market/filing_event_returns_daily_hybrid_api_a_conf49_v1.parquet` | daily_returns | required_current | missing_private_input | staged_in_private_root | legacy_b2_attrition_map | Private daily returns around filing events. |
| `data/interim/market/wrds_crsp_msf_full_sample_v1.parquet` | `interim/market/wrds_crsp_msf_full_sample_v1.parquet` | monthly_returns | required_current | missing_private_input | staged_in_private_root | test_05_size_heterogeneity, test_09_factor_adjusted_alpha | WRDS/CRSP monthly stock file; licensed/private. |
| `data/interim/market/wrds_crsp_msi_full_sample_v1.parquet` | `interim/market/wrds_crsp_msi_full_sample_v1.parquet` | market_index | required_current | missing_private_input | staged_in_private_root | test_09_factor_adjusted_alpha | WRDS/CRSP market index; licensed/private. |
| `data/labels/v1/labels_master.parquet` | `labels/v1/labels_master.parquet` | label_base | support_only | missing_private_input | staged_in_private_root | legacy_b1_measurement_audit | Legacy label base for measurement audit. |
| `data/labels/v2/labels_master_boundary_revised_v1_excluding_heldout_v4.parquet` | `labels/v2/labels_master_boundary_revised_v1_excluding_heldout_v4.parquet` | training_pool | support_only | missing_private_input | staged_in_private_root | legacy_b1_measurement_audit | Training/calibration pool for measurement audit. |
| `data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet` | `processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet` | annual_panel | required_current | missing_private_input | staged_in_private_root | most publication tests | Private derived annual firm-year panel; needed by most publication tables. |
| `data/processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet` | `processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet` | event_panel | required_current | missing_private_input | staged_in_private_root | event/market tests | Private filing-event estimation sample; needed by event/market tests. |
| `data/reports/evaluation/selective_defer_heldout_v4_hybrid_api_upgrade_v2.json` | `reports/evaluation/selective_defer_heldout_v4_hybrid_api_upgrade_v2.json` | hybrid_eval | support_only | missing_private_input | staged_in_private_root | legacy_b1_measurement_audit | Hybrid classifier evaluation report. |
| `data/reports/labels/irr_boundary_revised_v3_rerun_report.json` | `reports/labels/irr_boundary_revised_v3_rerun_report.json` | irr_report | support_only | missing_private_input | staged_in_private_root | legacy_b1_measurement_audit | Inter-rater/relabeling report for measurement audit. |
| `data/validation/held_out_v4/held_out_sentences_v4.csv` | `validation/held_out_v4/held_out_sentences_v4.csv` | heldout_v4 | support_only | missing_private_input | staged_in_private_root | legacy_b1_measurement_audit | Held-out validation sample for measurement audit. |

## Private Root Artifacts

The private root also contains binary/archive artifacts moved out of Git, including the small comment-letter event panel, Ken French factor cache files, and Test 25 generated parquet evidence. Checksums are recorded outside Git at:

```text
$AIW_DATA_ROOT/private_data_checksum_report.csv
$AIW_DATA_ROOT/private_data_staging_copy_log.csv
```
