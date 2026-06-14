from __future__ import annotations

import streamlit as st

from components.ui import badges, command_box, dataframe_or_info, hero
from services.audit_data import (
    compact_metrics,
    data_product_cards,
    evidence_panels,
    load_all_audit_reports,
    product_status_rows,
    product_validation_rows,
    report_inventory,
    status_counts,
)
from services.manifest_store import DashboardData, filter_frame
from state import DEMO_MODE

CATALOG_COLUMNS = [
    "product_id",
    "family",
    "contract_status",
    "validation_status",
    "coverage",
    "keys",
    "logical_private_path",
]


def _friendly_status(value: object) -> str:
    text = str(value or "").strip()
    return text or "not_available"


def _render_evidence_panel(panel, *, mode: str) -> None:
    with st.container(border=True):
        c1, c2 = st.columns([0.72, 0.28])
        with c1:
            st.subheader(panel.title)
            st.write(panel.summary)
        with c2:
            badges([panel.status])
        metrics = compact_metrics(panel.metrics)
        if not metrics.empty:
            st.dataframe(metrics, width="stretch", hide_index=True)
        if panel.products:
            st.markdown("**Inspect first**")
            badges(panel.products)
        if panel.docs:
            st.markdown("**Reference notes**")
            for doc in panel.docs:
                st.markdown(f"- `{doc}`")
        if panel.commands:
            with st.expander("Copy-ready audit commands", expanded=False):
                for item in panel.commands:
                    command_box(
                        item["command"],
                        mode=mode,
                        allow_demo=False if "requires private data" in item.get("tags", "") else True,
                        label=item["label"],
                        tags=[item.get("tags", "")],
                    )


def _render_product_detail(row, *, mode: str, reports) -> None:
    st.markdown(f"## `{row['product_id']}`")
    badges([row.get("family", ""), row.get("contract_status", ""), row.get("validation_status", "")])
    st.write(row["purpose"])
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Coverage:** {row['coverage']}")
        st.markdown(f"**Keys:** {row['keys']}")
        st.markdown(f"**Overwrite rule:** {row['overwrite_rule']}")
    with c2:
        st.markdown(f"**Extension relevance:** {row['extension_relevance']}")
        st.markdown(f"**Source lineage:** {row['source_lineage']}")
    if mode != DEMO_MODE:
        st.markdown(f"**Logical private path:** `{row['logical_private_path']}`")
    else:
        st.info("Demo Mode hides private-data-root paths and private-data commands.")

    status_df = product_status_rows(row) if mode != DEMO_MODE else None
    if status_df is not None and not status_df.empty:
        st.markdown("### Metadata-only path and schema status")
        st.caption("This section reports existence, size, row count, and column names only. It does not display private row values.")
        st.dataframe(
            status_df[["logical_path", "display_path", "status", "kind", "suffix", "file_count", "row_count", "columns", "note"]],
            width="stretch",
            hide_index=True,
        )

    validation = product_validation_rows(str(row["product_id"]), reports)
    if not validation.empty:
        st.markdown("### Validation checks")
        st.dataframe(validation[["artifact_id", "check_name", "severity", "status", "observed", "expected", "notes"]], width="stretch", hide_index=True)

    command_box(
        f"AIW_DATA_ROOT=/path/to/ai-washing-private-data make locate-data PRODUCT_ID={row['product_id']} PREVIEW=1",
        mode=mode,
        allow_demo=False,
        label="Locate this data product",
        tags=["requires private data", "metadata only"],
    )


def render(data: DashboardData, mode: str) -> None:
    hero(
        "Data Room",
        "Browse the cleaned panels, classifier outputs, patent artifacts, WRDS-derived products, and their audit status.",
    )
    if mode == DEMO_MODE:
        st.info("Demo Mode hides private-data-root paths and private-data commands while keeping high-level audit status visible.")

    reports = load_all_audit_reports()
    cards = data_product_cards(data.data_products, reports)

    st.subheader("Evidence cockpit")
    c1, c2, c3 = st.columns(3)
    c1.metric("Data products", len(cards))
    c2.metric("Contract statuses", ", ".join(f"{k}: {v}" for k, v in status_counts(cards, "contract_status").items()))
    c3.metric("Audit reports", f"{sum(1 for report in reports.values() if report.status == 'present')}/{len(reports)} present")

    panel_tabs = st.tabs(["Classifier evidence", "Patent evidence", "WRDS / market lanes"])
    for tab, panel in zip(panel_tabs, evidence_panels(cards, reports), strict=False):
        with tab:
            _render_evidence_panel(panel, mode=mode)

    st.divider()
    st.subheader("Data product catalog")
    family_options = ["all", *sorted(cards["family"].dropna().astype(str).unique())]
    contract_options = ["all", *sorted(cards["contract_status"].dropna().astype(str).unique())]
    validation_options = ["all", *sorted(cards["validation_status"].dropna().astype(str).unique())]
    f1, f2, f3 = st.columns(3)
    family = f1.selectbox("Family", family_options, key="data_room_family")
    contract = f2.selectbox("Contract status", contract_options, key="data_room_contract")
    validation_status = f3.selectbox("Validation status", validation_options, key="data_room_validation")
    query = st.text_input("Search data products", key="data_room_query")

    filtered = filter_frame(cards, query)
    if family != "all":
        filtered = filtered.loc[filtered["family"] == family]
    if contract != "all":
        filtered = filtered.loc[filtered["contract_status"] == contract]
    if validation_status != "all":
        filtered = filtered.loc[filtered["validation_status"] == validation_status]

    display = filtered.copy()
    if mode == DEMO_MODE and "logical_private_path" in display.columns:
        display["logical_private_path"] = "hidden in Demo Mode"
    display["contract_status"] = display["contract_status"].map(_friendly_status)
    display["validation_status"] = display["validation_status"].map(_friendly_status)
    dataframe_or_info(display, CATALOG_COLUMNS, empty_message="No matching data products.")
    if filtered.empty:
        return

    selected = st.selectbox("Open data product", filtered["product_id"].tolist(), key="selected_data_product")
    row = filtered.loc[filtered["product_id"] == selected].iloc[0]
    _render_product_detail(row, mode=mode, reports=reports)

    with st.expander("Audit report inventory", expanded=False):
        st.dataframe(report_inventory(reports), width="stretch", hide_index=True)
