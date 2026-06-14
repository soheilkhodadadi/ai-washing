# Dashboard User Stories

## Technical Coauthor

- As a coauthor, I want to select a paper table by paper label or asset ID so I can find the exact script, data products, and rerun command.
- As a coauthor, I want to see which constructs each table uses so I can evaluate whether a robustness test should modify the panel, the construct definition, or only the regression specification.
- As a coauthor, I want to locate classifier outputs, patent match artifacts, WRDS/CRSP/Compustat data, and annual/event panels without depending on old local paths.
- As a coauthor, I want extension lanes separated from frozen v4.3 evidence so exploratory outputs are not confused with manuscript results.
- As a coauthor, I want copy-ready commands and links to workbench bundles, but I do not need the browser to execute code in this phase.

## Supervisor Or Research Client

- As a supervisor, I want a paper-order results page so I can understand which table supports which part of the manuscript.
- As a supervisor, I want the dashboard to explain what a table asks and why it matters before showing technical implementation details.
- As a supervisor, I want easy links to readable outputs such as table bundles, figures, and status summaries.
- As a supervisor, I want the dashboard to avoid repository jargon unless it is necessary for reviewing the work.

## Journal Data Editor

- As a data editor, I want to verify that each table and figure has a documented reproduction path and data boundary.
- As a data editor, I want to see that private, restricted, and derived data are separated from Git-tracked code and documentation.
- As a data editor, I want visible reproduction status and audit commands without hidden dependencies on the old `semantic-patterns` workspace.

## Portfolio Reviewer

- As a portfolio reviewer, I want a safe demo mode that communicates the technical scope, reproducibility design, and dashboard capability without exposing private data.
- As a portfolio reviewer, I want evidence that the system combines NLP, finance, patent matching, reproducible data products, Docker, and client-facing analytics.

## Out Of Scope For Phase 9A/B

- Running empirical commands from the browser.
- Editing data, panels, scripts, or manifests from the app.
- Displaying private row-level values.
- Replacing the static dashboard, Make commands, or Docker workflow.
