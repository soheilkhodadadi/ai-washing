# AI Washing

Canonical private research workstation for the **AI Washing** project.

This repository is the long-term collaboration and reproducibility home for the AI Washing paper. It currently freezes **AI Washing v4.3** as the computational reference target while supporting future coauthor work, journal revisions, and table/figure reruns.

Start here:

- [README_START_HERE.md](README_START_HERE.md): full workstation quickstart.
- [AGENTS.md](AGENTS.md): operating rules for Codex and automation agents.
- [docs/collaboration_workflow.md](docs/collaboration_workflow.md): GitHub + private-data collaboration model.
- [docs/data_management.md](docs/data_management.md): `AIW_DATA_ROOT` policy and private data handling.
- [docs/artifact_coverage_policy.md](docs/artifact_coverage_policy.md): lane-specific v4.3 artifact coverage rules.
- [docs/coauthor_data_room.md](docs/coauthor_data_room.md): broader full-data handoff contract.
- [docs/t25_execucomp_policy.md](docs/t25_execucomp_policy.md): Test 25 staged ExecuComp policy.
- [docs/extension_playbook.md](docs/extension_playbook.md): coauthor extension lanes from Kuntara comments.
- [docs/private_data_contract.md](docs/private_data_contract.md): coauthor-facing private data mirror contract.
- [docs/coauthor_runbook.md](docs/coauthor_runbook.md): first-day clone, setup, validation, and reproduction commands.
- [docs/releases/v4_3_defense_freeze.md](docs/releases/v4_3_defense_freeze.md): current frozen v4.3 release target.
- [docs/current_state_and_roadmap.md](docs/current_state_and_roadmap.md): current diagnostic and next-phase roadmap.

## Repository Boundary

GitHub tracks code, documentation, manifests, small fixtures, and frozen manuscript assets. Private or licensed data are not tracked in Git. Stage those data through an external private data root:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
```

Do **not** clone this repository inside Dropbox, OneDrive, or another sync folder. Keep Git local and use Dropbox/OneDrive only for the external private data root or a mirrored copy of it.

## Quick Local Check

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
make validate
make path-leak-scan
make import-smoke
make smoke-fixture
make git-hygiene
```

For selected v4.3 reruns after private data are staged:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make audit-artifact-coverage
make reproduce-selected
make TABLE_ID=T16 reproduce-table
make compare-selected-reproduction
```
