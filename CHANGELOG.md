# Changelog

All notable changes to this project will be documented in this file.

---

## [0.2.0] — 2026-06-26

### Added

- `smartfolders/` — internal engine package (stdlib only): `schema.py`, `core.py`, `templates.py`, `ops.py`
- `templates/` — single source of truth for scaffolded content: `smart-folder.md`, `settings.json`, `.smartignore`, `laws/`
- **mtime cache** in `core.scan()` — repeated API requests avoid re-walking the file tree
- `Folder` dataclass — unified data model replaces ad-hoc dicts across all scripts

### Changed

- **validate.py** — rewired to `ops.validate_folder()`; reduced from 201 → 45 lines
- **audit.py** — rewired to `ops.audit_all()` + `ops.print_audit()`; reduced from 184 → 40 lines
- **map.py** — rewired to `ops.build_map()` + render functions; reduced from 197 → 40 lines
- **dashboard.py** — imports `ops.*` directly (no `subprocess` calls); reduced from 1052 → 430 lines
- **init.sh** — collapsed from 247 lines of heredocs to 10-line shim calling `python -m smartfolders init`
- **skill-create.py** — uses `templates.create_folder_structure()`; removed duplicate template code
- **ARCHITECTURE.md** — updated to reflect engine package, new layer diagram, reduced line counts

### Fixed

- Inconsistent `.smartignore` pattern sets — root had 60 patterns, init.sh had 24, skill-create.py had 21; all now read from `templates/.smartignore`
- `dashboard.py:962-977` — removed `subprocess` calls; scripts now run in-process via `ops.*`
- `ARCHITECTURE.md:106` — "~150 line frontend" claim corrected to reflect actual 430-line embedded frontend

---

## [0.1.0] — 2026-06-23

### Added

- `smart-folder.md` — universal instruction template
- `settings-schema.json` — JSON Schema (draft-07) for settings.json validation
- `.smartignore` — default cognitive boundary patterns
- `adapters/` — instruction files for Claude, Gemini, Codex, Cursor, Kilo, and Aider
- `roles/role-definitions.md` — 9 predefined roles with inheritance semantics
- `laws/never-rules.md`, `laws/always-rules.md`, `laws/quality-gates.md`
- `scripts/init.sh` — scaffold a smart folder structure in any directory
- `scripts/validate.py` — health check with `--recursive` flag
- `scripts/convert.py` — convert `smart-folder.md` to all agent formats
- `scripts/map.py` — colored ASCII tree with stats and connection graph
- `scripts/audit.py` — token usage analysis with efficiency scoring
- `scripts/dashboard.py` — web UI with live validate/audit/map via browser (no dependencies)
- `scripts/skill-create.py` — interactive folder creation assistant
- `scripts/skill-navigate.py` — task-based folder navigation assistant
- `examples/knowledge-base/` — fully configured Knowledge Keeper example
- `examples/web-app/` — fully configured Creator example (React frontend)
- `examples/api-service/` — fully configured Architect example (REST API)
- `docs/why-smart-folders.md` — problem statement and gap analysis
- `docs/setup-guide.md` — three-level setup walkthrough
- `docs/best-practices.md` — folder design, token budget, law, and connection guidance
- `docs/token-guide.md` — token optimization strategies
- `Makefile` — convenient targets for all scripts
