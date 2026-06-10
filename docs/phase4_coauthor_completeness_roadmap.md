# Phase 4 Coauthor Completeness Roadmap

Generated: 2026-06-09

## Purpose

The current AI Washing workstation can reproduce the v4.3 table evidence. Phase 4 moves the package from "v4.3 reproduction works" to "Kuntara and Thomas can independently audit, extend, and trust the project without using Soheil's old local workstation."

The main design principle is conservative: keep the Git repository small and executable, keep private and licensed data in `AIW_DATA_ROOT`, and make every major research construct traceable from source artifacts to the final tables.

## Current Verdict

The workstation is now in a coauthor-ready state for private package rehearsal and initial collaboration. v4.3 reproduction, patent/WRDS/SEC audit surfaces, extension scaffolding, Docker validation, and fresh-clone validation have all passed. Remaining issues are documented future-extension gaps or non-blocking maintenance items.

Phase 4H implementation update, 2026-06-10:

- `make doctor` and `make coauthor-preflight` now provide a coauthor first-day environment and validation path.
- `docs/coauthor_share_note.md` and `docs/onedrive_data_room_checklist.md` provide the polished send note and private data-room upload checklist.
- `make reproduce-figures` and `make figure-reproduction-status` regenerate candidate figure evidence while keeping frozen v4.3 manuscript PDFs canonical.
- `make c7-format-delta` documents the one C7 format-only CSV delta with cell-level evidence and an exact TeX match.
- The pandas FutureWarning in `test_05_size_heterogeneity.py` has been removed and covered by a focused test.
- The deferred financing item is now labeled as SEO/offering terms for the strong washing-pays extension. The v4.3 Test 30 CRSP `shrout`-growth issue proxy is already reproducible and should not be described as missing equity-issuance data.



Phase 4G implementation update, 2026-06-10:

- `docs/phase4g_final_coauthor_package_rehearsal.md` records the final coauthor package rehearsal.
- Local validation, private data validation, data-room validation, SEC/WRDS/patent gates, artifact-coverage audit, full table reproduction, Docker validation, and fresh-clone Docker validation passed.
- Docker was tested both without private data, where private-data gates failed with controlled missing-data messages, and with read-only mounted private data, where full v4.3 reproduction passed.
- Fresh-clone rehearsal from the private GitHub repo passed with read-only private-data mount and reported 20 passing tests.
- Full table status remains 23 CSV exact matches, 1 format-only delta, and 2 frozen figure assets.
- A read-only private-data bug in Ken French factor staging was found and fixed before the final rehearsal pass.



Phase 4E implementation update, 2026-06-10:

- `src/semantic_ai_washing/analysis/extensions/builder_hides_right_tail.py` provides a runnable first-pass builder-hides screen from the staged annual panel.
- `make builder-hides-first-pass` writes ignored extension outputs under `outputs/extensions/builder_hides_right_tail/` or `$AIW_OUTPUT_ROOT/extensions/builder_hides_right_tail/`.
- `docs/extensions/builder_hides_first_pass.md` documents the right-tail builder definition, output files, and interpretation discipline.
- `docs/extensions/washing_pays_data_requirements.md` separates the current Test 30 CRSP share-growth proxy from the stronger financing-terms extension requiring actual SEO/offering data.
- The extension layer is not promoted into v4.3 evidence or the table crosswalk.

Phase 4D implementation update, 2026-06-10:

- Full-sample Compustat fundamentals, CRSP monthly stock file, CRSP market-index file, annual market features, daily event-return cache, CIK-GVKEY crosswalk, annual WRDS backbone, filing-level WRDS bridge, unmatched-tail diagnostics, JSON build reports, and WRDS source/progress notes are staged in the private data room.
- `manifests/wrds_data_manifest.csv` and `make validate-wrds-data` now provide a dedicated market/accounting/linkage validation gate.
- `docs/wrds_crsp_compustat_method_note.md` explains the lane boundaries, refresh policy, and audit path.
- `docs/wrds_source_inventory.md` maps coauthor-facing private folders and files to their purpose.
- The remaining non-reproduction queue is narrowed to future-extension inputs: actual SEO/offering terms and optional job-posting data.

Phase 4C implementation update, 2026-06-10:

