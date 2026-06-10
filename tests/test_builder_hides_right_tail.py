from __future__ import annotations

from pathlib import Path

import pandas as pd

from semantic_ai_washing.analysis.extensions.builder_hides_right_tail import (
    _top_tail_by_year,
    prepare_panel,
    run,
)


def test_top_tail_by_year_requires_positive_observations() -> None:
    frame = pd.DataFrame(
        {
            "year": [2020, 2020, 2020, 2021, 2021, 2021],
            "value": [0, 0, 0, 1, 2, 10],
        }
    )

    flags = _top_tail_by_year(frame, "value", quantile=0.80, min_year_positive=2)

    assert flags.iloc[:3].sum() == 0
    assert flags.iloc[5] == 1


def test_prepare_panel_creates_lagged_builder_signal() -> None:
    panel = pd.DataFrame(
        {
            "cik": [str(i) for i in range(1, 7)],
            "year": [2020] * 6,
            "sic": [3570] * 6,
            "any_ai_talk": [1] * 6,
            "patents_ai": [0, 0, 1, 2, 5, 20],
            "applications_ai": [0, 0, 0, 1, 2, 10],
            "patents_ai_lag1": [0, 1, 2, 3, 4, 30],
            "applications_ai_lag1": [0, 0, 1, 1, 2, 20],
            "A_S": [0.2, 0.5, 1.0, 1.2, 0.8, 0.4],
            "SpecShare": [0.4, 0.3, 0.2, 0.2, 0.1, 0.5],
            "ActShare": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            "CredAI": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            "AI_Focus": [0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
            "share_A": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            "share_S": [0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
            "SpecMinusAct": [0.5, 0.3, 0.1, -0.1, -0.3, -0.5],
            "ln_assets": [1, 1, 1, 1, 1, 1],
            "leverage": [0.1] * 6,
            "cash": [0.2] * 6,
            "rd_intensity": [0.03] * 6,
            "capx_at": [0.02] * 6,
            "roa": [0.04] * 6,
            "sales_growth": [0.05] * 6,
        }
    )

    prepared, summary = prepare_panel(panel, tail_quantile=0.80, min_year_positive=2)

    assert "top_builder_lagged" in prepared.columns
    assert prepared["top_builder_lagged"].sum() == 1
    assert summary["top_builder_lagged_rows"] == 1
    assert summary["ai_talk_only"] is False


def test_builder_hides_run_writes_outputs(tmp_path: Path) -> None:
    rows = []
    for year in [2020, 2021, 2022]:
        for i in range(1, 9):
            rows.append(
                {
                    "cik": f"{year}{i}",
                    "year": year,
                    "sic": 3500 + i,
                    "any_ai_talk": 1,
                    "patents_ai": i,
                    "applications_ai": i // 2,
                    "patents_ai_lag1": i + 1,
                    "applications_ai_lag1": i // 2,
                    "A_S": 0.1 * i,
                    "SpecShare": 0.05 * i,
                    "ActShare": 0.04 * i,
                    "CredAI": 0.03 * i,
                    "AI_Focus": 0.01 * i,
                    "share_A": 0.04 * i,
                    "share_S": 0.02 * i,
                    "SpecMinusAct": -0.02 * i,
                    "ln_assets": 5 + i,
                    "leverage": 0.1,
                    "cash": 0.2,
                    "rd_intensity": 0.03,
                    "capx_at": 0.02,
                    "roa": 0.04,
                    "sales_growth": 0.05,
                }
            )
    panel_path = tmp_path / "panel.parquet"
    pd.DataFrame(rows).to_parquet(panel_path)

    outputs = run(panel_path, tmp_path / "out", tail_quantile=0.80, min_year_positive=2)

    assert outputs["descriptive"].exists()
    assert outputs["regressions"].exists()
    assert outputs["summary"].exists()
    assert outputs["memo"].exists()
