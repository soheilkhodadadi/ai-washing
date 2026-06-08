# Private Data Contract

This contract makes the AI Washing private data mirror mechanical for coauthors. The Git repository tracks code, docs, manifests, fixtures, and frozen v4.3 manuscript assets. Private or licensed inputs live outside Git under `AIW_DATA_ROOT`.

## Path Rule

`AIW_DATA_ROOT` is the folder equivalent of the repository's logical `data/` directory. Therefore a manifest path such as:

```text
data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet
```

must be staged as:

```text
$AIW_DATA_ROOT/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet
```

Do not put the Git repository itself inside Dropbox, OneDrive, or another sync folder. Clone the GitHub repository locally, then set `AIW_DATA_ROOT` to a local mirror of the shared private-data folder.

## Validation Command

From the repository root:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make check-private-data
```

Expected current result: 14 of 15 unique logical paths are present. The only documented gap is `data/external/execucomp_or_private_db`, which is a future-extension dependency for `test_25_exec_incentive_mismatch`.

The checker fails for missing `required_current` inputs. It exits cleanly for documented `future_extension` gaps so that coauthors can validate the current v4.3 reproduction surface without inventing an ExecuComp/database artifact.

## Logical Data Tree

| Manifest path | Runtime path | Classification | Dependency IDs | Used by tests | Notes |
|---|---|---|---|---|---|
| `data/curated/v4_3/comment_letter_event_panel.parquet` | `$AIW_DATA_ROOT/curated/v4_3/comment_letter_event_panel.parquet` | required_current | event_panel | test_20_comment_letter_cleanup | Generated comment-letter event panel from test_19; staged because it is small and required by test_20. |
| `data/curated/v4_3/factor_inputs` | `$AIW_DATA_ROOT/curated/v4_3/factor_inputs` | required_current | factor_root | test_09_factor_adjusted_alpha | Ken French factor cache; can be recreated if internet access and source availability allow. |
| `data/external/execucomp_or_private_db` | `$AIW_DATA_ROOT/external/execucomp_or_private_db` | future_extension | execucomp | test_25_exec_incentive_mismatch | Executive compensation data; test_25 currently uses database-backed/private source logic. |
| `data/interim/market/annual_market_features_ever_speaker_2016_2025_hybrid_api_a_conf49_v1.csv` | `$AIW_DATA_ROOT/interim/market/annual_market_features_ever_speaker_2016_2025_hybrid_api_a_conf49_v1.csv` | required_current | market_features | legacy_r1_summary_stats | Annual market features merged to firm-year panel. |
| `data/interim/market/filing_ai_measures_hybrid_api_a_conf49_v1.csv` | `$AIW_DATA_ROOT/interim/market/filing_ai_measures_hybrid_api_a_conf49_v1.csv` | required_current | filing_measures | legacy_classifier_risk_highconf | Filing-level AI measures used by high-confidence classifier-risk checks. |
| `data/interim/market/filing_event_returns_daily_hybrid_api_a_conf49_v1.parquet` | `$AIW_DATA_ROOT/interim/market/filing_event_returns_daily_hybrid_api_a_conf49_v1.parquet` | required_current | daily_returns | legacy_b2_attrition_map | Private daily returns around filing events. |
| `data/interim/market/wrds_crsp_msf_full_sample_v1.parquet` | `$AIW_DATA_ROOT/interim/market/wrds_crsp_msf_full_sample_v1.parquet` | required_current | monthly_returns | test_05_size_heterogeneity, test_09_factor_adjusted_alpha | WRDS/CRSP monthly stock file; licensed/private. |
| `data/interim/market/wrds_crsp_msi_full_sample_v1.parquet` | `$AIW_DATA_ROOT/interim/market/wrds_crsp_msi_full_sample_v1.parquet` | required_current | market_index | test_09_factor_adjusted_alpha | WRDS/CRSP market index; licensed/private. |
| `data/labels/v1/labels_master.parquet` | `$AIW_DATA_ROOT/labels/v1/labels_master.parquet` | support_only | label_base | legacy_b1_measurement_audit | Legacy label base for measurement audit. |
| `data/labels/v2/labels_master_boundary_revised_v1_excluding_heldout_v4.parquet` | `$AIW_DATA_ROOT/labels/v2/labels_master_boundary_revised_v1_excluding_heldout_v4.parquet` | support_only | training_pool | legacy_b1_measurement_audit | Training/calibration pool for measurement audit. |
| `data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet` | `$AIW_DATA_ROOT/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet` | required_current | annual_panel | legacy_a1_mismatch_determinants_full, legacy_a2_mismatch_intensity, legacy_b2_attrition_map, legacy_classifier_risk_highconf, legacy_r1_disclosure_volume, legacy_r1_summary_stats, legacy_r2_ai_focus_timing, legacy_r4_actionable_patent_timing, legacy_r5_speculative_patent_timing, legacy_r7_as_mismatch_tplus2, legacy_r8_mismatch_determinants_reduced, test_05_size_heterogeneity, test_09_factor_adjusted_alpha, test_12_predictive_return_controls, test_13_pre_post_event_path, test_15_matched_ai_talking_sample, test_16_construct_variant_screen, test_17_real_outcome_dynamics, test_20_comment_letter_cleanup, test_25_exec_incentive_mismatch, test_29_sec_ai_washing_enforcement_did, test_30_capital_raising_timing, test_32_market_reaction_in_issue_windows | Private derived annual firm-year panel; needed by most publication tables. |
| `data/processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet` | `$AIW_DATA_ROOT/processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet` | required_current | event_panel | legacy_b2_attrition_map, legacy_r1_summary_stats, test_05_size_heterogeneity, test_09_factor_adjusted_alpha, test_12_predictive_return_controls, test_15_matched_ai_talking_sample, test_32_market_reaction_in_issue_windows | Private filing-event estimation sample; needed by event/market tests. |
| `data/reports/evaluation/selective_defer_heldout_v4_hybrid_api_upgrade_v2.json` | `$AIW_DATA_ROOT/reports/evaluation/selective_defer_heldout_v4_hybrid_api_upgrade_v2.json` | support_only | hybrid_eval | legacy_b1_measurement_audit | Hybrid classifier evaluation report. |
| `data/reports/labels/irr_boundary_revised_v3_rerun_report.json` | `$AIW_DATA_ROOT/reports/labels/irr_boundary_revised_v3_rerun_report.json` | support_only | irr_report | legacy_b1_measurement_audit | Inter-rater/relabeling report for measurement audit. |
| `data/validation/held_out_v4/held_out_sentences_v4.csv` | `$AIW_DATA_ROOT/validation/held_out_v4/held_out_sentences_v4.csv` | support_only | heldout_v4 | legacy_b1_measurement_audit | Held-out validation sample for measurement audit. |

## Checksum Procedure

Private checksum reports should stay outside Git unless they are sanitized. The local/private mirror may contain:

```text
$AIW_DATA_ROOT/private_data_checksum_report.csv
$AIW_DATA_ROOT/private_data_staging_copy_log.csv
```

A coauthor should first run `make check-private-data`, then compare any private checksum report shared through Dropbox/OneDrive. If a checksum differs, do not patch table code first; resolve the staged input mismatch.

## Status Labels

- `required_current`: needed for current v4.3 table reruns.
- `support_only`: needed for validation, audits, or measurement documentation, but not always for a numerical table rerun.
- `future_extension`: intentionally not required for current v4.3 reproduction; document and skip unless that extension is promoted.
- `excluded`: not part of the curated workstation contract.
