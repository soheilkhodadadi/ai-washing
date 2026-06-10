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
make validate-data-room
make validate-wrds-data
make validate-patent-data
make audit-artifact-coverage
```

Expected current result: all 15 runtime table-dependency paths are present, the WRDS/market validator reports 16 of 16 manifest rows present, and the broad coauthor data-room check reports only explicitly deferred future-extension inputs.

The checker fails for missing `required_current` inputs. It exits cleanly for documented `future_extension` gaps so that coauthors can validate the current v4.3 reproduction surface without inventing an ExecuComp/database artifact.

`make audit-artifact-coverage` applies the stronger v4.3 provenance gate. It checks row counts, file counts, year coverage, and date coverage against `manifests/artifact_provenance_audit.csv`.

`make validate-patent-data` applies the patent-specific coauthor audit gate. It checks the staged final grant/pregrant counts, readable patent/application examples, diagnostics, hybrid company lookup and alias files, patent keyword files, PatentsView source documentation, and patent matching reports against `manifests/patent_data_manifest.csv`.

## Lane-Specific Coverage

Do not require every artifact to cover 2016-2025. v4.3 uses two different data lanes:

- `annual_nlp_patent`: 2016-2025. This includes the canonical annual panel and final hybrid API classifier output with 147,879 AI-related sentences.
- `event_market_return`: 2016-2024. This includes the filing-event estimation sample and CRSP-derived return inputs. This lane stops at 2024 because the staged CRSP/event-return files stop at 2024-12-31.
- `filing_spine_ai_measures`: 2016-2025. These files document filing-level disclosure lineage and WRDS/CRSP bridge construction, but they are not a completed 2025 event-return panel.
- `market_features`: source years through 2024. CRSP monthly and market-index inputs end at 2024-12-31.

See `docs/artifact_coverage_policy.md` before replacing staged artifacts. If a 2025 event-return artifact is found later, treat it as a v5+ extension candidate, not as a silent v4.3 replacement.

## Logical Data Tree

| Manifest path | Runtime path | Classification | Dependency IDs | Used by tests | Notes |
|---|---|---|---|---|---|
| `data/curated/v4_3/comment_letter_event_panel.parquet` | `$AIW_DATA_ROOT/curated/v4_3/comment_letter_event_panel.parquet` | required_current | event_panel | test_20_comment_letter_cleanup | Generated comment-letter event panel from test_19; staged because it is small and required by test_20. |
| `data/curated/v4_3/factor_inputs` | `$AIW_DATA_ROOT/curated/v4_3/factor_inputs` | required_current | factor_root | test_09_factor_adjusted_alpha | Ken French factor cache; can be recreated if internet access and source availability allow. |
| `data/external/execucomp/execucomp_ceo_anncomp_2015_2024.parquet` | `$AIW_DATA_ROOT/external/execucomp/execucomp_ceo_anncomp_2015_2024.parquet` | required_current | execucomp | test_25_exec_incentive_mismatch | Private staged WRDS ExecuComp CEO-row extract; normal reruns do not need WRDS credentials. |
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


## WRDS / Market / Accounting Audit Tree

The WRDS lane has an additional manifest, `manifests/wrds_data_manifest.csv`, because coauthors need to inspect more than the final annual/event panels.

| Logical path group | Runtime location | Purpose |
|---|---|---|
| `data/interim/accounting/` | `$AIW_DATA_ROOT/interim/accounting/` | Compustat fundamentals extract used to audit and rebuild accounting controls. |
| `data/interim/market/` | `$AIW_DATA_ROOT/interim/market/` | CRSP monthly/index inputs, annual market features, daily filing-event returns, filing AI measures, filing spine, and market bridge support. |
| `data/interim/linking/` | `$AIW_DATA_ROOT/interim/linking/` | CIK-GVKEY crosswalk, annual WRDS backbone, and filing-level WRDS bridge. |
| `data/reports/wrds/` | `$AIW_DATA_ROOT/reports/wrds/` | WRDS raw-pull/build reports and unmatched-link diagnostics. |
| `data/docs/wrds/` | `$AIW_DATA_ROOT/docs/wrds/` | Legacy WRDS source-review and bridge-progress notes retained for coauthor audit context. |

Run `make validate-wrds-data` before interpreting market/accounting changes. See `docs/wrds_crsp_compustat_method_note.md` and `docs/wrds_source_inventory.md`.

## Patent Audit Tree

The patent lane has an additional manifest, `manifests/patent_data_manifest.csv`, because this is the construct most likely to draw coauthor or referee scrutiny.

| Logical path group | Runtime location | Purpose |
|---|---|---|
| `data/processed/patents/*.csv` | `$AIW_DATA_ROOT/processed/patents/` | Final grant/pregrant counts, examples, and diagnostics used to audit the patent mismatch construct. |
| `data/metadata/company_identity/*.csv` | `$AIW_DATA_ROOT/metadata/company_identity/` | Hybrid lookup and alias files used for exact normalized company-to-assignee/applicant matching. |
| `data/metadata/patents/*.txt` | `$AIW_DATA_ROOT/metadata/patents/` | Patent AI keyword list and sensitivity keyword lists. |
| `data/reports/patents/*` | `$AIW_DATA_ROOT/reports/patents/` | Patent matching robustness note, fuzzy-sensitivity note, keyword benchmark outputs, and extraction progress logs. |
| `data/raw/patentsview/Guide/*` | `$AIW_DATA_ROOT/raw/patentsview/Guide/` | PatentsView data dictionaries and source documentation. |

The full raw PatentsView TSV mirror is optional for v4.3 reproduction. If coauthors request a full raw-source rebuild, stage grant TSVs under `$AIW_DATA_ROOT/raw/patentsview/granted/` and pregrant TSVs under `$AIW_DATA_ROOT/raw/patentsview/pregrant/`; keep those files outside Git.

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
