from __future__ import annotations

import pandas as pd
import streamlit as st

from services.manifest_store import DashboardData, load_manifest, public_frame


@st.cache_data(show_spinner=False)
def load_manifest_cached(name: str) -> pd.DataFrame:
    return public_frame(load_manifest(name))


@st.cache_data(show_spinner=False)
def load_dashboard_data_cached() -> DashboardData:
    return DashboardData(
        tables=load_manifest_cached("paper_table_workbench.csv"),
        data_products=load_manifest_cached("data_product_catalog.csv"),
        extensions=load_manifest_cached("extension_workbench.csv"),
    )
