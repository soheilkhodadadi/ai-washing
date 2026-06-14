from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
PAPER_ROOT = Path(os.environ.get("AIW_PAPER_ROOT", ROOT / "outputs" / "paper_exports")).resolve()
OUTPUT_ROOT = Path(os.environ.get("AIW_OUTPUT_ROOT", ROOT / "outputs" / "reproduced")).resolve()
WORKBENCH_ROOT = ROOT / "outputs" / "workbench"

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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def print_kv(label: str, value: str) -> None:
    print(f"{label}: {value if value else 'not specified'}")


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def table_rows() -> list[dict[str, str]]:
    return read_csv("manifests/paper_table_workbench.csv")


def crosswalk_rows() -> list[dict[str, str]]:
    return read_csv("manifests/table_to_script_crosswalk.csv")


def extension_rows() -> list[dict[str, str]]:
    return read_csv("manifests/extension_workbench.csv")


def resolve_table(table_id: str) -> dict[str, str] | None:
    key = table_id.strip().lower()
    for row in table_rows():
        labels = {row["asset_id"].lower(), row["paper_label"].lower(), row["paper_label"].lower().replace(" ", "")}
        if key in labels:
            return row
    return None


def resolve_crosswalk(asset_id: str) -> dict[str, str] | None:
    key = asset_id.strip().lower()
    for row in crosswalk_rows():
        if row["table_id"].lower() == key:
            return row
    return None


def resolve_extension(extension_id: str) -> dict[str, str] | None:
    key = extension_id.strip().lower().replace("-", "_")
    for row in extension_rows():
        if row["extension_id"].lower() == key:
            return row
    return None


def list_tables() -> int:
    print("asset_id,paper_label,asset_type,paper_section,caption")
    for row in table_rows():
        print(
            ",".join(
                [
                    row["asset_id"],
                    row["paper_label"],
                    row["asset_type"],
                    row["paper_section"],
                    row["caption"].replace(",", ";"),
                ]
            )
        )
    return 0


def table_info(table_id: str) -> int:
    row = resolve_table(table_id)
    if not row:
        valid = ", ".join(r["asset_id"] for r in table_rows())
        print(f"Unknown table or figure: {table_id}", file=sys.stderr)
        print(f"Valid asset IDs: {valid}", file=sys.stderr)
        return 2
    print(f"# {row['paper_label']} ({row['asset_id']})")
    print_kv("Caption", row["caption"])
    print_kv("Paper section", row["paper_section"])
    print_kv("Paper source", row["paper_tex_file"])
    print_kv("Empirical question", row["empirical_question"])
    print_kv("Primary data product", row["primary_data_product"])
    print_kv("Main constructs", row["main_constructs"])
    print_kv("Owning script", row["script_module"])
    print_kv("Rerun command", row["make_command"])
    print_kv("Reference outputs", row["reference_outputs"])
    print_kv("Coauthor use", row["coauthor_use"])
    print_kv("Safe modifications", row["safe_modifications"])
    print_kv("Extension relevance", row["extension_relevance"])
    return 0


def module_to_source_path(module: str) -> Path | None:
    if not module.startswith("semantic_ai_washing."):
        return None
    return ROOT / "src" / Path(*module.split(".")).with_suffix(".py")


def table_script(table_id: str) -> int:
    row = resolve_table(table_id)
    if not row:
        valid = ", ".join(r["asset_id"] for r in table_rows())
        print(f"Unknown table or figure: {table_id}", file=sys.stderr)
        print(f"Valid asset IDs: {valid}", file=sys.stderr)
        return 2
    module = row["script_module"]
    path = module_to_source_path(module)
    print(f"# {row['paper_label']} ({row['asset_id']}) script")
    print_kv("Owning module", module)
    if path:
        status = "present" if path.is_file() else "missing"
        print_kv("Repo source path", rel(path))
        print_kv("Source status", status)
    else:
        print_kv("Repo source path", "not a semantic_ai_washing module")
    print_kv("Rerun command", row["make_command"])
    return 0


