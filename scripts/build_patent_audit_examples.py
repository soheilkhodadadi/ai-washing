from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
DATA_ROOT = Path(os.environ.get("AIW_DATA_ROOT", ROOT / "data")).resolve()
GRANT_EXAMPLES = DATA_ROOT / "processed/patents/ai_patent_examples_ever_speaker_2016_2025_hybrid_grant_2014plus.csv"
PREGRANT_EXAMPLES = DATA_ROOT / "processed/patents/ai_application_examples_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv"
DEFAULT_OUTPUT = DATA_ROOT / "reports/patents/patent_audit_examples.csv"

OUTPUT_COLUMNS = [
    "source_lane",
    "cik",
    "firm_name",
    "record_id",
    "patent_id",
    "application_id",
    "pgpub_id",
    "year",
    "title",
    "abstract",
    "matched_keywords",
    "keyword_review_flag",
    "audit_note",
    "source_file",
]


def _read_required_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing required patent example file: {path}")
    return pd.read_csv(path)


def _clean_text(value: object) -> str:
    text = "" if pd.isna(value) else str(value)
    return " ".join(text.replace("\r", " ").replace("\n", " ").split())


def _keyword_review_flag(value: object) -> str:
    keywords = [item.strip().lower() for item in _clean_text(value).split("|") if item.strip()]
    short = {"ai", "ml"}
    if keywords and set(keywords).issubset(short):
        return "short_acronym_only"
    if any(keyword in short for keyword in keywords):
        return "contains_short_acronym"
    return ""


def _audit_note(base_note: str, matched_keywords: object) -> str:
    flag = _keyword_review_flag(matched_keywords)
    if flag == "short_acronym_only":
        return (
            base_note
            + " Short-acronym-only keyword hit; inspect context because AI/ML can be ambiguous in patent text."
        )
    if flag == "contains_short_acronym":
        return base_note + " Includes AI/ML acronym hit plus other keyword evidence."
    return base_note


def _select_diverse(frame: pd.DataFrame, count: int) -> pd.DataFrame:
    if frame.empty:
        return frame
    frame = frame.sort_values(["year", "cik", "record_id"]).drop_duplicates(
        ["source_lane", "cik", "record_id"], keep="first"
    )
    if len(frame) <= count:
        return frame
    if count <= 1:
        return frame.iloc[[0]]
    positions = [round(i * (len(frame) - 1) / (count - 1)) for i in range(count)]
    selected = frame.iloc[sorted(set(positions))].copy()
    if len(selected) < count:
        selected_keys = set(selected.index)
        fill = frame.loc[[idx for idx in frame.index if idx not in selected_keys]].head(
            count - len(selected)
        )
        selected = pd.concat([selected, fill], ignore_index=False)
    return selected.sort_values(["source_lane", "year", "firm_name", "record_id"])


def _grant_rows(path: Path, count: int) -> pd.DataFrame:
    source = _read_required_csv(path)
    required = ["cik", "name", "year", "patent_id", "patent_title", "patent_abstract", "matched_keywords"]
    missing = [column for column in required if column not in source.columns]
    if missing:
        raise ValueError(f"Grant examples missing columns: {missing}")

    out = pd.DataFrame(
        {
            "source_lane": "grant",
            "cik": source["cik"],
            "firm_name": source["name"].map(_clean_text),
            "record_id": source["patent_id"].astype(str),
            "patent_id": source["patent_id"].astype(str),
            "application_id": "",
            "pgpub_id": "",
            "year": source["year"],
            "title": source["patent_title"].map(_clean_text),
            "abstract": source["patent_abstract"].map(_clean_text),
            "matched_keywords": source["matched_keywords"].map(_clean_text),
            "source_file": "ai_patent_examples_ever_speaker_2016_2025_hybrid_grant_2014plus.csv",
        }
    )
    out["keyword_review_flag"] = out["matched_keywords"].map(_keyword_review_flag)
    out["audit_note"] = out["matched_keywords"].map(
        lambda value: _audit_note(
            "Grant lane: exact-normalized assignee match; AI keyword hit in title or abstract.",
            value,
        )
    )
    out = out[(out["title"] != "") & (out["abstract"] != "") & (out["matched_keywords"] != "")]
    return _select_diverse(out, count)


def _pregrant_rows(path: Path, count: int) -> pd.DataFrame:
    source = _read_required_csv(path)
    required = [
        "cik",
        "name",
        "year",
        "application_id",
        "pgpub_id",
        "patent_id",
        "application_title",
        "application_abstract",
        "matched_keywords",
    ]
    missing = [column for column in required if column not in source.columns]
    if missing:
        raise ValueError(f"Pregrant examples missing columns: {missing}")

    out = pd.DataFrame(
        {
            "source_lane": "pregrant",
            "cik": source["cik"],
            "firm_name": source["name"].map(_clean_text),
            "record_id": source["application_id"].astype(str),
            "patent_id": source["patent_id"].fillna("").astype(str),
            "application_id": source["application_id"].astype(str),
            "pgpub_id": source["pgpub_id"].fillna("").astype(str),
            "year": source["year"],
            "title": source["application_title"].map(_clean_text),
            "abstract": source["application_abstract"].map(_clean_text),
            "matched_keywords": source["matched_keywords"].map(_clean_text),
            "source_file": "ai_application_examples_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv",
        }
    )
    out["keyword_review_flag"] = out["matched_keywords"].map(_keyword_review_flag)
    out["audit_note"] = out["matched_keywords"].map(
        lambda value: _audit_note(
            "Pregrant lane: assignee-first match with applicant fallback; deduped at CIK-application_id.",
            value,
        )
    )
    out = out[(out["title"] != "") & (out["abstract"] != "") & (out["matched_keywords"] != "")]
    return _select_diverse(out, count)


def build_audit_examples(
    *,
    grant_examples: Path,
    pregrant_examples: Path,
    output: Path,
    per_lane: int,
) -> pd.DataFrame:
    grants = _grant_rows(grant_examples, per_lane)
    pregrants = _pregrant_rows(pregrant_examples, per_lane)
    combined = pd.concat([grants, pregrants], ignore_index=True)
    combined = combined[OUTPUT_COLUMNS].sort_values(["source_lane", "year", "firm_name", "record_id"])
    output.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(output, index=False)
    return combined


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a readable coauthor audit sample from staged patent example files."
    )
    parser.add_argument("--grant-examples", type=Path, default=GRANT_EXAMPLES)
    parser.add_argument("--pregrant-examples", type=Path, default=PREGRANT_EXAMPLES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--per-lane", type=int, default=20)
    args = parser.parse_args()

    if args.per_lane < 1:
        raise ValueError("--per-lane must be positive")

    frame = build_audit_examples(
        grant_examples=args.grant_examples,
        pregrant_examples=args.pregrant_examples,
        output=args.output,
        per_lane=args.per_lane,
    )
    print("AI Washing patent audit examples")
    print(f"- AIW_DATA_ROOT: {DATA_ROOT}")
    print(f"- grant examples: {args.grant_examples}")
    print(f"- pregrant examples: {args.pregrant_examples}")
    print(f"- output: {args.output}")
    print(f"- rows: {len(frame)}")
    print(f"- source lanes: {', '.join(sorted(frame['source_lane'].unique()))}")
    print(f"- year range: {int(frame['year'].min())}-{int(frame['year'].max())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
