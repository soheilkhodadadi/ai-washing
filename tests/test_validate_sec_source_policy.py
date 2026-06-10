from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_sec_source_policy.py"


def _write_manifest(path: Path, rows: list[str]) -> None:
    path.write_text(
        "artifact_id,logical_path,role,required,expected_format,expected_files,expected_rows,expected_year_min,expected_year_max,required_urls,notes\n"
        + "\n".join(rows)
        + "\n",
        encoding="utf-8",
    )


def test_validate_sec_source_policy_accepts_samples_links_and_parquet(tmp_path: Path) -> None:
    data_root = tmp_path / "private"
    samples = data_root / "raw" / "sec_samples" / "full_submission"
    samples.mkdir(parents=True)
    (samples / "AAPL_10-K_full-submission.txt").write_text("sample filing", encoding="utf-8")
    links = data_root / "docs" / "source_links" / "sec_stage_one_sources.md"
    links.parent.mkdir(parents=True)
    links.write_text("https://example.com/source\n", encoding="utf-8")
    parquet_dir = data_root / "processed" / "sec" / "sentences_clean" / "year=2025"
    parquet_dir.mkdir(parents=True)
    pd.DataFrame({"sentence": ["AI example", "ML example"]}).to_parquet(parquet_dir / "ai_sentences.parquet")

    manifest = tmp_path / "sec_manifest.csv"
    _write_manifest(
        manifest,
        [
            "samples,data/raw/sec_samples/full_submission,raw_source_sample,yes,txt_directory,1,,,,,fixture",
            "links,data/docs/source_links/sec_stage_one_sources.md,source_links,yes,markdown,1,,,,https://example.com/source,fixture",
            "sentences,data/processed/sec/sentences_clean,extracted_sentences,yes,parquet_directory,1,2,2025,2025,,fixture",
        ],
    )

    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--manifest", str(manifest), "--data-root", str(data_root)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "- present: 3" in result.stdout


def test_validate_sec_source_policy_fails_missing_required_artifact(tmp_path: Path) -> None:
    manifest = tmp_path / "sec_manifest.csv"
    _write_manifest(
        manifest,
        ["samples,data/raw/sec_samples/full_submission,raw_source_sample,yes,txt_directory,1,,,,,fixture"],
    )

    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--manifest", str(manifest), "--data-root", str(tmp_path / "private")],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "missing_required: samples" in result.stdout
