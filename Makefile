PYTHON ?= python
PATENT_AUDIT_ARGS :=
ifneq ($(strip $(PATENT_AUDIT_OUTPUT)),)
PATENT_AUDIT_ARGS += --output $(PATENT_AUDIT_OUTPUT)
endif

DOCKER_IMAGE ?= ai-washing:local
DOCKER_WORKDIR := /workspaces/ai-washing
DOCKER_DATA_DIR := /workspaces/ai-washing-private-data
DOCKER_USER := $(shell id -u):$(shell id -g)
DOCKER_COMMON_ARGS := --rm --user $(DOCKER_USER) -e HOME=/tmp -e MPLCONFIGDIR=/tmp/aiw-matplotlib -e XDG_CACHE_HOME=/tmp/aiw-cache -e AIW_REPO_ROOT=$(DOCKER_WORKDIR) -e AIW_OUTPUT_ROOT=$(DOCKER_WORKDIR)/outputs/reproduced -e AIW_PAPER_ROOT=$(DOCKER_WORKDIR)/outputs/paper_exports -e PYTHONPATH=$(DOCKER_WORKDIR)/src -v "$(CURDIR)":$(DOCKER_WORKDIR) -w $(DOCKER_WORKDIR)
ifneq ($(strip $(AIW_DATA_ROOT)),)
DOCKER_DATA_ARGS := -e AIW_DATA_ROOT=$(DOCKER_DATA_DIR) -v "$(AIW_DATA_ROOT)":$(DOCKER_DATA_DIR):ro
else
DOCKER_DATA_ARGS := -e AIW_DATA_ROOT=$(DOCKER_DATA_DIR)
endif

.PHONY: doctor coauthor-preflight validate compare-tables import-smoke path-leak-scan smoke-fixture reproduce-selected reproduce-table compare-selected-reproduction git-hygiene check-private-data audit-artifact-coverage reproduce-all-tables-dry-run reproduce-all-tables reproduction-status reproduce-figures figure-reproduction-status validate-data-room validate-patent-data patent-example-audit validate-wrds-data builder-hides-first-pass validate-sec-source c7-format-delta package-surface-audit data-sanity-audit textual-construct-audit patent-construct-audit journal-reproducibility-audit replication-audit referee-audit docker-build docker-preflight docker-private-check docker-reproduce-selected docker-replication-audit docker-shell share-readiness

doctor:
	$(PYTHON) scripts/doctor.py

coauthor-preflight: doctor validate path-leak-scan import-smoke smoke-fixture git-hygiene

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

reproduce-figures:
	PYTHONPATH=src $(PYTHON) scripts/reproduce_assets.py --tables F1,FC1 --include-figures --regenerate-figures --status-csv docs/figure_reproduction_status.csv --status-md docs/figure_reproduction_status.md

figure-reproduction-status:
	PYTHONPATH=src $(PYTHON) scripts/reproduce_assets.py --tables F1,FC1 --include-figures --regenerate-figures --status-only --status-csv docs/figure_reproduction_status.csv --status-md docs/figure_reproduction_status.md

validate-data-room:
	$(PYTHON) scripts/validate_data_room.py

audit-artifact-coverage:
	$(PYTHON) scripts/audit_artifact_coverage.py

validate-patent-data:
	$(PYTHON) scripts/validate_patent_data.py

patent-example-audit:
	$(PYTHON) scripts/build_patent_audit_examples.py $(PATENT_AUDIT_ARGS)

validate-wrds-data:
	$(PYTHON) scripts/validate_wrds_data.py

builder-hides-first-pass:
	PYTHONPATH=src $(PYTHON) -m semantic_ai_washing.analysis.extensions.builder_hides_right_tail

validate-sec-source:
	$(PYTHON) scripts/validate_sec_source_policy.py

reproduction-status:
	PYTHONPATH=src $(PYTHON) scripts/reproduce_assets.py --batch all --status-only --include-figures

git-hygiene:
	$(PYTHON) scripts/git_hygiene_check.py

compare-selected-reproduction:
	$(PYTHON) scripts/compare_selected_reproduction.py

c7-format-delta:
	$(PYTHON) scripts/explain_c7_format_delta.py

package-surface-audit:
	$(PYTHON) scripts/package_surface_audit.py

data-sanity-audit:
	$(PYTHON) scripts/data_sanity_audit.py

textual-construct-audit:
	$(PYTHON) scripts/textual_construct_audit.py

patent-construct-audit:
	$(PYTHON) scripts/patent_construct_audit.py

journal-reproducibility-audit:
	PYTHONPATH=src $(PYTHON) scripts/journal_reproducibility_audit.py

replication-audit:
	PYTHONPATH=src $(PYTHON) scripts/replication_audit.py

referee-audit: replication-audit

docker-build:
	docker build -t $(DOCKER_IMAGE) .

docker-preflight:
	docker run $(DOCKER_COMMON_ARGS) $(DOCKER_DATA_ARGS) $(DOCKER_IMAGE) make PYTHON=python coauthor-preflight

docker-private-check:
	@if [ -z "$(AIW_DATA_ROOT)" ]; then echo "Set AIW_DATA_ROOT=/path/to/ai-washing-private-data"; exit 2; fi
	docker run $(DOCKER_COMMON_ARGS) $(DOCKER_DATA_ARGS) $(DOCKER_IMAGE) make PYTHON=python check-private-data validate-data-room validate-sec-source validate-wrds-data validate-patent-data audit-artifact-coverage

docker-reproduce-selected:
	@if [ -z "$(AIW_DATA_ROOT)" ]; then echo "Set AIW_DATA_ROOT=/path/to/ai-washing-private-data"; exit 2; fi
	docker run $(DOCKER_COMMON_ARGS) $(DOCKER_DATA_ARGS) $(DOCKER_IMAGE) /bin/bash -lc 'make PYTHON=python reproduce-selected && make PYTHON=python TABLE_ID=T16 reproduce-table && make PYTHON=python compare-selected-reproduction'

docker-replication-audit:
	@if [ -z "$(AIW_DATA_ROOT)" ]; then echo "Set AIW_DATA_ROOT=/path/to/ai-washing-private-data"; exit 2; fi
	docker run $(DOCKER_COMMON_ARGS) $(DOCKER_DATA_ARGS) $(DOCKER_IMAGE) make PYTHON=python replication-audit

docker-shell:
	docker run -it $(DOCKER_COMMON_ARGS) $(DOCKER_DATA_ARGS) $(DOCKER_IMAGE) bash

share-readiness:
	AIW_DOCKER_IMAGE=$(DOCKER_IMAGE) AIW_DATA_ROOT="$(AIW_DATA_ROOT)" $(PYTHON) scripts/share_readiness.py
