from __future__ import annotations

import pandas as pd
import streamlit as st

from components.ui import badges, hero
from services.command_runner import (
    CommandRunResult,
    DashboardCommand,
    command_is_enabled,
    environment_summary,
    load_command_registry,
    run_dashboard_command,
)
from state import DEMO_MODE


def _category_options(commands: tuple[DashboardCommand, ...]) -> list[str]:
    return ["All", *sorted({command.category for command in commands})]


def _registry_frame(commands: tuple[DashboardCommand, ...]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "command_id": command.command_id,
                "title": command.title,
                "category": command.category,
                "command": command.display_command,
                "requires_private_data": command.requires_private_data,
                "writes_ignored_outputs": command.writes_ignored_outputs,
                "timeout_seconds": command.timeout_seconds,
            }
            for command in commands
        ]
    )


def _result_badge(result: CommandRunResult) -> None:
    if result.status == "passed":
        st.success(f"Passed in {result.duration_seconds:.1f}s · exit code 0")
    elif result.status == "blocked":
        st.warning(result.error_message)
    elif result.status == "timeout":
        st.error(result.error_message)
    else:
        st.error(f"Failed in {result.duration_seconds:.1f}s · exit code {result.exit_code}")
        if result.error_message:
            st.caption(result.error_message)


def _render_result(result: CommandRunResult) -> None:
    _result_badge(result)
    if result.rel_log_path:
        st.caption(f"Ignored log: `{result.rel_log_path}`")
    if result.log_tail:
        st.markdown("**Log tail**")
        st.code(result.log_tail, language="text")


def _render_command(command: DashboardCommand, mode: str) -> None:
    with st.container(border=True):
        top = st.columns([1.5, 0.8])
        with top[0]:
            st.markdown(f"### {command.title}")
            st.write(command.description)
            badges(command.tags)
        with top[1]:
            st.markdown("**Environment**")
            for key, value in environment_summary(command).items():
                st.caption(f"{key}: `{value}`")

        st.markdown("**Approved command**")
        st.code(command.display_command, language="bash")
        if command.expected_outputs:
            st.caption(f"Expected output: `{command.expected_outputs}`")
        if command.docs:
            st.caption(f"Documentation: `{command.docs}`")

        enabled, reason = command_is_enabled(command, mode=mode)
        confirmation = True
        if command.requires_confirmation:
            confirmation = st.checkbox(
                "I understand this command may read private data and/or write ignored outputs.",
                key=f"confirm_{command.command_id}",
                disabled=not enabled,
            )
        disabled = not enabled or (command.requires_confirmation and not confirmation)
        if mode == DEMO_MODE:
            st.info("Execution is disabled in Demo Mode. The command is shown for orientation only.")
        elif not enabled:
            st.warning(reason)

        if st.button("Run approved command", key=f"run_{command.command_id}", disabled=disabled):
            with st.spinner(f"Running {command.title}..."):
                result = run_dashboard_command(command.command_id, mode=mode, confirmed=confirmation)
            st.session_state[f"last_result_{command.command_id}"] = result

        result = st.session_state.get(f"last_result_{command.command_id}")
        if isinstance(result, CommandRunResult):
            _render_result(result)


def render(mode: str) -> None:
    hero(
        "Command Center",
        "Run approved workstation commands from the dashboard with fixed Make targets, confirmation gates, and ignored logs.",
    )
    st.caption(
        "This page is intentionally narrow: no arbitrary shell, no user-entered targets, no full reproduction or replication audit execution in v1."
    )
    commands = load_command_registry()

    filters = st.columns([0.6, 1.2])
    with filters[0]:
        category = st.selectbox("Command group", _category_options(commands), key="command_center_category")
    with filters[1]:
        query = st.text_input("Search approved commands", key="command_center_query")

    frame = _registry_frame(commands)
    filtered = commands
    if category != "All":
        filtered = tuple(command for command in filtered if command.category == category)
    if query:
        needle = query.lower()
        filtered = tuple(
            command
            for command in filtered
            if needle in " ".join([command.command_id, command.title, command.category, command.description]).lower()
        )

    st.dataframe(frame, width="stretch", hide_index=True)
    if mode == DEMO_MODE:
        st.warning("Demo Mode disables execution. Switch to Coauthor Mode on a trusted local workstation to run commands.")

    if not filtered:
        st.info("No approved commands match the current filters.")
        return
    for command in filtered:
        _render_command(command, mode)
