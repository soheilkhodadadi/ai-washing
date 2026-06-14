# Dashboard Information Architecture

## Navigation Structure

The app uses Streamlit multipage navigation with grouped pages.

- **Start**
  - Home / Project Overview
  - Portfolio Demo Mode
- **Paper Review**
  - Paper Results
  - Table Explorer
- **Data And Constructs**
  - Data Room
  - Construct Audits
- **Extensions And Reproduction**
  - Extension Lab
  - Reproduction Status
  - Share / Export Center

## Global Sidebar

The sidebar should contain:

- dashboard title;
- mode selector: `Coauthor Mode` or `Demo Mode`;
- safety note: read-only, manifest-first, no browser command execution;
- navigation pages grouped by task;
- quick links to static dashboard, README, dashboard guide, and table workbench docs.

## Page Contracts

| Page | Primary user | Main task | Inputs | Outputs | Safety rule |
| --- | --- | --- | --- | --- | --- |
| Home / Project Overview | all users | understand the project and first actions | table, data, extension manifests | metrics, paper story, first commands | no private data inspection |
| Paper Results | supervisor/client | review tables and figures in paper order | paper table workbench | paper sections, result cards, bundle commands | do not imply exploratory outputs are frozen evidence |
| Table Explorer | supervisor/client and technical coauthor | review one table by paper label, then inspect technical continuation details | paper table workbench, table crosswalk, data catalog, constructs, extensions, repo-contained artifacts | Open First panel, artifact downloads, safe CSV preview, source script, data products, metadata-only schema/status, construct links, extension relevance, copy-ready commands | preview only repo-contained artifacts; show private-data metadata only; copy commands only |
| Data Room | technical coauthor / data editor | locate data products and inspect audit status | data product catalog, source manifests, audit CSVs | data product cards, evidence panels, coverage, keys, validation status, metadata-only schema checks, locate-data commands | hide private path commands in demo mode; never display row-level values |
| Construct Audits | coauthor / data editor | inspect construct definitions, confidence, and limitations | construct playbooks, audit CSVs, data catalog | playbook links, construct commands, classifier/patent/WRDS evidence, acronym-risk status | summarize audit counts only; no private row examples |
| Extension Lab | coauthor | inspect extension lanes | extension workbench | status, commands, interpretation limits | label extensions as exploratory unless promoted |
| Reproduction Status | data editor | verify reproducibility posture | status docs and manifests | audit commands and status links | no command execution |
| Share / Export Center | all users | export bundles or run setup checks | workbench commands | copy-ready setup/export commands | commands are displayed, not executed |
| Portfolio Demo Mode | portfolio reviewer | see nonprivate capability showcase | manifests only | capability summary and demo-safe story | hide private-data-root instructions |

## Manifest Mapping

- `manifests/paper_table_workbench.csv` feeds Paper Results and Table Explorer.
- Repo-contained frozen/generated artifacts under `data/curated/v4_3/...` feed Table Explorer artifact previews and downloads.
- `manifests/data_product_catalog.csv` feeds Data Room and table data-product cross-references.
- `reports/replication_audit/*.csv` feeds Data Room and Construct Audits with nonprivate validation and construct-risk summaries.
- `manifests/extension_workbench.csv` feeds Extension Lab.
- Construct pages link to `docs/construct_playbooks/` and use registered construct IDs.
- Reproduction pages link to existing status documents and Make targets rather than duplicating table results.

## State Model

The app stores only nonprivate UI state:

- selected dashboard mode;
- selected paper section;
- selected table asset;
- selected data product;
- selected extension lane;
- search/filter strings.

No private file contents, access details, or command outputs should be stored in session state.

## Table Review Flow

The nontechnical review flow starts from paper labels rather than internal asset IDs:

1. Open **Paper Results** or **Table Explorer**.
2. Choose a result such as `Main Table 7 - Capital-raising timing and low-credibility AI disclosure`.
3. Read the **Open First** panel for the empirical question, relevance, canonical status, and first file to inspect.
4. Use the artifact sections to preview CSV evidence, view PNGs, and download DOCX/PDF/CSV/TeX/notes.
5. Use the technical details and copy-ready commands only if a rerun or modification is needed.

## Technical Drill-Down Flow

The technical coauthor flow starts from the same table selection but opens the **Technical Drill-Down** tab:

1. Select a paper table or figure by paper label.
2. Confirm the table-to-script crosswalk status and owning source module.
3. Inspect candidate data products, coverage, keys, overwrite rules, and metadata-only schema/status checks.
4. Open construct playbook links for variables that might be changed.
5. Review extension relevance and copy the relevant Make commands.
6. Run commands manually in a terminal; the browser does not execute them.

## Data Quality Cockpit Flow

The data-quality cockpit starts from **Data Room** or **Construct Audits**:

1. Open **Data Room** to answer “where is the classifier evidence?” or “where are the patent artifacts?”
2. Use the evidence tabs for classifier, patent, and WRDS lane status.
3. Filter data products by family, contract status, or validation status.
4. Open a product card to inspect coverage, keys, overwrite rules, logical private-data path, and metadata-only schema/status checks.
5. Open **Construct Audits** to answer “how confident are we in this construct?” using playbook links, audit counts, and copy-ready validation commands.

## Future Command Execution Boundary

A later command-execution phase may add an allowlisted runner for safe Make targets. That future runner must show the command, require confirmation, write logs to ignored outputs, and disable itself in Demo Mode. Phase 9A/B deliberately stops before this boundary.
