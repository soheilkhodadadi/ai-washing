# Capital-Raising Proxy

## Purpose

The v4.3 capital-raising result tests whether low-credibility AI disclosure is concentrated before large share-growth windows. It is a proxy screen, not a full SEO/offering-terms analysis.

## Source Artifacts

- Annual NLP/patent panel: `data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`
- CRSP share-outstanding support through market features and CRSP monthly extracts.
- Future strong extension placeholder: `data/external/seo_offering_terms`

## v4.3 Definitions

Test 30 uses next-year CRSP `shrout` growth above 5 percent as a large-equity-issuance proxy. This is reproducible and complete for v4.3, but it is not the same as direct SEO proceeds, offer price, discount, or issuance type.

## Owning Scripts And Tables

- Capital-raising timing: `semantic_ai_washing.analysis.publication_runs.test_30_capital_raising_timing` (`T30`)
- Market reactions in issue windows: `test_32_market_reaction_in_issue_windows` (`C5`)

## Validation Checks

- `make TABLE_ID=T30 reproduce-table`
- `make TABLE_ID=C5 reproduce-table`
- `make validate-wrds-data`

## Known Limitations

Share growth can reflect several financing or capital-structure events. The stronger washing-pays extension needs direct offering terms before making claims about financing cost or offer quality.

## Safe Update Path

1. Add SEO/offering terms under `data/external/seo_offering_terms` in the private data root.
2. Validate proceeds, offer date, offer price, discount, and issue type fields.
3. Build a new extension table rather than overwriting Test 30.
4. Promote only after treatment timing and sample attrition are documented.

## Likely Coauthor Or Referee Questions

- Is `shrout` growth a clean enough proxy for capital raising?
- Do results survive direct SEO data?
- Are effects driven by splits, mergers, or data artifacts?
