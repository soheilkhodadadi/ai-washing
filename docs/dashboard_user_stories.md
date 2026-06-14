# Dashboard User Stories

## Technical Coauthor

- As a coauthor, I want to select a paper table by paper label or asset ID so I can find the exact script, data products, and rerun command.
- As a coauthor, I want to see which constructs each table uses so I can evaluate whether a robustness test should modify the panel, the construct definition, or only the regression specification.
- As a coauthor, I want one technical drill-down tab that links the table to its source path, crosswalk status, data products, metadata-only schema checks, construct playbooks, and extension lanes.
- As a coauthor, I want copy-ready commands labeled by risk, such as read-only, requires private data, or writes ignored outputs.
- As a coauthor, I want schema and row-count checks to summarize private data products without printing private row-level values.
- As a coauthor, I want to locate classifier outputs, patent match artifacts, WRDS/CRSP/Compustat data, and annual/event panels without depending on old local paths.
- As a coauthor, I want a data-quality cockpit that answers where the classifier evidence lives, how patent matching was validated, and which WRDS lane each test uses.
- As a coauthor, I want metadata-only schema and row-count checks from `AIW_DATA_ROOT` without exposing sentence text, patent abstracts, or row-level private data.
- As a coauthor, I want textual acronym-risk and patent short-keyword-risk status summarized directly in the app so I know which construct-validity issues are already documented.
- As a coauthor, I want extension lanes separated from frozen v4.3 evidence so exploratory outputs are not confused with manuscript results.
- As a coauthor, I want most pages to stay read-only, with approved execution available only through a narrow Command Center allowlist.

## Supervisor Or Research Client

- As a supervisor, I want a paper-order results page so I can understand which table supports which part of the manuscript.
- As a supervisor, I want the dashboard to explain what a table asks and why it matters before showing technical implementation details.
- As a supervisor, I want to choose a table by paper label, such as `Main Table 7`, rather than by an internal asset ID.
- As a supervisor, I want an Open First panel that tells me whether to inspect DOCX, PNG, PDF, CSV, TeX, or notes first.
- As a supervisor, I want safe CSV previews and downloadable table-review packets when the files are already part of the canonical repository.
- As a supervisor, I want easy links to readable outputs such as table bundles, figures, and status summaries.
- As a supervisor, I want the dashboard to avoid repository jargon unless it is necessary for reviewing the work.

## Journal Data Editor

- As a data editor, I want to verify that each table and figure has a documented reproduction path and data boundary.
- As a data editor, I want to see that private, restricted, and derived data are separated from Git-tracked code and documentation.
- As a data editor, I want visible reproduction status and audit commands without hidden dependencies on the old `semantic-patterns` workspace.

## Portfolio Reviewer

- As a portfolio reviewer, I want a safe demo mode that communicates the technical scope, reproducibility design, and dashboard capability without exposing private data.
- As a portfolio reviewer, I want evidence that the system combines NLP, finance, patent matching, reproducible data products, Docker, and client-facing analytics.
- As a portfolio reviewer, I want a case-study page and screenshots that explain the reusable methodology without private research data.

## Out Of Scope For Phase 9

- Arbitrary shell commands or user-entered Make targets from the browser.
- Full-table reproduction or replication-audit execution from the browser.
- Editing data, panels, scripts, or manifests from the app.
- Displaying private row-level values.
- Replacing the static dashboard, Make commands, or Docker workflow.
