# Writer Packet: test_12_predictive_return_controls

## Purpose
- This run asks whether the post-filing return pattern survives richer observable controls instead of being subsumed by simple firm characteristics.
- It is the direct follow-up to the factor-adjusted alpha and horse-race results.

## Sample Definition
- Event panel: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet`
- Annual panel: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`
- Unit of observation: `AI-talking annual filing event`
- Outcomes: `BHAR[+2,+63]` and `BHAR[+2,+252]`
- Fixed effects: `SIC2` and `filing-year`
- Inference: `clustered by gvkey`

## Control Ladder
- Core: `ln_assets`, `leverage`, `cash`, `roa`
- Operating: `rd_intensity`, `capx_at`, `sales_growth`
- Market characteristics: `ln_mktcap_year_end`, `annual_ret`, `annual_bhar_vw`, `ln_vol`, `firm_age_market`
- Patent history: `log_patents_ai_lag1`

## Sample Counts
- AI-filing rows: `7355`
- Unique firms: `2753`

## Most Important Coefficient
- Full-controls BHAR[+2,+63] PatentMismatch coefficient: `0.0065` with p=`0.577`

## Caption Draft
This table tests whether the post-filing return pattern is subsumed by observable firm characteristics. The dependent variables are BHAR[+2,+63] in Panel A and BHAR[+2,+252] in Panel B. Each column adds progressively richer controls: core balance-sheet controls, operating controls, market characteristics, and prior AI patent history. All specifications include PatentMismatch, the A/S ratio, AI Focus, SIC2 fixed effects, filing-year fixed effects, and standard errors clustered by gvkey.
