# Selected Table Reproduction Status

This report records the Phase 2D selected rerun gate for `T00`, `T16`, `T17`, `T09`, and `T30`. Generated outputs are intentionally ignored by Git; this report preserves the comparison result.

## Summary

- Selected tables rerun: 5
- CSV/numeric matches against frozen generated evidence: 5/5
- TeX exact matches against frozen generated evidence: 1/5
- Interpretation: the numerical table payloads reproduce exactly for all selected targets. TeX deltas are wrapper/export-level differences and should not be treated as numerical differences without further inspection.

## Table-Level Status

| Table | Test ID | CSV/numeric status | TeX status | Reproduced CSV | Reference CSV |
|---|---|---|---|---|---|
| T00 | `legacy_r1_summary_stats` | `exact_match` | `exact_match` | `outputs/paper_exports/tables/legacy_r1_summary_stats_20260412_hybrid_api_a_conf49_main_v2.csv` | `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_r1_summary_stats_20260412_hybrid_api_a_conf49_main_v2.csv` |
| T16 | `test_16_construct_variant_screen` | `exact_match` | `content_delta` | `outputs/paper_exports/tables/test_16_construct_variant_screen_20260422_aiw_v3_1_test_16_construct_variant_screen_main_v1.csv` | `data/curated/v4_3/generated_exports/paper/generated/v3_1/tables/test_16_construct_variant_screen_20260422_aiw_v3_1_test_16_construct_variant_screen_main_v1.csv` |
| T17 | `test_17_real_outcome_dynamics` | `exact_match` | `content_delta` | `outputs/paper_exports/tables/test_17_real_outcome_dynamics_20260422_aiw_v3_1_test_17_real_outcome_dynamics_main_v1.csv` | `data/curated/v4_3/generated_exports/paper/generated/v3_1/tables/test_17_real_outcome_dynamics_20260422_aiw_v3_1_test_17_real_outcome_dynamics_main_v1.csv` |
| T30 | `test_30_capital_raising_timing` | `exact_match` | `content_delta` | `outputs/paper_exports/tables/test_30_capital_raising_timing_20260423_aiw_v3_2_test_30_capital_raising_timing_main_v1.csv` | `data/curated/v4_3/generated_exports/paper/generated/v3_2/tables/test_30_capital_raising_timing_20260423_aiw_v3_2_test_30_capital_raising_timing_main_v1.csv` |
| T09 | `test_09_factor_adjusted_alpha` | `exact_match` | `content_delta` | `outputs/paper_exports/tables/test_09_factor_adjusted_alpha_20260422_aiw_v3_1_test_09_factor_adjusted_alpha_main_v1.csv` | `data/curated/v4_3/generated_exports/paper/generated/v3_1/tables/test_09_factor_adjusted_alpha_20260422_aiw_v3_1_test_09_factor_adjusted_alpha_main_v1.csv` |

## Gate Result

Phase 2D selected-table numerical gate: **passed**. No selected table has an unexplained numerical difference at the CSV payload level.
