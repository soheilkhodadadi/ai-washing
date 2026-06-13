from __future__ import annotations

import csv
import os
from pathlib import Path
import sys
from typing import Any

import pandas as pd

ROOT = Path(os.environ.get("AIW_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
DATA_ROOT = Path(os.environ.get("AIW_DATA_ROOT", ROOT / "data")).resolve()
REPORT_DIR = ROOT / "reports" / "replication_audit"
REPORT_CSV = REPORT_DIR / "data_sanity_audit.csv"
REPORT_MD = REPORT_DIR / "data_sanity_summary.md"

EXPECTED = {
    "annual_panel": {
        "path": "data/processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet",
        "rows": 50840,
        "year_col": "year",
        "year_min": 2016,
        "year_max": 2025,
        "key": ["cik", "year"],
    },
    "event_panel": {
        "path": "data/processed/panel/filing_event_estimation_sample_hybrid_api_a_conf49_v1.parquet",
        "rows": 7355,
        "year_col": "filing_year",
        "year_min": 2016,
        "year_max": 2024,
        "key": ["filing_id"],
    },
    "daily_event_returns": {
        "path": "data/interim/market/filing_event_returns_daily_hybrid_api_a_conf49_v1.parquet",
        "rows": 1675992,
        "date_col": "trade_date",
        "date_max": "2024-12-31",
        "key": ["filing_id", "relative_day"],
    },
    "crsp_monthly": {
        "path": "data/interim/market/wrds_crsp_msf_full_sample_v1.parquet",
        "rows": 316921,
        "date_col": "date",
        "date_max": "2024-12-31",
        "key": ["permno", "date"],
    },
    "execucomp_ceo": {
        "path": "data/external/execucomp/execucomp_ceo_anncomp_2015_2024.parquet",
        "rows": 19878,
        "year_col": "year",
        "year_min": 2015,
        "year_max": 2024,
        "key": ["gvkey", "year", "execid"],
    },
}
NONNEGATIVE_COLUMNS = {
    "annual_panel": [
        "doc_count",
        "n_total",
        "n_A",
        "n_S",
        "n_I",
        "ai_total",
        "patents_total",
        "patents_ai",
        "applications_total",
        "applications_ai",
        "shrout",
        "market_cap_year_end",
    ],
    "event_panel": ["at", "sentence_count", "n_actionable", "n_speculative", "n_irrelevant", "n_ai_total"],
    "daily_event_returns": ["shrout"],
    "crsp_monthly": ["shrout"],
    "execucomp_ceo": ["salary", "bonus", "stock_awards_fv", "option_awards_fv", "tdc1", "ownership_pct"],
}
BOUNDED_01_COLUMNS = {
    "annual_panel": ["share_A", "share_S", "share_I", "ActShare", "SpecShare", "has_actionable", "has_spec_only"],
    "event_panel": ["share_actionable", "share_speculative", "share_irrelevant", "any_actionable", "any_speculative", "any_irrelevant"],
}


def runtime_path(logical_path: str) -> Path:
    path = Path(logical_path)
    if path.parts and path.parts[0] == "data":
        path = Path(*path.parts[1:])
    return DATA_ROOT / path


def add(rows: list[dict[str, Any]], artifact: str, check: str, severity: str, status: str, observed: Any, expected: Any, notes: str = "") -> None:
    rows.append(
        {
            "artifact_id": artifact,
            "check_name": check,
            "severity": severity,
            "status": status,
            "observed": str(observed),
            "expected": str(expected),
            "notes": notes,
        }
    )


def read_parquet(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path)


def check_artifact(name: str, spec: dict[str, Any], rows: list[dict[str, Any]]) -> pd.DataFrame | None:
    path = runtime_path(spec["path"])
    if not path.exists():
        add(rows, name, "artifact_present", "stop_the_line", "fail", "missing", spec["path"], "required private artifact is absent")
        return None
    df = read_parquet(path)
    add(rows, name, "row_count", "stop_the_line" if len(df) != spec["rows"] else "ok", "pass" if len(df) == spec["rows"] else "fail", len(df), spec["rows"])
    if "year_col" in spec:
        col = spec["year_col"]
        ymin, ymax = int(df[col].min()), int(df[col].max())
        ok = ymin == spec["year_min"] and ymax == spec["year_max"]
        add(rows, name, "year_coverage", "stop_the_line" if not ok else "ok", "pass" if ok else "fail", f"{ymin}-{ymax}", f"{spec['year_min']}-{spec['year_max']}")
    if "date_col" in spec:
        col = spec["date_col"]
        dmax = str(pd.to_datetime(df[col]).max().date())
        ok = dmax == spec["date_max"]
        add(rows, name, "date_max", "stop_the_line" if not ok else "ok", "pass" if ok else "fail", dmax, spec["date_max"])
    key = [c for c in spec.get("key", []) if c in df.columns]
    if key:
        dupes = int(df.duplicated(key).sum())
        severity = "stop_the_line" if dupes else "ok"
        add(rows, name, "duplicate_key_rows", severity, "pass" if dupes == 0 else "fail", dupes, 0, "+".join(key))
    missing_core = {c: int(df[c].isna().sum()) for c in key if c in df.columns}
    add(rows, name, "core_key_missingness", "stop_the_line" if any(missing_core.values()) else "ok", "pass" if not any(missing_core.values()) else "fail", missing_core, "all zero")
    return df


def check_numeric_ranges(name: str, df: pd.DataFrame, rows: list[dict[str, Any]]) -> None:
    for col in NONNEGATIVE_COLUMNS.get(name, []):
        if col not in df.columns:
            continue
        values = pd.to_numeric(df[col], errors="coerce")
        bad = int((values.dropna() < 0).sum())
        add(rows, name, f"nonnegative_{col}", "material_needs_review" if bad else "ok", "review" if bad else "pass", bad, 0)
    for col in BOUNDED_01_COLUMNS.get(name, []):
        if col not in df.columns:
            continue
        values = pd.to_numeric(df[col], errors="coerce")
        bad = int(((values.dropna() < -1e-12) | (values.dropna() > 1 + 1e-12)).sum())
        add(rows, name, f"bounded_0_1_{col}", "material_needs_review" if bad else "ok", "review" if bad else "pass", bad, 0)
    if name == "event_panel" and "sale" in df.columns:
        values = pd.to_numeric(df["sale"], errors="coerce")
        negative_sale = int((values.dropna() < 0).sum())
        add(rows, name, "negative_sales_observations", "manageable" if negative_sale else "ok", "review" if negative_sale else "pass", negative_sale, "0 preferred", "Compustat sales can be anomalous; report rather than silently drop.")
    if name in {"crsp_monthly", "daily_event_returns"} and "prc" in df.columns:
        values = pd.to_numeric(df["prc"], errors="coerce")
        negative_prc = int((values.dropna() < 0).sum())
        add(rows, name, "negative_crsp_price_sign_convention", "info" if negative_prc else "ok", "info" if negative_prc else "pass", negative_prc, "allowed", "CRSP negative price can indicate bid/ask average sign convention.")


def check_classification_and_sentence_counts(rows: list[dict[str, Any]]) -> None:
    class_root = runtime_path("data/processed/classifications/classifications_shadow_hybrid_api_a_conf49_v1")
    sent_root = runtime_path("data/processed/sec/sentences_clean")
    sent_2025 = runtime_path("data/processed/sec/sentences_clean_refresh_2025_v1")
    if not class_root.exists():
        add(rows, "classifier_outputs", "present", "stop_the_line", "fail", "missing", class_root)
        return
    class_frames = [pd.read_parquet(p) for p in sorted(class_root.rglob("classified_sentences.parquet"))]
    clf = pd.concat(class_frames, ignore_index=True)
    add(rows, "classifier_outputs", "row_count", "stop_the_line" if len(clf) != 147879 else "ok", "pass" if len(clf) == 147879 else "fail", len(clf), 147879)
    years = f"{int(clf['source_year'].min())}-{int(clf['source_year'].max())}" if "source_year" in clf.columns else "missing"
    add(rows, "classifier_outputs", "year_coverage", "stop_the_line" if years != "2016-2025" else "ok", "pass" if years == "2016-2025" else "fail", years, "2016-2025")
    labels = sorted(map(str, clf["predicted_label"].dropna().unique())) if "predicted_label" in clf.columns else []
    add(rows, "classifier_outputs", "label_set", "material_needs_review" if not labels else "ok", "pass" if labels else "review", labels, "non-empty classifier labels")
    dupes = int(clf.duplicated(["sentence_id"]).sum()) if "sentence_id" in clf.columns else -1
    add(rows, "classifier_outputs", "duplicate_sentence_id", "stop_the_line" if dupes else "ok", "pass" if dupes == 0 else "fail", dupes, 0)
    total_sentences = 0
    for root in [sent_root, sent_2025]:
        if root.exists():
            for file_path in root.rglob("ai_sentences.parquet"):
                total_sentences += len(pd.read_parquet(file_path, columns=["sentence_id"]))
    add(rows, "sec_sentence_outputs", "extracted_vs_classified_rows", "stop_the_line" if total_sentences != len(clf) else "ok", "pass" if total_sentences == len(clf) else "fail", total_sentences, len(clf), "2016-2024 plus 2025 refresh should reconcile to final classifier output.")


def check_patent_counts(rows: list[dict[str, Any]]) -> None:
    specs = [
        ("grant_counts", "data/processed/patents/ai_patent_counts_filtered_ever_speaker_2016_2025_hybrid_grant_2014plus.csv", "patents_ai", "patents_total", 11386),
        ("pregrant_counts", "data/processed/patents/ai_application_counts_filtered_ever_speaker_2016_2025_hybrid_pregrant_2014plus.csv", "applications_ai", "applications_total", 12051),
    ]
    for name, logical, ai_col, total_col, expected_rows in specs:
        path = runtime_path(logical)
        if not path.exists():
            add(rows, name, "present", "stop_the_line", "fail", "missing", logical)
            continue
        df = pd.read_csv(path)
        add(rows, name, "row_count", "stop_the_line" if len(df) != expected_rows else "ok", "pass" if len(df) == expected_rows else "fail", len(df), expected_rows)
        if {ai_col, total_col}.issubset(df.columns):
            bad = int((pd.to_numeric(df[ai_col], errors="coerce") > pd.to_numeric(df[total_col], errors="coerce")).sum())
            add(rows, name, "ai_count_not_above_total", "stop_the_line" if bad else "ok", "pass" if bad == 0 else "fail", bad, 0)


def write_outputs(rows: list[dict[str, Any]]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    fields = ["artifact_id", "check_name", "severity", "status", "observed", "expected", "notes"]
    with REPORT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["severity"]] = counts.get(row["severity"], 0) + 1
    lines = ["# Data Sanity Audit", "", "## Severity Counts", ""]
    for key in sorted(counts):
        lines.append(f"- `{key}`: {counts[key]}")
    lines += ["", "## Non-OK Findings", ""]
    for row in rows:
        if row["severity"] != "ok":
            lines.append(f"- `{row['artifact_id']}` / `{row['check_name']}`: {row['severity']} observed `{row['observed']}` expected `{row['expected']}`. {row['notes']}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    rows: list[dict[str, Any]] = []
    loaded: dict[str, pd.DataFrame] = {}
    for name, spec in EXPECTED.items():
        df = check_artifact(name, spec, rows)
        if df is not None:
            loaded[name] = df
            check_numeric_ranges(name, df, rows)
    check_classification_and_sentence_counts(rows)
    check_patent_counts(rows)
    write_outputs(rows)
    stop = sum(1 for row in rows if row["severity"] == "stop_the_line" and row["status"] != "pass")
    print("AI Washing data sanity audit")
    print(f"- checks: {len(rows)}")
    print(f"- stop_the_line_failures: {stop}")
    print(f"- wrote: {REPORT_CSV}")
    print(f"- wrote: {REPORT_MD}")
    return 1 if stop else 0


if __name__ == "__main__":
    sys.exit(main())
