from __future__ import annotations

import csv
import html
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "dashboard"
OUT_HTML = OUT_DIR / "index.html"

MANIFESTS = {
    "tables": ROOT / "manifests" / "paper_table_workbench.csv",
    "data_products": ROOT / "manifests" / "data_product_catalog.csv",
    "extensions": ROOT / "manifests" / "extension_workbench.csv",
}

CONSTRUCTS = [
    {
        "id": "ai_disclosure",
        "title": "AI disclosure and classifier constructs",
        "doc": "docs/construct_playbooks/ai_disclosure_and_classifier_constructs.md",
        "summary": "Sentence extraction, classifier outputs, credibility classes, and validation surface.",
    },
    {
        "id": "patent_mismatch",
        "title": "PatentMismatch construct",
        "doc": "docs/construct_playbooks/patent_mismatch_construct.md",
        "summary": "Disclosure-patent gap, AI patent realization, and construct-validity checks.",
    },
    {
        "id": "patent_matching",
        "title": "Patent matching and company identity",
        "doc": "docs/construct_playbooks/patent_matching_and_company_identity.md",
        "summary": "Company-assignee identity matching, alias policy, and patent evidence review.",
    },
    {
        "id": "market_returns",
        "title": "CRSP/Compustat linkage and market tests",
        "doc": "docs/construct_playbooks/crsp_compustat_linkage_and_market_return_tests.md",
        "summary": "Market-return sample, Compustat/CRSP links, event windows, and return tests.",
    },
    {
        "id": "capital_raising",
        "title": "Capital-raising proxy",
        "doc": "docs/construct_playbooks/capital_raising_proxy.md",
        "summary": "Current next-year share-growth proxy and stronger SEO/offering-terms path.",
    },
    {
        "id": "execucomp",
        "title": "ExecuComp incentives",
        "doc": "docs/construct_playbooks/execucomp_incentives.md",
        "summary": "CEO incentive extracts, staged cache policy, and refresh route.",
    },
    {
        "id": "sec_scrutiny",
        "title": "SEC scrutiny and enforcement timing",
        "doc": "docs/construct_playbooks/sec_scrutiny_enforcement_timing.md",
        "summary": "SEC/comment-letter and enforcement timing evidence.",
    },
]

