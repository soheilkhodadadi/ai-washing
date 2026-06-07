from __future__ import annotations

import csv
import difflib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def normalize_latex(text: str) -> str:
    text = re.sub(r"%.*", "", text)
    text = re.sub(r"\\caption\*?\{(?:[^{}]|\{[^{}]*\})*\}", "", text)
    text = re.sub(r"\\label\{[^}]+\}", "", text)
    text = re.sub(r"\\begin\{table\}\[[^]]+\]", r"\\begin{table}", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main() -> int:
    crosswalk_path = ROOT / "manifests" / "table_to_script_crosswalk.csv"
    rows = list(csv.DictReader(crosswalk_path.open(newline="")))
    print("table_id,match_status,similarity,paper_file,generated_candidate")
    for row in rows:
        if row["asset_type"] != "table":
            continue
        paper = ROOT / "paper" / "v4_3_source" / row["paper_tex_file"]
        generated_rel = row.get("capsule_generated_tex", "")
        if not generated_rel:
            print(f"{row['table_id']},content_delta,NA,{row['paper_tex_file']},NO_GENERATED_TEX")
            continue
        generated = ROOT / generated_rel
        if not paper.exists() or not generated.exists():
            print(f"{row['table_id']},unknown,NA,{row['paper_tex_file']},{generated_rel}")
            continue
        a = paper.read_text(errors="ignore")
        b = generated.read_text(errors="ignore")
        if a == b:
            status, ratio = "exact_match", "1.000"
        else:
            ratio_float = difflib.SequenceMatcher(None, normalize_latex(a), normalize_latex(b)).ratio()
            status = "format_only_delta" if normalize_latex(a) == normalize_latex(b) else "content_delta"
            ratio = f"{ratio_float:.3f}"
        print(f"{row['table_id']},{status},{ratio},{row['paper_tex_file']},{generated_rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
