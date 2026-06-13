from __future__ import annotations

import csv
import os
from pathlib import Path
import re
import sys
from typing import Any

import pandas as pd

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
DATA_ROOT = Path(os.environ.get("AIW_DATA_ROOT", ROOT / "data")).resolve()
REPORT_DIR = ROOT / "reports" / "replication_audit"
SUMMARY_CSV = REPORT_DIR / "patent_construct_audit.csv"
SAMPLES_CSV = REPORT_DIR / "patent_construct_red_flags.csv"
SUMMARY_MD = REPORT_DIR / "patent_construct_summary.md"
SHORT_KEYWORDS = {"ai", "ml"}
LONG_KEYWORDS = {"artificial intelligence", "machine learning", "deep learning", "neural network", "computer vision", "natural language processing", "large language model", "reinforcement learning"}
ML_UNIT_RE = re.compile(
    r"(?:\b\d+(?:\.\d+)?\s*m\.?l\.?\b|\bmillilit(?:er|re)s?\b|\bdosage\b|\bdose\b|\binjection\b|\bvial\b|\bserum\b)",
    re.IGNORECASE,
)


def runtime_path(logical_path: str) -> Path:
    path = Path(logical_path)
    if path.parts and path.parts[0] == "data":
        path = Path(*path.parts[1:])
    return DATA_ROOT / path


def split_keywords(value: Any) -> set[str]:
    return {item.strip().lower() for item in str(value or "").split("|") if item.strip()}


def short_only_keywords(value: Any) -> bool:
    kws = split_keywords(value)
    return bool(kws) and kws.issubset(SHORT_KEYWORDS)


def has_long_keyword(value: Any) -> bool:
    kws = split_keywords(value)
    return bool(kws & LONG_KEYWORDS) or any(k not in SHORT_KEYWORDS for k in kws)


def context_text(row: pd.Series) -> str:
    parts = []
    for col in ["patent_title", "patent_abstract", "application_title", "application_abstract"]:
        if col in row and pd.notna(row[col]):
            parts.append(str(row[col]))
    return " ".join(parts)


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_csv(logical: str) -> pd.DataFrame:
    path = runtime_path(logical)
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def audit_examples(name: str, df: pd.DataFrame, id_col: str) -> tuple[list[dict[str, Any]], pd.DataFrame]:
    keyword_sets = df["matched_keywords"].map(split_keywords)
    short_only = df["matched_keywords"].map(short_only_keywords)
    long_kw = df["matched_keywords"].map(has_long_keyword)
    unit_context = df.apply(lambda row: bool(ML_UNIT_RE.search(context_text(row))), axis=1)
    rows = [
        {"artifact_id": name, "check_name": "example_rows", "severity": "info", "observed": len(df), "expected": "context", "notes": "Readable patent/application examples staged for coauthor audit."},
        {"artifact_id": name, "check_name": "short_acronym_only_keyword_examples", "severity": "material_needs_future_layer" if int(short_only.sum()) else "negligible", "observed": int(short_only.sum()), "expected": "quantified and sampled", "notes": "Rows whose matched keyword evidence is only AI/ML."},
        {"artifact_id": name, "check_name": "ml_unit_context_examples", "severity": "material_needs_future_layer" if int((short_only & unit_context).sum()) else "negligible", "observed": int((short_only & unit_context).sum()), "expected": "near zero", "notes": "Potential ML-as-milliliter or dosage context in patent/application abstracts."},
        {"artifact_id": name, "check_name": "long_keyword_examples", "severity": "info", "observed": int(long_kw.sum()), "expected": "context", "notes": "Rows with longer AI keyword evidence."},
    ]
    sample = df.loc[short_only | unit_context].copy()
    sample["artifact_id"] = name
    sample["short_acronym_only_keywords"] = short_only.loc[sample.index].values
    sample["ml_unit_context"] = unit_context.loc[sample.index].values
    keep = [c for c in ["artifact_id", "cik", "name", "year", id_col, "patent_title", "application_title", "matched_keywords", "short_acronym_only_keywords", "ml_unit_context"] if c in sample.columns]
    return rows, sample.head(80)[keep]


