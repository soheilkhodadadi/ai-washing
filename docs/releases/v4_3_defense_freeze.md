# AI Washing v4.3 Defense Freeze

This release freezes AI Washing v4.3 as the current computational reference target for the workstation.

## Release Meaning

- The v4.3 PDF and LaTeX source under `paper/` are the reference manuscript assets.
- The v4.3 generated-run evidence under `data/curated/v4_3/generated_runs/` is the reference output evidence where safe to track.
- The v5.0 editorial source is preserved under `paper/v5_0_editorial_source/` and should guide manuscript presentation. It should not drive code reproduction unless a future release explicitly promotes v5.0 as a numerical freeze.

See `docs/v5_editorial_alignment.md` for the v4.3/v5.0 boundary.

## Validated Numerical Gate

Selected table reruns have passed for `T00`, `T16`, `T17`, `T09`, and `T30`. Fresh reproduced CSV outputs exactly match frozen v4.3 generated CSV evidence.

## Known Release Limits

- Full-table expansion remains pending.
- Several manuscript TeX files include wrapper, caption, note, or formatting deltas relative to generated numeric payloads.
- Private/licensed data remain outside Git and must be staged through `AIW_DATA_ROOT`.
- Figure PDFs remain frozen manuscript assets unless later regeneration is explicitly required.
