from __future__ import annotations

import csv
import os
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Any

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
IMAGE = os.environ.get("AIW_DOCKER_IMAGE", "ai-washing:local")
DATA_ROOT_RAW = os.environ.get("AIW_DATA_ROOT", "").strip()
DATA_ROOT = Path(DATA_ROOT_RAW).expanduser().resolve() if DATA_ROOT_RAW else None
REPORT_MD = ROOT / "docs" / "share_readiness_report.md"
REPORT_CSV = ROOT / "reports" / "share_readiness.csv"
WORKDIR = "/workspaces/ai-washing"
DATA_DIR = "/workspaces/ai-washing-private-data"


def sanitize(text: str) -> str:
    text = text.replace(str(ROOT), "$AIW_REPO_ROOT")
    if DATA_ROOT:
        text = text.replace(str(DATA_ROOT), "$AIW_DATA_ROOT")
    return text.strip()


def run_check(name: str, cmd: list[str], *, timeout: int = 1800, expect_failure: bool = False, required: bool = True) -> dict[str, Any]:
    command = sanitize(" ".join(shlex.quote(part) for part in cmd))
    try:
        result = subprocess.run(cmd, cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        output = sanitize(result.stdout[-1400:])
        passed = (result.returncode != 0) if expect_failure else (result.returncode == 0)
        severity = "ok" if passed else ("stop_the_line" if required else "manageable")
        status = "pass" if passed else "fail"
        return {
            "check_name": name,
            "severity": severity,
            "status": status,
            "return_code": result.returncode,
            "command": command,
            "notes": output,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "check_name": name,
            "severity": "stop_the_line" if required else "manageable",
            "status": "timeout",
            "return_code": "timeout",
            "command": command,
            "notes": sanitize(str(exc)),
        }
    except FileNotFoundError as exc:
        return {
            "check_name": name,
            "severity": "stop_the_line" if required else "manageable",
            "status": "missing",
            "return_code": "missing",
            "command": command,
            "notes": sanitize(str(exc)),
        }


def docker_base_args(*, with_data: bool) -> list[str]:
    args = [
        "docker",
        "run",
        "--rm",
        "--user",
        f"{os.getuid()}:{os.getgid()}",
        "-e",
        "HOME=/tmp",
        "-e",
        "MPLCONFIGDIR=/tmp/aiw-matplotlib",
        "-e",
        "XDG_CACHE_HOME=/tmp/aiw-cache",
        "-e",
        f"AIW_REPO_ROOT={WORKDIR}",
        "-e",
        f"AIW_OUTPUT_ROOT={WORKDIR}/outputs/reproduced",
        "-e",
        f"AIW_PAPER_ROOT={WORKDIR}/outputs/paper_exports",
        "-e",
        f"PYTHONPATH={WORKDIR}/src",
        "-v",
        f"{ROOT}:{WORKDIR}",
        "-w",
        WORKDIR,
    ]
    if with_data and DATA_ROOT:
        args.extend(["-e", f"AIW_DATA_ROOT={DATA_DIR}", "-v", f"{DATA_ROOT}:{DATA_DIR}:ro"])
    else:
        args.extend(["-e", f"AIW_DATA_ROOT={DATA_DIR}"])
    args.append(IMAGE)
    return args


def write_reports(rows: list[dict[str, Any]]) -> None:
    REPORT_CSV.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    fields = ["check_name", "severity", "status", "return_code", "command", "notes"]
    with REPORT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["severity"]] = counts.get(row["severity"], 0) + 1
    lines = [
        "# Share Readiness Report",
        "",
        "This report checks whether the AI Washing workstation can be used through the low-friction Docker path.",
        "",
        "## Environment Boundary",
        "",
        f"- Docker image: `{IMAGE}`",
        f"- Private data root provided: `{'yes' if DATA_ROOT else 'no'}`",
        "- Private data are mounted read-only at `/workspaces/ai-washing-private-data` when provided.",
        "- Private data are not copied into the image.",
        "",
        "## Severity Counts",
        "",
    ]
    for key in sorted(counts):
        lines.append(f"- `{key}`: {counts[key]}")
    lines += ["", "## Check Results", ""]
    for row in rows:
        lines.append(f"- `{row['check_name']}`: `{row['severity']}` / `{row['status']}` / return `{row['return_code']}`")
        if row["severity"] != "ok" and row["notes"]:
            lines.append(f"  - Notes: {row['notes']}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    rows: list[dict[str, Any]] = []
    rows.append(run_check("docker_cli_available", ["docker", "--version"]))
    rows.append(run_check("docker_engine_available", ["docker", "info", "--format", "{{.ServerVersion}} {{.OSType}} {{.Architecture}}"], timeout=30))
    rows.append(run_check("docker_compose_available", ["docker", "compose", "version"], timeout=30, required=False))
    rows.append(run_check("docker_image_build", ["docker", "build", "-t", IMAGE, "."], timeout=3600))
    rows.append(run_check("docker_code_only_preflight", docker_base_args(with_data=False) + ["make", "PYTHON=python", "coauthor-preflight"], timeout=1800))
    rows.append(run_check("docker_private_data_absent_fails_cleanly", docker_base_args(with_data=False) + ["make", "PYTHON=python", "check-private-data"], timeout=300, expect_failure=True))

    if DATA_ROOT and DATA_ROOT.exists():
        rows.append(run_check("docker_private_data_mount_check", docker_base_args(with_data=True) + ["make", "PYTHON=python", "check-private-data"], timeout=600))
    else:
        rows.append({
            "check_name": "docker_private_data_mount_check",
            "severity": "stop_the_line",
            "status": "fail",
            "return_code": "not_run",
            "command": "AIW_DATA_ROOT=/path/to/ai-washing-private-data make share-readiness",
            "notes": "AIW_DATA_ROOT must point to an existing private data mirror for final share readiness.",
        })

    write_reports(rows)
    stop = sum(1 for row in rows if row["severity"] == "stop_the_line")
    print("AI Washing share readiness")
    print(f"- checks: {len(rows)}")
    print(f"- stop_the_line: {stop}")
    print(f"- wrote: {REPORT_MD}")
    print(f"- wrote: {REPORT_CSV}")
    return 1 if stop else 0


if __name__ == "__main__":
    sys.exit(main())