- `docs/patent_mismatch_method_note.md` explains the construct lane, firm universe, identity layer, exact normalized matching, grant matching, pregrant assignee/applicant matching, AI patent keyword list, fuzzy rejection, and late-year pregrant caveat.
- `docs/patent_matching_validation.md` defines the patent validation surface and manual review procedure.
- `docs/patent_source_inventory.md` separates processed outputs, identity metadata, keyword metadata, reports, and optional raw PatentsView source.
- `docs/patent_fuzzy_sensitivity_note.md` records why fuzzy matching was rejected as too noisy for v4.3.
- `scripts/build_patent_audit_examples.py` and `make patent-example-audit` generate a 40-row balanced grant/pregrant audit sample under `$AIW_DATA_ROOT/reports/patents/patent_audit_examples.csv`.

Phase 4A/4B implementation update, 2026-06-09:

- Processed patent grant/pregrant counts, examples, and diagnostics are staged in the private data room.
- Hybrid company lookup and alias metadata are staged in the private data room.
- Patent keyword lists and sensitivity keyword lists are staged in the private data room.
- PatentsView guide/source files and a raw-source mirror policy note are staged in the private data room.
- Patent matching/fuzzy-sensitivity reports and progress logs are staged in the private data room.
- `manifests/patent_data_manifest.csv` and `make validate-patent-data` now enforce the patent audit surface.
- Final patent construction modules have been ported into `src/semantic_ai_washing/patents/` with portable path defaults.
- Focused patent unit tests have been ported under `tests/`.

Phase 4C through Phase 4G have now moved the package beyond table reproduction: the patent method/evidence pack is documented, the CRSP/Compustat merge-intermediate queue is closed for coauthor audit, the extension starter layer is available, the raw SEC source policy is explicit, and the final coauthor package rehearsal has passed.

What is already strong:

- The canonical repository is `/Users/soheilkhodadadi/DataWork/ai-washing`.
- The canonical private data root is `/Users/soheilkhodadadi/DataWork/ai-washing-private-data`.
- The repository is private on GitHub.
- v4.3 table reproduction is documented and currently reports 23 CSV exact matches, 1 format-only CSV delta, and 2 frozen figure assets.
- The annual NLP/patent lane is explicitly locked to 2016-2025.
- The event/market-return lane is explicitly locked to 2016-2024 because the staged CRSP return extracts stop at 2024-12-31.
- Classifier outputs, extracted AI sentences, annual panels, event panels, CRSP market inputs, and selected SEC samples are staged.

What still needs attention:

- The patent-mismatch construct is now documented and auditable through staged patent artifacts, method notes, and example files, but it remains the construct most likely to need coauthor/referee scrutiny before journal submission.
- The coauthor data-room manifest now marks `patent_raw`, `patent_match_artifacts`, `compustat_extracts`, and `crsp_compustat_linking` as present. The remaining deferred items are future-extension sources such as `seo_offering_terms` and `job_postings`.
- Kuntara's "washing pays" extension needs actual SEO/offering terms if the test is to go beyond the current share-growth proxy.
- The current panel includes `shrout` and a derived equity-issue proxy, but it does not include offer amount, offer discount, offer price, proceeds, or issuance valuation.
- The full raw PatentsView source is large but available locally; deciding whether to mirror it is a coauthor-friction choice, not a v4.3 reproduction requirement.

## Coauthor Request Crosswalk

### Thomas request

Thomas asked for "everything for the paper: the full raw data and all the code: the cleaned panel, the patent match, the classifier outputs, the CRSP and Compustat merges, and the scripts that build every table."

Current status:

| Request item | Current status | Phase 4 action |
| --- | --- | --- |
| Cleaned panel | Present | Keep canonical annual and event panels staged and checksummed. |
| Classifier outputs | Present | Keep final hybrid API classifier output as canonical; keep local layered output as support only. |
| Scripts that build every table | Present for v4.3 tables | Keep full reproduction ledger current after every change. |
| CRSP merge inputs | Present | Validate with `make validate-wrds-data`; inspect `docs/wrds_crsp_compustat_method_note.md` and `docs/wrds_source_inventory.md`. |
| Compustat extracts | Present | Full-sample Compustat fundamentals extract is staged under `$AIW_DATA_ROOT/interim/accounting/` and validated by `manifests/wrds_data_manifest.csv`. |
| Patent match | Present | Validate with `make validate-patent-data`; inspect the patent method/evidence docs and generated audit examples. |
| Raw patent data | Optional raw-source mirror | PatentsView source docs and policy are staged; full grant/pregrant TSV mirror can be added privately if coauthors request a bottom-up raw rebuild. |
| Folder labeling | Good but not final | Add coauthor-facing map that says what to open first, what is required, and what is optional. |

