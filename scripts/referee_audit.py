from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "referee_first_impression_report.md"
REPORT_DIR = ROOT / "reports" / "referee"

SCRIPTS = [
    ("package_surface", "scripts/package_surface_audit.py"),
    ("data_sanity", "scripts/data_sanity_audit.py"),
    ("textual_construct", "scripts/textual_construct_audit.py"),
    ("patent_construct", "scripts/patent_construct_audit.py"),
    ("journal_reproducibility", "scripts/journal_reproducibility_audit.py"),
]


def run_script(name: str, rel: str) -> tuple[str, int, str]:
    result = subprocess.run([sys.executable, rel], cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return name, result.returncode, result.stdout.strip()


def read_if_exists(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def main() -> int:
    results = [run_script(name, rel) for name, rel in SCRIPTS]
    stop = sum(1 for _, code, _ in results if code != 0)
    sections = [
        "# Referee First-Impression Report",
        "",
        "## Verdict",
        "",
    ]
    if stop:
        sections.append("The referee audit found at least one stop-the-line failure. Review the command logs and generated reports before sharing.")
    else:
        sections.append("The referee audit found no stop-the-line reproduction or package-surface failure. It does surface honest construct-validity risks, especially short-acronym AI/ML ambiguity, that should be disclosed as limitations and future audit layers.")
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
        "- `reports/referee/package_surface_audit.md`",
        "- `reports/referee/data_sanity_summary.md`",
        "- `reports/referee/textual_construct_summary.md`",
        "- `reports/referee/patent_construct_summary.md`",
        "- `reports/referee/journal_reproducibility_audit.md`",
        "",
        "## Referee Lens Summary",
        "",
        "- Package hygiene: coauthor-facing notes are useful for Thomas/Kuntara but should be excluded from a future journal archive profile.",
        "- Data integrity: row counts, lane coverage, duplicate keys, impossible values, and private-data availability are now checked mechanically.",
        "- Textual construct validity: short-acronym AI/ML hits are quantified and sampled rather than hidden.",
        "- Patent construct validity: short-acronym-only keyword evidence and potential ML-as-unit contexts are quantified and sampled.",
        "- Reproducibility: the environment, package dependencies, table/figure statuses, C7 format delta, and Git hygiene are checked from one command.",
    ]
    REPORT.write_text("\n".join(sections) + "\n", encoding="utf-8")
    print("AI Washing referee audit")
    print(f"- scripts: {len(results)}")
    print(f"- nonzero_exit_count: {stop}")
    print(f"- wrote: {REPORT}")
    return 1 if stop else 0


if __name__ == "__main__":
    sys.exit(main())
