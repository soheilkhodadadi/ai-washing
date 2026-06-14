from __future__ import annotations

import csv
from pathlib import Path

from scripts.build_dashboard import build_dashboard

ROOT = Path(__file__).resolve().parents[1]


def _rows(rel: str) -> list[dict[str, str]]:
    with (ROOT / rel).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_static_dashboard_contains_manifest_ids(tmp_path: Path) -> None:
    output = tmp_path / "dashboard.html"
    build_dashboard(output)
    text = output.read_text(encoding="utf-8")
    for row in _rows("manifests/paper_table_workbench.csv"):
        assert row["asset_id"] in text
    for row in _rows("manifests/data_product_catalog.csv"):
        assert row["product_id"] in text
    for row in _rows("manifests/extension_workbench.csv"):
        assert row["extension_id"] in text


def test_static_dashboard_excludes_local_or_private_leakage(tmp_path: Path) -> None:
    output = tmp_path / "dashboard.html"
    build_dashboard(output)
    text = output.read_text(encoding="utf-8")
    forbidden = [
        "/Users/soheilkhodadadi",
        "DataWork/semantic-patterns",
        "Documents/Projects/semantic-patterns",
        "password",
        "credential",
        "secret",
    ]
    lower = text.lower()
    for pattern in forbidden:
        assert pattern.lower() not in lower
