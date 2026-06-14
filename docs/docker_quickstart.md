# Docker Quickstart

Docker is the lowest-friction way to run the AI Washing workstation because the Python environment is built once inside a container. Coauthors still need the private data room separately, but they do not need to install Python packages by hand.

## What To Install

- Git, to clone the private repository.
- Docker Desktop on macOS or Windows, or Docker Engine on Linux.
- On Windows, use WSL2 or Docker Desktop with file sharing enabled for the folder that contains the private data mirror.

No private data are copied into the Docker image. Private data are mounted read-only at runtime.

## First Code-Only Check

From the cloned repository:

```bash
make docker-build
make docker-preflight
```

This builds the image and runs the code-only validation suite inside Docker. It does not require the private data room.

## Connect The Private Data Room

Set `AIW_DATA_ROOT` to the local Dropbox/private-data mirror:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
```

Then run:

```bash
make docker-private-check
```

Expected result: the private-data manifest checks pass, with only documented future-extension datasets deferred.

## Reproduce The Selected v4.3 Gate

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make docker-reproduce-selected
```

This runs the selected v4.3 gate inside Docker: dry-run checks for `T00`, `T16`, `T17`, `T09`, and `T30`, then an actual `T16` rerun and comparison.

## Run The Full Replication Audit

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make docker-replication-audit
```

This runs the strict replication and data-integrity audit from inside the container and writes the report to `docs/replication_audit_report.md`.

## Final Share-Readiness Check

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make share-readiness
```

This checks Docker availability, Docker Compose availability, image build, code-only container preflight, controlled failure without private data, and successful private-data mount validation.

## Interactive Shell

For interactive inspection:

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make docker-shell
```

Inside the shell, normal Make targets work:

```bash
make doctor
make check-private-data
make TABLE_ID=T16 reproduce-table
```

## Optional Dashboard App

The static dashboard does not require Docker:

```bash
make dashboard
open outputs/dashboard/index.html
```

For the optional Streamlit/Plotly app inside Docker:

```bash
make docker-build
make docker-dashboard-app
```

The app reads repository manifests only. It does not display private data values or execute empirical commands from the browser.

## Platform Notes

- macOS: Docker Desktop is the simplest route. Keep the repository outside Dropbox and mount only the private data mirror.
- Linux: Docker Engine is sufficient. If generated files appear with unexpected ownership, rerun from the Make targets, which pass the host user ID into the container.
- Windows: use WSL2 paths where possible. Avoid mixing Windows paths and WSL paths in `AIW_DATA_ROOT`; set the variable from the same shell used to run Make.
