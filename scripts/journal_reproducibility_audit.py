from __future__ import annotations

import csv
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
REPORT_DIR = ROOT / "reports" / "referee"
REPORT_CSV = REPORT_DIR / "journal_reproducibility_audit.csv"
REPORT_MD = REPORT_DIR / "journal_reproducibility_audit.md"
DOCS_TO_SCAN = [
    ROOT / "README_START_HERE.md",
    ROOT / "docs" / "coauthor_runbook.md",
    ROOT / "docs" / "onedrive_data_room_checklist.md",
]
REQUIRED_DOC_TERMS = {
    "Docker": "Docker setup or usage should be visible in the instructions.",
    "Windows": "Windows/WSL2 considerations should be visible for coauthors/data editors.",
    "Mac": "Mac instructions or compatibility should be visible.",
    "Linux": "Linux instructions or compatibility should be visible.",
    "AIW_DATA_ROOT": "Private data mount/path contract should be visible.",
    "runtime": "Runtime expectations should be stated or referenced.",
    "storage": "Storage or disk requirements should be stated or referenced.",
}


def normalize_output(output: str) -> str:
    """Remove incidental runtime text so audit ledgers are rerun-stable."""
    output = re.sub(r"\b(\d+\s+passed\s+in\s+)\d+(?:\.\d+)?s\b", r"\1<runtime>s", output)
    output = re.sub(r"\b(\d+\s+failed,\s+\d+\s+passed\s+in\s+)\d+(?:\.\d+)?s\b", r"\1<runtime>s", output)
    return output


def run_command(name: str, cmd: list[str], timeout: int = 1800) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    try:
        result = subprocess.run(cmd, cwd=ROOT, env=env, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        output = normalize_output(result.stdout.strip())
        return {"check_name": name, "severity": "ok" if result.returncode == 0 else "stop_the_line", "status": "pass" if result.returncode == 0 else "fail", "observed": result.returncode, "expected": 0, "notes": output[-900:]}
    except subprocess.TimeoutExpired as exc:
        return {"check_name": name, "severity": "stop_the_line", "status": "fail", "observed": "timeout", "expected": f"<{timeout}s", "notes": str(exc)}


def doc_text() -> str:
    parts = []
    for path in DOCS_TO_SCAN:
        if path.exists():
            parts.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts)


def docs_checks() -> list[dict[str, Any]]:
    text = doc_text().lower()
    rows: list[dict[str, Any]] = []
    for term, note in REQUIRED_DOC_TERMS.items():
        ok = term.lower() in text
        rows.append({"check_name": f"docs_mention_{term.lower().replace('/', '_')}", "severity": "ok" if ok else "manageable", "status": "pass" if ok else "review", "observed": ok, "expected": True, "notes": note})
    docker = shutil.which("docker")
    rows.append({"check_name": "docker_cli_available", "severity": "info" if docker else "manageable", "status": "info" if docker else "review", "observed": docker or "missing", "expected": "optional but recommended", "notes": "Docker is not required for native reruns, but useful for journal-style isolated validation."})
    return rows


def write_outputs(rows: list[dict[str, Any]]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    fields = ["check_name", "severity", "status", "observed", "expected", "notes"]
    with REPORT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["severity"]] = counts.get(row["severity"], 0) + 1
    lines = ["# Journal Reproducibility Audit", "", "## Severity Counts", ""]
    for key in sorted(counts):
        lines.append(f"- `{key}`: {counts[key]}")
    lines += ["", "## Non-OK Checks", ""]
    for row in rows:
        if row["severity"] != "ok":
            lines.append(f"- `{row['check_name']}`: {row['severity']} / {row['status']} / observed `{row['observed']}`. {row['notes']}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    py = sys.executable
    rows: list[dict[str, Any]] = []
    rows.extend(docs_checks())
    commands = [
        ("doctor", [py, "scripts/doctor.py"]),
        ("coauthor_preflight", ["make", f"PYTHON={py}", "coauthor-preflight"]),
        ("pytest", [py, "-m", "pytest", "-q"]),
        ("check_private_data", [py, "scripts/check_private_data.py"]),
        ("validate_data_room", [py, "scripts/validate_data_room.py"]),
        ("validate_sec_source", [py, "scripts/validate_sec_source_policy.py"]),
        ("validate_wrds_data", [py, "scripts/validate_wrds_data.py"]),
        ("validate_patent_data", [py, "scripts/validate_patent_data.py"]),
        ("audit_artifact_coverage", [py, "scripts/audit_artifact_coverage.py"]),
        ("reproduction_status", [py, "scripts/reproduce_assets.py", "--batch", "all", "--status-only", "--include-figures"]),
        ("figure_reproduction_status", [py, "scripts/reproduce_assets.py", "--tables", "F1,FC1", "--include-figures", "--regenerate-figures", "--status-only", "--status-csv", "docs/figure_reproduction_status.csv", "--status-md", "docs/figure_reproduction_status.md"]),
        ("c7_format_delta", [py, "scripts/explain_c7_format_delta.py"]),
        ("git_hygiene", [py, "scripts/git_hygiene_check.py"]),
    ]
    for name, cmd in commands:
        rows.append(run_command(name, cmd))
    write_outputs(rows)
    stop = sum(1 for row in rows if row["severity"] == "stop_the_line" and row["status"] != "pass")
    print("AI Washing journal reproducibility audit")
    print(f"- checks: {len(rows)}")
    print(f"- stop_the_line_failures: {stop}")
    print(f"- wrote: {REPORT_CSV}")
    print(f"- wrote: {REPORT_MD}")
    return 1 if stop else 0


if __name__ == "__main__":
    sys.exit(main())
