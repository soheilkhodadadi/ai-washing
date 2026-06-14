from __future__ import annotations

import argparse
from pathlib import Path
import sys

APP_DIR = Path(__file__).resolve().parents[1] / "apps" / "workstation_dashboard"
sys.path.insert(0, str(APP_DIR))

from services.extension_outputs import check_seo_schema_file  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an SEO/offering-terms CSV against the AI Washing extension template.")
    parser.add_argument("--file", required=True, help="CSV file to validate. Values are not printed; only schema metadata is reported.")
    args = parser.parse_args()

    path = Path(args.file).expanduser()
    if not path.is_file():
        print(f"SEO/offering-terms file not found: {path}", file=sys.stderr)
        return 2

    result = check_seo_schema_file(path)
    print("# SEO/offering-terms schema check")
    print(f"status: {result.status}")
    print(f"row_count: {'unknown' if result.row_count is None else result.row_count}")
    print(f"columns: {'; '.join(result.columns) if result.columns else 'none'}")
    print(f"required_columns: {'; '.join(result.required_columns)}")
    print(f"missing_required: {'; '.join(result.missing_required) or 'none'}")
    print(f"missing_preferred: {'; '.join(result.missing_preferred) or 'none'}")
    print(f"extra_columns: {'; '.join(result.extra_columns) or 'none'}")
    print(f"identifier_columns_present: {'; '.join(result.identifier_columns_present) or 'none'}")
    if result.parse_error:
        print(f"parse_error: {result.parse_error}")
    return 0 if result.is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
