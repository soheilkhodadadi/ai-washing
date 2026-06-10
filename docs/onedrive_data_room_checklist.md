# OneDrive Data Room Checklist

Use this checklist before sharing the private AI Washing data room. The Git repository and the private data room are intentionally separate.

## Sharing Model

- Share the GitHub repository privately: `https://github.com/soheilkhodadadi/ai-washing`.
- Share the private data room through OneDrive with read/edit access for the coauthor team.
- Do not place the Git clone itself inside OneDrive. Coauthors should clone the repo into a normal local folder and set `AIW_DATA_ROOT` to their local OneDrive-synced data mirror.
- Do not share WRDS credentials. The data room contains staged extracts needed for reproduction and audit; refreshes are explicit and local-only.

## Expected Local Path Shape

The coauthor's local private data mirror should behave like this:

```text
/path/to/ai-washing-private-data/
  curated/v4_3/factor_inputs/
  external/execucomp/
  interim/accounting/
  interim/linking/
  interim/market/
  labels/
  processed/classifications/
  processed/panel/
  processed/patents/
  raw/sec_filings/samples/
  raw/sec_stage_one/samples_2025/
  reports/
  source_links/
  validation/
```

The exact logical paths are validated by:

```bash
AIW_DATA_ROOT=/path/to/ai-washing-private-data make check-private-data
AIW_DATA_ROOT=/path/to/ai-washing-private-data make validate-data-room
AIW_DATA_ROOT=/path/to/ai-washing-private-data make validate-sec-source
AIW_DATA_ROOT=/path/to/ai-washing-private-data make validate-wrds-data
AIW_DATA_ROOT=/path/to/ai-washing-private-data make validate-patent-data
AIW_DATA_ROOT=/path/to/ai-washing-private-data make audit-artifact-coverage
```

## Pre-Share Checklist For Soheil

- Confirm the Git branch is clean and pushed to the private GitHub repo.
- Confirm OneDrive has finished syncing the private data root before sending the link.
- Confirm the OneDrive link allows the intended coauthors to read and edit.
- Confirm no `.git`, `.venv`, local caches, or generated `outputs/` folders are inside the shared data room.
- Confirm `README_PRIVATE_DATA_ROOT.md` is present at the private data root.
- Confirm the two expected future-extension gaps remain documented rather than hidden: `seo_offering_terms` and `job_postings`.
- Run the local pre-share gate:

```bash
cd /Users/soheilkhodadadi/DataWork/ai-washing
make doctor
make coauthor-preflight
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make check-private-data validate-data-room validate-sec-source validate-wrds-data validate-patent-data audit-artifact-coverage
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make reproduce-all-tables
AIW_DATA_ROOT=/Users/soheilkhodadadi/DataWork/ai-washing-private-data make reproduce-figures
make reproduction-status
make figure-reproduction-status
```

## Coauthor First-Day Commands

After cloning the GitHub repo and syncing OneDrive, coauthors should run:

```bash
cd ai-washing
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
export AIW_REPO_ROOT="$PWD"
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
export AIW_OUTPUT_ROOT="$PWD/outputs/reproduced"
export AIW_PAPER_ROOT="$PWD/outputs/paper_exports"
make doctor
make coauthor-preflight
make check-private-data
make validate-data-room
make reproduce-all-tables
make reproduction-status
```

If using Docker, mount the private data room read-only first. The Phase 4G rehearsal already confirmed that read-only private-data reproduction works.
