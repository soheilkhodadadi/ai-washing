# Paper Table Workbench

This workbench maps each v4.3 manuscript table and figure to the empirical question, data product, script, and safe modification path. It is designed for coauthors who want to inspect, rerun, or extend a specific part of the paper without reverse-engineering older development workspaces.

Use this document with `manifests/paper_table_workbench.csv` when changing a table. The CSV is the machine-readable version; this Markdown file is the readable guide.

## How To Use

1. Find the manuscript table or figure below.
2. Review the empirical question, data product, and main constructs.
3. Run the listed command from the repository root after setting `AIW_DATA_ROOT`.
4. Modify the owning script only after checking the safe-modification note and keeping v4.3 outputs as the frozen reference.

For setup, start with `README_START_HERE.md` or `docs/docker_quickstart.md`. For private data paths, use `docs/private_data_contract.md`.

## Main Text

### Figure 1: PatentMismatch surge through 2025

- Asset ID: `F1`
- Paper source: `figures/figure1_main.pdf`
- Empirical question: How did the share of AI-talking firm-years classified as PatentMismatch evolve through the 2025 refresh?
- Primary data product: Canonical annual AI/patent panel; figure-series CSV generated from the disclosure-volume script.
- Main constructs: AI-talking firm-year, PatentMismatch, annual disclosure/patent lane, year.
- Owning script: `semantic_ai_washing.analysis.publication_runs.legacy_r1_disclosure_volume`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make reproduce-figures`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_r1_disclosure_volume_20260411_hybrid_api_a_conf49_main_v1_series.csv | data/curated/v4_3/generated_exports/paper/generated/figures/legacy_r1_disclosure_volume_20260411_hybrid_api_a_conf49_main_v1.pdf | data/curated/v4_3/generated_runs/legacy_r1_disclosure_volume/20260411_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use to inspect the headline time-series pattern that motivates the paper.
- Safe modifications: Change sample years, patent weakness definition, or plotting style; keep the frozen v4.3 PDF as the reference asset until a new release is promoted.
- Extension relevance: Useful for checking whether future v5+ panels alter the central time-series narrative.
- Notes: Frozen v4.3 manuscript PDF remains canonical; candidate regeneration evidence is documented in docs/figure_reproduction_status.md.

### Main Table 1: Expanded-panel summary statistics and sample coverage

- Asset ID: `T00`
- Paper source: `table_inputs/test_00_summary_stats.tex`
- Empirical question: What is the scale, coverage, and baseline distribution of the annual panel and filing-event sample?
- Primary data product: Canonical annual AI/patent panel plus filing-event estimation sample and market-feature inputs.
- Main constructs: AI sentence counts, actionable/speculative/irrelevant classes, AI Focus, CredAI, AS ratio, PatentMismatch, controls, event returns.
- Owning script: `semantic_ai_washing.analysis.publication_runs.legacy_r1_summary_stats`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=T00 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_r1_summary_stats_20260412_hybrid_api_a_conf49_main_v2.csv | data/curated/v4_3/generated_exports/paper/generated/latex/legacy_r1_summary_stats_20260412_hybrid_api_a_conf49_main_v2.tex | data/curated/v4_3/generated_runs/legacy_r1_summary_stats/20260412_hybrid_api_a_conf49_main_v2`
- Coauthor use: Start here when checking whether row counts, sentence counts, and data-lane coverage match the manuscript.
- Safe modifications: Audit sample filters, control definitions, winsorization, and summary rows; do not silently replace the v4.3 reference counts.
- Extension relevance: Anchor for any future refresh because it exposes changes in sample coverage immediately.
- Notes: Expected headline anchors include 50,840 firm-years, 147,879 final classified AI sentences, and 7,355 filing-event observations.

### Main Table 2: Construct-variant screen for future AI realization

