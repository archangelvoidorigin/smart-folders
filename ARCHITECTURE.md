# Architecture

## Design Principles

1. **No required dependencies.** All scripts use Python standard library. Drop a file in a folder — that's the minimum viable unit.
2. **Hierarchical by default.** Instructions resolve from root to leaf. Closer wins, laws are absolute.
3. **Universal adapters.** One source file (`smart-folder.md`) generates all agent formats via `convert.py`.
4. **Three levels of depth.** Level 1 is one file. Level 2 adds configuration. Level 3 adds laws and chronicles. You pick.

---

## System Layers

```
┌─────────────────────────────────────────────────┐
│  INTERFACE LAYER                                │
│  dashboard.py (web UI)  |  skill-create.py      │
│  skill-navigate.py      |  make targets          │
├─────────────────────────────────────────────────┤
│  PROCESSING LAYER                               │
│  validate.py  |  convert.py  |  audit.py        │
│  map.py                                         │
├─────────────────────────────────────────────────┤
│  CORE LAYER                                     │
│  smart-folder.md (template)                     │
│  settings-schema.json                           │
│  adapters/  |  roles/  |  laws/                 │
├─────────────────────────────────────────────────┤
│  FILESYSTEM LAYER                               │
│  Any directory + smart-folder.md                │
│  settings.json  |  .smartignore  |  laws/       │
└─────────────────────────────────────────────────┘
```

---

## Core Entities

### Smart Folder

A directory with at minimum one `smart-folder.md`. That's the atomic unit of the system.

```
my-folder/
├── smart-folder.md      ← required (Level 1)
├── settings.json        ← optional (Level 2)
├── .smartignore         ← optional (Level 2)
└── laws/                ← optional (Level 3)
    ├── never-rules.md
    ├── always-rules.md
    └── quality-gates.md
```

### Instruction Resolution

When an agent enters a folder, it resolves instructions in this order:

1. Root-level adapter file (CLAUDE.md, AGENTS.md, etc.)
2. Current folder's smart-folder.md
3. Current folder's settings.json
4. Current folder's laws/
5. Parent folder's smart-folder.md (via reference in Context section)

**Conflict resolution:** Closer instructions win. Child folder rules override parent folder rules. Laws are the exception — no child can override a law from an ancestor.

### Role System

Roles are semantic labels that shape agent behavior. They are not technically enforced — they are instructions that well-behaved agents follow.

Role inheritance: a child folder's role operates within the boundaries set by its parent's role. A `Staging` folder inside an `Archive` can experiment freely within the Archive's immutability rules.

### Settings Schema

`settings.json` is validated against `settings-schema.json` (JSON Schema draft-07). Required fields: `folder.name`, `folder.role`, `boundaries.can_see`, `boundaries.cannot_see`.

The schema is in the repo root. `validate.py` loads it and checks compliance.

---

## Script Architecture

All scripts are standalone Python modules. No shared library, no imports between scripts. This is intentional — each script works independently, with no setup required.

| Script | Input | Output |
|--------|-------|--------|
| `init.sh` | folder name, role, depth | folder structure on disk |
| `validate.py` | folder path | pass/fail with error details |
| `convert.py` | folder path + agent | agent-specific instruction file |
| `map.py` | root path | ASCII tree + stats + connections |
| `audit.py` | root path | efficiency scores + suggestions |
| `dashboard.py` | root path | HTTP server on localhost:8080 |
| `skill-create.py` | interactive or args | folder structure on disk |
| `skill-navigate.py` | task + agent | recommended folder path + steps |

---

## Dashboard Architecture

`dashboard.py` uses Python's stdlib `http.server`. No Flask, no FastAPI, no npm.

Three endpoints:
- `GET /` — serves the dashboard HTML (embedded in the script)
- `GET /api/data` — returns folder tree as JSON
- `POST /api/validate|audit|map` — runs the corresponding script as a subprocess, returns stdout

The dashboard is a single-page app with vanilla JS. No React, no build step. The entire frontend is ~150 lines of HTML/CSS/JS embedded in the Python file.

---

## Extension Points

**Adding a new agent:**
1. Add entry to `AGENT_FILES` and `AGENT_TIPS` in `convert.py`
2. Add adapter file in `adapters/`
3. Add agent to the `allowed` enum in `settings-schema.json`

**Adding a new role:**
1. Add to the `role` enum in `settings-schema.json`
2. Add role definition in `roles/role-definitions.md`
3. Add color in `map.py` `ROLE_COLORS`
4. Add affinity in `skill-navigate.py` `ROLE_KEYWORD_AFFINITY`

**Adding a new script:**
1. Create standalone script in `scripts/`
2. Add make target in `Makefile`
3. Add API endpoint in `dashboard.py` if dashboard integration is needed
