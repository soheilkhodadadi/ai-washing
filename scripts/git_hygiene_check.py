from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

BANNED_SUFFIXES = {
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

BANNED_PREFIXES = (
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


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    failures: list[str] = []
    for rel in tracked_files():
        if rel in ALLOWED_TRACKED_OUTPUTS:
            continue
        suffixes = Path(rel).suffixes
        if any(suffix.lower() in BANNED_SUFFIXES for suffix in suffixes):
            failures.append(f"tracked banned file type: {rel}")
        if rel.startswith(BANNED_PREFIXES):
            failures.append(f"tracked private/generated path: {rel}")

    if failures:
        print("GIT HYGIENE CHECK FAILED")
        for item in failures:
            print(f"- {item}")
        return 1

    print("GIT HYGIENE CHECK PASSED")
    print("- no tracked private/generated data paths")
    print("- no tracked banned binary/archive file types")
    return 0


if __name__ == "__main__":
    sys.exit(main())
