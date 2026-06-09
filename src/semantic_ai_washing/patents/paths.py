"""Path helpers for patent construction scripts.

The coauthor workstation keeps raw and derived data outside Git. These helpers
resolve defaults through AIW_DATA_ROOT while still allowing explicit CLI
overrides for one-off rebuilds.
"""

from __future__ import annotations

import os
from pathlib import Path


def data_root() -> Path:
    return Path(os.environ.get("AIW_DATA_ROOT", "data")).resolve()


def data_path(*parts: str) -> str:
    return str(data_root().joinpath(*parts))


def grant_source_root() -> str:
    return os.environ.get("PATENT_DATA_ROOT", data_path("raw", "patentsview", "granted"))


def pregrant_source_root() -> str:
    return os.environ.get(
        "PATENT_PREGRANT_DATA_ROOT",
        data_path("raw", "patentsview", "pregrant"),
    )