- Asset ID: `T16`
- Paper source: `table_inputs/test_16_construct_variant_screen.tex`
- Empirical question: Which low-credibility disclosure construct best predicts future AI patent realization?
- Primary data product: Canonical annual AI/patent panel with grant and application horizons.
- Main constructs: Canonical PatentMismatch, strict grant mismatch, application mismatch, low credibility only, weak patent only, future AI patents/applications.
- Owning script: `semantic_ai_washing.analysis.publication_runs.test_16_construct_variant_screen`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=T16 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/v3_1/tables/test_16_construct_variant_screen_20260422_aiw_v3_1_test_16_construct_variant_screen_main_v1.csv | data/curated/v4_3/generated_exports/paper/generated/v3_1/latex/test_16_construct_variant_screen_20260422_aiw_v3_1_test_16_construct_variant_screen_main_v1.tex | data/curated/v4_3/generated_runs/test_16_construct_variant_screen/20260422_aiw_v3_1_test_16_construct_variant_screen_main_v1`
- Coauthor use: Use to evaluate whether the retained PatentMismatch definition is empirically defensible.
- Safe modifications: Add construct variants, change patent horizons, or compare application/grant definitions while preserving the original v4.3 rows.
- Extension relevance: Directly supports future construct-validity and reviewer robustness rounds.
- Notes: Selected reproduction gate table.

### Main Table 3: Real-outcome dynamics in the AI-talking sample

- Asset ID: `T17`
- Paper source: `table_inputs/test_17_real_outcome_dynamics.tex`
- Empirical question: Do low-credibility AI talkers subsequently realize weaker real outcomes?
- Primary data product: Canonical annual AI/patent panel with future innovation and operating outcomes.
- Main constructs: PatentMismatch, future AI patenting, future applications, firm controls, outcome horizons.
- Owning script: `semantic_ai_washing.analysis.publication_runs.test_17_real_outcome_dynamics`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=T17 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/v3_1/tables/test_17_real_outcome_dynamics_20260422_aiw_v3_1_test_17_real_outcome_dynamics_main_v1.csv | data/curated/v4_3/generated_exports/paper/generated/v3_1/latex/test_17_real_outcome_dynamics_20260422_aiw_v3_1_test_17_real_outcome_dynamics_main_v1.tex | data/curated/v4_3/generated_runs/test_17_real_outcome_dynamics/20260422_aiw_v3_1_test_17_real_outcome_dynamics_main_v1`
- Coauthor use: Use to inspect the economic meaning of the disclosure construct beyond text classification.
- Safe modifications: Change horizons, add controls, split by size or industry, or use application-based outcomes.
- Extension relevance: Natural starting point for the builder-hides and real-capability extension lanes.
- Notes: Selected reproduction gate table.

### Main Table 4: Disclosure cleanup after SEC comment-letter scrutiny

- Asset ID: `T20`
- Paper source: `table_inputs/test_20_comment_letter_cleanup.tex`
- Empirical question: Do firms clean up low-credibility AI disclosure after SEC comment-letter scrutiny?
- Primary data product: Comment-letter event panel linked to the annual AI/patent panel.
- Main constructs: SEC comment-letter event, PatentMismatch, AI Focus, disclosure cleanup, post-event timing.
- Owning script: `semantic_ai_washing.analysis.publication_runs.test_20_comment_letter_cleanup`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=T20 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/v3_2/tables/test_20_comment_letter_cleanup_20260423_aiw_v3_2_test_20_comment_letter_cleanup_main_v1.csv | data/curated/v4_3/generated_exports/paper/generated/v3_2/latex/test_20_comment_letter_cleanup_20260423_aiw_v3_2_test_20_comment_letter_cleanup_main_v1.tex | data/curated/v4_3/generated_runs/test_20_comment_letter_cleanup/20260423_aiw_v3_2_test_20_comment_letter_cleanup_main_v1`
- Coauthor use: Use to verify the regulatory-scrutiny channel and inspect event timing assumptions.
- Safe modifications: Change event windows, add fixed effects, narrow comments to AI-related letters if data are extended.
- Extension relevance: Supports future enforcement/scrutiny tests and regulatory mechanism refinements.
- Notes: Use the private comment-letter event panel staged under AIW_DATA_ROOT.

### Main Table 5: SEC AI-washing enforcement salience and disclosure cleanup

- Asset ID: `T29`
- Paper source: `table_inputs/test_29_sec_ai_washing_enforcement_did.tex`
- Empirical question: Does SEC AI-washing enforcement salience predict disclosure cleanup?
- Primary data product: Annual AI/patent panel with SEC enforcement-salience timing.
- Main constructs: Post-enforcement salience, PatentMismatch, AI Focus, disclosure cleanup, event timing.
- Owning script: `semantic_ai_washing.analysis.publication_runs.test_29_sec_ai_washing_enforcement_did`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=T29 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/v3_2/tables/test_29_sec_ai_washing_enforcement_did_20260423_aiw_v3_2_test_29_sec_ai_washing_enforcement_did_main_v1.csv | data/curated/v4_3/generated_exports/paper/generated/v3_2/latex/test_29_sec_ai_washing_enforcement_did_20260423_aiw_v3_2_test_29_sec_ai_washing_enforcement_did_main_v1.tex | data/curated/v4_3/generated_runs/test_29_sec_ai_washing_enforcement_did/20260423_aiw_v3_2_test_29_sec_ai_washing_enforcement_did_main_v1`
- Coauthor use: Use to inspect the enforcement-salience design and its treatment/control timing.
- Safe modifications: Change enforcement dates, treatment definitions, or pre/post windows while keeping the v4.3 baseline documented.
- Extension relevance: Useful if the paper later reframes AI washing around regulatory attention.
- Notes: Full reproduction table with exact generated CSV evidence.

