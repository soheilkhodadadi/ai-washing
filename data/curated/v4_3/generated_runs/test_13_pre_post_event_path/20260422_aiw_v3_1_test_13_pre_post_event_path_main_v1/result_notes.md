# Result Notes: test_13_pre_post_event_path

- Balanced event-time sample: `4222` filings across `1544` firms.
- Diff in cumulative BHAR at month `-1`: `-2.220` pct.
- Diff in cumulative BHAR at month `0`: `-2.300` pct.
- Diff in cumulative BHAR at month `+3`: `-4.076` pct.
- Diff in cumulative BHAR at month `+12`: `3.846` pct.
- Pre-filing BHAR[-12,-2] diff: `-0.248` pct (p=`0.947`).
- Early post-filing BHAR[+1,+3] diff: `-1.276` pct (p=`0.288`).
- Post-filing BHAR[+1,+12] diff: `11.927` pct (p=`0.199`).
- Interpretation discipline: if the pre-filing window is flat while the early post-filing window turns negative, that is more consistent with a short-horizon filing-related differentiation than with a deep pre-existing trend. If the gap is already open before month 0, the delayed-correction language should be dropped.
