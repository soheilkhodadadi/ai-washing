# Result Notes

- Human-human IRR rerun: Cohen's kappa `0.850` on `120` reviewed items.
- By-class kappa: Actionable `0.852`, Speculative `0.790`, Irrelevant `0.907`.
- Selected hybrid policy reaches `85.0%` accuracy and `83.6%` macro-F1 on `120` heldout-v4 items.
- Relative to the local-only baseline, the hybrid policy adds `6.7` percentage points of accuracy and `6.6` percentage points of macro-F1.
- Deferral footprint: `40` rows (`33.3%` of the benchmark) routed to API-A.
- The leakage-flagged local-only evaluation file `heldout_v4_selective_defer_conf49_v1.json` is intentionally excluded from the main audit.
