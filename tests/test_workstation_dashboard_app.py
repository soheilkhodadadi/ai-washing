from __future__ import annotations

from io import BytesIO
import subprocess
import sys
from pathlib import Path
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "apps" / "workstation_dashboard"
sys.path.insert(0, str(APP_DIR))

from services.command_runner import (  # noqa: E402
    CommandRegistryError,
    command_is_enabled,
    load_command_registry,
    run_dashboard_command,
    sanitize_log_text,
)
from services.manifest_store import dashboard_text_is_safe, load_dashboard_data, public_frame  # noqa: E402
from services.page_registry import PAGE_SPECS  # noqa: E402
from services.audit_data import (  # noqa: E402
    classifier_evidence_panel,
    compact_metrics,
    construct_evidence,
    data_product_cards,
    load_all_audit_reports,
    patent_evidence_panel,
    product_status_rows,
    product_validation_status,
    report_inventory,
    wrds_evidence_panel,
)
from services.extension_outputs import (  # noqa: E402
    HIDDEN_VALUE,
    check_seo_schema,
    extension_csv_preview,
    extension_json_preview,
    extension_markdown_preview,
    extension_output_bundle,
    safe_extension_output_dir,
    safe_schema_template,
    schema_template_fields,
    status_badges,
)
from services.table_artifacts import (  # noqa: E402
    REFERENCE_STATUS,
    build_review_packet,
    csv_preview,
    preferred_review_artifact,
    safe_repo_path,
    table_artifacts,
    table_display_label,
)
from services.technical_drilldown import (  # noqa: E402
    command_set,
    crosswalk_for_asset,
    data_product_path_statuses,
    linked_constructs,
    linked_data_products,
    linked_extensions,
    source_script_for_module,
)


def test_dashboard_page_specs_are_complete() -> None:
    expected = {
        "home",
        "paper_results",
        "table_explorer",
        "data_room",
        "construct_audits",
        "extension_lab",
        "reproduction_status",
        "command_center",
        "share_export",
        "portfolio_demo",
    }
    keys = {spec["key"] for spec in PAGE_SPECS}
    assert keys == expected
    required = {"group", "key", "title", "icon", "primary_user", "task", "inputs", "outputs", "safety_rule"}
    for spec in PAGE_SPECS:
        assert required <= set(spec)
        assert all(str(spec[field]).strip() for field in required)


def test_dashboard_manifests_load_from_canonical_contract() -> None:
    data = load_dashboard_data()
    assert len(data.tables) == 26
    assert len(data.data_products) >= 10
    assert len(data.extensions) >= 4
    assert {"asset_id", "paper_label", "script_module", "make_command"} <= set(data.tables.columns)
    assert {"product_id", "logical_private_path", "coverage"} <= set(data.data_products.columns)
    assert {"extension_id", "make_command", "interpretation_limits", "maturity_status", "manuscript_status"} <= set(
        data.extensions.columns
    )


def test_manifest_text_used_by_dashboard_is_public_safe() -> None:
    data = load_dashboard_data()
    text = "\n".join(
        [
            public_frame(data.tables).astype(str).to_csv(index=False),
            public_frame(data.data_products).astype(str).to_csv(index=False),
            public_frame(data.extensions).astype(str).to_csv(index=False),
        ]
    )
    assert dashboard_text_is_safe(text)


def test_dashboard_command_registry_is_allowlisted_and_fixed_make_only() -> None:
    commands = load_command_registry()
    ids = {command.command_id for command in commands}

    assert {"dashboard_check", "export_t30_bundle", "extension_washing_pays_proxy"} <= ids
    assert len(ids) == len(commands)
    for command in commands:
        assert command.argv[0] == "make"
        assert command.enabled_in_demo_mode is False
        assert command.display_command.startswith("make ")
        assert "\n" not in command.display_command
        assert ";" not in command.display_command


def test_dashboard_command_runner_rejects_unknown_or_unconfirmed_commands(tmp_path: Path) -> None:
    commands = load_command_registry()
    with pytest.raises(CommandRegistryError):
        run_dashboard_command("rm_rf", mode="Coauthor Mode", registry=commands, log_root=tmp_path)

    result = run_dashboard_command("export_t30_bundle", mode="Coauthor Mode", registry=commands, log_root=tmp_path)
    assert result.status == "blocked"
    assert "confirmation" in result.error_message.lower()
    assert result.log_path is None


