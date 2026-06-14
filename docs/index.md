# Documentation Index

This index is organized by coauthor task. Internal development reports and email drafts are archived outside this repository; the files listed here are the professional working surface for the AI Washing project.

## Empirical Orientation

- `empirical_workstation.md`: project-level map of the data flow, constructs, panels, and extension lanes.
- `paper_table_workbench.md`: table-by-table guide for rerunning, inspecting, or modifying manuscript assets.
- `panel_and_data_catalog.md`: catalog of the major panels, classifier outputs, patent match, WRDS/market products, and frozen evidence.
- `construct_playbooks/`: construct-level guides for safe modification and coauthor review.
- `../manifests/paper_table_workbench.csv`: machine-readable paper table workbench.
- `../manifests/data_product_catalog.csv`: machine-readable data product catalog.
- `../manifests/table_to_script_crosswalk.csv`: reproduction-oriented table/script crosswalk.
- Terminal helpers: `make workbench-index`, `make table-info TABLE_ID=T30`, and `make export-table-workbench TABLE_ID=T30`.
- `dashboard_guide.md`: optional static HTML dashboard and Streamlit/Plotly app, including table review, technical drill-down, and data-quality cockpit views.
- Dashboard helpers: `make dashboard`, `make dashboard-check`, and optional `make dashboard-app`.

## First-Day Setup

- `../README.md`: repository overview and shortest path.
- `../README_START_HERE.md`: setup, validation, and table-workbench entry point.
- `docker_quickstart.md`: lowest-friction container path.
- `dashboard_guide.md`: browser-based navigation layer for tables, data products, construct audits, classifier evidence, patent evidence, and extensions.
- `coauthor_quickstart.md`: compact first-run checklist.
- `coauthor_runbook.md`: detailed first-day runbook for setup, data validation, reruns, and extensions.

## Empirical Data And Construct Guides

- `panel_and_data_catalog.md`: readable data product catalog.
- `construct_playbooks/README.md`: guide to construct playbooks.
- `construct_playbooks/ai_disclosure_and_classifier_constructs.md`: AI sentence/classifier layer.
- `construct_playbooks/patent_mismatch_construct.md`: PatentMismatch variable and future AI realization.
- `construct_playbooks/patent_matching_and_company_identity.md`: company/assignee matching and alias policy.
- `construct_playbooks/crsp_compustat_linkage_and_market_return_tests.md`: WRDS/market linkage and return tests.
- `construct_playbooks/capital_raising_proxy.md`: current share-growth proxy and SEO extension.
- `construct_playbooks/execucomp_incentives.md`: CEO incentive data and refresh policy.
- `construct_playbooks/sec_scrutiny_enforcement_timing.md`: comment-letter and enforcement timing.

## Data-Room Contract

- `private_data_contract.md`: private data mirror and path policy.
- `coauthor_data_room.md`: full coauthor data-room contents and validation gates.
- `private_data_staging_map.md`: expected private data staging structure.
- `data_management.md`: what belongs in Git versus `AIW_DATA_ROOT`.
- `artifact_coverage_policy.md`: v4.3 lane-specific coverage rules.

## Reproduction

- `full_reproduction_status.md`: full v4.3 table and figure status ledger.
- `selected_reproduction_status.md`: selected-table reproduction gate.
- `figure_reproduction_status.md`: figure-series evidence and frozen figure policy.
- `c7_format_delta_explanation.md`: documented format-only C7 delta.
- `releases/v4_3_defense_freeze.md`: frozen v4.3 computational target.

## Source And Construct Audits

- `sec_raw_source_policy.md`: SEC source policy and sample strategy.
- `sec_extraction_classification_audit.md`: sentence extraction and classifier-output audit surface.
- `wrds_crsp_compustat_method_note.md`: WRDS/CRSP/Compustat data lane.
- `wrds_source_inventory.md`: WRDS source inventory and validation notes.
- `patent_mismatch_method_note.md`: patent mismatch construction.
- `patent_matching_validation.md`: patent matching checks and examples.
- `patent_source_inventory.md`: PatentsView source inventory.
- `patent_fuzzy_sensitivity_note.md`: fuzzy matching sensitivity note.
- `replication_audit_runbook.md`: strict replication and data-integrity audit procedure.
- `replication_audit_report.md`: current audit summary.
- `share_readiness_report.md`: Docker share-readiness result.

## Extension Starters

- `extension_playbook.md`: extension roadmap for the next empirical tests.
- `extension_notes_future_data.md`: data gaps for future extensions.
- `../manifests/extension_workbench.csv`: machine-readable extension registry.
- `extensions/builder_hides_first_pass.md`: first-pass builder-hides extension.
- `extensions/washing_pays_proxy_first_pass.md`: operational proxy screen based on Test 30 share-growth logic.
- `extensions/washing_pays_data_requirements.md`: data requirements for the stronger financing-terms extension.
- `../templates/seo_offering_terms_schema.csv`: template for future SEO/offering-terms data.
- Schema helper: `make check-seo-schema SEO_FILE=/path/to/seo_offering_terms.csv`.

## Limitations And Archive Policy

- `known_limitations.md`: current limitations and non-blockers.
- `journal_replication_archive_policy.md`: difference between this private coauthor workstation and a future journal archive.

## Dashboard

- [Dashboard guide](dashboard_guide.md)
- [Dashboard product spec](dashboard_product_spec.md)
- [Dashboard user stories](dashboard_user_stories.md)
- [Dashboard information architecture](dashboard_information_architecture.md)
