from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from services.manifest_store import load_manifest, split_tokens
from services.paths import ROOT, repo_relative
from services.technical_drilldown import data_product_path_statuses, split_private_paths

REPORT_DIR = ROOT / "reports" / "replication_audit"

REPORT_FILES = {
    "data_sanity": REPORT_DIR / "data_sanity_audit.csv",
    "textual_construct": REPORT_DIR / "textual_construct_audit.csv",
    "patent_construct": REPORT_DIR / "patent_construct_audit.csv",
    "journal_reproducibility": REPORT_DIR / "journal_reproducibility_audit.csv",
}

FAMILY_KEYWORDS = {
    "classifier": ("classifier", "sentence", "nlp", "label", "heldout"),
    "patents": ("patent", "pregrant", "application", "assignee", "keyword", "company_identity"),
    "wrds_market": ("wrds", "crsp", "compustat", "market", "event", "execucomp", "comment_letter"),
    "source_samples": ("sec_source", "source", "sample", "links"),
    "frozen_evidence": ("frozen", "generated", "evidence"),
}

PRODUCT_TO_DATA_SANITY_ARTIFACTS = {
    "annual_nlp_patent_panel": ("annual_panel", "classifier_outputs", "sec_sentence_outputs"),
    "filing_event_estimation_sample": ("event_panel",),
    "final_hybrid_classifier_outputs": ("classifier_outputs",),
    "extracted_ai_sentences": ("sec_sentence_outputs",),
    "patent_match_artifacts": ("grant_counts", "pregrant_counts"),
    "crsp_market_returns": ("crsp_monthly", "daily_event_returns"),
    "wrds_compustat_extracts": ("comp_funda_full_sample",),
    "execucomp_ceo_extract": ("execucomp_ceo",),
}


@dataclass(frozen=True)
class AuditLoadResult:
    name: str
    path: Path
    frame: pd.DataFrame
    status: str
    note: str


@dataclass(frozen=True)
class EvidencePanel:
    title: str
    status: str
    summary: str
    metrics: tuple[dict[str, str], ...]
    products: tuple[str, ...]
    commands: tuple[dict[str, str], ...]
    docs: tuple[str, ...]


def load_audit_report(name: str) -> AuditLoadResult:
    path = REPORT_FILES[name]
    if not path.is_file():
        return AuditLoadResult(name, path, pd.DataFrame(), "missing", f"Report not found: {repo_relative(path)}")
    try:
        return AuditLoadResult(name, path, pd.read_csv(path).fillna(""), "present", f"Loaded {repo_relative(path)}")
    except Exception as exc:  # pragma: no cover - defensive only
        return AuditLoadResult(name, path, pd.DataFrame(), "missing", f"Could not load {repo_relative(path)}: {exc}")


def load_all_audit_reports() -> dict[str, AuditLoadResult]:
    return {name: load_audit_report(name) for name in REPORT_FILES}


def product_family(row: pd.Series | dict[str, Any]) -> str:
    product_id = str(row.get("product_id", "") or "").lower()
    text = " ".join(str(row.get(key, "") or "").lower() for key in ["product_id", "purpose", "source_lineage", "extension_relevance"])
    for family, keywords in FAMILY_KEYWORDS.items():
        if any(keyword in product_id or keyword in text for keyword in keywords):
            return family
    return "panel_or_support"


def _coauthor_manifest_rows(row: pd.Series | dict[str, Any]) -> pd.DataFrame:
    try:
        manifest = load_manifest("coauthor_data_room_manifest.csv")
    except FileNotFoundError:
        return pd.DataFrame()
    paths = set(split_private_paths(row.get("logical_private_path", "")))
    if not paths:
        return manifest.head(0).copy()
    return manifest.loc[manifest["logical_path"].astype(str).isin(paths)].copy()


def product_contract_status(row: pd.Series | dict[str, Any]) -> str:
    manifest_rows = _coauthor_manifest_rows(row)
    if manifest_rows.empty:
        text = " ".join(str(row.get(key, "") or "").lower() for key in ["purpose", "extension_relevance", "overwrite_rule"])
        if "future" in text:
            return "future_extension"
        return "review_needed"
    statuses = set(manifest_rows["status"].astype(str).str.lower())
    roles = set(manifest_rows["role"].astype(str).str.lower())
    if "deferred_with_reason" in statuses:
        return "future_extension" if any("extension" in role for role in roles) else "deferred"
    if "present" in statuses:
        return "present"
    if "missing" in statuses:
        return "missing"
    return "review_needed"


