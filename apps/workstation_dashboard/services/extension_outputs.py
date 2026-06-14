from __future__ import annotations

import csv
from dataclasses import dataclass
from io import StringIO
import json
from pathlib import Path
from typing import BinaryIO

import pandas as pd

from services.manifest_store import dashboard_text_is_safe
from services.paths import OUTPUTS_DIR, ROOT, repo_relative

EXTENSIONS_DIR = OUTPUTS_DIR / "extensions"
TEMPLATE_DIR = ROOT / "templates"
SUPPORTED_SUFFIXES = {".csv", ".json", ".md"}
CSV_PREVIEW_ROWS = 25
TEXT_PREVIEW_CHARS = 8_000
MAX_DOWNLOAD_BYTES = 4 * 1024 * 1024
HIDDEN_VALUE = "[private/local path hidden]"


@dataclass(frozen=True)
class ExtensionOutputFile:
    label: str
    path: Path
    rel_path: str
    suffix: str
    category: str
    exists: bool
    size_bytes: int = 0

    @property
    def previewable_csv(self) -> bool:
        return self.exists and self.path.is_file() and self.suffix == ".csv"

    @property
    def previewable_markdown(self) -> bool:
        return self.exists and self.path.is_file() and self.suffix == ".md"

    @property
    def previewable_json(self) -> bool:
        return self.exists and self.path.is_file() and self.suffix == ".json"

    @property
    def safe_downloadable(self) -> bool:
        if not self.exists or not self.path.is_file() or self.size_bytes > MAX_DOWNLOAD_BYTES:
            return False
        if self.suffix in {".md", ".json"}:
            try:
                text = self.path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                return False
            return dashboard_text_is_safe(text) and not _looks_like_private_path(text)
        return self.suffix == ".csv"


@dataclass(frozen=True)
class ExtensionOutputBundle:
    extension_id: str
    output_dir: Path | None
    rel_output_dir: str
    exists: bool
    files: tuple[ExtensionOutputFile, ...]
    note: str = ""


@dataclass(frozen=True)
class SeoSchemaCheck:
    status: str
    row_count: int | None
    columns: tuple[str, ...]
    required_columns: tuple[str, ...]
    preferred_columns: tuple[str, ...]
    missing_required: tuple[str, ...]
    missing_preferred: tuple[str, ...]
    extra_columns: tuple[str, ...]
    identifier_columns_present: tuple[str, ...]
    parse_error: str = ""

    @property
    def is_valid(self) -> bool:
        return self.status == "valid"

    def summary_rows(self) -> pd.DataFrame:
        rows = [
            {"check": "schema_status", "result": self.status},
            {"check": "row_count", "result": "unknown" if self.row_count is None else str(self.row_count)},
            {"check": "required_columns", "result": "; ".join(self.required_columns)},
            {"check": "missing_required", "result": "; ".join(self.missing_required) or "none"},
            {"check": "missing_preferred", "result": "; ".join(self.missing_preferred) or "none"},
            {"check": "extra_columns", "result": "; ".join(self.extra_columns) or "none"},
            {"check": "identifier_columns_present", "result": "; ".join(self.identifier_columns_present) or "none"},
        ]
        if self.parse_error:
            rows.append({"check": "parse_error", "result": self.parse_error})
        return pd.DataFrame(rows)


def _looks_like_private_path(text: str) -> bool:
    compact = str(text or "").strip()
    if not compact:
        return False
    return any(
        marker in compact
        for marker in [
            "/Users/",
            "ai-washing-private-data",
            "DataWork/semantic-patterns",
            "Documents/Projects/semantic-patterns",
        ]
    ) or compact.startswith(("/", "~"))


def _safe_repo_path(raw_path: object, *, required_parent: Path) -> Path | None:
    text = str(raw_path or "").strip()
    if not text or text.startswith(("/", "~")) or "$AIW_DATA_ROOT" in text:
        return None
    parts = Path(text).parts
    if ".." in parts or not dashboard_text_is_safe(text):
        return None
    candidate = (ROOT / text).resolve()
    try:
        candidate.relative_to(required_parent.resolve())
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


