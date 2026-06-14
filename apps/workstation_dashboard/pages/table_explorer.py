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
from services.technical_drilldown import (
    command_set,
    crosswalk_for_asset,
    data_product_path_statuses,
    linked_constructs,
    linked_data_products,
    linked_extensions,
    source_script_for_module,
)
from state import DEMO_MODE

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


def _render_status_value(label: str, value: object) -> None:
    text = str(value or "").strip()
    if text:
        st.markdown(f"**{label}:** {text}")


def _render_data_product_status(product: pd.Series, mode: str) -> None:
    if mode == DEMO_MODE:
        st.info("Private-data path and schema checks are hidden in Demo Mode.")
        return
    statuses = data_product_path_statuses(product)
    if not statuses:
        st.caption("No logical private path is listed for this product.")
        return
    for status in statuses:
        with st.container(border=True):
            badges([status.status, status.kind, status.suffix])
            st.caption(f"Logical path: `{status.logical_path}`")
            st.caption(f"Mounted path: `{status.display_path}`")
            if status.size_bytes is not None:
                st.caption(f"Size: {status.size_bytes:,} bytes")
            if status.file_count:
                st.caption(f"File count: {status.file_count}")
            if status.row_count is not None:
                st.caption(f"Rows: {status.row_count:,}")
            if status.schema_source:
                st.caption(f"Schema source: `{status.schema_source}`")
            if status.columns:
                st.markdown("**Columns**")
                st.code(", ".join(status.columns), language="text")
            if status.note:
                st.caption(status.note)


def _render_technical_drilldown(row: pd.Series, data: DashboardData, mode: str) -> None:
    asset_id = str(row["asset_id"])
    crosswalk = crosswalk_for_asset(asset_id)
    script = source_script_for_module(row["script_module"])
    products = linked_data_products(row, data.data_products)
    constructs = linked_constructs(row)
    extensions = linked_extensions(row, data.extensions)

    st.markdown("### Technical Drill-Down")
    st.caption(
        "Read-only continuation map for coauthors. Approved in-app execution is limited to Command Center."
    )

    summary_left, summary_right = st.columns([1, 1])
    with summary_left:
        st.markdown("#### Table identity")
        _render_status_value("Paper label", row["paper_label"])
        _render_status_value("Asset ID", asset_id)
        _render_status_value("Paper section", row["paper_section"])
        _render_status_value("Paper source", row["paper_tex_file"])
    with summary_right:
        st.markdown("#### Reproduction status")
        if crosswalk is not None:
            badges([crosswalk.get("match_status", ""), crosswalk.get("priority", ""), crosswalk.get("test_id", "")])
            _render_status_value("Run ID", crosswalk.get("run_id", ""))
            _render_status_value("Match notes", crosswalk.get("match_notes", ""))
        else:
            st.warning("No table-to-script crosswalk row was found for this asset.")

    st.markdown("#### Owning script")
    script_cols = st.columns([1.2, 0.8])
    with script_cols[0]:
        _render_status_value("Module", script.module)
        _render_status_value("Repo source path", script.rel_path)
    with script_cols[1]:
        badges([script.status])
        if not script.exists:
            st.warning("The source path could not be resolved inside the canonical repo.")

    st.markdown("#### Data dependencies")
    if products.empty:
        st.info("No catalog data product is linked to this asset yet.")
    for _, product in products.iterrows():
        title = f"{product['product_id']} - {product['purpose']}"
        with st.expander(title, expanded=len(products) == 1):
            _render_status_value("Coverage", product["coverage"])
            _render_status_value("Keys", product["keys"])
            _render_status_value("Source lineage", product["source_lineage"])
            _render_status_value("Validation scripts", product["producing_or_validation_scripts"])
            _render_status_value("Overwrite rule", product["overwrite_rule"])
            _render_status_value("Extension relevance", product["extension_relevance"])
            if mode != DEMO_MODE:
                _render_status_value("Logical private path", f"`{product['logical_private_path']}`")
            _render_data_product_status(product, mode)

    st.markdown("#### Construct playbooks")
    if not constructs:
        st.info("No construct playbook was matched from the table constructs.")
    for construct in constructs:
        with st.container(border=True):
            st.markdown(f"**{construct['title']}**")
            st.write(construct["summary"])
            st.caption(f"Playbook: `{construct['doc']}`")
            command_box(
                construct["command"],
                mode=mode,
                label="Construct command",
                tags=["read-only"],
            )

    st.markdown("#### Extension relevance")
    if extensions.empty:
        st.info("No registered extension lane directly references this asset.")
    for _, extension in extensions.iterrows():
        with st.container(border=True):
            st.markdown(f"**{extension['title']}**")
            st.write(extension["research_question"])
            _render_status_value("Status", extension["current_status"])
            _render_status_value("Interpretation limits", extension["interpretation_limits"])
            _render_status_value("Documentation", f"`{extension['docs']}`")
            command_box(
                extension["make_command"],
                mode=mode,
                allow_demo=False,
                label="Extension command",
                tags=["extension", "writes ignored outputs"],
            )

    st.markdown("#### Controlled command clipboard")
    for item in command_set(row, products, extensions):
        tags = [part.strip() for part in item["tags"].split(";") if part.strip()]
        allow_demo = "requires private data" not in item["tags"]
        command_box(
            item["command"],
            mode=mode,
            allow_demo=allow_demo,
            label=item["label"],
            tags=tags,
            note=item["note"],
        )


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

    review_tab, technical_tab = st.tabs(["Review", "Technical Drill-Down"])
    with review_tab:
        _render_open_first(row, artifacts)

        st.markdown("### Safe CSV preview")
        _render_csv_preview(artifacts)

        _render_artifacts(row, artifacts)

        st.markdown("### Empirical summary")
        left, right = st.columns([1.1, 1])
        with left:
            st.markdown("#### What this result answers")
            st.write(row["empirical_question"])
            st.markdown(f"**Caption:** {row['caption']}")
            st.markdown(f"**Main constructs:** {row['main_constructs']}")
            st.markdown(f"**Extension relevance:** {row['extension_relevance']}")
        with right:
            st.markdown("#### Review commands")
            st.caption(
                "These commands are provided for copying into a terminal. Command Center runs only a narrow allowlist inside the app."
            )
            command_box(
                f"make export-table-workbench TABLE_ID={row['asset_id']}",
                mode=mode,
                label="Export review bundle",
                tags=["writes ignored outputs"],
            )
            command_box(
                row["make_command"],
                mode=mode,
                allow_demo=False,
                label="Rerun table",
                tags=["requires private data", "writes ignored outputs"],
            )

    with technical_tab:
        _render_technical_drilldown(row, data, mode)