### Kuntara request

Kuntara wants the data/code for two extension paths:

1. "Washing pays": among equity-raising firms, test whether inflated or low-substance AI talkers raise more capital, at better terms, than quiet real AI builders.
2. "Builder hides": among real AI leaders, test whether actionable 10-K disclosure is lower rather than higher.

Current status:

| Extension | Current readiness | Phase 4 action |
| --- | --- | --- |
| Builder hides, cheap version | Ready from current annual panel | Add a starter script/runbook using right-tail patent/application activity and disclosure outcomes. |
| Builder hides, stronger version | Mostly ready | Add matched/robust versions and patent-example audit support. |
| Washing pays, proxy version | Partly ready | Current Test 30 uses next-year CRSP `shrout` growth above 5 percent as an issue proxy. Document this clearly. |
| Washing pays, strong version | Not ready | Need actual financing/SEO terms: proceeds, offer price, discount, valuation, and offer timing. |
| Job postings/hiring validation | Not ready | Keep as future-extension data; do not block handoff. |

## Main Risks

### Risk 1: Patent mismatch looks like a black box

This is the highest remaining risk. If Kuntara sees only final patent variables in the panel, she may reasonably ask how names were matched, why application data were handled differently from grant data, and how AI patents were identified.

Control:

- Keep final patent construction scripts in the canonical repo and validate them with the focused patent tests.
- Keep final grant and pregrant count/example/diagnostic CSVs staged in the private data room.
- Keep final company lookup, alias files, and patent keyword lists staged and documented.
- Use the patent method note and generated audit examples when discussing construct validity with coauthors.

### Risk 2: Company-to-assignee matching is hard to trust

The project previously found that naive matching undercounted firms badly. Fuzzy matching also created false positives. That history should be preserved, not hidden.

Control:

- Document the hybrid identity layer: WRDS names, SEC header names, legacy validated aliases, and legal-suffix normalization.
- Document the exact-normalized match rule.
- Document the uniqueness screen that drops ambiguous normalized terms.
- Document why loose fuzzy matching was rejected.
- Include example false positives from the fuzzy sensitivity run.

### Risk 3: Pregrant matching appears inconsistent with grant matching

Pregrant application matching uses assignee first and applicant fallback. This is correct, but it can look ad hoc unless explained.

Control:

- Port the validation note showing that assignee-only pregrant matching undercounted obvious firms.
- Include the applicant fallback logic as part of the official method note.
- Stage pregrant counts, examples, and diagnostics separately from grant counts.

### Risk 4: "Full raw data" means different things to different people

For v4.3 reproduction, full raw SEC filings and full raw PatentsView TSVs are not needed. For coauthor confidence, they may still want a raw-source mirror.

Control:

- Separate `required_reproduction`, `required_extension`, `raw_source_optional`, and `raw_source_full_mirror`.
- Include source documentation and exact links for Notre Dame Stage-One 10-X files and PatentsView bulk data.
- If storage and upload time are acceptable, mirror the full PatentsView raw grant/pregrant source in the private data room, not Git.
- Do not mirror the full SEC corpus unless explicitly requested; include representative samples and source instructions.

### Risk 5: Washing-pays extension is overpromised

The current data can identify an equity-issue proxy from next-year share growth. It cannot answer offer discount, offer price, proceeds, or valuation without a separate issuance data source.

Control:

- Label the existing test as a CRSP share-growth issue-window proxy.
- Add a strong-version data schema for SEO/offering terms.
- Do not claim the current package already answers the full "washing pays" question.

### Risk 6: Private/licensed data enters Git

The coauthor data room will become larger and more useful, which increases leakage risk.

Control:

