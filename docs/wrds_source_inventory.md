# WRDS Source Inventory

This inventory is the coauthor-facing map for staged CRSP, Compustat, and linkage artifacts. It complements `manifests/wrds_data_manifest.csv`, which is the machine-readable validation contract.

## Validation Command

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make validate-wrds-data
```

Expected current result: all 16 manifest rows are present.

## Private Data Tree

| Private folder | Contents | Use |
|---|---|---|
| `$AIW_DATA_ROOT/interim/accounting/` | `wrds_comp_funda_full_sample_v1.parquet` | Compustat fundamentals used to audit and rebuild accounting controls. |
| `$AIW_DATA_ROOT/interim/market/` | CRSP monthly/index files, annual market features, daily filing-event returns, filing AI measures, filing spine, and a copy of the filing WRDS bridge | Market-return, factor, and disclosure-lineage support. |
| `$AIW_DATA_ROOT/interim/linking/` | CIK-GVKEY crosswalk, annual WRDS backbone, filing WRDS bridge | Main CIK-GVKEY-PERMNO linkage audit surface. |
| `$AIW_DATA_ROOT/reports/wrds/` | JSON raw-pull/build reports and unmatched filing bridge tail | Coauthor QA and mismatch diagnostics. |
| `$AIW_DATA_ROOT/docs/wrds/` | Legacy WRDS progress/source-review notes | Context for how the bridge and raw pulls were assembled. |

## Key Files

| Artifact ID | Runtime path under `$AIW_DATA_ROOT` | Required for |
|---|---|---|
| `comp_funda_full_sample` | `interim/accounting/wrds_comp_funda_full_sample_v1.parquet` | Control rebuilds and Compustat audit. |
| `crsp_msf_full_sample` | `interim/market/wrds_crsp_msf_full_sample_v1.parquet` | Annual market features, size tests, and factor/return tests. |
| `crsp_msi_full_sample` | `interim/market/wrds_crsp_msi_full_sample_v1.parquet` | Market-index and factor-adjustment tests. |
| `annual_market_features` | `interim/market/annual_market_features_ever_speaker_2016_2025_hybrid_api_a_conf49_v1.csv` | Annual market features merged to the firm-year panel. |
| `filing_event_returns_daily` | `interim/market/filing_event_returns_daily_hybrid_api_a_conf49_v1.parquet` | Daily event-return cache. |
| `filing_event_estimation_sample` | `processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet` | Canonical v4.3 event sample. |
| `cik_gvkey_refresh_crosswalk` | `interim/linking/cik_gvkey_ever_speaker_2016_2025_refresh_v1.csv` | CIK-GVKEY identity base. |
| `ever_speaker_wrds_backbone` | `interim/linking/ever_speaker_wrds_backbone_2016_2025_hybrid_api_a_conf49_v1.csv` | Annual CIK-GVKEY-PERMNO bridge. |
| `filing_wrds_bridge` | `interim/linking/filing_wrds_bridge_hybrid_api_a_conf49_v1.csv` | Filing-level CIK-GVKEY-PERMNO bridge. |
| `filing_wrds_bridge_unmatched` | `reports/wrds/filing_wrds_bridge_unmatched_hybrid_api_a_conf49_v1.csv` | Unmatched filing-level audit tail. |

## Provenance Modules From The Old Workspace

The canonical repo uses staged extracts for normal reproduction. The old `semantic-patterns` workspace remains provenance for refresh/build code. Relevant modules include:

- `pull_full_sample_wrds_raw.py`
- `build_wrds_gvkey_permno_bridge.py`
- `build_full_sample_wrds_backbone.py`
- `pull_compustat_controls.py`
- `download_crsp.py`
- `download_compustat.py`
- `clean_crsp.py`
- `clean_compustat.py`

These modules are reference material unless a WRDS refresh is explicitly promoted. Do not run refresh logic as part of normal table reproduction.

## What Remains Outside The Current WRDS Closure

The current WRDS closure satisfies the v4.3 reproduction and coauthor audit need for Compustat, CRSP, and bridge intermediates. It does not include actual equity-issuance terms. The strong "washing pays" extension still needs a separate SEO/offering dataset with proceeds, offer price, discount, valuation, and offer timing.
