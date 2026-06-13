# Known Limitations

- v4.3 is the current frozen computational target. Kuntara's v5.0 edits are editorial and are not treated as code-reproduction targets unless a later release explicitly promotes them.
- Private, licensed, large, and machine-local data are not tracked in Git. Use an external `AIW_DATA_ROOT`, such as `/path/to/ai-washing-private-data` on a local or shared private-data mirror.
- v4.3 has lane-specific data coverage. The annual NLP/patent panel covers 2016-2025, while event/market-return tables use 2016-2024 because the staged CRSP return extracts stop at 2024-12-31. This is a reproduction boundary, not an older-file mistake.
- Filing-spine and filing AI-measure files cover 2016-2025, but they are disclosure lineage/bridge inputs and are not a completed 2025 return-event panel.
- Selected numerical reruns pass for `T00`, `T16`, `T17`, `T09`, and `T30`: fresh CSV outputs exactly match frozen v4.3 generated CSV evidence.
- Many v4.3 manuscript table inputs add manuscript-facing captions, notes, resizing, or table wrappers around generated numeric content. These are separated from generated CSV evidence so numerical reproduction is not confused with manuscript layout.
- Several appendix tables were generated as CSV/MD/DOCX artifacts rather than paper-ready TeX exports. Their lineage is preserved through run directories and generated CSV files.
- Figure regeneration is available as an audit layer. v4.3 figure PDFs remain frozen manuscript assets, while regenerated figure-series CSV evidence and candidate PDFs are recorded in `docs/figure_reproduction_status.md`.
- Test 25 now uses a staged private ExecuComp cache for normal reproduction. WRDS refresh remains local-only and explicit; credentials are not shared or committed.
- Test 30 is reproducible and complete for v4.3. It uses next-year CRSP `shrout` growth above 5 percent as a large-equity-issuance proxy. The deferred future extension is actual SEO/offering terms: proceeds, offer price, discount, valuation base, offering type, and timing.
- Full raw SEC corpus files are not bundled in the current data room. Representative SEC full-submission samples, representative 2025 Stage-One cleaned filings, source links/documentation, extracted AI sentences, and final hybrid classifier outputs are staged for auditability. `make validate-sec-source` is the gate for this policy.
- No DVC or heavy cloud artifact versioning is introduced yet. Checksums, manifests, Git, and a separate private data root are used until the artifact surface stabilizes.
- Docker validation passed with both no-private-data and read-only private-data mounts. Devcontainer interactive use is scaffolded but has not been separately rehearsed on a coauthor machine.
- The previous pandas `.fillna` downcasting warning in `test_05_size_heterogeneity.py` has been removed and is covered by a focused regression test. If it reappears, treat it as an environment-drift or code-regression signal.
