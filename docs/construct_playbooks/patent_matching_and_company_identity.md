# Patent Matching And Company Identity

## Purpose

This layer links public firms to PatentsView assignees and applicants. It is separate from the patent keyword screen: first identify the firm, then classify patent/application records as AI-related.

## Source Artifacts

- Company lookup: `data/metadata/company_identity/company_lookup_ever_speaker_2016_2025_hybrid_v1.csv`
- Company aliases: `data/metadata/company_identity/company_aliases_ever_speaker_2016_2025_hybrid_v1.csv`
- Patent diagnostics: `data/processed/patents/*diagnostics*.csv`
- Audit examples and sensitivity notes: `data/reports/patents/`

## v4.3 Definitions

The baseline uses exact-normalized hybrid company names and aliases. Broad fuzzy matching is not promoted into the baseline because the sensitivity review produced implausible match expansions and visible false positives.

## Owning Scripts And Tables

- Company lookup builder: `semantic_ai_washing.patents.build_company_lookup`
- Patent extraction and matching helpers: `semantic_ai_washing.patents.*`
- Downstream tables: all PatentMismatch and future patent realization tables.

## Validation Checks

- `make validate-patent-data`
- `make patent-example-audit`
- Review `docs/patent_matching_validation.md` and `docs/patent_fuzzy_sensitivity_note.md`

## Known Limitations

Exact-normalized matching is conservative. It may miss subsidiaries, acquired entities, or patents assigned under legal names not present in the alias file. This is preferable to silently adding fuzzy false positives, but it should be reviewed for high-salience firms.

## Safe Update Path

1. Add candidate aliases in a new alias file or versioned extension.
2. Recompute diagnostics and readable examples.
3. Compare exact baseline, alias-expanded baseline, and fuzzy candidates.
4. Promote only after examples support the change.

## Likely Coauthor Or Referee Questions

- How many firms lose patent matches because of naming conventions?
- Are large AI firms undercounted because of subsidiaries?
- Are fuzzy-only matches plausible when inspected manually?
