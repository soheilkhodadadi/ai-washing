from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
import sys
from typing import Any

import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
DATA_ROOT = Path(os.environ.get("AIW_DATA_ROOT", ROOT / "data")).resolve()
MANIFEST = ROOT / "manifests" / "wrds_data_manifest.csv"
FAIL_ROLES = {"required_reproduction", "required_extension", "raw_source"}


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


def read_frame(path: Path, expected_format: str) -> pd.DataFrame | None:
    if expected_format == "parquet":
        return pd.read_parquet(path)
    if expected_format == "csv":
        return pd.read_csv(path)
    return None


def inspect_tabular(path: Path, row: dict[str, str]) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    info: dict[str, Any] = {"rows": "", "date_min": "", "date_max": "", "year_min": "", "year_max": ""}
    expected_format = row.get("expected_format", "")
    try:
        if expected_format == "parquet":
            meta = pq.ParquetFile(path).metadata
            info["rows"] = meta.num_rows
            df = pd.read_parquet(path)
        elif expected_format == "csv":
            df = pd.read_csv(path)
            info["rows"] = len(df)
        else:
            return failures, info
    except Exception as exc:  # noqa: BLE001
        return [f"could not read {expected_format}: {exc}"], info

    expected_rows = parse_int(row.get("expected_rows", ""))
    if expected_rows is not None and len(df) != expected_rows:
        failures.append(f"row count {len(df)} != expected {expected_rows}")

    required_columns = split_columns(row.get("required_columns", ""))
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        failures.append(f"missing columns: {missing_columns}")

    date_column = row.get("date_column", "").strip()
    if date_column:
        if date_column not in df.columns:
            failures.append(f"date column missing: {date_column}")
        elif not df.empty:
            parsed = pd.to_datetime(df[date_column].astype(str), errors="coerce")
            parsed = parsed.dropna()
            if parsed.empty:
                failures.append(f"date column could not be parsed: {date_column}")
            else:
                date_min = parsed.min().date().isoformat()
                date_max = parsed.max().date().isoformat()
                info["date_min"] = date_min
                info["date_max"] = date_max
                expected_min = row.get("expected_date_min", "").strip()
                expected_max = row.get("expected_date_max", "").strip()
                if expected_min and date_min != expected_min:
                    failures.append(f"date min {date_min} != expected {expected_min}")
                if expected_max and date_max != expected_max:
                    failures.append(f"date max {date_max} != expected {expected_max}")

    year_column = row.get("year_column", "").strip()
    if year_column:
        if year_column not in df.columns:
            failures.append(f"year column missing: {year_column}")
        elif not df.empty:
            years = pd.to_numeric(df[year_column], errors="coerce").dropna()
            if years.empty:
                failures.append(f"year column could not be parsed: {year_column}")
            else:
                year_min = int(years.min())
                year_max = int(years.max())
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
    if expected_format in {"csv", "parquet"}:
        failures, info = inspect_tabular(path, row)
    else:
        failures, info = [], {"size_bytes": path.stat().st_size if path.is_file() else ""}
    status = "failed" if failures else "present"
    return status, failures, info


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate staged AI Washing WRDS/CRSP/Compustat data-room artifacts.")
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
        results.append({**row, "runtime_path": str(path), "validation_status": status, "failures": " | ".join(failures), **info})

    print("AI Washing WRDS/market data check")
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
