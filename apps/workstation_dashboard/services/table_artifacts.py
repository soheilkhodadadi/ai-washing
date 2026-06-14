from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
import zipfile

import pandas as pd

from services.manifest_store import dashboard_text_is_safe, split_tokens
from services.paths import OUTPUTS_DIR, ROOT, repo_relative

REFERENCE_STATUS = "frozen_v4_3_reference"
GENERATED_STATUS = "generated_convenience"
WORKBENCH_STATUS = "workbench_bundle"
MISSING_STATUS = "missing"

SUPPORTED_SUFFIXES = {".csv", ".tex", ".docx", ".pdf", ".png", ".md", ".json"}
RUN_DIR_SUFFIXES = {".docx", ".pdf", ".png", ".md", ".json"}
WORKBENCH_SUFFIXES = SUPPORTED_SUFFIXES | {".sh"}
CSV_PREVIEW_ROWS = 25
MAX_DOWNLOAD_BYTES = 8 * 1024 * 1024


@dataclass(frozen=True)
class TableArtifact:
    label: str
    path: Path
    rel_path: str
    suffix: str
    category: str
    status: str
    exists: bool
    source: str
    size_bytes: int = 0

    @property
    def downloadable(self) -> bool:
        return self.exists and self.path.is_file() and self.size_bytes <= MAX_DOWNLOAD_BYTES

    @property
    def previewable_csv(self) -> bool:
        return self.exists and self.path.is_file() and self.suffix == ".csv"


def table_display_label(row: pd.Series | dict[str, object]) -> str:
    paper_label = str(row.get("paper_label", "") or "").strip()
    caption = str(row.get("caption", "") or "").strip()
    asset_id = str(row.get("asset_id", "") or "").strip()
    if paper_label and caption:
        return f"{paper_label} - {caption}"
    if paper_label:
        return paper_label
    return asset_id


def split_reference_outputs(value: object) -> list[str]:
    # Workbench references use pipe separators; split_tokens also tolerates semicolons.
    return split_tokens(value, delimiter="|")


def safe_repo_path(raw_path: str) -> Path | None:
    text = str(raw_path or "").strip()
    if not text or "$AIW_DATA_ROOT" in text or text.startswith(("~", "/")):
        return None
    if ".." in Path(text).parts:
        return None
    if not dashboard_text_is_safe(text):
        return None
    candidate = (ROOT / text).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        return None
    return candidate


def artifact_category(path: Path, *, source: str) -> str:
    suffix = path.suffix.lower()
    name = path.name.lower()
    if suffix in {".docx", ".pdf", ".png"}:
        return "Review first"
    if suffix == ".csv" and "figure_series" not in name:
        return "Numeric audit"
    if suffix == ".tex":
        return "Manuscript integration"
    if suffix == ".md" or "writer_packet" in name or "result_notes" in name or "figure_series" in name:
        return "Notes"
    if source == "workbench":
        return "Workbench metadata"
    return "Other evidence"


def artifact_label(path: Path, *, status: str) -> str:
    suffix = path.suffix.lower().lstrip(".").upper() or "File"
    if status == REFERENCE_STATUS:
        prefix = "Frozen v4.3"
    elif status == WORKBENCH_STATUS:
        prefix = "Workbench bundle"
    else:
        prefix = "Generated"
    if "writer_packet" in path.name:
        return f"{prefix} writer packet"
    if "result_notes" in path.name:
        return f"{prefix} result notes"
    if "figure_series" in path.name:
        return f"{prefix} figure-series CSV"
    return f"{prefix} {suffix}"


def _artifact_from_path(path: Path, *, status: str, source: str) -> TableArtifact:
    suffix = path.suffix.lower()
    exists = path.is_file()
    size = path.stat().st_size if exists else 0
    return TableArtifact(
        label=artifact_label(path, status=status),
        path=path,
        rel_path=repo_relative(path),
        suffix=suffix,
        category=artifact_category(path, source=source),
        status=status,
        exists=exists,
        source=source,
        size_bytes=size,
    )


def _iter_safe_files(path: Path, *, suffixes: set[str]) -> list[Path]:
    if path.is_file() and path.suffix.lower() in suffixes:
        return [path]
    if not path.is_dir():
        return []
    files = [child for child in path.rglob("*") if child.is_file() and child.suffix.lower() in suffixes]
    return sorted(files, key=repo_relative)


def reference_artifacts(row: pd.Series | dict[str, object]) -> list[TableArtifact]:
    artifacts: list[TableArtifact] = []
    for raw in split_reference_outputs(row.get("reference_outputs", "")):
        path = safe_repo_path(raw)
        if path is None:
            continue
        if path.is_file():
            artifacts.append(_artifact_from_path(path, status=REFERENCE_STATUS, source="reference"))
        elif path.is_dir():
            for child in _iter_safe_files(path, suffixes=RUN_DIR_SUFFIXES):
                artifacts.append(_artifact_from_path(child, status=REFERENCE_STATUS, source="reference_run_dir"))
        else:
            artifacts.append(
                TableArtifact(
                    label=f"Missing reference: {Path(raw).name}",
                    path=path,
                    rel_path=repo_relative(path),
                    suffix=path.suffix.lower(),
                    category="Missing",
                    status=MISSING_STATUS,
                    exists=False,
                    source="reference",
                )
            )
    return artifacts


