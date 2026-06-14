# Washing-Pays Extension: Proxy And Strong-Version Data Requirements

This note separates what the current AI Washing workstation can test from what requires new financing data.

## Research Question

The proposed washing-pays channel asks:

> Among firms raising capital, do low-substance AI talkers raise more capital, or raise it on better terms, than quieter but more substantive AI builders?

This is a powerful extension because it moves the paper from disclosure credibility to capital allocation. It also requires careful data discipline because the current v4.3 package does not contain full offering terms.

## What The Current Package Supports

The current package supports a proxy version through the v4.3 capital-raising timing test.

Existing proxy:

- next-year CRSP share growth above 5 percent
- constructed from `shrout`
- used as an issue-window proxy in Test 30

This can screen whether low-credibility AI talk is elevated around likely equity issuance windows. It does not measure offer terms.

Operational command:

```bash
export AIW_DATA_ROOT=/path/to/ai-washing-private-data
make extension-washing-pays-proxy
```

The command reruns the existing Test 30 logic and writes an ignored proxy bundle under `outputs/extensions/washing_pays_proxy/`.

Safe language:

> The current package can test whether low-substance AI disclosure clusters around a CRSP share-growth issue proxy. It cannot yet test whether AI washers receive better offer prices, lower discounts, or larger proceeds.

## What The Strong Version Requires

A strong washing-pays test needs an external SEO/offering-terms dataset under:

```text
$AIW_DATA_ROOT/external/seo_offering_terms/
```

Use `templates/seo_offering_terms_schema.csv` as the first schema checklist before staging or linking a new offering-level dataset.

Minimum fields:

| Field | Purpose |
|---|---|
| Firm identifier: CIK, GVKEY, PERMNO, or CUSIP | Link issuance events to the annual panel and filing windows. |
| Issue date or announcement date | Align financing to disclosure timing. |
| Proceeds or amount raised | Test whether washers raise more capital. |
| Offer price | Compute valuation and offer terms. |
| Pre-issue price or benchmark price | Compute offer discount. |
| Shares offered | Scale issuance size. |
| Market capitalization base | Normalize proceeds and issue size. |
| Offering type | Separate SEO, private placement, ATM, convertible, or mixed issuance. |
| Underwriter or placement details, if available | Optional quality/terms control. |

Preferred derived outcomes:

- proceeds scaled by lagged assets or market cap
- offer discount
- offer-size-to-market-cap
- announcement return
- post-issue return or operating outcome
- financing completion indicator

## Linkage Requirements

The current repo already stages CRSP/Compustat/linking files and validates them with:

```bash
make validate-wrds-data
```

A new issuance file should be added to the broad data-room manifest only after the source and schema are known. It should not be silently substituted for Test 30's share-growth proxy.

Recommended new manifest entry:

```text
artifact_id: equity_issuance_terms_v1
logical_path: data/external/seo_offering_terms/<source_name>_equity_issuance_terms_v1.parquet
role: required_extension
shareability: licensed_private_or_manual
status: present or deferred_with_reason
```

## Starter Analysis Design

Once issuance data are available, the clean extension sequence is:

1. Build an issuance-event panel linked to CIK/GVKEY/PERMNO.
2. Define pre-issuance disclosure windows, for example filing year t or filing within 12 months before issue date.
3. Compare low-credibility AI talkers, high-substance AI builders, and quiet real-AI firms.
4. Estimate issuance outcomes with industry/year controls and firm fundamentals.
5. Separate timing from terms: first ask who raises, then ask on what terms.

## Referee Lens

A strict referee will not accept the current share-growth proxy as evidence of better financing terms. It is useful for screening issuance timing, not pricing. The strong version needs actual SEO/offering terms before the paper can claim that AI washing pays in capital markets.
