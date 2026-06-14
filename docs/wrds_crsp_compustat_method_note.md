# WRDS, CRSP, Compustat, And Linkage Method Note

This note explains the market/accounting data lane used in the AI Washing v4.3 workstation. It is written for coauthors who want to inspect the CRSP, Compustat, and linking artifacts behind the final panels without relying on the older `semantic-patterns` workspace.

## What This Lane Does

The WRDS lane provides three kinds of evidence:

1. Compustat accounting fundamentals used to rebuild controls and accounting variables.
2. CRSP monthly/index and daily event-return inputs used in market-return and capital-market tests.
3. CIK-GVKEY-PERMNO bridge artifacts that connect SEC filers to Compustat firms and CRSP securities.

These artifacts are private/licensed or derived from licensed data. They are staged under `$AIW_DATA_ROOT`, not committed to Git.

## Canonical Coverage

The coverage is intentionally lane-specific:

| Lane | Canonical coverage | Why |
|---|---:|---|
| Annual WRDS backbone and filing bridge | 2016-2025 filing spine | Used for disclosure lineage and annual firm-year construction. |
| Compustat fundamentals extract | fiscal years 2014-2025 | Provides lagged/current accounting controls around the 2016-2025 analysis window. |
| CRSP monthly stock and market index extracts | 2015-01-30 to 2024-12-31 | Used for annual market features and factor/return tests. |
| Daily filing-event returns | 2016-01-26 to 2024-12-31 | Used for the v4.3 event-market lane. |
| v4.3 filing-event estimation sample | 2016-2024 filings | The return-event sample stops in 2024 because the staged CRSP return data stop at 2024-12-31. |

A 2016-2025 filing spine is not a 2016-2025 return-event panel. If a future 2025 CRSP/event-return refresh is found or created, treat it as a v5+ candidate until it is explicitly promoted.

## Staged Private Artifacts

Run this from the Git repository after setting `AIW_DATA_ROOT`:

```bash
make validate-wrds-data
```

The validator reads `manifests/wrds_data_manifest.csv` and checks row counts, required columns, date ranges, and year ranges for the staged WRDS artifacts.

The current Phase 4D private data room stages:

| Artifact group | Logical path | Purpose |
|---|---|---|
| Compustat fundamentals | `data/interim/accounting/wrds_comp_funda_full_sample_v1.parquet` | Full-sample accounting pull for controls and auditability. |
| CRSP monthly stock file | `data/interim/market/wrds_crsp_msf_full_sample_v1.parquet` | Monthly returns, prices, shares, and market-cap inputs. |
| CRSP market index | `data/interim/market/wrds_crsp_msi_full_sample_v1.parquet` | Market-index inputs for factor/market adjustment. |
| Annual market features | `data/interim/market/annual_market_features_ever_speaker_2016_2025_hybrid_api_a_conf49_v1.csv` | CRSP-derived annual return and market features merged to firm-years. |
| Daily event returns | `data/interim/market/filing_event_returns_daily_hybrid_api_a_conf49_v1.parquet` | Filing-window daily return cache. |
| Event estimation sample | `data/processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet` | Canonical v4.3 event-market sample. |
| CIK-GVKEY crosswalk | `data/interim/linking/cik_gvkey_ever_speaker_2016_2025_refresh_v1.csv` | Base Compustat identity layer for ever-speaker firms. |
| Annual WRDS backbone | `data/interim/linking/ever_speaker_wrds_backbone_2016_2025_hybrid_api_a_conf49_v1.csv` | Annual CIK-GVKEY-PERMNO bridge for the disclosure spine. |
| Filing WRDS bridge | `data/interim/linking/filing_wrds_bridge_hybrid_api_a_conf49_v1.csv` | Filing-level CIK-GVKEY-PERMNO bridge before return filters. |
| Unmatched bridge tail | `data/reports/wrds/filing_wrds_bridge_unmatched_hybrid_api_a_conf49_v1.csv` | Audit file for filings without a valid CRSP security link. |
| WRDS reports and notes | `data/reports/wrds/`, `data/docs/wrds/` | JSON reports and legacy progress notes used to audit the bridge build. |

## Credential Policy

Do not store or share WRDS credentials in this repository or in the private data room. Normal v4.3 reproduction uses staged private extracts and does not require WRDS access.

If a coauthor wants to refresh WRDS data, they should use their own WRDS credentials through an explicit local refresh path. A refresh should write new candidate artifacts under a separate private output folder, then run `make validate-wrds-data` and `make audit-artifact-coverage` before any artifact is promoted.

## How To Audit The Linkage

Start with these files:

1. `data/interim/linking/cik_gvkey_ever_speaker_2016_2025_refresh_v1.csv` for the issuer-to-Compustat identity layer.
2. `data/interim/linking/ever_speaker_wrds_backbone_2016_2025_hybrid_api_a_conf49_v1.csv` for annual CIK-GVKEY-PERMNO coverage.
3. `data/interim/linking/filing_wrds_bridge_hybrid_api_a_conf49_v1.csv` for filing-level bridge outcomes.
4. `data/reports/wrds/filing_wrds_bridge_unmatched_hybrid_api_a_conf49_v1.csv` for rows not linked to a valid CRSP security.
5. `data/reports/wrds/*.json` for machine-readable source/build reports.

If a market or accounting coefficient changes after a refresh, first compare these bridge artifacts and staged WRDS extracts before editing table scripts.

## Known Boundaries

- The current package does not include actual SEO/offering terms such as proceeds, offer price, discount, or valuation. The current capital-raising test uses a CRSP share-growth proxy and should be described as such.
- The current event-return lane is not extended through 2025.
- WRDS refresh scripts are provenance/reference code, not normal coauthor reproduction commands.
