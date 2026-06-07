# Final Validation Report

Generated: 2026-06-07

## Commands run

```bash
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python validate
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python path-leak-scan
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python import-smoke
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python smoke-fixture
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python compare-tables
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-v43-private-data make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python reproduce-selected
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python compare-selected-reproduction
make PYTHON=/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/.venv/bin/python git-hygiene
```

## Results

- Capsule validation: passed; 24 table assets, 2 figures, 44 dependency rows.
- Executable/config path leak scan: passed. Local absolute paths remain only in provenance docs/manifests/run evidence.
- Minimal source import smoke: passed for 34 modules using the repo-local `.venv` from `semantic-patterns`.
- Fixture pipeline: passed and wrote ignored output under `outputs/fixture/`.
- Table comparison against v4.3 manuscript inputs: completed; most v4.3 manuscript table inputs remain manuscript-facing deltas from generated evidence.
- Private data staging: all `required_current` and `support_only` unique inputs found and staged under `/Users/soheilkhodadadi/DataWork/ai-washing-v43-private-data`; only the future-extension ExecuComp/private DB placeholder remains deferred.
- Selected rerun dry-run: passed for `T00`, `T16`, `T17`, `T09`, and `T30`.
- Selected numerical reruns: completed for `T00`, `T16`, `T17`, `T09`, and `T30`.
- Selected reproduction comparison: all five fresh CSV outputs are exact SHA-256 matches to the frozen v4.3 generated CSV evidence.
- Git hygiene: passed; no tracked private/generated data paths and no tracked banned binary/archive file types.

## Current blocker for full handoff completion

The selected numerical gate has passed. The remaining work is Phase 2E full-table expansion, then optional containerization and share-package assembly. Test 25 still has a future-extension dependency on `data/external/execucomp_or_private_db`.