def private_data_root() -> Path | None:
    raw = os.environ.get("AIW_DATA_ROOT")
    return Path(raw).expanduser().resolve() if raw else None


def mounted_display(path: Path, root: Path) -> str:
    try:
        return "$AIW_DATA_ROOT/" + str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def format_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{size} B"


def iter_example_files(path: Path, limit: int = 5, count_limit: int = 1000) -> tuple[str, list[Path]]:
    examples: list[Path] = []
    count = 0
    capped = False
    for child in path.rglob("*"):
        if not child.is_file():
            continue
        count += 1
        if len(examples) < limit:
            examples.append(child)
        if count >= count_limit:
            capped = True
            break
    label = f">={count_limit}" if capped else str(count)
    return label, examples


def check_logical_private_paths(value: str) -> None:
    root = private_data_root()
    if not root:
        print("Private data check: AIW_DATA_ROOT is not set.")
        print("Set AIW_DATA_ROOT=/path/to/ai-washing-private-data and rerun this command.")
        return
    for raw in split_paths(value):
        print()
        print(f"Logical path: {raw}")
        if not raw.startswith("data/"):
            print("Status: reference-only or non-private path")
            print("Note: this entry is documented in the catalog but is not resolved through AIW_DATA_ROOT.")
            continue
        mounted = root / raw.removeprefix("data/")
        print(f"Mounted path: {mounted_display(mounted, root)}")
        if mounted.is_file():
            print("Status: present")
            print("Type: file")
            print(f"Suffix: {mounted.suffix or 'none'}")
            print(f"Size: {format_size(mounted.stat().st_size)}")
        elif mounted.is_dir():
            count, examples = iter_example_files(mounted)
            print("Status: present")
            print("Type: directory")
            print(f"File count: {count}")
            if examples:
                print("Example files:")
                for example in examples:
                    print(f"- {mounted_display(example, root)}")
            else:
                print("Example files: none found")
        else:
            print("Status: missing")
            print("Type: not found")


def data_products(product_id: str | None = None, check_files: bool = False) -> int:
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
        if check_files:
            check_logical_private_paths(row["logical_private_path"])
    return 0


def construct_info(construct: str) -> int:
    key = construct.strip().lower().replace("-", "_")
    if key not in CONSTRUCT_DOCS:
        print(f"Unknown construct: {construct}", file=sys.stderr)
        print("Known constructs:", ", ".join(sorted(CONSTRUCT_DOCS)), file=sys.stderr)
        return 2
    rel_path = CONSTRUCT_DOCS[key]
    path = ROOT / rel_path
    print(f"Construct: {key}")
    print(f"Playbook: {rel_path}")
    print()
    text = path.read_text(encoding="utf-8")
    sections = text.split("\n## ")
    preview = sections[0]
    if len(sections) > 1:
        preview += "\n## " + sections[1]
    print(preview.strip())
    return 0


def split_paths(value: str) -> list[str]:
    if not value:
        return []
    parts: list[str] = []
    for chunk in value.replace(";", "|").split("|"):
        item = chunk.strip()
        if item:
            parts.append(item)
    return parts


def safe_copy(src: Path, dest_dir: Path, copied_names: set[str]) -> dict[str, str]:
    src = src.resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)
    name = src.name
    if name in copied_names:
        stem = src.stem
        suffix = src.suffix
        counter = 2
        while f"{stem}_{counter}{suffix}" in copied_names:
            counter += 1
        name = f"{stem}_{counter}{suffix}"
    copied_names.add(name)
    dest = dest_dir / name
    shutil.copy2(src, dest)
    return {"source": rel(src), "bundle_path": rel(dest), "status": "copied"}


