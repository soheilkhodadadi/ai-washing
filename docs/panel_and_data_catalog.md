# Panel And Data Product Catalog

This catalog explains the private data room as empirical data products rather than loose files. It is the coauthor-facing map for the cleaned panel, patent match, classifier outputs, CRSP/Compustat merges, and frozen v4.3 evidence.

The machine-readable version is `manifests/data_product_catalog.csv`. Private data paths are logical paths: a path beginning with `data/` is staged under `$AIW_DATA_ROOT/` after removing the leading `data/` prefix, as described in `docs/private_data_contract.md`.

## How To Use This Catalog

- To rerun or modify a table, start with `docs/paper_table_workbench.md`.
- To inspect the panel or source data behind a table, find the relevant product below.
- To change a construct, read the matching file in `docs/construct_playbooks/` before editing scripts or data.
- To validate private files, run `make check-private-data validate-data-room validate-sec-source validate-wrds-data validate-patent-data audit-artifact-coverage`.

## `annual_nlp_patent_panel`

- Purpose: Canonical firm-year panel linking AI disclosure measures, patent support, Compustat controls, market features, and future outcomes.
- Logical private path: `data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`
- Coverage: 2016-2025 firm-years; expected 50,840 rows in v4.3.
- Keys: cik; year; firm identifiers; WRDS identifiers where available.
- Source lineage: Built from SEC filing measures, final hybrid classifier outputs, patent grant/pregrant counts, WRDS/Compustat/CRSP bridges, and controls.
- Producing or validation scripts: `scripts/check_private_data.py; scripts/audit_artifact_coverage.py; scripts/validate_data_room.py`
- Tables using it: F1; T00; T16; T17; T20; T29; T25; T30; B1; B2; B3; B4; C1; C2; C3; C4; FC1
- Safe modifications: Use as the baseline for new v5+ variables; add columns in a copied or versioned panel before replacing canonical v4.3 evidence.
- Overwrite rule: Do not overwrite the v4.3 parquet. Stage a new version and update manifests/release notes.
- Extension relevance: Core input for builder-hides, governance, incentives, and construct-validity extensions.

## `filing_event_estimation_sample`

- Purpose: Canonical filing-event sample used for event-window and market-return tests.
- Logical private path: `data/processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet`
- Coverage: 2016-2024 event/market lane; expected 7,355 filing events in v4.3.
- Keys: filing_id; cik; filing_date; permno; permco; event timing fields.
- Source lineage: Filing spine merged to WRDS/CRSP links and daily/monthly return inputs.
- Producing or validation scripts: `scripts/check_private_data.py; scripts/validate_wrds_data.py; scripts/audit_artifact_coverage.py`
- Tables using it: T00; T09; C4; C5; C6; C7
- Safe modifications: Change event windows or return outcomes in a new output branch while retaining the v4.3 sample.
- Overwrite rule: Do not silently add 2025 return events; a CRSP refresh becomes a v5+ data lane.
- Extension relevance: Required for market-response and financing-window extensions.

## `filing_spine_ai_measures`

- Purpose: Filing-level disclosure lineage before return-data filters, including AI measure aggregation.
- Logical private path: `data/interim/market/filing_ai_measures_hybrid_api_a_conf49_v1.csv; data/interim/market/filing_event_spine_hybrid_api_a_conf49_v1.csv`
- Coverage: 2016-2025 disclosure filing spine; event returns still stop at 2024.
- Keys: filing_id; source_filename; cik; filing_date.
- Source lineage: Aggregated from extracted and classified AI sentences into filing-level disclosure measures.
- Producing or validation scripts: `scripts/validate_sec_source_policy.py; scripts/validate_wrds_data.py`
- Tables using it: A3; A4; T00 support; event-lane audit support.
- Safe modifications: Use to inspect filing-level disclosure composition or rebuild event filters.
- Overwrite rule: Treat this as lineage support; do not confuse it with the completed event-return panel.
- Extension relevance: Useful for new filing-level event studies and disclosure-timing tests.

## `final_hybrid_classifier_outputs`

