PYTHON ?= python

.PHONY: validate compare-tables import-smoke path-leak-scan smoke-fixture reproduce-selected reproduce-table compare-selected-reproduction git-hygiene

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


git-hygiene:
	$(PYTHON) scripts/git_hygiene_check.py


compare-selected-reproduction:
	$(PYTHON) scripts/compare_selected_reproduction.py
