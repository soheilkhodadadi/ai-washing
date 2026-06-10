# Patent Matching Validation

Generated: 2026-06-10

## Purpose

This note records the validation surface for the patent matching lane. It is meant to answer a practical coauthor question: can I see how the patent mismatch variable was built, and can I inspect enough examples to trust the direction of the construct?

## Validation Artifacts

The private data room stages the following patent validation artifacts under `$AIW_DATA_ROOT`:

| Artifact | Logical path | Role |
| --- | --- | --- |
| Grant counts | `data/processed/patents/ai_patent_counts_filtered_ever_speaker_2016_2025_hybrid_grant_2014plus.csv` | Annual grant-side patent and AI-patent counts. |
| Pregrant counts | `data/processed/patents/ai_application_counts_filtered_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv` | Annual pregrant application and AI-application counts. |
| Grant examples | `data/processed/patents/ai_patent_examples_ever_speaker_2016_2025_hybrid_grant_2014plus.csv` | Matched AI grant examples with title, abstract, and keywords. |
| Pregrant examples | `data/processed/patents/ai_application_examples_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv` | Matched AI pregrant examples with title, abstract, and keywords. |
| Grant diagnostics | `data/processed/patents/patents_diagnostics_ever_speaker_2016_2025_hybrid_grant_2014plus.csv` | Firm-level grant matching diagnostics. |
| Pregrant diagnostics | `data/processed/patents/application_diagnostics_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv` | Firm-level pregrant matching diagnostics. |
| Lookup and aliases | `data/metadata/company_identity/` | Hybrid identity layer used to build normalized matching terms. |
| Patent keywords | `data/metadata/patents/` | Baseline and sensitivity keyword lists. |
| Robustness/fuzzy notes | `data/reports/patents/` | Method reports, progress logs, and rejected fuzzy sensitivity evidence. |

## Current Row-Count Gates

`make validate-patent-data` enforces the current staged row-count and schema gates:

- Grant counts: 11,386 rows, 2014-2025.
- Pregrant counts: 12,051 rows, 2014-2025.
- Grant examples: 1,403 rows, 2014-2025.
- Pregrant examples: 1,920 rows, 2014-2025.
- Grant diagnostics: 1,754 firm rows.
- Pregrant diagnostics: 1,881 firm rows.
- Hybrid lookup: 4,907 rows.
- Hybrid aliases: 4,823 rows.
- Fuzzy sensitivity examples: 120 rows.
- Coauthor patent audit examples: 40 rows once `make patent-example-audit` has been run.

## Example Audit Procedure

Run:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make patent-example-audit
make validate-patent-data
```

Then open:

```text
$AIW_DATA_ROOT/reports/patents/patent_audit_examples.csv
```

The file is deliberately small and readable. It includes 20 grant examples and 20 pregrant examples selected deterministically across the staged files. Each row includes CIK, firm name, patent/application identifiers, year, title, abstract, matched keywords, source lane, a `keyword_review_flag`, and an audit note.

The `keyword_review_flag` is especially important for short acronym hits. Exact `AI`/`ML`-only hits are flagged as `short_acronym_only`; rows where those acronyms appear alongside stronger phrases are flagged as `contains_short_acronym`. These flags preserve the v4.3 evidence while making likely keyword-ambiguity cases easy to inspect.

## What To Check Manually

A coauthor reviewing the audit file should check three things:

1. Firm match: does the patent/application plausibly belong to the listed firm or its normalized assignee/applicant identity?
2. Keyword hit: does the matched keyword refer to AI or ML in a substantive technical sense rather than a generic phrase?
3. Lane interpretation: is the row a grant-side patent or a pregrant application, and is the timing caveat relevant?

If a row looks questionable, inspect the full staged example files and the lookup/alias records for that CIK. The audit file is a sample, not the only evidence.

## Known Weaknesses

- Exact normalized matching can miss firms when PatentsView organization names differ substantially from WRDS/SEC names and no curated alias exists.
- Generic or short company names are safer to exclude than force-match, but this lowers recall.
- Pregrant application counts are affected by publication lag in late years, especially 2025.
- The patent keyword dictionary is intentionally compact. It avoids broad technology terms that could raise recall but weaken construct validity.
- Short acronym-only hits for `AI` and especially `ML` need manual attention because they can capture non-AI patent language such as measurement units. The audit file flags these rows rather than suppressing them.

## Why This Is Still The Right Baseline

The current design is conservative, auditable, and stable. The alternative fuzzy supplement produced implausibly large match increases and obvious false positives. For a paper where the patent mismatch variable is central, this exact-normalized hybrid method is a defensible baseline and a better starting point for coauthor extensions.
