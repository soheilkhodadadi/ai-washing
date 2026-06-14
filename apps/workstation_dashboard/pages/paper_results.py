from __future__ import annotations

import streamlit as st

from components.ui import badges, command_box, hero
from services.manifest_store import DashboardData, filter_frame

TABLE_SELECTION_KEY = "selected_table_asset"


def _asset_card(row, mode: str) -> None:
    with st.container(border=True):
        st.markdown(f"### {row['paper_label']}: {row['caption']}")
        st.write(row["empirical_question"])
        badges([row["asset_type"], row["paper_section"], row["primary_data_product"]])
        st.caption(f"Technical ID: {row['asset_id']}")
        if st.button("Prepare review in Table Explorer", key=f"prepare_{row['asset_id']}"):
            st.session_state[TABLE_SELECTION_KEY] = row["asset_id"]
            st.query_params["asset"] = row["asset_id"]
            st.success("Selection saved. Open Table Explorer from the sidebar to review this table.")
        command_box(f"make export-table-workbench TABLE_ID={row['asset_id']}", mode=mode)


def render(data: DashboardData, mode: str) -> None:
    hero("Paper Results", "Review the manuscript assets in paper order before drilling into scripts or data products.")
    sections = ["All"] + sorted(section for section in data.tables["paper_section"].unique() if section)
    section = st.selectbox("Paper section", sections)
    query = st.text_input("Search results", placeholder="Try PatentMismatch, capital, market, appendix...")
    df = data.tables.copy()
    if section != "All":
        df = df.loc[df["paper_section"] == section]
    df = filter_frame(df, query)
    st.caption(f"Showing {len(df)} of {len(data.tables)} paper assets.")
    for _, row in df.iterrows():
        _asset_card(row, mode)