def product_validation_rows(product_id: str, reports: dict[str, AuditLoadResult] | None = None) -> pd.DataFrame:
    reports = reports or load_all_audit_reports()
    artifact_ids = PRODUCT_TO_DATA_SANITY_ARTIFACTS.get(product_id, ())
    if not artifact_ids:
        return pd.DataFrame()
    data_sanity = reports["data_sanity"].frame
    if data_sanity.empty or "artifact_id" not in data_sanity.columns:
        return pd.DataFrame()
    return data_sanity.loc[data_sanity["artifact_id"].astype(str).isin(artifact_ids)].copy()


def product_validation_status(product_id: str, reports: dict[str, AuditLoadResult] | None = None) -> str:
    checks = product_validation_rows(product_id, reports)
    if checks.empty:
        return "not_audited"
    severities = set(checks["severity"].astype(str).str.lower())
    statuses = set(checks.get("status", pd.Series(dtype=str)).astype(str).str.lower())
    if "stop_the_line" in severities or "fail" in statuses:
        return "stop_the_line"
    if {"material_needs_review", "material_needs_future_layer", "manageable"} & severities or "review" in statuses:
        return "review_needed"
    return "validated"


def data_product_cards(data_products: pd.DataFrame, reports: dict[str, AuditLoadResult] | None = None) -> pd.DataFrame:
    if data_products.empty:
        return data_products.copy()
    reports = reports or load_all_audit_reports()
    cards = data_products.copy()
    cards["family"] = cards.apply(product_family, axis=1)
    cards["contract_status"] = cards.apply(product_contract_status, axis=1)
    cards["validation_status"] = cards["product_id"].apply(lambda product_id: product_validation_status(str(product_id), reports))
    return cards


def status_counts(frame: pd.DataFrame, column: str) -> dict[str, int]:
    if frame.empty or column not in frame.columns:
        return {}
    return {str(key): int(value) for key, value in frame[column].value_counts(dropna=False).items()}


def _metric_from_check(report: pd.DataFrame, check_name: str, *, artifact_id: str = "") -> dict[str, str]:
    if report.empty or "check_name" not in report.columns:
        return {"label": check_name, "value": "not available", "status": "missing", "note": ""}
    mask = report["check_name"].astype(str).str.lower() == check_name.lower()
    if artifact_id and "artifact_id" in report.columns:
        mask &= report["artifact_id"].astype(str).str.lower() == artifact_id.lower()
    match = report.loc[mask]
    if match.empty:
        return {"label": check_name, "value": "not available", "status": "missing", "note": ""}
    row = match.iloc[0]
    return {
        "label": str(row.get("check_name", check_name)),
        "value": str(row.get("observed", "")),
        "status": str(row.get("severity", row.get("status", "")) or ""),
        "note": str(row.get("notes", "") or ""),
    }


def _product_ids(data_products: pd.DataFrame, ids: list[str]) -> tuple[str, ...]:
    available = set(data_products["product_id"].astype(str)) if not data_products.empty and "product_id" in data_products.columns else set()
    return tuple(product_id for product_id in ids if product_id in available)


def classifier_evidence_panel(data_products: pd.DataFrame, reports: dict[str, AuditLoadResult] | None = None) -> EvidencePanel:
    reports = reports or load_all_audit_reports()
    textual = reports["textual_construct"].frame
    metrics = (
        _metric_from_check(textual, "row_count"),
        _metric_from_check(textual, "year_coverage"),
        _metric_from_check(textual, "label_inventory"),
        _metric_from_check(textual, "short_acronym_only_sentence_rate"),
        _metric_from_check(textual, "ml_unit_context_sentence_count"),
        _metric_from_check(textual, "heldout_validation_file"),
    )
    status = "review_needed" if any(metric["status"] in {"material_needs_future_layer", "manageable"} for metric in metrics) else "validated"
    return EvidencePanel(
        title="Classifier Evidence",
        status=status,
        summary="Final hybrid classifier outputs reconcile to the v4.3 sentence count and coverage; acronym ambiguity is quantified as a construct-validity review item.",
        metrics=metrics,
        products=_product_ids(data_products, ["final_hybrid_classifier_outputs", "extracted_ai_sentences", "classifier_validation_labels"]),
        commands=(
            {"label": "Locate classifier outputs", "command": "AIW_DATA_ROOT=/path/to/ai-washing-private-data make locate-data PRODUCT_ID=final_hybrid_classifier_outputs PREVIEW=1", "tags": "requires private data; metadata only"},
            {"label": "Run SEC source validation", "command": "make validate-sec-source", "tags": "read-only validation"},
            {"label": "Run textual construct audit", "command": "AIW_DATA_ROOT=/path/to/ai-washing-private-data make textual-construct-audit", "tags": "requires private data; writes audit reports"},
        ),
        docs=("docs/sec_extraction_classification_audit.md", "docs/construct_playbooks/ai_disclosure_and_classifier_constructs.md", "reports/replication_audit/textual_construct_summary.md"),
    )


