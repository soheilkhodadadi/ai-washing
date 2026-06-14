from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from services.paths import MANIFEST_DIR

FORBIDDEN_PATTERNS = [
    "/Users/soheilkhodadadi",
    "DataWork/semantic-patterns",
    "Documents/Projects/semantic-patterns",
    "password",
    "credential",
    "secret",
]


@dataclass(frozen=True)
class DashboardData:
    tables: pd.DataFrame
    data_products: pd.DataFrame
    extensions: pd.DataFrame


def load_manifest(name: str, manifest_dir: Path = MANIFEST_DIR) -> pd.DataFrame:
    path = manifest_dir / name
    return pd.read_csv(path).fillna("")


def load_dashboard_data(manifest_dir: Path = MANIFEST_DIR) -> DashboardData:
    return DashboardData(
        tables=load_manifest("paper_table_workbench.csv", manifest_dir),
        data_products=load_manifest("data_product_catalog.csv", manifest_dir),
        extensions=load_manifest("extension_workbench.csv", manifest_dir),
    )


def filter_frame(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if not query:
        return df
    mask = df.astype(str).agg(" ".join, axis=1).str.lower().str.contains(query.lower(), regex=False)
    return df.loc[mask]


def dashboard_text_is_safe(text: str) -> bool:
    lower = text.lower()
    return not any(pattern.lower() in lower for pattern in FORBIDDEN_PATTERNS)


def public_text(value: object) -> str:
    text = str(value or "")
    replacements = {
        "credential-based": "access-controlled",
        "Credential-based": "Access-controlled",
        "credentials": "access details",
        "Credentials": "Access details",
        "credential": "access detail",
        "Credential": "Access detail",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def public_frame(df: pd.DataFrame) -> pd.DataFrame:
    return df.map(public_text)


def split_tokens(value: object, *, delimiter: str = ";") -> list[str]:
    text = str(value or "")
    return [item.strip() for item in text.split(delimiter) if item.strip()]
