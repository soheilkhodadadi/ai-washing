# Coauthor Data Room

This document defines the private data room that accompanies the `ai-washing` GitHub repository. Git tracks code, docs, manifests, fixtures, and frozen v4.3 manuscript assets. The private data room stores WRDS-derived files, raw or near-raw source data, derived panels, classifier artifacts, and extension inputs.

## Operating Rule

Clone the GitHub repository into a normal local folder. Keep Dropbox, OneDrive, or another shared drive for `AIW_DATA_ROOT` only.

```bash
cd /path/to/ai-washing
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make check-private-data
make validate-data-room
```

Do not commit private data. Do not share WRDS credentials. If a coauthor wants to refresh WRDS data, they should use their own local `.env` and explicit refresh commands.

## Manifest

The coauthor data-room manifest is `manifests/coauthor_data_room_manifest.csv`. It is broader than `manifests/data_dependency_manifest.csv`:

- `data_dependency_manifest.csv` is the runtime input contract for v4.3 table reruns.
- `coauthor_data_room_manifest.csv` is the handoff contract for full coauthor work, including raw sources, intermediate NLP artifacts, patent-match lineage, CRSP/Compustat bridges, and future extension inputs.

Roles:

- `required_reproduction`: needed to reproduce v4.3 tables.
- `required_extension`: not always needed for v4.3 reruns but needed for Kuntara/Thomas extension work or deeper audit.
- `support_only`: useful for documentation, quality checks, or validation reports.
- `raw_source`: raw or near-raw source files for bottom-up rebuilds.
- `deferred_with_reason`: intentionally not yet staged; the manifest names what to stage next.

## Current Interpretation

The current private root is enough for v4.3 reproduction except that the broad data-room items remain partially staged. The missing/deferred items are not table-rerun blockers unless `scripts/validate_data_room.py --strict-deferred` is run manually. They are the next data-room expansion checklist.

## Coauthor Request Coverage

Kuntara requested the full data and code: cleaned panel, patent match, classifier outputs, CRSP and Compustat merges, and table-building scripts. The current repository already tracks the publication scripts and staged table-rerun inputs. The data-room manifest adds a visible queue for the broader requested artifacts, especially standalone patent-match lineage, classifier outputs, raw/near-raw SEC filings, and Compustat/CRSP merge intermediates.
