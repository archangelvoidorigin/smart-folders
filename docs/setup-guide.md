# Setup Guide

## Requirements

- Python 3.8+
- bash (for `init.sh`)
- No other dependencies

## Installation

```bash
git clone https://github.com/ArchangelVoidOrigin/smart-folders.git
cd smart-folders
```

That's it. No `pip install`, no `npm install`.

---

## Level 1: Simple (5 minutes)

Copy `smart-folder.md` into any folder and fill it out.

```bash
cp smart-folder.md /path/to/my-project/
```

Open it in any editor. Fill in Purpose, Role, Scope, and Instructions. Your agent will read it.

**Rename for your agent:**

```bash
# Claude Code
cp smart-folder.md /path/to/my-project/CLAUDE.md

# OpenAI Codex / OpenCode
cp smart-folder.md /path/to/my-project/AGENTS.md

# Gemini
cp smart-folder.md /path/to/my-project/GEMINI.md

# Cursor
cp smart-folder.md /path/to/my-project/CURSOR.md

# Aider
cp smart-folder.md /path/to/my-project/AIDER.md
```

Or use the converter to generate all formats at once:

```bash
python scripts/convert.py /path/to/my-project/ --agent all
```

---

## Level 2: Custom (15 minutes)

Use `init.sh` to scaffold the full structure automatically.

```bash
bash scripts/init.sh my-project Creator medium
```

Arguments:
- Folder name (required)
- Role: `Knowledge Keeper`, `Creator`, `Architect`, `Connector`, `Chronicler`, `Enabler`, `Archive`, `Staging`, `Custom`
- Depth: `shallow`, `medium`, `deep`

Or use the interactive skill:

```bash
python scripts/skill-create.py
```

It will ask you questions and generate everything.

After creation, open `settings.json` and configure:
- `boundaries.can_see` — what files agents may load
- `boundaries.cannot_see` — cognitive boundaries
- `boundaries.token_budget` — max tokens for this folder
- `connections.feeds_into` — downstream folders

Validate your setup:

```bash
python scripts/validate.py my-project/
```

---

## Level 3: Deep

Add `laws/` for absolute guardrails.

```bash
mkdir my-project/laws/
cp laws/never-rules.md my-project/laws/
cp laws/always-rules.md my-project/laws/
cp laws/quality-gates.md my-project/laws/
```

Edit the law files to add folder-specific rules. The starter rules in `laws/` are sensible defaults — customize them for your project.

Add `.smartignore` to enforce cognitive boundaries:

```bash
cp .smartignore my-project/
```

Edit it to exclude anything agents should not think about.

---

## Dashboard

Launch the visual dashboard to see all folders, health status, roles, and token budgets:

```bash
python scripts/dashboard.py my-project/
# Open http://localhost:8080
```

From the dashboard you can also run validate, audit, and map directly in the browser.

---

## Validation

Run at any time to check your folder structure:

```bash
# Single folder
python scripts/validate.py my-project/

# All folders recursively
python scripts/validate.py my-project/ --recursive
```

---

## Token Audit

See how much token budget you've allocated and where efficiency can improve:

```bash
python scripts/audit.py my-project/
python scripts/audit.py my-project/ --output report.json
```

---

## make Targets

If you prefer make:

```bash
make init    FOLDER=my-project
make validate FOLDER=my-project
make convert  FOLDER=my-project AGENT=claude
make map      FOLDER=my-project
make audit    FOLDER=my-project
make dashboard FOLDER=my-project
make validate-examples  # validates the bundled examples
```

---

## Multi-folder Projects

For projects with multiple smart folders, use `--recursive` validation and the map tool:

```bash
python scripts/validate.py /path/to/project/ --recursive
python scripts/map.py /path/to/project/ --stats --connections
```

The map shows the full hierarchy, role distribution, and connection graph.