def workbench_artifacts(asset_id: str) -> list[TableArtifact]:
    bundle = OUTPUTS_DIR / "workbench" / asset_id
    if not bundle.exists():
        return []
    return [
        _artifact_from_path(path, status=WORKBENCH_STATUS, source="workbench")
        for path in _iter_safe_files(bundle, suffixes=WORKBENCH_SUFFIXES)
    ]


def generated_artifacts(asset_id: str) -> list[TableArtifact]:
    # Generated exports are optional convenience files. They are ignored by Git,
    # so the app must remain useful when this list is empty.
    generated_roots = [
        OUTPUTS_DIR / "paper_exports",
        OUTPUTS_DIR / "reproduced",
    ]
    needles = {asset_id.lower()}
    artifacts: list[TableArtifact] = []
    for root in generated_roots:
        if not root.exists():
            continue
        for path in _iter_safe_files(root, suffixes=SUPPORTED_SUFFIXES):
            lower = path.name.lower()
            if any(needle in lower for needle in needles) or "test_30" in lower and asset_id == "T30":
                artifacts.append(_artifact_from_path(path, status=GENERATED_STATUS, source="generated_outputs"))
    return artifacts


def table_artifacts(row: pd.Series | dict[str, object]) -> list[TableArtifact]:
    asset_id = str(row.get("asset_id", "") or "")
    artifacts = reference_artifacts(row)
    artifacts.extend(workbench_artifacts(asset_id))
    artifacts.extend(generated_artifacts(asset_id))

    # Keep a stable, compact review surface. If the same path appears through
    # multiple sources, keep the first status found in the order above.
    by_path: dict[Path, TableArtifact] = {}
    for artifact in artifacts:
        by_path.setdefault(artifact.path.resolve(), artifact)
    return sorted(by_path.values(), key=lambda item: (category_rank(item.category), status_rank(item.status), item.rel_path))


def category_rank(category: str) -> int:
    order = {
        "Review first": 0,
        "Numeric audit": 1,
        "Manuscript integration": 2,
        "Notes": 3,
        "Workbench metadata": 4,
        "Other evidence": 5,
        "Missing": 9,
    }
    return order.get(category, 8)


def status_rank(status: str) -> int:
    order = {
        REFERENCE_STATUS: 0,
        WORKBENCH_STATUS: 1,
        GENERATED_STATUS: 2,
        MISSING_STATUS: 9,
    }
    return order.get(status, 8)


def grouped_artifacts(artifacts: list[TableArtifact]) -> dict[str, list[TableArtifact]]:
    groups: dict[str, list[TableArtifact]] = {}
    for artifact in artifacts:
        groups.setdefault(artifact.category, []).append(artifact)
    return dict(sorted(groups.items(), key=lambda item: category_rank(item[0])))


def csv_preview(artifact: TableArtifact, *, max_rows: int = CSV_PREVIEW_ROWS) -> pd.DataFrame:
    if not artifact.previewable_csv:
        return pd.DataFrame()
    return pd.read_csv(artifact.path, nrows=max_rows, dtype=str).fillna("")


def preferred_review_artifact(artifacts: list[TableArtifact]) -> TableArtifact | None:
    suffix_order = {".docx": 0, ".png": 1, ".pdf": 2, ".csv": 3, ".tex": 4}
    candidates = [artifact for artifact in artifacts if artifact.exists and artifact.suffix in suffix_order]
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: (suffix_order[item.suffix], status_rank(item.status), item.rel_path))[0]


def build_review_packet(row: pd.Series | dict[str, object], artifacts: list[TableArtifact]) -> bytes:
    buffer = BytesIO()
    asset_id = str(row.get("asset_id", "") or "table")
    readme = f"""# {table_display_label(row)}

Asset ID: {asset_id}

Empirical question: {row.get("empirical_question", "")}

Caption: {row.get("caption", "")}

Canonical status: frozen v4.3 reference files are the baseline. Generated and workbench files are convenience copies.

This packet contains only repo-contained public/review artifacts. It does not include private panels, raw data, access details, or generated private outputs.
"""
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("OPEN_FIRST.md", readme)
        included: set[str] = set()
        for artifact in artifacts:
            if not artifact.downloadable:
                continue
            folder = artifact.category.lower().replace(" ", "_")
            arcname = f"{folder}/{artifact.path.name}"
            if arcname in included:
                continue
            included.add(arcname)
            zf.write(artifact.path, arcname=arcname)
    return buffer.getvalue()
