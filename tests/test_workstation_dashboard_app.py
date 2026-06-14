from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "apps" / "workstation_dashboard"
sys.path.insert(0, str(APP_DIR))

from services.manifest_store import dashboard_text_is_safe, load_dashboard_data, public_frame  # noqa: E402
from services.page_registry import PAGE_SPECS  # noqa: E402


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
