# v5.0 Editorial Alignment

This workstation keeps **AI Washing v4.3** as the frozen computational reference and preserves **AI Washing v5.0** as the current editorial presentation benchmark.

The distinction is intentional. v4.3 is the version whose tables, figures, scripts, and generated evidence are validated by the reproduction ledgers. v5.0 records coauthor edits to manuscript wording, figure captions, appendix wrappers, table notes, and presentation. It is not treated as a new numerical release unless the team later promotes it explicitly.

## What v5.0 Contributes

The v5.0 source package is preserved under:

```text
paper/v5_0_editorial_source/
```

The inventory is tracked at:

```text
manifests/v5_0_editorial_asset_inventory.csv
```

Compared with the v4.3 source, the v5.0 package mainly changes:

- manuscript wording in the introduction, methods, results, conclusion, and references;
- the figure caption for the time-series plot so the caption matches the 2018-2025 x-axis shown in the figure;
- appendix table wrappers, including controls/fixed-effect rows, repeated standard errors, column-separation notes, and variable-definition presentation;
- internal development labels in appendix presentation, such as raw classifier code labels, replaced with reader-facing descriptions.

The v5.0 package did not include a compiled `main.pdf` in the source zip staged here. Use the separate Overleaf/PDF copy if a rendered v5.0 manuscript is needed.

## What Remains v4.3

The following remain the computational source of truth until a later release is promoted:

```text
paper/v4_3_source/
data/curated/v4_3/
docs/full_reproduction_status.md
manifests/table_to_script_crosswalk.csv
manifests/paper_table_workbench.csv
```

Coauthors should use v4.3 for numerical verification and v5.0 for manuscript presentation. If a v5.0 numerical freeze is later required, rerun the full table and figure checks, refresh the reproduction ledger, and tag a new release.

## Practical Rule

When a table or figure differs between v4.3 and v5.0, first ask whether the difference is numerical or presentational.

- Numerical difference: treat it as a release-promotion issue and rerun the relevant script before circulating the paper.
- Caption, wrapper, note, or prose difference: use the v5.0 editorial source as the presentation benchmark while keeping v4.3 generated CSV evidence as the numerical reference.

This policy acknowledges the coauthor editorial work without weakening the reproducibility boundary around the validated v4.3 evidence.
