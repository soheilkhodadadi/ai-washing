# Washing-Pays Proxy First Pass

This extension lane packages the current v4.3 capital-raising timing test as an operational first screen. It uses the existing Test 30 logic: a firm is treated as entering a large capital-raising window when next-year CRSP share outstanding growth exceeds 5 percent.

## What It Answers

The proxy test asks whether low-credibility AI disclosure is concentrated before large next-year share-growth windows. It is useful as a quick screen for whether the paper's disclosure construct is connected to financing timing.

## What It Does Not Answer

This is not a full SEO or offering-terms test. It does not measure proceeds, offer discounts, underwriting terms, issuance costs, completion status, or valuation effects around actual offering events. Those require a separate offering-level dataset.

## Run Command

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make extension-washing-pays-proxy
```

The command reruns the existing Test 30 publication script, refreshes the `T30` table workbench bundle, and writes a proxy extension bundle under `outputs/extensions/washing_pays_proxy/`.

## Key Files

- Owning script: `semantic_ai_washing.analysis.publication_runs.test_30_capital_raising_timing`
- Paper table: `T30`, Main Table 7
- Workbench export: `outputs/workbench/T30/`
- Extension output folder: `outputs/extensions/washing_pays_proxy/`
- Future data template: `templates/seo_offering_terms_schema.csv`

## Safe Next Step

If coauthors want the stronger washing-pays test, stage an offering-level dataset following `templates/seo_offering_terms_schema.csv`, then add a new extension script rather than replacing the v4.3 Test 30 proxy. Keep the proxy result as the baseline screen until the stronger data are validated.
