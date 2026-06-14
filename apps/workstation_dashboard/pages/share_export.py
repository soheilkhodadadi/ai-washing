from __future__ import annotations

import streamlit as st

from components.ui import command_box, hero


def render(mode: str) -> None:
    hero("Share / Export Center", "Copy the commands used to export bundles, regenerate dashboards, and prepare a coauthor handoff.")

    st.subheader("Table and extension bundles")
    command_box("make workbench-index", mode=mode)
    command_box("make export-table-workbench TABLE_ID=T30", mode=mode)
    command_box("AIW_DATA_ROOT=/path/to/ai-washing-private-data make extension-builder-hides", mode=mode, allow_demo=False)

    st.subheader("Dashboard paths")
    command_box("make dashboard", mode=mode)
    command_box("make dashboard-check", mode=mode)
    command_box("make dashboard-app", mode=mode)
    command_box("make docker-dashboard-app", mode=mode)

    st.subheader("Share readiness")
    command_box("make share-readiness", mode=mode)
    command_box("make package-surface-audit", mode=mode)
    command_box("git status --short", mode=mode)
