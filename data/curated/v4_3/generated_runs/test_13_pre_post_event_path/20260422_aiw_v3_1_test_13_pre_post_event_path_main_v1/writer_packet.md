# Writer Packet: test_13_pre_post_event_path

## Purpose
- This run tests whether the mismatch return gap opens after the filing or is already visible in the year before the filing month.
- Because the daily event-return file begins only at trading day -2, this diagnostic is built from monthly CRSP event time instead of the daily file.

## Sample Definition
- Event panel: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet`
- Monthly firm returns: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/interim/market/wrds_crsp_msf_full_sample_v1.parquet`
- Monthly market index: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/interim/market/wrds_crsp_msi_full_sample_v1.parquet`
- Unit of observation: `AI-talking annual filing event × event month`
- Balanced window: `-12` to `+12` months around the filing month

## Sample Counts
- AI-filing events before balancing: `7355`
- Balanced filing events: `4222`
- Balanced unique firms: `1544`

## Key Diagnostics
- Cumulative BHAR diff at month -1: `-2.220` pct
- Cumulative BHAR diff at month +3: `-4.076` pct
- Cumulative BHAR diff at month +12: `3.846` pct
- Pre window BHAR[-12,-2] diff p-value: `0.947`
- Early post window BHAR[+1,+3] diff p-value: `0.288`
- Post window BHAR[+1,+12] diff p-value: `0.199`

## Caption Draft
This figure and table trace the event-time return path around the AI-related annual filing using monthly CRSP returns. The sample is restricted to filings with complete return coverage from month -12 to month +12 around the filing month. The key diagnostic is whether the mismatch-minus-non-mismatch gap is already open in the pre-filing window or instead appears mainly in the first few months after the filing month.
