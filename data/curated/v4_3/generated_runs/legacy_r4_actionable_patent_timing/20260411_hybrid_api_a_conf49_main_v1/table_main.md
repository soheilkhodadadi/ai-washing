## Table R4. Actionable Disclosure and AI Patent Timing

This table presents distributed-lag style firm-year regressions on the expanded 2016-2025 ever-speaker annual panel. The dependent variable is the actionable-disclosure indicator. Each column includes the full set of AI patent timing terms from `t-2` through `t+2`, so the rows trace how prior, contemporaneous, and future AI patenting line up with actionable AI disclosure. Columns vary the fixed-effects structure and sample trim while keeping the same baseline control set: size, leverage, cash/assets, R&D/assets, CAPX/assets, ROA, sales growth, and employees. Standard errors clustered at the firm level are shown in parentheses. Constants are omitted. (* p<0.1, ** p<0.05, *** p<0.01).

Dependent variable: Actionable disclosure

| Variable | Firm + year FE | Industry + year FE | Firm + year FE, non-fin. | Firm + year FE, non-fin./non-util. |
| --- | --- | --- | --- | --- |
| log(1 + AI patents) at t-2 | 0.018 | 0.015 | 0.013 | 0.013 |
|  | (0.018) | (0.020) | (0.017) | (0.017) |
| log(1 + AI patents) at t-1 | 0.021 | 0.023 | 0.024 | 0.024 |
|  | (0.016) | (0.016) | (0.016) | (0.016) |
| log(1 + AI patents) at t | 0.033** | 0.040** | 0.030* | 0.030* |
|  | (0.017) | (0.016) | (0.017) | (0.017) |
| log(1 + AI patents) at t+1 | 0.018 | 0.023** | 0.019* | 0.019* |
|  | (0.012) | (0.011) | (0.011) | (0.011) |
| log(1 + AI patents) at t+2 | 0.050*** | 0.057*** | 0.048*** | 0.048*** |
|  | (0.011) | (0.014) | (0.012) | (0.012) |
| Controls | Y | Y | Y | Y |
| Firm FE | Y | N | Y | Y |
| Industry FE | N | Y | N | N |
| Year FE | Y | Y | Y | Y |
| Non-fin. | N | N | Y | Y |
| No util. | N | N | N | Y |
| Adj. R² | -0.160 | 0.016 | -0.163 | -0.163 |
| Observations | 14,968 | 14,968 | 13,759 | 13,737 |
