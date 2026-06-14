from __future__ import annotations

import csv
from pathlib import Path

from scripts.build_dashboard import build_dashboard
from scripts.build_portfolio_demo import build_portfolio_demo

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


def test_portfolio_demo_contains_showcase_ids_and_product_story(tmp_path: Path) -> None:
    output = tmp_path / "portfolio.html"
    build_portfolio_demo(output)
    text = output.read_text(encoding="utf-8")

    for asset_id in ["T00", "T16", "T17", "T30", "T09"]:
        assert asset_id in text
    for product_id in [
        "final_hybrid_classifier_outputs",
        "patent_match_artifacts",
        "annual_nlp_patent_panel",
        "filing_event_estimation_sample",
    ]:
        assert product_id in text
    for row in _rows("manifests/extension_workbench.csv"):
        assert row["extension_id"] in text
    assert "Portfolio-safe static demo" in text
    assert "The workflow is the product." in text


def test_portfolio_demo_excludes_private_or_local_leakage(tmp_path: Path) -> None:
    output = tmp_path / "portfolio.html"
    build_portfolio_demo(output)
    text = output.read_text(encoding="utf-8")
    forbidden = [
        "/Users/soheilkhodadadi",
        "DataWork/semantic-patterns",
        "Documents/Projects/semantic-patterns",
        "ai-washing-private-data",
        "password",
        "credential",
        "secret",
    ]
    lower = text.lower()
    for pattern in forbidden:
        assert pattern.lower() not in lower
