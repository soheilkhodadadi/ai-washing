from __future__ import annotations

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
          --aiw-ink: #102729;
          --aiw-deep: #173b3f;
          --aiw-teal: #0d5c63;
          --aiw-mint: #dcece6;
          --aiw-sand: #fbf7ee;
          --aiw-paper: #fffdf8;
          --aiw-gold: #d99a2b;
          --aiw-clay: #9b6542;
          --aiw-slate: #486367;
          --aiw-faint: #edf3ef;
          --aiw-border: #d7e2dd;
          --aiw-shadow: 0 20px 46px rgba(16, 39, 41, .10);
          --aiw-font: Avenir Next, Gill Sans, Segoe UI, Verdana, sans-serif;
        }
        html, body, [class*="css"] {
          font-family: var(--aiw-font);
          color: var(--aiw-ink);
        }
        .stApp {
          background:
            radial-gradient(circle at 9% 4%, rgba(217, 154, 43, .16), transparent 28rem),
            radial-gradient(circle at 94% 0%, rgba(13, 92, 99, .15), transparent 32rem),
            linear-gradient(180deg, #fbf7ee 0%, #f7f4ec 52%, #ffffff 100%);
        }
        .block-container {
          max-width: 1240px;
          padding-top: 1.6rem;
          padding-bottom: 3rem;
        }
        section[data-testid="stSidebar"] {
          background: linear-gradient(180deg, #102729 0%, #153b3f 68%, #204c4f 100%);
          border-right: 1px solid rgba(255, 255, 255, .08);
        }
        section[data-testid="stSidebar"] * {
          color: #f9f2e5;
        }
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] a {
          color: #f3c568;
          text-decoration: none;
        }
        .aiw-sidebar-brand {
          padding: .6rem .15rem 1rem .15rem;
        }
        .aiw-sidebar-brand svg {
          width: 100%;
          height: auto;
          display: block;
        }
        .aiw-hero {
          position: relative;
          overflow: hidden;
          padding: 1.55rem 1.7rem;
          border-radius: 30px;
          background:
            radial-gradient(circle at top left, rgba(243, 197, 104, .34), transparent 17rem),
            radial-gradient(circle at 88% 12%, rgba(255, 253, 248, .19), transparent 12rem),
            linear-gradient(135deg, #102729 0%, #17484d 60%, #255d5e 100%);
          color: white;
          margin-bottom: 1.15rem;
          box-shadow: var(--aiw-shadow);
          border: 1px solid rgba(255, 255, 255, .12);
        }
        .aiw-hero:after {
          content: "";
          position: absolute;
          right: -60px;
          bottom: -88px;
          width: 260px;
          height: 260px;
          border-radius: 50%;
          border: 42px solid rgba(255, 255, 255, .08);
        }
        .aiw-hero h1 {
          margin: 0 0 .35rem 0;
          color: #fffdf8;
          letter-spacing: -.035em;
          font-weight: 820;
        }
        .aiw-hero p {
          margin: 0;
          max-width: 820px;
          color: rgba(255, 253, 248, .88);
          font-size: 1.03rem;
          line-height: 1.55;
        }
        .aiw-card {
          border: 1px solid var(--aiw-border);
          border-radius: 22px;
          padding: 1rem 1.05rem;
          background:
            linear-gradient(180deg, rgba(255, 253, 248, .96), rgba(255, 253, 248, .9)),
            radial-gradient(circle at top right, rgba(217, 154, 43, .08), transparent 15rem);
          box-shadow: 0 10px 28px rgba(17, 38, 40, .06);
          margin-bottom: .85rem;
        }
        .aiw-card h3 {
          margin-top: 0;
          margin-bottom: .35rem;
          letter-spacing: -.02em;
        }
        .aiw-badge {
          display: inline-block;
          border-radius: 999px;
          padding: .18rem .62rem;
          background: #e8f2ef;
          color: #17484d;
          border: 1px solid rgba(13, 92, 99, .12);
          font-size: .76rem;
          font-weight: 760;
          margin-right: .35rem;
          margin-bottom: .28rem;
          letter-spacing: .01em;
        }
        .aiw-muted {
          color: #5c7073;
          font-size: .92rem;
        }
        .aiw-section-kicker {
          display: inline-flex;
          align-items: center;
          gap: .35rem;
          text-transform: uppercase;
          letter-spacing: .14em;
          font-size: .72rem;
          font-weight: 820;
          color: var(--aiw-clay);
          margin-bottom: .35rem;
        }
        .aiw-mode-ribbon {
          border-radius: 18px;
          border: 1px solid var(--aiw-border);
          background: linear-gradient(135deg, #fffdf8, #eef7f4);
          padding: .8rem 1rem;
          margin: .75rem 0 1rem 0;
          box-shadow: 0 8px 24px rgba(16, 39, 41, .06);
        }
        .aiw-mode-ribbon strong {
          color: var(--aiw-teal);
        }
        .aiw-timeline {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
          gap: .75rem;
          margin: .5rem 0 1rem 0;
        }
        .aiw-step {
          background: rgba(255, 253, 248, .92);
          border: 1px solid var(--aiw-border);
          border-radius: 20px;
          padding: .9rem;
          min-height: 138px;
          box-shadow: 0 10px 26px rgba(16, 39, 41, .055);
        }
        .aiw-step-number {
          width: 2rem;
          height: 2rem;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          border-radius: 999px;
          background: #173b3f;
          color: #fffdf8;
          font-weight: 820;
          margin-bottom: .65rem;
        }
        .aiw-step h4 {
          margin: 0 0 .25rem 0;
          font-size: 1rem;
        }
        .aiw-step p {
          margin: 0;
          color: #52696c;
          font-size: .9rem;
          line-height: 1.45;
        }
        div[data-testid="stMetric"] {
          background: linear-gradient(135deg, #fffdf8 0%, #eef7f4 100%);
          border: 1px solid var(--aiw-border);
          border-radius: 20px;
          padding: 1rem;
          box-shadow: 0 9px 24px rgba(17, 38, 40, .05);
        }
        div[data-testid="stDataFrame"] {
          border: 1px solid var(--aiw-border);
          border-radius: 18px;
          overflow: hidden;
          box-shadow: 0 10px 30px rgba(16, 39, 41, .045);
        }
        div[data-testid="stCodeBlock"] {
          border-radius: 16px;
          border: 1px solid rgba(13, 92, 99, .14);
        }
        button[kind="primary"], div.stButton > button {
          border-radius: 999px;
          border: 1px solid rgba(13, 92, 99, .2);
          font-weight: 750;
        }
        hr {
          border: none;
          height: 1px;
          background: linear-gradient(90deg, transparent, rgba(13, 92, 99, .32), transparent);
          margin: 1.25rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
