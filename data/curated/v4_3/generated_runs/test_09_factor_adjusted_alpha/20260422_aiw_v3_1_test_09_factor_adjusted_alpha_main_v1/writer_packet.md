# Writer Packet: test_09_factor_adjusted_alpha

## Identification Role
- This run strengthens the earlier calendar-time portfolio result by replacing the market-only benchmark with standard factor models.
- The output is designed to answer whether the long-short spread survives CAPM, FF3, FF5, and FF5+Momentum benchmarking.

## Sample Definition
- Event panel: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet`
- Annual panel: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`
- Monthly returns: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/interim/market/wrds_crsp_msf_full_sample_v1.parquet`
- Market index: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/interim/market/wrds_crsp_msi_full_sample_v1.parquet`
- Size subset: `all`
- Unit of observation: `calendar-month long-short portfolio return`
- Signal rule: `AI-talking annual filers with PatentMismatch label; one active signal per stock-month using the latest filing`

## Factor Inputs
- Official FF5 monthly source: `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip`
- Official monthly momentum source: `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip`
- Factor month range staged locally: `1963-07` to `2026-02`
- Inference: `Newey-West HAC with lag 3`

## Headline Numbers
- EW 3m CAPM alpha: `0.934` pp/month (p=`0.036`)
- EW 3m FF5+Mom alpha: `0.976` pp/month (p=`0.026`)

## Caption Draft
This table reports factor-adjusted calendar-time long-short portfolio returns formed after annual AI-related filing signals. Each month, the long leg holds non-mismatch AI filers and the short leg holds mismatch AI filers that filed within the prior 1, 3, 6, or 12 months. Equal-weight and value-weight portfolios are benchmarked against CAPM, FF3, FF5, and FF5 plus the momentum factor using monthly data from the Ken French Data Library. Alpha is the intercept from time-series regressions estimated with Newey-West standard errors.
