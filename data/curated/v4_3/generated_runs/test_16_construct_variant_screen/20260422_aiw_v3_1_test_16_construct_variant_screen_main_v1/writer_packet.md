# Writer Packet: test_16_construct_variant_screen

## Role In The Paper
- This run opens the post-market non-risky lane: a structured screen of nearby AI-washing constructs against later AI realization outcomes.
- It helps decide whether the canonical PatentMismatch construct remains the right main text measure and which nearby variants deserve appendix or robustness status.

## Sample Definition
- Annual panel: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`
- Working sample: `AI-talking firm-years only`
- Rows: `13777`
- Firms: `5084`
- Fixed effects: `firm + year`
- Inference: `firm-clustered standard errors`

## Variant Definitions
- Canonical grant mismatch: low-credibility disclosure plus weak contemporaneous grant-side capability relative to the industry-year mean.
- Strict grant mismatch: same as above, but the low-credibility leg requires both low A/S and high speculative share instead of either condition alone.
- Application mismatch: low-credibility disclosure plus weak contemporaneous application-side capability relative to the industry-year mean.
- Low credibility only: disclosure-side construct without the capability filter.
- Weak patent only: capability-side construct without the disclosure filter.

## Headline Read
- Canonical PatentMismatch on future grants t+1: `-0.0435` (p=`0.001`)
- Canonical PatentMismatch on future applications t+2: `0.0685` (p=`0.000`)
- WeakPatentRelative on future grants t+1: `-0.1276` (p=`0.000`)

## Caption Draft
This table screens nearby AI-washing constructs inside the AI-talking annual sample. Panel A relates each construct variant to future AI grant realization, and Panel B relates the same variants to future AI application realization. All specifications absorb firm and year fixed effects, include AI Focus and core firm controls, and cluster standard errors by firm. The table is meant to rank interpretability and predictive content across nearby constructs rather than to mechanically replace the audited canonical measure.
