# Coauthor Quickstart

1. Clone the private `ai-washing` GitHub repository into a normal local folder, not Dropbox or OneDrive.
2. Open `README_START_HERE.md` first.
3. Prefer Docker for the first run: `make docker-build` then `make docker-preflight`. Use native `.venv` setup only if you want direct Python development.
4. Open `docs/empirical_workstation.md` for the project map.
5. Open `docs/paper_table_workbench.md` or `manifests/paper_table_workbench.csv` to see which script, data product, and rerun command supports each v4.3 table or figure.
6. Inspect `data/curated/v4_3/generated_runs/` for prior generated outputs, run manifests, writer packets, and result notes.
7. For full reruns, stage private inputs under `AIW_DATA_ROOT` using `manifests/data_dependency_manifest.csv` and `docs/private_data_contract.md`.
8. Start with selected table reruns: `T00`, `T16`, `T17`, `T09`, and `T30`.

The repository intentionally does not track private or licensed data. Code/manifests/docs belong in Git; large or restricted data belong in the external private data root.