def copy_reference_outputs(row: dict[str, str], dest: Path) -> list[dict[str, str]]:
    copied: list[dict[str, str]] = []
    copied_names: set[str] = set()
    for raw in split_paths(row.get("reference_outputs", "")):
        src = ROOT / raw
        if src.is_file():
            copied.append(safe_copy(src, dest, copied_names))
        elif src.is_dir():
            copied.append({"source": raw, "bundle_path": "", "status": "directory_reference_not_copied"})
        else:
            copied.append({"source": raw, "bundle_path": "", "status": "missing_reference"})
    return copied


def candidate_generated_files(crosswalk: dict[str, str] | None) -> list[Path]:
    if not crosswalk:
        return []
    run_id = crosswalk.get("run_id", "")
    test_id = crosswalk.get("test_id", "")
    candidates: list[Path] = []
    roots = [PAPER_ROOT, OUTPUT_ROOT / test_id / run_id]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and (run_id in path.name or test_id in path.name):
                candidates.append(path)
    # Preserve stable order and avoid duplicates from overlapping roots.
    unique: dict[Path, Path] = {}
    for path in candidates:
        unique[path.resolve()] = path
    return sorted(unique.values(), key=lambda p: rel(p))


def copy_generated_outputs(crosswalk: dict[str, str] | None, dest: Path) -> list[dict[str, str]]:
    copied: list[dict[str, str]] = []
    copied_names: set[str] = set()
    for src in candidate_generated_files(crosswalk):
        copied.append(safe_copy(src, dest, copied_names))
    return copied


def rerun_table(asset_id: str) -> int:
    cmd = [sys.executable, str(ROOT / "scripts" / "run_publication_table.py"), asset_id]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    result = subprocess.run(cmd, cwd=ROOT, env=env, check=False)
    return result.returncode


