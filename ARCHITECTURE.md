# Architecture

## Design Principles

1. **No required dependencies.** All scripts use Python standard library. Drop a file in a folder — that's the minimum viable unit.
2. **One engine, many faces.** The `smartfolders/` package is the shared engine. CLI scripts import it. No duplicated logic.
3. **Hierarchical by default.** Instructions resolve from root to leaf. Closer wins, laws are absolute.
4. **Universal adapters.** One source file (`smart-folder.md`) generates all agent formats via `convert.py`.
5. **Three levels of depth.** Level 1 is one file. Level 2 adds configuration. Level 3 adds laws and chronicles. You pick.

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
│  map.py        (thin CLI wrappers)              │
├─────────────────────────────────────────────────┤
│  ENGINE LAYER                                   │
│  smartfolders/  package (stdlib only)           │
│  ├── schema.py    ← settings-schema.json loader │
│  ├── core.py      ← scan() + Folder dataclass   │
│  ├── templates.py ← render + create structure   │
│  └── ops.py       ← validate/audit/map logic    │
├─────────────────────────────────────────────────┤
│  TEMPLATES LAYER                                │
│  templates/ (single source of truth)            │
│  ├── smart-folder.md   ├── settings.json        │
│  ├── .smartignore      └── laws/                │
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

---

## Engine Package: `smartfolders/`

All scripts import from this package instead of duplicating logic.

| Module | Purpose |
|--------|---------|
| `schema.py` | Loads `settings-schema.json` once → roles, bounds, defaults. Cached. |
| `core.py` | `Folder` dataclass. `scan(root)` — one `rglob` + mtime cache returns `list[Folder]`. |
| `templates.py` | Renders templates from `templates/`. `create_folder_structure()` used by init + skill-create. |
| `ops.py` | `validate_folder()` / `audit_folder()` / `build_map()` — importable functions returning data (not printing). |
| `__main__.py` | `python -m smartfolders init <name>` — the init command. |

## Templates: `templates/`

Single source of truth for all scaffolded content. Both `init.sh` and `skill-create.py` render from these files. No more duplicate heredocs.

| File | Used By |
|------|---------|
| `smart-folder.md` | init, skill-create |
| `settings.json` | init, skill-create |
| `.smartignore` | init, skill-create (root version has 60 patterns) |
| `laws/never-rules.md` | init, skill-create |
| `laws/always-rules.md` | init, skill-create |
| `sub-folder.md` | init, skill-create |

---

## Script Architecture

All scripts are thin wrappers around the `smartfolders/` package.

| Script | Input | Output | Lines |
|--------|-------|--------|-------|
| `init.sh` | folder name, role, depth | calls `python -m smartfolders init` | 10 |
| `validate.py` | folder path | pass/fail via `ops.validate_folder()` | 45 |
| `convert.py` | folder path + agent | agent-specific instruction file | 184 |
| `map.py` | root path | ASCII tree via `ops.build_map()` + render | 40 |
| `audit.py` | root path | efficiency scores via `ops.audit_all()` | 40 |
| `dashboard.py` | root path | HTTP API server + vanilla JS frontend | 430 |
| `skill-create.py` | interactive or args | folder structure via `templates.create_folder_structure()` | 110 |
| `skill-navigate.py` | task + agent | recommended folder path + steps | 216 |

---

## Dashboard Architecture

`dashboard.py` is a stdlib `http.server` REST API. No Flask, no FastAPI. It serves two
frontends from the same API:

- **Lite (default, zero-dep):** `dashboard/index.html` — vanilla HTML/CSS/JS, no build step.
  Served at `/` when no Control OS build is present. `make dashboard`.
- **Control OS (opt-in):** `control-os/dist/` — React + Vite + Cytoscape graph, editors,
  wizard. Built with `make control-os`; auto-detected and served at `/` when `control-os/dist/`
  exists. Requires `npm install` once — never in the default path.

Read endpoints (no CSRF): `GET /api/folders`, `/api/folders/:path`, `/api/folders/:path/{settings,smart-folder,smartignore,laws[/:file]}`, `/api/graph`, `/api/stats`, `/api/search/:term`, `/api/csrf-token`, `/api/{validate,audit,map}` (run `ops.*` directly, no subprocess).

Write endpoints (guarded): `PUT /api/folders/:path/{settings,smart-folder,smartignore,laws/:file}`, `POST /api/folders`, `POST /api/folders/:path/delete` (soft-delete — moves the folder to `.trash/` inside the root, never `rm`; recoverable; excluded from scans).

**Security guard** (`_guard`, on every PUT/POST): Origin/Host must be localhost, a per-process
CSRF token is required, and write targets are contained to the root via `_within()` (a
`relative_to` check, not string-prefix). CORS reflects only localhost origins — never `*`.

---

## Extension Points

**Adding a new agent:**
1. Add entry to `AGENT_FILES` and `AGENT_TIPS` in `convert.py`
2. Add adapter file in `adapters/`
3. Add agent to the `allowed` enum in `settings-schema.json`

**Adding a new role:**
1. Add to the `role` enum in `settings-schema.json`
2. Add role definition in `roles/role-definitions.md`
3. Add color in `ops.py` `ROLE_COLORS`
4. Add affinity in `skill-navigate.py` `ROLE_KEYWORD_AFFINITY`

**Adding a new script:**
1. Create standalone script in `scripts/` (add to sys.path, import from `smartfolders`)
2. Add make target in `Makefile`
3. Add API endpoint in `dashboard.py` if dashboard integration is needed
