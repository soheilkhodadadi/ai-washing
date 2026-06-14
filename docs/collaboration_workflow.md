# Collaboration Workflow

This repository is designed for coauthor collaboration through GitHub while keeping private data outside Git.

## Recommended Setup For Each Collaborator

1. Clone the private GitHub repository into a normal local development folder.
2. Create a local `.venv` and install the package with `python -m pip install -e .`.
3. Obtain the private data root separately through Dropbox or a local mirror.
4. Set `AIW_DATA_ROOT` to that external folder.
5. Run the validation commands in `README_START_HERE.md`.

## What Goes Where

- GitHub: scripts, docs, manifests, fixtures, frozen manuscript assets, and reproducibility instructions.
- External private data root: WRDS/CRSP inputs, derived panels, label files, generated private evidence, and other restricted artifacts.
- Local ignored outputs: table reruns, paper exports, fixture output, logs, and exploratory scratch files.

## Branching

- `main` is for validated states only.
- Use short-lived branches for risky table rewrites, new data modules, or journal-response work.
- Keep v4.3 release evidence immutable unless a later release is explicitly promoted.

## Avoiding Sync Conflicts

Do not clone this Git repository inside Dropbox or another sync folder. Sync tools can corrupt `.git` metadata or create conflicting copies. Instead, keep the repository local and point `AIW_DATA_ROOT` to a Dropbox-synced data folder or to a local mirror of that folder.
