# Extension Playbook

This playbook turns Kuntara's comments into coauthor-ready extension lanes. It is not a commitment that Soheil must run these tests before handoff; it is a map so Kuntara/Thomas can begin from the shared workstation.

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
- External issuance data under `data/external/equity_issuance` if a richer issuance database is used.
- CRSP/Compustat controls already staged and validated through `make validate-wrds-data`.

Current status:

- Proxy version is available from Test 30's next-year CRSP `shrout` growth rule.
- Strong version is not available until actual issuance terms are staged.
- See `docs/extensions/washing_pays_data_requirements.md` before writing any manuscript claim.

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

- First-pass starter script is available through `make builder-hides-first-pass`.
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