- Keep all staged raw, licensed, derived, and generated data under `AIW_DATA_ROOT`.
- Extend validation scripts to check data presence and metadata without committing data.
- Run `make git-hygiene` after every staging-oriented change.

## Phase 4A: Patent Source And Processed Artifact Staging

Goal: make the patent lane independently auditable without requiring immediate full raw rebuilds.

Stage these processed artifacts under `$AIW_DATA_ROOT/data/processed/patents/`:

- `ai_patent_counts_filtered_ever_speaker_2016_2025_hybrid_grant_2014plus.csv`
- `ai_application_counts_filtered_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv`
- `ai_patent_examples_ever_speaker_2016_2025_hybrid_grant_2014plus.csv`
- `ai_application_examples_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv`
- `patents_diagnostics_ever_speaker_2016_2025_hybrid_grant_2014plus.csv`
- `application_diagnostics_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv`

Stage these metadata artifacts under `$AIW_DATA_ROOT/data/metadata/` or `$AIW_DATA_ROOT/data/interim/patents/metadata/`:

- `company_lookup_ever_speaker_2016_2025_hybrid_v1.csv`
- `company_aliases_ever_speaker_2016_2025_hybrid_v1.csv`
- final patent keyword lists used by the grant/pregrant extractors
- keyword benchmark and fuzzy-sensitivity outputs used to justify the final dictionary and exact-match posture

Stage PatentsView public-source documentation under `$AIW_DATA_ROOT/data/raw/patentsview/Guide/`:

- `2026BulkDataProductDescriptions.xlsx`
- `PV_grant_data_dictionary.pdf`
- `PV_pregrant_data_dictionary.pdf`
- saved bulk-data directory page, if useful

Recommended raw-source policy:

- Include the processed patent counts/examples/diagnostics in the core private data room.
- Include PatentsView guide files and source links in the core private data room.
- Mirror the full local PatentsView raw source as an optional private raw-source pack if upload time is acceptable:
  - grant files are about 8.2GB
  - pregrant files are about 9.0GB
  - total PatentsView root is about 18GB
- Do not put PatentsView raw files in Git.

Gate:

- `make validate-data-room` reports patent processed artifacts present.
- A new patent data validator reports expected row counts, year coverage, and required columns.
- The coauthor manifest no longer leaves `patent_match_artifacts` vague or deferred.

## Phase 4B: Patent Code Closure

Goal: move the final patent construction code into the canonical repo without copying unrelated pilot scripts.

Port these final or near-final modules from the old `semantic-patterns` provenance repository into `src/semantic_ai_washing/patents/`:

- `keyword_matching.py`
- `patentsview_sources.py`
- `pregrant_sources.py`
- `build_company_lookup.py`
- `extract_filtered_patents_lightweight.py`
- `extract_filtered_pregrant_applications_lightweight.py`
- `benchmark_keyword_sets_lightweight.py`
- `run_patent_fuzzy_sensitivity_sample.py`

Do not automatically port:

- one-off pilot extractors
- obsolete sample scripts
- modules that assume legacy PatentsView filenames without the modern resolver
- scripts that require local absolute paths

Required path contract:

- `AIW_DATA_ROOT` controls private project data.
- `PATENT_DATA_ROOT` can override grant raw-source location.
- `PATENT_PREGRANT_DATA_ROOT` can override pregrant raw-source location.
- No executable code may require `/Users/soheilkhodadadi/...`.

Add Makefile targets after scripts are ported:

- `validate-patent-data`
- `patent-example-audit`
- `patent-source-dry-run`
- `rebuild-patent-counts-sample`

Gate:

- Patent modules import cleanly in the repo-local environment.
- A small fixture/sample patent pipeline runs without full raw data.
- Full raw-source rebuild commands are documented but not required for the normal v4.3 reproduction path.

## Phase 4C: Patent Method And Evidence Pack

Goal: give Kuntara a quick way to judge whether the patent mismatch variable is credible.

Create or port these docs:

- `docs/patent_mismatch_method_note.md`
- `docs/patent_matching_validation.md`
- `docs/patent_source_inventory.md`
- `docs/patent_fuzzy_sensitivity_note.md`

The method note should explain:

