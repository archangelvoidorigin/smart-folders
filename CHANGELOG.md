# Changelog

All notable changes to this project will be documented in this file.

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
