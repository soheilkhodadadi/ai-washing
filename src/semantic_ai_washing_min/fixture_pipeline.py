from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def run_fixture_pipeline(fixture_dir: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    filings = pd.read_csv(fixture_dir / "sample_filings.csv")
    labels = pd.read_csv(fixture_dir / "sample_labels.csv")
    panel = pd.read_csv(fixture_dir / "sample_market_patent_panel.csv")

    sentence_counts = (
        labels.groupby(["firm_id", "year", "label"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    for col in ["actionable", "speculative", "irrelevant"]:
        if col not in sentence_counts:
            sentence_counts[col] = 0
    sentence_counts["ai_sentence_count"] = sentence_counts[["actionable", "speculative", "irrelevant"]].sum(axis=1)
    sentence_counts["actionable_share"] = sentence_counts["actionable"] / sentence_counts["ai_sentence_count"].clip(lower=1)
    sentence_counts["speculative_share"] = sentence_counts["speculative"] / sentence_counts["ai_sentence_count"].clip(lower=1)

    merged = panel.merge(sentence_counts, on=["firm_id", "year"], how="left").fillna(0)
    merged["low_credibility"] = (merged["speculative_share"] > merged["actionable_share"]).astype(int)
    merged["weak_patent"] = (merged["ai_patent_grants"] <= merged["industry_ai_patent_median"]).astype(int)
    merged["patent_mismatch"] = (merged["low_credibility"] & merged["weak_patent"]).astype(int)

    table = merged[[
        "firm_id", "year", "ai_sentence_count", "actionable_share", "speculative_share",
        "ai_patent_grants", "low_credibility", "weak_patent", "patent_mismatch",
    ]].copy()
    table_path = output_dir / "fixture_patent_mismatch_table.csv"
    table.to_csv(table_path, index=False)

    summary_path = output_dir / "fixture_summary.md"
    summary_path.write_text(
        "# Fixture Pipeline Summary\n\n"
        f"Filings: {len(filings)}\n\n"
        f"Firm-year rows: {len(table)}\n\n"
        f"PatentMismatch rows: {int(table['patent_mismatch'].sum())}\n"
    )
    return table_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run tiny non-sensitive AI washing fixture pipeline.")
    parser.add_argument("--fixture-dir", type=Path, default=Path("data/fixtures"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/fixture"))
    args = parser.parse_args()
    table_path = run_fixture_pipeline(args.fixture_dir, args.output_dir)
    print(f"Wrote {table_path}")


if __name__ == "__main__":
    main()