- firm universe
- company lookup and alias construction
- legal suffix normalization
- exact normalized matching
- ambiguous-term exclusion
- grant-side assignee matching
- pregrant assignee-first/applicant-fallback matching
- patent AI keyword list
- why fuzzy matching was rejected
- publication-lag caveat for late pregrant application years

Create an audit example file:

- `$AIW_DATA_ROOT/reports/patents/patent_audit_examples.csv`

It should include a small, readable sample:

- CIK
- firm name
- patent/application ID
- year
- title
- abstract
- matched keywords
- source lane: grant or pregrant
- notes if the example illustrates a matching or keyword issue

Gate:

- A coauthor can inspect 20 to 50 actual matched patents/applications and see why they were classified as AI-related.
- The method note explains known weaknesses rather than hiding them.

## Phase 4D: CRSP, Compustat, And Linkage Closure

Status: implemented on 2026-06-10.

Goal: satisfy Thomas's request for CRSP and Compustat merges, not only final merged variables.

Staged and validated artifacts include:

- `data/interim/accounting/wrds_comp_funda_full_sample_v1.parquet`
- `data/interim/market/wrds_crsp_msf_full_sample_v1.parquet`
- `data/interim/market/wrds_crsp_msi_full_sample_v1.parquet`
- `data/interim/market/annual_market_features_ever_speaker_2016_2025_hybrid_api_a_conf49_v1.csv`
- `data/interim/linking/ever_speaker_wrds_backbone_2016_2025_hybrid_api_a_conf49_v1.csv`
- `data/interim/linking/filing_wrds_bridge_hybrid_api_a_conf49_v1.csv`
- `data/reports/wrds/filing_wrds_bridge_unmatched_hybrid_api_a_conf49_v1.csv`
- WRDS bridge JSON reports and retained source/progress notes

Documented provenance modules from the old workspace include:

- `pull_full_sample_wrds_raw.py`
- `build_wrds_gvkey_permno_bridge.py`
- `build_full_sample_wrds_backbone.py`
- `pull_compustat_controls.py`
- `download_crsp.py`
- `download_compustat.py`
- `clean_crsp.py`
- `clean_compustat.py`

Policy:

- Do not share WRDS credentials.
- Stage derived WRDS extracts privately for coauthor use.
- Make refresh scripts opt-in and credential-dependent.
- Reproduction must not require fresh WRDS access.

Gate:

- `compustat_extracts` and `crsp_compustat_linking` in `coauthor_data_room_manifest.csv` are present.
- `make validate-wrds-data` reports all 16 WRDS manifest rows present.
- Kuntara can see which file produced each market/accounting variable in the annual and event panels.

## Phase 4E: Extension Readiness Layer

Status: implemented on 2026-06-10.

Goal: give Kuntara starting points for her two proposed tests without pretending missing data exist.

### Builder hides

This is the most immediately ready extension.

Inputs already available:

- annual panel
- patent counts and AI patent/application variables
- actionable/speculative disclosure measures
- firm controls
- year and industry variables

Implemented starter script:

- `src/semantic_ai_washing/analysis/extensions/builder_hides_right_tail.py`
- `make builder-hides-first-pass`

Cheap version:

- define top patent/application tail using `patents_ai`, `applications_ai`, or lagged versions
- compare `ActShare`, `CredAI`, `AI_Focus`, `share_A`, and `share_S`
- estimate right-tail regressions with controls, year fixed effects, and industry fixed effects
- output a clean CSV and markdown interpretation memo

Gate:

- The script runs from the current annual panel and produces a first-pass result without new data.

### Washing pays

This has two levels.

Proxy version:

- use the current issue-window proxy based on next-year CRSP `shrout` growth above 5 percent
- compare washers and substantive firms around issue windows
- frame as a screening exercise, not the full financing-terms test

Strong version:

- requires external SEO/equity issuance terms
- required fields likely include firm identifier, issue date, proceeds, offer price, pre-issue price, discount, offer size, and valuation/market-cap base
- possible sources need to be decided by Kuntara/Thomas based on their data access

Implemented docs:

- `docs/extensions/washing_pays_data_requirements.md`
- `docs/extensions/builder_hides_first_pass.md`

Gate:

- Current package supports the proxy version.
- Strong version is explicitly marked as waiting on issuance-term data.

