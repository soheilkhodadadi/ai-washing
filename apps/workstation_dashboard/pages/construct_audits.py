from __future__ import annotations

import pandas as pd
import streamlit as st

from components.ui import badges, command_box, hero
from services.audit_data import compact_metrics, construct_evidence, data_product_cards, load_all_audit_reports
from services.constructs import CONSTRUCTS
from services.manifest_store import DashboardData, filter_frame
from state import DEMO_MODE


def _render_construct_panel(item: dict[str, str], data_products: pd.DataFrame, reports, *, mode: str) -> None:
    panel = construct_evidence(item["id"], data_products, reports)
    with st.expander(f"{item['title']} · `{item['id']}`", expanded=item["id"] in {"ai_disclosure", "patent_mismatch"}):
        badges([panel.status])
        st.write(item["summary"])
        st.markdown(f"**Playbook:** `{item['doc']}`")
        st.markdown(f"**Audit orientation:** {panel.summary}")
        if panel.products:
            st.markdown("**Relevant data products**")
            badges(panel.products)
        metrics = compact_metrics(panel.metrics)
        if not metrics.empty:
            st.markdown("**Audit checks and headline counts**")
            st.dataframe(metrics, width="stretch", hide_index=True)
        if panel.docs:
            st.markdown("**Reference notes**")
            for doc in panel.docs:
                st.markdown(f"- `{doc}`")
        command_box(item["command"], mode=mode, label="Open construct info", tags=["read-only"])
        for command in panel.commands:
            command_box(
                command["command"],
                mode=mode,
                allow_demo=False if "requires private data" in command.get("tags", "") else True,
                label=command["label"],
                tags=[command.get("tags", "")],
            )


def render(data: DashboardData, mode: str) -> None:
    hero(
        "Construct Audits",
        "Inspect construct definitions, validation surfaces, acronym-risk status, patent-match confidence, and WRDS lane checks.",
    )
    if mode == DEMO_MODE:
        st.info("Demo Mode keeps construct summaries visible but hides private-data commands.")

    reports = load_all_audit_reports()
    products = data_product_cards(data.data_products, reports)

    st.subheader("What to inspect first")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Classifier evidence**")
        st.caption("Final classifier outputs, extracted sentences, held-out support, and acronym-risk status.")
        command_box("make construct-info CONSTRUCT=ai_disclosure", mode=mode, label="Disclosure construct", tags=["read-only"])
    with c2:
        st.markdown("**Patent match evidence**")
        st.caption("Grant/pregrant examples, keyword metadata, company identity aliases, and red-flag counts.")
        command_box("make construct-info CONSTRUCT=patent_mismatch", mode=mode, label="PatentMismatch construct", tags=["read-only"])
    with c3:
        st.markdown("**WRDS lane checks**")
        st.caption("Annual panel coverage, event sample coverage, and CRSP 2024 cutoff.")
        command_box("make validate-wrds-data", mode=mode, allow_demo=False, label="WRDS validation", tags=["requires private data"])

    st.divider()
    df = pd.DataFrame(CONSTRUCTS)
    query = st.text_input("Search constructs", key="construct_query")
    filtered = filter_frame(df, query)
    for item in filtered.to_dict("records"):
        _render_construct_panel(item, products, reports, mode=mode)
