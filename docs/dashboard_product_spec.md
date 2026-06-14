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
- **Nontechnical external viewer:** opens a static one-click portfolio page without installing Python, Docker, or Streamlit.

## Dashboard Modes

### Coauthor Mode

Coauthor Mode is the default. It may show real manifest metadata, paper labels, asset IDs, repo-relative paths, logical private-data paths, copy-ready Make commands, and links to workbench bundles. It must not show private row-level data, access details, local absolute paths, or untracked private outputs.

### Demo Mode

Demo Mode is portfolio-safe. It should emphasize the project narrative, dashboard capabilities, static summary metrics, nonprivate manifest metadata, and case-study screenshots. It should hide private-data-root instructions, disable command execution, and avoid copy-ready commands that imply access to private data.

The separate static portfolio demo is the simplest public-facing surface. It is generated with `make portfolio-demo`, checked with `make portfolio-demo-check`, and can be opened as `outputs/portfolio_demo/index.html` or hosted later as a static site. It is presentation-only and does not replace the Streamlit coauthor workstation.

### Thomas-Facing Table Review

The Table Explorer should support a nontechnical table review path. A supervisor or research client can select a result by paper label, for example `Main Table 7`, see the empirical question and review priority first, preview a safe CSV table, and download available DOCX, PDF, PNG, CSV, TeX, and notes artifacts from the canonical repository. Technical asset IDs such as `T30` remain visible, but they should not be the primary entry point for nontechnical review.

### Technical Coauthor Drill-Down

The Table Explorer should also support a technical continuation path. A coauthor can select any table or figure and open a **Technical Drill-Down** view that shows the owning script, source path, table-to-script crosswalk status, candidate data products, metadata-only source schema/status checks, construct playbooks, registered extension lanes, and copy-ready rerun/export/location commands. The drill-down may inspect file metadata under `AIW_DATA_ROOT` when the root is set, but it must not display private row-level values.

### Data Product And Construct Audit Browser

The Data Room and Construct Audits pages should support a data-quality cockpit view. A coauthor can inspect data product cards, coverage lanes, keys, logical private-data paths, validation status, classifier evidence, patent-match evidence, textual acronym-risk status, and WRDS/CRSP/Compustat lane checks. Metadata previews may report file existence, file count, size, row count, and column names from `AIW_DATA_ROOT`; they must not display private row-level values, sentence text, patent titles, abstracts, access details, or local absolute paths.


### Extension Lab And Future Tests

The Extension Lab is a follow-on research cockpit, not a frozen-results page. It should make Builder Hides, Builder Hides AI-talk-only, Washing Pays Proxy, and the future SEO/offering-terms version tangible while keeping all lanes clearly labeled as exploratory or future-data-required. Generated extension outputs may be previewed when they are aggregate repo-contained files under `outputs/extensions/`; private source rows and local paths must remain hidden. The strong washing-pays version may validate an uploaded CSV schema in memory, but it must not store uploaded data or display row values.

### Command Execution Policy

Most dashboard pages display copy-ready commands only. **Command Center** is the controlled exception: it may execute approved local Make targets from `manifests/dashboard_command_registry.csv`. It must not accept arbitrary shell text or user-entered Make targets. It must show the fixed command, require confirmation for data-dependent or output-writing commands, write raw logs under ignored `outputs/dashboard_runs/`, show a sanitized log tail, and disable execution in Demo Mode.

## Safety Model

- Read manifests and tracked documentation by default.
- Treat `$AIW_DATA_ROOT` as external and private.
- Display logical paths and schemas/status only when they are already documented in manifests.
- Never display private row-level values or file contents.
- Preview only repo-contained review artifacts, such as frozen v4.3 CSV outputs; never preview `$AIW_DATA_ROOT`.
- Never mutate v4.3 frozen evidence from the app.
- Keep generated dashboard outputs under ignored folders.
- Keep Command Center logs under ignored `outputs/dashboard_runs/`.
- Run only fixed allowlisted Make targets with `shell=False`; do not expose arbitrary shell execution.
- Keep static HTML and Make/Docker commands as the reproducibility backbone.

## Page Set

- **Home / Project Overview:** paper story, dashboard modes, quick metrics, and recommended first actions.
- **Paper Results:** paper-order map of tables and figures with plain-language purpose and review affordances.
- **Table Explorer:** paper-label table review with an Open First panel, safe CSV preview, artifact downloads, technical drill-down, source schema/status metadata, and export/rerun commands.
- **Data Room:** data product catalog, logical paths, coverage, keys, validation status, classifier/patent/WRDS evidence panels, and private-data boundary.
- **Construct Audits:** construct playbook index, validation/audit orientation, acronym-risk status, patent-match confidence, and WRDS lane checks.
- **Extension Lab:** registered follow-on tests, maturity badges, generated aggregate output previews, interpretation limits, copy-ready commands, and schema-only checks for future SEO/offering-terms data.
- **Reproduction Status:** validation posture, table/figure status links, and audit commands.
- **Command Center:** approved local Make targets, confirmation gates, environment summary, exit code, duration, and sanitized log tail.
- **Share / Export Center:** export bundles, dashboard generation, Docker instructions, and share-readiness commands.
- **Portfolio Demo Mode:** nonprivate, presentation-oriented case study of the workstation capability and reusable methodology.
- **Static Portfolio Demo:** one-click HTML landing page for nontechnical or public portfolio review, generated from manifests and safe narrative content.

## Success Criteria

- A coauthor can identify the owning script and data products for any table without reading the whole README.
- A technical coauthor can move from a table to source script, data dependencies, construct guidance, and extension relevance in under one minute.
- A coauthor can answer where the classifier evidence lives and how confident the patent match is without reading the full documentation set.
- A supervisor can start with paper results, open Main Table 7, inspect readable artifacts, and download a compact review packet without needing command-line literacy.
- A journal-style reviewer can find reproduction status, data boundaries, and audit materials.
- The dashboard works through both native Streamlit and Docker.
- The app remains read-only outside Command Center and never exposes private data values.
- Command Center can run approved local Make targets, but not arbitrary shell commands or full reproduction/audit targets.
- Portfolio Demo Mode and the static portfolio demo can be shown in screenshots or a portfolio without private data roots, row-level research data, command logs, or local machine paths.
