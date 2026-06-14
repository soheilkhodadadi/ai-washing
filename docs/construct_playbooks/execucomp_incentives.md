# ExecuComp Incentives

## Purpose

This layer tests whether CEO incentive measures are associated with low-credibility AI disclosure.

## Source Artifacts

- Staged ExecuComp cache: `data/external/execucomp/execucomp_ceo_anncomp_2015_2024.parquet`
- Annual NLP/patent panel: `data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`
- Policy note: `docs/t25_execucomp_policy.md`

## v4.3 Definitions

Normal Test 25 reruns use the staged private ExecuComp extract. They do not require WRDS credentials. Any refresh should be explicit, local, and kept outside Git.

## Owning Scripts And Tables

- Executive incentives: `semantic_ai_washing.analysis.publication_runs.test_25_exec_incentive_mismatch` (`T25`)

## Validation Checks

- `make TABLE_ID=T25 reproduce-table`
- `make check-private-data`
- Review `docs/t25_execucomp_policy.md`

## Known Limitations

The staged extract is sufficient for v4.3 reproduction but does not exhaust all governance or incentive channels. Broader governance data should be added as extension data, not folded silently into v4.3.

## Safe Update Path

1. Refresh ExecuComp only with local WRDS access and no credential sharing.
2. Save a new cache with a versioned filename.
3. Rebuild T25 or a new extension table and compare row counts.
4. Update the catalog and playbook when promoted.

## Likely Coauthor Or Referee Questions

- Are CEO rows selected consistently?
- Are incentive measures aligned to disclosure timing?
- Do results survive alternative compensation measures?
