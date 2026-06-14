from __future__ import annotations

CONSTRUCTS = [
    {
        "id": "ai_disclosure",
        "title": "AI disclosure and classifier constructs",
        "doc": "docs/construct_playbooks/ai_disclosure_and_classifier_constructs.md",
        "summary": "Sentence extraction, classifier outputs, credibility classes, and validation surface.",
        "command": "make construct-info CONSTRUCT=ai_disclosure",
    },
    {
        "id": "patent_mismatch",
        "title": "PatentMismatch construct",
        "doc": "docs/construct_playbooks/patent_mismatch_construct.md",
        "summary": "Disclosure-patent gap, AI patent realization, and construct-validity checks.",
        "command": "make construct-info CONSTRUCT=patent_mismatch",
    },
    {
        "id": "patent_matching",
        "title": "Patent matching and company identity",
        "doc": "docs/construct_playbooks/patent_matching_and_company_identity.md",
        "summary": "Company-assignee identity matching, alias policy, and patent evidence review.",
        "command": "make construct-info CONSTRUCT=patent_matching",
    },
    {
        "id": "market_returns",
        "title": "CRSP/Compustat linkage and market tests",
        "doc": "docs/construct_playbooks/crsp_compustat_linkage_and_market_return_tests.md",
        "summary": "Market-return sample, Compustat/CRSP links, event windows, and return tests.",
        "command": "make construct-info CONSTRUCT=market_returns",
    },
    {
        "id": "capital_raising",
        "title": "Capital-raising proxy",
        "doc": "docs/construct_playbooks/capital_raising_proxy.md",
        "summary": "Current next-year share-growth proxy and stronger SEO/offering-terms path.",
        "command": "make construct-info CONSTRUCT=capital_raising",
    },
    {
        "id": "execucomp",
        "title": "ExecuComp incentives",
        "doc": "docs/construct_playbooks/execucomp_incentives.md",
        "summary": "CEO incentive extracts, staged cache policy, and refresh route.",
        "command": "make construct-info CONSTRUCT=execucomp",
    },
    {
        "id": "sec_scrutiny",
        "title": "SEC scrutiny and enforcement timing",
        "doc": "docs/construct_playbooks/sec_scrutiny_enforcement_timing.md",
        "summary": "SEC/comment-letter and enforcement timing evidence.",
        "command": "make construct-info CONSTRUCT=sec_scrutiny",
    },
]