def patent_evidence_panel(data_products: pd.DataFrame, reports: dict[str, AuditLoadResult] | None = None) -> EvidencePanel:
    reports = reports or load_all_audit_reports()
    patent = reports["patent_construct"].frame
    metrics = (
        _metric_from_check(patent, "example_rows", artifact_id="grant_examples"),
        _metric_from_check(patent, "short_acronym_only_keyword_examples", artifact_id="grant_examples"),
        _metric_from_check(patent, "ml_unit_context_examples", artifact_id="grant_examples"),
        _metric_from_check(patent, "example_rows", artifact_id="pregrant_examples"),
        _metric_from_check(patent, "short_acronym_only_keyword_examples", artifact_id="pregrant_examples"),
        _metric_from_check(patent, "ml_unit_context_examples", artifact_id="pregrant_examples"),
    )
    status = "review_needed" if any(metric["status"] == "material_needs_future_layer" for metric in metrics) else "validated"
    return EvidencePanel(
        title="Patent Match Evidence",
        status=status,
        summary="Patent grant/pregrant evidence, examples, diagnostics, identity metadata, and keyword lists are staged; short acronym hits are explicitly flagged for coauthor review.",
        metrics=metrics,
        products=_product_ids(data_products, ["patent_match_artifacts", "patent_keyword_metadata", "company_identity_patent_lookup"]),
        commands=(
            {"label": "Locate patent artifacts", "command": "AIW_DATA_ROOT=/path/to/ai-washing-private-data make locate-data PRODUCT_ID=patent_match_artifacts PREVIEW=1", "tags": "requires private data; metadata only"},
            {"label": "Validate patent data", "command": "AIW_DATA_ROOT=/path/to/ai-washing-private-data make validate-patent-data", "tags": "requires private data; read-only validation"},
            {"label": "Run patent construct audit", "command": "AIW_DATA_ROOT=/path/to/ai-washing-private-data make patent-construct-audit", "tags": "requires private data; writes audit reports"},
        ),
        docs=("docs/patent_matching_validation.md", "docs/patent_mismatch_method_note.md", "docs/construct_playbooks/patent_matching_and_company_identity.md", "reports/replication_audit/patent_construct_summary.md"),
    )


def wrds_evidence_panel(data_products: pd.DataFrame, reports: dict[str, AuditLoadResult] | None = None) -> EvidencePanel:
    reports = reports or load_all_audit_reports()
    sanity = reports["data_sanity"].frame
    journal = reports["journal_reproducibility"].frame
    metrics = (
        _metric_from_check(sanity, "row_count", artifact_id="annual_panel"),
        _metric_from_check(sanity, "year_coverage", artifact_id="annual_panel"),
        _metric_from_check(sanity, "row_count", artifact_id="event_panel"),
        _metric_from_check(sanity, "year_coverage", artifact_id="event_panel"),
        _metric_from_check(sanity, "date_max", artifact_id="crsp_monthly"),
        _metric_from_check(journal, "docs_mention_aiw_data_root"),
    )
    return EvidencePanel(
        title="WRDS / CRSP / Compustat Lane Checks",
        status="validated",
        summary="The annual NLP/patent lane covers 2016-2025 while the event/market-return lane intentionally stops at 2024 because staged CRSP inputs stop at 2024-12-31.",
        metrics=metrics,
        products=_product_ids(data_products, ["annual_nlp_patent_panel", "filing_event_estimation_sample", "wrds_compustat_extracts", "crsp_market_returns", "crsp_compustat_linkage", "execucomp_ceo_extract"]),
        commands=(
            {"label": "Run data sanity audit", "command": "AIW_DATA_ROOT=/path/to/ai-washing-private-data make data-sanity-audit", "tags": "requires private data; writes audit reports"},
            {"label": "Validate WRDS data", "command": "AIW_DATA_ROOT=/path/to/ai-washing-private-data make validate-wrds-data", "tags": "requires private data; read-only validation"},
        ),
        docs=("docs/wrds_crsp_compustat_method_note.md", "docs/wrds_source_inventory.md", "reports/replication_audit/data_sanity_summary.md"),
    )


