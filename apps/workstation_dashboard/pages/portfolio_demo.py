from __future__ import annotations

import streamlit as st

from components.ui import badges, hero, safety_banner
from services.manifest_store import DashboardData
from services.portfolio_content import (
    CASE_STUDY_SECTIONS,
    DEMO_SAFETY_POINTS,
    WORKFLOW_STEPS,
    portfolio_summary_metrics,
)


def _section_card(title: str, body: str, bullets: tuple[str, ...]) -> None:
    with st.container(border=True):
        st.markdown(f"#### {title}")
        st.write(body)
        for bullet in bullets:
            st.markdown(f"- {bullet}")


def _workflow_timeline() -> None:
    html = ['<div class="aiw-timeline">']
    for index, (label, description) in enumerate(WORKFLOW_STEPS, start=1):
        html.append(
            f"""
            <div class="aiw-step">
              <div class="aiw-step-number">{index}</div>
              <h4>{label}</h4>
              <p>{description}</p>
            </div>
            """
        )
    html.append("</div>")
    st.markdown("\n".join(html), unsafe_allow_html=True)


def render(data: DashboardData, mode: str) -> None:
    hero(
        "Portfolio Demo Mode",
        "A nonprivate case-study view of the AI Washing workstation as a reproducible finance, NLP, "
        "and analytics product.",
    )
    safety_banner(mode)
    badges(["portfolio-safe", "manifest metadata", "no private row values", "command execution disabled in Demo Mode"])

    metrics = portfolio_summary_metrics(data)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Assets", metrics["manuscript_assets"])
    c2.metric("Tables", metrics["paper_tables"])
    c3.metric("Figures", metrics["figures"])
    c4.metric("Data products", metrics["data_products"])
    c5.metric("Extensions", metrics["extension_lanes"])

    overview, workflow, evidence, reusable, hidden = st.tabs(
        ["Case Study", "Workflow", "Evidence", "Reusable Method", "Demo Safety"]
    )

    with overview:
        st.markdown('<div class="aiw-section-kicker">Client-facing research software</div>', unsafe_allow_html=True)
        _section_card(CASE_STUDY_SECTIONS[0].title, CASE_STUDY_SECTIONS[0].body, CASE_STUDY_SECTIONS[0].bullets)
        st.markdown(
            """
            This dashboard is designed to make a complex empirical project legible to three audiences at once:
            a technical coauthor who wants scripts and data lineage, a supervisor who wants readable tables,
            and a portfolio reviewer who wants to see the system design without private research data.
            """
        )

    with workflow:
        st.markdown(
            '<div class="aiw-section-kicker">From research question to controlled execution</div>',
            unsafe_allow_html=True,
        )
        st.write(CASE_STUDY_SECTIONS[1].body)
        _workflow_timeline()

    with evidence:
        st.markdown('<div class="aiw-section-kicker">What the demo can show safely</div>', unsafe_allow_html=True)
        _section_card(CASE_STUDY_SECTIONS[2].title, CASE_STUDY_SECTIONS[2].body, CASE_STUDY_SECTIONS[2].bullets)
        left, right = st.columns(2)
        with left:
            st.markdown("**Nonprivate evidence surfaces**")
            st.markdown(
                """
                - Paper-order table and figure workbench.
                - Data product catalog with coverage lanes and keys.
                - Construct audit summaries for classifier, patent, and WRDS lanes.
                - Extension registry with maturity and manuscript-readiness status.
                """
            )
        with right:
            st.markdown("**What remains protected**")
            st.markdown(
                """
                - Private data roots and local machine paths.
                - Row-level sentences, patent abstracts, and licensed data values.
                - Access details and untracked coauthor outputs.
                - Command logs outside explicit local Command Center runs.
                """
            )

    with reusable:
        st.markdown('<div class="aiw-section-kicker">Reusable methodology</div>', unsafe_allow_html=True)
        _section_card(CASE_STUDY_SECTIONS[3].title, CASE_STUDY_SECTIONS[3].body, CASE_STUDY_SECTIONS[3].bullets)
        st.info(
            "The reusable pattern is manifest-first: define the public contract, keep private data external, "
            "map every result to code and evidence, then add a client-facing review layer on top."
        )

    with hidden:
        st.markdown('<div class="aiw-section-kicker">Portfolio-safe boundary</div>', unsafe_allow_html=True)
        for point in DEMO_SAFETY_POINTS:
            st.markdown(f"- {point}")
        st.warning(
            "External screenshots should be captured in Demo Mode. Coauthor Mode is for trusted local review only."
        )
