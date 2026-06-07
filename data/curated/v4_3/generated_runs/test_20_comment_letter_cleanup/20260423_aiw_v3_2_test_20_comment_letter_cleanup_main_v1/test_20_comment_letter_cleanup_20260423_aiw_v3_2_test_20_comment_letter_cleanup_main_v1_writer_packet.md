# Writer Packet: Test 20 disclosure cleanup after SEC scrutiny

## What this run does

- Anchors on each firm's first SEC comment-letter year from Test 19.
- Restricts the main sample to active AI disclosers: firms that talk about AI both at `t-1` and `t+1`.
- Measures within-firm paired changes in disclosure composition relative to `t-1`.

## Why this design matters

- It avoids a mechanical entry/exit story where disclosure falls just because the firm stops mentioning AI entirely.
- It is a direct oversight-discipline test: after scrutiny, do continuing AI disclosers become more credible?

## Sample

- Any-comment active sample: `70` firms and `330` event-window rows.
- AI-related comment active sample: `11` firms and `52` rows.

## Headline read

- In the main any-comment sample, `A/S` rises by `+0.1796` at `t+1` (p=`0.007`).
- `SpecShare` falls by `-0.1051` at `t+2` (p=`0.025`).
- `PatentMismatch` declines by `-0.1143` at `t+1` (p=`0.073`).
- `AI_Focus` rises after scrutiny, so the pattern is not silence; it is more compatible with continuing AI talk alongside cleaner composition.

## Interpretation discipline

- This is a within-firm dynamic response, not a causal claim about why the SEC chose to comment.
- The AI-related comment subset is still useful, but it remains a pilot because the event count is small.