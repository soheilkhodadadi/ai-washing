from __future__ import annotations

import argparse
import csv
import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None  # type: ignore[assignment]

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
DATA_ROOT = Path(os.environ.get("AIW_DATA_ROOT", ROOT / "data")).resolve()
MANIFEST = ROOT / "manifests" / "artifact_provenance_audit.csv"

YEAR_COLUMNS = ("year", "source_year", "filing_year")
DATE_COLUMNS = ("date", "datadate", "filing_date", "trade_date")


@dataclass(frozen=True)
class ObservedCoverage:
    exists: bool
    kind: str
    file_count: int
    size_bytes: int
    row_count: int | None
    column_count: int | None
    year_min: str
    year_max: str
    date_min: str
    date_max: str
    columns: str
    checksum: str


def runtime_path(logical_path: str, data_root: Path) -> Path:
    path = Path(logical_path)
    if path.parts and path.parts[0] == "data":
        path = Path(*path.parts[1:])
    return data_root / path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_table(path: Path) -> Any:
    if pd is None:
        raise RuntimeError("pandas is required for artifact coverage audit")
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix == ".csv":
        return pd.read_csv(path, low_memory=False)
    return None


def _merge_min_max(current_min: Any, current_max: Any, values: Any) -> tuple[Any, Any]:
    if values is None or len(values) == 0:
        return current_min, current_max
    vmin = values.min()
    vmax = values.max()
    if current_min is None or vmin < current_min:
        current_min = vmin
    if current_max is None or vmax > current_max:
        current_max = vmax
    return current_min, current_max


def inspect_path(path: Path, include_hash: bool) -> ObservedCoverage:
    if not path.exists():
        return ObservedCoverage(False, "missing", 0, 0, None, None, "", "", "", "", "", "")

    files = [path] if path.is_file() else sorted(p for p in path.rglob("*") if p.is_file() and p.name != ".DS_Store")
    size_bytes = sum(p.stat().st_size for p in files)
    row_count = 0
    column_count: int | None = None
    year_min = year_max = date_min = date_max = None
    first_columns: list[str] = []
    hash_parts: list[str] = []

    for file_path in files:
        suffix = file_path.suffix.lower()
        if suffix not in {".parquet", ".csv"}:
            if include_hash and file_path.is_file() and len(files) == 1:
                hash_parts.append(sha256(file_path))
            continue
        try:
            df = _read_table(file_path)
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"Could not inspect {file_path}: {exc}") from exc
        if df is None:
            continue
        row_count += len(df)
        column_count = len(df.columns) if column_count is None else max(column_count, len(df.columns))
        if not first_columns:
            first_columns = [str(c) for c in df.columns[:60]]
        for col in YEAR_COLUMNS:
            if col in df.columns:
                vals = df[col].dropna()
                year_min, year_max = _merge_min_max(year_min, year_max, vals)
                break
        for col in DATE_COLUMNS:
            if col in df.columns:
                vals = df[col].dropna()
                date_min, date_max = _merge_min_max(date_min, date_max, vals)
                break
        if include_hash and file_path.is_file():
            hash_parts.append(sha256(file_path))

    checksum = ""
    if include_hash:
        if len(files) == 1 and hash_parts:
            checksum = hash_parts[0]
        elif hash_parts:
            checksum = hashlib.sha256("\n".join(sorted(hash_parts)).encode()).hexdigest()

    return ObservedCoverage(
        True,
        "file" if path.is_file() else "directory",
        len(files),
        size_bytes,
        row_count if row_count else None,
        column_count,
        "" if year_min is None else str(int(year_min)) if str(year_min).replace(".", "", 1).isdigit() else str(year_min),
        "" if year_max is None else str(int(year_max)) if str(year_max).replace(".", "", 1).isdigit() else str(year_max),
        "" if date_min is None else str(date_min),
        "" if date_max is None else str(date_max),
        ";".join(first_columns),
        checksum,
    )


def compare_expected(row: dict[str, str], obs: ObservedCoverage) -> tuple[str, list[str]]:
    if row["promotion_decision"] in {"defer", "exclude"}:
        return "not_promoted", []
    failures: list[str] = []
    if not obs.exists:
        failures.append("missing_runtime_path")
    checks = [
        ("expected_year_min", obs.year_min),
        ("expected_year_max", obs.year_max),
        ("expected_date_min", obs.date_min),
        ("expected_date_max", obs.date_max),
        ("expected_row_count", "" if obs.row_count is None else str(obs.row_count)),
        ("expected_file_count", str(obs.file_count)),
    ]
    for field, actual in checks:
        expected = row.get(field, "").strip()
        if expected and str(actual) != expected:
            failures.append(f"{field} expected={expected} actual={actual}")
    return ("coverage_fail" if failures else "coverage_pass"), failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit v4.3 artifact provenance and lane-specific coverage.")
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--data-root", type=Path, default=DATA_ROOT)
    parser.add_argument("--report-csv", type=Path)
    parser.add_argument("--hash", action="store_true", help="Compute file hashes; slower on large artifacts.")
    args = parser.parse_args()

    rows = list(csv.DictReader(args.manifest.open(newline="")))
    results: list[dict[str, str]] = []
    counts: dict[str, int] = {}
    failed = False
    data_root = args.data_root.resolve()

    for row in rows:
        logical_path = row["private_logical_path"]
        path = runtime_path(logical_path, data_root) if logical_path else Path()
        obs = inspect_path(path, include_hash=args.hash) if logical_path else ObservedCoverage(False, "not_applicable", 0, 0, None, None, "", "", "", "", "", "")
        status, failures = compare_expected(row, obs)
        counts[status] = counts.get(status, 0) + 1
        if status == "coverage_fail" and row.get("required_gate", "").lower() == "yes":
            failed = True
        results.append(
            {
                **row,
                "runtime_path": str(path) if logical_path else "",
                "observed_exists": str(obs.exists),
                "observed_kind": obs.kind,
                "observed_file_count": str(obs.file_count),
                "observed_size_bytes": str(obs.size_bytes),
                "observed_row_count": "" if obs.row_count is None else str(obs.row_count),
                "observed_column_count": "" if obs.column_count is None else str(obs.column_count),
                "observed_year_min": obs.year_min,
                "observed_year_max": obs.year_max,
                "observed_date_min": obs.date_min,
                "observed_date_max": obs.date_max,
                "observed_columns": obs.columns,
                "observed_checksum": obs.checksum,
                "coverage_status": status,
                "coverage_failures": " | ".join(failures),
            }
        )

    print("AI Washing artifact provenance coverage audit")
    print(f"- manifest: {args.manifest}")
    print(f"- AIW_DATA_ROOT: {data_root}")
    print(f"- rows: {len(rows)}")
    for key in sorted(counts):
        print(f"- {key}: {counts[key]}")

    for item in results:
        if item["coverage_status"] == "coverage_fail":
            print(f"\ncoverage_fail: {item['artifact_id']}")
            print(f"- lane: {item['lane']}")
            print(f"- path: {item['private_logical_path']}")
            print(f"- failures: {item['coverage_failures']}")

    if args.report_csv:
        args.report_csv.parent.mkdir(parents=True, exist_ok=True)
        fields = list(results[0].keys()) if results else []
        with args.report_csv.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(results)
        print(f"\nWrote report: {args.report_csv}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
