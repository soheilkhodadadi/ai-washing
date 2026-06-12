# Referee First-Impression Report

## Verdict

The referee audit found no stop-the-line reproduction or package-surface failure. It does surface honest construct-validity risks, especially short-acronym AI/ML ambiguity, that should be disclosed as limitations and future audit layers.

## Command Outcomes

- `package_surface`: exit `0`
  `AI Washing package surface audit
  - rows: 535
  - stop_the_line: 0
  - wrote: /Users/soheilkhodadadi/DataWork/ai-washing/reports/referee/package_surface_audit.csv
  - wrote: /Users/soheilkhodadadi/DataWork/ai-washing/reports/referee/package_surface_audit.md`
- `data_sanity`: exit `0`
  `AI Washing data sanity audit
  - checks: 71
  - stop_the_line_failures: 0
  - wrote: /Users/soheilkhodadadi/DataWork/ai-washing/reports/referee/data_sanity_audit.csv
  - wrote: /Users/soheilkhodadadi/DataWork/ai-washing/reports/referee/data_sanity_summary.md`
- `textual_construct`: exit `0`
  `AI Washing textual construct audit
  - final classified sentences: 147879
  - short_acronym_only: 83253 (56.30%)
  - ml_unit_context: 22
  - wrote: /Users/soheilkhodadadi/DataWork/ai-washing/reports/referee/textual_construct_audit.csv
  - wrote: /Users/soheilkhodadadi/DataWork/ai-washing/reports/referee/textual_construct_red_flags.csv
  - wrote: /Users/soheilkhodadadi/DataWork/ai-washing/reports/referee/textual_construct_summary.md`
- `patent_construct`: exit `0`
  `AI Washing patent construct audit
  - grant examples: 1403
  - pregrant examples: 1920
  - stop_the_line_failures: 0
  - wrote: /Users/soheilkhodadadi/DataWork/ai-washing/reports/referee/patent_construct_audit.csv
  - wrote: /Users/soheilkhodadadi/DataWork/ai-washing/reports/referee/patent_construct_red_flags.csv
  - wrote: /Users/soheilkhodadadi/DataWork/ai-washing/reports/referee/patent_construct_summary.md`
- `journal_reproducibility`: exit `0`
  `AI Washing journal reproducibility audit
  - checks: 21
  - stop_the_line_failures: 0
  - wrote: /Users/soheilkhodadadi/DataWork/ai-washing/reports/referee/journal_reproducibility_audit.csv
  - wrote: /Users/soheilkhodadadi/DataWork/ai-washing/reports/referee/journal_reproducibility_audit.md`

## Generated Evidence

- `reports/referee/package_surface_audit.md`
- `reports/referee/data_sanity_summary.md`
- `reports/referee/textual_construct_summary.md`
- `reports/referee/patent_construct_summary.md`
- `reports/referee/journal_reproducibility_audit.md`

## Referee Lens Summary

- Package hygiene: coauthor-facing notes are useful for Thomas/Kuntara but should be excluded from a future journal archive profile.
- Data integrity: row counts, lane coverage, duplicate keys, impossible values, and private-data availability are now checked mechanically.
- Textual construct validity: short-acronym AI/ML hits are quantified and sampled rather than hidden.
- Patent construct validity: short-acronym-only keyword evidence and potential ML-as-unit contexts are quantified and sampled.
- Reproducibility: the environment, package dependencies, table/figure statuses, C7 format delta, and Git hygiene are checked from one command.
