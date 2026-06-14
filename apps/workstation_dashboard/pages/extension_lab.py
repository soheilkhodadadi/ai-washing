from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from components.ui import badges, command_box, dataframe_or_info, hero
from services.extension_outputs import (
    ExtensionOutputFile,
    check_seo_schema,
    extension_csv_preview,
    extension_json_preview,
    extension_markdown_preview,
    extension_output_bundle,
    grouped_extension_files,
    safe_schema_template,
    schema_template_fields,
    status_badges,
)
from services.manifest_store import DashboardData, filter_frame
from state import DEMO_MODE

COLUMNS = [
    "extension_id",
    "title",
    "current_status",
    "maturity_status",
    "manuscript_status",
    "interpretation_limits",
]


def _safe_text(value: object, fallback: str = "Not specified") -> str:
    text = str(value or "").strip()
    return text or fallback


def _status_caption(row: pd.Series) -> str:
    maturity = _safe_text(row.get("maturity_status", ""), "extension").replace("_", " ")
    manuscript = _safe_text(row.get("manuscript_status", ""), "not manuscript ready").replace("_", " ")
    return f"{maturity} / {manuscript}"


def _render_extension_card(row: pd.Series) -> None:
    with st.container(border=True):
        st.markdown(f"### {row['title']}")
        badges(status_badges(row))
        st.caption(_status_caption(row))
        st.write(row["research_question"])
        st.caption(row["interpretation_limits"])


def _download_file_button(file: ExtensionOutputFile, *, key: str) -> None:
    if not file.safe_downloadable:
        st.caption("Download hidden if the file contains local/private paths or is too large.")
        return
    mime = {
        ".csv": "text/csv",
        ".md": "text/markdown",
        ".json": "application/json",
    }.get(file.suffix, "application/octet-stream")
    st.download_button(
        "Download",
        data=file.path.read_bytes(),
        file_name=file.path.name,
        mime=mime,
        key=key,
    )


def _render_overview(row: pd.Series) -> None:
    st.subheader("Purpose and status")
    badges(status_badges(row))
    if str(row.get("manuscript_status", "")) == "not_manuscript_ready":
        st.warning(
            "This extension is not manuscript-ready evidence. Treat it as exploratory or future-work material until it is reviewed and explicitly promoted."
        )
    st.markdown("**Research question**")
    st.write(row["research_question"])
    st.markdown("**Current status**")
    st.write(row["current_status"])
    st.markdown("**Interpretation limits**")
    st.write(row["interpretation_limits"])
    st.markdown("**Documentation**")
    st.code(row["docs"], language="text")


def _render_inputs(row: pd.Series) -> None:
    st.subheader("Inputs and implementation surface")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Primary data product**")
        st.write(row["primary_data_product"])
        st.markdown("**Reference table IDs**")
        st.write(_safe_text(row.get("reference_table_ids", "")))
    with c2:
        st.markdown("**Source scripts or templates**")
        st.write(row["source_scripts"])
        st.markdown("**Strong-version data need**")
        st.write(row["strong_version_data_needed"])
    schema = safe_schema_template(row)
    if schema is not None:
        st.markdown("**Future data template**")
        st.code(str(schema.relative_to(Path(__file__).resolve().parents[3])), language="text")


def _render_json(file: ExtensionOutputFile) -> None:
    payload = extension_json_preview(file)
    if not payload:
        st.caption("No JSON preview available.")
        return
    st.json(payload, expanded=False)


def _render_markdown(file: ExtensionOutputFile) -> None:
    text = extension_markdown_preview(file)
    if text:
        st.markdown(text)
    else:
        st.caption("No Markdown preview available.")


def _render_csv(file: ExtensionOutputFile) -> None:
    preview = extension_csv_preview(file)
    if preview.empty:
        st.caption("No CSV preview available.")
        return
    st.caption(f"Previewing first {len(preview)} rows from `{file.rel_path}`. Extension outputs are aggregate artifacts, not private row-level source data.")
    st.dataframe(preview, width="stretch", hide_index=True)


def _render_output_file(file: ExtensionOutputFile, *, index: int) -> None:
    with st.container(border=True):
        top = st.columns([1.6, 0.4])
        with top[0]:
            st.markdown(f"**{file.label}**")
            st.caption(f"`{file.rel_path}` · {file.size_bytes:,} bytes")
        with top[1]:
            _download_file_button(file, key=f"extension_file_{index}_{file.rel_path}")
        if file.previewable_json:
            _render_json(file)
        elif file.previewable_markdown:
            _render_markdown(file)
        elif file.previewable_csv:
            _render_csv(file)