### Main Table 6: Executive incentives and low-credibility AI disclosure

- Asset ID: `T25`
- Paper source: `table_inputs/test_25_exec_incentive_mismatch.tex`
- Empirical question: Are executive incentives associated with low-credibility AI disclosure?
- Primary data product: Canonical annual AI/patent panel merged with staged private ExecuComp CEO compensation extract.
- Main constructs: PatentMismatch, equity incentives, option incentives, CEO compensation measures, firm controls.
- Owning script: `semantic_ai_washing.analysis.publication_runs.test_25_exec_incentive_mismatch`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=T25 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/v3_2/tables/test_25_exec_incentive_mismatch_20260423_aiw_v3_2_test_25_exec_incentive_mismatch_main_v1.csv | data/curated/v4_3/generated_exports/paper/generated/v3_2/latex/test_25_exec_incentive_mismatch_20260423_aiw_v3_2_test_25_exec_incentive_mismatch_main_v1.tex | data/curated/v4_3/generated_runs/test_25_exec_incentive_mismatch/20260423_aiw_v3_2_test_25_exec_incentive_mismatch_main_v1`
- Coauthor use: Use to inspect the managerial-incentive channel and rerun with alternative compensation variables.
- Safe modifications: Change ExecuComp measures or sample restrictions; WRDS refresh must remain explicit and local.
- Extension relevance: Feeds governance and incentive-based interpretations of AI disclosure choices.
- Notes: Normal reruns use the staged ExecuComp cache; credentials are not required.

### Main Table 7: Capital-raising timing and low-credibility AI disclosure

- Asset ID: `T30`
- Paper source: `table_inputs/test_30_capital_raising_timing.tex`
- Empirical question: Is low-credibility AI disclosure concentrated before large share-growth capital-raising windows?
- Primary data product: Canonical annual AI/patent panel with CRSP share-outstanding growth proxy.
- Main constructs: PatentMismatch, next-year CRSP shrout growth above 5 percent, capital-raising proxy, controls.
- Owning script: `semantic_ai_washing.analysis.publication_runs.test_30_capital_raising_timing`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=T30 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/v3_2/tables/test_30_capital_raising_timing_20260423_aiw_v3_2_test_30_capital_raising_timing_main_v1.csv | data/curated/v4_3/generated_exports/paper/generated/v3_2/latex/test_30_capital_raising_timing_20260423_aiw_v3_2_test_30_capital_raising_timing_main_v1.tex | data/curated/v4_3/generated_runs/test_30_capital_raising_timing/20260423_aiw_v3_2_test_30_capital_raising_timing_main_v1`
- Coauthor use: Use to inspect the current financing-timing proxy before adding actual SEO/offering-term data.
- Safe modifications: Change issuance threshold, window, or controls; stronger offering-terms data should be added as a new extension dataset.
- Extension relevance: Starting point for the washing-pays extension.
- Notes: Selected reproduction gate table; current result is a proxy screen, not an SEO terms test.

### Main Table 8: Factor-adjusted calendar-time long-short alpha after AI filing signals

