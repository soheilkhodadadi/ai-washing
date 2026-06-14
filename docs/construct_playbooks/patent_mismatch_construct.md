# PatentMismatch Construct

## Purpose

PatentMismatch captures firm-years with meaningful AI disclosure but weak observable AI patent or application support. It is the central credibility construct in v4.3.

## Source Artifacts

- Canonical annual panel: `data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`
- Patent counts and examples: `data/processed/patents/`
- Patent keywords and identity metadata: `data/metadata/patents/` and `data/metadata/company_identity/`
- Patent method notes: `docs/patent_mismatch_method_note.md`, `docs/patent_matching_validation.md`, and `docs/patent_fuzzy_sensitivity_note.md`

## v4.3 Definitions

The v4.3 construct combines AI disclosure intensity/composition with patent and application support. The exact columns are read from the canonical annual panel and publication scripts. Use `T16` to compare construct variants before changing the retained definition.

## Owning Scripts And Tables

- Disclosure-volume figure: `legacy_r1_disclosure_volume` (`F1`)
- Construct screen: `test_16_construct_variant_screen` (`T16`)
- Real outcomes: `test_17_real_outcome_dynamics` (`T17`)
- Timing and determinants: `B1`-`B4`, `C1`-`C3`

## Validation Checks

- `make validate-patent-data`
- `make patent-example-audit`
- `make patent-construct-audit`
- `make TABLE_ID=T16 reproduce-table`

## Known Limitations

Patent keyword matching can produce false positives when a phrase is technically adjacent to AI but not evidence of AI capability. It can also miss proprietary or trade-secret AI work that never appears in patents. v4.3 documents this as a construct-validity limitation rather than hiding it.

## Safe Update Path

1. Review grant and pregrant examples before changing any patent keyword or matching rule.
2. Run fuzzy/keyword sensitivity checks in a separate output.
3. Rebuild patent counts and diagnostics under a versioned path.
4. Rebuild the annual panel only after row counts and examples are reconciled.

## Likely Coauthor Or Referee Questions

- Are patent examples truly AI-related, or keyword artifacts?
- Does company-name matching miss subsidiaries or create false matches?
- Do results survive grant-only, pregrant, stricter keyword, or high-precision patent definitions?