## Phase 4F: Raw SEC Policy

Goal: avoid unnecessary raw SEC bulk while keeping the extraction/classification path transparent.

Status: implemented on 2026-06-10.

Recommendation:

- Do not mirror the full raw SEC corpus in the main coauthor data room unless Thomas or Kuntara specifically asks.
- Keep representative raw/full-submission samples and Stage-One cleaned samples.
- Keep Notre Dame Stage-One source links and parsing documentation.
- Keep extracted AI sentences and classifier outputs as the practical audit surface.

Reason:

- v4.3 reproduction does not require the full raw SEC corpus.
- Coauthors can independently retrieve Stage-One files from the documented source if they want to rebuild the extraction layer.
- The extraction/classification mechanics can be demonstrated through samples and fixtures.

Gate:

- SEC raw-source policy is documented in the coauthor data room.
- Extraction/classification sample pipeline runs.
- No one expects full raw 10-K text to be inside Git.

Implemented artifacts:

- `docs/sec_raw_source_policy.md`
- `docs/sec_extraction_classification_audit.md`
- `manifests/sec_source_manifest.csv`
- `scripts/validate_sec_source_policy.py`
- `make validate-sec-source`

Current validated anchors:

- 5 representative raw SEC full-submission samples.
- 4 representative Notre Dame Stage-One 2025 samples.
- Notre Dame/SRAF documentation and Google Drive source links.
- 106,977 extracted AI sentences for 2016-2024.
- 40,902 extracted AI sentences for the 2025 refresh.
- 147,879 final hybrid classified AI sentences for 2016-2025.

## Phase 4G: Final Coauthor Package Rehearsal

Status: implemented on 2026-06-10.

Goal: prove the package works before sharing.

Run these checks:

```bash
cd /Users/soheilkhodadadi/DataWork/ai-washing
make validate
make path-leak-scan
make import-smoke
make smoke-fixture
make git-hygiene
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make check-private-data
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make validate-data-room
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make validate-sec-source
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make audit-artifact-coverage
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make reproduce-all-tables
make reproduction-status
```

After Phase 4 patent closure, also run:

```bash
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make validate-patent-data
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make patent-example-audit
```

Container checks:

- Docker without private data should pass repo validation and fixture tests, then fail private-data reproduction with clear missing-data messages.
- Docker with mounted `AIW_DATA_ROOT` should pass private-data validation and full v4.3 reproduction.

Fresh-clone checks:

- clone private GitHub repo into a temporary directory
- install pinned requirements
- run non-private validation
- mount or point to private data root
- run data-room validation and full table reproduction

Gate:

- The final handoff can be explained in one page.
- A coauthor can clone the repo, set `AIW_DATA_ROOT`, run validation, inspect patent examples, reproduce v4.3, and begin extension tests.
- Gate passed on 2026-06-10. See `docs/phase4g_final_coauthor_package_rehearsal.md`.

## Recommended Execution Order

1. Stage processed patent counts/examples/diagnostics and final patent metadata in the private data room.
2. Add manifest rows and `validate-patent-data`.
3. Port final patent construction modules and keyword resources into the canonical repo.
4. Add patent method and evidence docs.
5. Stage CRSP/Compustat merge intermediates and source/build reports.
6. Add builder-hides starter extension. Completed.
7. Add washing-pays data-requirements note and proxy/strong-version separation. Completed.
8. Rerun full v4.3 reproduction.
9. Rerun Docker and fresh-clone validation. Completed.
10. Prepare the coauthor share package and private-data-room upload. Ready for final sharing decision.

## Decision Recommendation

Proceed with Phase 4 before sharing the package.

The package is already technically credible for v4.3 table reproduction, but Thomas and Kuntara asked for a collaboration-ready data room. The remaining work is not cosmetic. It directly protects the project from the most predictable critique: "I can rerun the tables, but I cannot see how the patent mismatch construct was built or how to extend the paper."

The highest-return next step is operational: decide the private-data-room sharing channel, invite coauthors to the private GitHub repo, and run a coauthor first-day rehearsal using the documented runbook. Patent closure, WRDS/CRSP/Compustat closure, SEC source policy, extension scaffolding, and final package rehearsal are now implemented.
