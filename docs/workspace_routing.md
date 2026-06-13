# Workspace Routing Note

This Codex thread may remain a global, memory-rich session that opens from another workspace, including the older `semantic-patterns` repository. That is acceptable as long as AI Washing work is routed explicitly.

For AI Washing, the canonical project root is the local clone of this repository:

```text
/path/to/ai-washing
```

When running commands from a multi-project Codex session, use that directory as the command working directory. Do not infer the active project from the UI sidebar or shell prompt alone.

Recommended shell guard:

```bash
cd /path/to/ai-washing
git status --short --branch
```

The older `semantic-patterns` repository is provenance only. New AI Washing code, manifests, runbooks, and reproduction ledgers belong in this canonical repository.
