from __future__ import annotations

import argparse
import csv
import hashlib
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
DATA_ROOT = Path(os.environ.get("AIW_DATA_ROOT", ROOT / "data")).resolve()
PAPER_ROOT = Path(os.environ.get("AIW_PAPER_ROOT", ROOT / "outputs" / "paper_exports")).resolve()
CROSSWALK = ROOT / "manifests" / "table_to_script_crosswalk.csv"
DEPS = ROOT / "manifests" / "data_dependency_manifest.csv"
DEFAULT_STATUS_CSV = ROOT / "docs" / "full_reproduction_status.csv"
DEFAULT_STATUS_MD = ROOT / "docs" / "full_reproduction_status.md"

SELECTED = {"T00", "T16", "T17", "T09", "T30"}
MAIN_EXTRA = {"T20", "T29", "T25"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def data_runtime_path(manifest_path: str) -> Path:
    path = Path(manifest_path)
    if path.parts and path.parts[0] == "data":
        path = Path(*path.parts[1:])
    return DATA_ROOT / path


def table_filter(rows: list[dict[str, str]], batch: str, table_ids: set[str] | None, include_figures: bool) -> list[dict[str, str]]:
    if table_ids:
        selected = [r for r in rows if r["table_id"] in table_ids]
    elif batch == "selected":
        selected = [r for r in rows if r["table_id"] in SELECTED]
    elif batch == "main":
        selected = [r for r in rows if r["table_id"] in (SELECTED | MAIN_EXTRA)]
    elif batch == "remaining-main":
        selected = [r for r in rows if r["table_id"] in MAIN_EXTRA]
    elif batch == "appendix":
        selected = [r for r in rows if r["table_id"].startswith(("A", "B", "C"))]
    elif batch == "all":
        selected = rows[:]
    else:
        raise ValueError(f"unknown batch: {batch}")
    if not include_figures:
        selected = [r for r in selected if r["asset_type"] == "table"]
    return selected


def dependency_status(row: dict[str, str], deps: list[dict[str, str]]) -> tuple[str, str]:
    relevant = [d for d in deps if d["test_id"] == row["test_id"]]
    missing_required: list[str] = []
    missing_support: list[str] = []
    future: list[str] = []
    for dep in relevant:
        path = data_runtime_path(dep["expected_capsule_path"])
        if path.exists():
            continue
        item = f"{dep['dependency_id']}={dep['expected_capsule_path']}"
        if dep["classification"] == "future_extension":
            future.append(item)
        elif dep["classification"] == "support_only":
            missing_support.append(item)
        else:
            missing_required.append(item)
    if missing_required:
        return "blocked_private_input", "; ".join(missing_required)
    if missing_support:
        return "blocked_private_input", "; ".join(missing_support)
    if future:
        return "not_regenerated_by_design", "; ".join(future)
    return "ready", "all required inputs present"


def file_status(reference: Path, reproduced: Path) -> tuple[str, str]:
    if not reference.exists() and not reproduced.exists():
        return "missing_both", "reference and reproduced files are missing"
    if not reference.exists():
        return "missing_reference", str(reference.relative_to(ROOT) if reference.is_relative_to(ROOT) else reference)
    if not reproduced.exists():
        return "missing_reproduced", str(reproduced.relative_to(ROOT) if reproduced.is_relative_to(ROOT) else reproduced)
    ref_hash = sha256(reference)
    repro_hash = sha256(reproduced)
    if ref_hash == repro_hash:
        return "exact_match", ref_hash
    return "content_delta", f"reference={ref_hash}; reproduced={repro_hash}"


def output_paths(row: dict[str, str]) -> tuple[Path, Path, Path, Path]:
    ref_csv = ROOT / row["capsule_generated_csv"] if row["capsule_generated_csv"] else Path()
    ref_tex = ROOT / row["capsule_generated_tex"] if row["capsule_generated_tex"] else Path()
    repro_csv = PAPER_ROOT / "tables" / Path(row["generated_csv"]).name if row["generated_csv"] else Path()
    repro_tex = PAPER_ROOT / "latex" / Path(row["generated_tex"]).name if row["generated_tex"] else Path()
    return ref_csv, ref_tex, repro_csv, repro_tex


def relative(path: Path) -> str:
    if not path:
        return ""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def assess_asset(row: dict[str, str], deps: list[dict[str, str]], dry_run: bool, status_only: bool) -> dict[str, str]:
    dep_status, dep_note = dependency_status(row, deps)
    base = {
        "table_id": row["table_id"],
        "asset_type": row["asset_type"],
        "paper_location": row["paper_location"],
        "test_id": row["test_id"],
        "script_module": row["script_module"],
        "run_id": row["run_id"],
        "priority": row["priority"],
        "crosswalk_match_status": row["match_status"],
        "reproduction_status": "",
        "csv_status": "",
        "tex_status": "",
        "notes": "",
        "reference_csv": "",
        "reproduced_csv": "",
        "reference_tex": "",
        "reproduced_tex": "",
    }

    if row["asset_type"] != "table":
        base["reproduction_status"] = "frozen_asset_only"
        base["notes"] = "Figure is preserved as frozen v4.3 manuscript asset; regeneration is skipped by default."
        return base

    if dep_status != "ready":
        base["reproduction_status"] = dep_status
        base["notes"] = dep_note
        return base

    if dry_run:
        base["reproduction_status"] = "dry_run_ready"
        base["notes"] = "All required inputs are present; no table script was executed."
        return base

    if not status_only:
        cmd = [sys.executable, str(ROOT / "scripts" / "run_publication_table.py"), row["table_id"]]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
        result = subprocess.run(cmd, cwd=ROOT, env=env, check=False)
        if result.returncode != 0:
            base["reproduction_status"] = "run_failed"
            base["notes"] = f"run_publication_table.py exited {result.returncode}"
            return base

    ref_csv, ref_tex, repro_csv, repro_tex = output_paths(row)
    csv_status, csv_note = file_status(ref_csv, repro_csv) if row["generated_csv"] else ("not_applicable", "no CSV target")
    tex_status, tex_note = file_status(ref_tex, repro_tex) if row["generated_tex"] else ("not_applicable", "no generated TeX target")

    base.update(
        {
            "csv_status": csv_status,
            "tex_status": tex_status,
            "reference_csv": relative(ref_csv),
            "reproduced_csv": relative(repro_csv),
            "reference_tex": relative(ref_tex),
            "reproduced_tex": relative(repro_tex),
        }
    )
    if csv_status == "exact_match":
        base["reproduction_status"] = "csv_exact_match"
    elif csv_status == "content_delta":
        base["reproduction_status"] = "content_delta"
    elif csv_status.startswith("missing"):
        base["reproduction_status"] = "blocked_private_input" if status_only else "content_delta"
    else:
        base["reproduction_status"] = csv_status
    base["notes"] = f"csv={csv_status}: {csv_note}; tex={tex_status}: {tex_note}"
    return base


def write_status_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "table_id",
        "asset_type",
        "paper_location",
        "test_id",
        "script_module",
        "run_id",
        "priority",
        "crosswalk_match_status",
        "reproduction_status",
        "csv_status",
        "tex_status",
        "notes",
        "reference_csv",
        "reproduced_csv",
        "reference_tex",
        "reproduced_tex",
    ]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_status_md(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Full Reproduction Status",
        "",
        "This ledger is generated by `scripts/reproduce_assets.py`. It separates generated CSV evidence from manuscript-facing TeX wrappers so numerical reproduction does not get confused with caption, note, or layout differences.",
        "",
        "Allowed statuses: `csv_exact_match`, `format_only_delta`, `content_delta`, `blocked_private_input`, `frozen_asset_only`, `not_regenerated_by_design`, `dry_run_ready`, and `run_failed`.",
        "",
        "| Asset | Type | Test | Priority | Status | CSV | TeX | Notes |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        note = row["notes"].replace("|", "/")
        if len(note) > 180:
            note = note[:177] + "..."
        lines.append(
            f"| {row['table_id']} | {row['asset_type']} | `{row['test_id']}` | {row['priority']} | {row['reproduction_status']} | {row['csv_status']} | {row['tex_status']} | {note} |"
        )
    lines.append("")
    path.write_text("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch dry-run, rerun, or report AI Washing v4.3 table/figure reproduction status.")
    parser.add_argument("--batch", choices=["selected", "main", "remaining-main", "appendix", "all"], default="all")
    parser.add_argument("--tables", help="Comma-separated table IDs. Overrides --batch.")
    parser.add_argument("--include-figures", action="store_true", help="Include figure assets in the status ledger; figures are not regenerated by default.")
    parser.add_argument("--dry-run", action="store_true", help="Check input readiness without executing table scripts.")
    parser.add_argument("--status-only", action="store_true", help="Compare existing outputs without executing table scripts.")
    parser.add_argument("--status-csv", type=Path, default=DEFAULT_STATUS_CSV)
    parser.add_argument("--status-md", type=Path, default=DEFAULT_STATUS_MD)
    args = parser.parse_args()

    crosswalk = read_csv(CROSSWALK)
    deps = read_csv(DEPS)
    table_ids = {item.strip() for item in args.tables.split(",") if item.strip()} if args.tables else None
    selected = table_filter(crosswalk, args.batch, table_ids, args.include_figures)
    if not selected:
        print("No assets selected.", file=sys.stderr)
        return 2

    statuses = [assess_asset(row, deps, dry_run=args.dry_run, status_only=args.status_only) for row in selected]
    write_status_csv(args.status_csv, statuses)
    write_status_md(args.status_md, statuses)

    print(f"Wrote {args.status_csv}")
    print(f"Wrote {args.status_md}")
    counts: dict[str, int] = {}
    for row in statuses:
        counts[row["reproduction_status"]] = counts.get(row["reproduction_status"], 0) + 1
    for key in sorted(counts):
        print(f"- {key}: {counts[key]}")

    failures = [r for r in statuses if r["reproduction_status"] in {"content_delta", "blocked_private_input", "run_failed"}]
    if args.dry_run:
        failures = [r for r in failures if r["reproduction_status"] == "blocked_private_input"]
    return 1 if failures and not args.status_only else 0


if __name__ == "__main__":
    sys.exit(main())
