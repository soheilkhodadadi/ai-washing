from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
import sys
from typing import Any

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None  # type: ignore[assignment]

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
DATA_ROOT = Path(os.environ.get("AIW_DATA_ROOT", ROOT / "data")).resolve()
MANIFEST = ROOT / "manifests" / "patent_data_manifest.csv"
FAIL_ROLES = {"required_extension", "required_reproduction", "raw_source"}


def runtime_path(logical_path: str, data_root: Path) -> Path:
    path = Path(logical_path)
    if path.parts and path.parts[0] == "data":
        path = Path(*path.parts[1:])
    return data_root / path


def parse_int(value: str) -> int | None:
    value = str(value or "").strip()
    return int(value) if value else None


def split_columns(value: str) -> list[str]:
    return [item.strip() for item in str(value or "").split(";") if item.strip()]


def inspect_csv(path: Path, row: dict[str, str]) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    info: dict[str, Any] = {"rows": "", "year_min": "", "year_max": ""}
    if pd is None:
        return ["pandas is required for CSV patent validation"], info
    try:
        df = pd.read_csv(path)
    except Exception as exc:  # noqa: BLE001
        return [f"could not read CSV: {exc}"], info

    info["rows"] = len(df)
    expected_rows = parse_int(row.get("expected_rows", ""))
    if expected_rows is not None and len(df) != expected_rows:
        failures.append(f"row count {len(df)} != expected {expected_rows}")

    required_columns = split_columns(row.get("required_columns", ""))
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        failures.append(f"missing columns: {missing_columns}")

    year_column = row.get("year_column", "").strip()
    if year_column:
        if year_column not in df.columns:
            failures.append(f"year column missing: {year_column}")
        elif not df.empty:
            year_min = int(df[year_column].min())
            year_max = int(df[year_column].max())
            info["year_min"] = year_min
            info["year_max"] = year_max
            expected_min = parse_int(row.get("expected_year_min", ""))
            expected_max = parse_int(row.get("expected_year_max", ""))
            if expected_min is not None and year_min != expected_min:
                failures.append(f"year min {year_min} != expected {expected_min}")
            if expected_max is not None and year_max != expected_max:
                failures.append(f"year max {year_max} != expected {expected_max}")
    return failures, info


def inspect_artifact(path: Path, row: dict[str, str]) -> tuple[str, list[str], dict[str, Any]]:
    if not path.exists():
        role = row.get("role", "")
        status = "missing_required" if role in FAIL_ROLES else "missing_support"
        return status, ["path does not exist"], {}
    expected_format = row.get("expected_format", "")
    if expected_format == "csv":
        failures, info = inspect_csv(path, row)
    else:
        failures, info = [], {"size_bytes": path.stat().st_size if path.is_file() else ""}
    status = "failed" if failures else "present"
    return status, failures, info


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate staged AI Washing patent data-room artifacts.")
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--data-root", type=Path, default=DATA_ROOT)
    parser.add_argument("--report-csv", type=Path)
    args = parser.parse_args()

    rows = list(csv.DictReader(args.manifest.open(newline="")))
    results: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    failures_total = 0
    for row in rows:
        path = runtime_path(row["logical_path"], args.data_root.resolve())
        status, failures, info = inspect_artifact(path, row)
        counts[status] = counts.get(status, 0) + 1
        if status in {"failed", "missing_required"}:
            failures_total += 1
        result = {
            **row,
            "runtime_path": str(path),
            "validation_status": status,
            "failures": " | ".join(failures),
            **info,
        }
        results.append(result)

    print("AI Washing patent data check")
    print(f"- manifest: {args.manifest}")
    print(f"- AIW_DATA_ROOT: {args.data_root.resolve()}")
    print(f"- manifest rows: {len(rows)}")
    for key in sorted(counts):
        print(f"- {key}: {counts[key]}")

    for result in results:
        if result["validation_status"] in {"present", "missing_support"}:
            continue
        print(f"\n{result['validation_status']}: {result['artifact_id']}")
        print(f"- path: {result['runtime_path']}")
        print(f"- failures: {result['failures']}")

    if args.report_csv:
        args.report_csv.parent.mkdir(parents=True, exist_ok=True)
        fieldnames: list[str] = []
        for result in results:
            for key in result:
                if key not in fieldnames:
                    fieldnames.append(key)
        with args.report_csv.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            writer.writerows(results)
        print(f"\nWrote report: {args.report_csv}")

    return 1 if failures_total else 0


if __name__ == "__main__":
    sys.exit(main())
