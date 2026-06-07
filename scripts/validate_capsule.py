from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    failures: list[str] = []
    crosswalk = read_csv(ROOT / "manifests" / "table_to_script_crosswalk.csv")
    inventory = read_csv(ROOT / "manifests" / "v4_3_manuscript_asset_inventory.csv")
    deps = read_csv(ROOT / "manifests" / "data_dependency_manifest.csv")

    table_rows = [r for r in crosswalk if r["asset_type"] == "table"]
    figure_rows = [r for r in crosswalk if r["asset_type"] == "figure"]
    if len(table_rows) != 24:
        failures.append(f"Expected 24 v4.3 table inputs in crosswalk, found {len(table_rows)}")
    if len(figure_rows) != 2:
        failures.append(f"Expected 2 v4.3 figures in crosswalk, found {len(figure_rows)}")

    inv_paths = {r["relative_path"] for r in inventory}
    for row in crosswalk:
        paper_path = row["paper_tex_file"]
        if paper_path not in inv_paths and not Path(ROOT / "paper" / "v4_3_source" / paper_path).exists():
            failures.append(f"Paper asset missing from inventory/source: {row['table_id']} {paper_path}")
        if not row["script_module"]:
            failures.append(f"Missing script module for {row['table_id']}")
        if row["match_status"] not in {"exact_match", "format_only_delta", "content_delta", "unknown"}:
            failures.append(f"Invalid match status for {row['table_id']}: {row['match_status']}")

    # Dependencies may be missing_private_input in Phase 1, but the manifest should not be empty.
    if not deps:
        failures.append("Data dependency manifest is empty")

    if failures:
        print("CAPSULE VALIDATION FAILED")
        for item in failures:
            print(f"- {item}")
        return 1
    print("CAPSULE VALIDATION PASSED")
    print(f"- table assets: {len(table_rows)}")
    print(f"- figures: {len(figure_rows)}")
    print(f"- dependency rows: {len(deps)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
