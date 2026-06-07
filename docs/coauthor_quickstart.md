# Coauthor Quickstart

1. Open `README_START_HERE.md` first.
2. Inspect `manifests/table_to_script_crosswalk.csv` to see which script/run supports each v4.3 table or figure.
3. Inspect `data/curated/v4_3/generated_runs/` for prior generated outputs, run manifests, writer packets, and result notes.
4. Run `make validate`, `make path-leak-scan`, `make import-smoke`, `make smoke-fixture`, and `make git-hygiene` to confirm the workstation is structurally healthy.
5. For full reruns, stage private inputs under `AIW_DATA_ROOT` using `manifests/data_dependency_manifest.csv` and `docs/private_data_staging_map.md`.
6. Start with selected table reruns: `T00`, `T16`, `T17`, `T09`, and `T30`.

The repository intentionally does not track private or licensed data. Code/manifests/docs belong in Git; large or restricted data belong in the external private data root.
