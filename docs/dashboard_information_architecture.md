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
| Table Explorer | technical coauthor | inspect one asset deeply | paper table workbench | script, command, data products, outputs, safe modifications | copy commands only |
| Data Room | technical coauthor / data editor | locate data products and boundaries | data product catalog | coverage, keys, logical paths, locate-data commands | hide private path commands in demo mode |
| Construct Audits | coauthor / data editor | inspect construct definitions and limitations | construct playbooks | playbook links, construct commands, audit orientation | no private row examples |
| Extension Lab | coauthor | inspect extension lanes | extension workbench | status, commands, interpretation limits | label extensions as exploratory unless promoted |
| Reproduction Status | data editor | verify reproducibility posture | status docs and manifests | audit commands and status links | no command execution |
| Share / Export Center | all users | export bundles or run setup checks | workbench commands | copy-ready setup/export commands | commands are displayed, not executed |
| Portfolio Demo Mode | portfolio reviewer | see nonprivate capability showcase | manifests only | capability summary and demo-safe story | hide private-data-root instructions |

## Manifest Mapping

- `manifests/paper_table_workbench.csv` feeds Paper Results and Table Explorer.
- `manifests/data_product_catalog.csv` feeds Data Room and table data-product cross-references.
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

## Future Command Execution Boundary

A later command-execution phase may add an allowlisted runner for safe Make targets. That future runner must show the command, require confirmation, write logs to ignored outputs, and disable itself in Demo Mode. Phase 9A/B deliberately stops before this boundary.
