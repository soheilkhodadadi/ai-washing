# Final Validation Report

Generated: 2026-06-08

## Commands Run

```bash
make validate
make path-leak-scan
make import-smoke
make smoke-fixture
make compare-tables
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make reproduce-selected
make compare-selected-reproduction
make git-hygiene
```

## Results

- Workstation validation: passed; 24 table assets, 2 figures, 44 dependency rows.
- Executable/config path leak scan: passed. Local absolute paths remain only in provenance docs/manifests/run evidence.
- Minimal source import smoke: passed for 34 modules.
- Fixture pipeline: passed and wrote ignored output under `outputs/fixture/`.
- Table comparison against v4.3 manuscript inputs: completed; most v4.3 manuscript table inputs remain manuscript-facing deltas from generated evidence.
- Private data staging: all `required_current` and `support_only` unique inputs found and staged under `/Users/soheilkhodadadi/DataWork/ai-washing-private-data`; only the future-extension ExecuComp/private DB placeholder remains deferred.
- Selected rerun dry-run: passed for `T00`, `T16`, `T17`, `T09`, and `T30`.
- Selected numerical reruns: completed for `T00`, `T16`, `T17`, `T09`, and `T30`.
- Selected reproduction comparison: all five fresh CSV outputs are exact SHA-256 matches to the frozen v4.3 generated CSV evidence.
- Environment pinning: an initial fresh environment with `pandas 3.0.3` / `numpy 2.4.6` caused a tiny `T09` CSV representation delta; pinning back to the v4.3-validated stack restored exact matching.
- Git hygiene: passed; no tracked private/generated data paths and no tracked banned binary/archive file types.

## Current Blocker For Full Reproduction Completion

The selected numerical gate has passed. The remaining work is full-table expansion, then optional containerization and share-package assembly. Test 25 still has a future-extension dependency on `data/external/execucomp_or_private_db`.