def safe_extension_output_dir(row: pd.Series | dict[str, object]) -> Path | None:
    return _safe_repo_path(row.get("output_dir", ""), required_parent=EXTENSIONS_DIR)


def safe_schema_template(row: pd.Series | dict[str, object]) -> Path | None:
    return _safe_repo_path(row.get("schema_template", ""), required_parent=TEMPLATE_DIR)


def _file_category(path: Path) -> str:
    name = path.name.lower()
    if path.suffix.lower() == ".csv":
        return "Aggregate CSV"
    if "summary" in name and path.suffix.lower() == ".json":
        return "Summary JSON"
    if "interpretation" in name or path.suffix.lower() == ".md":
        return "Narrative notes"
    return "Bundle metadata"


def _file_label(path: Path) -> str:
    name = path.name.replace("_", " ").replace("-", " ")
    return name.rsplit(".", 1)[0].title()


def _iter_output_files(path: Path) -> list[Path]:
    if not path.exists() or not path.is_dir():
        return []
    return sorted(
        [child for child in path.rglob("*") if child.is_file() and child.suffix.lower() in SUPPORTED_SUFFIXES],
        key=repo_relative,
    )


def extension_output_bundle(row: pd.Series | dict[str, object]) -> ExtensionOutputBundle:
    extension_id = str(row.get("extension_id", "") or "")
    output_dir = safe_extension_output_dir(row)
    if output_dir is None:
        return ExtensionOutputBundle(
            extension_id=extension_id,
            output_dir=None,
            rel_output_dir="",
            exists=False,
            files=(),
            note="No safe repo-contained output directory is registered.",
        )
    if not output_dir.exists():
        return ExtensionOutputBundle(
            extension_id=extension_id,
            output_dir=output_dir,
            rel_output_dir=repo_relative(output_dir),
            exists=False,
            files=(),
            note="Output directory is not present yet. Run the registered Make command to generate ignored outputs.",
        )
    files = tuple(
        ExtensionOutputFile(
            label=_file_label(path),
            path=path,
            rel_path=repo_relative(path),
            suffix=path.suffix.lower(),
            category=_file_category(path),
            exists=True,
            size_bytes=path.stat().st_size,
        )
        for path in _iter_output_files(output_dir)
    )
    return ExtensionOutputBundle(
        extension_id=extension_id,
        output_dir=output_dir,
        rel_output_dir=repo_relative(output_dir),
        exists=True,
        files=files,
    )


def grouped_extension_files(files: tuple[ExtensionOutputFile, ...]) -> dict[str, list[ExtensionOutputFile]]:
    groups: dict[str, list[ExtensionOutputFile]] = {}
    for file in files:
        groups.setdefault(file.category, []).append(file)
    order = {"Summary JSON": 0, "Narrative notes": 1, "Aggregate CSV": 2, "Bundle metadata": 3}
    return dict(sorted(groups.items(), key=lambda item: order.get(item[0], 9)))


def extension_csv_preview(file: ExtensionOutputFile, *, max_rows: int = CSV_PREVIEW_ROWS) -> pd.DataFrame:
    if not file.previewable_csv:
        return pd.DataFrame()
    return pd.read_csv(file.path, nrows=max_rows, dtype=str).fillna("")


def extension_markdown_preview(file: ExtensionOutputFile, *, max_chars: int = TEXT_PREVIEW_CHARS) -> str:
    if not file.previewable_markdown:
        return ""
    text = file.path.read_text(encoding="utf-8")[:max_chars]
    if not dashboard_text_is_safe(text) or _looks_like_private_path(text):
        return "This note contains local/private path details and is hidden in the dashboard."
    return text


def _sanitize_json_value(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): _sanitize_json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize_json_value(item) for item in value]
    if isinstance(value, str):
        if not dashboard_text_is_safe(value) or _looks_like_private_path(value):
            return HIDDEN_VALUE
        return value
    return value


