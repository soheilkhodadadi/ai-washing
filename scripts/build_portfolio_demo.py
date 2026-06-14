from __future__ import annotations

import csv
import html
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "public_demo"
OUT_HTML = OUT_DIR / "index.html"

MANIFESTS = {
    "tables": ROOT / "manifests" / "paper_table_workbench.csv",
    "data_products": ROOT / "manifests" / "data_product_catalog.csv",
    "extensions": ROOT / "manifests" / "extension_workbench.csv",
}
REPRO_STATUS = ROOT / "docs" / "full_reproduction_status.csv"

FORBIDDEN_PATTERNS = [
    "/Users/soheilkhodadadi",
    "DataWork/semantic-patterns",
    "Documents/Projects/semantic-patterns",
    "ai-washing-private-data",
    "password",
    "credential",
    "secret",
]

SHOWCASE_PRODUCTS = [
    "final_hybrid_classifier_outputs",
    "patent_match_artifacts",
    "annual_nlp_patent_panel",
    "filing_event_estimation_sample",
    "patent_keyword_metadata",
    "crsp_compustat_bridge",
]

SHOWCASE_TABLES = ["T00", "T16", "T17", "T30", "T09"]


class PortfolioBuildError(RuntimeError):
    pass


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def slug(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")


def card(title: str, kicker: str, body: str, meta: Iterable[str] = (), *, accent: str = "blue") -> str:
    meta_html = "".join(f'<span class="pill">{e(item)}</span>' for item in meta if item)
    return f"""
<article class="card {accent}">
  <div class="kicker">{e(kicker)}</div>
  <h3>{e(title)}</h3>
  <p>{e(body)}</p>
  <div class="pills">{meta_html}</div>
</article>
"""


def status_metrics(status_rows: list[dict[str, str]]) -> dict[str, int]:
    csv_exact = sum(1 for row in status_rows if row.get("csv_status") == "exact_match")
    table_rows = [row for row in status_rows if row.get("asset_type") == "table"]
    figure_rows = [row for row in status_rows if row.get("asset_type") == "figure"]
    return {
        "csv_exact": csv_exact,
        "status_rows": len(status_rows),
        "status_tables": len(table_rows),
        "status_figures": len(figure_rows),
    }


def table_showcase(rows: list[dict[str, str]]) -> str:
    by_id = {row["asset_id"]: row for row in rows}
    cards: list[str] = []
    for asset_id in SHOWCASE_TABLES:
        row = by_id.get(asset_id)
        if not row:
            continue
        cards.append(
            card(
                f"{row['paper_label']} ({asset_id})",
                row["paper_section"],
                row["empirical_question"],
                [asset_id, row["primary_data_product"], row["main_constructs"].split(",")[0], "table workbench ready"],
                accent="green" if asset_id == "T30" else "blue",
            )
        )
    return "\n".join(cards)


def data_showcase(rows: list[dict[str, str]]) -> str:
    by_id = {row["product_id"]: row for row in rows}
    cards: list[str] = []
    for product_id in SHOWCASE_PRODUCTS:
        row = by_id.get(product_id)
        if not row:
            continue
        cards.append(
            card(
                product_id.replace("_", " ").title(),
                row["coverage"],
                row["purpose"],
                [product_id, row["keys"], row["extension_relevance"]],
                accent="gold" if "patent" in product_id else "blue",
            )
        )
    return "\n".join(cards)


def extension_showcase(rows: list[dict[str, str]]) -> str:
    cards: list[str] = []
    for row in rows:
        cards.append(
            card(
                row["title"], 
                row["maturity_status"].replace("_", " ").title(),
                row["research_question"],
                [
                    row["extension_id"],
                    row["manuscript_status"].replace("_", " ").title(),
                    row["status_badges"],
                    row["interpretation_limits"],
                ],
                accent="rose" if "future" in row["maturity_status"] else "green",
            )
        )
    return "\n".join(cards)


def html_document(tables: list[dict[str, str]], data_products: list[dict[str, str]], extensions: list[dict[str, str]], status_rows: list[dict[str, str]]) -> str:
    table_count = sum(1 for row in tables if row["asset_type"] == "table")
    figure_count = sum(1 for row in tables if row["asset_type"] == "figure")
    metrics = status_metrics(status_rows)
    t30 = next((row for row in tables if row["asset_id"] == "T30"), {})
    status_line = f"{metrics['csv_exact']} table/figure status rows with exact CSV evidence" if status_rows else "CSV evidence status available in the workstation"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI Washing Analytics Workstation - Public Demo</title>
  <style>
    :root {{
      --ink: #10222b;
      --muted: #64727a;
      --paper: #fbf7ee;
      --panel: rgba(255, 255, 255, 0.82);
      --line: #d9ddd2;
      --teal: #0d5c63;
      --blue: #174ea6;
      --green: #2f6f4e;
      --gold: #b77816;
      --rose: #9f1239;
      --shadow: 0 24px 70px rgba(16, 34, 43, 0.14);
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ margin: 0; color: var(--ink); background: radial-gradient(circle at 12% 0%, #dff4f0 0, rgba(223,244,240,0) 28rem), radial-gradient(circle at 80% 8%, #ffe7b8 0, rgba(255,231,184,0) 24rem), linear-gradient(180deg, #fbf7ee 0%, #f4f0e5 100%); font-family: ui-serif, Georgia, 'Times New Roman', serif; }}
    nav {{ position: sticky; top: 0; z-index: 10; display: flex; justify-content: space-between; gap: 1rem; align-items: center; padding: .9rem min(6vw, 5rem); background: rgba(251,247,238,.84); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(217,221,210,.75); }}
    nav a {{ color: var(--ink); text-decoration: none; font-weight: 700; margin-left: .9rem; }}
    .brand {{ display: flex; align-items: center; gap: .65rem; font-weight: 800; }}
    .mark {{ width: 2.15rem; height: 2.15rem; border-radius: 1rem; background: conic-gradient(from 210deg, var(--teal), #f3c45f, #f5efe2, var(--teal)); box-shadow: var(--shadow); }}
    header {{ padding: 4.5rem min(6vw, 5rem) 3rem; }}
    .eyebrow {{ color: var(--teal); letter-spacing: .16em; text-transform: uppercase; font-size: .78rem; font-weight: 800; }}
    h1 {{ font-size: clamp(2.6rem, 7vw, 6.7rem); letter-spacing: -.055em; line-height: .92; margin: .55rem 0 1.2rem; max-width: 1120px; }}
    .hero-copy {{ color: var(--muted); max-width: 910px; font-size: 1.22rem; line-height: 1.65; }}
    .hero-actions {{ display: flex; gap: .75rem; flex-wrap: wrap; margin-top: 1.7rem; }}
    .button {{ display: inline-flex; align-items: center; gap: .45rem; border-radius: 999px; padding: .88rem 1.05rem; text-decoration: none; font-weight: 800; border: 1px solid var(--line); background: white; color: var(--ink); box-shadow: 0 10px 28px rgba(16,34,43,.08); }}
    .button.primary {{ background: var(--ink); color: white; border-color: var(--ink); }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 1rem; max-width: 980px; margin-top: 2.2rem; }}
    .metric {{ background: var(--panel); border: 1px solid var(--line); border-radius: 1.35rem; padding: 1rem 1.05rem; box-shadow: 0 12px 40px rgba(16,34,43,.08); }}
    .metric b {{ display: block; font-size: 2.2rem; letter-spacing: -.04em; }}
    .metric span {{ color: var(--muted); }}
    main {{ padding: 0 min(6vw, 5rem) 4rem; }}
    section {{ margin-top: 3rem; }}
    h2 {{ font-size: clamp(1.75rem, 3.3vw, 3.2rem); letter-spacing: -.035em; margin: 0 0 .5rem; }}
    .section-copy {{ color: var(--muted); max-width: 900px; font-size: 1.05rem; line-height: 1.6; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 1rem; margin-top: 1.1rem; }}
    .card {{ min-height: 255px; background: var(--panel); border: 1px solid var(--line); border-radius: 1.35rem; padding: 1.1rem; box-shadow: 0 16px 42px rgba(16,34,43,.08); position: relative; overflow: hidden; }}
    .card::before {{ content: ''; position: absolute; inset: 0 0 auto; height: .32rem; background: var(--blue); }}
    .card.green::before {{ background: var(--green); }}
    .card.gold::before {{ background: var(--gold); }}
    .card.rose::before {{ background: var(--rose); }}
    .kicker {{ color: var(--teal); font-weight: 800; text-transform: uppercase; letter-spacing: .11em; font-size: .72rem; margin-top: .5rem; }}
    .card h3 {{ margin: .35rem 0 .55rem; font-size: 1.18rem; }}
    .card p {{ color: var(--muted); line-height: 1.5; }}
    .pills {{ display: flex; gap: .4rem; flex-wrap: wrap; margin-top: .9rem; }}
    .pill {{ display: inline-flex; border-radius: 999px; background: #eef6f1; color: #24513d; padding: .33rem .58rem; font-size: .76rem; font-weight: 700; max-width: 100%; overflow-wrap: anywhere; }}
    .wide {{ display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(280px, .9fr); gap: 1rem; align-items: stretch; }}
    .panel {{ background: var(--ink); color: white; border-radius: 1.5rem; padding: 1.25rem; box-shadow: var(--shadow); }}
    .panel p, .panel li {{ color: #dce6ea; line-height: 1.55; }}
    .panel code {{ color: #fff2c4; }}
    code {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .9rem; background: rgba(255,255,255,.14); border: 1px solid rgba(255,255,255,.22); border-radius: .55rem; padding: .22rem .38rem; }}
    .timeline {{ display: grid; gap: .75rem; margin-top: 1rem; }}
    .step {{ display: grid; grid-template-columns: 2.1rem 1fr; gap: .8rem; align-items: start; }}
    .step b {{ width: 2.1rem; height: 2.1rem; border-radius: 999px; background: var(--teal); color: white; display: grid; place-items: center; }}
    .safe {{ border: 1px solid #a7d8c2; background: #effaf4; border-radius: 1.25rem; padding: 1rem; }}
    .safe strong {{ color: var(--green); }}
    footer {{ border-top: 1px solid var(--line); padding: 2rem min(6vw, 5rem); color: var(--muted); }}
    @media (max-width: 780px) {{ .wide {{ grid-template-columns: 1fr; }} nav {{ align-items: flex-start; flex-direction: column; }} nav a {{ margin-left: 0; margin-right: .7rem; }} }}
  </style>
</head>
<body>
<nav>
  <div class="brand"><span class="mark" aria-hidden="true"></span><span>AI Washing Analytics Workstation</span></div>
  <div>
    <a href="#workflow">Workflow</a>
    <a href="#tables">Results</a>
    <a href="#evidence">Evidence</a>
    <a href="#roadmap">Roadmap</a>
  </div>
</nav>
<header>
  <div class="eyebrow">Public-review safe research overview</div>
  <h1>A reproducible evidence map for the AI Washing paper.</h1>
  <p class="hero-copy">This static overview shows how the AI Washing workstation connects paper results, construct validation, table navigation, extension lanes, and reproducibility checks. It is generated from repository manifests and contains no private research data values, local machine paths, access details, or browser command execution.</p>
  <div class="hero-actions">
    <a class="button primary" href="#tables">Review the paper results</a>
    <a class="button" href="../dashboard/index.html">Open the manifest dashboard</a>
    <a class="button" href="../../docs/dashboard_guide.md">Read the dashboard guide</a>
  </div>
  <div class="metrics">
    <div class="metric"><b>{table_count}</b><span>paper tables mapped</span></div>
    <div class="metric"><b>{figure_count}</b><span>figures tracked</span></div>
    <div class="metric"><b>{len(data_products)}</b><span>data products cataloged</span></div>
    <div class="metric"><b>{len(extensions)}</b><span>extension lanes registered</span></div>
    <div class="metric"><b>{metrics['csv_exact']}</b><span>exact CSV evidence rows</span></div>
  </div>
</header>
<main>
  <section id="workflow" class="wide">
    <div>
      <h2>Research workflow and evidence map.</h2>
      <p class="section-copy">The workstation gives reviewers a direct path from a paper result to the relevant data product, construct definition, script, validation status, and extension lane.</p>
      <div class="timeline">
        <div class="step"><b>1</b><div><strong>Paper question.</strong> Identify firms whose AI disclosure appears stronger than observable AI capability.</div></div>
        <div class="step"><b>2</b><div><strong>Data spine.</strong> Connect SEC disclosure text, classifier outputs, patent evidence, WRDS/market data, and annual/event panels.</div></div>
        <div class="step"><b>3</b><div><strong>Construct audit.</strong> Inspect classifier accuracy, acronym risk, patent matching, CRSP/Compustat boundaries, and source provenance.</div></div>
        <div class="step"><b>4</b><div><strong>Table workbench.</strong> Map each manuscript asset to scripts, frozen evidence, generated outputs, and safe modification notes.</div></div>
        <div class="step"><b>5</b><div><strong>Extension lab.</strong> Separate exploratory next tests from frozen v4.3 evidence.</div></div>
      </div>
    </div>
    <aside class="panel">
      <h3>What makes this public-review safe?</h3>
      <ul>
        <li>No private data values or row-level text are displayed.</li>
        <li>No local machine paths or private storage locations are embedded.</li>
        <li>No commands execute in the browser.</li>
        <li>The page can be opened as a static HTML file or hosted as a static site.</li>
      </ul>
      <p>For coauthor use, the full Streamlit workstation adds Table Explorer, Data Room, Extension Lab, and a controlled Command Center on a trusted local machine.</p>
    </aside>
  </section>

  <section id="tables">
    <h2>Results a reviewer can understand first.</h2>
    <p class="section-copy">The table layer is organized by paper labels, not internal filenames. Main Table 7 is the current table-review gate case: a reviewer can open the app, select the table by label, inspect readable artifacts, and download a compact review packet.</p>
    <div class="grid">{table_showcase(tables)}</div>
    <div class="safe"><strong>Status cue:</strong> {e(status_line)}. Frozen v4.3 evidence remains canonical; exploratory outputs stay separate until deliberately promoted.</div>
  </section>

  <section id="evidence">
    <h2>Data and construct evidence, summarized safely.</h2>
    <p class="section-copy">The overview answers core audit questions quickly: where the classifier evidence lives, how the patent match is supported, which market data lane ends in 2024, and which products can be modified safely for a future release.</p>
    <div class="grid">{data_showcase(data_products)}</div>
  </section>

  <section id="extensions">
    <h2>Future tests are tangible, but clearly labeled.</h2>
    <p class="section-copy">Extension lanes make follow-on work visible without blending exploratory outputs into manuscript evidence. The dashboard labels maturity, limitations, and future data needs directly.</p>
    <div class="grid">{extension_showcase(extensions)}</div>
  </section>

  <section id="roadmap" class="wide">
    <div>
    <h2>Future development options.</h2>
      <p class="section-copy">The current one-click layer is static and safe. The richer local Streamlit app supports technical drill-down, metadata-only data checks, extension inspection, and approved command execution. Future work can add hosted demo deployment, automated screenshot capture, and narrowly scoped AI assistants for documentation search or table triage.</p>
    </div>
    <aside class="panel">
      <h3>Suggested next commands</h3>
      <p>Generate this page locally:</p>
      <p><code>make public-demo</code></p>
      <p>Validate that it is safe to share:</p>
      <p><code>make public-demo-check</code></p>
      <p>Open the one-click demo:</p>
      <p><code>open outputs/public_demo/index.html</code></p>
    </aside>
  </section>
</main>
<footer>
  Generated from AI Washing workstation manifests. The Git repository and private data room remain authoritative for reproduction, data validation, and empirical extensions.
</footer>
</body>
</html>
"""


def validate_public_html(text: str) -> None:
    lower = text.lower()
    leaked = [pattern for pattern in FORBIDDEN_PATTERNS if pattern.lower() in lower]
    if leaked:
        raise PortfolioBuildError(f"Public demo contains forbidden pattern(s): {', '.join(leaked)}")


def build_portfolio_demo(output_path: Path = OUT_HTML) -> Path:
    tables = read_csv(MANIFESTS["tables"])
    data_products = read_csv(MANIFESTS["data_products"])
    extensions = read_csv(MANIFESTS["extensions"])
    status_rows = read_csv(REPRO_STATUS) if REPRO_STATUS.exists() else []
    text = html_document(tables, data_products, extensions, status_rows)
    validate_public_html(text)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    return output_path


def main() -> int:
    path = build_portfolio_demo()
    payload = {
        "public_demo": str(path.relative_to(ROOT)),
        "tables": len(read_csv(MANIFESTS["tables"])),
        "data_products": len(read_csv(MANIFESTS["data_products"])),
        "extensions": len(read_csv(MANIFESTS["extensions"])),
    }
    print("AI Washing public demo generated")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
