from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import pandas as pd
import streamlit as st

from state import DEMO_MODE

ASSET_DIR = Path(__file__).resolve().parents[1] / "assets"


def hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <section class="aiw-hero">
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def brand_header() -> None:
    logo = ASSET_DIR / "aiw_mark.svg"
    if logo.is_file():
        st.sidebar.markdown(
            f'<div class="aiw-sidebar-brand">{logo.read_text(encoding="utf-8")}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.title("AI Washing")


def badges(items: Iterable[object]) -> None:
    html = "".join(f'<span class="aiw-badge">{item}</span>' for item in items if str(item or "").strip())
    if html:
        st.markdown(html, unsafe_allow_html=True)


def card(title: str, body: str, *, meta: Iterable[object] = ()) -> None:
    meta_html = "".join(f'<span class="aiw-badge">{item}</span>' for item in meta if str(item or "").strip())
    st.markdown(
        f"""
        <div class="aiw-card">
          <h3>{title}</h3>
          <p>{body}</p>
          <div>{meta_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def command_box(
    command: str,
    *,
    mode: str,
    allow_demo: bool = True,
    note: str = "",
    label: str = "",
    tags: Iterable[object] = (),
) -> None:
    if not command:
        return
    if mode == DEMO_MODE and not allow_demo:
        st.info("Private-data command hidden in Demo Mode. Switch to Coauthor Mode when using the private data room.")
        return
    if label:
        st.markdown(f"**{label}**")
    badges(tags)
    if note:
        st.caption(note)
    st.code(command, language="bash")


def dataframe_or_info(df: pd.DataFrame, columns: list[str], *, empty_message: str) -> None:
    if df.empty:
        st.info(empty_message)
        return
    visible = [column for column in columns if column in df.columns]
    st.dataframe(df[visible], width="stretch", hide_index=True)


def safety_banner(mode: str) -> None:
    if mode == DEMO_MODE:
        st.info("Demo Mode is public-review safe: private-data instructions are hidden and command execution is disabled.")
    else:
        st.success(
            "Coauthor Mode: most pages are read-only; Command Center can run approved local Make targets with confirmation and logs."
        )
