# Phase 4G Final Coauthor Package Rehearsal

Date: 2026-06-10

## Verdict

Phase 4G passes.

The canonical AI Washing workstation is ready for a private coauthor rehearsal: a coauthor can clone the private GitHub repository, mount a private `AIW_DATA_ROOT`, run validation gates, inspect staged source/data evidence, reproduce the frozen v4.3 table surface, and begin extension work without using Soheil's old local `semantic-patterns` workspace.

This does not mean the paper is publication-final. It means the computational package is now coherent enough to share with Kuntara/Thomas for audit, reruns, and extension testing.

## Scope Rehearsed

Canonical repository:

```text
/Users/soheilkhodadadi/DataWork/ai-washing
```

Canonical private data root:

```text
/Users/soheilkhodadadi/DataWork/ai-washing-private-data
```

Private GitHub repository:

```text
https://github.com/soheilkhodadadi/ai-washing
```

Code state rehearsed before this report commit:

```text
6ff13ec Harden read-only coauthor data rehearsal
```

Fresh-clone rehearsal directory:

```text
/tmp/aiw-fresh-clone-phase4g-o3B5Mo/ai-washing
```

Docker image used:

```text
ai-washing-phase4g
```

## Validation Summary

| Layer | Result | Evidence |
| --- | --- | --- |
| Local repo validation | Pass | `make validate`, `make path-leak-scan`, `make import-smoke`, `make smoke-fixture`, and `make git-hygiene` passed. |
| Local test suite | Pass | `python -m pytest -q` reported 20 passed. |
| Private data mirror | Pass | `make check-private-data` reported 15 of 15 logical runtime paths present. |
| Coauthor data room | Pass with documented extension gaps | `make validate-data-room` reported 35 present rows and 2 deferred future-extension rows: `seo_offering_terms` and `job_postings`. |
| SEC source policy | Pass | `make validate-sec-source` reported 7 of 7 source-policy rows present. |
| WRDS/CRSP/Compustat evidence pack | Pass | `make validate-wrds-data` reported 16 of 16 rows present. |
| Patent evidence pack | Pass | `make validate-patent-data` reported 29 of 29 rows present. |
| Artifact coverage | Pass | `make audit-artifact-coverage` reported 20 `coverage_pass` rows and 2 documented `not_promoted` candidates. |
| Patent audit examples | Pass | `make patent-example-audit` produced 40 balanced grant/pregrant examples using a configurable output path. |
| Full v4.3 table reproduction | Pass | `make reproduce-all-tables` reported 23 `csv_exact_match`, 1 `format_only_delta`, and 2 `frozen_asset_only`. |
| Fresh-clone Docker rehearsal | Pass | Clean GitHub clone plus read-only private-data mount passed validation, full reproduction, and 20 tests. |

## Reproduction Status

The full v4.3 reproduction ledger remains:

```text
csv_exact_match: 23
format_only_delta: 1
frozen_asset_only: 2
```

Interpretation:

- The numeric table CSV evidence is stable for all but one documented format-only case.
- The remaining `format_only_delta` is a formatting/representation issue, not an unexplained numerical difference.
- Figures remain frozen manuscript assets by design unless a future phase explicitly promotes regeneration scripts.

Selected table checks also remain clean for the core rehearsal targets:

```text
T00, T16, T17, T09, T30: CSV exact matches against frozen v4.3 generated evidence.
```

Some manuscript-facing TeX/table-wrapper deltas remain because the manuscript files include captions, notes, resizing, or hand-facing wrappers around generated evidence. These are already treated separately from numerical CSV reproduction.

## Container Rehearsal

Two container modes were rehearsed.

### Without Private Data

Docker validation without private data passed for code-only checks and failed only at private-data gates with controlled missing-data messages. This is the expected behavior for a fresh clone before the coauthor has mounted the private data room.

### With Read-Only Private Data

Docker validation with the private data root mounted read-only passed:

```text
-v /Users/soheilkhodadadi/DataWork/ai-washing-private-data:/workspaces/ai-washing-private-data:ro
```

This is the strongest practical coauthor test because it proves normal reproduction does not need to mutate shared private data.

## Issue Found And Fixed During Rehearsal

The first read-only Docker run exposed a real coauthor-readiness bug: the Ken French factor staging helper tried to rewrite extraction folders under `AIW_DATA_ROOT` even when the parsed monthly factor cache already existed.

Fix implemented:

- `src/semantic_ai_washing/analysis/ken_french_factors.py` now reuses the cached parsed factor parquet when `refresh=False`.
- `tests/test_ken_french_factors.py` verifies that cached parsed factors can be read without raw/extracted factor folders.
- `make patent-example-audit` now supports `PATENT_AUDIT_OUTPUT=...`, so audit examples can be written to repo outputs instead of mutating the private data room during read-only rehearsals.

This fix materially improves Kuntara's first-day experience because the private data room can be mounted as read-only for validation and reproduction.

## Remaining Non-Blocking Items After Phase 4G

These are not blockers for coauthor handoff, but they should stay visible.

- `seo_offering_terms` remains deferred because the strong washing-pays extension needs actual SEO/offering terms beyond the current CRSP `shrout`-growth proxy.
- `job_postings` remains deferred because it is a future extension input, not a v4.3 reproduction dependency.
- Figures are frozen by design in Phase 4G; Phase 4H adds regeneration evidence without replacing frozen manuscript PDFs.
- One full-table asset remains a `format_only_delta` rather than a CSV exact match; Phase 4H documents this at the cell level.
- `test_05_size_heterogeneity.py` emitted a pandas `FutureWarning` on `.fillna` downcasting during Phase 4G. Phase 4H removes this warning and adds a regression test.

## Recommended Coauthor Sharing Procedure

1. Share the private GitHub repository with Kuntara/Thomas.
2. Share the private data room through Dropbox/OneDrive or another private channel.
3. Ask the coauthor to clone the repo outside Dropbox/OneDrive.
4. Ask the coauthor to place or mirror private data outside Git and set `AIW_DATA_ROOT`.
5. Start with:

```bash
make validate
make import-smoke
make smoke-fixture
AIW_DATA_ROOT=/path/to/ai-washing-private-data make check-private-data
AIW_DATA_ROOT=/path/to/ai-washing-private-data make validate-data-room
AIW_DATA_ROOT=/path/to/ai-washing-private-data make reproduce-all-tables
make reproduction-status
```

6. For a stronger environment match, use the Docker path in `docs/coauthor_runbook.md` and mount `AIW_DATA_ROOT` read-only.

## Final Gate

Phase 4G gate is satisfied: the package has now been tested as a local repo, a Dockerized repo, and a fresh GitHub clone with mounted private data. No unexplained numerical reproduction difference remains in the v4.3 table surface.
