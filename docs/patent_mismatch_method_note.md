# Patent Mismatch Method Note

Generated: 2026-06-10

## Purpose

This note explains how the AI Washing project builds the patent side of the disclosure/patent mismatch construct. It is written for coauthor audit, not as a manuscript paragraph. The goal is to make the matching design inspectable before anyone extends the paper or sends the package to a referee.

## Construct Overview

The patent lane measures whether firms have observable AI-related invention activity that is stronger than, weaker than, or inconsistent with their AI disclosure language. The v4.3 workstation keeps two patent source lanes:

- Grant lane: granted PatentsView patents assigned to firms in the ever-speaker universe.
- Pregrant lane: published patent applications, matched first through pregrant assignees and then through applicant names when assignee matching misses obvious firm records.

The annual NLP/patent panel covers 2016-2025. Upstream grant and pregrant count files start in 2014 so lagged patent/application measures can be used without mechanically dropping early panel years.

## Firm Universe

The firm universe is the refreshed ever-speaker filing universe used in v4.3. The staged lookup and alias files are:

- `data/metadata/company_identity/company_lookup_ever_speaker_2016_2025_hybrid_v1.csv`
- `data/metadata/company_identity/company_aliases_ever_speaker_2016_2025_hybrid_v1.csv`

The lookup has 4,907 rows. The alias file has 4,823 rows. Together they provide a hybrid identity layer built from WRDS identities, SEC filing/header names, ticker/name metadata, and prior validated aliases. This is intentionally broader than a bare CIK-name list because patent assignee names often differ from Compustat/SEC issuer names.

## Name Normalization

The canonical normalizer lives in `src/semantic_ai_washing/patents/keyword_matching.py`. It lowercases text, removes punctuation, tokenizes the organization name, and strips trailing legal suffixes such as `inc`, `corp`, `corporation`, `co`, `company`, `ltd`, `llc`, `plc`, `ag`, `nv`, `sa`, `gmbh`, `holding`, and `holdings`.

Examples:

- `Snowflake Inc.` becomes `snowflake`.
- `QUALCOMM Incorporated` becomes `qualcomm`.
- `International Business Machines Corp.` becomes `international business machines`.

This is exact normalized matching, not fuzzy matching.

## Exact Normalized Matching

The live patent lane builds a normalized term index from firm names and aliases. A normalized term is retained only if it maps to exactly one CIK. Terms shared by multiple CIKs are excluded rather than assigned by guesswork.

This conservative design trades some recall for a lower false-positive risk. That is appropriate here because the mismatch construct is central to the paper. A small number of false positives can be more damaging than modest undercoverage.

## Grant Matching

The grant-side extractor is `src/semantic_ai_washing/patents/extract_filtered_patents_lightweight.py`.

It uses PatentsView grant files:

- `g_assignee_disambiguated.tsv`
- `g_patent.tsv`
- `g_patent_abstract.tsv`
- `g_application.tsv` when application timing is requested

The extractor matches disambiguated assignee organization names to the unique normalized firm-term index. It then filters to patents with usable timing and searches titles plus abstracts for AI-related patent keywords.

Staged grant outputs:

- `data/processed/patents/ai_patent_counts_filtered_ever_speaker_2016_2025_hybrid_grant_2014plus.csv`
- `data/processed/patents/ai_patent_examples_ever_speaker_2016_2025_hybrid_grant_2014plus.csv`
- `data/processed/patents/patents_diagnostics_ever_speaker_2016_2025_hybrid_grant_2014plus.csv`

The staged grant count file has 11,386 firm-year rows over 2014-2025. The staged grant example file has 1,403 AI-related matched patent examples.

## Pregrant Matching

The pregrant-side extractor is `src/semantic_ai_washing/patents/extract_filtered_pregrant_applications_lightweight.py`.

It uses PatentsView pregrant files:

- `pg_published_application.tsv`
- `pg_published_application_abstract.tsv`
- `pg_assignee_disambiguated.tsv`
- `pg_applicant_not_disambiguated.tsv`
- `pg_granted_pgpubs_crosswalk.tsv`

The pregrant lane first matches disambiguated assignee names. It then uses applicant names as a fallback for publication identifiers not already matched through assignees. Matched records are deduplicated at the `(CIK, application_id)` level, with current publication identifiers and later publication dates preferred when duplicate publication rows exist.

The applicant fallback is not cosmetic. The robustness note shows that assignee-only matching materially undercounted pregrant applications. For 2024, assignee-only matching found 6,432 total applications and 447 AI applications; assignee plus applicant fallback found 27,597 total applications and 1,850 AI applications.

Staged pregrant outputs:

- `data/processed/patents/ai_application_counts_filtered_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv`
- `data/processed/patents/ai_application_examples_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv`
- `data/processed/patents/application_diagnostics_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv`

The staged pregrant count file has 12,051 firm-year rows over 2014-2025. The staged pregrant example file has 1,920 AI-related matched application examples.

## AI Patent Keyword List

The baseline patent keyword list is staged at `data/metadata/patents/patent_keywords.txt`. It contains the final compact dictionary used by the grant and pregrant extractors, including phrases such as artificial intelligence, machine learning, deep learning, neural network, natural language processing, computer vision, reinforcement learning, language model, large language model, and generative AI.

The matching helper compiles a boundary-aware regex and treats multiword phrases flexibly, so `machine learning` can also match hyphenated text such as `machine-learning`. The staged sensitivity dictionaries under `data/metadata/patents/` are retained for audit and future robustness work; they are not automatic replacements for the baseline keyword file.

Important caveat: the baseline list includes short acronyms `AI` and `ML`. The exact boundary pattern prevents substring matches inside longer words, but it cannot by itself distinguish machine-learning `ML` from non-AI uses such as milliliter units in pharmaceutical patents. In the staged AI example files, exact `AI`/`ML`-only hits account for 86 of 1,403 grant examples and 130 of 1,920 pregrant examples. The generated audit file therefore includes a `keyword_review_flag` column so these cases are not hidden from coauthor review. This is a candidate refinement for a future patent-keyword robustness pass, not a silent v4.3 change.

## Why Fuzzy Matching Was Rejected

A bounded 2024 fuzzy-matching sensitivity run was tested at thresholds 0.90 and 0.95. The result was not credible as a robustness lane. At threshold 0.95, grant matches increased from 40,931 to 76,063, and pregrant matches increased from 27,595 to 51,557. Manual examples showed false positives driven by generic terms such as `city`, `one`, `view`, and `discovery`.

The current v4.3 patent lane therefore uses exact normalized matching plus curated alias expansion. Fuzzy matching remains documented as a rejected stress test, not as part of the live construct.

## Publication-Lag Caveat

Pregrant application counts decline sharply in the latest years, especially 2025. The post-fallback pattern is more consistent with publication lag than a matching collapse, but late pregrant years should still be interpreted cautiously. Grant timing is the safer full-span backbone; pregrant timing is useful but should be read with this lag caveat.

## Coauthor Audit Surface

Run:

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make patent-example-audit
AIW_DATA_ROOT=/path/to/ai-washing-private-data make validate-patent-data
```

The audit builder writes `data/reports/patents/patent_audit_examples.csv` under `$AIW_DATA_ROOT`. It contains a balanced sample of 40 actual matched grant/pregrant records with firm identifiers, patent/application identifiers, titles, abstracts, matched keywords, source lane, and notes.
