from __future__ import annotations

from dataclasses import dataclass

from services.manifest_store import DashboardData, dashboard_text_is_safe


@dataclass(frozen=True)
class CaseStudySection:
    title: str
    body: str
    bullets: tuple[str, ...]


WORKFLOW_STEPS: tuple[tuple[str, str], ...] = (
    ("Research question", "Measure when AI disclosure appears stronger than observable AI capability."),
    ("Data room", "Keep private research data outside Git while exposing schemas, lineage, and validation status."),
    ("Construct validation", "Audit classifier, patent, WRDS, and capital-raising constructs before extending tests."),
    ("Table workbench", "Map each manuscript result to the script, data products, artifacts, and safe rerun path."),
    ("Extension lab", "Separate exploratory follow-on tests from frozen v4.3 evidence."),
    (
        "Command center",
        "Run only approved local Make targets with confirmation, sanitized logs, and Demo Mode disabled.",
    ),
)

CASE_STUDY_SECTIONS: tuple[CaseStudySection, ...] = (
    CaseStudySection(
        "Problem",
        "Empirical research projects often become hard to review because code, data, tables, and validation notes "
        "drift into separate places.",
        (
            "Coauthors need fast access to tables, scripts, and data lineage.",
            "Supervisors need readable outputs without navigating source code first.",
            "External reviewers need a safe view of the research system without private research data.",
        ),
    ),
    CaseStudySection(
        "Workflow",
        "The dashboard adds a manifest-driven navigation layer on top of the validated Make/Docker workstation.",
        tuple(f"{label}: {description}" for label, description in WORKFLOW_STEPS),
    ),
    CaseStudySection(
        "Evidence",
        "The app surfaces nonprivate evidence about reproducibility, construct quality, and extension readiness.",
        (
            "Paper assets are organized by manuscript label and technical ID.",
            "Classifier, patent, and WRDS lanes are summarized through metadata and audit status, not row values.",
            "Extension outputs are labeled exploratory unless explicitly promoted.",
        ),
    ),
    CaseStudySection(
        "Reusable Methodology",
        "The same pattern can be reused for finance, NLP, and research-software handoffs that need a clean "
        "review interface.",
        (
            "Use manifests as the public contract between scripts, data, outputs, and documentation.",
            "Keep private data outside Git and preview only metadata in the app.",
            "Offer a polished review layer while preserving command-line reproducibility underneath.",
        ),
    ),
)

DEMO_SAFETY_POINTS: tuple[str, ...] = (
    "Private data roots and row-level values are hidden in Demo Mode.",
    "Command execution is disabled in Demo Mode.",
    "The page uses manifest metadata and static narrative content only.",
    "Screenshots should be captured from Demo Mode unless coauthors explicitly approve a private internal view.",
)


def portfolio_summary_metrics(data: DashboardData) -> dict[str, int]:
    return {
        "manuscript_assets": len(data.tables),
        "paper_tables": int((data.tables["asset_type"] == "table").sum()),
        "figures": int((data.tables["asset_type"] == "figure").sum()),
        "data_products": len(data.data_products),
        "extension_lanes": len(data.extensions),
    }


def portfolio_content_is_safe() -> bool:
    text = "\n".join(
        [
            *(section.title for section in CASE_STUDY_SECTIONS),
            *(section.body for section in CASE_STUDY_SECTIONS),
            *(bullet for section in CASE_STUDY_SECTIONS for bullet in section.bullets),
            *DEMO_SAFETY_POINTS,
            *(f"{label}: {description}" for label, description in WORKFLOW_STEPS),
        ]
    )
    return dashboard_text_is_safe(text)
