# AI Washing Research Workstation

This private repository is the computational workstation for the **AI Washing** project. It preserves **AI Washing v4.3** as the frozen computational reference while supporting coauthor verification, extension work, and future journal replication preparation.

The repository is intentionally curated. It is not a wholesale copy of the older `semantic-patterns` workspace.

## Documentation Map

Start with `docs/index.md` for the full document map. The main operational documents are:

- `docs/coauthor_runbook.md`: first-day setup, validation, and reproduction commands.
- `docs/private_data_contract.md`: private data mirror and path contract.
- `docs/full_reproduction_status.md`: full v4.3 table and figure reproduction status.
- `docs/known_limitations.md`: documented limitations and future robustness layers.
- `docs/replication_audit_report.md`: current strict replication and data-integrity audit summary.

## What Git Tracks

- Frozen v4.3 manuscript assets and generated comparison evidence.
- Source code required by publication-table scripts and validation utilities.
- Manifests for table scripts, data dependencies, source closure, and artifact provenance.
- Small non-sensitive fixtures for smoke tests.
- Formal setup, data, method, reproduction, and audit documentation.

## What Stays Outside Git

Private, licensed, large, or machine-local data are deliberately excluded from Git. This includes raw SEC/WRDS data, full derived panels, label/evaluation parquet files, archives, generated outputs, credentials, and local environments.

Use an external private data root:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
```

The expected private paths are listed in `manifests/data_dependency_manifest.csv`, `manifests/coauthor_data_room_manifest.csv`, and `docs/private_data_contract.md`.

## Environment Setup

Recommended local setup from a fresh clone:

```bash
cd ai-washing
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Set the path contract:

```bash
export AIW_REPO_ROOT="$PWD"
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
export AIW_OUTPUT_ROOT="$PWD/outputs/reproduced"
export AIW_PAPER_ROOT="$PWD/outputs/paper_exports"
```

The direct runtime dependencies are pinned to the v4.3-validated environment because some table scripts are sensitive to floating-point and string-representation changes across package versions.

## Platform, Runtime, And Storage Notes

- Native reruns are validated on macOS with Python 3.11 and the pinned package set.
- Linux should work natively or through Docker/devcontainer because the commands use the same environment contract.
- Windows users should prefer WSL2 or Docker Desktop and mount the private data room as a normal filesystem path before setting `AIW_DATA_ROOT`.
- Docker is optional for coauthor work but useful for isolated validation. Private data are mounted from outside the image and are not bundled into it.
- Keep several GB of free disk space for generated table/figure outputs. Larger optional source corpora require more storage in the private data room.
- The code-only preflight usually takes a few minutes. Full private-data table and figure reproduction should be run after the private mirror validates.

## First Validation

Run the code-only checks first:

```bash
make doctor
make coauthor-preflight
```

`make coauthor-preflight` runs environment, manifest, path-leak, import-smoke, fixture, and Git hygiene checks. These should pass even before private data are mounted.

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

The selected numerical reproduction gate covers `T00`, `T16`, `T17`, `T09`, and `T30`:

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

## Strict Replication And Data-Integrity Audit

Before sharing or preparing a journal-facing archive, run:

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make replication-audit
```

This writes `docs/replication_audit_report.md` and machine-readable evidence under `reports/replication_audit/`. The audit checks package surface, panel sanity, SEC text construct risks, patent keyword/assignee risks, environment reproducibility, and documented limitations.

## Collaboration Model

- GitHub tracks code, docs, fixtures, manifests, and frozen manuscript assets.
- Dropbox/OneDrive can share the external private data root.
- Do not put this Git repository inside Dropbox or OneDrive.
- Keep future table changes documented in manifests and release notes before treating them as replacements for v4.3 evidence.
