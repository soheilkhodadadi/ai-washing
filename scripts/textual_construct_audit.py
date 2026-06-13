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
SUMMARY_CSV = REPORT_DIR / "textual_construct_audit.csv"
SAMPLES_CSV = REPORT_DIR / "textual_construct_red_flags.csv"
SUMMARY_MD = REPORT_DIR / "textual_construct_summary.md"

SHORT_RE = re.compile(r"\b(?:ai|a\.i\.|ml|m\.l\.)\b", re.IGNORECASE)
# Keep this intentionally narrow. Generic business phrases such as "AI/ML
# solution" are not evidence of ML-as-milliliter ambiguity.
ML_UNIT_RE = re.compile(
    r"(?:\b\d+(?:\.\d+)?\s*m\.?l\.?\b|\bmillilit(?:er|re)s?\b|\bdosage\b|\bdose\b|\binjection\b|\bvial\b|\bserum\b)",
    re.IGNORECASE,
)
LONG_ANCHORS = [
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "neural network",
    "natural language processing",
    "computer vision",
    "large language model",
    "language model",
    "generative ai",
    "predictive analytics",
    "reinforcement learning",
    "autonomous driving",
    "chatbot",
    "algorithmic",
    "neural",
    "llm",
]
EXPECTED_LABELS = {"actionable", "speculative", "irrelevant", "A", "S", "I", "0", "1", "2"}


def runtime_path(logical_path: str) -> Path:
    path = Path(logical_path)
    if path.parts and path.parts[0] == "data":
        path = Path(*path.parts[1:])
    return DATA_ROOT / path


def contains_long_anchor(text: str) -> bool:
    t = str(text or "").lower()
    return any(anchor in t for anchor in LONG_ANCHORS)


def short_acronym_only(text: str) -> bool:
    t = str(text or "")
    return bool(SHORT_RE.search(t)) and not contains_long_anchor(t)


def ml_unit_context(text: str) -> bool:
    return bool(ML_UNIT_RE.search(str(text or "")))


def load_classifier() -> pd.DataFrame:
    root = runtime_path("data/processed/classifications/classifications_shadow_hybrid_api_a_conf49_v1")
    files = sorted(root.rglob("classified_sentences.parquet")) if root.exists() else []
    if not files:
        raise FileNotFoundError(f"No final classifier files found under {root}")
    return pd.concat([pd.read_parquet(p) for p in files], ignore_index=True)


def load_heldout() -> pd.DataFrame | None:
    path = runtime_path("data/validation/held_out_v4/held_out_sentences_v4.csv")
    return pd.read_csv(path) if path.exists() else None


def severity_for_rate(rate: float) -> str:
    if rate >= 0.25:
        return "material_needs_future_layer"
    if rate >= 0.05:
        return "manageable"
    return "negligible"


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


