# Coauthor Share Note

Dear Thomas and Kuntara,

I have prepared a cleaned computational workstation for the AI Washing project so that the paper can be audited, extended, and rerun without relying on my older local `semantic-patterns` workspace. The package is split into two parts. The private GitHub repository contains the code, documentation, manifests, small fixtures, frozen v4.3 manuscript assets, and the scripts that reproduce the v4.3 tables. The OneDrive data room contains the private data mirror: cleaned annual and event panels, classifier outputs, extracted AI-sentence outputs, patent-match artifacts, WRDS/CRSP/Compustat extracts and bridges, selected SEC source samples, and validation reports.

The frozen computational reference is AI Washing v4.3. Kuntara's v5.0 manuscript edits are treated as editorial until we explicitly promote a later computational release. In the current v4.3 reproduction gate, all table CSV evidence is accounted for: 23 table assets reproduce exactly, one appendix table has only floating-point string representation differences at the final decimal places, and the two manuscript figures are preserved as frozen assets with regenerable candidate figure evidence. The event/market-return tables intentionally use the 2016-2024 event lane because the staged CRSP return extracts stop at 2024-12-31, while the annual NLP/patent lane extends through 2025.

For a first pass, please open `README_START_HERE.md`, then `docs/coauthor_runbook.md`. The fastest validation path is to clone the GitHub repo outside OneDrive, set `AIW_DATA_ROOT` to the local OneDrive-synced private data folder, and run the preflight and data-room checks. The runbook also explains the patent evidence pack, the SEC source policy, and the WRDS/CRSP/Compustat merge artifacts. The full raw SEC corpus is not bundled by default because v4.3 reproduction does not require it; instead, the data room includes representative full-submission samples, Notre Dame Stage-One samples, source links, extracted AI sentences, and final classifier outputs.

The capital-raising test in v4.3 is complete as a share-growth issue-window proxy: it defines a large equity-issuance window using next-year CRSP shares-outstanding growth above 5 percent. A stronger future “washing pays” test would require separate SEO/offering terms, such as proceeds, offer price, discount, valuation base, and offering type. Job postings are also left as a future extension, not a current reproduction dependency.

If anything fails during setup, the most useful diagnostic is the exact command output from `make doctor`, `make coauthor-preflight`, and `make check-private-data`. Those checks are designed to identify missing environment packages, path-contract mistakes, or incomplete OneDrive data syncing before table scripts are run.

Best,

Soheil