FORBIDDEN_PATTERNS = [
    "/Users/soheilkhodadadi",
    "DataWork/semantic-patterns",
    "Documents/Projects/semantic-patterns",
    "password",
    "credential",
    "secret",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def public_text(value: object) -> str:
    text = str(value or "")
    replacements = {
        "credential-based": "access-based",
        "Credential-based": "Access-based",
        "credentials": "access details",
        "Credentials": "Access details",
        "credential": "access detail",
        "Credential": "Access detail",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def e(value: object) -> str:
    return html.escape(public_text(value), quote=True)


def repo_link(path: str) -> str:
    path = path.strip()
    if not path:
        return ""
    return "../../" + path


def docs_link(path: str) -> str:
    return repo_link(path)


def command_button(command: str) -> str:
    if not command:
        return ""
    return f'<button class="copy" data-copy="{e(command)}">Copy</button><code>{e(command)}</code>'


def card(title: str, subtitle: str, body: str, meta: Iterable[str], *, tags: Iterable[str], links: Iterable[tuple[str, str]], command: str = "") -> str:
    meta_html = "".join(f'<span class="badge">{e(item)}</span>' for item in meta if item)
    link_html = "".join(f'<a href="{e(href)}">{e(label)}</a>' for label, href in links if href)
    tags_text = " ".join(public_text(item) for item in tags)
    search_text = public_text(" ".join([title, subtitle, body, tags_text, command]))
    return f"""
<article class="card" data-tags="{e(tags_text)}" data-search="{e(search_text).lower()}">
  <div class="card-top">
    <h3>{e(title)}</h3>
    <span>{e(subtitle)}</span>
  </div>
  <p>{e(body)}</p>
  <div class="badges">{meta_html}</div>
  <div class="links">{link_html}</div>
  <div class="command">{command_button(command)}</div>
</article>
"""


def table_cards(rows: list[dict[str, str]]) -> str:
    cards: list[str] = []
    for row in rows:
        asset_id = row["asset_id"]
        tags = ["asset", row["asset_type"], row["paper_section"].replace(" ", "_").lower(), asset_id.lower()]
        links = [
            ("Open table bundle", f"../workbench/{asset_id}/OPEN_FIRST.md"),
            ("Workbench guide", "../../docs/paper_table_workbench.md"),
        ]
        command = f"make export-table-workbench TABLE_ID={asset_id}"
        cards.append(
            card(
                f"{row['paper_label']} ({asset_id})",
                row["asset_type"].title(),
                row["empirical_question"],
                [row["paper_section"], row["primary_data_product"], row["script_module"]],
                tags=tags,
                links=links,
                command=command,
            )
        )
    return "\n".join(cards)


def data_product_cards(rows: list[dict[str, str]]) -> str:
    cards: list[str] = []
    for row in rows:
        product_id = row["product_id"]
        command = f"make locate-data PRODUCT_ID={product_id} PREVIEW=1"
        cards.append(
            card(
                product_id,
                row["coverage"],
                row["purpose"],
                [row["keys"], row["overwrite_rule"], row["extension_relevance"]],
                tags=["data", product_id, row["coverage"]],
                links=[("Data catalog", "../../docs/panel_and_data_catalog.md")],
                command=command,
            )
        )
    return "\n".join(cards)


def extension_cards(rows: list[dict[str, str]]) -> str:
    cards: list[str] = []
    for row in rows:
        extension_id = row["extension_id"]
        cards.append(
            card(
                row["title"],
                extension_id,
                row["research_question"],
                [row["current_status"], row["interpretation_limits"], row["strong_version_data_needed"]],
                tags=["extension", extension_id, row["current_status"]],
                links=[("Extension doc", docs_link(row["docs"])), ("Registry", "../../manifests/extension_workbench.csv")],
                command=row["make_command"],
            )
        )
    return "\n".join(cards)


def construct_cards() -> str:
    cards: list[str] = []
    for item in CONSTRUCTS:
        cards.append(
            card(
                item["title"],
                item["id"],
                item["summary"],
                ["Construct playbook", "Safe modification path"],
                tags=["construct", item["id"]],
                links=[("Open playbook", docs_link(item["doc"]))],
                command=f"make construct-info CONSTRUCT={item['id']}",
            )
        )
    return "\n".join(cards)


def html_document(tables: list[dict[str, str]], data_products: list[dict[str, str]], extensions: list[dict[str, str]]) -> str:
    table_count = len(tables)
    data_count = len(data_products)
    extension_count = len(extensions)
    figure_count = sum(1 for row in tables if row["asset_type"] == "figure")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI Washing Workstation Dashboard</title>
  <style>
    :root {{
      --ink: #10202b;
      --muted: #5b6b74;
      --paper: #fbf8ef;
      --panel: #ffffff;
      --line: #d9ded5;
      --blue: #075985;
      --green: #2f6f4e;
      --gold: #b7791f;
      --rose: #9f1239;
      --shadow: 0 18px 45px rgba(16, 32, 43, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: ui-serif, Georgia, 'Times New Roman', serif; color: var(--ink); background: radial-gradient(circle at top left, #e0f2fe 0, rgba(224,242,254,0) 28rem), radial-gradient(circle at 80% 10%, #fef3c7 0, rgba(254,243,199,0) 22rem), var(--paper); }}
    header {{ padding: 3rem min(6vw, 5rem) 2rem; }}
    .eyebrow {{ text-transform: uppercase; letter-spacing: .15em; font-size: .75rem; font-weight: 700; color: var(--green); }}
    h1 {{ margin: .4rem 0; font-size: clamp(2.2rem, 6vw, 5.2rem); line-height: .95; max-width: 1050px; }}
    header p {{ max-width: 850px; color: var(--muted); font-size: 1.15rem; line-height: 1.6; }}
    .hero-actions {{ display: flex; gap: .75rem; flex-wrap: wrap; margin-top: 1.5rem; }}
    .hero-actions a {{ color: white; background: var(--ink); text-decoration: none; padding: .78rem 1rem; border-radius: 999px; box-shadow: var(--shadow); }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 1rem; margin-top: 2rem; max-width: 920px; }}
    .metric {{ background: rgba(255,255,255,.72); border: 1px solid var(--line); border-radius: 1.2rem; padding: 1rem; backdrop-filter: blur(8px); }}
    .metric b {{ display: block; font-size: 2rem; }}
    main {{ padding: 0 min(6vw, 5rem) 4rem; }}
    .toolbar {{ position: sticky; top: 0; z-index: 5; padding: 1rem 0; background: linear-gradient(to bottom, var(--paper), rgba(251,248,239,.85)); backdrop-filter: blur(8px); display: flex; gap: .75rem; align-items: center; flex-wrap: wrap; }}
    input[type="search"] {{ flex: 1 1 280px; padding: .95rem 1rem; border: 1px solid var(--line); border-radius: 1rem; font: inherit; }}
    .filter {{ border: 1px solid var(--line); background: white; border-radius: 999px; padding: .7rem .9rem; cursor: pointer; }}
    .filter.active {{ background: var(--ink); color: white; }}
    section {{ margin-top: 2.5rem; }}
    section > h2 {{ font-size: clamp(1.7rem, 3vw, 2.8rem); margin-bottom: .4rem; }}
    section > p {{ color: var(--muted); max-width: 900px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-top: 1rem; }}
    .card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 1.2rem; padding: 1rem; box-shadow: 0 8px 30px rgba(16,32,43,.07); display: flex; flex-direction: column; min-height: 260px; }}
    .card-top {{ display: flex; justify-content: space-between; gap: .75rem; align-items: start; }}
    .card h3 {{ margin: 0; font-size: 1.15rem; }}
    .card-top span {{ color: var(--green); font-weight: 700; white-space: nowrap; }}
    .card p {{ color: var(--muted); line-height: 1.45; }}
    .badges {{ display: flex; flex-wrap: wrap; gap: .35rem; margin-top: auto; }}
    .badge {{ background: #eef6f1; color: #24513d; border-radius: 999px; padding: .28rem .55rem; font-size: .78rem; }}
    .links {{ display: flex; flex-wrap: wrap; gap: .6rem; margin: .9rem 0; }}
    .links a {{ color: var(--blue); font-weight: 700; text-decoration: none; }}
    .command {{ display: flex; gap: .45rem; align-items: center; flex-wrap: wrap; }}
    code {{ background: #f3f5f2; border: 1px solid var(--line); border-radius: .55rem; padding: .35rem .45rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .82rem; overflow-wrap: anywhere; }}
    button.copy {{ border: 0; background: var(--blue); color: white; border-radius: .55rem; padding: .45rem .65rem; cursor: pointer; }}
    .start-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; }}
    .start-card {{ background: var(--ink); color: white; border-radius: 1.2rem; padding: 1rem; box-shadow: var(--shadow); }}
    .start-card p {{ color: #dce6ea; }}
    .hidden {{ display: none !important; }}
    footer {{ padding: 2rem min(6vw, 5rem); color: var(--muted); border-top: 1px solid var(--line); }}
  </style>
</head>
<body>
<header>
  <div class="eyebrow">AI Washing Research Workstation</div>
  <h1>Paper-first navigation for tables, data products, constructs, and extensions.</h1>
  <p>This static dashboard is generated from repository manifests. It exposes no private data values and runs no commands in the browser. Use it to find the relevant table, data product, construct playbook, extension lane, and copy-ready terminal command.</p>
  <div class="hero-actions">
    <a href="../../README_START_HERE.md">Start here</a>
    <a href="../../docs/paper_table_workbench.md">Paper table workbench</a>
    <a href="../../docs/panel_and_data_catalog.md">Data catalog</a>
    <a href="../../docs/extensions/README.md">Extensions</a>
  </div>
  <div class="metrics">
    <div class="metric"><b>{table_count}</b><span>paper assets</span></div>
    <div class="metric"><b>{figure_count}</b><span>frozen/candidate figures</span></div>
    <div class="metric"><b>{data_count}</b><span>data products</span></div>
    <div class="metric"><b>{extension_count}</b><span>extension lanes</span></div>
  </div>
</header>
<main>
  <div class="toolbar">
    <input id="search" type="search" placeholder="Search tables, data products, constructs, extensions, scripts, or commands..." />
    <button class="filter active" data-filter="all">All</button>
    <button class="filter" data-filter="asset">Tables & figures</button>
    <button class="filter" data-filter="data">Data products</button>
    <button class="filter" data-filter="construct">Constructs</button>
    <button class="filter" data-filter="extension">Extensions</button>
  </div>

  <section id="start">
    <h2>Start Here</h2>
    <p>The dashboard is a navigation layer. The validated execution path remains Make/Docker plus the private data root.</p>
    <div class="start-grid">
      <div class="start-card"><h3>1. Export one table</h3><p>Creates an ignored bundle with open-first guidance and reference evidence.</p>{command_button('make export-table-workbench TABLE_ID=T30')}</div>
      <div class="start-card"><h3>2. Locate one data product</h3><p>Checks the mounted private data root and prints safe schema/row-count previews.</p>{command_button('AIW_DATA_ROOT=/path/to/ai-washing-private-data make locate-data PRODUCT_ID=final_hybrid_classifier_outputs PREVIEW=1')}</div>
      <div class="start-card"><h3>3. Run one extension</h3><p>Runs a first-pass extension without replacing frozen v4.3 evidence.</p>{command_button('AIW_DATA_ROOT=/path/to/ai-washing-private-data make extension-builder-hides')}</div>
    </div>
  </section>

  <section id="tables">
    <h2>Tables & Figures</h2>
    <p>Each card maps a paper asset to its empirical question, owning script, primary data product, and export command.</p>
    <div class="grid">{table_cards(tables)}</div>
  </section>

  <section id="data-products">
    <h2>Data Products</h2>
    <p>These are logical data-room products. The dashboard shows paths and checks only, not private data contents.</p>
    <div class="grid">{data_product_cards(data_products)}</div>
  </section>

  <section id="constructs">
    <h2>Construct Playbooks</h2>
    <p>Use these guides when modifying variables, refreshing data, or responding to coauthor/referee questions.</p>
    <div class="grid">{construct_cards()}</div>
  </section>

  <section id="extensions">
    <h2>Extension Lanes</h2>
    <p>Registered extension starters are operational but do not overwrite v4.3 evidence.</p>
    <div class="grid">{extension_cards(extensions)}</div>
  </section>

  <section id="share-readiness">
    <h2>Share Readiness</h2>
    <p>Run these before sending the workstation or opening a review session.</p>
    <div class="start-grid">
      <div class="start-card"><h3>Static dashboard</h3>{command_button('make dashboard && make dashboard-check')}</div>
      <div class="start-card"><h3>Code-only preflight</h3>{command_button('make coauthor-preflight')}</div>
      <div class="start-card"><h3>Replication audit</h3>{command_button('AIW_DATA_ROOT=/path/to/ai-washing-private-data make replication-audit')}</div>
    </div>
  </section>
</main>
<footer>
  Generated from manifest files. Private data remain outside Git and outside this dashboard.
</footer>
<script>
const search = document.getElementById('search');
const filters = [...document.querySelectorAll('.filter')];
const cards = [...document.querySelectorAll('.card')];
let active = 'all';
function applyFilters() {{
  const query = search.value.trim().toLowerCase();
  for (const card of cards) {{
    const tags = card.dataset.tags || '';
    const text = card.dataset.search || '';
    const okFilter = active === 'all' || tags.includes(active);
    const okSearch = !query || text.includes(query);
    card.classList.toggle('hidden', !(okFilter && okSearch));
  }}
}}
search.addEventListener('input', applyFilters);
for (const btn of filters) {{
  btn.addEventListener('click', () => {{
    filters.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    active = btn.dataset.filter;
    applyFilters();
  }});
}}
for (const btn of document.querySelectorAll('button.copy')) {{
  btn.addEventListener('click', async () => {{
    await navigator.clipboard.writeText(btn.dataset.copy);
    const old = btn.textContent;
    btn.textContent = 'Copied';
    setTimeout(() => btn.textContent = old, 900);
  }});
}}
</script>
</body>
</html>
"""


def build_dashboard(output_path: Path = OUT_HTML) -> Path:
    tables = read_csv(MANIFESTS["tables"])
    data_products = read_csv(MANIFESTS["data_products"])
    extensions = read_csv(MANIFESTS["extensions"])
    text = html_document(tables, data_products, extensions)
    lower = text.lower()
    leaked = [pattern for pattern in FORBIDDEN_PATTERNS if pattern.lower() in lower]
    if leaked:
        raise RuntimeError(f"Dashboard contains forbidden pattern(s): {', '.join(leaked)}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    return output_path


def main() -> int:
    path = build_dashboard()
    payload = {
        "dashboard": str(path.relative_to(ROOT)),
        "tables": len(read_csv(MANIFESTS["tables"])),
        "data_products": len(read_csv(MANIFESTS["data_products"])),
        "extensions": len(read_csv(MANIFESTS["extensions"])),
    }
    print("AI Washing dashboard generated")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
