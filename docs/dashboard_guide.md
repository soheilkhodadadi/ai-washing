# Dashboard Guide

The dashboard layer is a navigation aid for the AI Washing workstation. It does not replace the Make/Docker workflow, does not execute commands from the browser, and does not expose private data values.

## Static Dashboard

The static dashboard is the default coauthor-safe option. It is generated from three manifests:

- `manifests/paper_table_workbench.csv`
- `manifests/data_product_catalog.csv`
- `manifests/extension_workbench.csv`

Generate and validate it with:

```bash
make dashboard
make dashboard-check
```

Open:

```bash
open outputs/dashboard/index.html
```

The dashboard includes searchable cards for paper assets, data products, construct playbooks, extension lanes, and share-readiness commands. It prints copy-ready terminal commands, but the browser does not run them.


## Streamlit App Product Layer

The Streamlit app is the richer coauthor/client interface. It is organized as a multipage dashboard with Coauthor Mode and Demo Mode. The product contract is documented in:

- `docs/dashboard_product_spec.md`
- `docs/dashboard_user_stories.md`
- `docs/dashboard_information_architecture.md`

The app remains read-only in Phase 9A/B. It displays copy-ready commands but does not execute empirical scripts from the browser.

## Optional Streamlit App

The Streamlit app is an optional richer interface for coauthor demonstrations or portfolio presentation. It reads the same manifests as the static dashboard.

Native setup:

```bash
make dashboard-app-install
make dashboard-app
```

Docker setup:

```bash
make docker-build
make docker-dashboard-app
```

Then open the local URL printed by Streamlit. If private data are mounted, the app still does not display private values; use terminal commands such as `make locate-data PRODUCT_ID=... PREVIEW=1` for safe data-location checks.

## Scope Boundary

- Safe: browsing table/data/extension metadata, copying commands, locating documentation.
- Not included: executing empirical scripts from the browser, editing panels, rendering manuscript PDFs, or previewing private data rows.
- Future option: a controlled local command runner can be added later, but only after the static navigation layer is stable.
