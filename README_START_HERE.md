# AI Washing Research Workstation

This private repository is the canonical computational workstation for the **AI Washing** project. It preserves **AI Washing v4.3** as the current frozen computational reference while giving the project a permanent place for future coauthor work, journal revisions, and reproducibility checks.

The workstation is intentionally curated. It is not a wholesale copy of the older `semantic-patterns` repository. That older repository remains provenance; this repository is where future AI Washing code, manifests, validation docs, and manuscript-facing reproduction logic should live.

## What Git Tracks

- `paper/v4_3_source/`: frozen v4.3 LaTeX source and manuscript table/figure inputs.
- `paper/ai_washing_v4.3.pdf`: frozen v4.3 manuscript PDF.
- `manifests/`: table/script/data/artifact lineage files.
- `manifests/artifact_provenance_audit.csv`: lane-specific artifact provenance and coverage gate.
- `data/curated/v4_3/generated_runs/`: safe generated run evidence used for v4.3 comparisons.
- `data/fixtures/`: tiny non-sensitive fixture data for smoke tests.
- `src/semantic_ai_washing/`: minimal source closure needed by mapped publication scripts.
- `src/semantic_ai_washing_min/`: workstation-specific fixture and validation utilities.
- `scripts/`: validation, comparison, hygiene, and reproduction wrappers.
- `docs/`: collaboration guidance, release notes, data management, and reproduction status.

## What Stays Outside Git

Private, licensed, large, or machine-local data are deliberately excluded from Git. This includes raw SEC/WRDS data, full derived panels, label/evaluation parquet files, archives, and generated outputs.

Use an external private data root and point the workstation to it:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
```

The expected private input paths are listed in `manifests/data_dependency_manifest.csv` and summarized in `docs/private_data_staging_map.md` and `docs/private_data_contract.md`.

The v4.3 target has lane-specific coverage. The annual NLP/patent lane covers 2016-2025, while the event/market-return lane covers 2016-2024 because the staged CRSP/event-return inputs stop at 2024-12-31. See `docs/artifact_coverage_policy.md` before replacing or promoting any private artifact.

## Environment Setup

Recommended local setup from a fresh clone:

```bash
cd ai-washing
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python - <<'PY'
import pandas, numpy, pyarrow
print(pandas.__version__, numpy.__version__, pyarrow.__version__)
PY
```

Then set the explicit path contract:

```bash
export AIW_REPO_ROOT="$PWD"
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
export AIW_OUTPUT_ROOT="$PWD/outputs/reproduced"
export AIW_PAPER_ROOT="$PWD/outputs/paper_exports"
```

If `.venv` is not available yet, pass another Python interpreter with `make PYTHON=/path/to/python ...`.

The direct runtime dependencies are pinned to the v4.3-validated environment because some table scripts are sensitive to floating-point/string representation changes across `pandas` and `numpy` major versions.

## Platform, Runtime, And Storage Notes

- Native reruns are validated on Mac with Python 3.11 and the pinned package set in this repository.
- Linux should work either natively or through the Docker/devcontainer path because the reproduction commands use the same environment contract.
- Windows users should prefer WSL2 or Docker Desktop and mount the private data room as a normal filesystem path before setting `AIW_DATA_ROOT`.
- Docker is optional for coauthor work but useful for journal-style isolation checks; it does not bundle private data and expects `AIW_DATA_ROOT` to be mounted from outside the image.
- Expected storage depends on the private data room rather than the Git repository. Keep several GB of free disk space for generated table/figure outputs and substantially more if staging larger optional source corpora.
- Expected runtime for the code-only preflight is a few minutes; full private-data table and figure reproduction is longer and should be run after the private mirror validates.

## Quick Validation

Start with the environment doctor and the non-mutating coauthor preflight:

```bash
make doctor
make coauthor-preflight
```

`make coauthor-preflight` runs the first-day code-only checks that should pass before private data are mounted: `doctor`, `validate`, `path-leak-scan`, `import-smoke`, `smoke-fixture`, and `git-hygiene`.

The individual checks are also available:

```bash
make validate
make path-leak-scan
make import-smoke
make smoke-fixture
make git-hygiene
```

If private data are staged, validate the mirror before rerunning tables:

```bash
make check-private-data
make validate-data-room
make validate-sec-source
make validate-wrds-data
make validate-patent-data
make audit-artifact-coverage
```

## Comparison And Rerun Preflight

```bash
make compare-tables
make reproduce-selected
```

`reproduce-selected` dry-runs the selected reference targets `T00`, `T16`, `T17`, `T09`, and `T30`. It reports missing private inputs without failing the workstation.

## Selected Table Reruns

After private inputs are staged under `AIW_DATA_ROOT`, run one table at a time:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
export AIW_OUTPUT_ROOT="$PWD/outputs/reproduced"
export AIW_PAPER_ROOT="$PWD/outputs/paper_exports"
make TABLE_ID=T16 reproduce-table
```

