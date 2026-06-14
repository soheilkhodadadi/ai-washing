# SEC Scrutiny And Enforcement Timing

## Purpose

This layer tests whether regulatory scrutiny or SEC AI-washing salience is followed by disclosure cleanup.

## Source Artifacts

- Comment-letter event panel: `data/curated/v4_3/comment_letter_event_panel.parquet`
- Annual NLP/patent panel and SEC enforcement-salience timing fields.
- Source and method notes in `docs/coauthor_data_room.md` and table workbench entries for T20/T29.

## v4.3 Definitions

The comment-letter cleanup test uses a staged event panel. The SEC enforcement-salience design uses annual timing around SEC AI-washing enforcement salience. Both are frozen as v4.3 table scripts until a future release promotes revised event definitions.

## Owning Scripts And Tables

- Comment-letter cleanup: `semantic_ai_washing.analysis.publication_runs.test_20_comment_letter_cleanup` (`T20`)
- SEC enforcement salience: `semantic_ai_washing.analysis.publication_runs.test_29_sec_ai_washing_enforcement_did` (`T29`)

## Validation Checks

- `make TABLE_ID=T20 reproduce-table`
- `make TABLE_ID=T29 reproduce-table`
- `make check-private-data`

## Known Limitations

Regulatory-event definitions can be refined. v4.3 should be treated as a reproducible baseline, while later work may narrow events to AI-specific comment letters or refine salience windows.

## Safe Update Path

1. Add or revise event data in a versioned private-data location.
2. Document treatment timing and sample attrition.
3. Rerun T20/T29 as new candidate outputs.
4. Promote only after pre/post windows and fixed-effects choices are documented.

## Likely Coauthor Or Referee Questions

- Are comment letters directly AI-related or general scrutiny?
- Are treatment and control timing choices defensible?
- Do disclosure cleanup results survive narrower event definitions?
