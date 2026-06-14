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
from services.technical_drilldown import (  # noqa: E402
    command_set,
    crosswalk_for_asset,
    data_product_path_statuses,
    linked_constructs,
    linked_data_products,
    linked_extensions,
    source_script_for_module,
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


def test_t30_technical_drilldown_resolves_script_data_construct_and_extension() -> None:
    data = load_dashboard_data()
    row = data.tables.loc[data.tables["asset_id"] == "T30"].iloc[0]
    crosswalk = crosswalk_for_asset("T30")
    script = source_script_for_module(row["script_module"])
    products = linked_data_products(row, data.data_products)
    constructs = linked_constructs(row)
    extensions = linked_extensions(row, data.extensions)

    assert crosswalk is not None
    assert crosswalk["test_id"] == "test_30_capital_raising_timing"
    assert script.exists
    assert script.rel_path.endswith("test_30_capital_raising_timing.py")
    assert "annual_nlp_patent_panel" in set(products["product_id"])
    assert "capital_raising" in {construct["id"] for construct in constructs}
    assert "washing_pays_proxy" in set(extensions["extension_id"])


def test_every_table_has_drilldown_commands() -> None:
    data = load_dashboard_data()
    for _, row in data.tables.iterrows():
        products = linked_data_products(row, data.data_products)
        extensions = linked_extensions(row, data.extensions)
        commands = command_set(row, products, extensions)
        labels = {item["label"] for item in commands}
        assert "Export table bundle" in labels
        assert "Rerun table" in labels
        assert "Show owning script" in labels
        assert all(item["command"].strip() for item in commands)


def test_data_product_status_reports_metadata_only(monkeypatch, tmp_path: Path) -> None:
    import duckdb

    private_root = tmp_path / "private"
    panel_path = private_root / "processed" / "panel" / "example.parquet"
    panel_path.parent.mkdir(parents=True)
    import pandas as pd

    pd.DataFrame({"cik": ["0001", "0002"], "secret_value": ["alpha", "beta"]}).to_parquet(panel_path)
    monkeypatch.setenv("AIW_DATA_ROOT", str(private_root))
    status = data_product_path_statuses({"logical_private_path": "data/processed/panel/example.parquet"})[0]
    payload = status.to_public_dict()

    assert duckdb.__version__
    assert status.status == "present"
    assert status.kind == "file"
    assert status.row_count == 2
    assert "secret_value" in status.columns
    assert "alpha" not in str(payload)
    assert "beta" not in str(payload)
    assert str(tmp_path) not in payload["display_path"]


def test_data_product_status_rejects_unsafe_paths(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("AIW_DATA_ROOT", str(tmp_path))
    statuses = data_product_path_statuses({"logical_private_path": "/tmp/private.csv; ../outside.csv"})
    assert [status.status for status in statuses] == ["not_resolved", "not_resolved"]
    assert all(status.kind == "reference" for status in statuses)
