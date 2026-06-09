# Coauthor Data Room

This document defines the private data room that accompanies the `ai-washing` GitHub repository. Git tracks code, docs, manifests, fixtures, and frozen v4.3 manuscript assets. The private data room stores WRDS-derived files, raw or near-raw source data, derived panels, classifier artifacts, and extension inputs.

## Operating Rule

Clone the GitHub repository into a normal local folder. Keep Dropbox, OneDrive, or another shared drive for `AIW_DATA_ROOT` only.

```bash
cd /path/to/ai-washing
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make check-private-data
make validate-data-room
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
- `required_extension`: not always needed for v4.3 reruns but needed for Kuntara/Thomas extension work or deeper audit.
- `support_only`: useful for documentation, quality checks, or validation reports.
- `raw_source`: raw or near-raw source files for bottom-up rebuilds.
- `deferred_with_reason`: intentionally not yet staged; the manifest names what to stage next.

## Current Interpretation

The current private root is enough for v4.3 table reproduction. The broad data-room manifest is now more complete: the final hybrid classifier outputs, extracted sentence support, lineage annual panels, filing spine, WRDS bridge, SEC samples, and source documentation are staged. The remaining deferred items are not table-rerun blockers unless `scripts/validate_data_room.py --strict-deferred` is run manually. They are the next data-room expansion checklist.

The coverage target is lane-specific:

- Annual NLP/patent artifacts cover 2016-2025.
- Event/market-return artifacts cover 2016-2024 because the staged CRSP return files stop at 2024-12-31.
- Filing-spine and AI-measure artifacts cover 2016-2025, but they are disclosure lineage and bridge inputs, not a completed 2025 return-event panel.
- Full raw SEC filings are not bundled. The data room includes representative SEC full-submission samples, representative 2025 Stage-One cleaned filings, and source links so coauthors can obtain the full source corpus if they want a bottom-up raw rebuild.

## Coauthor Request Coverage

Kuntara requested the full data and code: cleaned panel, patent match, classifier outputs, CRSP and Compustat merges, and table-building scripts. The current repository tracks the publication scripts and staged table-rerun inputs. The data-room manifest now stages the final classifier outputs and core lineage/provenance files, while keeping a visible queue for remaining broader artifacts such as standalone patent-source files, Compustat source/merge intermediates, and future extension inputs.
