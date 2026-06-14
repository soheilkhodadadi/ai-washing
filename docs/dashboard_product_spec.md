# Dashboard Product Spec

## Purpose

The AI Washing dashboard is a coauthor-facing interface for navigating the empirical workstation. It sits above the existing Git, Docker, Make, manifest, and private-data-root workflow. The dashboard should make the paper easier to review, extend, and explain without weakening the validated command-line reproduction path.

The dashboard has three jobs:

1. Help a technical coauthor locate tables, scripts, panels, construct definitions, classifier evidence, patent evidence, and extension lanes quickly.
2. Help a nontechnical supervisor or research client inspect results, understand the paper narrative, and review polished outputs without starting from terminal commands.
3. Provide a portfolio-safe demonstration of a reproducible finance, NLP, and data-science workstation.

## Audiences

- **Technical coauthor:** validates table outputs, inspects data products, modifies scripts, and develops follow-on tests.
- **Supervisor / research client:** reviews the paper map, table meaning, figures, and extension outputs without needing to understand the repository internals.
- **Journal data editor:** verifies that the package has reproducible scripts, documented data boundaries, and no hidden local-machine dependency.
- **Portfolio reviewer:** sees a polished nonprivate demonstration of the project workflow and technical depth.

## Dashboard Modes

### Coauthor Mode

Coauthor Mode is the default. It may show real manifest metadata, paper labels, asset IDs, repo-relative paths, logical private-data paths, copy-ready Make commands, and links to workbench bundles. It must not show private row-level data, access details, local absolute paths, or untracked private outputs.

### Demo Mode

Demo Mode is portfolio-safe. It should emphasize the project narrative, dashboard capabilities, static summary metrics, and nonprivate manifest metadata. It should hide private-data-root instructions and avoid copy-ready commands that imply access to private data.

### Command Execution Policy

Phase 9A/B does not execute commands from the browser. The dashboard may display copy-ready commands only. Future command execution requires a separate design pass with an allowlist, explicit confirmation, run logs, output isolation, and disabled behavior in Demo Mode.

## Safety Model

- Read manifests and tracked documentation by default.
- Treat `$AIW_DATA_ROOT` as external and private.
- Display logical paths and schemas/status only when they are already documented in manifests.
- Never display private row-level values or file contents.
- Never mutate v4.3 frozen evidence from the app.
- Keep generated dashboard outputs under ignored folders.
- Keep static HTML and Make/Docker commands as the reproducibility backbone.

## Page Set

- **Home / Project Overview:** paper story, dashboard modes, quick metrics, and recommended first actions.
- **Paper Results:** paper-order map of tables and figures with plain-language purpose and review affordances.
- **Table Explorer:** technical table drilldown with script, data products, reference outputs, and export commands.
- **Data Room:** data product catalog, logical paths, coverage, keys, and private-data boundary.
- **Construct Audits:** construct playbook index and validation/audit orientation.
- **Extension Lab:** registered extension lanes, status, interpretation limits, and commands.
- **Reproduction Status:** validation posture, table/figure status links, and audit commands.
- **Share / Export Center:** export bundles, dashboard generation, Docker instructions, and share-readiness commands.
- **Portfolio Demo Mode:** nonprivate, presentation-oriented view of the workstation capability.

## Success Criteria

- A coauthor can identify the owning script and data products for any table without reading the whole README.
- A supervisor can start with paper results and inspect a table bundle without needing command-line literacy.
- A journal-style reviewer can find reproduction status, data boundaries, and audit materials.
- The dashboard works through both native Streamlit and Docker.
- The app remains read-only and does not expose private data values.
