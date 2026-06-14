from __future__ import annotations

from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
MANIFEST_DIR = ROOT / "manifests"
DOCS_DIR = ROOT / "docs"
OUTPUTS_DIR = ROOT / "outputs"


def repo_relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def repo_link(path: str) -> str:
    return path.strip()
