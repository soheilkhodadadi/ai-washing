# Coauthor Data Room

This document defines the private data room that accompanies the `ai-washing` GitHub repository. Git tracks code, docs, manifests, fixtures, and frozen v4.3 manuscript assets. The private data room stores WRDS-derived files, raw or near-raw source data, derived panels, classifier artifacts, and extension inputs.

## Operating Rule

Clone the GitHub repository into a normal local folder. Keep Dropbox for `AIW_DATA_ROOT` only; do not sync the Git repository itself.

```bash
cd /path/to/ai-washing
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make check-private-data
make validate-data-room
make validate-wrds-data
make validate-patent-data
make validate-sec-source
make audit-artifact-coverage
```

Do not commit private data. Do not share WRDS credentials. If a coauthor wants to refresh WRDS data, they should use their own local `.env` and explicit refresh commands.

## Manifest

The coauthor data-room manifest is `manifests/coauthor_data_room_manifest.csv`. It is broader than `manifests/data_dependency_manifest.csv`:

- `data_dependency_manifest.csv` is the runtime input contract for v4.3 table reruns.
- `coauthor_data_room_manifest.csv` is the handoff contract for full coauthor work, including raw sources, intermediate NLP artifacts, patent-match lineage, CRSP/Compustat bridges, and future extension inputs.
- `artifact_provenance_audit.csv` is the lane-specific promotion gate. It prevents April/v4.3 artifacts from being confused with older March/v3 artifacts or future-extension candidates.

Roles:

- `required_reproduction`: needed to reproduce v4.3 tables.
- `required_extension`: not always needed for v4.3 reruns but needed for coauthor extension work or deeper audit.
- `support_only`: useful for documentation, quality checks, or validation reports.
- `raw_source`: raw or near-raw source files for bottom-up rebuilds.
- `deferred_with_reason`: intentionally not yet staged; the manifest names what to stage next.

## Current Interpretation

The current private root is enough for v4.3 table reproduction and is now substantially broader than the table-rerun surface. The final hybrid classifier outputs, extracted sentence support, lineage annual panels, filing spine, WRDS/CRSP/Compustat bridge artifacts, WRDS raw-pull/build reports, SEC samples, patent counts/examples/diagnostics, patent identity metadata, patent keyword metadata, PatentsView source documentation, and patent method reports are staged. The remaining deferred items are not table-rerun blockers unless `scripts/validate_data_room.py --strict-deferred` is run manually. They are documented future-extension inputs, not hidden reproduction dependencies.

The coverage target is lane-specific:

- Annual NLP/patent artifacts cover 2016-2025.
- Event/market-return artifacts cover 2016-2024 because the staged CRSP return files stop at 2024-12-31.
- Filing-spine and AI-measure artifacts cover 2016-2025, but they are disclosure lineage and bridge inputs, not a completed 2025 return-event panel.
- Full raw SEC filings are not bundled. The data room includes representative SEC full-submission samples, representative 2025 Stage-One cleaned filings, and source links so coauthors can obtain the full source corpus if they want a bottom-up raw rebuild.

## SEC Source Policy Gate

The SEC source layer has its own validator:

```bash
make validate-sec-source
```

This reads `manifests/sec_source_manifest.csv` and checks the representative SEC source samples, Stage-One source links, extracted AI sentence support, and final hybrid classifier outputs. The expected current anchors are 5 SEC full-submission samples, 4 Stage-One 2025 samples, 106,977 extracted AI sentences for 2016-2024, 40,902 extracted AI sentences for 2025, and 147,879 final hybrid classified AI sentences for 2016-2025.

The policy is intentional: the full raw SEC corpus is not bundled unless coauthors specifically request a bottom-up raw rebuild. The practical coauthor audit surface is source samples plus extracted sentences plus final classifier outputs. See `docs/sec_raw_source_policy.md` and `docs/sec_extraction_classification_audit.md`.

## Coauthor Request Coverage

The coauthor handoff request asked for the full data and code: cleaned panel, patent match, classifier outputs, CRSP and Compustat merges, and table-building scripts. The current repository tracks the publication scripts and staged table-rerun inputs. The data-room manifest now stages the final classifier outputs, patent-match lineage, keyword/identity metadata, Compustat fundamentals extract, CRSP monthly/index and daily return inputs, CIK-GVKEY-PERMNO bridge files, WRDS build reports, and core provenance files. The visible remaining queue is now limited to future extension data such as actual SEO/offering terms and optional job-posting data.



## Extension Starter Layer

The extension layer helps coauthors begin testing without changing the v4.3 freeze.

```bash
make builder-hides-first-pass
```

This writes ignored outputs under `outputs/extensions/builder_hides_right_tail/` unless `AIW_OUTPUT_ROOT` is set. The supporting docs are:

- `docs/extensions/builder_hides_first_pass.md`
- `docs/extensions/washing_pays_data_requirements.md`

The washing-pays strong version still requires external issuance terms under `data/external/seo_offering_terms`; the current package only supports the share-growth proxy screen.

## WRDS / CRSP / Compustat Gate

The CRSP, Compustat, and linkage layer has its own validator:

```bash
make validate-wrds-data
```

This reads `manifests/wrds_data_manifest.csv` and checks the staged Compustat fundamentals extract, CRSP monthly/index extracts, daily filing-event returns, annual market features, CIK-GVKEY crosswalk, annual WRDS backbone, filing-level WRDS bridge, unmatched-tail audit file, and WRDS reports/notes. The supporting docs are:

- `docs/wrds_crsp_compustat_method_note.md`
- `docs/wrds_source_inventory.md`

Normal reproduction does not require WRDS credentials. Refreshing WRDS data is an explicit coauthor action using that coauthor's own WRDS access, followed by validation before promotion.

## Patent Data Gate

Patent matching is the central construct-audit layer. In addition to the broad data-room check, run:

```bash
make validate-patent-data
```

This validates `manifests/patent_data_manifest.csv` against `$AIW_DATA_ROOT`. It checks the final grant and pregrant count files, example files, diagnostics, hybrid lookup/alias metadata, patent keyword files, PatentsView source documentation, final matching/fuzzy-sensitivity reports, and the generated coauthor audit sample.

Before sharing the patent evidence pack, run:

```bash
make patent-example-audit
make validate-patent-data
```

The supporting method notes are tracked in Git:

- `docs/patent_mismatch_method_note.md`
- `docs/patent_matching_validation.md`
- `docs/patent_source_inventory.md`
- `docs/patent_fuzzy_sensitivity_note.md`
