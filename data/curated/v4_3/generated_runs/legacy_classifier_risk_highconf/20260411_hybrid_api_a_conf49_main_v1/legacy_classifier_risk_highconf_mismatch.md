## Table C2. High-Confidence Local-Only Subset: A/S Ratio, PatentMismatch, and Future AI Patenting

This appendix table reruns the main `A/S × PatentMismatch` specification on the same conservative high-confidence subset used in Table C1. A firm-year enters only when the hybrid conf49 policy never deferred any sentence to API-A in that filing year. The dependent variable is `log(1 + AI patents)` at `t+1`, controls are unchanged, and columns vary the fixed-effects structure and sample trim.

Dependent variable: log(1 + AI patents at t+1)

| Variable | Firm + year FE | Industry×year FE | Firm + year FE, non-fin. | Firm + year FE, non-fin./non-util. |
| --- | --- | --- | --- | --- |
| A/S ratio | 0.085* | 0.267*** | 0.087* | 0.087* |
|  | (0.049) | (0.046) | (0.052) | (0.052) |
| A/S ratio × PatentMismatch | -0.065 | -0.408*** | -0.068 | -0.068 |
|  | (0.040) | (0.054) | (0.042) | (0.042) |
| Controls | Y | Y | Y | Y |
| Firm FE | Y | N | Y | Y |
| Industry×Year FE | N | Y | N | N |
| Year FE | Y | N | Y | Y |
| Non-fin. | N | N | Y | Y |
| No util. | N | N | N | Y |
| Adj. R² | -0.909 | 0.081 | -0.885 | -0.883 |
| Observations | 2,810 | 2,810 | 2,632 | 2,630 |