def audit_counts(name: str, df: pd.DataFrame, ai_col: str, total_col: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    bad = int((pd.to_numeric(df[ai_col], errors="coerce") > pd.to_numeric(df[total_col], errors="coerce")).sum())
    zero_total = int((pd.to_numeric(df[total_col], errors="coerce").fillna(0) == 0).sum())
    rows.append({"artifact_id": name, "check_name": "ai_not_above_total", "severity": "stop_the_line" if bad else "ok", "observed": bad, "expected": 0, "notes": f"{ai_col} should not exceed {total_col}."})
    rows.append({"artifact_id": name, "check_name": "zero_total_rows", "severity": "info", "observed": zero_total, "expected": "context", "notes": "Rows with zero total patents/applications are acceptable but useful for coverage context."})
    return rows


def observed_value(rows: list[dict[str, Any]], artifact_id: str, check_name: str) -> Any:
    for row in rows:
        if row.get("artifact_id") == artifact_id and row.get("check_name") == check_name:
            return row.get("observed")
    return "see CSV"


def main() -> int:
    grant_examples = load_csv("data/processed/patents/ai_patent_examples_ever_speaker_2016_2025_hybrid_grant_2014plus.csv")
    pregrant_examples = load_csv("data/processed/patents/ai_application_examples_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv")
    grant_counts = load_csv("data/processed/patents/ai_patent_counts_filtered_ever_speaker_2016_2025_hybrid_grant_2014plus.csv")
    pregrant_counts = load_csv("data/processed/patents/ai_application_counts_filtered_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv")
    rows: list[dict[str, Any]] = []
    samples: list[pd.DataFrame] = []
    example_rows, sample = audit_examples("grant_examples", grant_examples, "patent_id")
    rows.extend(example_rows)
    samples.append(sample)
    example_rows, sample = audit_examples("pregrant_examples", pregrant_examples, "application_id")
    rows.extend(example_rows)
    samples.append(sample)
    rows.extend(audit_counts("grant_counts", grant_counts, "patents_ai", "patents_total"))
    rows.extend(audit_counts("pregrant_counts", pregrant_counts, "applications_ai", "applications_total"))
    red_flags = pd.concat(samples, ignore_index=True) if samples else pd.DataFrame()
    write_csv(rows, SUMMARY_CSV)
    write_csv(red_flags.to_dict("records"), SAMPLES_CSV)
    lines = [
        "# Patent Construct Audit",
        "",
        "## Verdict",
        "",
        "Patent AI identification has readable grant and pregrant evidence staged. Short-acronym-only keyword matches are quantified and sampled because they are the main construct-validity risk in the patent layer.",
        "",
        "## Key Counts",
        "",
        f"- Grant examples: {len(grant_examples):,}",
        f"- Pregrant examples: {len(pregrant_examples):,}",
        f"- Grant short-acronym-only examples: {observed_value(rows, 'grant_examples', 'short_acronym_only_keyword_examples')}",
        f"- Pregrant short-acronym-only examples: {observed_value(rows, 'pregrant_examples', 'short_acronym_only_keyword_examples')}",
        f"- Grant ML unit-context examples: {observed_value(rows, 'grant_examples', 'ml_unit_context_examples')}",
        f"- Pregrant ML unit-context examples: {observed_value(rows, 'pregrant_examples', 'ml_unit_context_examples')}",
        "",
        "## Action",
        "",
        "Keep current v4.3 reproduction unchanged, but disclose acronym ambiguity and preserve the red-flag examples for coauthor review before journal submission.",
    ]
    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    stop = sum(1 for row in rows if row["severity"] == "stop_the_line" and str(row["observed"]) != str(row["expected"]))
    print("AI Washing patent construct audit")
    print(f"- grant examples: {len(grant_examples)}")
    print(f"- pregrant examples: {len(pregrant_examples)}")
    print(f"- stop_the_line_failures: {stop}")
    print(f"- wrote: {SUMMARY_CSV}")
    print(f"- wrote: {SAMPLES_CSV}")
    print(f"- wrote: {SUMMARY_MD}")
    return 1 if stop else 0


if __name__ == "__main__":
    sys.exit(main())
