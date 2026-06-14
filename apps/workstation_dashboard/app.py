from __future__ import annotations

import streamlit as st

from pages import (
    command_center,
    construct_audits,
    data_room,
    extension_lab,
    home,
    paper_results,
    portfolio_demo,
    reproduction_status,
    share_export,
    table_explorer,
)
from services.page_registry import PAGE_SPECS
from services.streamlit_data import load_dashboard_data_cached
from state import render_mode_selector
from styles import apply_styles


def _spec(key: str) -> dict[str, str]:
    return next(item for item in PAGE_SPECS if item["key"] == key)


def main() -> None:
    st.set_page_config(page_title="AI Washing Workstation", layout="wide", page_icon="🏛️")
    apply_styles()
    data = load_dashboard_data_cached()

    st.sidebar.title("AI Washing")
    mode = render_mode_selector()
    st.sidebar.caption(
        "Manifest-first dashboard. Most pages are read-only; Command Center runs approved local Make targets only."
    )
    st.sidebar.markdown("[Dashboard guide](docs/dashboard_guide.md) · [Table workbench](docs/paper_table_workbench.md)")

    pages = {
        "Start": [
            st.Page(lambda: home.render(data, mode), title=_spec("home")["title"], icon=_spec("home")["icon"], url_path="home"),
            st.Page(lambda: portfolio_demo.render(data, mode), title=_spec("portfolio_demo")["title"], icon=_spec("portfolio_demo")["icon"], url_path="portfolio-demo"),
        ],
        "Paper Review": [
            st.Page(lambda: paper_results.render(data, mode), title=_spec("paper_results")["title"], icon=_spec("paper_results")["icon"], url_path="paper-results"),
            st.Page(lambda: table_explorer.render(data, mode), title=_spec("table_explorer")["title"], icon=_spec("table_explorer")["icon"], url_path="table-explorer"),
        ],
        "Data And Constructs": [
            st.Page(lambda: data_room.render(data, mode), title=_spec("data_room")["title"], icon=_spec("data_room")["icon"], url_path="data-room"),
            st.Page(lambda: construct_audits.render(data, mode), title=_spec("construct_audits")["title"], icon=_spec("construct_audits")["icon"], url_path="construct-audits"),
        ],
        "Extensions And Reproduction": [
            st.Page(lambda: extension_lab.render(data, mode), title=_spec("extension_lab")["title"], icon=_spec("extension_lab")["icon"], url_path="extension-lab"),
            st.Page(lambda: reproduction_status.render(data, mode), title=_spec("reproduction_status")["title"], icon=_spec("reproduction_status")["icon"], url_path="reproduction-status"),
            st.Page(lambda: command_center.render(mode), title=_spec("command_center")["title"], icon=_spec("command_center")["icon"], url_path="command-center"),
            st.Page(lambda: share_export.render(mode), title=_spec("share_export")["title"], icon=_spec("share_export")["icon"], url_path="share-export"),
        ],
    }
    selected_page = st.navigation(pages, expanded=True)
    selected_page.run()


if __name__ == "__main__":
    main()
