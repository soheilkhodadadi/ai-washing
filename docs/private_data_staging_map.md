# Private Data Staging Map

This file summarizes the private/support inputs required for full AI Washing v4.3 table reruns. `manifests/data_dependency_manifest.csv` records paths with a leading `data/` because those are workstation-relative logical paths. For runtime, `AIW_DATA_ROOT` points to the folder equivalent to repository `data/`, so the leading `data/` is removed.

Recommended external data root:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
```

Example: manifest path `data/processed/panel/file.parquet` should be staged at `$AIW_DATA_ROOT/processed/panel/file.parquet`.

## Status Summary

- Dependency rows: 44
- Unique expected paths: 15
- Unique inputs staged in the current private root: 15/15
- Current Phase 3F result: table-rerun private inputs are staged, and lane-specific coverage is enforced separately by `make audit-artifact-coverage`.
- Important distinction: annual NLP/patent artifacts cover 2016-2025; event/market-return artifacts cover 2016-2024 because v4.3 CRSP/event-return inputs stop at 2024-12-31.

## Unique Inputs

| Manifest path | Runtime path under AIW_DATA_ROOT | Dependency IDs | Classification | Manifest status | Used by tests | Notes |
|---|---|---|---|---|---|---|
| `data/curated/v4_3/comment_letter_event_panel.parquet` | `curated/v4_3/comment_letter_event_panel.parquet` | event_panel | required_current | present | test_20_comment_letter_cleanup | Canonical v4.3 event-market estimation sample; 7,355 filing events, 2016-2024 because staged CRSP returns stop 2024-12-31. |
| `data/curated/v4_3/factor_inputs` | `curated/v4_3/factor_inputs` | factor_root | required_current | present | test_09_factor_adjusted_alpha | Ken French factor cache; can be recreated if internet access and source availability allow. |
| `data/external/execucomp/execucomp_ceo_anncomp_2015_2024.parquet` | `external/execucomp/execucomp_ceo_anncomp_2015_2024.parquet` | execucomp | required_current | present_private_root | test_25_exec_incentive_mismatch | Private staged WRDS ExecuComp CEO-row extract, 2015-2024; normal reruns do not require credentials. |
| `data/interim/market/annual_market_features_ever_speaker_2016_2025_hybrid_api_a_conf49_v1.csv` | `interim/market/annual_market_features_ever_speaker_2016_2025_hybrid_api_a_conf49_v1.csv` | market_features | required_current | present_private_root | legacy_r1_summary_stats | CRSP-derived annual market features; observed feature years 2015-2024. |
| `data/interim/market/filing_ai_measures_hybrid_api_a_conf49_v1.csv` | `interim/market/filing_ai_measures_hybrid_api_a_conf49_v1.csv` | filing_measures | required_current | present_private_root | legacy_classifier_risk_highconf | Filing-level AI disclosure measures for the 2016-2025 filing spine; disclosure lineage, not completed return-event panel. |
| `data/interim/market/filing_event_returns_daily_hybrid_api_a_conf49_v1.parquet` | `interim/market/filing_event_returns_daily_hybrid_api_a_conf49_v1.parquet` | daily_returns | required_current | present_private_root | legacy_b2_attrition_map | Daily return-event cache for the 2016-2024 v4.3 event-market lane. |
| `data/interim/market/wrds_crsp_msf_full_sample_v1.parquet` | `interim/market/wrds_crsp_msf_full_sample_v1.parquet` | monthly_returns | required_current | present_private_root | test_05_size_heterogeneity, test_09_factor_adjusted_alpha | WRDS/CRSP monthly stock file extract; date range 2015-01-30 to 2024-12-31. |
| `data/interim/market/wrds_crsp_msi_full_sample_v1.parquet` | `interim/market/wrds_crsp_msi_full_sample_v1.parquet` | market_index | required_current | present_private_root | test_09_factor_adjusted_alpha | WRDS/CRSP market index extract; date range 2015-01-30 to 2024-12-31. |
| `data/labels/v1/labels_master.parquet` | `labels/v1/labels_master.parquet` | label_base | support_only | present_private_root | legacy_b1_measurement_audit | Legacy label base for measurement audit. |
| `data/labels/v2/labels_master_boundary_revised_v1_excluding_heldout_v4.parquet` | `labels/v2/labels_master_boundary_revised_v1_excluding_heldout_v4.parquet` | training_pool | support_only | present_private_root | legacy_b1_measurement_audit | Training/calibration pool for measurement audit. |
| `data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet` | `processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet` | annual_panel | required_current | present_private_root | most publication tests | Canonical 99-column v4.3 annual NLP/patent panel; 50,840 firm-years, 2016-2025. |
| `data/processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet` | `processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet` | event_panel | required_current | present_private_root | legacy_b2_attrition_map, legacy_r1_summary_stats, test_05_size_heterogeneity, test_09_factor_adjusted_alpha, test_12_predictive_return_controls, test_15_matc... | Canonical v4.3 event-market estimation sample; 7,355 filing events, 2016-2024 because staged CRSP returns stop 2024-12-31. |
| `data/reports/evaluation/selective_defer_heldout_v4_hybrid_api_upgrade_v2.json` | `reports/evaluation/selective_defer_heldout_v4_hybrid_api_upgrade_v2.json` | hybrid_eval | support_only | present_private_root | legacy_b1_measurement_audit | Hybrid classifier evaluation report. |
| `data/reports/labels/irr_boundary_revised_v3_rerun_report.json` | `reports/labels/irr_boundary_revised_v3_rerun_report.json` | irr_report | support_only | present_private_root | legacy_b1_measurement_audit | Inter-rater/relabeling report for measurement audit. |
| `data/validation/held_out_v4/held_out_sentences_v4.csv` | `validation/held_out_v4/held_out_sentences_v4.csv` | heldout_v4 | support_only | present_private_root | legacy_b1_measurement_audit | Held-out validation sample for measurement audit. |

## Artifact Coverage Audit

The staging map answers whether required private paths exist. The artifact coverage audit answers whether the staged files are the correct v4.3 artifacts. Run both before sharing or replacing data:

```bash
make check-private-data
make validate-data-room
make audit-artifact-coverage
```

See `docs/artifact_coverage_policy.md` and `manifests/artifact_provenance_audit.csv` for the lane-specific coverage gate.

## Private Root Artifacts

The private root also contains binary/archive artifacts moved out of Git, including the small comment-letter event panel, Ken French factor cache files, representative SEC samples, final classifier outputs, sentence extracts, lineage panel CSVs, and Test 25 generated parquet evidence. Checksums are recorded outside Git at:

```text
$AIW_DATA_ROOT/private_data_checksum_report.csv
$AIW_DATA_ROOT/private_data_staging_copy_log.csv
```
