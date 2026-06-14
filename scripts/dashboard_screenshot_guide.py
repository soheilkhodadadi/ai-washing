from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "portfolio_screenshots"
TARGETS = [
    {
        "view": "Home / Project Overview",
        "url_path": "open root, then select Home / Project Overview",
        "mode": "Demo Mode",
        "purpose": "Portfolio-safe first impression and project metrics.",
        "suggested_file": "01_home_demo.png",
    },
    {
        "view": "Portfolio Demo Mode",
        "url_path": "open root, then select Portfolio Demo Mode",
        "mode": "Demo Mode",
        "purpose": "Case-study overview and reusable methodology narrative.",
        "suggested_file": "02_portfolio_case_study.png",
    },
    {
        "view": "Table Explorer - Main Table 7",
        "url_path": "open root, then select Table Explorer",
        "mode": "Demo Mode",
        "purpose": "Thomas-facing table review flow with Open First guidance.",
        "suggested_file": "03_table_explorer_main_table_7.png",
    },
    {
        "view": "Data Room - Evidence cockpit",
        "url_path": "open root, then select Data Room",
        "mode": "Demo Mode",
        "purpose": "Classifier, patent, and WRDS evidence without private values.",
        "suggested_file": "04_data_room_evidence.png",
    },
    {
        "view": "Extension Lab",
        "url_path": "open root, then select Extension Lab",
        "mode": "Demo Mode",
        "purpose": "Exploratory extension lanes and not-manuscript-ready badges.",
        "suggested_file": "05_extension_lab.png",
    },
    {
        "view": "Command Center",
        "url_path": "open root, then select Command Center",
        "mode": "Demo Mode",
        "purpose": "Approved command registry with execution disabled in Demo Mode.",
        "suggested_file": "06_command_center_demo_disabled.png",
    },
]


def _target_row(target: dict[str, str]) -> str:
    return (
        f"| {target['view']} | {target['url_path']} | {target['mode']} | "
        f"`{target['suggested_file']}` | {target['purpose']} |"
    )


def _display_path(path: Path) -> Path:
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def write_targets() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUT_DIR / "screenshot_targets.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["view", "url_path", "mode", "purpose", "suggested_file"])
        writer.writeheader()
        writer.writerows(TARGETS)

    lines = [
        "# Portfolio Screenshot Targets",
        "",
        "This ignored folder is for local screenshot capture only. Do not commit generated screenshots unless a later "
        "portfolio release explicitly asks for them.",
        "",
        "## How to capture",
        "",
        "1. Start the app with `make dashboard-app` or `make docker-dashboard-app`.",
        "2. Switch to Demo Mode in the sidebar before capturing portfolio screenshots.",
        "3. Capture the views listed below. Suggested filenames are stable so a future portfolio package can refer "
        "to them.",
        "",
        "| View | Navigation | Mode | Suggested file | Purpose |",
        "| --- | --- | --- | --- | --- |",
    ]
    for target in TARGETS:
        lines.append(_target_row(target))
    lines.extend(
        [
            "",
            "Safety rule: screenshots for external portfolio use should not show private data roots, row-level data, "
            "command logs, or Coauthor Mode private-data instructions.",
        ]
    )
    (OUT_DIR / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote screenshot guide: {_display_path(OUT_DIR)}/README.md")
    print(f"Wrote screenshot target map: {_display_path(csv_path)}")


if __name__ == "__main__":
    write_targets()
