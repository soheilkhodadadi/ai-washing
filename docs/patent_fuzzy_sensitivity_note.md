# Patent Fuzzy Sensitivity Note

Generated: 2026-06-10

## Purpose

This note explains why the final v4.3 patent lane rejects fuzzy organization-name matching and keeps exact normalized matching as the baseline.

## Test Design

A bounded fuzzy sensitivity test was run for 2024 on both patent families:

- Grant patents.
- Pregrant published applications.

The test considered thresholds 0.90 and 0.95, with a best-vs-second-best gap rule. The goal was to see whether fuzzy matching could safely recover additional true firm-assignee matches that exact normalized matching might miss.

## Baseline Method

The live baseline is exact normalized matching:

1. Build normalized firm and alias terms from the hybrid company identity layer.
2. Drop normalized terms that map to more than one CIK.
3. Normalize PatentsView organization names.
4. Match only when the normalized PatentsView organization equals a unique normalized firm/alias term.

This method is conservative by design.

## Fuzzy Sensitivity Results

The fuzzy supplement produced implausibly large jumps.

Grant family:

| Lane | Total matches | AI matches |
| --- | ---: | ---: |
| Exact hybrid baseline | 40,931 | 2,122 |
| Fuzzy 0.90 | 105,018 | 4,453 |
| Fuzzy 0.95 | 76,063 | 3,621 |

Pregrant family:

| Lane | Total matches | AI matches |
| --- | ---: | ---: |
| Exact hybrid baseline | 27,595 | 1,849 |
| Fuzzy 0.90 | 72,886 | 3,923 |
| Fuzzy 0.95 | 51,557 | 3,302 |

These changes are too large to treat as a modest recall improvement.

## Manual Review Examples

The staged fuzzy example file is:

```text
data/reports/patents/ai_washing_patent_fuzzy_sensitivity_2024_sample_examples_v1.csv
```

Manual review found false positives driven by generic or short terms:

- `City of Hope` matched to `CITY HOLDING CO` through `city`.
- `CAPITAL ONE SERVICES, LLC` matched to an unrelated firm through `one`.
- `INTELLECTUAL DISCOVERY CO., LTD.` matched to `WARNER BROS DISCOVERY INC` through `discovery`.
- `ADVANCED VIEW INC.` matched to `VIEW INC` through `view`.

These are not harmless edge cases. They would directly contaminate the patent mismatch construct.

## Decision

Fuzzy matching is rejected for v4.3. The final patent lane uses exact normalized matching plus curated alias expansion.

This decision should be presented as a strength rather than an omission. The project tested a plausible broader match strategy, found that it generated too many false positives, and chose the more conservative method.

## Future Work If Fuzzy Matching Is Reopened

A future fuzzy/semantic matching lane would need a stricter method, for example:

- reject single-token generic matches;
- require multiple meaningful shared tokens;
- maintain a stoplist for generic terms such as `city`, `new`, `one`, `view`, `discovery`, and `southern`;
- use curated historical legal-name registries;
- manually validate sampled fuzzy-only additions by industry and firm size.

That would be a new method-development task, not a parameter tweak.
