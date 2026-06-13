# Journal Replication Archive Policy

The AI Washing workstation supports two related but distinct release profiles. Keeping them separate reduces confusion for coauthors now and for a journal data editor later.

## Private Coauthor Workstation

Audience: project coauthors.

Purpose: reproduce the v4.3 computational results, inspect data provenance, review construct-validity limitations, and extend the analysis.

May include:

- coauthor setup and data-room runbooks;
- extension starters and future-data notes;
- private data-room instructions;
- frozen v4.3 manuscript assets and generated comparison evidence;
- formal audit outputs under `reports/replication_audit/`.

This profile can include more operational guidance than a journal archive because it is designed to reduce collaboration friction.

## Future Journal Archive

Audience: journal data editor, referee, replication archive, or future public supplement.

Purpose: reproduce published results and document data restrictions without exposing private, informal, or collaborator-specific materials.

Should include:

- root README and formal reproduction instructions;
- code, scripts, tests, pinned dependencies, Docker/devcontainer files;
- table-to-script and data-dependency manifests;
- formal data availability and provenance statements;
- pseudo/sample data where restricted data cannot be distributed;
- frozen generated evidence and validation logs needed to compare outputs;
- known limitations stated in formal language.

Should exclude:

- informal email drafts and internal phase logs;
- local validation notes and development diaries;
- local paths except formal provenance references where unavoidable;
- private or licensed data unless journal policy and provider terms explicitly allow it;
- credentials, tokens, `.env`, caches, generated runtime folders, and raw worktree artifacts.

## Practical Rule

For coauthors, share the private GitHub repo plus the OneDrive private-data room.

For a journal, create a clean release archive from Git and run `make package-surface-audit` before deposit. Do not zip the raw working directory because ignored local folders such as `.venv`, `.pytest_cache`, and generated `outputs/` may be present.

## Current Split

The current repository is prepared as a private coauthor workstation. Informal share notes, phase logs, and development process reports have been archived outside the repository under the internal handoff archive. The visible repository keeps formal runbooks, manifests, reproduction scripts, audit summaries, extension starters, and documented limitations.
