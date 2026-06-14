# Extension Starters

This folder contains coauthor extension material that is intentionally separate from the frozen v4.3 reproduction evidence. Extension outputs are ignored under `outputs/extensions/` and should be promoted only through an explicit future manuscript release.

## Available Lanes

- `builder_hides_first_pass.md`: runnable first-pass test for whether real-AI right-tail firms disclose less actionable AI detail.
- `washing_pays_proxy_first_pass.md`: operational proxy screen based on Test 30's next-year CRSP share-growth rule.
- `washing_pays_data_requirements.md`: data requirements and schema-check path for the stronger SEO/offering-terms version of the capital-raising extension.

## Commands

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make extension-info EXTENSION=builder_hides
make extension-builder-hides
make extension-builder-hides-ai-talk-only
make extension-info EXTENSION=washing_pays_proxy
make extension-washing-pays-proxy
make check-seo-schema SEO_FILE=/path/to/seo_offering_terms.csv
```

The extension registry is `manifests/extension_workbench.csv`. It records each lane's purpose, command, data needs, output folder, and interpretation limits.

## Promotion Rule

Do not overwrite v4.3 evidence with extension outputs. If an extension becomes part of a new manuscript version, add a release note, update the paper table workbench, and preserve the v4.3 reference files.


## Streamlit Extension Lab

The optional Streamlit app has an **Extension Lab** page that presents the same registry with a more readable interface. It can preview generated aggregate extension outputs under `outputs/extensions/` and run an in-memory schema-only check for a candidate SEO/offering-terms CSV. Extension Lab itself is read-only; approved extension commands can run only through Command Center. The app does not save uploads or display private row-level values.
