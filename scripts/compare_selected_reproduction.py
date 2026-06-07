from __future__ import annotations

import csv
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SELECTED = {"T00", "T16", "T17", "T09", "T30"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def compare_pair(reference: Path, reproduced: Path) -> tuple[str, str]:
    if not reference.exists() and not reproduced.exists():
        return "missing_both", "reference and reproduced files are missing"
    if not reference.exists():
        return "missing_reference", str(reference)
    if not reproduced.exists():
        return "missing_reproduced", str(reproduced)
    ref_hash = sha256(reference)
    repro_hash = sha256(reproduced)
    if ref_hash == repro_hash:
        return "exact_match", ref_hash
    return "content_delta", f"reference={ref_hash}; reproduced={repro_hash}"


def main() -> int:
    crosswalk = read_csv(ROOT / "manifests" / "table_to_script_crosswalk.csv")
    rows: list[dict[str, str]] = []
    for row in crosswalk:
        if row["table_id"] not in SELECTED:
            continue
        ref_csv = ROOT / row["capsule_generated_csv"] if row["capsule_generated_csv"] else Path()
        ref_tex = ROOT / row["capsule_generated_tex"] if row["capsule_generated_tex"] else Path()
        repro_csv = ROOT / "outputs" / "paper_exports" / "tables" / Path(row["generated_csv"]).name
        repro_tex = ROOT / "outputs" / "paper_exports" / "latex" / Path(row["generated_tex"]).name
        csv_status, csv_note = compare_pair(ref_csv, repro_csv)
        tex_status, tex_note = compare_pair(ref_tex, repro_tex)
        rows.append(
            {
                "table_id": row["table_id"],
                "test_id": row["test_id"],
                "run_id": row["run_id"],
                "csv_status": csv_status,
                "tex_status": tex_status,
                "csv_note": csv_note,
                "tex_note": tex_note,
                "reproduced_csv": str(repro_csv.relative_to(ROOT)),
                "reproduced_tex": str(repro_tex.relative_to(ROOT)),
                "reference_csv": str(ref_csv.relative_to(ROOT)) if ref_csv.exists() else str(ref_csv),
                "reference_tex": str(ref_tex.relative_to(ROOT)) if ref_tex.exists() else str(ref_tex),
            }
        )

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=[
            "table_id",
            "test_id",
            "run_id",
            "csv_status",
            "tex_status",
            "csv_note",
            "tex_note",
            "reproduced_csv",
            "reproduced_tex",
            "reference_csv",
            "reference_tex",
        ],
    )
    writer.writeheader()
    writer.writerows(rows)

    failures = [r for r in rows if r["csv_status"] != "exact_match"]
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
