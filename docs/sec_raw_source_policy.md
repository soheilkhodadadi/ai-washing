# SEC Raw-Source Policy

Phase 4F makes the SEC source boundary explicit. The coauthor workstation does not mirror the full raw SEC or full Notre Dame Stage-One 10-X corpus by default. It ships a smaller audit surface that is enough for v4.3 reproduction, coauthor inspection, and extraction/classification method review.

## Policy

- Git never tracks raw SEC filings, Stage-One filing corpora, extracted sentence parquet files, classifier outputs, or generated data.
- The private data room includes representative SEC full-submission samples and representative Notre Dame Stage-One cleaned samples.
- The private data room includes extracted AI sentence outputs and final hybrid classifier outputs because these are the practical audit layer used by v4.3 and extension work.
- Source links and documentation point coauthors to the full Stage-One corpus if they want a bottom-up rebuild.
- The full raw SEC corpus should be mirrored only if coauthors specifically ask for it, and only in the private data room, not Git.

## Why This Is Not A Missing-Data Gap

v4.3 table reproduction starts from staged panels, market inputs, patent-match artifacts, extracted sentence support, and final classifier outputs. It does not require raw 10-K text. The raw-text layer is still auditable because the package includes:

- representative full-submission SEC samples;
- representative Stage-One cleaned samples;
- source links for obtaining the full Stage-One 10-X corpus;
- extracted AI sentence parquet outputs for 2016-2024 and the 2025 refresh;
- final April/v4.3 hybrid classifier outputs for 2016-2025;
- classifier validation reports and held-out validation support.

This is the right default tradeoff: enough evidence to audit the method, without forcing a large raw-corpus transfer that is not needed for the current reproduction target.

## Validation Gate

Run from the repository root after setting `AIW_DATA_ROOT`:

```bash
make validate-sec-source
make audit-artifact-coverage
```

`make validate-sec-source` checks `manifests/sec_source_manifest.csv` and confirms that the source/audit surface exists. The current expected anchors are:

- 5 representative full-submission SEC samples;
- 4 representative 2025 Stage-One cleaned samples;
- Notre Dame/SRAF source documentation and Google Drive source links;
- 106,977 extracted AI sentences for 2016-2024;
- 40,902 extracted AI sentences in the 2025 refresh;
- 147,879 final hybrid classified AI sentences for 2016-2025.

## If A Coauthor Wants A Full Raw Rebuild

Use a separate private raw-source mirror, not Git. A safe layout would be:

```text
$AIW_DATA_ROOT/raw/sec_full_corpus/
$AIW_DATA_ROOT/raw/stage_one_10x_full_corpus/
```

Then add a new manifest row and validator only after the mirror is staged. Do not silently promote full-corpus files into the v4.3 reproduction surface.
