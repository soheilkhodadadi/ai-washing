# AI Washing

Canonical private research workstation for the **AI Washing** project.

This repository contains the code, manifests, documentation, fixtures, and frozen v4.3 manuscript assets needed to audit and reproduce the current computational version of the paper. Private or licensed data are kept outside Git under `AIW_DATA_ROOT`.

## Start Here

- [README_START_HERE.md](README_START_HERE.md): setup, validation, and reproduction guide.
- [docs/index.md](docs/index.md): documentation map.
- [docs/docker_quickstart.md](docs/docker_quickstart.md): lowest-friction Docker path.
- [docs/coauthor_runbook.md](docs/coauthor_runbook.md): first-day coauthor runbook.
- [docs/private_data_contract.md](docs/private_data_contract.md): private data mirror contract.
- [docs/full_reproduction_status.md](docs/full_reproduction_status.md): v4.3 table/figure reproduction status.
- [docs/replication_audit_report.md](docs/replication_audit_report.md): strict replication and data-integrity audit summary.

## Repository Boundary

Git tracks code, documentation, manifests, small fixtures, and frozen manuscript assets. It does not track private data, WRDS/CRSP/Compustat extracts, raw SEC corpora, large derived panels, credentials, local environments, caches, or generated outputs.

Set the private data root before running data-dependent checks:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
```

Keep the Git repository outside Dropbox, OneDrive, and other sync folders. Use cloud storage only for the external private data mirror.

## Quick Check

Recommended Docker path:

```bash
make docker-build
make docker-preflight
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make docker-private-check
make docker-reproduce-selected
make docker-replication-audit
```

Native Python remains available for technical users:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
make coauthor-preflight
```

See [docs/docker_quickstart.md](docs/docker_quickstart.md) for Mac, Linux, and Windows/WSL2 notes.