- Asset ID: `T09`
- Paper source: `table_inputs/test_09_factor_adjusted_alpha.tex`
- Empirical question: Do long credible-AI / short mismatch portfolios earn factor-adjusted returns after AI filings?
- Primary data product: Filing-event estimation sample, CRSP monthly returns, CRSP market index, and Ken French factor cache.
- Main constructs: Credible AI filer, mismatch AI filer, calendar-time portfolios, CAPM, FF3, FF5, momentum alpha.
- Owning script: `semantic_ai_washing.analysis.publication_runs.test_09_factor_adjusted_alpha`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=T09 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/v3_1/tables/test_09_factor_adjusted_alpha_20260422_aiw_v3_1_test_09_factor_adjusted_alpha_main_v1.csv | data/curated/v4_3/generated_exports/paper/generated/v3_1/latex/test_09_factor_adjusted_alpha_20260422_aiw_v3_1_test_09_factor_adjusted_alpha_main_v1.tex | data/curated/v4_3/generated_runs/test_09_factor_adjusted_alpha/20260422_aiw_v3_1_test_09_factor_adjusted_alpha_main_v1`
- Coauthor use: Use to inspect market-pricing implications and factor-model sensitivity.
- Safe modifications: Change holding horizons, weighting, factor set, or portfolio-leg definitions.
- Extension relevance: Supports future market-efficiency and investor-response revisions.
- Notes: Selected reproduction gate table; event/market lane is 2016-2024 for v4.3.

## Appendix A: Measurement And Sample

### Appendix Table A1: Measurement audit of the disclosure-classification layer

- Asset ID: `A1`
- Paper source: `table_inputs/appendix/appendix_A1_measurement_audit.tex`
- Empirical question: How reliable is the disclosure-classification layer?
- Primary data product: Human labels, held-out validation files, classifier evaluation reports, and IRR reports.
- Main constructs: Actionable, speculative, irrelevant labels, held-out accuracy, macro-F1, Cohen kappa, defer policy.
- Owning script: `semantic_ai_washing.analysis.publication_runs.legacy_b1_measurement_audit`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=A1 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_b1_measurement_audit_20260411_hybrid_api_a_conf49_main_v1.csv | data/curated/v4_3/generated_runs/legacy_b1_measurement_audit/20260411_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use to audit whether the text-classification layer is strong enough for the empirical tests.
- Safe modifications: Add new labeled examples or evaluation slices; keep held-out leakage controls explicit.
- Extension relevance: Natural home for the future acronym-disambiguation and reviewer-labeled robustness layer.
- Notes: Generated CSV/MD artifacts are the lineage source; manuscript TeX is a formatted appendix input.

### Appendix Table A2: Attrition map for the expanded 2016--2025 AI-washing sample

- Asset ID: `A2`
- Paper source: `table_inputs/appendix/appendix_A2_attrition_map.tex`
- Empirical question: Where do observations enter or leave the expanded AI-washing sample?
- Primary data product: Canonical annual panel, filing-event sample, and staged market-return inputs.
- Main constructs: Sample attrition, annual panel rows, AI-talking rows, filing-event rows, usable return outcomes.
- Owning script: `semantic_ai_washing.analysis.publication_runs.legacy_b2_attrition_map`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=A2 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_b2_attrition_map_20260411_hybrid_api_a_conf49_main_v1.csv | data/curated/v4_3/generated_runs/legacy_b2_attrition_map/20260411_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use to locate attrition points before changing samples or adding new years.
- Safe modifications: Add attrition rows for any new data source or stricter sample filter.
- Extension relevance: Protects future extension tests from unexplained sample shifts.
- Notes: Generated CSV/MD artifacts are the lineage source.

### Appendix Table A3: Classifier-risk robustness: high-confidence composition tests

- Asset ID: `A3`
- Paper source: `table_inputs/appendix/appendix_A3_highconf_composition.tex`
- Empirical question: Do high-confidence classifier subsets preserve the disclosure-composition patterns?
- Primary data product: Final classifier outputs, filing-level AI measures, and annual panel.
- Main constructs: Classifier confidence, actionable/speculative composition, AI Focus, PatentMismatch.
- Owning script: `semantic_ai_washing.analysis.publication_runs.legacy_classifier_risk_highconf`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=A3 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_classifier_risk_highconf_composition_20260411_hybrid_api_a_conf49_main_v1.csv | data/curated/v4_3/generated_runs/legacy_classifier_risk_highconf/20260411_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use to check whether results depend on low-confidence model calls.
- Safe modifications: Change confidence thresholds or compare local-only and hybrid classifier policies.
- Extension relevance: Useful for reviewer concerns about LLM/NLP measurement noise.
- Notes: Shares script module with A4 but uses the composition output.

### Appendix Table A4: Classifier-risk robustness: high-confidence mismatch tests

- Asset ID: `A4`
- Paper source: `table_inputs/appendix/appendix_A4_highconf_mismatch.tex`
- Empirical question: Do high-confidence classifier subsets preserve the mismatch relations?
- Primary data product: Final classifier outputs, filing-level AI measures, and annual panel.
- Main constructs: Classifier confidence, PatentMismatch, AS ratio, weak patent support, high-confidence subset.
- Owning script: `semantic_ai_washing.analysis.publication_runs.legacy_classifier_risk_highconf`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=A4 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_classifier_risk_highconf_mismatch_20260411_hybrid_api_a_conf49_main_v1.csv | data/curated/v4_3/generated_runs/legacy_classifier_risk_highconf/20260411_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use to check whether the core mismatch construct is robust to classifier-confidence restrictions.
- Safe modifications: Change confidence thresholds or isolate short-acronym-only AI hits for review.
- Extension relevance: Supports future disambiguation and measurement-validation layers.
- Notes: Shares script module with A3 but uses the mismatch output.

### Appendix Table A5: Variable definitions

- Asset ID: `A5`
- Paper source: `table_inputs/appendix/appendix_A5_variable_definitions.tex`
- Empirical question: How are the paper variables defined?
- Primary data product: Variable-definition registry embedded in the publication script.
- Main constructs: Variable names, definitions, source data, transformations, and timing.
- Owning script: `semantic_ai_washing.analysis.publication_runs.appendix_variable_definitions`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=A5 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/appendix_variable_definitions_20260412_hybrid_api_a_conf49_main_v1.csv | data/curated/v4_3/generated_exports/paper/generated/latex/appendix_variable_definitions_20260412_hybrid_api_a_conf49_main_v1.tex | data/curated/v4_3/generated_runs/appendix_variable_definitions/20260412_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use when changing code or paper prose so variable labels remain synchronized.
- Safe modifications: Add definitions for new extension variables before adding them to manuscript tables.
- Extension relevance: Required for clean future journal archive and referee replication package.
- Notes: Exact generated CSV and TeX evidence are available.

## Appendix B: Timing And Patent Realization

### Appendix Table B1: AI disclosure intensity and AI patent timing

- Asset ID: `B1`
- Paper source: `table_inputs/appendix/appendix_B1_ai_focus_timing.tex`
- Empirical question: How does AI disclosure intensity relate to AI patent timing?
- Primary data product: Canonical annual AI/patent panel.
- Main constructs: AI Focus, AI patent grants, patent timing horizons, controls.
- Owning script: `semantic_ai_washing.analysis.publication_runs.legacy_r2_ai_focus_timing`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=B1 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_r2_ai_focus_timing_20260411_hybrid_api_a_conf49_main_v1.csv | data/curated/v4_3/generated_runs/legacy_r2_ai_focus_timing/20260411_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use to inspect basic disclosure/patent timing before applying credibility gates.
- Safe modifications: Change horizons, fixed effects, or patent-grant/application outcome choice.
- Extension relevance: Baseline timing layer for construct-validity revisions.
- Notes: Generated CSV/MD artifacts are the lineage source.

### Appendix Table B2: Actionable disclosure and AI patent timing

- Asset ID: `B2`
- Paper source: `table_inputs/appendix/appendix_B2_actionable_timing.tex`
- Empirical question: How does actionable AI disclosure relate to AI patent timing?
- Primary data product: Canonical annual AI/patent panel.
- Main constructs: Actionable AI disclosure, AI patents, patent timing horizons, controls.
- Owning script: `semantic_ai_washing.analysis.publication_runs.legacy_r4_actionable_patent_timing`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=B2 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_r4_actionable_patent_timing_20260411_hybrid_api_a_conf49_main_v1.csv | data/curated/v4_3/generated_runs/legacy_r4_actionable_patent_timing/20260411_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use to test whether more concrete AI language is tied to future AI realization.
- Safe modifications: Change actionable-share definition, horizons, or patent outcome.
- Extension relevance: Important for the builder-hides channel.
- Notes: Generated CSV/MD artifacts are the lineage source.

### Appendix Table B3: Speculative-only disclosure and AI patent timing

- Asset ID: `B3`
- Paper source: `table_inputs/appendix/appendix_B3_speculative_timing.tex`
- Empirical question: How does speculative-only AI disclosure relate to AI patent timing?
- Primary data product: Canonical annual AI/patent panel.
- Main constructs: Speculative AI disclosure, speculative share, AI patents, patent timing horizons.
- Owning script: `semantic_ai_washing.analysis.publication_runs.legacy_r5_speculative_patent_timing`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=B3 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_r5_speculative_patent_timing_20260411_hybrid_api_a_conf49_main_v1.csv | data/curated/v4_3/generated_runs/legacy_r5_speculative_patent_timing/20260411_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use to isolate the aspirational-language component of AI disclosure.
- Safe modifications: Change speculative threshold, lag structure, or outcome horizon.
- Extension relevance: Useful for refining low-substance disclosure definitions.
- Notes: Generated CSV/MD artifacts are the lineage source.

### Appendix Table B4: AS ratio, PatentMismatch, and longer-horizon AI patenting

- Asset ID: `B4`
- Paper source: `table_inputs/appendix/appendix_B4_as_mismatch_tplus2.tex`
- Empirical question: How do AS ratio and PatentMismatch relate to longer-horizon AI patenting?
- Primary data product: Canonical annual AI/patent panel.
- Main constructs: AS ratio, PatentMismatch, AI patent t+2, longer-horizon innovation outcome.
- Owning script: `semantic_ai_washing.analysis.publication_runs.legacy_r7_as_mismatch_tplus2`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=B4 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_r7_as_mismatch_tplus2_20260411_hybrid_api_a_conf49_main_v1.csv | data/curated/v4_3/generated_runs/legacy_r7_as_mismatch_tplus2/20260411_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use to test whether mismatch captures weak future realization beyond short horizons.
- Safe modifications: Change horizon, grant/application outcome, or continuous mismatch intensity.
- Extension relevance: Supports future horizon and construct refinements.
- Notes: Generated CSV/MD artifacts are the lineage source.

## Appendix C: Robustness And Market Tests

### Appendix Table C1: Reduced-baseline determinants of PatentMismatch

- Asset ID: `C1`
- Paper source: `table_inputs/appendix/appendix_C1_det_reduced.tex`
- Empirical question: Which baseline firm characteristics predict PatentMismatch in a reduced model?
- Primary data product: Canonical annual AI/patent panel with Compustat/market controls.
- Main constructs: PatentMismatch, size, leverage, cash/assets, R&D/assets, CAPX/assets, market controls.
- Owning script: `semantic_ai_washing.analysis.publication_runs.legacy_r8_mismatch_determinants_reduced`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=C1 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_r8_mismatch_determinants_reduced_20260411_hybrid_api_a_conf49_main_v1.csv | data/curated/v4_3/generated_runs/legacy_r8_mismatch_determinants_reduced/20260411_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use to inspect determinants under a lean control specification.
- Safe modifications: Change controls, fixed effects, or sample restrictions.
- Extension relevance: Baseline for future determinants and governance extensions.
- Notes: Generated CSV/MD artifacts are the lineage source.

### Appendix Table C2: Full-baseline determinants of PatentMismatch

- Asset ID: `C2`
- Paper source: `table_inputs/appendix/appendix_C2_det_full.tex`
- Empirical question: Which firm characteristics predict PatentMismatch in the full baseline model?
- Primary data product: Canonical annual AI/patent panel with full Compustat/market controls.
- Main constructs: PatentMismatch, firm controls, industry/year effects, disclosure and patent variables.
- Owning script: `semantic_ai_washing.analysis.publication_runs.legacy_a1_mismatch_determinants_full`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=C2 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_a1_mismatch_determinants_full_20260411_hybrid_api_a_conf49_main_v1.csv | data/curated/v4_3/generated_runs/legacy_a1_mismatch_determinants_full/20260411_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use to inspect full determinant specification before adding new channels.
- Safe modifications: Add governance, institutional ownership, labor, or industry-salience variables as extension inputs.
- Extension relevance: Natural staging point for Kuntara-led channel tests.
- Notes: Generated CSV/MD artifacts are the lineage source.

### Appendix Table C3: Full-baseline determinants of PatentMismatch intensity

- Asset ID: `C3`
- Paper source: `table_inputs/appendix/appendix_C3_det_intensity.tex`
- Empirical question: What predicts the intensity of PatentMismatch rather than only its indicator?
- Primary data product: Canonical annual AI/patent panel.
- Main constructs: PatentMismatch intensity, disclosure intensity, patent weakness, firm controls.
- Owning script: `semantic_ai_washing.analysis.publication_runs.legacy_a2_mismatch_intensity`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=C3 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/legacy_a2_mismatch_intensity_20260411_hybrid_api_a_conf49_main_v1.csv | data/curated/v4_3/generated_runs/legacy_a2_mismatch_intensity/20260411_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use to test continuous versions of the mismatch concept.
- Safe modifications: Change scaling, winsorization, or continuous intensity definition.
- Extension relevance: Useful if a referee asks whether the binary construct hides variation.
- Notes: Generated CSV/MD artifacts are the lineage source.

### Appendix Table C4: Size heterogeneity in filing-date and post-filing mismatch effects

- Asset ID: `C4`
- Paper source: `table_inputs/appendix/appendix_C4_size_heterogeneity.tex`
- Empirical question: Do filing-date and post-filing mismatch effects differ by firm size?
- Primary data product: Annual panel linked to filing-event market-return sample.
- Main constructs: Small/large firm split, PatentMismatch, filing-date CAR, post-filing returns.
- Owning script: `semantic_ai_washing.analysis.publication_runs.test_05_size_heterogeneity`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=C4 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/tables/test_05_size_heterogeneity_20260411_hybrid_api_a_conf49_main_v1.csv | data/curated/v4_3/generated_exports/paper/generated/latex/test_05_size_heterogeneity_20260411_hybrid_api_a_conf49_main_v1.tex | data/curated/v4_3/generated_runs/test_05_size_heterogeneity/20260411_hybrid_api_a_conf49_main_v1`
- Coauthor use: Use to inspect heterogeneity in market response and event-window patterns.
- Safe modifications: Change size breakpoint, event windows, or return outcome.
- Extension relevance: Useful for market-frictions and investor-attention explanations.
- Notes: Previous pandas dtype warning has a focused regression test.

