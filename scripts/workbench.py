from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

CONSTRUCT_DOCS = {
    "ai_disclosure": "docs/construct_playbooks/ai_disclosure_and_classifier_constructs.md",
    "classifier": "docs/construct_playbooks/ai_disclosure_and_classifier_constructs.md",
    "patent_mismatch": "docs/construct_playbooks/patent_mismatch_construct.md",
    "patent_matching": "docs/construct_playbooks/patent_matching_and_company_identity.md",
    "company_identity": "docs/construct_playbooks/patent_matching_and_company_identity.md",
    "crsp_compustat": "docs/construct_playbooks/crsp_compustat_linkage_and_market_return_tests.md",
    "market_returns": "docs/construct_playbooks/crsp_compustat_linkage_and_market_return_tests.md",
    "capital_raising": "docs/construct_playbooks/capital_raising_proxy.md",
    "execucomp": "docs/construct_playbooks/execucomp_incentives.md",
    "sec_scrutiny": "docs/construct_playbooks/sec_scrutiny_enforcement_timing.md",
    "enforcement": "docs/construct_playbooks/sec_scrutiny_enforcement_timing.md",
}


def read_csv(rel: str) -> list[dict[str, str]]:
    path = ROOT / rel
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def print_kv(label: str, value: str) -> None:
    print(f"{label}: {value if value else 'not specified'}")


def table_info(table_id: str) -> int:
    table_id = table_id.strip()
    rows = read_csv("manifests/paper_table_workbench.csv")
    matches = [row for row in rows if row["asset_id"].lower() == table_id.lower() or row["paper_label"].lower() == table_id.lower()]
    if not matches:
        valid = ", ".join(row["asset_id"] for row in rows)
        print(f"Unknown table or figure: {table_id}", file=sys.stderr)
        print(f"Valid asset IDs: {valid}", file=sys.stderr)
        return 2
    row = matches[0]
    print(f"# {row['paper_label']} ({row['asset_id']})")
    print_kv("Caption", row["caption"])
    print_kv("Paper source", row["paper_tex_file"])
    print_kv("Empirical question", row["empirical_question"])
    print_kv("Primary data product", row["primary_data_product"])
    print_kv("Main constructs", row["main_constructs"])
    print_kv("Owning script", row["script_module"])
    print_kv("Rerun command", row["make_command"])
    print_kv("Reference outputs", row["reference_outputs"])
    print_kv("Safe modifications", row["safe_modifications"])
    print_kv("Extension relevance", row["extension_relevance"])
    return 0


def data_products(product_id: str | None = None) -> int:
    rows = read_csv("manifests/data_product_catalog.csv")
    if product_id:
        rows = [row for row in rows if row["product_id"].lower() == product_id.lower()]
        if not rows:
            print(f"Unknown data product: {product_id}", file=sys.stderr)
            return 2
    for i, row in enumerate(rows):
        if i:
            print()
        print(f"# {row['product_id']}")
        print_kv("Purpose", row["purpose"])
        print_kv("Logical private path", row["logical_private_path"])
        print_kv("Coverage", row["coverage"])
        print_kv("Keys", row["keys"])
        print_kv("Tables using it", row["tables_using_it"])
        print_kv("Validation scripts", row["producing_or_validation_scripts"])
        print_kv("Overwrite rule", row["overwrite_rule"])
    return 0


def construct_info(construct: str) -> int:
    key = construct.strip().lower().replace("-", "_")
    if key not in CONSTRUCT_DOCS:
        print(f"Unknown construct: {construct}", file=sys.stderr)
        print("Known constructs:", ", ".join(sorted(CONSTRUCT_DOCS)), file=sys.stderr)
        return 2
    rel = CONSTRUCT_DOCS[key]
    path = ROOT / rel
    print(f"Construct: {key}")
    print(f"Playbook: {rel}")
    print()
    text = path.read_text(encoding="utf-8")
    # Print the first two sections as a compact terminal preview.
    sections = text.split("\n## ")
    preview = sections[0]
    if len(sections) > 1:
        preview += "\n## " + sections[1]
    print(preview.strip())
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only AI Washing empirical workbench navigator")
    sub = parser.add_subparsers(dest="command", required=True)

    p_table = sub.add_parser("table-info", help="Show the script, data product, and reference outputs for a paper asset")
    p_table.add_argument("--table-id", required=True, help="Asset ID such as T29, C7, F1, or paper label")

    p_data = sub.add_parser("data-products", help="List data products or show one product")
    p_data.add_argument("--product-id", help="Optional product ID")

    p_construct = sub.add_parser("construct-info", help="Show the playbook for a construct")
    p_construct.add_argument("--construct", required=True, help="Construct alias such as patent_mismatch or crsp_compustat")

    args = parser.parse_args()
    if args.command == "table-info":
        return table_info(args.table_id)
    if args.command == "data-products":
        return data_products(args.product_id)
    if args.command == "construct-info":
        return construct_info(args.construct)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
