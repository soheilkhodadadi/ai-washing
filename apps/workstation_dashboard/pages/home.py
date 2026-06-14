from __future__ import annotations

import plotly.express as px
import streamlit as st

from components.ui import command_box, hero, safety_banner
from services.manifest_store import DashboardData


def render(data: DashboardData, mode: str) -> None:
    hero(
        "AI Washing Workstation",
        "A reproducible empirical dashboard for reviewing paper results, locating data products, and planning extension tests.",
    )
    safety_banner(mode)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Paper assets", len(data.tables))
    c2.metric("Figures", int((data.tables["asset_type"] == "figure").sum()))
    c3.metric("Data products", len(data.data_products))
    c4.metric("Extensions", len(data.extensions))

    left, right = st.columns([1.25, 1])
    with left:
        st.subheader("What this dashboard is for")
        st.markdown(
            """
            - Review the paper in table-and-figure order.
            - Locate the exact scripts, data products, and construct playbooks behind each result.
            - Inspect extension lanes without confusing exploratory outputs with frozen v4.3 evidence.
            - Use Docker/Make for reproducibility; use the dashboard for navigation and presentation.
            """
        )
    with right:
        counts = data.tables.groupby("paper_section", dropna=False).size().reset_index(name="count")
        fig = px.bar(counts, x="paper_section", y="count", color="paper_section", title="Assets by paper section")
        fig.update_layout(showlegend=False, xaxis_title="Section", yaxis_title="Assets", height=350)
        st.plotly_chart(fig, width="stretch")

    st.subheader("Recommended first actions")
    command_box("make workbench-index", mode=mode)
    command_box("make export-table-workbench TABLE_ID=T30", mode=mode)
    command_box(
        "AIW_DATA_ROOT=/path/to/ai-washing-private-data make locate-data PRODUCT_ID=final_hybrid_classifier_outputs PREVIEW=1",
        mode=mode,
        allow_demo=False,
    )
