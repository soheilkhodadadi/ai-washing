# Package Surface Audit

This report separates the coauthor workstation surface from a future journal replication archive surface.

## Severity Counts

- `info`: 325
- `material_needs_review`: 15
- `ok`: 207

## Verdict

No stop-the-line tracked package-surface leakage was found.

## Journal-Archive Exclusions To Remember

- `Dockerfile`: modified/staged worktree entry; should be intentional before sharing (material_needs_review)
- `Makefile`: modified/staged worktree entry; should be intentional before sharing (material_needs_review)
- `README.md`: modified/staged worktree entry; should be intentional before sharing (material_needs_review)
- `README_START_HERE.md`: modified/staged worktree entry; should be intentional before sharing (material_needs_review)
- `docs/coauthor_quickstart.md`: modified/staged worktree entry; should be intentional before sharing (material_needs_review)
- `docs/coauthor_runbook.md`: modified/staged worktree entry; should be intentional before sharing (material_needs_review)
- `docs/index.md`: modified/staged worktree entry; should be intentional before sharing (material_needs_review)
- `docs/replication_audit_report.md`: modified/staged worktree entry; should be intentional before sharing (material_needs_review)
- `scripts/doctor.py`: modified/staged worktree entry; should be intentional before sharing (material_needs_review)
- `.dockerignore`: untracked file would be missed by Git archive; review before zipping a raw folder (material_needs_review)
- `docker-compose.yml`: untracked file would be missed by Git archive; review before zipping a raw folder (material_needs_review)
- `docs/docker_quickstart.md`: untracked file would be missed by Git archive; review before zipping a raw folder (material_needs_review)
- `docs/share_readiness_report.md`: untracked file would be missed by Git archive; review before zipping a raw folder (material_needs_review)
- `reports/share_readiness.csv`: untracked file would be missed by Git archive; review before zipping a raw folder (material_needs_review)
- `scripts/share_readiness.py`: untracked file would be missed by Git archive; review before zipping a raw folder (material_needs_review)
