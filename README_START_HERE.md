# AI Washing Research Workstation

This repository is the active empirical workstation for the **AI Washing** paper. It preserves **AI Washing v4.3** as the frozen computational reference while making it easier for coauthors to inspect the paper logic, rerun tables, and add new tests.

The repository is intentionally curated. It is not a wholesale copy of the older `semantic-patterns` workspace.

The package also includes the v5.0 editorial LaTeX source as the current manuscript-presentation benchmark. Use v5.0 for wording, captions, appendix wrappers, and table-note presentation; use v4.3 for numerical reproduction until a later release is promoted.

## If You Only Do One Thing First

Export one table bundle and open its `OPEN_FIRST.md` file. That gives the fastest view of how a manuscript result connects to the empirical question, data products, owning script, frozen v4.3 evidence, and safe modification path.

```bash
make export-table-workbench TABLE_ID=T30
open outputs/workbench/T30/OPEN_FIRST.md
```

## Three-Command Empirical Path

Use these commands after setup to move from the paper map to a concrete table and one extension lane:

```bash
make workbench-index
make export-table-workbench TABLE_ID=T30
make extension-info EXTENSION=builder_hides
```

Optional browser index:

```bash
make dashboard
open outputs/dashboard/index.html
```

Optional one-click public demo:

```bash
make public-demo
make public-demo-check
open outputs/public_demo/index.html
```

Optional local app:

```bash
make dashboard-app
```

In the Streamlit app, use **Command Center** only for approved local Make targets. It is disabled in Demo Mode, requires confirmation for private-data or output-writing commands, and stores raw logs under ignored `outputs/dashboard_runs/`.

After private data are mounted, run the first extension:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make extension-builder-hides
```

## Recommended Reading Order

1. `docs/empirical_workstation.md`: how the data, constructs, panels, tables, and extension lanes fit together.
2. `docs/coauthor_delivery_overview.md`: what the package contains and how it answers the coauthor handoff request.
3. `docs/paper_table_workbench.md`: where each manuscript table or figure comes from and how to rerun or modify it.
4. `docs/panel_and_data_catalog.md`: what the cleaned panels, classifier outputs, patent files, and WRDS/market products are.
5. `docs/v5_editorial_alignment.md`: how the v5.0 editorial source relates to the v4.3 numerical freeze.
6. `docs/construct_playbooks/`: how central constructs are built and safely updated.
7. `docs/dashboard_guide.md`: optional static and Streamlit navigation interfaces.
8. `docs/public_demo_deployment.md`: static public demo path without private data.
9. `docs/dashboard_sharing_options.md`: why generated dashboard files are local/ignored and how to share Dropbox, static, or hosted previews.
10. `docs/docker_quickstart.md`: lowest-friction setup path.
11. `docs/private_data_contract.md`: how to mount the private data room.
12. `docs/coauthor_runbook.md`: complete first-day command sequence.

The full documentation map is `docs/index.md`.

## Five-Minute Docker Path

From a fresh clone:

```bash
cd ai-washing
make docker-build
make docker-preflight
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make docker-private-check
make docker-reproduce-selected
```

Docker Desktop on macOS/Windows or Docker Engine on Linux is enough for this route. Private data are mounted read-only and are not copied into the image. See `docs/docker_quickstart.md` for Mac, Linux, and Windows/WSL2 notes.

## Native Python Path

Use this if you plan to edit code directly:

```bash
cd ai-washing
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
make coauthor-preflight
```

Set the path contract for data-dependent work:

```bash
export AIW_REPO_ROOT="$PWD"
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
export AIW_OUTPUT_ROOT="$PWD/outputs/reproduced"
export AIW_PAPER_ROOT="$PWD/outputs/paper_exports"
```

The direct runtime dependencies are pinned to the v4.3-validated environment because some table scripts are sensitive to floating-point and string-representation changes across package versions.

## Find Or Modify A Paper Table

Use `docs/paper_table_workbench.md` first. It maps each table and figure to the empirical question, primary data product, constructs, script module, rerun command, reference outputs, and safe modifications. For a terminal view, run:

```bash
make workbench-index
make table-info TABLE_ID=T29
make export-table-workbench TABLE_ID=T30
make data-products
make dashboard
make construct-info CONSTRUCT=patent_mismatch
```

Example rerun:

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=T30 reproduce-table
```

