# Coauthor Quickstart

1. Clone the private `ai-washing` GitHub repository into a normal local folder, not Dropbox or OneDrive.
2. Open `README_START_HERE.md` first.
3. Create a local `.venv`, install the package with `python -m pip install -e .`, and run the quick validation commands.
4. Inspect `manifests/table_to_script_crosswalk.csv` to see which script/run supports each v4.3 table or figure.
5. Inspect `data/curated/v4_3/generated_runs/` for prior generated outputs, run manifests, writer packets, and result notes.
6. For full reruns, stage private inputs under `AIW_DATA_ROOT` using `manifests/data_dependency_manifest.csv` and `docs/private_data_staging_map.md`.
7. Start with selected table reruns: `T00`, `T16`, `T17`, `T09`, and `T30`.

The repository intentionally does not track private or licensed data. Code/manifests/docs belong in Git; large or restricted data belong in the external private data root.
