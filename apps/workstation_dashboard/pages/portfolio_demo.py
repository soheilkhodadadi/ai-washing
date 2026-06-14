from __future__ import annotations

import streamlit as st

from components.ui import hero
from services.manifest_store import DashboardData


def render(data: DashboardData, mode: str) -> None:
    hero("Portfolio Demo Mode", "A nonprivate view of the workstation as a reproducible AI, NLP, and finance analytics product.")
    st.info("This page is designed for screenshots or demonstrations. It uses manifest metadata only and does not require private data.")

    st.subheader("Capabilities demonstrated")
    st.markdown(
        """
        - NLP extraction and classification of AI-related disclosures.
        - Patent matching and construct-validity review for AI capability signals.
        - WRDS/CRSP/Compustat-style empirical finance workflow.
        - Reproducible table, figure, and extension workbench.
        - Docker-backed coauthor setup and static/interactive dashboard layers.
        """
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Manuscript assets", len(data.tables))
    c2.metric("Data products", len(data.data_products))
    c3.metric("Extension lanes", len(data.extensions))

    st.subheader("What a client sees")
    st.write(
        "A structured research software product: paper results, data products, constructs, extension lanes, and reproducibility checks in one navigable interface."
    )
