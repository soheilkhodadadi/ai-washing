# Table Main

## Panel A. Human labeling and validation
| Item | N | Primary metric | Supporting metric | Notes |
| --- | --- | --- | --- | --- |
| Adjudicated sentence base | 551 | Human-reviewed labels | Historical master corpus | Used to seed and refine the local sentence classifier. |
| Leakage-safe training pool | 431 | Human-reviewed labels | Excludes heldout-v4 items | Current training/calibration pool after removing benchmark sentences. |
| Current adjudicated benchmark | 120 | Final heldout-v4 labels | Deployment benchmark | Balanced benchmark used for the current hybrid evaluation posture. |
| Human-human IRR v3 rerun | 120 | Cohen's kappa = 0.850 | 12/12 disagreements adjudicated | By-class kappa: Actionable 0.852; Speculative 0.790; Irrelevant 0.907. |

## Panel B. Heldout-v4 model evaluation
| Item | N | Primary metric | Supporting metric | Notes |
| --- | --- | --- | --- | --- |
| Local-only baseline | 120 | Accuracy = 78.3% | Macro-F1 = 77.1% | Binary relevance 90.0%; A/S 78.4%; defer 0/120. |
| Selected hybrid policy | 120 | Accuracy = 85.0% | Macro-F1 = 83.6% | api_a_conf_or_margin; binary relevance 91.7%; A/S 86.5%; defer 40/120. |
