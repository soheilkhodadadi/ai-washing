from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
from typing import Any

import pandas as pd

from services.constructs import CONSTRUCTS
from services.manifest_store import dashboard_text_is_safe, load_manifest, split_tokens
from services.paths import ROOT, repo_relative

MAX_DIRECTORY_COUNT = 1000
MAX_SCHEMA_COLUMNS = 60

CONSTRUCT_ALIASES = {
    "ai_disclosure": [
        "ai disclosure",
        "ai sentence",
        "classifier",
        "classification",
        "credai",
        "ai focus",
        "actionable",
        "speculative",
    ],
    "patent_mismatch": [
        "patentmismatch",
        "patent mismatch",
        "weak patent",
        "future ai patent",
        "future ai application",
        "disclosure-patent",
    ],
    "patent_matching": ["patent matching", "assignee", "applicant", "company identity", "patent keyword"],
    "market_returns": ["market", "return", "alpha", "crsp", "event", "factor", "filing-event"],
    "capital_raising": ["capital", "share", "shrout", "equity", "issuance", "offering", "seo"],
    "execucomp": ["execucomp", "ceo", "incentive", "delta", "vega", "compensation"],
    "sec_scrutiny": ["sec", "comment", "scrutiny", "enforcement", "timing"],
}


@dataclass(frozen=True)
class SourceScript:
    module: str
    rel_path: str
    exists: bool
    status: str


@dataclass(frozen=True)
class DataPathStatus:
    logical_path: str
    display_path: str
    status: str
    kind: str
    suffix: str = ""
    size_bytes: int | None = None
    file_count: str = ""
    row_count: int | None = None
    columns: tuple[str, ...] = ()
    schema_source: str = ""
    note: str = ""

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "logical_path": self.logical_path,
            "display_path": self.display_path,
            "status": self.status,
            "kind": self.kind,
            "suffix": self.suffix,
            "size_bytes": self.size_bytes,
            "file_count": self.file_count,
            "row_count": self.row_count,
            "columns": list(self.columns),
            "schema_source": self.schema_source,
            "note": self.note,
        }


def load_crosswalk() -> pd.DataFrame:
    return load_manifest("table_to_script_crosswalk.csv")


def load_reproduction_status() -> pd.DataFrame:
    path = ROOT / "docs" / "full_reproduction_status.csv"
    if not path.is_file():
        return pd.DataFrame()
    return pd.read_csv(path).fillna("")


def reproduction_status_for_asset(asset_id: str, status_frame: pd.DataFrame | None = None) -> pd.Series | None:
    df = status_frame if status_frame is not None else load_reproduction_status()
    if df.empty or "table_id" not in df.columns:
        return None
    match = df.loc[df["table_id"].astype(str).str.lower() == asset_id.lower()]
    if match.empty:
        return None
    return match.iloc[0]


def source_script_for_module(module: object) -> SourceScript:
    module_text = str(module or "").strip()
    if not module_text.startswith("semantic_ai_washing."):
        return SourceScript(module_text, "not a semantic_ai_washing module", False, "not_applicable")
    path = ROOT / "src" / Path(*module_text.split(".")).with_suffix(".py")
    exists = path.is_file()
    return SourceScript(module_text, repo_relative(path), exists, "present" if exists else "missing")


def crosswalk_for_asset(asset_id: str, crosswalk: pd.DataFrame | None = None) -> pd.Series | None:
    df = crosswalk if crosswalk is not None else load_crosswalk()
    match = df.loc[df["table_id"].astype(str).str.lower() == asset_id.lower()]
    if match.empty:
        return None
    return match.iloc[0]


def _asset_in_list(asset_id: str, value: object) -> bool:
    return bool(re.search(rf"\b{re.escape(asset_id)}\b", str(value or ""), flags=re.IGNORECASE))


def linked_data_products(table_row: pd.Series | dict[str, object], data_products: pd.DataFrame) -> pd.DataFrame:
    asset_id = str(table_row.get("asset_id", "") or "")
    primary = str(table_row.get("primary_data_product", "") or "").lower()
    if data_products.empty:
        return data_products

    def matches(product: pd.Series) -> bool:
        if _asset_in_list(asset_id, product.get("tables_using_it", "")):
            return True
        product_id = str(product.get("product_id", "") or "").replace("_", " ").lower()
        purpose = str(product.get("purpose", "") or "").lower()
        return bool(product_id and product_id in primary) or bool(purpose and purpose[:40] in primary)

    linked = data_products.loc[data_products.apply(matches, axis=1)].copy()
    if linked.empty and primary:
        linked = data_products.head(0).copy()
    return linked