def evidence_panels(data_products: pd.DataFrame, reports: dict[str, AuditLoadResult] | None = None) -> tuple[EvidencePanel, ...]:
    reports = reports or load_all_audit_reports()
    return (
        classifier_evidence_panel(data_products, reports),
        patent_evidence_panel(data_products, reports),
        wrds_evidence_panel(data_products, reports),
    )


def construct_evidence(construct_id: str, data_products: pd.DataFrame, reports: dict[str, AuditLoadResult] | None = None) -> EvidencePanel:
    reports = reports or load_all_audit_reports()
    if construct_id == "ai_disclosure":
        return classifier_evidence_panel(data_products, reports)
    if construct_id in {"patent_matching", "patent_mismatch"}:
        return patent_evidence_panel(data_products, reports)
    if construct_id in {"market_returns", "execucomp"}:
        return wrds_evidence_panel(data_products, reports)
    if construct_id == "capital_raising":
        panel = wrds_evidence_panel(data_products, reports)
        return EvidencePanel(
            title="Capital-Raising Proxy Audit Surface",
            status=panel.status,
            summary="The v4.3 proxy is based on next-year CRSP share-growth logic; SEO/offering-term data remain a future stronger extension.",
            metrics=panel.metrics,
            products=_product_ids(data_products, ["annual_nlp_patent_panel", "crsp_market_returns"]),
            commands=(
                {"label": "Open proxy extension", "command": "make extension-info EXTENSION=washing_pays_proxy", "tags": "read-only"},
                {"label": "Export Main Table 7 bundle", "command": "make export-table-workbench TABLE_ID=T30", "tags": "writes ignored outputs"},
            ),
            docs=("docs/construct_playbooks/capital_raising_proxy.md", "docs/extensions/washing_pays_proxy_first_pass.md"),
        )
    if construct_id == "sec_scrutiny":
        return EvidencePanel(
            title="SEC Scrutiny Evidence",
            status="documented",
            summary="SEC/comment-letter and enforcement timing artifacts are staged and documented as source-specific construct inputs.",
            metrics=(),
            products=_product_ids(data_products, ["comment_letter_and_enforcement_events", "filing_spine_ai_measures"]),
            commands=({"label": "Validate data room", "command": "AIW_DATA_ROOT=/path/to/ai-washing-private-data make validate-data-room", "tags": "requires private data; read-only validation"},),
            docs=("docs/construct_playbooks/sec_scrutiny_enforcement_timing.md",),
        )
    return EvidencePanel(
        title=f"{construct_id} Audit Surface",
        status="documented",
        summary="Construct guidance is available in the playbook; no dedicated dashboard evidence panel is registered yet.",
        metrics=(),
        products=(),
        commands=(),
        docs=(),
    )


def report_inventory(reports: dict[str, AuditLoadResult] | None = None) -> pd.DataFrame:
    reports = reports or load_all_audit_reports()
    return pd.DataFrame(
        [
            {
                "report": item.name,
                "status": item.status,
                "path": repo_relative(item.path),
                "rows": len(item.frame),
                "note": item.note,
            }
            for item in reports.values()
        ]
    )


def product_status_rows(row: pd.Series | dict[str, Any]) -> pd.DataFrame:
    statuses = data_product_path_statuses(row)
    return pd.DataFrame([status.to_public_dict() for status in statuses])


def compact_metrics(metrics: tuple[dict[str, str], ...]) -> pd.DataFrame:
    return pd.DataFrame(metrics)[["label", "value", "status", "note"]] if metrics else pd.DataFrame(columns=["label", "value", "status", "note"])
