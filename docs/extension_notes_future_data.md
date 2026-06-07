# Extension Notes For Future Data

If the project later adds job postings, updated patent data, or new market data, avoid editing the v4.3 freeze directly. Instead:

1. Create a new versioned input folder under `data/processed/` or an external `AIW_DATA_ROOT`.
2. Add the new artifact to `manifests/data_dependency_manifest.csv` with a versioned filename and checksum.
3. Add a new script/run row to `manifests/table_to_script_crosswalk.csv` only when it supports a manuscript table or planned appendix table.
4. Keep v4.3 generated evidence unchanged.
5. Record any new manuscript target as v4.4 or later.

This prevents the coauthor-facing handoff from drifting away from the exact v4.3 target.