def export_table(table_id: str, rerun: bool = False) -> int:
    row = resolve_table(table_id)
    if not row:
        valid = ", ".join(r["asset_id"] for r in table_rows())
        print(f"Unknown table or figure: {table_id}", file=sys.stderr)
        print(f"Valid asset IDs: {valid}", file=sys.stderr)
        return 2
    asset_id = row["asset_id"]
    if rerun:
        rc = rerun_table(asset_id)
        if rc != 0:
            return rc
    crosswalk = resolve_crosswalk(asset_id)
    bundle = WORKBENCH_ROOT / asset_id
    if bundle.exists():
        shutil.rmtree(bundle)
    (bundle / "reference_outputs").mkdir(parents=True, exist_ok=True)
    (bundle / "generated_outputs").mkdir(parents=True, exist_ok=True)

    reference_copies = copy_reference_outputs(row, bundle / "reference_outputs")
    generated_copies = copy_generated_outputs(crosswalk, bundle / "generated_outputs")
    rerun_command = row["make_command"].replace("AIW_DATA_ROOT=/path/to/ai-washing-private-data ", "")
    open_first = f"""# Open First: {row['paper_label']} ({asset_id})

Use this file as the first stop when reviewing the exported table bundle.

## Recommended First Files

- Table review: open any `.docx`, `.png`, or `.pdf` file in `generated_outputs/` first if present.
- Numeric audit: open the copied `.csv` files in `reference_outputs/` and `generated_outputs/`.
- Manuscript integration: open copied `.tex` files in `reference_outputs/` or `generated_outputs/`.
- Narrative or interpretation notes: open `notes_for_modification.md` and any writer packet or result-note file in `generated_outputs/`.

## Canonical Versus Generated

- `reference_outputs/` contains frozen v4.3 evidence copied from the curated repository where practical.
- Frozen run directories are referenced in `table_info.json` and `input_artifacts.md` but are not copied into this bundle, to keep exports compact.
- `generated_outputs/` contains current rerun artifacts if they already exist or if this bundle was exported with `RERUN=1`.
- Private panels and licensed data are never copied into this bundle; reruns read them through `AIW_DATA_ROOT`.
"""

    write_text(
        bundle / "OPEN_FIRST.md",
        open_first,
    )
    write_text(
        bundle / "README.md",
        f"""# {row['paper_label']} ({asset_id}) Workbench Bundle

This ignored bundle summarizes the paper asset, the owning script, the safe modification path, and the available public evidence files. It does not include private panels or licensed data.

## Open First

- Reviewer/table read: open `.docx`, `.png`, or `.pdf` files in `generated_outputs/` first when present.
- Numeric audit: open `.csv` files in `reference_outputs/` and `generated_outputs/`.
- Manuscript integration: open `.tex` files in `reference_outputs/` or `generated_outputs/`.
- Narrative notes: open `notes_for_modification.md` and any writer packet or result-note file in `generated_outputs/`.

See `OPEN_FIRST.md` for the compact reviewer guide.

## Empirical Question

{row['empirical_question']}

## Owning Script

`{row['script_module']}`

## Standard Rerun

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
{rerun_command}
```

## Bundle Contents

- `input_artifacts.md`: data products and construct inputs to inspect before editing.
- `run_command.sh`: a shell command template for rerunning and refreshing this bundle.
- `reference_outputs/`: copied frozen v4.3 CSV/TeX/PDF evidence files where practical.
- `generated_outputs/`: copied current generated outputs where available.
- `notes_for_modification.md`: safe edits and extension notes.
- `table_info.json`: machine-readable metadata for this bundle.

Frozen run directories are referenced rather than copied, so the bundle stays compact.
""",
    )
    write_text(
        bundle / "input_artifacts.md",
        f"""# Input Artifacts For {asset_id}

- Primary data product: {row['primary_data_product']}
- Main constructs: {row['main_constructs']}
- Paper source: `{row['paper_tex_file']}`
- Private data policy: data-dependent reruns read from `AIW_DATA_ROOT`; private data are not copied into this bundle.

## Reference Outputs Listed In The Workbench

{os.linesep.join(f'- `{item}`' for item in split_paths(row.get('reference_outputs', ''))) or '- None listed.'}
""",
    )
    write_text(
        bundle / "notes_for_modification.md",
        f"""# Notes For Modifying {asset_id}

## Coauthor Use

{row['coauthor_use']}

## Safe Modifications

{row['safe_modifications']}

## Extension Relevance

{row['extension_relevance']}

## Notes

{row['notes']}

Keep the frozen v4.3 reference files as the baseline until a new manuscript release is deliberately promoted.
""",
    )
    write_text(
        bundle / "run_command.sh",
        f"""#!/usr/bin/env bash
set -euo pipefail
: "${{AIW_DATA_ROOT:?Set AIW_DATA_ROOT=/path/to/ai-washing-private-data}}"
make TABLE_ID={asset_id} reproduce-table
make TABLE_ID={asset_id} export-table-workbench
""",
    )
    (bundle / "run_command.sh").chmod(0o755)
    metadata = {
        "asset": row,
        "crosswalk": crosswalk or {},
        "bundle_path": rel(bundle),
        "rerun_executed": rerun,
        "reference_outputs_copied": reference_copies,
        "generated_outputs_copied": generated_copies,
    }
    write_text(bundle / "table_info.json", json.dumps(metadata, indent=2, sort_keys=True))
    print(f"Exported {asset_id} workbench bundle: {rel(bundle)}")
    return 0


def extension_info(extension_id: str) -> int:
    row = resolve_extension(extension_id)
    if not row:
        valid = ", ".join(r["extension_id"] for r in extension_rows())
        print(f"Unknown extension: {extension_id}", file=sys.stderr)
        print(f"Valid extensions: {valid}", file=sys.stderr)
        return 2
    print(f"# {row['title']} ({row['extension_id']})")
    for key in [
        "research_question",
        "current_status",
        "make_command",
        "output_dir",
        "primary_data_product",
        "source_scripts",
        "reference_table_ids",
        "strong_version_data_needed",
        "interpretation_limits",
        "docs",
    ]:
        print_kv(key.replace("_", " ").title(), row.get(key, ""))
    return 0


