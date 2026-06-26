.PHONY: init validate convert map audit dashboard create navigate clean help

FOLDER ?= .
AGENT  ?= all
PORT   ?= 8080

help:
	@echo "Smart Folders — available targets:"
	@echo ""
	@echo "  make init      FOLDER=my-dir    Initialize smart folders in a directory"
	@echo "  make validate  FOLDER=my-dir    Validate folder health"
	@echo "  make convert   FOLDER=my-dir    Convert to all agent formats"
	@echo "  make map       FOLDER=my-dir    Generate folder map"
	@echo "  make audit     FOLDER=my-dir    Analyze token usage"
	@echo "  make dashboard FOLDER=my-dir    Launch web dashboard (port 8080)"
	@echo "  make create                     Interactive folder creator"
	@echo "  make navigate                   Interactive navigation assistant"
	@echo "  make validate-examples          Validate all examples"
	@echo "  make clean                      Remove generated files"
	@echo ""
	@echo "Zero-dependency core: Python stdlib only."
	@echo "For the graph-based Control OS, see: make control-os"

init:
	bash scripts/init.sh $(FOLDER) Creator medium

validate:
	python scripts/validate.py $(FOLDER)

convert:
	python scripts/convert.py $(FOLDER) --agent $(AGENT)

map:
	python scripts/map.py $(FOLDER)

audit:
	python scripts/audit.py $(FOLDER)

dashboard:
	python scripts/dashboard.py $(FOLDER) --port $(PORT)

create:
	python scripts/skill-create.py

navigate:
	python scripts/skill-navigate.py

validate-examples:
	python scripts/validate.py examples/knowledge-base/
	python scripts/validate.py examples/web-app/
	python scripts/validate.py examples/api-service/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

control-os:
	@echo "Control OS is an optional power-up (Vite + Cytoscape)."
	@echo "To build: cd control-os && npm install && npm run build"
	@echo "Control OS is NOT required. The Lite dashboard works with zero deps."
