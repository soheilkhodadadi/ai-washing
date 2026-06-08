from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
DATA_ROOT = Path(os.environ.get("AIW_DATA_ROOT", ROOT / "data")).resolve()
OUTPUT_ROOT = Path(os.environ.get("AIW_OUTPUT_ROOT", ROOT / "outputs" / "reproduced")).resolve()
PAPER_ROOT = Path(os.environ.get("AIW_PAPER_ROOT", ROOT / "outputs" / "paper_exports")).resolve()

ARG_BY_DEP = {
    "annual_panel": "--annual-panel",
    "event_panel": "--event-panel",
    "daily_returns": "--daily-returns",
    "monthly_returns": "--monthly-returns",
    "market_index": "--market-index",
    "market_features": "--market-features",
    "filing_measures": "--filing-measures",
    "label_base": "--label-base",
    "training_pool": "--training-pool",
    "heldout_v4": "--heldout-v4",
    "irr_report": "--irr-report",
    "hybrid_eval": "--hybrid-eval",
    "factor_root": "--factor-root",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one v4.3 publication table with explicit workstation paths.")
    parser.add_argument("table_id", help="Crosswalk table_id, e.g. T00 or T16")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    crosswalk = read_csv(ROOT / "manifests" / "table_to_script_crosswalk.csv")
    deps = read_csv(ROOT / "manifests" / "data_dependency_manifest.csv")
    row = next((r for r in crosswalk if r["table_id"] == args.table_id), None)
    if not row:
        print(f"Unknown table_id: {args.table_id}", file=sys.stderr)
        return 2
    if row["asset_type"] != "table":
        print(f"{args.table_id} is not a table asset.", file=sys.stderr)
        return 2

    dep_rows = [d for d in deps if d["test_id"] == row["test_id"] and d["dependency_id"] in ARG_BY_DEP]
    missing = []
    cmd = [sys.executable, "-m", row["script_module"]]
    for dep in dep_rows:
        path = DATA_ROOT / Path(dep["expected_capsule_path"]).relative_to("data")
        if not path.exists():
            missing.append(f"{dep['dependency_id']} -> {path}")
        cmd.extend([ARG_BY_DEP[dep["dependency_id"]], str(path)])
    run_output = OUTPUT_ROOT / row["test_id"] / row["run_id"]
    cmd.extend(["--test-root", str(OUTPUT_ROOT), "--paper-root", str(PAPER_ROOT), "--run-id", row["run_id"]])

    if missing:
        print("Private/full-rerun inputs are not staged:")
        for item in missing:
            print(f"- {item}")
        print("Stage these files under AIW_DATA_ROOT using the paths in manifests/data_dependency_manifest.csv.")
        print("Command that will run after staging:")
        print(" ".join(cmd))
        return 0 if args.dry_run else 3
    print("Command:")
    print(" ".join(cmd))
    if args.dry_run:
        return 0
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    result = subprocess.run(cmd, cwd=ROOT, env=env, check=False)
    print(f"Output root: {run_output}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
