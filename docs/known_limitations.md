# Known Limitations

- v4.3 is the current frozen computational target. Kuntara's v5.0 edits are editorial and are not treated as code-reproduction targets unless a later release explicitly promotes them.
- Private, licensed, large, and machine-local data are not tracked in Git. Use an external `AIW_DATA_ROOT`, such as `/Users/soheilkhodadadi/DataWork/ai-washing-private-data` on Soheil's machine.
- v4.3 has lane-specific data coverage. The annual NLP/patent panel covers 2016-2025, while event/market-return tables use 2016-2024 because the staged CRSP return extracts stop at 2024-12-31. This is a reproduction boundary, not an older-file mistake.
- Filing-spine and filing AI-measure files cover 2016-2025, but they are disclosure lineage/bridge inputs and are not a completed 2025 return-event panel.
- Selected numerical reruns pass for `T00`, `T16`, `T17`, `T09`, and `T30`: fresh CSV outputs exactly match frozen v4.3 generated CSV evidence.
- Many v4.3 manuscript table inputs add manuscript-facing captions, notes, resizing, or table wrappers around generated numeric content. These remain marked as `content_delta` until manuscript-level wrapper deltas are separately normalized.
- Several appendix tables were generated as CSV/MD/DOCX artifacts rather than paper-ready TeX exports. Their lineage is preserved through run directories and generated CSV files.
- Figure regeneration is not guaranteed in the current phase. v4.3 figure PDFs are frozen as manuscript assets; generated candidates are recorded as provenance evidence.
- Test 25 now uses a staged private ExecuComp cache for normal reproduction. WRDS refresh remains local-only and explicit; credentials are not shared or committed.
- Full raw SEC corpus files are not bundled in the current data room. Representative SEC full-submission samples, representative 2025 Stage-One cleaned filings, source links/documentation, extracted AI sentences, and final hybrid classifier outputs are staged for auditability. `make validate-sec-source` is the gate for this policy.
- No DVC or heavy cloud artifact versioning is introduced yet. Checksums, manifests, Git, and a separate private data root are used until the artifact surface stabilizes.
- Docker validation passed with both no-private-data and read-only private-data mounts. Devcontainer interactive use is scaffolded but has not been separately rehearsed on a coauthor machine.
- `test_05_size_heterogeneity.py` emits a pandas `.fillna` downcasting `FutureWarning`; this is not a v4.3 reproduction blocker, but it should be cleaned in a maintenance pass.
