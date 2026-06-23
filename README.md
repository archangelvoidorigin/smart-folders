# Smart Folders

**Universal AI agent workspace organization. One system, every agent.**

[![Validate Examples](https://github.com/ArchangelVoidOrigin/smart-folders/actions/workflows/validate.yml/badge.svg)](https://github.com/ArchangelVoidOrigin/smart-folders/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![No Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)]()

---

## The Problem

AI agents get lost. They create files in wrong places, duplicate functionality, break conventions, and bloat context windows. The larger the codebase, the worse it gets.

DOX proved hierarchical instructions work. MWP proved folder-based context loading saves tokens. But no system combines all of this:

- One file format that works with Claude, Gemini, Codex, Cursor, Kilo, and Aider
- Three levels of depth — drop-in simple to full biological architecture
- Cognitive boundaries (`.smartignore`) — not just file exclusion, but what agents must not *think about*
- Per-folder role system with semantic inheritance
- A visual dashboard non-technical users can actually use
- AI skills that guide folder creation and navigation

Smart Folders closes that gap.

---

## How It Works

Drop a `smart-folder.md` in any folder. Your agent reads it and knows exactly where it is, what it can do, and what it cannot touch. Child folders inherit from parents. Laws are absolute. Context stays focused.

```
my-project/
├── smart-folder.md          ← "This is a React web app. Read this first."
├── src/
│   ├── smart-folder.md      ← "Source code. Follow these conventions."
│   └── components/
│       └── smart-folder.md  ← "UI components. WCAG 2.1 AA required."
└── docs/
    └── smart-folder.md      ← "Documentation. Keep it concise."
```

Every agent reads its own format. Rename `smart-folder.md` to what your agent reads:

| Agent | File |
|-------|------|
| Claude Code | `CLAUDE.md` |
| OpenAI Codex / OpenCode | `AGENTS.md` |
| Gemini / Antigravity | `GEMINI.md` |
| Cursor | `CURSOR.md` |
| Kilo Code | `KILO.md` |
| Aider | `AIDER.md` |

Or use `convert.py` to generate all formats from one source file.

---

## See It

`python scripts/map.py examples/ --stats --connections` renders the whole tree —
roles, token budgets, and how folders feed each other (colored in a real terminal):

```
SMART FOLDER MAP
============================================================
Root: examples
Folders: 3

Role distribution:
  Architect: 1
  Creator: 1
  Knowledge Keeper: 1

Tree:
  └── api-service [Architect]
      -> web-app/
  └── knowledge-base [Knowledge Keeper]
      -> ../web-app/, ../api-service/
  └── web-app [Creator]
      -> deploy/

STATISTICS
============================================================
Total folders : 3      Total tokens : 32,000
Max depth     : 1      Avg tokens   : 10,666
```

The same data is available in the browser via `dashboard.py` — folder health,
role distribution, and live validate/audit/map, with zero dependencies.

---

## Three Levels of Depth

**Level 1 — Simple.** Drop `smart-folder.md` in any folder. Done.

**Level 2 — Custom.** Add `settings.json` to configure role, token budget, boundaries, and agent preferences.

**Level 3 — Deep.** Add `laws/` for absolute guardrails, `.smartignore` for cognitive boundaries, and `chronicles/` for session documentation.

Start at Level 1. Add depth only when you need it.

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/ArchangelVoidOrigin/smart-folders.git
cd smart-folders

# Initialize Smart Folders in your project
bash scripts/init.sh my-project Creator medium

# Or run interactively
python scripts/skill-create.py

# Validate your folder structure
python scripts/validate.py my-project/

# Convert to agent-specific formats
python scripts/convert.py my-project/ --agent all

# Launch the dashboard
python scripts/dashboard.py my-project/

# Generate a folder map
python scripts/map.py my-project/ --stats --connections
```

---

## What's Inside

```
smart-folders/
├── smart-folder.md          ← The universal template
├── settings-schema.json     ← JSON Schema for settings.json
├── .smartignore             ← Default cognitive boundaries
├── adapters/                ← Per-agent instruction files
│   ├── AGENTS.md, CLAUDE.md, GEMINI.md, CURSOR.md, KILO.md, AIDER.md
├── roles/                   ← Role definitions
├── laws/                    ← Default guardrails
├── scripts/                 ← The toolkit
│   ├── init.sh              ← Initialize smart folders in any directory
│   ├── validate.py          ← Check folder health and consistency
│   ├── convert.py           ← Generate agent-specific formats
│   ├── map.py               ← Visual tree of all folders and connections
│   ├── dashboard.py         ← Web UI (no dependencies, pure stdlib)
│   ├── audit.py             ← Token usage analysis and optimization
│   ├── skill-create.py      ← Interactive folder creation assistant
│   └── skill-navigate.py    ← Navigate to the right folder for any task
├── examples/                ← Working demos
│   ├── knowledge-base/      ← Research and documentation setup
│   ├── web-app/             ← Frontend project setup
│   └── api-service/         ← Backend API setup
└── docs/                    ← Guides and philosophy
```

---

## The Role System

Each folder has a semantic role that shapes how agents behave inside it:

| Role | What It Is | Metaphor |
|------|------------|---------|
| **Knowledge Keeper** | Stores and organizes information | The library |
| **Creator** | Builds and creates things | The workshop |
| **Architect** | Designs systems and schemas | The blueprint room |
| **Connector** | Links tools and workflows | The switchboard |
| **Chronicler** | Documents everything | The scribe |
| **Enabler** | Provides tools and utilities | The toolbox |
| **Archive** | Preserves history | The vault |
| **Staging** | Experiments safely | The sandbox |

Roles inherit. A child `Creator` folder inside a `Knowledge Keeper` parent inherits the parent's constraints while adding its own.

---

## The Dashboard

```bash
python scripts/dashboard.py /path/to/project
# Open http://localhost:8080
```

No external dependencies. Pure Python stdlib. Shows folder health, role distribution, token budgets, and connections. Validate, audit, and map your project from the browser.

---

## Philosophy

> "People don't create from facts. They create from imagination."

Smart Folders are not about constraining how you organize. They are about making organization explicit enough that any AI agent — large or small, any provider — can follow it precisely.

The system breaks down instructions to the minimum. If a small model can follow it, a large model can follow it better.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and PRs welcome.

## License

MIT — see [LICENSE](LICENSE).
