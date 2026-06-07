# Writer Packet: Test 25 executive incentives and low-credibility AI disclosure

## Setup

- Sample: AI-talking annual panel linked to lagged CEO observations from ExecuComp.
- CEO row rule: use the highest-TDC1 CEO-designated row in each firm-year when multiple CEO rows appear.
- Predictors: lagged CEO equity-award share, lagged CEO ownership pct, lagged log CEO total pay.

## Density

- ExecuComp CEO rows: `19,878` across `2,436` firms.
- Co-CEO firm-years collapsed by highest-TDC1 rule: `3,520`.
- Lagged CEO-linked AI-talking rows: `1,007` across `303` firms.
- Big matched rows: `772`; post-ChatGPT matched rows: `416`.

## Main read

- Post-ChatGPT PatentMismatch on lagged CEO equity-award share: `0.1787**` (p=`0.041`).
- Post-ChatGPT PatentMismatch on lagged CEO ownership pct: `0.0170**` (p=`0.036`).
- Big-firm PatentMismatch on lagged CEO ownership pct: `0.1038***` (p=`0.000`).

## Placement

- Best use: Packet F determinants table, probably main text if the incentive lane remains one of the cleanest explanations for mismatch.
- Suggested framing: stronger equity-oriented CEO incentives and higher CEO ownership are associated with more low-credibility AI disclosure where the incentive channel is most salient, especially in the covered large-firm / post-ChatGPT slice.
