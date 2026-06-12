# Referee Audit Runbook

This runbook is the hostile-but-fair audit layer for the AI Washing workstation. It is designed to answer the question a finance referee or data editor would ask: if I try to reproduce the paper and inspect the data work, what could be wrong, hidden, or insufficiently documented?

## Benchmark Standards

The audit is aligned with five replication-package benchmarks:

- Journal of Finance Data and Code Sharing Policy: computational materials should disclose software, computation methods, logs, data or pseudo-data where restricted, package organization, usage instructions, operating system, packages, execution order, and random seeds where relevant.
- AEA Data Editor guidance: use computational empathy; the package should have a root README, source/provenance statements, computational requirements, software versions, runtime/storage expectations, instructions to replicators, and table-program mapping.
- Journal of Financial Economics policy: code should document raw-to-final data processing, sample construction, variable definitions, outlier treatment, and final output generation.
- Review of Financial Studies policy: a dedicated environment should reproduce key tables and figures, with clear documentation for derivative and restricted-access data.
- ACM artifact-review guidance: artifacts should be documented, consistent with the paper, complete enough to exercise, portable where possible, and accompanied by validation evidence.

## Audit Layers

Run the full audit with:

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make referee-audit
```

The full audit calls these layers:

```bash
make package-surface-audit
AIW_DATA_ROOT=/path/to/ai-washing-private-data make data-sanity-audit
AIW_DATA_ROOT=/path/to/ai-washing-private-data make textual-construct-audit
AIW_DATA_ROOT=/path/to/ai-washing-private-data make patent-construct-audit
AIW_DATA_ROOT=/path/to/ai-washing-private-data make journal-reproducibility-audit
```

## Severity Vocabulary

- `stop_the_line`: do not share until fixed or explicitly waived; examples include missing required data, duplicate primary keys, broken reproduction, or tracked private data.
- `material_needs_future_layer`: real risk that should be disclosed and addressed before journal submission, but not necessarily a blocker for coauthor handoff.
- `manageable`: visible issue that should be documented or cleaned, but does not undermine the current v4.3 reproduction package.
- `negligible`: checked risk with low observed exposure.
- `info`: contextual evidence useful for a reviewer.
- `ok`: audit passed.

## Referee Questions Covered

- Package surface: Are we accidentally sharing private data, generated outputs, cache files, credentials, or informal documents in the wrong package profile?
- Reproduction: Can the package rerun the v4.3 table/figure evidence and explain known deltas such as C7?
- Data lanes: Do annual NLP/patent and event/market-return panels have the correct row counts, date coverage, and key structure?
- Accounting/market sanity: Are there impossible values, duplicate keys, missing identifiers, or untreated CRSP/Compustat conventions?
- SEC text construct: Are `AI` and `ML` hits actually artificial-intelligence content, or are short-acronym false positives contaminating the measure?
- Patent construct: Are AI patent hits supported by title/abstract context, and are short-acronym-only matches flagged for review?
- WRDS/licensed data: Are source extracts, credentials, and redistribution boundaries handled cleanly?
- Coauthor versus journal archive: Is the package generous enough for Kuntara/Thomas but clean enough to later become a journal replication archive?

## Outputs

The audit writes machine-readable reports under `reports/referee/` and a human-facing summary at:

```text
docs/referee_first_impression_report.md
```

Generated reports are evidence, not manuscript results. If a report surfaces a limitation, update the relevant limitation note rather than hiding the finding.