### Appendix Table C5: Market reactions in capital-raising windows

- Asset ID: `C5`
- Paper source: `table_inputs/appendix/appendix_C5_issue_window_market.tex`
- Empirical question: How does the market react in capital-raising windows?
- Primary data product: Filing-event sample with market returns and capital-raising proxy inputs.
- Main constructs: Capital-raising window, PatentMismatch, CAR/BHAR outcomes, event timing.
- Owning script: `semantic_ai_washing.analysis.publication_runs.test_32_market_reaction_in_issue_windows`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=C5 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/v3_2/tables/test_32_market_reaction_in_issue_windows_20260423_aiw_v3_2_test_32_market_reaction_in_issue_windows_main_v1.csv | data/curated/v4_3/generated_exports/paper/generated/v3_2/latex/test_32_market_reaction_in_issue_windows_20260423_aiw_v3_2_test_32_market_reaction_in_issue_windows_main_v1.tex | data/curated/v4_3/generated_runs/test_32_market_reaction_in_issue_windows/20260423_aiw_v3_2_test_32_market_reaction_in_issue_windows_main_v1`
- Coauthor use: Use to evaluate whether financing-window effects are visible in market reactions.
- Safe modifications: Change event windows, issuance proxy, or return horizon.
- Extension relevance: Bridge between current share-growth proxy and future SEO/offering-terms data.
- Notes: Full reproduction table with exact generated CSV evidence.

### Appendix Table C6: Predictive post-filing return regressions with richer controls

- Asset ID: `C6`
- Paper source: `table_inputs/appendix/appendix_C6_predictive_return_controls.tex`
- Empirical question: Do predictive post-filing return regressions survive richer controls?
- Primary data product: Filing-event estimation sample, CRSP returns, annual controls, and market features.
- Main constructs: PatentMismatch, post-filing returns, richer controls, market features.
- Owning script: `semantic_ai_washing.analysis.publication_runs.test_12_predictive_return_controls`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=C6 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/v3_1/tables/test_12_predictive_return_controls_20260422_aiw_v3_1_test_12_predictive_return_controls_main_v1.csv | data/curated/v4_3/generated_exports/paper/generated/v3_1/latex/test_12_predictive_return_controls_20260422_aiw_v3_1_test_12_predictive_return_controls_main_v1.tex | data/curated/v4_3/generated_runs/test_12_predictive_return_controls/20260422_aiw_v3_1_test_12_predictive_return_controls_main_v1`
- Coauthor use: Use to inspect whether return predictability is robust to additional controls.
- Safe modifications: Add controls, change horizons, or rerun with alternative event samples.
- Extension relevance: Supports market-efficiency and investor-response revision paths.
- Notes: Exact generated CSV and TeX evidence are available.

