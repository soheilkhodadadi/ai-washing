# Artifact Coverage Policy

This workstation reproduces AI Washing v4.3 with lane-specific data coverage. Do not force every artifact to cover 2016-2025. The correct target is determined by the role the artifact plays in the v4.3 manuscript.

## Canonical Lanes

| Lane | Required coverage | Canonical artifacts | Interpretation |
|---|---:|---|---|
| `annual_nlp_patent` | 2016-2025 | `ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`; hybrid API classifier outputs with 147,879 AI-related sentences | Main annual NLP, patent, disclosure-credibility, and real-outcome analyses. |
| `event_market_return` | 2016-2024 | `filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet`; CRSP-derived daily/monthly return inputs ending 2024-12-31 | v4.3 filing-event and market-return tests. This lane is intentionally 2016-2024 because the staged CRSP/event-return extracts stop at 2024-12-31. |
| `filing_spine_ai_measures` | 2016-2025 | `filing_ai_measures_hybrid_api_a_conf49_v1.csv`; `filing_event_spine_hybrid_api_a_conf49_v1.csv`; `filing_wrds_bridge_hybrid_api_a_conf49_v1.csv` | Disclosure lineage and CRSP-link bridge. These files are not a completed 2025 return-event panel. |
| `market_features` | 2015-2024 source years | `annual_market_features_ever_speaker_2016_2025_hybrid_api_a_conf49_v1.csv`; `wrds_crsp_msf_full_sample_v1.parquet`; `wrds_crsp_msi_full_sample_v1.parquet` | CRSP-derived market inputs used by v4.3. The final source coverage stops at 2024 even where filenames retain the broader project target. |

## Promotion Rule

Before staging or replacing any private artifact, record the candidate in `manifests/artifact_provenance_audit.csv` or a private candidate-audit report with:

- candidate path,
- size,
- modified time,
- row count,
- columns,
- checksum when practical,
- year/date coverage,
- intended role,
- promotion decision.

Promote only artifacts that match the lane target above. If a newer 2025 event-return artifact is found later, treat it as a v5+ extension candidate, not as a silent replacement for the v4.3 event-market lane.

## Current v4.3 Facts

- Annual panel: 50,840 firm-year observations, 2016-2025.
- Final hybrid classifier outputs: 147,879 AI-related sentences, 2016-2025.
- Extracted sentence support: 106,977 rows from 2016-2024 plus 40,902 rows from the 2025 refresh, matching 147,879 total rows.
- Filing-event estimation sample: 7,355 events, 2016-2024.
- Daily event-return file: filing dates 2016-01-28 through 2024-12-31.
- CRSP monthly and market-index inputs: 2015-01-30 through 2024-12-31.

## Audit Command

Run the provenance/coverage gate after staging or replacing private artifacts:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make audit-artifact-coverage
```

Expected current result: all promoted required artifacts pass lane-specific coverage; excluded/not-promoted candidates remain documented but do not fail the gate.

## Raw SEC Policy

Full raw SEC filings are not required for v4.3 reproduction. The private data room includes representative full-submission samples and Stage-One cleaned samples plus the Notre Dame Stage-One source documentation and source folder link. Coauthors can independently download the full source corpus if they want a bottom-up rebuild beyond the v4.3 reproduction surface.
