from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from semantic_ai_washing.analysis.ken_french_factors import stage_ken_french_monthly_factors


def test_stage_ken_french_monthly_factors_reuses_cached_parquet_without_raw_dirs(tmp_path: Path) -> None:
    factor_root = tmp_path / "factor_inputs"
    parsed = factor_root / "parsed"
    parsed.mkdir(parents=True)
    frame = pd.DataFrame(
        {
            "month": pd.period_range("2020-01", periods=2, freq="M"),
            "mkt_rf": [0.01, 0.02],
            "smb": [0.0, 0.0],
            "hml": [0.0, 0.0],
            "rmw": [0.0, 0.0],
            "cma": [0.0, 0.0],
            "rf": [0.001, 0.001],
            "mom": [0.03, 0.04],
        }
    )
    frame.to_parquet(parsed / "ff5_momentum_monthly.parquet", index=False)
    (parsed / "factor_bundle_manifest.json").write_text(
        json.dumps({"row_count": 2, "month_min": "2020-01", "month_max": "2020-02"}),
        encoding="utf-8",
    )

    out, manifest = stage_ken_french_monthly_factors(factor_root)

    assert len(out) == 2
    assert manifest["cache_status"] == "reused"
    assert not (factor_root / "raw").exists()
    assert not (factor_root / "extracted").exists()