def _render_outputs(row: pd.Series) -> None:
    st.subheader("Generated result viewer")
    bundle = extension_output_bundle(row)
    if not bundle.exists:
        st.info(bundle.note or "No generated extension outputs are present yet.")
        command_box(
            row["make_command"],
            mode=st.session_state.get("dashboard_mode", "Coauthor Mode"),
            allow_demo=False,
            label="Generate or validate this lane",
            tags=["copy-ready", "manual terminal command"],
        )
        return
    st.success(f"Output folder found: `{bundle.rel_output_dir}`")
    if not bundle.files:
        st.info("The output folder exists but contains no supported dashboard-preview files.")
        return
    for category, files in grouped_extension_files(bundle.files).items():
        with st.expander(category, expanded=category in {"Summary JSON", "Narrative notes"}):
            for index, file in enumerate(files):
                _render_output_file(file, index=index)


def _render_commands(row: pd.Series, mode: str) -> None:
    st.subheader("Copy-ready commands")
    command_box(
        row["make_command"],
        mode=mode,
        allow_demo=False if str(row.get("maturity_status", "")) != "future_data_required" else True,
        label="Primary command",
        tags=["manual", "writes ignored outputs" if "extension-" in str(row["make_command"]) else "metadata check"],
        note="The dashboard displays commands only. It does not execute empirical scripts from the browser.",
    )
    command_box(
        f"make extension-info EXTENSION={row['extension_id']}",
        mode=mode,
        label="Inspect registry entry in terminal",
        tags=["read-only"],
    )


def _render_schema_checker(row: pd.Series) -> None:
    schema = safe_schema_template(row)
    if schema is None:
        st.info("No future-data schema is registered for this extension lane.")
        return
    st.subheader("Future SEO/offering-terms schema checker")
    st.caption(
        "This checker validates column coverage and row count only. It does not show uploaded row values and does not save the uploaded file."
    )
    fields = schema_template_fields(schema)
    st.dataframe(fields[["field_name", "required", "preferred_type", "description"]], width="stretch", hide_index=True)
    uploaded = st.file_uploader(
        "Upload a candidate SEO/offering-terms CSV for a schema-only check",
        type=["csv"],
        key=f"seo_schema_upload_{row['extension_id']}",
    )
    if uploaded is None:
        command_box(
            "make check-seo-schema SEO_FILE=/path/to/seo_offering_terms.csv",
            mode=st.session_state.get("dashboard_mode", "Coauthor Mode"),
            label="Terminal schema check",
            tags=["metadata only", "no row values printed"],
        )
        return
    result = check_seo_schema(uploaded.getvalue(), template_path=schema)
    if result.is_valid:
        st.success("Schema check passed for required columns and identifier coverage.")
    else:
        st.warning("Schema check needs attention before this data can support a strong washing-pays extension.")
    st.dataframe(result.summary_rows(), width="stretch", hide_index=True)
    st.caption("Detected columns are shown as schema metadata only; uploaded row values are intentionally not displayed.")


def render(data: DashboardData, mode: str) -> None:
    hero(
        "Extension Lab",
        "Inspect follow-on tests, generated exploratory outputs, and future-data requirements without mixing them into frozen v4.3 evidence.",
    )
    if mode == DEMO_MODE:
        st.info("Demo Mode keeps the extension narrative visible but hides private-data commands and generated-data details where needed.")

    query = st.text_input("Search extension lanes", key="extension_query")
    filtered = filter_frame(data.extensions, query)
    dataframe_or_info(filtered, COLUMNS, empty_message="No matching extension lanes.")
    if filtered.empty:
        return

    st.subheader("Extension lanes")
    columns = st.columns(2)
    for idx, (_, row) in enumerate(filtered.iterrows()):
        with columns[idx % 2]:
            _render_extension_card(row)

    options = filtered["extension_id"].tolist()
    selected = st.selectbox(
        "Open extension",
        options,
        key="selected_extension",
        format_func=lambda extension_id: str(filtered.loc[filtered["extension_id"] == extension_id, "title"].iloc[0]),
    )
    row = filtered.loc[filtered["extension_id"] == selected].iloc[0]
    st.markdown(f"## {row['title']}")

    overview, inputs, outputs, commands, schema = st.tabs(
        ["Overview", "Inputs", "Generated Outputs", "Commands", "Future Data Schema"]
    )
    with overview:
        _render_overview(row)
    with inputs:
        _render_inputs(row)
    with outputs:
        _render_outputs(row)
    with commands:
        _render_commands(row, mode)
    with schema:
        _render_schema_checker(row)
