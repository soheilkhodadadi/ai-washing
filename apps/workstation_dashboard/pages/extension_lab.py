from __future__ import annotations

import streamlit as st

from components.ui import command_box, dataframe_or_info, hero
from services.manifest_store import DashboardData, filter_frame

COLUMNS = ["extension_id", "title", "research_question", "current_status", "interpretation_limits"]


def render(data: DashboardData, mode: str) -> None:
    hero("Extension Lab", "Inspect follow-on tests without mixing exploratory evidence into the frozen v4.3 release.")
    query = st.text_input("Search extension lanes", key="extension_query")
    filtered = filter_frame(data.extensions, query)
    dataframe_or_info(filtered, COLUMNS, empty_message="No matching extension lanes.")
    if filtered.empty:
        return

    selected = st.selectbox("Open extension", filtered["extension_id"].tolist(), key="selected_extension")
    row = filtered.loc[filtered["extension_id"] == selected].iloc[0]
    st.markdown(f"## {row['title']}")
    st.write(row["research_question"])
    st.markdown(f"**Current status:** {row['current_status']}")
    st.markdown(f"**Primary data product:** {row['primary_data_product']}")
    st.markdown(f"**Interpretation limits:** {row['interpretation_limits']}")
    st.markdown(f"**Docs:** `{row['docs']}`")
    command_box(row["make_command"], mode=mode, allow_demo=False)