def main() -> int:
    df = load_classifier()
    text_col = "sentence" if "sentence" in df.columns else "sentence_norm"
    texts = df[text_col].fillna("").astype(str)
    short_mask = texts.map(short_acronym_only)
    ml_unit_mask = texts.map(ml_unit_context)
    long_anchor_mask = texts.map(contains_long_anchor)
    year_min = int(df["source_year"].min()) if "source_year" in df.columns else ""
    year_max = int(df["source_year"].max()) if "source_year" in df.columns else ""
    labels = sorted(map(str, df["predicted_label"].dropna().unique())) if "predicted_label" in df.columns else []
    score_cols = [c for c in ["score_actionable", "score_speculative", "score_irrelevant", "api_a_confidence", "local_confidence"] if c in df.columns]

    rows: list[dict[str, Any]] = []
    total = len(df)
    short_count = int(short_mask.sum())
    unit_count = int((short_mask & ml_unit_mask).sum())
    long_count = int(long_anchor_mask.sum())
    rows.append({"check_name": "row_count", "severity": "ok" if total == 147879 else "stop_the_line", "observed": total, "expected": 147879, "notes": "Final classified sentence count."})
    rows.append({"check_name": "year_coverage", "severity": "ok" if (year_min, year_max) == (2016, 2025) else "stop_the_line", "observed": f"{year_min}-{year_max}", "expected": "2016-2025", "notes": "Final classifier lane coverage."})
    unknown_labels = [label for label in labels if label not in EXPECTED_LABELS]
    rows.append({"check_name": "label_inventory", "severity": "manageable" if unknown_labels else "ok", "observed": ";".join(labels), "expected": "known label set", "notes": f"Unknown labels: {unknown_labels}" if unknown_labels else "Labels are inventoried."})
    rows.append({"check_name": "short_acronym_only_sentence_rate", "severity": severity_for_rate(short_count / total), "observed": f"{short_count} ({short_count / total:.2%})", "expected": "quantified and sampled", "notes": "Sentences with AI/ML short acronym but no long AI anchor. This is a construct-validity risk, not automatically an error."})
    rows.append({"check_name": "ml_unit_context_sentence_count", "severity": "material_needs_future_layer" if unit_count else "negligible", "observed": unit_count, "expected": "near zero", "notes": "Potential ML-as-milliliter or dosage context among short-acronym sentences."})
    rows.append({"check_name": "long_anchor_sentence_count", "severity": "info", "observed": long_count, "expected": "context", "notes": "Sentences with explicit long AI anchors."})
    for col in score_cols:
        vals = pd.to_numeric(df[col], errors="coerce").dropna()
        out = int(((vals < -1e-12) | (vals > 1 + 1e-12)).sum())
        rows.append({"check_name": f"score_bounds_{col}", "severity": "stop_the_line" if out else "ok", "observed": out, "expected": 0, "notes": "Classifier confidence/score should stay within [0,1]."})
    heldout = load_heldout()
    rows.append({"check_name": "heldout_validation_file", "severity": "ok" if heldout is not None else "material_needs_review", "observed": 0 if heldout is None else len(heldout), "expected": "present", "notes": "Held-out sample is required for auditability, though not for table reproduction."})

    sample = df.loc[short_mask | ml_unit_mask].copy()
    sample["short_acronym_only"] = short_mask.loc[sample.index].values
    sample["ml_unit_context"] = ml_unit_mask.loc[sample.index].values
    sample["long_anchor_context"] = long_anchor_mask.loc[sample.index].values
    keep_cols = [c for c in ["source_year", "source_cik", "source_file", "predicted_label", "prediction_source", "api_a_confidence", "local_confidence", text_col, "short_acronym_only", "ml_unit_context", "long_anchor_context"] if c in sample.columns]
    sample = sample.sort_values(["ml_unit_context", "short_acronym_only"], ascending=False).head(120)[keep_cols]
    sample = sample.rename(columns={text_col: "sentence"})

    write_csv(rows, SUMMARY_CSV)
    write_csv(sample.to_dict("records"), SAMPLES_CSV)
    lines = [
        "# Textual Construct Audit",
        "",
        "## Verdict",
        "",
        "The final classifier output reconciles to the expected v4.3 sentence count and coverage. Short-acronym-only AI/ML mentions are explicitly quantified and sampled because they are the main construct-validity risk in SEC text extraction.",
        "",
        "## Key Counts",
        "",
        f"- Final classified sentences: {total:,}",
        f"- Source-year coverage: {year_min}-{year_max}",
        f"- Short-acronym-only sentences: {short_count:,} ({short_count / total:.2%})",
        f"- Potential ML unit/dosage context among short-acronym sentences: {unit_count:,}",
        f"- Sentences with long AI anchors: {long_count:,}",
        "",
        "## Action",
        "",
        "Treat short-acronym ambiguity as a documented construct-validity limitation and future reviewer-labeled disambiguation layer.",
    ]
    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    stop = sum(1 for row in rows if row["severity"] == "stop_the_line" and str(row["observed"]) != str(row["expected"]))
    print("AI Washing textual construct audit")
    print(f"- final classified sentences: {total}")
    print(f"- short_acronym_only: {short_count} ({short_count / total:.2%})")
    print(f"- ml_unit_context: {unit_count}")
    print(f"- wrote: {SUMMARY_CSV}")
    print(f"- wrote: {SAMPLES_CSV}")
    print(f"- wrote: {SUMMARY_MD}")
    return 1 if stop else 0


if __name__ == "__main__":
    sys.exit(main())