- Purpose: Final sentence-level hybrid classifier outputs used to build v4.3 disclosure measures.
- Logical private path: `data/processed/classifications/classifications_shadow_hybrid_api_a_conf49_v1`
- Coverage: 2016-2025; expected 147,879 classified AI sentences.
- Keys: filing/source identifiers; sentence identifiers; year; predicted labels and confidence fields.
- Source lineage: Hybrid classifier output after local/model layers and API-assisted classification policy.
- Producing or validation scripts: `scripts/validate_sec_source_policy.py; scripts/textual_construct_audit.py`
- Tables using it: T00; A1; A3; A4; disclosure constructs used throughout.
- Safe modifications: Review label slices, confidence thresholds, or acronym-only hits without overwriting the canonical output.
- Overwrite rule: Any new classifier run must receive a new folder/version and a validation report.
- Extension relevance: Starting point for measurement robustness and reviewer-labeled disambiguation layers.

## `extracted_ai_sentences`

- Purpose: Extracted AI sentence support used to audit the text extraction layer before classification.
- Logical private path: `data/processed/sec/sentences_clean; data/processed/sec/sentences_clean_refresh_2025_v1`
- Coverage: 2016-2024 extracted sentences plus 2025 refresh; expected 106,977 plus 40,902 rows.
- Keys: filing/source identifiers; sentence text; year; extraction metadata.
- Source lineage: Extracted from Stage-One cleaned SEC 10-X text and representative SEC source samples.
- Producing or validation scripts: `scripts/validate_sec_source_policy.py; docs/sec_extraction_classification_audit.md`
- Tables using it: A1; A3; A4; support for all disclosure constructs.
- Safe modifications: Use for spot checks and reviewer samples; rerun extraction only in a new versioned output.
- Overwrite rule: Do not replace extracted sentence support without reconciling to the final 147,879 classifier rows.
- Extension relevance: Useful for short-acronym false-positive review and additional training data selection.

## `classifier_validation_labels`

- Purpose: Human labels, held-out samples, IRR reports, and classifier evaluation outputs.
- Logical private path: `data/labels/v1; data/labels/v2; data/validation/held_out_v4; data/reports/evaluation; data/reports/labels`
- Coverage: Held-out and support samples used for v4.3 measurement audit.
- Keys: sentence/sample identifiers; labels; annotator/evaluation metadata where available.
- Source lineage: Boundary-revised label files and held-out validation artifacts.
- Producing or validation scripts: `semantic_ai_washing.analysis.publication_runs.legacy_b1_measurement_audit; scripts/textual_construct_audit.py`
- Tables using it: A1
- Safe modifications: Add new labeled examples as a new validation layer; keep old held-out files fixed for v4.3.
- Overwrite rule: Never train on held-out files or overwrite the frozen evaluation evidence.
- Extension relevance: Basis for stronger journal-review measurement validation.

## `patent_match_artifacts`

- Purpose: Final PatentsView grant and pregrant counts, examples, diagnostics, and audit samples.
- Logical private path: `data/processed/patents; data/reports/patents`
- Coverage: Patent/application evidence through the 2016-2025 annual-panel build; source years begin in 2014 for lookback support.
- Keys: cik; firm name; year; patent/application identifiers; matched keywords.
- Source lineage: PatentsView grant and pregrant data filtered by AI keyword lists and matched to company identity metadata.
- Producing or validation scripts: `scripts/validate_patent_data.py; scripts/build_patent_audit_examples.py; semantic_ai_washing.patents.*`
- Tables using it: F1; T16; T17; B1; B2; B3; B4; C1; C2; C3
- Safe modifications: Inspect examples and diagnostics first; test any new matching rule in a sensitivity output before promotion.
- Overwrite rule: Do not replace the patent counts without updating patent manifests, method notes, and the annual panel version.
- Extension relevance: Core evidence for PatentMismatch, builder-hides, and construct-validity revisions.

## `patent_keyword_metadata`