For a richer local interface, run `make dashboard-app`. Use **Table Explorer** for table review and technical drill-down. Use **Data Room** and **Construct Audits** to inspect classifier evidence, patent-match confidence, textual acronym-risk status, WRDS/CRSP/Compustat lane checks, and metadata-only private-data schema/status summaries.

Use **Public Demo Mode** when showing the dashboard outside the private data room. It is nonprivate by design and disables command execution.

If the result changes numerically, keep the original v4.3 output as the reference and document whether the change is intended for a future release.

## Run A First Extension

Extension outputs are ignored and separate from frozen v4.3 evidence:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make extension-info EXTENSION=builder_hides
make extension-builder-hides
make extension-builder-hides-ai-talk-only
make extension-info EXTENSION=washing_pays_proxy
make extension-washing-pays-proxy
make check-seo-schema SEO_FILE=/path/to/seo_offering_terms.csv
```

Use `docs/extensions/README.md` and `manifests/extension_workbench.csv` to see the purpose, data needs, and interpretation limits for each lane. The washing-pays command is a share-growth proxy screen; the stronger SEO/offering-terms version needs new data following `templates/seo_offering_terms_schema.csv`.

## What Git Tracks

- Frozen v4.3 manuscript assets and generated comparison evidence.
- v5.0 editorial LaTeX source, preserved separately from the v4.3 computational freeze.
- Source code required by publication-table scripts and validation utilities.
- Manifests for paper-table ownership, table scripts, data dependencies, source closure, and artifact provenance.
- Small non-sensitive fixtures for smoke tests.
- Formal setup, data, method, reproduction, extension, and audit documentation.

## What Stays Outside Git

Private, licensed, large, or machine-local data are deliberately excluded from Git. This includes raw SEC/WRDS data, full derived panels, label/evaluation parquet files, archives, generated outputs, access details, and local environments.

Use an external private data root:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
```

The expected private paths are listed in `manifests/data_dependency_manifest.csv`, `manifests/coauthor_data_room_manifest.csv`, and `docs/private_data_contract.md`.

## First Validation

Run code-only checks first:

```bash
make doctor
make coauthor-preflight
```

After private data are staged, validate the data mirror:

```bash
make check-private-data
make validate-data-room
make validate-sec-source
make validate-wrds-data
make validate-patent-data
make audit-artifact-coverage
```

## Reproduce v4.3 Outputs

Selected numerical reproduction gate:

```bash
make reproduce-selected
make TABLE_ID=T16 reproduce-table
make compare-selected-reproduction
```

Full table and figure evidence:

```bash
make reproduce-all-tables
make reproduce-figures
make reproduction-status
make figure-reproduction-status
```

Current expected status: 23 table CSVs match exactly, one table has a documented C7 format-only delta, and two figures remain frozen manuscript assets with regenerable candidate evidence.

## Known Data-Lane Boundary

The v4.3 target has lane-specific coverage. The annual NLP/patent lane covers 2016-2025. The event/market-return lane covers 2016-2024 because the staged CRSP/event-return inputs stop at 2024-12-31. See `docs/artifact_coverage_policy.md` before replacing or promoting private artifacts.

## v5.0 Editorial Boundary

The v5.0 editorial source is tracked under `paper/v5_0_editorial_source/`. It preserves coauthor edits to prose, captions, appendix wrappers, controls/fixed-effect rows, standard-error placement, and table notes. It does not replace the v4.3 numerical evidence. See `docs/v5_editorial_alignment.md`.

## Collaboration Model

- GitHub tracks code, docs, fixtures, manifests, and frozen manuscript assets.
- Dropbox is the canonical channel for sharing the external private data root.
- Do not put this Git repository inside Dropbox or any other sync folder.
- Keep future table changes documented in manifests and release notes before treating them as replacements for v4.3 evidence.
