from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "outputs" / "dashboard" / "index.html"
FORBIDDEN = [
    "/Users/soheilkhodadadi",
    "DataWork/semantic-patterns",
    "Documents/Projects/semantic-patterns",
    "password",
    "credential",
    "secret",
]


def read_csv(rel: str) -> list[dict[str, str]]:
    with (ROOT / rel).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    if not DASHBOARD.is_file():
        print(f"Dashboard not found: {DASHBOARD.relative_to(ROOT)}", file=sys.stderr)
        return 2
    text = DASHBOARD.read_text(encoding="utf-8")
    lower = text.lower()
    errors: list[str] = []
    for pattern in FORBIDDEN:
        if pattern.lower() in lower:
            errors.append(f"forbidden pattern present: {pattern}")
    for row in read_csv("manifests/paper_table_workbench.csv"):
        if row["asset_id"] not in text:
            errors.append(f"missing paper asset: {row['asset_id']}")
    for row in read_csv("manifests/data_product_catalog.csv"):
        if row["product_id"] not in text:
            errors.append(f"missing data product: {row['product_id']}")
    for row in read_csv("manifests/extension_workbench.csv"):
        if row["extension_id"] not in text:
            errors.append(f"missing extension: {row['extension_id']}")
    if errors:
        print("AI Washing dashboard check failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("AI Washing dashboard check passed")
    print(f"- dashboard: {DASHBOARD.relative_to(ROOT)}")
    print(f"- paper assets: {len(read_csv('manifests/paper_table_workbench.csv'))}")
    print(f"- data products: {len(read_csv('manifests/data_product_catalog.csv'))}")
    print(f"- extensions: {len(read_csv('manifests/extension_workbench.csv'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
