from __future__ import annotations

import argparse
import csv
from pathlib import Path
import subprocess
import sys
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "replication_audit"
REPORT_CSV = REPORT_DIR / "package_surface_audit.csv"
REPORT_MD = REPORT_DIR / "package_surface_audit.md"

STOP_SUFFIXES = {
    ".parquet",
    ".dta",
    ".sas7bdat",
    ".rds",
    ".rda",
    ".feather",
    ".h5",
    ".hdf5",
    ".pkl",
    ".pickle",
    ".zip",
    ".tar",
    ".tgz",
    ".7z",
}
STOP_PREFIXES = (
    "data/private/",
    "data/raw/",
    "data/interim/",
    "data/processed/",
    "data/labels/",
    "data/validation/",
    "data/reports/",
    "private_data/",
    "outputs/reproduced/",
    "outputs/paper_exports/",
)
ALLOWED_TRACKED_OUTPUTS = {"outputs/reproduced/README.md", "outputs/fixture/.gitkeep"}
JOURNAL_EXCLUDE_PREFIXES = (
    "docs/phase",
    "docs/cloud_share_",
)
JOURNAL_EXCLUDE_EXACT: set[str] = set()
JOURNAL_OPTIONAL_EXACT = {
    "paper/ai_washing_v4.3.pdf",
    "paper/v5_0_editorial_source/README.md",
    "docs/coauthor_runbook.md",
    "docs/coauthor_quickstart.md",
    "docs/coauthor_delivery_overview.md",
    "docs/coauthor_data_room.md",
    "docs/v5_editorial_alignment.md",
    "docs/extension_playbook.md",
    "docs/extension_notes_future_data.md",
    "docs/extensions/builder_hides_first_pass.md",
    "docs/extensions/washing_pays_data_requirements.md",
}


def _git_lines(args: list[str]) -> list[str]:
    result = subprocess.run(args, cwd=ROOT, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return [line.rstrip("\n") for line in result.stdout.splitlines() if line.strip()]


def tracked_files() -> list[str]:
    return _git_lines(["git", "ls-files"])


def status_entries() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "--ignored", "--untracked-files=normal"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    for line in result.stdout.splitlines():
        if not line:
            continue
        rows.append((line[:2], line[3:]))
    return rows


def _has_stop_suffix(path: str) -> bool:
    suffixes = [s.lower() for s in Path(path).suffixes]
    return any(s in STOP_SUFFIXES for s in suffixes)


def classify_tracked(path: str) -> dict[str, str]:
    severity = "ok"
    coauthor_profile = "include"
    journal_profile = "include"
    reason = "tracked project file"

    if path in ALLOWED_TRACKED_OUTPUTS:
        return {
            "path": path,
            "surface": "tracked",
            "severity": "ok",
            "coauthor_profile": "include_placeholder",
            "journal_profile": "include_placeholder",
            "reason": "allowed tracked placeholder under outputs",
        }

    if _has_stop_suffix(path):
        severity = "stop_the_line"
        coauthor_profile = "exclude"
        journal_profile = "exclude"
        reason = "tracked banned binary/archive/private data file type"
    elif path.startswith(STOP_PREFIXES):
        severity = "stop_the_line"
        coauthor_profile = "exclude"
        journal_profile = "exclude"
        reason = "tracked private or generated runtime path"
    elif path.startswith(JOURNAL_EXCLUDE_PREFIXES) or path in JOURNAL_EXCLUDE_EXACT:
        severity = "manageable"
        coauthor_profile = "include"
        journal_profile = "exclude"
        reason = "useful coauthor/process document but not suitable for a cold journal archive"
    elif path.startswith("paper/v5_0_editorial_source/"):
        severity = "info"
        coauthor_profile = "include_editorial_source"
        journal_profile = "optional_include_editorial_source"
        reason = "v5.0 editorial source is useful for coauthor presentation review; journal archive inclusion depends on release policy"
    elif path in JOURNAL_OPTIONAL_EXACT:
        severity = "info"
        coauthor_profile = "include"
        journal_profile = "optional_exclude"
        reason = "useful for review, but journal replication archives may request code/data only"
    elif path.startswith("data/curated/v4_3/generated_"):
        severity = "info"
        coauthor_profile = "include_frozen_evidence"
        journal_profile = "include_frozen_evidence"
        reason = "frozen v4.3 generated evidence used for reproduction comparison"
    return {
        "path": path,
        "surface": "tracked",
        "severity": severity,
        "coauthor_profile": coauthor_profile,
        "journal_profile": journal_profile,
        "reason": reason,
    }


def classify_worktree(status: str, path: str) -> dict[str, str]:
    severity = "ok"
    reason = "ignored or untracked local artifact"
    coauthor_profile = "exclude"
    journal_profile = "exclude"
    if path.startswith("reports/replication_audit/"):
        severity = "info"
        coauthor_profile = "include_generated_audit_evidence"
        journal_profile = "optional_include_generated_audit_evidence"
        reason = "generated replication audit evidence; review before deciding whether to commit or archive"
    elif status == "??":
        severity = "material_needs_review"
        reason = "untracked file would be missed by Git archive; review before zipping a raw folder"
    elif status == "!!":
        severity = "info"
        reason = "ignored local/generated artifact; excluded from Git archive"
    else:
        severity = "material_needs_review"
        reason = "modified/staged worktree entry; should be intentional before sharing"
    return {
        "path": path,
        "surface": status,
        "severity": severity,
        "coauthor_profile": coauthor_profile,
        "journal_profile": journal_profile,
        "reason": reason,
    }


def write_csv(rows: Iterable[dict[str, str]], path: Path) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["path", "surface", "severity", "coauthor_profile", "journal_profile", "reason"]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]], path: Path) -> None:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["severity"]] = counts.get(row["severity"], 0) + 1
    stop_rows = [r for r in rows if r["severity"] == "stop_the_line"]
    material_rows = [r for r in rows if r["severity"] in {"material_needs_review", "manageable"}]
    lines = [
        "# Package Surface Audit",
        "",
        "This report separates the coauthor workstation surface from a future journal replication archive surface.",
        "",
        "## Severity Counts",
        "",
    ]
    for key in sorted(counts):
        lines.append(f"- `{key}`: {counts[key]}")
    lines += ["", "## Verdict", ""]
    if stop_rows:
        lines.append("Stop-the-line tracked package-surface issues were found.")
    else:
        lines.append("No stop-the-line tracked package-surface leakage was found.")
    lines += ["", "## Journal-Archive Exclusions To Remember", ""]
    for row in material_rows[:40]:
        lines.append(f"- `{row['path']}`: {row['reason']} ({row['severity']})")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_rows() -> list[dict[str, str]]:
    rows = [classify_tracked(path) for path in tracked_files()]
    rows.extend(classify_worktree(status, path) for status, path in status_entries() if status != "  ")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the AI Washing package surface.")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Write the tracked report files under reports/replication_audit.",
    )
    args = parser.parse_args()

    rows = build_rows()
    stop_count = sum(1 for row in rows if row["severity"] == "stop_the_line")
    print("AI Washing package surface audit")
    print(f"- rows: {len(rows)}")
    print(f"- stop_the_line: {stop_count}")
    if args.refresh:
        write_csv(rows, REPORT_CSV)
        write_md(rows, REPORT_MD)
        print(f"- wrote: {REPORT_CSV}")
        print(f"- wrote: {REPORT_MD}")
    else:
        print("- mode: check-only; no files written")
        print("- refresh reports with: make package-surface-audit-refresh")
    return 1 if stop_count else 0


if __name__ == "__main__":
    sys.exit(main())
