# Test 25 ExecuComp Policy

Test 25 links lagged CEO incentive structure to low-credibility AI disclosure. Earlier versions pulled ExecuComp directly from WRDS inside the table script. The coauthor workstation now treats ExecuComp as a staged private input.

## Default Reproduction Path

Normal reruns use:

```bash
$AIW_DATA_ROOT/external/execucomp/execucomp_ceo_anncomp_2015_2024.parquet
```

The publication runner passes this path as `--execucomp-cache`. No WRDS credentials are needed for normal v4.3 reproduction.

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make TABLE_ID=T25 reproduce-table
```

## Refresh Path

A refresh from WRDS is explicit and local-only:

```bash
python -m semantic_ai_washing.analysis.publication_runs.test_25_exec_incentive_mismatch \
  --annual-panel "$AIW_DATA_ROOT/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet" \
  --execucomp-cache "$AIW_DATA_ROOT/external/execucomp/execucomp_ceo_anncomp_2015_2024.parquet" \
  --refresh-execucomp-from-wrds \
  --dotenv-path .env
```

The `.env` file is local and ignored by Git. Do not share credentials through GitHub, email, or the data room. Coauthors with their own WRDS access can refresh independently.

## Current Cache Provenance

The staged cache was copied from the frozen v4.3 Test 25 generated-run evidence. Its SHA-256 is:

```text
4939509c2ad3af31a68fcf0e478a0bc69d6c935a04cec5d22413baa10d22e1df
```

The cache includes the CEO row retained for each gvkey-year after the highest-TDC1 co-CEO rule, plus the compensation variables used by Test 25.
