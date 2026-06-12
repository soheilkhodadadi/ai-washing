from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_script(name: str):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_package_surface_flags_coauthor_note_as_journal_excluded() -> None:
    module = _load_script("package_surface_audit")
    row = module.classify_tracked("docs/coauthor_share_note.md")
    assert row["severity"] == "manageable"
    assert row["coauthor_profile"] == "include"
    assert row["journal_profile"] == "exclude"


def test_package_surface_blocks_tracked_private_data() -> None:
    module = _load_script("package_surface_audit")
    row = module.classify_tracked("data/processed/panel/example.parquet")
    assert row["severity"] == "stop_the_line"
    assert row["journal_profile"] == "exclude"


def test_textual_short_acronym_detection_distinguishes_long_anchor() -> None:
    module = _load_script("textual_construct_audit")
    assert module.short_acronym_only("We use AI to improve workflow.")
    assert not module.short_acronym_only("We use artificial intelligence to improve workflow.")
    assert not module.short_acronym_only("We use machine learning and AI to improve workflow.")


def test_textual_ml_unit_context_detection() -> None:
    module = _load_script("textual_construct_audit")
    assert module.ml_unit_context("The vial contains 10 ml of solution.")
    assert not module.ml_unit_context("The machine learning model improves routing.")
    assert not module.ml_unit_context("The AI/ML solution improves routing.")


def test_patent_short_only_keyword_detection() -> None:
    module = _load_script("patent_construct_audit")
    assert module.short_only_keywords("ml")
    assert module.short_only_keywords("ai | ml")
    assert not module.short_only_keywords("machine learning | neural network")


def test_journal_audit_normalizes_pytest_runtime() -> None:
    module = _load_script("journal_reproducibility_audit")
    output = ".......................... [100%]\n26 passed in 4.42s"
    assert module.normalize_output(output).endswith("26 passed in <runtime>s")