def test_dashboard_command_runner_blocks_demo_and_missing_private_data(monkeypatch, tmp_path: Path) -> None:
    commands = load_command_registry()
    command = {item.command_id: item for item in commands}["check_private_data"]
    monkeypatch.delenv("AIW_DATA_ROOT", raising=False)

    enabled, reason = command_is_enabled(command, mode="Coauthor Mode", env={})
    assert not enabled
    assert "AIW_DATA_ROOT" in reason

    demo = run_dashboard_command("dashboard_check", mode="Demo Mode", registry=commands, log_root=tmp_path)
    missing_private = run_dashboard_command("check_private_data", mode="Coauthor Mode", confirmed=True, registry=commands, log_root=tmp_path)
    assert demo.status == "blocked"
    assert "Demo Mode" in demo.error_message
    assert missing_private.status == "blocked"
    assert "AIW_DATA_ROOT" in missing_private.error_message


def test_dashboard_command_runner_uses_subprocess_safely_and_writes_sanitized_logs(tmp_path: Path) -> None:
    commands = load_command_registry()
    captured: dict[str, object] = {}

    def fake_runner(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        captured["argv"] = argv
        captured["shell"] = kwargs["shell"]
        captured["cwd"] = kwargs["cwd"]
        captured["timeout"] = kwargs["timeout"]
        return subprocess.CompletedProcess(argv, 0, stdout=f"ok from {ROOT}\n", stderr="")

    result = run_dashboard_command(
        "dashboard_check",
        mode="Coauthor Mode",
        registry=commands,
        log_root=tmp_path,
        runner=fake_runner,
    )

    assert captured["argv"] == ["make", "dashboard-check"]
    assert captured["shell"] is False
    assert captured["cwd"] == ROOT
    assert captured["timeout"] == 120
    assert result.status == "passed"
    assert result.exit_code == 0
    assert result.log_path is not None and result.log_path.is_file()
    assert "$AIW_REPO_ROOT" in result.log_tail
    assert str(ROOT) not in result.log_tail


def test_dashboard_command_runner_reports_failures_and_timeouts(tmp_path: Path) -> None:
    commands = load_command_registry()

    def failing_runner(argv: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(argv, 2, stdout="", stderr=f"failed inside {ROOT}\n")

    failed = run_dashboard_command(
        "dashboard_check",
        mode="Coauthor Mode",
        registry=commands,
        log_root=tmp_path / "failed",
        runner=failing_runner,
    )
    assert failed.status == "failed"
    assert failed.exit_code == 2
    assert "$AIW_REPO_ROOT" in failed.log_tail
    assert str(ROOT) not in failed.log_tail

    def timeout_runner(argv: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired(argv, 1, output="", stderr=f"timeout at {ROOT}")

    timed_out = run_dashboard_command(
        "dashboard_check",
        mode="Coauthor Mode",
        registry=commands,
        log_root=tmp_path / "timeout",
        runner=timeout_runner,
    )
    assert timed_out.status == "timeout"
    assert timed_out.timed_out
    assert "$AIW_REPO_ROOT" in timed_out.log_tail


def test_dashboard_log_sanitizer_hides_private_and_home_paths(monkeypatch, tmp_path: Path) -> None:
    private_root = tmp_path / "ai-washing-private-data"
    private_root.mkdir()
    monkeypatch.setenv("AIW_DATA_ROOT", str(private_root))
    text = f"repo={ROOT}\nprivate={private_root}\nhome={Path.home()}\n"
    sanitized = sanitize_log_text(text)

    assert "$AIW_REPO_ROOT" in sanitized
    assert "$AIW_DATA_ROOT" in sanitized
    assert "$HOME" in sanitized
    assert str(ROOT) not in sanitized
    assert str(private_root) not in sanitized


def test_main_table_7_maps_to_t30_and_paper_label_display() -> None:
    data = load_dashboard_data()
    row = data.tables.loc[data.tables["paper_label"] == "Main Table 7"].iloc[0]
    assert row["asset_id"] == "T30"
    label = table_display_label(row)
    assert label.startswith("Main Table 7 - Capital-raising timing")
    assert "T30" not in label


def test_t30_artifact_resolution_finds_review_and_audit_formats() -> None:
    data = load_dashboard_data()
    row = data.tables.loc[data.tables["asset_id"] == "T30"].iloc[0]
    artifacts = table_artifacts(row)
    suffixes = {artifact.suffix for artifact in artifacts if artifact.exists}
    labels = "\n".join(artifact.label for artifact in artifacts)

    assert {".csv", ".tex", ".docx", ".pdf", ".png", ".md"} <= suffixes
    assert any(artifact.status == REFERENCE_STATUS for artifact in artifacts)
    assert "writer packet" in labels
    assert "result notes" in labels
    assert preferred_review_artifact(artifacts) is not None


def test_safe_repo_path_rejects_private_absolute_and_old_local_paths() -> None:
    assert safe_repo_path("data/curated/v4_3/generated_exports") is not None
    assert safe_repo_path("/Users/soheilkhodadadi/DataWork/ai-washing-private-data/panel.parquet") is None
    assert safe_repo_path("../../../outside.csv") is None
    assert safe_repo_path("DataWork/semantic-patterns/paper/generated/table.csv") is None
    assert safe_repo_path("$AIW_DATA_ROOT/panel.parquet") is None


def test_t30_csv_preview_is_capped_and_repo_contained() -> None:
    data = load_dashboard_data()
    row = data.tables.loc[data.tables["asset_id"] == "T30"].iloc[0]
    csv_artifact = next(artifact for artifact in table_artifacts(row) if artifact.previewable_csv)
    preview = csv_preview(csv_artifact, max_rows=3)
    assert len(preview) <= 3
    assert "Outcome" in preview.columns


def test_review_packet_contains_only_safe_artifacts() -> None:
    data = load_dashboard_data()
    row = data.tables.loc[data.tables["asset_id"] == "T30"].iloc[0]
    packet = build_review_packet(row, table_artifacts(row))
    with zipfile.ZipFile(BytesIO(packet)) as zf:
        names = zf.namelist()
        text = "\n".join(names)
        text += "\n" + zf.read("OPEN_FIRST.md").decode("utf-8")
    assert "OPEN_FIRST.md" in names
    assert "/Users/soheilkhodadadi" not in text
    assert "DataWork/semantic-patterns" not in text


def test_t30_technical_drilldown_resolves_script_data_construct_and_extension() -> None:
    data = load_dashboard_data()
    row = data.tables.loc[data.tables["asset_id"] == "T30"].iloc[0]
    crosswalk = crosswalk_for_asset("T30")
    script = source_script_for_module(row["script_module"])
    products = linked_data_products(row, data.data_products)
    constructs = linked_constructs(row)
    extensions = linked_extensions(row, data.extensions)

    assert crosswalk is not None
    assert crosswalk["test_id"] == "test_30_capital_raising_timing"
    assert script.exists
    assert script.rel_path.endswith("test_30_capital_raising_timing.py")
    assert "annual_nlp_patent_panel" in set(products["product_id"])
    assert "capital_raising" in {construct["id"] for construct in constructs}
    assert "washing_pays_proxy" in set(extensions["extension_id"])


def test_every_table_has_drilldown_commands() -> None:
    data = load_dashboard_data()
    for _, row in data.tables.iterrows():
        products = linked_data_products(row, data.data_products)
        extensions = linked_extensions(row, data.extensions)
        commands = command_set(row, products, extensions)
        labels = {item["label"] for item in commands}
        assert "Export table bundle" in labels
        assert "Rerun table" in labels
        assert "Show owning script" in labels
        assert all(item["command"].strip() for item in commands)


def test_data_product_status_reports_metadata_only(monkeypatch, tmp_path: Path) -> None:
    import duckdb

    private_root = tmp_path / "private"
    panel_path = private_root / "processed" / "panel" / "example.parquet"
    panel_path.parent.mkdir(parents=True)
    import pandas as pd

    pd.DataFrame({"cik": ["0001", "0002"], "secret_value": ["alpha", "beta"]}).to_parquet(panel_path)
    monkeypatch.setenv("AIW_DATA_ROOT", str(private_root))
    status = data_product_path_statuses({"logical_private_path": "data/processed/panel/example.parquet"})[0]
    payload = status.to_public_dict()

    assert duckdb.__version__
    assert status.status == "present"
    assert status.kind == "file"
    assert status.row_count == 2
    assert "secret_value" in status.columns
    assert "alpha" not in str(payload)
    assert "beta" not in str(payload)
    assert str(tmp_path) not in payload["display_path"]


def test_data_product_status_rejects_unsafe_paths(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("AIW_DATA_ROOT", str(tmp_path))
    statuses = data_product_path_statuses({"logical_private_path": "/tmp/private.csv; ../outside.csv"})
    assert [status.status for status in statuses] == ["not_resolved", "not_resolved"]
    assert all(status.kind == "reference" for status in statuses)


def test_audit_reports_load_and_degrade_to_public_inventory() -> None:
    reports = load_all_audit_reports()
    inventory = report_inventory(reports)
    assert {"data_sanity", "textual_construct", "patent_construct", "journal_reproducibility"} <= set(inventory["report"])
    assert {"report", "status", "path", "rows", "note"} <= set(inventory.columns)
    assert "/Users/soheilkhodadadi" not in inventory.astype(str).to_csv(index=False)


def test_data_product_cards_add_family_and_validation_status() -> None:
    data = load_dashboard_data()
    reports = load_all_audit_reports()
    cards = data_product_cards(data.data_products, reports)
    classifier = cards.loc[cards["product_id"] == "final_hybrid_classifier_outputs"].iloc[0]
    patent = cards.loc[cards["product_id"] == "patent_match_artifacts"].iloc[0]
    annual = cards.loc[cards["product_id"] == "annual_nlp_patent_panel"].iloc[0]

    assert classifier["family"] == "classifier"
    assert classifier["contract_status"] == "present"
    assert classifier["validation_status"] == "validated"
    assert patent["family"] == "patents"
    assert patent["validation_status"] in {"validated", "not_audited", "review_needed"}
    assert annual["validation_status"] == "validated"
    assert product_validation_status("missing_product", reports) == "not_audited"


def test_classifier_evidence_panel_resolves_counts_and_risks() -> None:
    data = load_dashboard_data()
    panel = classifier_evidence_panel(data.data_products, load_all_audit_reports())
    metrics = compact_metrics(panel.metrics)
    assert "final_hybrid_classifier_outputs" in panel.products
    assert "extracted_ai_sentences" in panel.products
    assert "classifier_validation_labels" in panel.products
    assert set(metrics["label"]) >= {"row_count", "year_coverage", "short_acronym_only_sentence_rate"}
    assert "147879" in set(metrics["value"])
    assert panel.status == "review_needed"


def test_patent_evidence_panel_resolves_audit_surface_without_examples() -> None:
    data = load_dashboard_data()
    panel = patent_evidence_panel(data.data_products, load_all_audit_reports())
    text = "\n".join([panel.summary, *panel.products, *panel.docs, compact_metrics(panel.metrics).astype(str).to_csv(index=False)])
    assert "patent_match_artifacts" in panel.products
    assert "patent_keyword_metadata" in panel.products
    assert "company_identity_patent_lookup" in panel.products
    assert "short_acronym_only_keyword_examples" in text
    assert "Compounded surface treated" not in text


def test_wrds_and_construct_evidence_map_to_expected_surfaces() -> None:
    data = load_dashboard_data()
    reports = load_all_audit_reports()
    wrds = wrds_evidence_panel(data.data_products, reports)
    patent_construct = construct_evidence("patent_mismatch", data.data_products, reports)
    disclosure_construct = construct_evidence("ai_disclosure", data.data_products, reports)

    assert "annual_nlp_patent_panel" in wrds.products
    assert "filing_event_estimation_sample" in wrds.products
    assert wrds.status == "validated"
    assert patent_construct.title == "Patent Match Evidence"
    assert disclosure_construct.title == "Classifier Evidence"


def test_extension_manifest_registers_future_seo_placeholder() -> None:
    data = load_dashboard_data()
    extension = data.extensions.loc[data.extensions["extension_id"] == "washing_pays_strong_seo"].iloc[0]

    assert extension["maturity_status"] == "future_data_required"
    assert extension["manuscript_status"] == "not_manuscript_ready"
    assert safe_schema_template(extension) is not None
    assert "Not manuscript-ready" in status_badges(extension)


def test_extension_output_bundle_discovers_generated_aggregate_files() -> None:
    data = load_dashboard_data()
    extension = data.extensions.loc[data.extensions["extension_id"] == "builder_hides"].iloc[0]
    bundle = extension_output_bundle(extension)
    names = {file.path.name for file in bundle.files}

    assert bundle.exists
    assert bundle.rel_output_dir == "outputs/extensions/builder_hides_right_tail"
    assert "builder_hides_summary.json" in names
    assert "builder_hides_interpretation.md" in names
    assert "builder_hides_descriptive.csv" in names


def test_extension_output_bundle_handles_missing_placeholder_outputs() -> None:
    data = load_dashboard_data()
    extension = data.extensions.loc[data.extensions["extension_id"] == "washing_pays_strong_seo"].iloc[0]
    bundle = extension_output_bundle(extension)

    assert not bundle.exists
    assert bundle.files == ()
    assert "not present" in bundle.note.lower()


def test_extension_output_path_safety_rejects_private_or_old_local_paths() -> None:
    assert safe_extension_output_dir({"output_dir": "outputs/extensions/example"}) is not None
    assert safe_extension_output_dir({"output_dir": "/Users/soheilkhodadadi/DataWork/ai-washing-private-data/x"}) is None
    assert safe_extension_output_dir({"output_dir": "DataWork/semantic-patterns/outputs/extensions/x"}) is None
    assert safe_extension_output_dir({"output_dir": "../outputs/extensions/x"}) is None


def test_extension_json_preview_hides_private_paths() -> None:
    data = load_dashboard_data()
    extension = data.extensions.loc[data.extensions["extension_id"] == "builder_hides"].iloc[0]
    bundle = extension_output_bundle(extension)
    summary = next(file for file in bundle.files if file.path.name == "builder_hides_summary.json")
    payload = extension_json_preview(summary)

    assert payload["annual_panel"] == HIDDEN_VALUE
    assert "/Users/soheilkhodadadi" not in str(payload)
    assert "ai-washing-private-data" not in str(payload)


def test_extension_csv_and_markdown_previews_are_safe_and_capped() -> None:
    data = load_dashboard_data()
    extension = data.extensions.loc[data.extensions["extension_id"] == "builder_hides"].iloc[0]
    bundle = extension_output_bundle(extension)
    csv_file = next(file for file in bundle.files if file.path.name == "builder_hides_descriptive.csv")
    md_file = next(file for file in bundle.files if file.path.name == "builder_hides_interpretation.md")

    preview = extension_csv_preview(csv_file, max_rows=2)
    markdown = extension_markdown_preview(md_file)

    assert len(preview) <= 2
    assert not preview.empty
    assert "Builder-Hides" in markdown
    assert "/Users/soheilkhodadadi" not in markdown


def test_seo_schema_checker_validates_headers_without_values() -> None:
    source = (
        "firm_id,issue_announcement_date,offering_type,completion_status,source_file\n"
        "secret_firm,2026-01-05,SEO,Completed,private_vendor.csv\n"
    ).encode()
    result = check_seo_schema(source)
    payload = result.summary_rows().astype(str).to_csv(index=False)

    assert result.is_valid
    assert result.row_count == 1
    assert result.missing_required == ()
    assert "secret_firm" not in payload
    assert "private_vendor.csv" not in payload


def test_seo_schema_checker_reports_missing_required_extra_and_parse_errors() -> None:
    missing = check_seo_schema(b"gvkey,extra_field\n001000,value\n")
    malformed = check_seo_schema(b"")
    fields = schema_template_fields()

    assert not missing.is_valid
    assert "issue_announcement_date" in missing.missing_required
    assert "extra_field" in missing.extra_columns
    assert malformed.status == "parse_error"
    assert "field_name" in fields.columns


def test_product_status_rows_are_metadata_only(monkeypatch, tmp_path: Path) -> None:
    private_root = tmp_path / "private"
    path = private_root / "processed" / "classifications" / "classified_sentences.parquet"
    path.parent.mkdir(parents=True)
    import pandas as pd

    pd.DataFrame({"sentence": ["private text"], "label": ["Actionable"]}).to_parquet(path)
    monkeypatch.setenv("AIW_DATA_ROOT", str(private_root))
    status = product_status_rows({"logical_private_path": "data/processed/classifications/classified_sentences.parquet"})
    payload = status.astype(str).to_csv(index=False)

    assert "present" in payload
    assert "sentence" in payload
    assert "private text" not in payload
    assert str(tmp_path) not in payload
