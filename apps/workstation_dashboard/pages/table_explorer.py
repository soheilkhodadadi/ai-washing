from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from components.ui import badges, command_box, dataframe_or_info, hero
from services.manifest_store import DashboardData, filter_frame
from services.paths import OUTPUTS_DIR
from services.table_artifacts import (
    TableArtifact,
    build_review_packet,
    csv_preview,
    grouped_artifacts,
    preferred_review_artifact,
    table_artifacts,
    table_display_label,
)

DETAIL_COLUMNS = [
    "paper_label",
    "asset_id",
    "asset_type",
    "paper_section",
    "caption",
    "empirical_question",
    "primary_data_product",
    "main_constructs",
]


def _query_asset() -> str:
    value = st.query_params.get("asset", "")
    if isinstance(value, list):
        return str(value[0]) if value else ""
    return str(value or "")


def _asset_options(df: pd.DataFrame) -> list[str]:
    return [str(value) for value in df["asset_id"].tolist()]


def _label_lookup(df: pd.DataFrame) -> dict[str, str]:
    return {str(row["asset_id"]): table_display_label(row) for _, row in df.iterrows()}


def _default_asset(options: list[str]) -> str:
    requested = _query_asset()
    if requested in options:
        return requested
    if "T30" in options:
        return "T30"
    return options[0]


def _mime_type(path: Path) -> str:
    suffix = path.suffix.lower()
    return {
        ".csv": "text/csv",
        ".tex": "text/plain",
        ".md": "text/markdown",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".pdf": "application/pdf",
        ".png": "image/png",
        ".json": "application/json",
        ".zip": "application/zip",
    }.get(suffix, "application/octet-stream")


def _status_label(status: str) -> str:
    return status.replace("_", " ")


def _download_button(artifact: TableArtifact, *, key_prefix: str) -> None:
    if not artifact.downloadable:
        st.caption("Not downloadable from the dashboard")
        return
    st.download_button(
        "Download",
        data=artifact.path.read_bytes(),
        file_name=artifact.path.name,
        mime=_mime_type(artifact.path),
        key=f"{key_prefix}_{artifact.status}_{artifact.rel_path}",
    )


def _render_open_first(row: pd.Series, artifacts: list[TableArtifact]) -> None:
    preferred = preferred_review_artifact(artifacts)
    bundle_path = OUTPUTS_DIR / "workbench" / str(row["asset_id"])
    with st.container(border=True):
        st.markdown("### Open First")
        left, right = st.columns([1.35, 1])
        with left:
            st.markdown("**What this table asks**")
            st.write(row["empirical_question"])
            st.markdown("**Why it matters**")
            st.write(row["coauthor_use"] or row["extension_relevance"])
            st.markdown("**Canonical status**")
            st.write(
                "Frozen v4.3 reference files are the baseline. Generated and workbench files are convenience copies for review."
            )
            if preferred:
                st.markdown("**Best first file**")
                st.write(f"{preferred.label}: `{preferred.rel_path}`")
            if bundle_path.exists():
                st.success(f"Workbench bundle available: `outputs/workbench/{row['asset_id']}/OPEN_FIRST.md`")
            else:
                st.info("Workbench bundle not found yet. Use the export command below to create it.")
        with right:
            if preferred and preferred.suffix == ".png":
                st.image(str(preferred.path), caption=preferred.label, width="stretch")
            else:
                st.markdown("**Suggested review order**")
                st.markdown(
                    """
                    1. DOCX, PNG, or PDF for visual review.
                    2. CSV for numeric audit.
                    3. TeX for manuscript integration.
                    4. Writer packet or result notes for interpretation.
                    """
                )


def _render_csv_preview(artifacts: list[TableArtifact]) -> None:
    csv_artifacts = [artifact for artifact in artifacts if artifact.previewable_csv]
    if not csv_artifacts:
        st.info("No safe repo-contained CSV preview is available for this table.")
        return
    labels = {artifact.rel_path: artifact for artifact in csv_artifacts}
    selected = st.selectbox("CSV preview", list(labels), format_func=lambda rel: labels[rel].label)
    artifact = labels[selected]
    preview = csv_preview(artifact)
    st.caption(f"Previewing first {len(preview)} rows from `{artifact.rel_path}`.")
    st.dataframe(preview, width="stretch", hide_index=True)


