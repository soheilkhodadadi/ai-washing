from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO_DEMO = ROOT / "outputs" / "portfolio_demo" / "index.html"
FORBIDDEN = [
    "/Users/soheilkhodadadi",
    "DataWork/semantic-patterns",
    "Documents/Projects/semantic-patterns",
    "ai-washing-private-data",
    "password",
    "credential",
    "secret",
]
REQUIRED_TEXT = [
    "Portfolio-safe static demo",
    "Main Table 7",
    "final_hybrid_classifier_outputs",
    "patent_match_artifacts",
    "Builder Hides",
    "make portfolio-demo-check",
]


def read_csv(rel: str) -> list[dict[str, str]]:
    with (ROOT / rel).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    if not PORTFOLIO_DEMO.is_file():
        print(f"Portfolio demo not found: {PORTFOLIO_DEMO.relative_to(ROOT)}", file=sys.stderr)
        return 2
    text = PORTFOLIO_DEMO.read_text(encoding="utf-8")
    lower = text.lower()
    errors: list[str] = []
    for pattern in FORBIDDEN:
        if pattern.lower() in lower:
            errors.append(f"forbidden pattern present: {pattern}")
    for phrase in REQUIRED_TEXT:
        if phrase not in text:
            errors.append(f"missing required phrase: {phrase}")
    for row in read_csv("manifests/extension_workbench.csv"):
        if row["extension_id"] not in text:
            errors.append(f"missing extension: {row['extension_id']}")
    for product_id in [
        "final_hybrid_classifier_outputs",
        "patent_match_artifacts",
        "annual_nlp_patent_panel",
        "filing_event_estimation_sample",
    ]:
        if product_id not in text:
            errors.append(f"missing data product: {product_id}")
    for asset_id in ["T00", "T16", "T17", "T30", "T09"]:
        if asset_id not in text:
            errors.append(f"missing showcase asset: {asset_id}")
    if errors:
        print("AI Washing portfolio demo check failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("AI Washing portfolio demo check passed")
    print(f"- portfolio_demo: {PORTFOLIO_DEMO.relative_to(ROOT)}")
    print("- mode: static, non-executing, portfolio-safe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