### Appendix Table C7: Matched AI-talking comparison sample

- Asset ID: `C7`
- Paper source: `table_inputs/appendix/appendix_C7_matched_ai_talking.tex`
- Empirical question: How do mismatch and non-mismatch AI talkers compare in a matched sample?
- Primary data product: Filing-event estimation sample and annual panel controls used for matching.
- Main constructs: Matched AI-talking sample, PatentMismatch, controls, balance/comparison statistics.
- Owning script: `semantic_ai_washing.analysis.publication_runs.test_15_matched_ai_talking_sample`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=C7 reproduce-table`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/v3_1/tables/test_15_matched_ai_talking_sample_20260422_aiw_v3_1_test_15_matched_ai_talking_sample_main_v1.csv | data/curated/v4_3/generated_exports/paper/generated/v3_1/latex/test_15_matched_ai_talking_sample_20260422_aiw_v3_1_test_15_matched_ai_talking_sample_main_v1.tex | data/curated/v4_3/generated_runs/test_15_matched_ai_talking_sample/20260422_aiw_v3_1_test_15_matched_ai_talking_sample_main_v1`
- Coauthor use: Use to inspect whether comparisons survive matching rather than raw sample differences.
- Safe modifications: Change matching covariates, calipers, or balance diagnostics.
- Extension relevance: Useful if coauthors add stronger causal or quasi-experimental designs.
- Notes: CSV delta is numeric-string format only; generated TeX is exact. See docs/c7_format_delta_explanation.md.

