# Writer Packet: test_15_matched_ai_talking_sample

## Purpose
- This run asks whether mismatch filings still differ from non-mismatch filings after comparing them to observationally similar AI-talking peers.
- The matching layer is intended to address the obvious cross-sectional-composition critique more directly than the raw portfolio sorts.

## Matching Design
- Exact match dimensions: `filing_year`, `sic2`
- Nearest-neighbor dimensions: `log(Market Cap, t-1)`, `annual BHAR, t-1`, `annual return, t-1`, `ln(Assets)`, `leverage`, `cash`, `ROA`
- Matching: one-to-one without replacement
- Standardized-distance caliper: `1.50`

## Sample Counts
- AI-filing rows available for matching: `6861`
- Unique firms: `2604`
- Matched pairs: `1297`

## Balance
- Median match distance: `0.857`
- Max absolute matched SMD: `0.025`

## Main Read
- Matched CAR[-1,+1] difference: `0.101` pct (p=`0.812`)

## Caption Draft
This table and figure compare mismatch filings to matched non-mismatch AI-talking filings. Matches are exact on filing year and industry and nearest on lagged size, lagged return history, and core balance-sheet characteristics, subject to a standardized-distance caliper. If the filing-date CAR difference does not survive in the tightened matched sample, the market-results block should not be presented as robust to richer observable balancing.
