from __future__ import annotations

import importlib
from importlib import metadata
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
EXPECTED = {
    "pandas": "2.2.3",
    "numpy": "1.26.4",
    "scipy": "1.17.1",
    "statsmodels": "0.14.6",
    "matplotlib": "3.10.8",
    "python-docx": "1.2.0",
    "python-dotenv": "1.2.2",
    "psycopg2-binary": "2.9.12",
    "pyarrow": "23.0.1",
    "pytest": "9.0.2",
}
IMPORTS = {
    "pandas": "pandas",
    "numpy": "numpy",
    "scipy": "scipy",
    "statsmodels": "statsmodels",
    "matplotlib": "matplotlib",
    "python-docx": "docx",
    "python-dotenv": "dotenv",
    "psycopg2-binary": "psycopg2",
    "pyarrow": "pyarrow",
    "pytest": "pytest",
}


def _docker_version() -> str:
    docker = shutil.which("docker")
    if not docker:
        if Path("/.dockerenv").exists():
            return "not installed inside container; this is expected"
        return "not installed on host"
    try:
        result = subprocess.run([docker, "--version"], check=False, text=True, capture_output=True, timeout=10)
    except Exception as exc:  # pragma: no cover - defensive diagnostic only
        return f"installed but unavailable: {exc}"
    return result.stdout.strip() if result.returncode == 0 else f"installed but unavailable: {result.stderr.strip()}"


def main() -> int:
    failures: list[str] = []
    print("AI Washing environment doctor")
    print(f"- python: {sys.version.split()[0]} ({sys.executable})")
    if not ((3, 10) <= sys.version_info[:2] < (3, 12)):
        failures.append("Python must be >=3.10,<3.12 for the pinned reproduction environment.")

    print(f"- AIW_REPO_ROOT: {ROOT}")
    for name, default in [
        ("AIW_DATA_ROOT", "not set"),
        ("AIW_OUTPUT_ROOT", str(ROOT / "outputs" / "reproduced")),
        ("AIW_PAPER_ROOT", str(ROOT / "outputs" / "paper_exports")),
    ]:
        value = os.environ.get(name, default)
        suffix = ""
        if name == "AIW_DATA_ROOT" and value != "not set":
            suffix = " (exists)" if Path(value).exists() else " (missing)"
        print(f"- {name}: {value}{suffix}")

    for dist_name, expected in EXPECTED.items():
        try:
            version = metadata.version(dist_name)
            importlib.import_module(IMPORTS[dist_name])
        except Exception as exc:
            failures.append(f"{dist_name}: import/version check failed: {exc}")
            continue
        marker = "OK" if version == expected else "MISMATCH"
        print(f"- {dist_name}: {version} ({marker}; expected {expected})")
        if version != expected:
            failures.append(f"{dist_name}: expected {expected}, found {version}")

    try:
        importlib.import_module("semantic_ai_washing.analysis.publication_runs.test_30_capital_raising_timing")
        importlib.import_module("semantic_ai_washing_min.fixture_pipeline")
        print("- package imports: OK")
    except Exception as exc:
        failures.append(f"package imports failed: {exc}")

    print(f"- docker CLI: {_docker_version()}")
    if failures:
        print("\nDOCTOR FAILED")
        for item in failures:
            print(f"- {item}")
        return 1
    print("\nDOCTOR PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
