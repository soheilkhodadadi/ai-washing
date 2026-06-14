from __future__ import annotations

from io import BytesIO
import sys
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "apps" / "workstation_dashboard"
sys.path.insert(0, str(APP_DIR))

from services.manifest_store import dashboard_text_is_safe, load_dashboard_data, public_frame  # noqa: E402
from services.page_registry import PAGE_SPECS  # noqa: E402
from services.table_artifacts import (  # noqa: E402
    REFERENCE_STATUS,
    build_review_packet,
    csv_preview,
    preferred_review_artifact,
    safe_repo_path,
    table_artifacts,
    table_display_label,
)


def test_dashboard_page_specs_are_complete() -> None:
    expected = {
        "home",
        "paper_results",
        "table_explorer",
        "data_room",
        "construct_audits",
        "extension_lab",
        "reproduction_status",
        "share_export",
        "portfolio_demo",
    }
    keys = {spec["key"] for spec in PAGE_SPECS}
    assert keys == expected
    required = {"group", "key", "title", "icon", "primary_user", "task", "inputs", "outputs", "safety_rule"}
    for spec in PAGE_SPECS:
        assert required <= set(spec)
        assert all(str(spec[field]).strip() for field in required)


def test_dashboard_manifests_load_from_canonical_contract() -> None:
    data = load_dashboard_data()
    assert len(data.tables) == 26
    assert len(data.data_products) >= 10
    assert len(data.extensions) >= 3
    assert {"asset_id", "paper_label", "script_module", "make_command"} <= set(data.tables.columns)
    assert {"product_id", "logical_private_path", "coverage"} <= set(data.data_products.columns)
    assert {"extension_id", "make_command", "interpretation_limits"} <= set(data.extensions.columns)


def test_manifest_text_used_by_dashboard_is_public_safe() -> None:
    data = load_dashboard_data()
    text = "\n".join(
        [
            public_frame(data.tables).astype(str).to_csv(index=False),
            public_frame(data.data_products).astype(str).to_csv(index=False),
            public_frame(data.extensions).astype(str).to_csv(index=False),
        ]
    )
    assert dashboard_text_is_safe(text)


def test_main_table_7_maps_to_t30_and_paper_label_display() -> None:
    data = load_dashboard_data()
    row = data.tables.loc[data.tables["paper_label"] == "Main Table 7"].iloc[0]
    assert row["asset_id"] == "T30"
    label = table_display_label(row)
    assert label.startswith("Main Table 7 - Capital-raising timing")
    assert "T30" not in label


def test_t30_artifact_resolution_finds_review_and_audit_formats() -> None:
    data = load_dashboard_data()
    row = data.tables.loc[data.tables["asset_id"] == "T30"].iloc[0]
    artifacts = table_artifacts(row)
    suffixes = {artifact.suffix for artifact in artifacts if artifact.exists}
    labels = "\n".join(artifact.label for artifact in artifacts)

    assert {".csv", ".tex", ".docx", ".pdf", ".png", ".md"} <= suffixes
    assert any(artifact.status == REFERENCE_STATUS for artifact in artifacts)
    assert "writer packet" in labels
    assert "result notes" in labels
    assert preferred_review_artifact(artifacts) is not None


def test_safe_repo_path_rejects_private_absolute_and_old_local_paths() -> None:
    assert safe_repo_path("data/curated/v4_3/generated_exports") is not None
    assert safe_repo_path("/Users/soheilkhodadadi/DataWork/ai-washing-private-data/panel.parquet") is None
    assert safe_repo_path("../../../outside.csv") is None
    assert safe_repo_path("DataWork/semantic-patterns/paper/generated/table.csv") is None
    assert safe_repo_path("$AIW_DATA_ROOT/panel.parquet") is None


def test_t30_csv_preview_is_capped_and_repo_contained() -> None:
    data = load_dashboard_data()
    row = data.tables.loc[data.tables["asset_id"] == "T30"].iloc[0]
    csv_artifact = next(artifact for artifact in table_artifacts(row) if artifact.previewable_csv)
    preview = csv_preview(csv_artifact, max_rows=3)
    assert len(preview) <= 3
    assert "Outcome" in preview.columns


def test_review_packet_contains_only_safe_artifacts() -> None:
    data = load_dashboard_data()
    row = data.tables.loc[data.tables["asset_id"] == "T30"].iloc[0]
    packet = build_review_packet(row, table_artifacts(row))
    with zipfile.ZipFile(BytesIO(packet)) as zf:
        names = zf.namelist()
        text = "\n".join(names)
        text += "\n" + zf.read("OPEN_FIRST.md").decode("utf-8")
    assert "OPEN_FIRST.md" in names
    assert "/Users/soheilkhodadadi" not in text
    assert "DataWork/semantic-patterns" not in text
