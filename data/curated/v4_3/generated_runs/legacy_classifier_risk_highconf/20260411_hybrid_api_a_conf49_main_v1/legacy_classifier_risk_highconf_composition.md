## Table C1. High-Confidence Local-Only Subset: Disclosure Composition and AI Patent Timing

This appendix table reruns the disclosure-composition timing regressions on a conservative high-confidence subset. A firm-year enters the subset only when the hybrid conf49 policy never deferred any sentence to API-A in that filing year, so all AI sentence labels remain local high-confidence classifications. The dependent variable is `log(1 + AI patents)` measured at different calendar-time horizons relative to the disclosure year. Firm and year fixed effects are included in all columns, the baseline control set is unchanged, and standard errors are clustered at the firm level.

### Panel A. Actionable disclosure

| Variable | t-2 | t-1 | t | t+1 | t+2 |
| --- | --- | --- | --- | --- | --- |
| Actionable disclosure (dummy) | 0.047 | 0.049* | 0.030 | 0.035 | 0.072 |
|  | (0.029) | (0.029) | (0.029) | (0.039) | (0.047) |

### Panel B. Speculative-only disclosure

| Variable | t-2 | t-1 | t | t+1 | t+2 |
| --- | --- | --- | --- | --- | --- |
| Speculative-only disclosure (dummy) | -0.014 | -0.010 | -0.006 | -0.076 | -0.129 |
|  | (0.049) | (0.046) | (0.044) | (0.080) | (0.082) |
| Controls | Y | Y | Y | Y | Y |
| Firm FE | Y | Y | Y | Y | Y |
| Year FE | Y | Y | Y | Y | Y |
| Adj. R² | -0.953 | -0.954 | -0.928 | -0.922 | -0.916 |
| Observations | 2,810 | 2,810 | 2,810 | 2,810 | 2,810 |
