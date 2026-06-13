# Replication Audit Report

## Verdict

The replication audit found no stop-the-line reproduction or package-surface failure. It does surface construct-validity risks, especially short-acronym AI/ML ambiguity, that should be documented as limitations and future robustness layers.

## Command Outcomes

- `package_surface`: exit `0`
  `AI Washing package surface audit
  - rows: 540
  - stop_the_line: 0
  - wrote: /workspaces/ai-washing/reports/replication_audit/package_surface_audit.csv
  - wrote: /workspaces/ai-washing/reports/replication_audit/package_surface_audit.md`
- `data_sanity`: exit `0`
  `AI Washing data sanity audit
  - checks: 71
  - stop_the_line_failures: 0
  - wrote: /workspaces/ai-washing/reports/replication_audit/data_sanity_audit.csv
  - wrote: /workspaces/ai-washing/reports/replication_audit/data_sanity_summary.md`
- `textual_construct`: exit `0`
  `AI Washing textual construct audit
  - final classified sentences: 147879
  - short_acronym_only: 83253 (56.30%)
  - ml_unit_context: 22
  - wrote: /workspaces/ai-washing/reports/replication_audit/textual_construct_audit.csv
  - wrote: /workspaces/ai-washing/reports/replication_audit/textual_construct_red_flags.csv
  - wrote: /workspaces/ai-washing/reports/replication_audit/textual_construct_summary.md`
- `patent_construct`: exit `0`
  `AI Washing patent construct audit
  - grant examples: 1403
  - pregrant examples: 1920
  - stop_the_line_failures: 0
  - wrote: /workspaces/ai-washing/reports/replication_audit/patent_construct_audit.csv
  - wrote: /workspaces/ai-washing/reports/replication_audit/patent_construct_red_flags.csv
  - wrote: /workspaces/ai-washing/reports/replication_audit/patent_construct_summary.md`
- `journal_reproducibility`: exit `0`
  `AI Washing journal reproducibility audit
  - checks: 21
  - stop_the_line_failures: 0
  - wrote: /workspaces/ai-washing/reports/replication_audit/journal_reproducibility_audit.csv
  - wrote: /workspaces/ai-washing/reports/replication_audit/journal_reproducibility_audit.md`

## Generated Evidence

- `reports/replication_audit/package_surface_audit.md`
- `reports/replication_audit/data_sanity_summary.md`
- `reports/replication_audit/textual_construct_summary.md`
- `reports/replication_audit/patent_construct_summary.md`
- `reports/replication_audit/journal_reproducibility_audit.md`

## Replication Audit Summary

- Package hygiene: coauthor-facing runbooks are appropriate for the private collaboration package, while informal phase notes and email drafts remain outside the shared repo.
- Data integrity: row counts, lane coverage, duplicate keys, impossible values, and private-data availability are now checked mechanically.
- Textual construct validity: short-acronym AI/ML hits are quantified and sampled as documented construct-validity evidence.
- Patent construct validity: short-acronym-only keyword evidence and potential ML-as-unit contexts are quantified and sampled.
- Reproducibility: the environment, package dependencies, table/figure statuses, C7 format delta, and Git hygiene are checked from one command.
