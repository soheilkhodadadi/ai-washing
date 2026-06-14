# Extension Playbook

This playbook turns coauthor comments into extension lanes that can be run from the shared workstation. It separates first-pass screens from stronger tests that require new data.

For a terminal summary of each lane, use:

```bash
make extension-info EXTENSION=builder_hides
make extension-info EXTENSION=washing_pays_proxy
```

The machine-readable registry is `manifests/extension_workbench.csv`.

## E1: Washing Pays

Question: among firms raising equity, do low-substance AI talkers receive better financing outcomes than firms with quieter but more substantive AI activity?

Core sample:

- Firms with equity issuance or capital raising events.
- Compare high low-credibility AI disclosure, high speculative AI talk, and weak patent-backed AI claims against firms with stronger real AI evidence.

Candidate outcomes:

- Amount raised.
- Offer discount or offer-price valuation.
- Financing terms or issuance cost proxies.
- Post-issuance return or operating outcomes if available.

Data-room needs:

- Existing annual panel and filing-event panel.
- Capital-raising table inputs from v4.3.
- External issuance data under `data/external/seo_offering_terms` if a richer issuance database is used.
- CRSP/Compustat controls already staged and validated through `make validate-wrds-data`.

Current status:

- Proxy version is available from Test 30's next-year CRSP `shrout` growth rule.
- Strong version is not available until actual SEO/offering terms are staged.
- Operational proxy command: `make extension-washing-pays-proxy`.
- See `docs/extensions/washing_pays_data_requirements.md` before writing any manuscript claim.
- See `docs/extensions/washing_pays_proxy_first_pass.md` for the current proxy workflow and interpretation limits.

Decision rule:

- If washers receive better terms, the contribution moves toward market efficiency, capital allocation, and mispricing.
- If not, report the null cleanly and use it to bound the economic consequence of AI washing.

## E2: Builder Hides

Question: among firms with strong real AI innovation, is actionable AI disclosure lower rather than higher?

Core sample:

- Firms in the upper tail of AI patenting or AI application intensity.
- Compare actionable disclosure intensity and AI focus across patent bins or continuous patent intensity.

Candidate outcomes:

- Actionable AI share.
- AI focus.
- A/S ratio or low-credibility disclosure measures.
- Future AI patenting and applications.

Data-room needs:

- Annual panel with patent and application columns.
- Standalone patent match/crosswalk artifacts under the patent data room.
- Raw PatentsView source files only if a full bottom-up rebuild is needed.

Current status:

- First-pass starter script is available through `make extension-builder-hides`.
- AI-talking-sample robustness command: `make extension-builder-hides-ai-talk-only`.
- Outputs are written under ignored extension outputs, not promoted into v4.3 evidence.
- See `docs/extensions/builder_hides_first_pass.md` before interpreting signs.

Decision rule:

- If top builders disclose less actionable detail, the paper gains a strategic disclosure interpretation: real innovators may hide details while weaker firms talk more.
- If top builders disclose more, the result supports the existing validation logic and constrains the strategic-hiding channel.

## Git Workflow For Extensions

```bash
git switch -c extension/washing-pays
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make validate
make check-private-data
```

Commit code, docs, and small manifests only. Keep new datasets and generated outputs in `AIW_DATA_ROOT` or ignored `outputs/` folders.
