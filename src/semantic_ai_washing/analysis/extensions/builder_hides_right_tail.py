"""First-pass builder-hides extension using the v4.3 annual panel.

This script is intentionally an extension sandbox, not a v4.3 manuscript table.
It asks whether firms with strong real AI innovation disclose less actionable AI
content. The headline specification uses lagged patent/application activity so
that the disclosure outcome is not mechanically compared with future innovation.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from semantic_ai_washing.analysis.delivery_table_payloads import _fit_absorbed_ols, sig_stars
from semantic_ai_washing.analysis.publication_runs.test_16_construct_variant_screen import (
    _add_construct_variants,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_PANEL_RELATIVE = Path(
    "processed/panel/canonical/ever_speaker_panel_2016_2025_hybrid_api_a_conf49_v1.parquet"
)
DEFAULT_OUTPUT_RELATIVE = Path("extensions/builder_hides_right_tail")

DISCLOSURE_OUTCOMES: list[tuple[str, str]] = [
    ("ActShare", "Actionable disclosure share"),
    ("CredAI", "Credible AI disclosure index"),
    ("AI_Focus", "AI focus"),
    ("share_A", "Actionable sentence share"),
    ("share_S", "Speculative sentence share"),
    ("SpecShare", "Speculative disclosure share"),
    ("SpecMinusAct", "Speculative minus actionable share"),
    ("LowCredibility", "Low-credibility indicator"),
]
CONTROL_CANDIDATES = ["ln_assets", "leverage", "cash", "rd_intensity", "capx_at", "roa", "sales_growth"]
MAIN_SIGNAL = "top_builder_lagged"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annual-panel", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--tail-quantile", type=float, default=0.90)
    parser.add_argument("--min-year-positive", type=int, default=10)
    parser.add_argument(
        "--ai-talk-only",
        action="store_true",
        help="Restrict the extension screen to firm-years with any AI disclosure talk.",
    )
    return parser.parse_args()


def default_annual_panel() -> Path:
    data_root = os.environ.get("AIW_DATA_ROOT")
    if data_root:
        return Path(data_root).resolve() / DEFAULT_PANEL_RELATIVE
    return REPO_ROOT / "data" / DEFAULT_PANEL_RELATIVE


def default_output_dir() -> Path:
    output_root = os.environ.get("AIW_OUTPUT_ROOT")
    if output_root:
        return Path(output_root).resolve() / DEFAULT_OUTPUT_RELATIVE
    return REPO_ROOT / "outputs" / DEFAULT_OUTPUT_RELATIVE



def _ensure_construct_inputs(panel: pd.DataFrame) -> pd.DataFrame:
    out = panel.copy()
    if "log_patents_ai_lead0" not in out.columns and "patents_ai" in out.columns:
        out["log_patents_ai_lead0"] = np.log1p(pd.to_numeric(out["patents_ai"], errors="coerce").fillna(0))
    if "log_applications_ai_lead0" not in out.columns and "applications_ai" in out.columns:
        out["log_applications_ai_lead0"] = np.log1p(
            pd.to_numeric(out["applications_ai"], errors="coerce").fillna(0)
        )
    if "A_S" not in out.columns and {"ActShare", "SpecShare"}.issubset(out.columns):
        spec = pd.to_numeric(out["SpecShare"], errors="coerce")
        act = pd.to_numeric(out["ActShare"], errors="coerce")
        out["A_S"] = np.where(spec.gt(0), act / spec, np.nan)
    return out

def _numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for column in columns:
        if column in out.columns:
            out[column] = pd.to_numeric(out[column], errors="coerce").replace([np.inf, -np.inf], np.nan)
    return out


def _top_tail_by_year(
    frame: pd.DataFrame,
    value_col: str,
    *,
    quantile: float,
    min_year_positive: int,
) -> pd.Series:
    """Flag year-specific positive right-tail observations.

    The positive-value requirement prevents zero-innovation years from being
    classified as "top builders" merely because the year-level quantile is zero.
    """
    values = pd.to_numeric(frame[value_col], errors="coerce").replace([np.inf, -np.inf], np.nan)
    years = pd.to_numeric(frame["year"], errors="coerce")
    result = pd.Series(0, index=frame.index, dtype="int64")
    for year, index in years.dropna().groupby(years.dropna()).groups.items():
        year_index = list(index)
        positive = values.loc[year_index].dropna()
        positive = positive.loc[positive.gt(0)]
        if len(positive) < min_year_positive:
            continue
        cutoff = float(positive.quantile(quantile))
        result.loc[year_index] = values.loc[year_index].ge(cutoff).fillna(False).astype(int)
    return result


def prepare_panel(
    panel: pd.DataFrame,
    *,
    tail_quantile: float,
    min_year_positive: int,
    ai_talk_only: bool = False,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    required = ["cik", "year", "patents_ai", "applications_ai", "patents_ai_lag1", "applications_ai_lag1"]
    missing = [column for column in required if column not in panel.columns]
    if missing:
        raise KeyError(f"Missing required builder-hides columns: {missing}")

    use = _add_construct_variants(_ensure_construct_inputs(panel)).copy()
    numeric_columns = sorted({
        "year",
        "patents_ai",
        "applications_ai",
        "patents_ai_lag1",
        "applications_ai_lag1",
        "sic",
        "sic2",
        *[column for column, _label in DISCLOSURE_OUTCOMES],
        *CONTROL_CANDIDATES,
    })
    use = _numeric(use, numeric_columns)
    use["cik"] = use["cik"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    if "sic2" not in use.columns or use["sic2"].isna().all():
        use["sic2"] = (pd.to_numeric(use.get("sic"), errors="coerce") // 100).astype("Int64")

    use["real_ai_current"] = use[["patents_ai", "applications_ai"]].fillna(0).sum(axis=1)
    use["real_ai_lagged"] = use[["patents_ai_lag1", "applications_ai_lag1"]].fillna(0).sum(axis=1)
    use["log_real_ai_current"] = np.log1p(use["real_ai_current"])
    use["log_real_ai_lagged"] = np.log1p(use["real_ai_lagged"])
    use["top_builder_current"] = _top_tail_by_year(
        use,
        "real_ai_current",
        quantile=tail_quantile,
        min_year_positive=min_year_positive,
    )
    use[MAIN_SIGNAL] = _top_tail_by_year(
        use,
        "real_ai_lagged",
        quantile=tail_quantile,
        min_year_positive=min_year_positive,
    )

    needed_outcomes = [column for column, _label in DISCLOSURE_OUTCOMES if column in use.columns]
    sample_mask = use["cik"].ne("") & use["year"].notna() & use["sic2"].notna()
    sample_mask &= use[needed_outcomes].notna().any(axis=1)
    if ai_talk_only:
        sample_mask &= pd.to_numeric(use["any_ai_talk"], errors="coerce").fillna(0).astype(int).eq(1)
    use = use.loc[sample_mask].copy()
    use["year"] = pd.to_numeric(use["year"], errors="coerce").astype(int)
    use["sic2"] = pd.to_numeric(use["sic2"], errors="coerce").astype(int)

    summary = {
        "rows": int(len(use)),
        "firms": int(use["cik"].nunique()),
        "year_min": int(use["year"].min()) if len(use) else None,
        "year_max": int(use["year"].max()) if len(use) else None,
        "tail_quantile": tail_quantile,
        "min_year_positive": min_year_positive,
        "top_builder_lagged_rows": int(use[MAIN_SIGNAL].sum()),
        "top_builder_lagged_firms": int(use.loc[use[MAIN_SIGNAL].eq(1), "cik"].nunique()),
        "top_builder_current_rows": int(use["top_builder_current"].sum()),
        "top_builder_current_firms": int(use.loc[use["top_builder_current"].eq(1), "cik"].nunique()),
        "ai_talk_only": bool(ai_talk_only),
    }
    return use, summary


def descriptive_table(sample: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for outcome, label in DISCLOSURE_OUTCOMES:
        if outcome not in sample.columns:
            continue
        for signal, signal_label in [(MAIN_SIGNAL, "Lagged right-tail builder"), ("top_builder_current", "Current right-tail builder")]:
            grouped = sample.dropna(subset=[outcome, signal]).groupby(signal)[outcome]
            low = grouped.mean().get(0, np.nan)
            high = grouped.mean().get(1, np.nan)
            n_low = grouped.count().get(0, 0)
            n_high = grouped.count().get(1, 0)
            rows.append(
                {
                    "signal": signal,
                    "signal_label": signal_label,
                    "outcome": outcome,
                    "outcome_label": label,
                    "non_top_mean": low,
                    "top_mean": high,
                    "difference_top_minus_non_top": high - low if pd.notna(high) and pd.notna(low) else np.nan,
                    "n_non_top": int(n_low),
                    "n_top": int(n_high),
                }
            )
    return pd.DataFrame(rows)


def regression_table(sample: pd.DataFrame) -> pd.DataFrame:
    controls = [column for column in CONTROL_CANDIDATES if column in sample.columns]
    rows: list[dict[str, Any]] = []
    for outcome, label in DISCLOSURE_OUTCOMES:
        if outcome not in sample.columns:
            continue
        try:
            result, use, adj_r2 = _fit_absorbed_ols(
                sample,
                dependent=outcome,
                rhs_terms=[MAIN_SIGNAL],
                absorb_col="sic2",
                include_year=True,
                controls=controls,
            )
            coef = float(result.params.get(MAIN_SIGNAL, np.nan))
            se = float(result.bse.get(MAIN_SIGNAL, np.nan))
            pvalue = float(result.pvalues.get(MAIN_SIGNAL, np.nan))
            rows.append(
                {
                    "outcome": outcome,
                    "outcome_label": label,
                    "signal": MAIN_SIGNAL,
                    "coef": coef,
                    "se": se,
                    "pvalue": pvalue,
                    "stars": sig_stars(pvalue),
                    "nobs": int(result.nobs),
                    "adj_r2": adj_r2,
                    "outcome_mean": float(use[outcome].mean()),
                    "controls": ";".join(controls),
                    "fixed_effects": "sic2;year",
                    "cluster": "cik",
                }
            )
        except Exception as exc:  # noqa: BLE001
            rows.append(
                {
                    "outcome": outcome,
                    "outcome_label": label,
                    "signal": MAIN_SIGNAL,
                    "coef": np.nan,
                    "se": np.nan,
                    "pvalue": np.nan,
                    "stars": "",
                    "nobs": 0,
                    "adj_r2": np.nan,
                    "outcome_mean": np.nan,
                    "controls": ";".join(controls),
                    "fixed_effects": "sic2;year",
                    "cluster": "cik",
                    "error": str(exc),
                }
            )
    return pd.DataFrame(rows)


def _fmt(value: Any, digits: int = 4) -> str:
    if value is None:
        return ""
    try:
        value_float = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(value_float):
        return ""
    return f"{value_float:.{digits}f}"


def write_interpretation(
    *,
    output_path: Path,
    summary: dict[str, Any],
    descriptive: pd.DataFrame,
    regressions: pd.DataFrame,
) -> None:
    headline = regressions.loc[regressions["outcome"].isin(["ActShare", "CredAI", "AI_Focus"])].copy()
    lines = [
        "# Builder-Hides First-Pass Extension",
        "",
        "This is a coauthor extension starter, not a frozen v4.3 manuscript table.",
        "It asks whether firms with strong lagged real-AI activity disclose less actionable AI content.",
        "",
        "## Sample",
        "",
        f"- Rows: {summary['rows']:,}",
        f"- Firms: {summary['firms']:,}",
        f"- Years: {summary['year_min']} to {summary['year_max']}",
        f"- Right-tail rule: year-specific positive real-AI activity at or above the {summary['tail_quantile']:.0%} quantile.",
        f"- AI-talk-only restriction: {summary['ai_talk_only']}",
        f"- Lagged right-tail builder rows: {summary['top_builder_lagged_rows']:,}",
        f"- Lagged right-tail builder firms: {summary['top_builder_lagged_firms']:,}",
        "",
        "## Headline Regression Screen",
        "",
        "Each row regresses a disclosure outcome on the lagged right-tail-builder indicator with SIC2 and year fixed effects, controls, and firm-clustered standard errors.",
        "",
        "| Outcome | Coef. | SE | p-value | N |",
        "|---|---:|---:|---:|---:|",
    ]
    for _, row in headline.iterrows():
        coef = _fmt(row.get("coef")) + str(row.get("stars", ""))
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row.get("outcome_label", row.get("outcome", ""))),
                    coef,
                    _fmt(row.get("se")),
                    _fmt(row.get("pvalue"), 3),
                    str(int(row.get("nobs", 0))) if pd.notna(row.get("nobs", np.nan)) else "0",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Discipline",
            "",
        "- Treat this as a coauthor screening exercise, not as a causal or manuscript-ready result.",
            "- A negative coefficient on actionable or credible disclosure would be consistent with a builder-hides channel.",
            "- A positive coefficient would support the simpler validation channel that real AI builders also disclose more substantively.",
            "- If results are sensitive, inspect industry composition and the patent/application examples before rewriting the paper narrative.",
            "",
            "## Output Files",
            "",
            "- `builder_hides_descriptive.csv`",
            "- `builder_hides_regressions.csv`",
            "- `builder_hides_summary.json`",
            "",
        ]
    )
    output_path.write_text("\n".join(lines))


def run(
    annual_panel: Path,
    output_dir: Path,
    *,
    tail_quantile: float,
    min_year_positive: int,
    ai_talk_only: bool = False,
) -> dict[str, Path]:
    panel = pd.read_parquet(annual_panel)
    sample, summary = prepare_panel(
        panel,
        tail_quantile=tail_quantile,
        min_year_positive=min_year_positive,
        ai_talk_only=ai_talk_only,
    )
    desc = descriptive_table(sample)
    regs = regression_table(sample)
    output_dir.mkdir(parents=True, exist_ok=True)
    desc_path = output_dir / "builder_hides_descriptive.csv"
    regs_path = output_dir / "builder_hides_regressions.csv"
    summary_path = output_dir / "builder_hides_summary.json"
    memo_path = output_dir / "builder_hides_interpretation.md"
    desc.to_csv(desc_path, index=False)
    regs.to_csv(regs_path, index=False)
    summary_payload = {
        **summary,
        "annual_panel": str(annual_panel),
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "main_signal": MAIN_SIGNAL,
        "status": "extension_screen_not_v4_3_evidence",
    }
    summary_path.write_text(json.dumps(summary_payload, indent=2, sort_keys=True) + "\n")
    write_interpretation(output_path=memo_path, summary=summary_payload, descriptive=desc, regressions=regs)
    return {
        "descriptive": desc_path,
        "regressions": regs_path,
        "summary": summary_path,
        "memo": memo_path,
    }


def main() -> int:
    args = _parse_args()
    if not 0 < args.tail_quantile < 1:
        raise ValueError("--tail-quantile must be between 0 and 1")
    annual_panel = (args.annual_panel or default_annual_panel()).resolve()
    output_dir = (args.output_dir or default_output_dir()).resolve()
    outputs = run(
        annual_panel,
        output_dir,
        tail_quantile=args.tail_quantile,
        min_year_positive=args.min_year_positive,
        ai_talk_only=args.ai_talk_only,
    )
    print("Builder-hides first-pass extension written:")
    for label, path in outputs.items():
        print(f"- {label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
