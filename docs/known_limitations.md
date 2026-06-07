# Known Limitations

- v4.3 is the computational target. Kuntara's v5.0 edits are not treated as code-reproduction targets.
- Private, licensed, large, and machine-local data are not tracked in Git. The local private data root is `/Users/soheilkhodadadi/DataWork/ai-washing-v43-private-data`.
- Selected numerical reruns now pass for `T00`, `T16`, `T17`, `T09`, and `T30`: fresh CSV outputs exactly match frozen v4.3 generated CSV evidence.
- Many v4.3 manuscript table inputs add manuscript-facing captions, notes, resizing, or table wrappers around generated numeric content. These remain marked as `content_delta` until manuscript-level wrapper deltas are separately normalized.
- Several appendix tables were generated as CSV/MD/DOCX artifacts rather than paper-ready TeX exports. Their lineage is preserved through run directories and generated CSV files.
- Figure regeneration is not guaranteed in Phase 2A-2D. v4.3 figure PDFs are frozen as manuscript assets; generated candidates are recorded as provenance evidence.
- Test 25 depends on private executive-compensation/database-backed logic. The future-extension placeholder `data/external/execucomp_or_private_db` is not staged.
- No DVC or heavy cloud artifact versioning is introduced in this phase. Checksums, manifests, local Git, and a separate private data root are used instead.
- Docker/devcontainer support is intentionally deferred until after full-table expansion clarifies the stable runtime surface.
