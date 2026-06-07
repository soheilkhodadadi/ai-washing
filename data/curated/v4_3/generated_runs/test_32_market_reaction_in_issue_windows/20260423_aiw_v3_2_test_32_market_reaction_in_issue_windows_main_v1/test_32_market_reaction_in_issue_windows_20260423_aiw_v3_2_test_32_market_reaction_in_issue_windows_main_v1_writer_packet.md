# Writer Packet: Test 32 market reactions in capital-raising windows

## Setup

- Issue-window rule: IssueWindow equals one when next-year CRSP shrout growth exceeds 5%.
- The filing-event sample is collapsed to one firm-year return observation and merged to the annual issue-window flag.
- The key question is whether the return relation for low-credibility AI disclosure changes when financing incentives are salient.

## Density

- Filing-year rows in the merged sample: `4,455` across `1,605` firms.
- Issue-window rows: `1,138` across `709` firms.
- Non-big rows: `2,096`.

## Main read

- In the full sample, baseline `PatentMismatch` predicts weaker `BHAR[+2,+63]`: `-0.0272` (p=`0.004`).
- But the `PatentMismatch × IssueWindow` interaction for `BHAR[+2,+63]` is positive: `0.0716` (p=`0.038`).
- The same interaction is directionally stronger in non-big firms: `0.0918` (p=`0.068`).

## Interpretation

- Best reading: the weak post-filing return pattern attached to mismatch is less negative inside financing windows than outside them.
- That is consistent with financing-salience muting or offsetting the broad negative pricing pattern we saw in the full sample.
- This gives the market section a narrower and more defensible interpretation than the earlier broad portfolio tests.

## Placement

- Best use: supporting market table if we keep a market section, especially alongside Test 30.
