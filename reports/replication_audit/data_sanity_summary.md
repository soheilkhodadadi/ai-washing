# Data Sanity Audit

## Severity Counts

- `info`: 2
- `manageable`: 1
- `material_needs_review`: 2
- `ok`: 66

## Non-OK Findings

- `event_panel` / `negative_sales_observations`: manageable observed `4` expected `0 preferred`. Compustat sales can be anomalous; report rather than silently drop.
- `daily_event_returns` / `negative_crsp_price_sign_convention`: info observed `7078` expected `allowed`. CRSP negative price can indicate bid/ask average sign convention.
- `crsp_monthly` / `negative_crsp_price_sign_convention`: info observed `2917` expected `allowed`. CRSP negative price can indicate bid/ask average sign convention.
- `execucomp_ceo` / `nonnegative_bonus`: material_needs_review observed `1` expected `0`. 
- `execucomp_ceo` / `nonnegative_ownership_pct`: material_needs_review observed `1` expected `0`. 
