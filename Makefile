PYTHON ?= python

.PHONY: validate compare-tables import-smoke path-leak-scan smoke-fixture reproduce-selected reproduce-table compare-selected-reproduction git-hygiene check-private-data audit-artifact-coverage reproduce-all-tables-dry-run reproduce-all-tables reproduction-status validate-data-room validate-patent-data patent-example-audit validate-wrds-data

validate:
	$(PYTHON) scripts/validate_capsule.py

compare-tables:
	$(PYTHON) scripts/compare_tables.py

import-smoke:
	PYTHONPATH=src $(PYTHON) scripts/import_smoke.py

path-leak-scan:
	$(PYTHON) scripts/path_leak_scan.py

smoke-fixture:
	PYTHONPATH=src $(PYTHON) -m semantic_ai_washing_min.fixture_pipeline --fixture-dir data/fixtures --output-dir outputs/fixture

reproduce-selected:
	PYTHONPATH=src $(PYTHON) scripts/run_publication_table.py T00 --dry-run
	PYTHONPATH=src $(PYTHON) scripts/run_publication_table.py T16 --dry-run
	PYTHONPATH=src $(PYTHON) scripts/run_publication_table.py T17 --dry-run
	PYTHONPATH=src $(PYTHON) scripts/run_publication_table.py T09 --dry-run
	PYTHONPATH=src $(PYTHON) scripts/run_publication_table.py T30 --dry-run

reproduce-table:
	PYTHONPATH=src $(PYTHON) scripts/run_publication_table.py $(TABLE_ID)

check-private-data:
	$(PYTHON) scripts/check_private_data.py

reproduce-all-tables-dry-run:
	PYTHONPATH=src $(PYTHON) scripts/reproduce_assets.py --batch all --dry-run --include-figures

reproduce-all-tables:
	PYTHONPATH=src $(PYTHON) scripts/reproduce_assets.py --batch all --include-figures

validate-data-room:
	$(PYTHON) scripts/validate_data_room.py

audit-artifact-coverage:
	$(PYTHON) scripts/audit_artifact_coverage.py

validate-patent-data:
	$(PYTHON) scripts/validate_patent_data.py

patent-example-audit:
	$(PYTHON) scripts/build_patent_audit_examples.py

validate-wrds-data:
	$(PYTHON) scripts/validate_wrds_data.py

reproduction-status:
	PYTHONPATH=src $(PYTHON) scripts/reproduce_assets.py --batch all --status-only --include-figures

git-hygiene:
	$(PYTHON) scripts/git_hygiene_check.py

compare-selected-reproduction:
	$(PYTHON) scripts/compare_selected_reproduction.py
