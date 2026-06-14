# Public Demo Deployment

The public demo is a static, non-executing research presentation layer for the AI Washing workstation. It is meant for public or semi-public review when the viewer should understand the project, dashboard, and reproducibility design without seeing private research data or installing Python, Docker, or Streamlit.

## What It Shows

- The AI Washing research workflow from question to data room, construct audit, table workbench, and extension lab.
- Nonprivate manifest-derived counts for paper assets, data products, and extension lanes.
- A Main Table 7 spotlight and other representative manuscript assets.
- The evidence spine for classifier outputs, patent matching, annual/event panels, and market-data boundaries.
- A clear path for hosted research review, screenshot capture, and carefully scoped documentation assistants.

## What It Does Not Show

- Private row-level data, sentence text, patent titles or abstracts, WRDS extracts, or local file paths.
- Private data-room mount instructions.
- Browser command execution.
- Any replacement for the frozen v4.3 empirical evidence.

## Local One-Click Demo

Generate and validate the static page:

```bash
make public-demo
make public-demo-check
```

Open it locally:

```bash
open outputs/public_demo/index.html
```

The output folder is ignored by Git, so it will not appear on GitHub after a push. Regenerate it whenever manifests or dashboard narratives change.

## Static Hosting Options

The generated `outputs/public_demo/index.html` can be copied to Dropbox for a quick private preview or later hosted as a static page through GitHub Pages, Vercel, Netlify, or an internal university/project site. Before hosting, run:

```bash
make public-demo
make public-demo-check
make dashboard-check
make package-surface-audit
```

Do not host the private coauthor data room or generated command logs. If the static manifest dashboard is also hosted, generate it with `make dashboard` and review `outputs/dashboard/index.html` separately.

## Relationship To Streamlit

The public demo is the simplest one-click public surface. The Streamlit app remains the richer local workstation for trusted coauthors: Table Explorer, Data Room, Construct Audits, Extension Lab, and Command Center. Streamlit should be shared through a local run, Docker, or a future controlled deployment only when the private-data and command-execution boundaries are explicit.

## Future Hosted Review Path

1. Add automated browser screenshots for the public demo and Streamlit Demo Mode.
2. Create a hosted static site profile with a polished landing page and dashboard links.
3. Add an optional hosted Streamlit Public Demo Mode with command execution disabled.
4. Add narrow documentation assistants only for nonprivate documentation search, manifest explanation, or table triage after a separate safety review.
