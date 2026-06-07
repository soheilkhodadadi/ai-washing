# Match Status Report

`content_delta` does not automatically mean the generated numbers differ. In this capsule it often means the v4.3 manuscript table added a publication note, `resizebox`, panel header, or other paper-facing wrapper around generated values. Use `make compare-tables` for normalized similarity scores and inspect CSV/run artifacts for numeric provenance.

Match status categories:

- `exact_match`: generated TeX exactly equals the v4.3 table input.
- `format_only_delta`: wrappers/captions differ after normalization, but the normalized table body matches.
- `content_delta`: generated candidate and v4.3 table are related but not identical; inspect before rerun/replacement.
- `unknown`: candidate missing or comparison could not be performed.