def _render_artifact_group(category: str, artifacts: list[TableArtifact], *, expanded: bool) -> None:
    with st.expander(category, expanded=expanded):
        for index, artifact in enumerate(artifacts):
            cols = st.columns([1.4, 0.8, 0.45])
            with cols[0]:
                st.markdown(f"**{artifact.label}**")
                st.caption(f"`{artifact.rel_path}`")
            with cols[1]:
                badges([_status_label(artifact.status), artifact.suffix.upper() or "FILE"])
                if artifact.exists:
                    st.caption(f"{artifact.size_bytes:,} bytes")
                else:
                    st.caption("Missing")
            with cols[2]:
                _download_button(artifact, key_prefix=f"{category}_{index}")
            if artifact.suffix == ".png" and artifact.exists:
                st.image(str(artifact.path), caption=artifact.label, width="stretch")


def _render_artifacts(row: pd.Series, artifacts: list[TableArtifact]) -> None:
    st.markdown("### Available review artifacts")
    if not artifacts:
        st.info("No safe repo-contained artifacts were resolved for this table.")
        return
    packet = build_review_packet(row, artifacts)
    st.download_button(
        "Download table review packet (.zip)",
        data=packet,
        file_name=f"{row['asset_id']}_table_review_packet.zip",
        mime="application/zip",
        key=f"{row['asset_id']}_review_packet",
    )
    for category, items in grouped_artifacts(artifacts).items():
        _render_artifact_group(category, items, expanded=category in {"Review first", "Numeric audit"})


def render(data: DashboardData, mode: str) -> None:
    hero("Table Explorer", "Review manuscript tables by paper label, with readable outputs first and technical details second.")
    if st.button("Review Main Table 7", help="Open the capital-raising timing table used as the supervisor review example."):
        st.query_params["asset"] = "T30"
        st.rerun()

    query = st.text_input("Search tables and figures", key="table_explorer_query")
    filtered = filter_frame(data.tables, query)
    dataframe_or_info(filtered, DETAIL_COLUMNS, empty_message="No matching paper assets.")
    if filtered.empty:
        return

    options = _asset_options(filtered)
    labels = _label_lookup(filtered)
    default_asset = _default_asset(options)
    selected = st.selectbox(
        "Choose a paper table or figure",
        options,
        index=options.index(default_asset),
        format_func=lambda asset_id: labels.get(asset_id, asset_id),
        key="selected_table_asset",
    )
    row = data.tables.loc[data.tables["asset_id"] == selected].iloc[0]
    artifacts = table_artifacts(row)

    st.markdown(f"## {row['paper_label']}: {row['caption']}")
    badges([row["asset_type"], row["paper_section"], f"Asset {row['asset_id']}"])
    _render_open_first(row, artifacts)

    st.markdown("### Safe CSV preview")
    _render_csv_preview(artifacts)

    _render_artifacts(row, artifacts)

    st.markdown("### Empirical and technical details")
    left, right = st.columns([1.1, 1])
    with left:
        st.markdown("### What this result answers")
        st.write(row["empirical_question"])
        st.markdown(f"**Caption:** {row['caption']}")
        st.markdown(f"**Main constructs:** {row['main_constructs']}")
        st.markdown(f"**Extension relevance:** {row['extension_relevance']}")
    with right:
        st.markdown("### Implementation details")
        st.markdown(f"**Primary data product:** {row['primary_data_product']}")
        st.markdown(f"**Owning script:** `{row['script_module']}`")
        st.markdown(f"**Reference outputs:** `{row['reference_outputs']}`")
        st.markdown(f"**Safe modifications:** {row['safe_modifications']}")

    st.markdown("### Copy-ready commands")
    st.caption("The browser does not run these commands. They are provided for copying into a terminal.")
    command_box(f"make export-table-workbench TABLE_ID={row['asset_id']}", mode=mode)
    command_box(row["make_command"], mode=mode, allow_demo=False)
