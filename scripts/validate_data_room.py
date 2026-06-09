from __future__ import annotations

import argparse
import csv
import hashlib
import os
from pathlib import Path
import sys
from typing import Any

try:
    import pandas as pd
except ImportError:  # pragma: no cover - surfaced in CLI output
    pd = None  # type: ignore[assignment]

try:
    import pyarrow.parquet as pq
except ImportError:  # pragma: no cover - surfaced in CLI output
    pq = None  # type: ignore[assignment]

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
DATA_ROOT = Path(os.environ.get("AIW_DATA_ROOT", ROOT / "data")).resolve()
MANIFEST = ROOT / "manifests" / "coauthor_data_room_manifest.csv"
FAIL_ROLES = {"required_reproduction", "required_extension", "raw_source"}
WARN_ROLES = {"support_only"}
DEFERRED_STATUSES = {"deferred_with_reason", "future_extension"}


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


def csv_row_count(path: Path) -> int | None:
    with path.open("rb") as f:
        count = sum(1 for _ in f)
    return max(count - 1, 0) if count else 0


def inspect_path(path: Path, include_hash: bool) -> dict[str, Any]:
    info: dict[str, Any] = {
        "exists": path.exists(),
        "kind": "missing",
        "size_bytes": "",
        "row_count": "",
        "column_count": "",
        "columns": "",
        "sha256": "",
    }
    if not path.exists():
        return info
    if path.is_dir():
        files = [p for p in path.rglob("*") if p.is_file()]
        info.update({"kind": "directory", "size_bytes": sum(p.stat().st_size for p in files), "row_count": len(files)})
        return info
    info.update({"kind": "file", "size_bytes": path.stat().st_size})
    suffix = path.suffix.lower()
    if suffix == ".parquet" and pq is not None:
        meta = pq.ParquetFile(path).metadata
        info["row_count"] = meta.num_rows
        info["column_count"] = meta.num_columns
        schema_names = pq.ParquetFile(path).schema_arrow.names
        info["columns"] = ";".join(schema_names[:40])
    elif suffix in {".csv", ".txt", ".tsv"}:
        if suffix in {".csv", ".tsv"} and pd is not None:
            try:
                sample = pd.read_csv(path, nrows=0, sep="\t" if suffix == ".tsv" else ",")
                info["column_count"] = len(sample.columns)
                info["columns"] = ";".join(map(str, sample.columns[:40]))
            except Exception as exc:  # noqa: BLE001
                info["columns"] = f"header_read_failed:{exc.__class__.__name__}"
        try:
            info["row_count"] = csv_row_count(path)
        except UnicodeDecodeError:
            info["row_count"] = "binary_or_non_utf8"
    if include_hash and path.is_file():
        info["sha256"] = sha256(path)
    return info


def status_for(row: dict[str, str], exists: bool) -> str:
    role = row["role"]
    manifest_status = row["status"]
    if exists:
        return "present"
    if manifest_status in DEFERRED_STATUSES:
        return manifest_status
    if role in FAIL_ROLES:
        return "missing_required"
    if role in WARN_ROLES:
        return "missing_support"
    return "missing_unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the coauthor private data-room manifest.")
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--data-root", type=Path, default=DATA_ROOT)
    parser.add_argument("--report-csv", type=Path)
    parser.add_argument("--hash", action="store_true", help="Compute SHA-256 hashes; can be slow on large files.")
    parser.add_argument("--strict-deferred", action="store_true", help="Fail if required artifacts are deferred rather than present.")
    args = parser.parse_args()

    rows = list(csv.DictReader(args.manifest.open(newline="")))
    results: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    for row in rows:
        path = runtime_path(row["logical_path"], args.data_root.resolve())
        info = inspect_path(path, include_hash=args.hash)
        status = status_for(row, bool(info["exists"]))
        counts[status] = counts.get(status, 0) + 1
        results.append(
            {
                **row,
                "runtime_path": str(path),
                "validation_status": status,
                **info,
            }
        )

    print("AI Washing coauthor data-room check")
    print(f"- manifest: {args.manifest}")
    print(f"- AIW_DATA_ROOT: {args.data_root.resolve()}")
    print(f"- manifest rows: {len(rows)}")
    for key in sorted(counts):
        print(f"- {key}: {counts[key]}")

    for item in results:
        if item["validation_status"] == "present":
            continue
        print(f"\n{item['validation_status']}: {item['artifact_id']}")
        print(f"- role: {item['role']}")
        print(f"- stage as: {item['logical_path']}")
        print(f"- note: {item['notes']}")

    if args.report_csv:
        args.report_csv.parent.mkdir(parents=True, exist_ok=True)
        fields = list(results[0].keys()) if results else []
        with args.report_csv.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(results)
        print(f"\nWrote report: {args.report_csv}")

    hard_fail = counts.get("missing_required", 0) + counts.get("missing_unknown", 0)
    if args.strict_deferred:
        hard_fail += counts.get("deferred_with_reason", 0) + counts.get("future_extension", 0)
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
