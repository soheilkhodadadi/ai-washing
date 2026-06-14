from __future__ import annotations

import streamlit as st

from components.ui import command_box, hero
from services.constructs import CONSTRUCTS
from services.manifest_store import filter_frame
import pandas as pd


def render(mode: str) -> None:
    hero("Construct Audits", "Open the playbooks that define, validate, and stress-test the paper's main constructs.")
    df = pd.DataFrame(CONSTRUCTS)
    query = st.text_input("Search constructs", key="construct_query")
    filtered = filter_frame(df, query)
    for item in filtered.to_dict("records"):
        with st.expander(f"{item['title']} · `{item['id']}`", expanded=False):
            st.write(item["summary"])
            st.markdown(f"**Playbook:** `{item['doc']}`")
            command_box(item["command"], mode=mode)
