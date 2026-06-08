from __future__ import annotations

import argparse
import csv
import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import sys

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
DATA_ROOT = Path(os.environ.get("AIW_DATA_ROOT", ROOT / "data")).resolve()
MANIFEST = ROOT / "manifests" / "data_dependency_manifest.csv"

FAIL_CLASSES = {"required_current"}
WARN_CLASSES = {"support_only"}
FUTURE_CLASSES = {"future_extension"}


@dataclass(frozen=True)
class DependencyPath:
    manifest_path: str
    runtime_path: Path
    dependency_ids: tuple[str, ...]
    tests: tuple[str, ...]
    classifications: tuple[str, ...]
    manifest_statuses: tuple[str, ...]
    notes: tuple[str, ...]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def runtime_path(manifest_path: str) -> Path:
    path = Path(manifest_path)
    if path.parts and path.parts[0] == "data":
        path = Path(*path.parts[1:])
    return DATA_ROOT / path


def unique_dependencies(rows: list[dict[str, str]]) -> list[DependencyPath]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["expected_capsule_path"]].append(row)

    deps: list[DependencyPath] = []
    for manifest_path, group in sorted(grouped.items()):
        deps.append(
            DependencyPath(
                manifest_path=manifest_path,
                runtime_path=runtime_path(manifest_path),
                dependency_ids=tuple(sorted({r["dependency_id"] for r in group})),
                tests=tuple(sorted({r["test_id"] for r in group})),
                classifications=tuple(sorted({r["classification"] for r in group})),
                manifest_statuses=tuple(sorted({r["status"] for r in group})),
                notes=tuple(sorted({r["note"] for r in group if r.get("note")})),
            )
        )
    return deps


def classify(dep: DependencyPath) -> str:
    if dep.runtime_path.exists():
        return "present"
    classes = set(dep.classifications)
    if classes & FUTURE_CLASSES:
        return "future_extension"
    if classes & FAIL_CLASSES:
        return "missing_required"
    if classes & WARN_CLASSES:
        return "missing_support"
    return "missing_unknown"


def rel_or_abs(path: Path) -> str:
    try:
        return str(path.relative_to(DATA_ROOT))
    except ValueError:
        return str(path)


def write_csv_report(path: Path, deps: list[DependencyPath]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "manifest_path",
        "runtime_path_under_aiw_data_root",
        "status",
        "classification",
        "dependency_ids",
        "tests",
        "manifest_status",
        "notes",
    ]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for dep in deps:
            writer.writerow(
                {
                    "manifest_path": dep.manifest_path,
                    "runtime_path_under_aiw_data_root": rel_or_abs(dep.runtime_path),
                    "status": classify(dep),
                    "classification": ";".join(dep.classifications),
                    "dependency_ids": ";".join(dep.dependency_ids),
                    "tests": ";".join(dep.tests),
                    "manifest_status": ";".join(dep.manifest_statuses),
                    "notes": " | ".join(dep.notes),
                }
            )


def main() -> int:
    global DATA_ROOT

    parser = argparse.ArgumentParser(description="Validate the external AIW_DATA_ROOT mirror against the data dependency manifest.")
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--data-root", type=Path, default=DATA_ROOT)
    parser.add_argument("--report-csv", type=Path, help="Optional status CSV path. Prefer writing this outside Git for private mirrors.")
    parser.add_argument("--strict-support", action="store_true", help="Fail if support-only inputs are missing.")
    args = parser.parse_args()

    DATA_ROOT = args.data_root.resolve()

    rows = read_rows(args.manifest)
    deps = unique_dependencies(rows)
    statuses = {"present": 0, "missing_required": 0, "missing_support": 0, "future_extension": 0, "missing_unknown": 0}
    by_status: dict[str, list[DependencyPath]] = defaultdict(list)
    for dep in deps:
        status = classify(dep)
        statuses[status] += 1
        by_status[status].append(dep)

    print("AI Washing private data mirror check")
    print(f"- manifest: {args.manifest}")
    print(f"- AIW_DATA_ROOT: {DATA_ROOT}")
    print(f"- unique logical paths: {len(deps)}")
    print(f"- present: {statuses['present']}")
    print(f"- missing required current: {statuses['missing_required']}")
    print(f"- missing support-only: {statuses['missing_support']}")
    print(f"- documented future extensions: {statuses['future_extension']}")
    print(f"- missing unknown: {statuses['missing_unknown']}")

    for status in ("missing_required", "missing_support", "future_extension", "missing_unknown"):
        if not by_status[status]:
            continue
        print(f"\n{status}:")
        for dep in by_status[status]:
            print(f"- {dep.manifest_path}")
            print(f"  stage as: {rel_or_abs(dep.runtime_path)}")
            print(f"  tests: {', '.join(dep.tests)}")
            print(f"  dependencies: {', '.join(dep.dependency_ids)}")

    if args.report_csv:
        write_csv_report(args.report_csv, deps)
        print(f"\nWrote report: {args.report_csv}")

    if statuses["missing_required"] or statuses["missing_unknown"]:
        return 1
    if args.strict_support and statuses["missing_support"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
