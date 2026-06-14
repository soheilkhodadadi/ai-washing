# Coauthor Delivery Overview

This repository and the separate private data room are designed to answer the coauthor request for the full AI Washing research package: code, cleaned panel, patent match, classifier outputs, CRSP/Compustat merges, and scripts that build every table.

## What To Open First

Start with these files:

```text
README_START_HERE.md
docs/coauthor_delivery_overview.md
docs/paper_table_workbench.md
docs/panel_and_data_catalog.md
```

For a browser-based view, run the dashboard locally:

```bash
make dashboard-app
```

The dashboard includes a table explorer, data room, construct audit browser, extension lab, reproduction status page, and a controlled command center for approved local Make targets. Generated dashboard HTML is local and ignored by Git unless the team deliberately publishes a sanitized static or hosted release; see `docs/dashboard_sharing_options.md`.

## What Is In Git

Git contains the materials that should be versioned and reviewed as code:

- publication table scripts and helper modules;
- the table-to-script crosswalk and paper table workbench;
- data-product, source, artifact, and extension manifests;
- formal setup, method, validation, and limitation documentation;
- small fixtures and smoke tests;
- frozen v4.3 manuscript assets and safe generated evidence;
- v5.0 editorial LaTeX source as a presentation benchmark;
- static and Streamlit dashboard code.

## What Is In The Private Data Room

Private, licensed, large, or machine-local data live outside Git under `AIW_DATA_ROOT`. The private data room includes or points to:

- the canonical cleaned annual NLP/patent panel;
- filing-event and market-return panels;
- final classifier outputs and extracted AI-sentence support;
- label and held-out validation support files;
- patent match artifacts, keyword metadata, company identity metadata, and patent validation reports;
- CRSP, Compustat, ExecuComp, linking, and market-feature extracts needed for current reruns;
- representative SEC source samples and source-documentation links;
- frozen generated-run evidence where it is not appropriate to track the artifact in Git.

Validate the private data room with:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make check-private-data
make validate-data-room
make validate-sec-source
make validate-wrds-data
make validate-patent-data
make audit-artifact-coverage
```

## Where To Find A Table

Use the table workbench rather than searching by filename:

```bash
make workbench-index
make table-info TABLE_ID=T30
make table-script TABLE_ID=T30
make export-table-workbench TABLE_ID=T30
```

Each table bundle explains the question, data products, owning script, reference outputs, rerun command, and safe modification path.

## Current Numerical Reference

The frozen computational reference is v4.3. The current reproduction status is documented in:

```text
docs/full_reproduction_status.md
docs/figure_reproduction_status.md
docs/c7_format_delta_explanation.md
```

The expected status is exact CSV reproduction for the validated table evidence, with the known C7 numeric-string formatting delta documented separately. Figure PDFs remain frozen manuscript assets; regenerated figure-series evidence is available as an audit layer.

## v5.0 Editorial Source

The v5.0 editorial source is included under:

```text
paper/v5_0_editorial_source/
```

Use it for manuscript presentation, wording, captions, appendix wrapper fixes, and table notes. Use v4.3 for numerical reproduction until a later release promotes v5.0 or another version as a new computational freeze.

See `docs/v5_editorial_alignment.md` for the exact policy.

## Extension Lanes

Two follow-on directions are ready for coauthor inspection:

```bash
make extension-info EXTENSION=builder_hides
make extension-builder-hides
make extension-builder-hides-ai-talk-only
make extension-info EXTENSION=washing_pays_proxy
make extension-washing-pays-proxy
```

Builder Hides and the AI-talk-only variant are exploratory first-pass tests. Washing Pays currently uses the v4.3 share-growth proxy from Test 30. The stronger SEO/offering-terms version remains a future-data extension and should use:

```bash
make check-seo-schema SEO_FILE=/path/to/seo_offering_terms.csv
```

## Sharing Rule

Share the package as two coordinated pieces:

1. Private GitHub repository for code, documentation, manifests, dashboards, and versioned evidence.
2. Private Dropbox data room for restricted data and large artifacts.

Do not put the Git repository inside Dropbox or any other sync folder. Keep `.git` local and use Dropbox only for the external data mirror. Share the live Dropbox URL privately; do not commit the access link to Git.
