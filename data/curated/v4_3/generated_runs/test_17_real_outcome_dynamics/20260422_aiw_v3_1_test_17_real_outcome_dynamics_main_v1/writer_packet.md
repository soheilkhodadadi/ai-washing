# Writer Packet: test_17_real_outcome_dynamics

## Role In The Paper
- This run asks whether the AI-talking sample reveals stronger non-market consequences than the older full-panel real-effects table.
- The comparison keeps the canonical construct in the lead, but checks whether an application-side mismatch or a disclosure-only low-credibility flag tells a cleaner operating story.

## Sample Definition
- Annual panel: `/Users/soheilkhodadadi/Documents/Projects/semantic-patterns/data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet`
- Working sample: `AI-talking firm-years only`
- Rows: `13777`
- Firms: `5084`
- Fixed effects: `firm + year`
- Winsorization: `1st / 99th percentile on each future outcome`

## Headline Read
- Canonical PatentMismatch on ROA t+2: `-0.0672` (p=`0.013`)
- Canonical PatentMismatch on R&D/assets t+2: `0.0178` (p=`0.012`)
- LowCredibility on ROA t+2: `-0.0649` (p=`0.009`)

## Caption Draft
This table revisits non-market consequences inside the AI-talking sample. Each row is a future operating or investment outcome measured at t+1 or t+2. The columns compare the canonical grant-based PatentMismatch construct, the application-based mismatch variant, and the disclosure-side LowCredibility variant. All specifications absorb firm and year fixed effects, include outcome-appropriate core controls, cluster standard errors by firm, and winsorize each future outcome at the 1st and 99th percentiles.
