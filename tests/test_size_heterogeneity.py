from __future__ import annotations

from pathlib import Path
import warnings

import pandas as pd

from semantic_ai_washing.analysis.publication_runs import test_05_size_heterogeneity as size_mod


def test_prepare_sample_uses_nullable_small_indicator_without_futurewarning(monkeypatch, tmp_path: Path) -> None:
    base_sample = pd.DataFrame(
        {
            "is_ai_filing": [True, True, True],
            "permno": ["10001", "10002", "10003"],
            "filing_date": ["2020-03-15", "2020-03-20", "2020-04-15"],
            "filing_year": [2020, 2020, 2020],
        }
    )
    monthly = pd.DataFrame(
        {
            "permno": ["10001", "10002", "10003"],
            "month": pd.PeriodIndex(["2020-03", "2020-03", "2020-04"], freq="M"),
            "lag_mcap": [10.0, 30.0, 20.0],
        }
    )
    monkeypatch.setattr(size_mod, "_build_analysis_sample", lambda event_panel, annual_panel: base_sample.copy())
    monkeypatch.setattr(size_mod, "_load_monthly_returns", lambda monthly_returns: monthly.copy())

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        sample, summary = size_mod._prepare_sample(tmp_path / "event.parquet", tmp_path / "annual.parquet", tmp_path / "monthly.parquet")

    assert not [item for item in caught if issubclass(item.category, FutureWarning)]
    assert str(sample["Small"].dtype) == "Int64"
    assert summary["small_count"] == 2
    assert summary["big_count"] == 1
