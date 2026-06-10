from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
import sys
from typing import Any

try:
    import pyarrow.parquet as pq
except ImportError:  # pragma: no cover - surfaced in CLI output
    pq = None  # type: ignore[assignment]

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
DATA_ROOT = Path(os.environ.get("AIW_DATA_ROOT", ROOT / "data")).resolve()
MANIFEST = ROOT / "manifests" / "sec_source_manifest.csv"


def runtime_path(logical_path: str, data_root: Path) -> Path:
    path = Path(logical_path)
    if path.parts and path.parts[0] == "data":
        path = Path(*path.parts[1:])
    return data_root / path


def parse_int(value: str) -> int | None:
    value = str(value or "").strip()
    return int(value) if value else None


def parse_bool(value: str) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}


def required_urls(value: str) -> list[str]:
    return [item.strip() for item in str(value or "").split(";") if item.strip()]


def years_from_path(path: Path) -> list[int]:
    years: list[int] = []
    for part in path.parts:
        if part.startswith("year="):
            value = part.split("=", 1)[1]
            if value.isdigit():
                years.append(int(value))
    return years


def inspect_txt_directory(path: Path) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    files = sorted(p for p in path.rglob("*.txt") if p.is_file()) if path.exists() else []
    empty = [str(p.name) for p in files if p.stat().st_size == 0]
    if empty:
        failures.append(f"empty text files: {empty[:5]}")
    return failures, {"files": len(files), "rows": "", "year_min": "", "year_max": ""}


def inspect_markdown(path: Path, row: dict[str, str]) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    text = path.read_text(encoding="utf-8")
    for url in required_urls(row.get("required_urls", "")):
        if url not in text:
            failures.append(f"missing required URL: {url}")
    return failures, {"files": 1, "rows": "", "year_min": "", "year_max": ""}


def inspect_parquet_directory(path: Path) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    if pq is None:
        return ["pyarrow is required for parquet directory validation"], {"files": "", "rows": "", "year_min": "", "year_max": ""}
    files = sorted(p for p in path.rglob("*.parquet") if p.is_file()) if path.exists() else []
    rows = 0
    years: list[int] = []
    for file_path in files:
        try:
            rows += pq.ParquetFile(file_path).metadata.num_rows
        except Exception as exc:  # noqa: BLE001
            failures.append(f"could not read parquet metadata for {file_path.name}: {exc}")
        years.extend(years_from_path(file_path))
    return failures, {
        "files": len(files),
        "rows": rows if files else "",
        "year_min": min(years) if years else "",
        "year_max": max(years) if years else "",
    }


def inspect_artifact(path: Path, row: dict[str, str]) -> tuple[str, list[str], dict[str, Any]]:
    required = parse_bool(row.get("required", ""))
    if not path.exists():
        return ("missing_required" if required else "missing_optional"), ["path does not exist"], {}

    expected_format = row.get("expected_format", "").strip()
    if expected_format == "txt_directory":
        failures, info = inspect_txt_directory(path)
    elif expected_format == "markdown":
        failures, info = inspect_markdown(path, row)
    elif expected_format == "parquet_directory":
        failures, info = inspect_parquet_directory(path)
    else:
        failures, info = [f"unsupported expected_format: {expected_format}"], {}

    expected_files = parse_int(row.get("expected_files", ""))
    if expected_files is not None and info.get("files") != expected_files:
        failures.append(f"file count {info.get('files')} != expected {expected_files}")

    expected_rows = parse_int(row.get("expected_rows", ""))
    if expected_rows is not None and info.get("rows") != expected_rows:
        failures.append(f"row count {info.get('rows')} != expected {expected_rows}")

    expected_year_min = parse_int(row.get("expected_year_min", ""))
    if expected_year_min is not None and info.get("year_min") != expected_year_min:
        failures.append(f"year min {info.get('year_min')} != expected {expected_year_min}")

    expected_year_max = parse_int(row.get("expected_year_max", ""))
    if expected_year_max is not None and info.get("year_max") != expected_year_max:
        failures.append(f"year max {info.get('year_max')} != expected {expected_year_max}")

    if failures:
        return ("failed" if required else "optional_failed"), failures, info
    return "present", [], info


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the SEC raw-source/sample policy surface.")
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--data-root", type=Path, default=DATA_ROOT)
    parser.add_argument("--report-csv", type=Path)
    args = parser.parse_args()

    rows = list(csv.DictReader(args.manifest.open(newline="")))
    results: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    failures_total = 0
    data_root = args.data_root.resolve()

    for row in rows:
        path = runtime_path(row["logical_path"], data_root)
        status, failures, info = inspect_artifact(path, row)
        counts[status] = counts.get(status, 0) + 1
        if status in {"missing_required", "failed"}:
            failures_total += 1
        results.append(
            {
                **row,
                "runtime_path": str(path),
                "validation_status": status,
                "failures": " | ".join(failures),
                **info,
            }
        )

    print("AI Washing SEC source policy check")
    print(f"- manifest: {args.manifest}")
    print(f"- AIW_DATA_ROOT: {data_root}")
    print(f"- manifest rows: {len(rows)}")
    for key in sorted(counts):
        print(f"- {key}: {counts[key]}")

    for result in results:
        if result["validation_status"] == "present":
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
