from __future__ import annotations

import streamlit as st

from components.ui import command_box, dataframe_or_info, hero
from services.manifest_store import DashboardData, filter_frame

DETAIL_COLUMNS = [
    "paper_label",
    "asset_id",
    "asset_type",
    "paper_section",
    "caption",
    "empirical_question",
    "primary_data_product",
    "main_constructs",
]


def render(data: DashboardData, mode: str) -> None:
    hero("Table Explorer", "Find the owning script, reference outputs, and safe modification notes for any paper asset.")
    query = st.text_input("Search tables and figures", key="table_explorer_query")
    filtered = filter_frame(data.tables, query)
    dataframe_or_info(filtered, DETAIL_COLUMNS, empty_message="No matching paper assets.")
    if filtered.empty:
        return

    selected = st.selectbox("Open asset", filtered["asset_id"].tolist(), key="selected_table_asset")
    row = data.tables.loc[data.tables["asset_id"] == selected].iloc[0]

    st.markdown(f"## {row['paper_label']} · `{row['asset_id']}`")
    left, right = st.columns([1.1, 1])
    with left:
        st.markdown("### What this result answers")
        st.write(row["empirical_question"])
        st.markdown(f"**Caption:** {row['caption']}")
        st.markdown(f"**Main constructs:** {row['main_constructs']}")
        st.markdown(f"**Extension relevance:** {row['extension_relevance']}")
    with right:
        st.markdown("### Implementation details")
        st.markdown(f"**Primary data product:** {row['primary_data_product']}")
        st.markdown(f"**Owning script:** `{row['script_module']}`")
        st.markdown(f"**Reference outputs:** `{row['reference_outputs']}`")
        st.markdown(f"**Safe modifications:** {row['safe_modifications']}")

    st.markdown("### Copy-ready commands")
    command_box(f"make export-table-workbench TABLE_ID={row['asset_id']}", mode=mode)
    command_box(row["make_command"], mode=mode, allow_demo=False)
