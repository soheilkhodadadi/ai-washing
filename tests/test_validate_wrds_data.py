from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_wrds_data.py"


def _write_manifest(path: Path, logical_path: str, role: str = "required_reproduction") -> None:
    path.write_text(
        "artifact_id,logical_path,role,expected_format,expected_rows,date_column,expected_date_min,expected_date_max,year_column,expected_year_min,expected_year_max,required_columns,notes\n"
        f"sample,{logical_path},{role},csv,2,date,2020-01-02,2020-01-03,year,2020,2020,id;date;year,value,fixture\n"
    )


def test_validate_wrds_data_accepts_matching_tabular_artifact(tmp_path: Path) -> None:
    data_root = tmp_path / "private"
    artifact = data_root / "interim" / "market" / "sample.csv"
    artifact.parent.mkdir(parents=True)
    pd.DataFrame(
        [
            {"id": 1, "date": "2020-01-02", "year": 2020, "value": 10},
            {"id": 2, "date": "2020-01-03", "year": 2020, "value": 20},
        ]
    ).to_csv(artifact, index=False)
    manifest = tmp_path / "manifest.csv"
    _write_manifest(manifest, "data/interim/market/sample.csv")

    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--manifest", str(manifest), "--data-root", str(data_root)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "- present: 1" in result.stdout


def test_validate_wrds_data_fails_missing_required_artifact(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.csv"
    _write_manifest(manifest, "data/interim/market/missing.csv")

    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--manifest", str(manifest), "--data-root", str(tmp_path / "private")],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "missing_required: sample" in result.stdout
