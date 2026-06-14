from __future__ import annotations

import streamlit as st

COAUTHOR_MODE = "Coauthor Mode"
DEMO_MODE = "Demo Mode"
MODE_KEY = "dashboard_mode"


def initialize_state() -> None:
    st.session_state.setdefault(MODE_KEY, COAUTHOR_MODE)


def render_mode_selector() -> str:
    initialize_state()
    mode = st.sidebar.radio(
        "Dashboard mode",
        [COAUTHOR_MODE, DEMO_MODE],
        index=0 if st.session_state[MODE_KEY] == COAUTHOR_MODE else 1,
        key=MODE_KEY,
        help="Coauthor Mode shows repo/logical data paths. Demo Mode hides private-data-root instructions.",
    )
    return str(mode)


def is_demo_mode(mode: str) -> bool:
    return mode == DEMO_MODE
