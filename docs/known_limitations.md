# Known Limitations

- v4.3 is the current frozen computational target. Kuntara's v5.0 edits are editorial and are not treated as code-reproduction targets unless a later release explicitly promotes them.
- Private, licensed, large, and machine-local data are not tracked in Git. Use an external `AIW_DATA_ROOT`, such as `/Users/soheilkhodadadi/DataWork/ai-washing-private-data` on Soheil's machine.
- Selected numerical reruns pass for `T00`, `T16`, `T17`, `T09`, and `T30`: fresh CSV outputs exactly match frozen v4.3 generated CSV evidence.
- Many v4.3 manuscript table inputs add manuscript-facing captions, notes, resizing, or table wrappers around generated numeric content. These remain marked as `content_delta` until manuscript-level wrapper deltas are separately normalized.
- Several appendix tables were generated as CSV/MD/DOCX artifacts rather than paper-ready TeX exports. Their lineage is preserved through run directories and generated CSV files.
- Figure regeneration is not guaranteed in the current phase. v4.3 figure PDFs are frozen as manuscript assets; generated candidates are recorded as provenance evidence.
- Test 25 depends on private executive-compensation/database-backed logic. The future-extension placeholder `data/external/execucomp_or_private_db` is not staged.
- No DVC or heavy cloud artifact versioning is introduced yet. Checksums, manifests, Git, and a separate private data root are used until the artifact surface stabilizes.
- Docker/devcontainer support remains deferred until after full-table expansion clarifies the stable runtime surface.
