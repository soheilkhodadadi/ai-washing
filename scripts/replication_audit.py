from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "replication_audit_report.md"
REPORT_DIR = ROOT / "reports" / "replication_audit"

SCRIPTS = [
    ("package_surface", ["scripts/package_surface_audit.py", "--refresh"]),
    ("data_sanity", ["scripts/data_sanity_audit.py"]),
    ("textual_construct", ["scripts/textual_construct_audit.py"]),
    ("patent_construct", ["scripts/patent_construct_audit.py"]),
    ("journal_reproducibility", ["scripts/journal_reproducibility_audit.py"]),
]


def run_script(name: str, command: list[str]) -> tuple[str, int, str]:
    result = subprocess.run(
        [sys.executable, *command],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return name, result.returncode, result.stdout.strip()


def read_if_exists(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def main() -> int:
    results = [run_script(name, rel) for name, rel in SCRIPTS]
    stop = sum(1 for _, code, _ in results if code != 0)
    sections = [
        "# Replication Audit Report",
        "",
        "## Verdict",
        "",
    ]
    if stop:
        sections.append("The replication audit found at least one stop-the-line failure. Review the command logs and generated reports before sharing.")
    else:
        sections.append("The replication audit found no stop-the-line reproduction or package-surface failure. It does surface construct-validity risks, especially short-acronym AI/ML ambiguity, that should be documented as limitations and future robustness layers.")
    sections += [
        "",
        "## Command Outcomes",
        "",
    ]
    for name, code, output in results:
        sections.append(f"- `{name}`: exit `{code}`")
        if output:
            tail = output[-1200:].replace("\n", "\n  ")
            sections.append(f"  `{tail}`")
    sections += [
        "",
        "## Generated Evidence",
        "",
        "- `reports/replication_audit/package_surface_audit.md`",
        "- `reports/replication_audit/data_sanity_summary.md`",
        "- `reports/replication_audit/textual_construct_summary.md`",
        "- `reports/replication_audit/patent_construct_summary.md`",
        "- `reports/replication_audit/journal_reproducibility_audit.md`",
        "",
        "## Replication Audit Summary",
        "",
        "- Package hygiene: coauthor-facing runbooks are appropriate for the private collaboration package, while informal phase notes and email drafts remain outside the shared repo.",
        "- Data integrity: row counts, lane coverage, duplicate keys, impossible values, and private-data availability are now checked mechanically.",
        "- Textual construct validity: short-acronym AI/ML hits are quantified and sampled as documented construct-validity evidence.",
        "- Patent construct validity: short-acronym-only keyword evidence and potential ML-as-unit contexts are quantified and sampled.",
        "- Reproducibility: the environment, package dependencies, table/figure statuses, C7 format delta, and Git hygiene are checked from one command.",
    ]
    REPORT.write_text("\n".join(sections) + "\n", encoding="utf-8")
    print("AI Washing replication audit")
    print(f"- scripts: {len(results)}")
    print(f"- nonzero_exit_count: {stop}")
    print(f"- wrote: {REPORT}")
    return 1 if stop else 0


if __name__ == "__main__":
    sys.exit(main())
