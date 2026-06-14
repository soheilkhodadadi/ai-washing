# AI Washing

Private coauthor workstation for the **AI Washing** paper.

This repository lets coauthors inspect the empirical pipeline, rerun v4.3 tables and figures, and start new tests from the same data spine. The older `semantic-patterns` repository is provenance only; this repository is the active project workspace.

## What You Can Do Here

- Understand how the paper's SEC text, classifier outputs, patent data, WRDS/Compustat/CRSP data, and event panels fit together.
- Find the script and data product behind each v4.3 manuscript table or figure.
- Rerun selected or full v4.3 table evidence from a mounted private data room.
- Modify a table script or extension starter while keeping v4.3 as the frozen reference.
- Run a strict replication and data-integrity audit before sharing or journal deposit.

## Start With The Paper Workbench

- [README_START_HERE.md](README_START_HERE.md): fastest setup and first validation path.
- [docs/empirical_workstation.md](docs/empirical_workstation.md): empirical map of data, constructs, panels, and extension lanes.
- [docs/paper_table_workbench.md](docs/paper_table_workbench.md): table-by-table guide for rerunning or modifying manuscript results.
- [docs/panel_and_data_catalog.md](docs/panel_and_data_catalog.md): catalog of cleaned panels, classifier outputs, patent match artifacts, and WRDS/market data products.
- [docs/construct_playbooks/](docs/construct_playbooks/): concise guides for changing central constructs safely.
- [manifests/paper_table_workbench.csv](manifests/paper_table_workbench.csv): machine-readable version of the paper workbench.
- [docs/coauthor_runbook.md](docs/coauthor_runbook.md): first-day commands and detailed validation path.

## Fastest Setup

Use Docker if you want the lowest-friction route. Docker keeps Python dependencies inside the container; private data are mounted from outside the image.

```bash
make docker-build
make docker-preflight
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make docker-private-check
make docker-reproduce-selected
```

Native Python remains available for direct development:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
make coauthor-preflight
```

## Private Data Boundary

Git tracks code, documentation, manifests, fixtures, and frozen v4.3 manuscript assets. It does not track private or licensed data, WRDS/CRSP/Compustat extracts, full raw SEC corpora, derived panels, credentials, local environments, caches, or generated outputs.

Set the private data root before running data-dependent checks:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
```

Keep this Git repository outside Dropbox, OneDrive, and other sync folders. Use cloud storage only for the external private data mirror. See [docs/private_data_contract.md](docs/private_data_contract.md) and [docs/coauthor_data_room.md](docs/coauthor_data_room.md).

## Table Reruns

Use the paper workbench to find the relevant `TABLE_ID`, or print a terminal summary:

```bash
make table-info TABLE_ID=T29
make data-products
make construct-info CONSTRUCT=patent_mismatch
```

Then run the table command:

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=T30 reproduce-table
```

Selected v4.3 gate:

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make docker-reproduce-selected
```

Full evidence:

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make reproduce-all-tables
AIW_DATA_ROOT=/path/to/ai-washing-private-data make reproduce-figures
```

Current expected status: all table CSV evidence matches v4.3 exactly except Appendix Table C7, which has a documented numeric-string format-only delta; figure-series CSV evidence matches, while frozen manuscript PDFs remain canonical.

## Documentation Map

See [docs/index.md](docs/index.md) for the complete navigation map, including setup, data contracts, source audits, extension starters, limitations, Docker guidance, and future journal-archive policy.