- Purpose: Base and sensitivity AI keyword lists for patent/application classification.
- Logical private path: `data/metadata/patents`
- Coverage: Keyword dictionaries used by final patent extraction and sensitivity screens.
- Keys: keyword terms; sensitivity family where applicable.
- Source lineage: Final patent keyword list plus core/applied/precise/expanded/automation/industry/watchlist variants.
- Producing or validation scripts: `semantic_ai_washing.patents.keyword_matching; semantic_ai_washing.patents.benchmark_keyword_sets_lightweight; scripts/validate_patent_data.py`
- Tables using it: Patent support for F1; T16; T17; B*; C*
- Safe modifications: Add candidate keywords to a sensitivity list first; review false positives before changing the base list.
- Overwrite rule: Version keyword files and rerun patent audit examples before promoting.
- Extension relevance: Important for reducing acronym/keyword false-positive risk.

## `company_identity_patent_lookup`

- Purpose: Hybrid company lookup and aliases used to match public firms to patent assignees/applicants.
- Logical private path: `data/metadata/company_identity`
- Coverage: Ever-speaker company identity support for 2016-2025 panel firms.
- Keys: cik; name; cleaned name; ticker; gvkey; aliases.
- Source lineage: Hybrid lookup and alias artifacts from the final company-identity matching pass.
- Producing or validation scripts: `semantic_ai_washing.patents.build_company_lookup; scripts/validate_patent_data.py`
- Tables using it: All patent-backed tables through the annual panel.
- Safe modifications: Add aliases carefully and rerun diagnostics for high-salience firms before changing counts.
- Overwrite rule: Do not switch to broad fuzzy matching without preserving exact-normalized baseline and review samples.
- Extension relevance: Main audit surface for patent-match completeness and false positives.

## `wrds_compustat_extracts`

- Purpose: Compustat fundamentals used for controls and coauthor rebuilds of accounting variables.
- Logical private path: `data/interim/accounting/wrds_comp_funda_full_sample_v1.parquet`
- Coverage: Fiscal years 2014-2025 support; v4.3 panel uses aligned 2016-2025 firm-years.
- Keys: gvkey; datadate; fyear.
- Source lineage: WRDS Compustat fundamentals pull staged in the private data root.
- Producing or validation scripts: `scripts/validate_wrds_data.py; docs/wrds_crsp_compustat_method_note.md`
- Tables using it: T00; T16; T17; T20; T25; T29; T30; C1; C2; C3; C4; C6; C7
- Safe modifications: Use for rebuilding controls or adding accounting variables in a versioned panel.
- Overwrite rule: Do not refresh WRDS inputs without a local credential-based refresh note and validation report.
- Extension relevance: Needed for additional firm fundamentals, governance, and channel tests.

## `crsp_market_returns`

- Purpose: CRSP monthly/index/daily return inputs used in market features, factor alpha, and event-window tests.
- Logical private path: `data/interim/market/wrds_crsp_msf_full_sample_v1.parquet; data/interim/market/wrds_crsp_msi_full_sample_v1.parquet; data/interim/market/filing_event_returns_daily_hybrid_api_a_conf49_v1.parquet; data/curated/v4_3/factor_inputs`
- Coverage: Market-return inputs currently stop at 2024-12-31.
- Keys: permno; permco; date; filing_id where event returns are used.
- Source lineage: WRDS CRSP monthly stock file, CRSP market index, daily filing returns, and Ken French factor cache.
- Producing or validation scripts: `scripts/validate_wrds_data.py; semantic_ai_washing.analysis.publication_runs.test_09_factor_adjusted_alpha`
- Tables using it: T00; T09; C4; C5; C6; C7; FC1
- Safe modifications: Change factor models, event windows, or return horizons in scripts; keep source CRSP lane fixed for v4.3.
- Overwrite rule: A 2025 return refresh is a v5+ extension and must not silently replace v4.3.
- Extension relevance: Required for market efficiency, investor response, and financing-window work.

## `crsp_compustat_linkage`