def linked_constructs(table_row: pd.Series | dict[str, object]) -> list[dict[str, str]]:
    haystack = " ".join(
        str(table_row.get(key, "") or "")
        for key in ["main_constructs", "empirical_question", "primary_data_product", "caption", "extension_relevance"]
    ).lower()
    matches: list[dict[str, str]] = []
    seen: set[str] = set()
    for construct in CONSTRUCTS:
        construct_id = construct["id"]
        aliases = [construct_id.replace("_", " "), construct["title"].lower(), *CONSTRUCT_ALIASES.get(construct_id, [])]
        if any(alias and alias in haystack for alias in aliases):
            matches.append(construct)
            seen.add(construct_id)
    if not matches and str(table_row.get("main_constructs", "") or "").strip():
        # Fall back to the broad disclosure playbook when constructs are present
        # but not matched by the small alias map.
        for construct in CONSTRUCTS:
            if construct["id"] == "ai_disclosure" and construct["id"] not in seen:
                matches.append(construct)
                break
    return matches


def linked_extensions(table_row: pd.Series | dict[str, object], extensions: pd.DataFrame) -> pd.DataFrame:
    asset_id = str(table_row.get("asset_id", "") or "")
    if extensions.empty:
        return extensions
    linked = extensions.loc[extensions["reference_table_ids"].apply(lambda value: _asset_in_list(asset_id, value))].copy()
    return linked


def split_private_paths(value: object) -> list[str]:
    text = str(value or "")
    parts: list[str] = []
    for chunk in text.replace(";", "|").split("|"):
        item = chunk.strip()
        if item:
            parts.append(item)
    return parts


def private_data_root() -> Path | None:
    raw = os.environ.get("AIW_DATA_ROOT")
    if not raw:
        return None
    return Path(raw).expanduser().resolve()


def _display_mounted_path(path: Path, root: Path) -> str:
    try:
        return "$AIW_DATA_ROOT/" + str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return "$AIW_DATA_ROOT/<outside-root>"


def _safe_logical_to_mounted(logical_path: str, root: Path) -> tuple[Path | None, str]:
    text = logical_path.strip()
    if not text:
        return None, "empty logical path"
    if text.startswith(("~", "/")) or ".." in Path(text).parts:
        return None, "unsafe path outside the private data contract"
    if not dashboard_text_is_safe(text):
        return None, "unsafe path text"
    if not text.startswith("data/"):
        return None, "reference-only path; not resolved through AIW_DATA_ROOT"
    mounted = (root / text.removeprefix("data/")).resolve()
    try:
        mounted.relative_to(root)
    except ValueError:
        return None, "resolved outside AIW_DATA_ROOT"
    return mounted, ""


def _format_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{size} B"


def _tabular_metadata(path: Path) -> tuple[int | None, tuple[str, ...], str]:
    suffix = path.suffix.lower()
    if suffix not in {".parquet", ".csv"}:
        return None, (), "unsupported file type"
    try:
        import duckdb

        con = duckdb.connect(database=":memory:", read_only=False)
        try:
            if suffix == ".parquet":
                relation = con.read_parquet(str(path))
            else:
                relation = con.read_csv(str(path), sample_size=20480)
            columns = tuple(str(column) for column in relation.columns[:MAX_SCHEMA_COLUMNS])
            row_count = int(relation.aggregate("count(*)").fetchone()[0])
            note = "duckdb metadata"
            if len(relation.columns) > MAX_SCHEMA_COLUMNS:
                note += f"; showing first {MAX_SCHEMA_COLUMNS} of {len(relation.columns)} columns"
            return row_count, columns, note
        finally:
            con.close()
    except Exception as exc:  # pragma: no cover - fallback/defensive path
        return None, (), f"schema unavailable: {exc}"


