# AGENTS.md - AI Washing Workstation

This repository is the canonical private workstation for the AI Washing project. Treat the older `semantic-patterns` repository as provenance only; do not add new AI Washing work there unless explicitly instructed.

## Core Rules

- Keep Git clean: track code, docs, manifests, fixtures, and frozen manuscript assets only.
- Never commit private, licensed, raw, derived panel, label, archive, or generated output data.
- Use `AIW_DATA_ROOT` for private data and `AIW_OUTPUT_ROOT` / `AIW_PAPER_ROOT` for generated outputs.
- Do not put the `.git` repository inside Dropbox, OneDrive, or other syncing folders. Use cloud storage for the external data root only.
- Keep v4.3 as the frozen computational reference until a later version is explicitly promoted.

## Validation

Use a repo-local environment when possible:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python - <<'PY'
import pandas, numpy, pyarrow
print(pandas.__version__, numpy.__version__, pyarrow.__version__)
PY
```

Before commits or handoffs, run:

```bash
make validate
make path-leak-scan
make import-smoke
make smoke-fixture
make git-hygiene
make replication-audit
```

If private data are staged, also run:

```bash
make reproduce-selected
make TABLE_ID=T16 reproduce-table
make compare-selected-reproduction
```

## Development Discipline

- Prefer small, documented changes with a clean Git status after each validated state.
- Add new table scripts to the table/script crosswalk and data dependency manifest before relying on them.
- If a script needs private data, document the logical path under `AIW_DATA_ROOT`; never hard-code local user paths.
- If a new result is intended to replace v4.3 evidence, create a new release note under `docs/releases/` rather than silently overwriting the v4.3 reference.
