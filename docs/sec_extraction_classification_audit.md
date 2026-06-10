# SEC Extraction And Classification Audit Surface

This note explains what a coauthor should inspect if they want to evaluate the NLP construction without rebuilding the full SEC corpus.

## Current Audit Surface

The private data room contains four layers:

1. Source examples: representative full-submission SEC filings and Stage-One cleaned 2025 filings.
2. Extracted sentence layer: `processed/sec/sentences_clean` for 2016-2024 and `processed/sec/sentences_clean_refresh_2025_v1` for 2025.
3. Classifier layer: `processed/classifications/classifications_shadow_hybrid_api_a_conf49_v1`, the canonical April/v4.3 hybrid classifier output.
4. Quality support: held-out validation files, label files, and classifier evaluation reports.

The local-layered classifier output is retained as support/provenance, but it is not the canonical v4.3 classifier layer.

## What To Check First

A coauthor should start with:

```bash
make validate-sec-source
make audit-artifact-coverage
```

Then inspect a few source examples, extracted AI sentences, and classified outputs for the same year. The purpose is not to prove every filing manually. The purpose is to verify that the pipeline's source layer, extracted-sentence layer, and final classifier layer are coherent and traceable.

## Known Boundary

The package currently demonstrates extraction/classification mechanics through representative samples and staged outputs. It does not yet provide a one-command full-corpus raw SEC rebuild. That is by design for Phase 4F. If the paper moves to a journal replication package, we can either document public source download instructions or add a private full raw-source mirror depending on the journal and coauthor requirements.