def list_existing_files(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [rel(p) for p in sorted(path.rglob("*")) if p.is_file()]


def export_extension(extension_id: str, rerun: bool = False) -> int:
    row = resolve_extension(extension_id)
    if not row:
        valid = ", ".join(r["extension_id"] for r in extension_rows())
        print(f"Unknown extension: {extension_id}", file=sys.stderr)
        print(f"Valid extensions: {valid}", file=sys.stderr)
        return 2

    if row["extension_id"] == "washing_pays_proxy":
        if rerun:
            rc = rerun_table("T30")
            if rc != 0:
                return rc
        export_table("T30", rerun=False)

    output_dir = ROOT / row["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    run_command = row["make_command"]
    write_text(
        output_dir / "README.md",
        f"""# {row['title']}

## Research Question

{row['research_question']}

## Current Status

{row['current_status']}

## How To Run

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
{run_command}
```

## Primary Data Product

{row['primary_data_product']}

## Source Scripts

{row['source_scripts']}

## Reference Table IDs

{row['reference_table_ids']}

## Interpretation Limits

{row['interpretation_limits']}

## Strong-Version Data Need

{row['strong_version_data_needed']}

## Documentation

{row['docs']}
""",
    )
    write_text(output_dir / "extension_info.json", json.dumps(row, indent=2, sort_keys=True))
    existing = list_existing_files(output_dir)
    write_text(
        output_dir / "available_outputs.md",
        "# Available Outputs\n\n" + ("\n".join(f"- `{item}`" for item in existing) if existing else "No generated outputs are present yet."),
    )
    print(f"Exported extension bundle: {rel(output_dir)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="AI Washing empirical workbench helper")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-tables", help="List all paper assets in workbench order")

    p_table = sub.add_parser("table-info", help="Show the script, data product, and reference outputs for a paper asset")
    p_table.add_argument("--table-id", required=True, help="Asset ID such as T29, C7, F1, or paper label")

    p_show = sub.add_parser("show-table", help="Alias for table-info")
    p_show.add_argument("--table", required=True, help="Asset ID such as T29, C7, F1, or paper label")

    p_script = sub.add_parser("table-script", help="Show the owning source file for a paper asset")
    p_script.add_argument("--table", required=True, help="Asset ID such as T30")

    p_export = sub.add_parser("export-table", help="Export an ignored coauthor workbench bundle for one table or figure")
    p_export.add_argument("--table", required=True, help="Asset ID such as T30")
    p_export.add_argument("--rerun", action="store_true", help="Run the existing publication-table command before exporting")

    p_data = sub.add_parser("data-products", help="List data products or show one product")
    p_data.add_argument("--product-id", help="Optional product ID")
    p_data.add_argument("--check-files", action="store_true", help="Check mounted AIW_DATA_ROOT paths for this product")

    p_construct = sub.add_parser("construct-info", help="Show the playbook for a construct")
    p_construct.add_argument("--construct", required=True, help="Construct alias such as patent_mismatch or crsp_compustat")

    p_ext = sub.add_parser("extension-info", help="Show a registered extension lane")
    p_ext.add_argument("--extension", required=True, help="Extension ID such as builder_hides")

    p_export_ext = sub.add_parser("export-extension", help="Export or refresh an ignored extension workbench bundle")
    p_export_ext.add_argument("--extension", required=True, help="Extension ID such as washing_pays_proxy")
    p_export_ext.add_argument("--rerun", action="store_true", help="Run the backing existing command before exporting where applicable")

    args = parser.parse_args()
    if args.command == "list-tables":
        return list_tables()
    if args.command == "table-info":
        return table_info(args.table_id)
    if args.command == "show-table":
        return table_info(args.table)
    if args.command == "table-script":
        return table_script(args.table)
    if args.command == "export-table":
        return export_table(args.table, args.rerun)
    if args.command == "data-products":
        return data_products(args.product_id, args.check_files)
    if args.command == "construct-info":
        return construct_info(args.construct)
    if args.command == "extension-info":
        return extension_info(args.extension)
    if args.command == "export-extension":
        return export_extension(args.extension, args.rerun)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
