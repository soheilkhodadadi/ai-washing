# Writer Packet: Test 30 capital-raising timing and disclosure opportunism

## Setup

- Event year 0 is the disclosure year before a large equity-issuance window.
- Issuance rule: Issue>5% uses next-year CRSP shrout growth above 5%.
- Sample keeps each firm's first such issue year and focuses on active AI issuers that continue discussing AI in year 0 and year +1.

## Density

- First issue-event firms: `2,105`.
- Active AI issue-event firms: `367` across `1,775` event-window rows.
- Non-big active issue-event firms: `251` across `1,220` rows.

## Main read

- All active AI issuers: `PatentMismatch` rises into the issuance window by `0.1787` (p=`0.000`) and then falls by `-0.0926` (p=`0.000`) in the following year.
- `LowCredibility` shows the same rise-then-partial-unwind pattern: `0.2334` into the event year and `-0.1063` afterward.
- `AI_Focus` keeps rising through and after issuance: `1.0051` into year 0 and `0.3962` afterward.
- Non-big issuers retain the credibility-timing pattern: `PatentMismatch` `0.1708` into year 0 and `-0.0797` after issuance.

## Interpretation

- Best reading: capital-raising windows line up with a temporary deterioration in disclosure credibility rather than a simple disappearance of AI talk.
- The rise in `AI_Focus` means the pattern is more consistent with amplified AI promotion around financing than with post-issue silence.
- Because the credibility measures partly unwind after the issue year, the financing-opportunism interpretation is stronger than the earlier broad financing-outcome regressions.

## Placement

- Best use: high appendix or supporting main-text incentive/financing extension if we want one explicit opportunism result tied to capital markets.
