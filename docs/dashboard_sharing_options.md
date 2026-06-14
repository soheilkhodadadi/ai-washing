# Dashboard Sharing Options

This project has two browser interfaces:

- a generated static dashboard at `outputs/dashboard/index.html`;
- a generated static portfolio demo at `outputs/portfolio_demo/index.html`;
- an optional local Streamlit app started with `make dashboard-app` or `make docker-dashboard-app`.

The generated `outputs/` folders are intentionally ignored by Git. They are local build artifacts, like rendered tables or command logs. They are not visible on GitHub after a push unless the team deliberately publishes a sanitized static or hosted dashboard release.

## Why The Dashboard Is Not Visible On GitHub By Default

GitHub shows the tracked repository files. The files below are generated locally and ignored:

```text
outputs/dashboard/index.html
outputs/portfolio_demo/index.html
outputs/dashboard_runs/
outputs/workbench/
outputs/extensions/
```

This protects the repository from accidentally tracking generated files, command logs, or private-path metadata. Coauthors can regenerate the static pages locally:

```bash
make dashboard
make dashboard-check
open outputs/dashboard/index.html

make portfolio-demo
make portfolio-demo-check
open outputs/portfolio_demo/index.html
```

## Recommended Sharing Model Now

Use three coordinated channels:

1. Private GitHub repository: code, docs, manifests, dashboard source, Docker setup, and frozen v4.3 evidence.
2. Private Dropbox data room: private data mirror used as `AIW_DATA_ROOT`.
3. Optional local dashboard: coauthors generate the static dashboard or run the Streamlit app after cloning the repository.

Do not place this Git repository inside Dropbox. Keep `.git` local and use Dropbox only for the external private data root. Share the live Dropbox folder URL through a private message or email, not in the Git repository.

## Quick Nontechnical Preview

If a nontechnical viewer only needs to see the portfolio-safe presentation, generate the portfolio demo and copy the generated folder to a shared location:

```bash
make portfolio-demo
make portfolio-demo-check
```

Then share a copy of:

```text
outputs/portfolio_demo/index.html
```

This is the fastest way to provide a click-open demo through Dropbox or another private file-share folder. It is static, does not execute commands, and does not expose private data values.

## Hosted Static Site Option

For a cleaner one-click link, publish a sanitized static site. The safest v1 is a static release generated from:

```bash
make portfolio-demo
make dashboard
make portfolio-demo-check
make dashboard-check
```

Possible hosting targets:

- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages): static HTML/CSS/JavaScript from a repository. This is appropriate for a portfolio-safe dashboard or private-project static site if account permissions allow private Pages.
- [Vercel](https://vercel.com/docs/deployments): deploys from Git or CLI and provides preview/production URLs. This is useful for polished static demos or later web-app front ends.
- Internal university/project hosting: appropriate if access control or branding matters.

A hosted static site should not include the private data room, generated command logs, private row-level data, or private-data paths.

## Hosted Streamlit Option

The Streamlit app is richer than the static dashboard, but it requires a Python runtime. It can be shared through:

- local native run: `make dashboard-app`;
- local Docker run: `make docker-dashboard-app`;
- a future hosted deployment through [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app) or [Hugging Face Spaces with Streamlit](https://huggingface.co/docs/hub/en/spaces-sdks-streamlit).

A hosted Streamlit demo should be Demo Mode only unless there is a separate security review. Browser command execution, private-data mounts, and row-level private previews should remain disabled in a public or semi-public hosted app.

## Decision Rule

- Coauthor reproduction: GitHub repo plus Dropbox `AIW_DATA_ROOT`, run locally or through Docker.
- Thomas-style visual review: local Streamlit app or copied static portfolio demo.
- Public/portfolio link: sanitized static site first; hosted Streamlit Demo Mode only after a separate deployment review.
- Journal archive: do not include internal dashboard logs or private data; provide reproducible code, formal README, manifests, and restricted-data instructions.