- Purpose: CIK-GVKEY-PERMNO bridge and WRDS linkage reports used to connect filings to accounting and market data.
- Logical private path: `data/interim/linking; data/reports/wrds`
- Coverage: Annual bridge 2016-2025; filing bridge 2016-2025 before return filters.
- Keys: cik; gvkey; permno; permco; filing_id; year.
- Source lineage: Ever-speaker CIK-GVKEY crosswalk, annual WRDS backbone, filing-level bridge, and unmatched-link diagnostics.
- Producing or validation scripts: `scripts/validate_wrds_data.py; docs/wrds_source_inventory.md`
- Tables using it: All WRDS-backed tables through annual and event panels.
- Safe modifications: Inspect unmatched tails before changing linkage logic; test changes in a new bridge version.
- Overwrite rule: Do not overwrite the v4.3 bridge without preserving unmatched diagnostics and row-count reconciliation.
- Extension relevance: Important for any added market, governance, or labor dataset.

## `execucomp_ceo_extract`

- Purpose: Staged CEO-row ExecuComp extract used for the executive-incentive table.
- Logical private path: `data/external/execucomp/execucomp_ceo_anncomp_2015_2024.parquet`
- Coverage: 2015-2024 support for v4.3 Test 25.
- Keys: gvkey/company identifier; fiscal year; executive/CEO rows.
- Source lineage: WRDS ExecuComp extract staged as a private cache so reruns do not require credentials.
- Producing or validation scripts: `scripts/check_private_data.py; docs/t25_execucomp_policy.md`
- Tables using it: T25
- Safe modifications: Add compensation variables in a copied extract or versioned refresh.
- Overwrite rule: Never store WRDS credentials; any refresh is explicit and local to the coauthor.
- Extension relevance: Supports governance and incentive mechanism revisions.

## `sec_source_samples_and_links`

- Purpose: Representative raw/Stage-One SEC samples plus source links for bottom-up text-source audit.
- Logical private path: `data/raw/sec_samples; data/docs/source_links/sec_stage_one_sources.md`
- Coverage: Representative samples; full raw corpus intentionally excluded.
- Keys: source filenames and filing identifiers where available.
- Source lineage: Selected SEC full-submission samples, Notre Dame Stage-One samples, and public source documentation.
- Producing or validation scripts: `scripts/validate_sec_source_policy.py; docs/sec_raw_source_policy.md`
- Tables using it: Support for all disclosure-measure tables.
- Safe modifications: Add more samples for audit; do not bundle full raw SEC unless coauthors request a raw rebuild.
- Overwrite rule: Keep source samples separate from extracted sentence and classifier outputs.
- Extension relevance: Useful for reviewer demonstrations of extraction mechanics.

## `comment_letter_and_enforcement_events`

- Purpose: SEC comment-letter and enforcement-salience event inputs for scrutiny-channel tests.
- Logical private path: `data/curated/v4_3/comment_letter_event_panel.parquet; annual panel enforcement-salience columns`
- Coverage: v4.3 event and annual timing windows as staged.
- Keys: cik; year; event timing fields.
- Source lineage: Comment-letter event panel and annual enforcement-salience timing merged into publication scripts.
- Producing or validation scripts: `semantic_ai_washing.analysis.publication_runs.test_20_comment_letter_cleanup; semantic_ai_washing.analysis.publication_runs.test_29_sec_ai_washing_enforcement_did`
- Tables using it: T20; T29
- Safe modifications: Change event windows or salience definitions only in new output runs.
- Overwrite rule: Keep original v4.3 event definitions until a release note promotes a revised scrutiny design.
- Extension relevance: Supports regulatory attention and disclosure-cleanup extensions.

## `frozen_v43_generated_evidence`

- Purpose: Frozen v4.3 generated table/figure CSV, TeX, PDF, and run-directory evidence used for comparison.
- Logical private path: `Git tracked under data/curated/v4_3/generated_exports and data/curated/v4_3/generated_runs`
- Coverage: All 24 tables and 2 figures in the v4.3 reproduction surface.
- Keys: asset_id; run_id; script/test identifiers.
- Source lineage: Curated from the v4.3 release build and used by reproduction status checks.
- Producing or validation scripts: `scripts/reproduce_assets.py; scripts/compare_selected_reproduction.py`
- Tables using it: All v4.3 assets.
- Safe modifications: Use as reference evidence; write new generated outputs under outputs/ and compare before promotion.
- Overwrite rule: Do not overwrite frozen evidence; create a new release folder for v5+.
- Extension relevance: Allows coauthors to see whether changes are numerical, formatting-only, or intentional future results.
