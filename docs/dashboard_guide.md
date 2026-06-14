# Dashboard Guide

The dashboard layer is a navigation aid for the AI Washing workstation. It does not replace the Make/Docker workflow and does not expose private data values. Most pages are read-only; the Streamlit **Command Center** can run a small allowlist of local Make targets with confirmation gates and ignored logs.

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

The dashboard includes searchable cards for paper assets, data products, construct playbooks, extension lanes, and share-readiness commands. The static dashboard is non-executing and prints copy-ready terminal commands only. Its generated HTML lives under ignored `outputs/dashboard/`, so it is local until copied to Dropbox or published through a deliberate static-site release.


## Streamlit App Product Layer

The Streamlit app is the richer coauthor/client interface. It is organized as a multipage dashboard with Coauthor Mode and Demo Mode. The product contract is documented in:

- `docs/dashboard_product_spec.md`
- `docs/dashboard_user_stories.md`
- `docs/dashboard_information_architecture.md`

The app is read-mostly in Phase 9. Review, data, construct, and extension pages display copy-ready commands; **Command Center** is the only page that can execute approved local Make targets.

## Review Main Table 7 In The App

For a nontechnical table review, open the Streamlit app and go to **Table Explorer**. The page opens around paper labels rather than internal asset IDs. Use **Review Main Table 7** or select:

```text
Main Table 7 - Capital-raising timing and low-credibility AI disclosure
```

The page shows an **Open First** panel, safe CSV preview, available PNG/PDF/DOCX/CSV/TeX/notes artifacts, and a downloadable table-review packet. Table Explorer does not rerun the table or inspect private panels; it only reads repo-contained review artifacts.

## Inspect A Table Technically

For technical continuation work, open the same **Table Explorer** page and switch to **Technical Drill-Down**. This tab maps the selected table to:

- the owning Python module and repo-relative source file;
- the table-to-script crosswalk status and notes;
- candidate data products, keys, coverage, overwrite rules, and metadata-only schema/status checks;
- construct playbooks and extension lanes;
- copy-ready commands for table export, rerun, data location, and registered extensions.

If `AIW_DATA_ROOT` is set before launching the app, the drill-down can report file existence, row counts, file counts, and column names for private data products. It does not display row-level private values, access details, or old local workspace paths.

## Inspect Data Quality And Construct Evidence

Use **Data Room** when the question is, “where is this data product and what is its validation status?” The page now shows:

- classifier evidence, including final classifier coverage, row count, label inventory, held-out support, and acronym-risk status;
- patent-match evidence, including grant/pregrant example counts, keyword ambiguity counts, company identity metadata, and patent audit links;
- WRDS/CRSP/Compustat lane checks, including the 2016-2025 annual panel lane and the 2016-2024 event/market-return lane;
- metadata-only schema/status checks from `AIW_DATA_ROOT`, limited to existence, file count, row count, column names, and file type.

Use **Construct Audits** when the question is, “how confident are we in this construct?” The page links each construct to its playbook, relevant data products, audit checks, and copy-ready validation commands. It does not display private row-level values.


## Inspect Extension Lanes In The App

Open **Extension Lab** to review follow-on tests without mixing them into frozen v4.3 evidence. The page shows Builder Hides, Builder Hides AI-talk-only, Washing Pays Proxy, and the future SEO/offering-terms placeholder with status badges, purpose, inputs, generated aggregate outputs where present, interpretation limits, and copy-ready commands.

Every lane is marked as exploratory, proxy, or future-data-required, and as not manuscript-ready unless a later release explicitly promotes it. The strong washing-pays placeholder includes a schema-only CSV checker for future SEO/offering-terms data. The checker reports column coverage and row count only; it does not save uploaded files or display row values.

## Controlled Command Center

Open **Command Center** when a trusted local coauthor wants to run a routine workstation command from the app. The page is deliberately narrow:

- commands are selected from `manifests/dashboard_command_registry.csv`;
- every command maps to fixed `make ...` argv and runs with `shell=False`;
- data-dependent or output-writing commands require explicit confirmation;
- execution is disabled in Demo Mode;
- raw logs and metadata are written under ignored `outputs/dashboard_runs/`;
- the app shows exit code, duration, sanitized log tail, and a readable failure hint.

Full-table reproduction and replication-audit execution are not exposed in Command Center v1. Run those manually from a terminal or Docker after the allowlisted runner has been proven stable.

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

Then open the local URL printed by Streamlit. If private data are mounted, the app still does not display private values. Use Data Room for metadata-only data checks or Command Center for approved local Make targets.

## Portfolio Demo And Screenshots

Use **Portfolio Demo Mode** when showing the dashboard outside the private research team. It presents a nonprivate case-study overview of the workstation: the research problem, manifest-first workflow, evidence surfaces, reusable methodology, and the information hidden in Demo Mode.

For a simpler one-click static presentation that does not require Streamlit, generate the portfolio demo:

```bash
make portfolio-demo
make portfolio-demo-check
open outputs/portfolio_demo/index.html
```

This page is generated from manifests, executes no commands, and is designed for nontechnical review or public-safe demonstration. See `docs/portfolio_demo_deployment.md` and `docs/dashboard_sharing_options.md`.

To prepare a local screenshot checklist, run:

```bash
make dashboard-screenshots
```

This writes an ignored guide under `outputs/portfolio_screenshots/`. Capture external screenshots in Demo Mode unless a coauthor explicitly requests an internal view.

## Scope Boundary

- Safe: browsing table/data/extension metadata, copying commands, locating documentation, and running approved Command Center targets locally.
- Not included: arbitrary shell commands, editing panels, rendering manuscript PDFs, full-table reproduction from the browser, replication-audit execution from the browser, or previewing private data rows.
- Future option: broader command execution can be considered only after the narrow allowlisted runner remains stable.
