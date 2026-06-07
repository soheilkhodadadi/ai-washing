# Writer Packet

## Metadata
- Test id: `test_05_size_heterogeneity`
- Run id: `20260411_hybrid_api_a_conf49_main_v1`
- Date run: `2026-04-11`
- Script/module path: `semantic_ai_washing.analysis.publication_runs.test_05_size_heterogeneity`
- Input files: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet`, `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`, `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/interim/market/wrds_crsp_msf_full_sample_v1.parquet`
- Unit of observation: `annual AI filing event`

## Size Design
- Breakpoint method: `monthly active-sample median lagged market cap from CRSP MSF`
- Filings with size assignment: `7262`
- Small-firm filings: `3655`
- Big-firm filings: `3607`

## Outcomes
- Short-run outcome: `CAR[-1,+1]`
- Drift outcome: `BHAR[+2,+63]`
- Main specification: `small subsample, big subsample, and pooled interaction with PatentMismatch × Small`

## Results
- CAR pooled interaction differential: `PatentMismatch × Small = 0.0033` with p = `0.575`
- BHAR pooled interaction differential: `PatentMismatch × Small = 0.0171` with p = `0.369`
- Implied small-firm mismatch effect in BHAR: `0.0122` with p = `0.518`

## Caption Draft
This table reports heterogeneity by firm size for the filing-date and post-filing mismatch effects. Small firms are defined using the monthly active-sample median lagged market capitalization from CRSP MSF because NYSE breakpoints are not available in the local extract. For each outcome, the first two columns re-estimate the baseline regression separately in the small-firm and big-firm subsamples. The third column estimates a pooled interaction regression with PatentMismatch, Small, and PatentMismatch × Small, alongside the same disclosure controls, industry fixed effects, filing-year fixed effects, and firm-clustered standard errors.
