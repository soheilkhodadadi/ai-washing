from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = [ROOT / "src", ROOT / "scripts"]
SCAN_FILES = [ROOT / "Makefile", ROOT / "pyproject.toml"]
BANNED = ["/Users/" + "soheilkhodadadi/"]


def main() -> int:
    failures: list[str] = []
    files: list[Path] = []
    for scan_dir in SCAN_DIRS:
        files.extend(p for p in scan_dir.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    files.extend(p for p in SCAN_FILES if p.exists())
    for path in files:
        text = path.read_text(errors="ignore")
        for token in BANNED:
            if token in text:
                failures.append(str(path.relative_to(ROOT)))
                break
    if failures:
        print("PATH LEAK SCAN FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PATH LEAK SCAN PASSED for executable/config files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
