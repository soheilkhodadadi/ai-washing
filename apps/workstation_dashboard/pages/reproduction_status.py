from __future__ import annotations

import streamlit as st

from components.ui import command_box, hero
from services.manifest_store import DashboardData


def render(data: DashboardData, mode: str) -> None:
    hero("Reproduction Status", "Find the validation and audit path for the frozen v4.3 empirical package.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tracked paper assets", len(data.tables))
    c2.metric("Data products", len(data.data_products))
    c3.metric("Extension lanes", len(data.extensions))

    st.subheader("Status documents")
    st.markdown(
        """
        - `docs/full_reproduction_status.md`
        - `docs/figure_reproduction_status.md`
        - `docs/referee_first_impression_report.md`
        - `docs/journal_replication_archive_policy.md`
        - `docs/known_limitations.md`
        """
    )

    st.subheader("Audit commands")
    command_box("make coauthor-preflight", mode=mode)
    command_box("make replication-audit", mode=mode)
    command_box("AIW_DATA_ROOT=/path/to/ai-washing-private-data make reproduce-all-tables", mode=mode, allow_demo=False)
