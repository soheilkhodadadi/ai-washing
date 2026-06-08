# Data Management

The AI Washing workstation separates reproducible code from private data.

## Path Contract

All executable code should use these paths instead of hard-coded machine paths:

```bash
AIW_REPO_ROOT=/path/to/ai-washing
AIW_DATA_ROOT=/path/to/ai-washing-private-data
AIW_OUTPUT_ROOT=/path/to/ai-washing/outputs/reproduced
AIW_PAPER_ROOT=/path/to/ai-washing/outputs/paper_exports
```

`AIW_DATA_ROOT` is equivalent to the repository's logical `data/` folder. A manifest path such as `data/processed/panel/file.parquet` should be staged at `$AIW_DATA_ROOT/processed/panel/file.parquet`.

## Private Data Policy

Do not commit:

- raw SEC filings or WRDS/CRSP downloads,
- derived full panels,
- label or held-out parquet files,
- large generated outputs,
- archives or transfer packages,
- machine-local reports that expose private paths.

Use `manifests/data_dependency_manifest.csv` to document required data, and use checksums outside Git for private artifact verification.

## Adding Future Data

For future extensions such as job postings or executive-compensation data:

1. Add a logical dependency path under `AIW_DATA_ROOT`.
2. Add or update the table/script crosswalk.
3. Add status notes in `docs/full_reproduction_status.md`.
4. Keep raw/private source files outside Git.
5. Commit only the script, manifest, documentation, and non-sensitive fixture needed to prove the workflow mechanics.