Recommended first rerun targets: `T00`, `T16`, `T17`, `T09`, and `T30`.

## Full Tables, Figures, And Known Deltas

Full v4.3 table reproduction is controlled by:

```bash
make reproduce-all-tables
make reproduction-status
```

Figure regeneration is available as an audit layer, but the frozen manuscript PDFs remain canonical for v4.3:

```bash
make reproduce-figures
make figure-reproduction-status
```

The figure runner regenerates candidate figure outputs and compares the figure-series CSV evidence against the frozen v4.3 exports. Current figure data match exactly; generated PDF hashes differ from the frozen manuscript PDFs because manuscript rendering/layout is preserved as the official v4.3 artifact. See `docs/figure_reproduction_status.md`.

The one known CSV format-only table delta is `C7`, where 16 numeric-string cells differ only at floating-point representation depth. The TeX output is exact and the numeric deltas are bounded at `1e-10`. See `docs/c7_format_delta_explanation.md` and refresh the evidence with:

```bash
make c7-format-delta
```

## Collaboration Model

- GitHub tracks code, docs, fixtures, manifests, and frozen manuscript assets.
- Dropbox/OneDrive can share the external private data root.
- Do **not** put this `.git` repository inside Dropbox or OneDrive; clone it into a normal local working folder and set `AIW_DATA_ROOT` to the shared or mirrored data folder.
- See `docs/collaboration_workflow.md`, `docs/data_management.md`, `docs/private_data_contract.md`, and `docs/coauthor_runbook.md` before adding new data or scripts.

## Current Status

The selected numerical reproduction gate has passed for `T00`, `T16`, `T17`, `T09`, and `T30`: fresh reproduced CSV outputs exactly match the frozen v4.3 generated CSV evidence. Full-table expansion is controlled through `scripts/reproduce_assets.py` and the `reproduce-all-tables-*` Make targets.

The artifact-coverage gate makes the March/v3 versus April/v4.3 distinction explicit: final classifier and annual NLP/patent artifacts cover 2016-2025, but event/market-return artifacts are intentionally 2016-2024 for v4.3 reproduction.

For sharing, open `docs/coauthor_share_note.md` first, use `docs/onedrive_data_room_checklist.md` as the private data-room upload checklist, and keep `docs/phase4h_pre_share_polish_report.md` as the validation record.

## Referee-Style Audit Layer

Before sharing or preparing a journal-facing replication archive, run the hostile-but-fair data-editor audit:

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make referee-audit
```

This writes `docs/referee_first_impression_report.md` plus machine-readable evidence under `reports/referee/`. The audit checks package surface, panel sanity, SEC text construct risks, patent keyword/assignee risks, and reproduction hygiene. It is intentionally stricter than the coauthor preflight: its job is to find issues before a referee, data editor, or coauthor does.

Use `docs/journal_replication_archive_policy.md` to separate the current coauthor package from a future journal archive. Coauthor notes and phase reports are useful here, but they should be excluded from a cold journal replication archive.
