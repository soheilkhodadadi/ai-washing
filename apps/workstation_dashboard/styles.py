from __future__ import annotations

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
          --aiw-ink: #172526;
          --aiw-teal: #0d5c63;
          --aiw-sand: #f4efe3;
          --aiw-gold: #d99a2b;
          --aiw-slate: #486367;
        }
        .block-container { padding-top: 2rem; }
        div[data-testid="stMetric"] {
          background: linear-gradient(135deg, #f7f4eb 0%, #eef7f4 100%);
          border: 1px solid #d8e3df;
          border-radius: 18px;
          padding: 1rem;
        }
        .aiw-hero {
          padding: 1.25rem 1.35rem;
          border-radius: 24px;
          background: radial-gradient(circle at top left, rgba(217,154,43,.24), transparent 28%),
                      linear-gradient(135deg, #102729 0%, #17484d 62%, #f4efe3 190%);
          color: white;
          margin-bottom: 1rem;
        }
        .aiw-hero h1 { margin-bottom: .25rem; }
        .aiw-card {
          border: 1px solid #dce6e3;
          border-radius: 18px;
          padding: 1rem;
          background: #fffdf8;
          box-shadow: 0 1px 8px rgba(17, 38, 40, .04);
          margin-bottom: .75rem;
        }
        .aiw-badge {
          display: inline-block;
          border-radius: 999px;
          padding: .16rem .55rem;
          background: #e8f2ef;
          color: #17484d;
          font-size: .78rem;
          font-weight: 650;
          margin-right: .35rem;
          margin-bottom: .25rem;
        }
        .aiw-muted { color: #5c7073; font-size: .92rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )
