from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]


@st.cache_data(show_spinner=False)
def load_manifest(name: str) -> pd.DataFrame:
    path = ROOT / "manifests" / name
    return pd.read_csv(path).fillna("")


def command_box(command: str) -> None:
    if command:
        st.code(command, language="bash")


def filter_frame(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if not query:
        return df
    mask = df.astype(str).agg(" ".join, axis=1).str.lower().str.contains(query.lower(), regex=False)
    return df.loc[mask]


def overview(tables: pd.DataFrame, data_products: pd.DataFrame, extensions: pd.DataFrame) -> None:
    st.title("AI Washing Workstation")
    st.caption("Read-only coauthor dashboard generated from manifests. It does not expose private data values or execute commands.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Paper assets", len(tables))
    c2.metric("Figures", int((tables["asset_type"] == "figure").sum()))
    c3.metric("Data products", len(data_products))
    c4.metric("Extensions", len(extensions))

    section_counts = tables.groupby("paper_section", dropna=False).size().reset_index(name="count")
    fig = px.bar(section_counts, x="paper_section", y="count", color="paper_section", title="Paper assets by section")
    fig.update_layout(showlegend=False, xaxis_title="Paper section", yaxis_title="Assets")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("First commands")
    command_box("make export-table-workbench TABLE_ID=T30")
    command_box("AIW_DATA_ROOT=/path/to/ai-washing-private-data make locate-data PRODUCT_ID=final_hybrid_classifier_outputs PREVIEW=1")
    command_box("AIW_DATA_ROOT=/path/to/ai-washing-private-data make extension-builder-hides")


def tables_view(tables: pd.DataFrame) -> None:
    st.title("Tables & Figures")
    query = st.text_input("Search paper assets", key="table_query")
    filtered = filter_frame(tables, query)
    st.dataframe(
        filtered[["paper_label", "asset_id", "asset_type", "paper_section", "caption", "script_module", "make_command"]],
        use_container_width=True,
        hide_index=True,
    )
    selected = st.selectbox("Open asset", filtered["asset_id"].tolist() if not filtered.empty else [])
    if selected:
        row = tables.loc[tables["asset_id"] == selected].iloc[0]
        st.subheader(f"{row['paper_label']} ({row['asset_id']})")
        st.write(row["empirical_question"])
        st.markdown(f"**Primary data product:** {row['primary_data_product']}")
        st.markdown(f"**Owning script:** `{row['script_module']}`")
        st.markdown(f"**Safe modifications:** {row['safe_modifications']}")
        command_box(f"make export-table-workbench TABLE_ID={row['asset_id']}")
        command_box(row["make_command"])


def data_view(data_products: pd.DataFrame) -> None:
    st.title("Data Products")
    query = st.text_input("Search data products", key="data_query")
    filtered = filter_frame(data_products, query)
    st.dataframe(
        filtered[["product_id", "purpose", "coverage", "keys", "logical_private_path", "overwrite_rule"]],
        use_container_width=True,
        hide_index=True,
    )
    selected = st.selectbox("Open data product", filtered["product_id"].tolist() if not filtered.empty else [])
    if selected:
        row = data_products.loc[data_products["product_id"] == selected].iloc[0]
        st.subheader(row["product_id"])
        st.write(row["purpose"])
        st.markdown(f"**Logical private path:** `{row['logical_private_path']}`")
        st.markdown(f"**Coverage:** {row['coverage']}")
        command_box(f"AIW_DATA_ROOT=/path/to/ai-washing-private-data make locate-data PRODUCT_ID={row['product_id']} PREVIEW=1")


def constructs_view() -> None:
    st.title("Construct Playbooks")
    playbooks = [
        ("ai_disclosure", "AI disclosure and classifier constructs", "docs/construct_playbooks/ai_disclosure_and_classifier_constructs.md"),
        ("patent_mismatch", "PatentMismatch construct", "docs/construct_playbooks/patent_mismatch_construct.md"),
        ("patent_matching", "Patent matching and company identity", "docs/construct_playbooks/patent_matching_and_company_identity.md"),
        ("market_returns", "CRSP/Compustat linkage and market tests", "docs/construct_playbooks/crsp_compustat_linkage_and_market_return_tests.md"),
        ("capital_raising", "Capital-raising proxy", "docs/construct_playbooks/capital_raising_proxy.md"),
        ("execucomp", "ExecuComp incentives", "docs/construct_playbooks/execucomp_incentives.md"),
        ("sec_scrutiny", "SEC scrutiny and enforcement timing", "docs/construct_playbooks/sec_scrutiny_enforcement_timing.md"),
    ]
    for key, title, path in playbooks:
        with st.expander(title):
            st.markdown(f"Path: `{path}`")
            command_box(f"make construct-info CONSTRUCT={key}")


def extensions_view(extensions: pd.DataFrame) -> None:
    st.title("Extension Lanes")
    query = st.text_input("Search extensions", key="extension_query")
    filtered = filter_frame(extensions, query)
    st.dataframe(
        filtered[["extension_id", "title", "research_question", "current_status", "make_command", "interpretation_limits"]],
        use_container_width=True,
        hide_index=True,
    )
    selected = st.selectbox("Open extension", filtered["extension_id"].tolist() if not filtered.empty else [])
    if selected:
        row = extensions.loc[extensions["extension_id"] == selected].iloc[0]
        st.subheader(row["title"])
        st.write(row["research_question"])
        st.markdown(f"**Status:** {row['current_status']}")
        st.markdown(f"**Interpretation limits:** {row['interpretation_limits']}")
        command_box(row["make_command"])


def main() -> None:
    st.set_page_config(page_title="AI Washing Workstation", layout="wide")
    tables = load_manifest("paper_table_workbench.csv")
    data_products = load_manifest("data_product_catalog.csv")
    extensions = load_manifest("extension_workbench.csv")

    st.sidebar.title("AI Washing")
    page = st.sidebar.radio(
        "Navigate",
        ["Overview", "Tables & Figures", "Data Products", "Constructs", "Extensions"],
    )
    st.sidebar.info("This app reads manifests only. It does not inspect private data or execute commands.")

    if page == "Overview":
        overview(tables, data_products, extensions)
    elif page == "Tables & Figures":
        tables_view(tables)
    elif page == "Data Products":
        data_view(data_products)
    elif page == "Constructs":
        constructs_view()
    elif page == "Extensions":
        extensions_view(extensions)


if __name__ == "__main__":
    main()
