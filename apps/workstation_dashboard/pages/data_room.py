from __future__ import annotations

import streamlit as st

from components.ui import command_box, dataframe_or_info, hero
from services.manifest_store import DashboardData, filter_frame
from state import DEMO_MODE

COLUMNS = ["product_id", "purpose", "coverage", "keys", "logical_private_path", "overwrite_rule", "extension_relevance"]


def render(data: DashboardData, mode: str) -> None:
    hero("Data Room", "Browse the cleaned panels, classifier outputs, patent artifacts, and WRDS-derived data products.")
    if mode == DEMO_MODE:
        st.info("Demo Mode hides private-data-root commands and logical paths. Switch to Coauthor Mode when using the private data room.")

    query = st.text_input("Search data products", key="data_room_query")
    filtered = filter_frame(data.data_products, query)
    display = filtered.copy()
    if mode == DEMO_MODE and "logical_private_path" in display.columns:
        display["logical_private_path"] = "hidden in Demo Mode"
    dataframe_or_info(display, COLUMNS, empty_message="No matching data products.")
    if filtered.empty:
        return

    selected = st.selectbox("Open data product", filtered["product_id"].tolist(), key="selected_data_product")
    row = filtered.loc[filtered["product_id"] == selected].iloc[0]
    st.markdown(f"## `{row['product_id']}`")
    st.write(row["purpose"])
    st.markdown(f"**Coverage:** {row['coverage']}")
    st.markdown(f"**Keys:** {row['keys']}")
    st.markdown(f"**Source lineage:** {row['source_lineage']}")
    if mode != DEMO_MODE:
        st.markdown(f"**Logical private path:** `{row['logical_private_path']}`")
    command_box(
        f"AIW_DATA_ROOT=/path/to/ai-washing-private-data make locate-data PRODUCT_ID={row['product_id']} PREVIEW=1",
        mode=mode,
        allow_demo=False,
    )