def extension_json_preview(file: ExtensionOutputFile) -> dict[str, object]:
    if not file.previewable_json:
        return {}
    try:
        payload = json.loads(file.path.read_text(encoding="utf-8"))
    except ValueError:
        return {"parse_error": "Unable to parse JSON preview."}
    sanitized = _sanitize_json_value(payload)
    if not isinstance(sanitized, dict):
        return {"value": sanitized}
    return sanitized


def status_badges(row: pd.Series | dict[str, object]) -> list[str]:
    explicit = str(row.get("status_badges", "") or "")
    badges = [item.strip() for item in explicit.split(";") if item.strip()]
    if not badges:
        maturity = str(row.get("maturity_status", "") or "").replace("_", " ").strip().title()
        manuscript = str(row.get("manuscript_status", "") or "").replace("_", " ").strip().title()
        badges = [item for item in [maturity, manuscript] if item]
    return badges


def schema_template_fields(template_path: Path | None = None) -> pd.DataFrame:
    path = template_path or (TEMPLATE_DIR / "seo_offering_terms_schema.csv")
    if not path.is_file():
        return pd.DataFrame(columns=["field_name", "required", "preferred_type", "description"])
    return pd.read_csv(path, dtype=str).fillna("")


def _read_uploaded_csv(source: str | bytes | BinaryIO) -> tuple[list[str], int, str]:
    try:
        if isinstance(source, bytes):
            raw = source.decode("utf-8-sig")
            buffer = StringIO(raw)
        elif isinstance(source, str):
            buffer = Path(source).open(newline="", encoding="utf-8-sig")
        else:
            raw_bytes = source.read()
            if isinstance(raw_bytes, str):
                buffer = StringIO(raw_bytes)
            else:
                buffer = StringIO(raw_bytes.decode("utf-8-sig"))
    except UnicodeDecodeError as exc:
        return [], 0, f"unable to decode as UTF-8 CSV: {exc}"

    try:
        with buffer:
            reader = csv.reader(buffer)
            try:
                columns = next(reader)
            except StopIteration:
                return [], 0, "CSV file is empty"
            row_count = sum(1 for _ in reader)
    except (csv.Error, OSError) as exc:
        return [], 0, f"unable to parse CSV: {exc}"
    columns = [column.strip() for column in columns if column.strip()]
    return columns, row_count, ""


def check_seo_schema(source: str | bytes | BinaryIO, *, template_path: Path | None = None) -> SeoSchemaCheck:
    template = schema_template_fields(template_path)
    required = tuple(template.loc[template["required"].str.lower() == "yes", "field_name"].astype(str))
    preferred = tuple(template.loc[template["required"].str.lower() == "preferred", "field_name"].astype(str))
    columns, row_count, error = _read_uploaded_csv(source)
    if error:
        return SeoSchemaCheck(
            status="parse_error",
            row_count=None,
            columns=(),
            required_columns=required,
            preferred_columns=preferred,
            missing_required=required,
            missing_preferred=preferred,
            extra_columns=(),
            identifier_columns_present=(),
            parse_error=error,
        )

    column_set = set(columns)
    required_set = set(required)
    preferred_set = set(preferred)
    missing_required = tuple(column for column in required if column not in column_set)
    missing_preferred = tuple(column for column in preferred if column not in column_set)
    known = required_set | preferred_set | set(template["field_name"].astype(str))
    extra = tuple(column for column in columns if column not in known)
    identifier_candidates = ("firm_id", "gvkey", "permno", "cik", "cusip")
    identifiers = tuple(column for column in identifier_candidates if column in column_set)
    status = "valid" if not missing_required else "missing_required_columns"
    if not identifiers:
        status = "missing_identifier_column"
    return SeoSchemaCheck(
        status=status,
        row_count=row_count,
        columns=tuple(columns),
        required_columns=required,
        preferred_columns=preferred,
        missing_required=missing_required,
        missing_preferred=missing_preferred,
        extra_columns=extra,
        identifier_columns_present=identifiers,
    )


def check_seo_schema_file(path: Path) -> SeoSchemaCheck:
    # CLI paths can be absolute because users check local private files, but the
    # checker reports metadata only and never prints row values.
    return check_seo_schema(str(path))