### Appendix Figure C1: Event-study path around the release of ChatGPT

- Asset ID: `FC1`
- Paper source: `figures/figureC1.pdf`
- Empirical question: What is the event-study path around the ChatGPT release for PatentMismatch and filing-date returns?
- Primary data product: Annual AI/patent panel with event-time indicators and filing-event returns.
- Main constructs: Post-ChatGPT timing, PatentMismatch, filing-date CAR, event-study coefficients, pretrend diagnostics.
- Owning script: `semantic_ai_washing.analysis.publication_runs.test_13_pre_post_event_path`
- Rerun command: `AIW_DATA_ROOT=/path/to/ai-washing-private-data make reproduce-figures`
- Reference outputs: `data/curated/v4_3/generated_exports/paper/generated/v3_1/tables/test_13_pre_post_event_path_20260422_aiw_v3_1_test_13_pre_post_event_path_main_v1.csv | data/curated/v4_3/generated_exports/paper/generated/v3_1/figures/test_13_pre_post_event_path_20260422_aiw_v3_1_test_13_pre_post_event_path_main_v1.pdf | data/curated/v4_3/generated_runs/test_13_pre_post_event_path/20260422_aiw_v3_1_test_13_pre_post_event_path_main_v1`
- Coauthor use: Use to inspect timing patterns and pretrend evidence around late 2022.
- Safe modifications: Change event date, event-time window, or outcome variable; keep frozen v4.3 PDF until a new release is promoted.
- Extension relevance: Supports future shock/timing and attention-channel revisions.
- Notes: Frozen v4.3 manuscript PDF remains canonical; candidate regeneration evidence is documented in docs/figure_reproduction_status.md.