def _directory_file_count(path: Path) -> tuple[str, Path | None]:
    count = 0
    first_tabular: Path | None = None
    capped = False
    for child in path.rglob("*"):
        if not child.is_file():
            continue
        count += 1
        if first_tabular is None and child.suffix.lower() in {".parquet", ".csv"}:
            first_tabular = child
        if count >= MAX_DIRECTORY_COUNT:
            capped = True
            break
    return (f">={MAX_DIRECTORY_COUNT}" if capped else str(count)), first_tabular


def data_product_path_statuses(product_row: pd.Series | dict[str, object]) -> list[DataPathStatus]:
    root = private_data_root()
    statuses: list[DataPathStatus] = []
    for logical_path in split_private_paths(product_row.get("logical_private_path", "")):
        if root is None:
            statuses.append(
                DataPathStatus(
                    logical_path=logical_path,
                    display_path="$AIW_DATA_ROOT is not set",
                    status="not_checked",
                    kind="unknown",
                    note="Set AIW_DATA_ROOT to enable metadata-only status checks.",
                )
            )
            continue
        mounted, error = _safe_logical_to_mounted(logical_path, root)
        if mounted is None:
            statuses.append(
                DataPathStatus(
                    logical_path=logical_path,
                    display_path=logical_path,
                    status="not_resolved",
                    kind="reference",
                    note=error,
                )
            )
            continue
        display = _display_mounted_path(mounted, root)
        if mounted.is_file():
            row_count, columns, note = _tabular_metadata(mounted)
            statuses.append(
                DataPathStatus(
                    logical_path=logical_path,
                    display_path=display,
                    status="present",
                    kind="file",
                    suffix=mounted.suffix.lower() or "none",
                    size_bytes=mounted.stat().st_size,
                    row_count=row_count,
                    columns=columns,
                    schema_source=display,
                    note=note,
                )
            )
        elif mounted.is_dir():
            file_count, schema_file = _directory_file_count(mounted)
            row_count: int | None = None
            columns: tuple[str, ...] = ()
            note = "directory metadata"
            schema_source = ""
            if schema_file is not None:
                row_count, columns, note = _tabular_metadata(schema_file)
                schema_source = _display_mounted_path(schema_file, root)
            statuses.append(
                DataPathStatus(
                    logical_path=logical_path,
                    display_path=display,
                    status="present",
                    kind="directory",
                    file_count=file_count,
                    row_count=row_count,
                    columns=columns,
                    schema_source=schema_source,
                    note=note,
                )
            )
        else:
            statuses.append(
                DataPathStatus(
                    logical_path=logical_path,
                    display_path=display,
                    status="missing",
                    kind="not_found",
                    note="Path is listed in the catalog but was not found under AIW_DATA_ROOT.",
                )
            )
    return statuses


def command_set(table_row: pd.Series | dict[str, object], data_products: pd.DataFrame, extensions: pd.DataFrame) -> list[dict[str, str]]:
    asset_id = str(table_row.get("asset_id", "") or "")
    commands = [
        {
            "label": "Export table bundle",
            "command": f"make export-table-workbench TABLE_ID={asset_id}",
            "tags": "writes ignored outputs",
            "note": "Creates or refreshes outputs/workbench/<asset_id>/.",
        },
        {
            "label": "Rerun table",
            "command": str(table_row.get("make_command", "") or ""),
            "tags": "requires private data; writes ignored outputs",
            "note": "Uses the frozen v4.3 reproduction command for this asset.",
        },
        {
            "label": "Show owning script",
            "command": f"make table-script TABLE_ID={asset_id}",
            "tags": "read-only",
            "note": "Prints module and repo-relative source path.",
        },
    ]
    for _, product in data_products.iterrows():
        product_id = str(product.get("product_id", "") or "")
        if product_id:
            commands.append(
                {
                    "label": f"Locate {product_id}",
                    "command": f"AIW_DATA_ROOT=/path/to/ai-washing-private-data make locate-data PRODUCT_ID={product_id} PREVIEW=1",
                    "tags": "requires private data; read-only metadata",
                    "note": "Reports existence, row counts, and schema summaries without printing private values.",
                }
            )
    for _, extension in extensions.iterrows():
        command = str(extension.get("make_command", "") or "")
        if command:
            commands.append(
                {
                    "label": str(extension.get("title", "") or extension.get("extension_id", "Extension")),
                    "command": command,
                    "tags": "extension; writes ignored outputs",
                    "note": str(extension.get("interpretation_limits", "") or ""),
                }
            )
    return commands
