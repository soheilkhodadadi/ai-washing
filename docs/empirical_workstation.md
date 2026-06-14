# Empirical Workstation Guide

This repository is the working empirical environment for the AI Washing paper. It is organized so coauthors can verify v4.3, inspect the data products behind each table, and start new tests without using the older `semantic-patterns` workspace.

## What The Workstation Does

The paper studies whether firms use AI-related disclosure that is not supported by observable AI innovation. The core workflow links four layers:

1. SEC disclosure text is cleaned and searched for AI-related sentences.
2. A hybrid classifier separates actionable AI language from speculative or irrelevant AI language.
3. AI disclosure measures are merged with PatentsView AI patent/application evidence, WRDS/Compustat controls, CRSP market data, and selected governance/event data.
4. Publication scripts generate the v4.3 tables, figures, and extension-ready data products.

The repository keeps v4.3 as the frozen computational reference. Future work should create a new release note before replacing v4.3 evidence.

## Data Flow

```text
SEC filings and Stage-One cleaned text
    -> extracted AI sentence files
    -> final hybrid classifier outputs
    -> filing-level AI measures
    -> annual AI disclosure panel

PatentsView grants and pregrant applications
    -> AI patent keyword screens
    -> company/assignee matching and diagnostics
    -> annual patent support measures

WRDS, Compustat, CRSP, ExecuComp, and event files
    -> firm controls, market features, event returns, CEO incentive data
    -> annual and event-analysis panels

Annual/event panels
    -> publication scripts
    -> table CSV/TeX evidence, figure-series evidence, and frozen manuscript assets
```

Private or licensed inputs live under `AIW_DATA_ROOT`; Git tracks code, docs, manifests, fixtures, and frozen manuscript assets.

## Main Data Products

- Annual NLP/patent panel: the main firm-year panel for disclosure, patent, control, governance, and future-outcome tests. The v4.3 annual lane covers 2016-2025.
- Filing-event estimation sample: the filing-event panel for return and event-window tests. The v4.3 event/market lane covers 2016-2024 because staged CRSP return inputs stop at 2024-12-31.
- Final classifier outputs: the 2016-2025 hybrid classifier output with 147,879 classified AI sentences.
- Patent evidence pack: final grant and pregrant counts, company/assignee matching diagnostics, keyword metadata, examples, and PatentsView source documentation.
- WRDS/market bridge: Compustat, CRSP, CIK-GVKEY-PERMNO bridge files, market features, daily filing returns, and validation reports.

Use `docs/private_data_contract.md` and `docs/coauthor_data_room.md` for exact private-data paths.

## How To Find And Modify A Table

Use `docs/paper_table_workbench.md` first. It maps each manuscript table and figure to:

- the empirical question;
- the main data product and constructs;
- the owning Python module;
- the rerun command;
- reference outputs;
- safe modification notes;
- extension relevance.

The machine-readable version is `manifests/paper_table_workbench.csv`. The older `manifests/table_to_script_crosswalk.csv` remains the reproduction crosswalk; the workbench adds paper-facing interpretation and coauthor workflow guidance.

Useful terminal helpers:

```bash
make workbench-index
make table-info TABLE_ID=T30
make export-table-workbench TABLE_ID=T30
```

The export command writes an ignored inspection bundle under `outputs/workbench/<asset_id>/` without copying private data.

## Historical Run Identifiers

Some script modules and output filenames retain labels such as `legacy_*`, `v3_1`, or `v3_2`. These are historical run identifiers from the v4.3 build sequence. They are kept because they preserve provenance and make reproduced outputs comparable to the frozen manuscript evidence. They are not separate workstations and they do not require access to the older project folders. Coauthors should navigate by manuscript table labels, asset IDs, and the canonical `data/curated/v4_3/...` reference paths listed in the paper table workbench.

## Fastest Coauthor Path

```bash
make docker-build
make docker-preflight
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make docker-private-check
make docker-reproduce-selected
```

After that, use the table workbench to rerun or modify a specific table:

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make TABLE_ID=T30 reproduce-table
make export-table-workbench TABLE_ID=T30
```

## Extension Lanes

The repository includes extension starters but does not promote them into v4.3 results automatically.

- Washing pays: starts from Test 30 and future SEO/offering-terms data. The current v4.3 result uses next-year CRSP share-growth as a capital-raising proxy.
- Builder hides: starts from the annual patent and disclosure panel to test whether stronger AI builders disclose less actionable detail.
- Measurement robustness: starts from Appendix A, the classifier evaluation files, and short-acronym/keyword audit layers.
- Market response: starts from Main Table 8 and Appendix C return/event-window tests.

See `docs/extension_playbook.md` and `docs/extensions/` for starter notes.

Operational extension helpers:

```bash
make extension-info EXTENSION=builder_hides
make extension-builder-hides
make extension-builder-hides-ai-talk-only
make extension-info EXTENSION=washing_pays_proxy
make extension-washing-pays-proxy
```

## Guardrails

- Do not commit private data, generated outputs, local environments, or credentials.
- Do not replace v4.3 evidence silently; create a release note for promoted v5+ results.
- Keep annual and event-market lanes separate unless a new CRSP/event-return refresh is explicitly staged and validated.
- Use the table workbench before changing an empirical script so table ownership and data dependencies stay clear.
