# Builder-Hides First-Pass Extension

This note gives coauthors a low-friction starting point for testing the "builder hides" channel: among firms with strong real AI activity, do disclosures contain less actionable AI detail?

This is an extension screen, not a frozen v4.3 result and not a causal claim.

## Research Question

The current paper mostly asks whether firms with low-substance AI talk have weak real AI evidence. The builder-hides extension asks the mirror-image question:

> Among firms with strong real AI evidence, is actionable AI disclosure lower rather than higher?

A positive relation between real AI activity and actionable disclosure supports the validation channel. A negative relation is consistent with a strategic disclosure channel in which real builders avoid revealing implementation detail.

## Runnable Starter

From the repository root:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make extension-builder-hides
```

To restrict the screen to firm-years that mention AI:

```bash
make extension-builder-hides-ai-talk-only
```

Outputs are written under:

```text
outputs/extensions/builder_hides_right_tail/
outputs/extensions/builder_hides_right_tail_ai_talk_only/
```

The output files are:

- `builder_hides_descriptive.csv`
- `builder_hides_regressions.csv`
- `builder_hides_summary.json`
- `builder_hides_interpretation.md`

Generated outputs stay outside Git unless deliberately promoted as sanitized documentation.

## Design Choices

The starter script is `src/semantic_ai_washing/analysis/extensions/builder_hides_right_tail.py`.

It uses the canonical annual panel:

```text
$AIW_DATA_ROOT/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet
```

The main right-tail builder indicator is `top_builder_lagged`:

- `real_ai_lagged = patents_ai_lag1 + applications_ai_lag1`
- within each year, among firms with positive lagged real AI activity, flag observations at or above the 90th percentile
- require at least 10 positive real-AI observations in the year before computing the tail

The lagged signal is the safer first-pass specification because it avoids defining current disclosure outcomes using future patent/application activity. The default sample includes all valid firm-years so that non-disclosure can be part of the hiding margin; use `--ai-talk-only` for the intensive-margin version among firms that already mention AI.

The script also reports `top_builder_current` descriptively, but the regression screen uses the lagged signal.

## Outcomes

The starter script checks these disclosure outcomes when available:

- `ActShare`
- `CredAI`
- `AI_Focus`
- `share_A`
- `share_S`
- `SpecShare`
- `SpecMinusAct`
- `LowCredibility`

The regression screen estimates each disclosure outcome on `top_builder_lagged`, controls, SIC2 fixed effects, and year fixed effects, with firm-clustered standard errors.

## Interpretation Rules

Use this as a diagnostic, not as a final table.

- If `top_builder_lagged` is negative for actionable or credible disclosure, inspect patent examples before claiming a builder-hides channel.
- If `top_builder_lagged` is positive, that supports the validation interpretation that real AI builders also disclose more substance.
- If the signs differ by outcome, separate the disclosure-margin story: broad AI focus can rise while implementation detail remains protected.
- If results are weak or sensitive, treat this as a null or boundary condition rather than forcing the narrative.

## Suggested Next Edits

Useful variations that do not need new data:

1. Replace the 90th percentile with 75th, 80th, or 95th percentile thresholds.
2. Use patents-only and applications-only right tails separately.
3. Restrict to firms with any AI talk using `--ai-talk-only`.
4. Add firm fixed effects rather than industry fixed effects if the goal is within-firm disclosure changes.
5. Compare the result after excluding obvious short-acronym patent keyword cases once the next patent-quality layer is available.

Useful variations that need new data or stronger design:

1. Add product-launch, hiring, or customer-facing AI evidence.
2. Add more refined patent-quality measures based on abstracts or CPC classes.
3. Build matched samples by industry, firm size, and prior disclosure activity.

## Referee Lens

A strict referee would object if we overstate this script as evidence that firms intentionally hide information. The current script only shows whether real-AI right-tail firms disclose less actionable detail conditional on controls and fixed effects. Intent requires stronger institutional evidence or additional design.
