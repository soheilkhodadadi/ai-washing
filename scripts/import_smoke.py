from __future__ import annotations

import csv
import importlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    rows = list(csv.DictReader((ROOT / "manifests" / "source_closure_manifest.csv").open(newline="")))
    failures: list[str] = []
    for row in rows:
        mod = row["module"]
        try:
            importlib.import_module(mod)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{mod}: {exc}")
    if failures:
        print("IMPORT SMOKE FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"IMPORT SMOKE PASSED ({len(rows)} modules)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
