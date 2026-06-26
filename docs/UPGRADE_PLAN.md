# Smart Folders — Upgrade Plan (v0.2.0)

> Two-tier dashboard + engine refactor. One tool, zero-dep by default, an optional
> build-step "Control OS" power-up. Status: **planned, not started.**

## Goal

Upgrade Smart Folders without breaking its identity. The default install stays
**zero-dependency, no-build** (`git clone && make dashboard` just works). A heavier,
graph-driven **Control OS** becomes an explicit opt-in (`make control-os`) behind its
own `package.json`. Both UIs share one backend.

The selling line — kept literally true: *"Zero dependencies, always. The Control OS is
an optional power-up — one command, never required."*

## Guiding constraints

1. **Zero-dep core is non-negotiable.** Everything outside `control-os/` is Python stdlib
   + vanilla JS. The new `smartfolders/` package adds *internal* imports, never an external dependency.
2. **Lite tier must be complete, not a demo.** Anything with a CLI equivalent (`validate`,
   `audit`, `map`, view, navigate) works in Lite. Only genuinely-new visual/edit affordances
   (Cytoscape graph, in-browser editing, creation wizard) may be Control-OS-only.
3. **No deletion, ever.** `DELETE`/remove = move to `06_LIMBO/`. No `rm`.
4. **One repo, one version, one CHANGELOG.** `control-os/` is a subdirectory, not a fork.

---

## The core optimization: one engine, many faces

Today four scripts (`validate.py`, `audit.py`, `map.py`, `dashboard.py`) each independently
`rglob("smart-folder.md")` and re-parse `settings.json` with duplicated boilerplate.
`init.sh` and `skill-create.py` each embed the same four templates. Collapse both into a
single internal package.

```
smartfolders/                 ← NEW internal package (the engine) — stdlib only
├── __init__.py
├── schema.py     ← load settings-schema.json ONCE → roles, bounds, defaults
│                    (moves validate.py:28-45 here; becomes the single source for all scripts)
├── core.py       ← scan(root) -> list[Folder]; ONE rglob + mtime cache; Folder dataclass
├── templates.py  ← render smart-folder.md / settings.json / .smartignore / laws from templates/
└── ops.py        ← validate(folder) / audit(folder) / build_map(folders)
                     as importable functions returning DATA (not printing)
```

`core.scan()` is the keystone — one cached tree walk returning a `Folder` dataclass
(`path`, `settings`, `role`, flags, `token_budget`, …) replaces four separate walks.

- `validate.py`, `audit.py`, `map.py` → thin CLI wrappers (~30 lines) that call `ops.*` and print.
- `dashboard.py` → **imports** `ops.*` directly; the `subprocess` calls (`dashboard.py:962-977`) are deleted.
- mtime cache in `core.scan` means repeated `/api/data` requests don't re-walk a 100k-file tree.

### Templates: one source of truth

```
templates/
├── smart-folder.md          ← {{name}} {{role}} {{depth}} {{date}} placeholders
├── settings.json
├── .smartignore
└── laws/
    ├── never-rules.md
    └── always-rules.md
```

`templates.py` renders these. `init.sh` collapses to a ~5-line shim calling
`python -m smartfolders.init`. The bash heredocs (`init.sh:27-188`) and the duplicate
Python templates in `skill-create.py:86-202` both delete. One templating path, reused by
the CLI, the create-wizard, and the API. This also fixes the inconsistent `.smartignore`
pattern sets (root has 40, init.sh 24, skill-create 21 → all read `templates/.smartignore`).

---

## Two-tier dashboard, one backend

```
scripts/dashboard.py   ← REST API (stdlib http.server). Serves dashboard/ (Lite)
│                         and control-os/dist/ when present. Imports ops.* (no subprocess).
dashboard/             ← Tier 1 LITE: extracted vanilla HTML/CSS/JS. No build.
│                         `make dashboard`. (current 912 embedded lines → real files)
└── control-os/        ← Tier 2: Vite + TS + Cytoscape. OPTIONAL. `make control-os`.
                          Own package.json. Talks to the same /api.
```

`dashboard.py` drops from **1052 → ~150 lines**. `ARCHITECTURE.md:106` ("~150 line frontend",
currently false at 912) becomes true again.

### README positioning (must ship with the tiering)

A tier table right after quickstart:

```
Dashboard comes in two flavors. Same API, same data, your choice.

  Lite (default)    Control OS (opt-in)
  make dashboard    make control-os
  Zero deps         Vite + Cytoscape
  Vanilla JS        Graph, editors, wizard
  Always works      Run once: npm install
```

The quickstart must never mention `npm`. If a basic action only works in Control OS, the
zero-dep story becomes marketing instead of fact — that's the trap to police.

---

## API contract (the shared spine — design once, both UIs consume)

Read endpoints (no security surface — ship first):

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/folders` | list (from `core.scan`, cached) |
| GET | `/api/folders/:path` | one folder, full detail |
| GET | `/api/folders/:path/settings` | settings.json content |
| GET | `/api/folders/:path/smart-folder` | smart-folder.md content |
| GET | `/api/folders/:path/smartignore` | .smartignore content |
| GET | `/api/folders/:path/laws` · `/laws/:file` | law files |
| GET | `/api/graph` | nodes + edges for Cytoscape |
| GET | `/api/stats` | aggregates |

Write endpoints (gated — see security; ship in Phase C):

| Method | Endpoint | Purpose |
|--------|----------|---------|
| PUT | `/api/folders/:path/settings` | update settings.json (schema-validated) |
| PUT | `/api/folders/:path/smart-folder` | update smart-folder.md |
| PUT | `/api/folders/:path/smartignore` | update .smartignore |
| PUT/POST | `/api/folders/:path/laws/:file` | update/create law file |
| POST | `/api/folders` | create folder (calls templates.py) |
| POST | `/api/folders/:path/move-to-limbo` | move to `06_LIMBO/` (never delete) |
| POST | `/api/{validate,audit,map}` | run via `ops.*` import (no subprocess) |

### `/api/graph` schema

```json
{
  "nodes": [{
    "id": "web-app", "label": "Web App", "role": "Creator", "depth": 1,
    "token_budget": 10000, "file_count": 45,
    "has_settings": true, "has_smartignore": false, "has_laws": false,
    "purpose": "Build and maintain the React frontend"
  }],
  "edges": [{
    "id": "kb->webapp", "source": "knowledge-base", "target": "web-app",
    "type": "feeds_into", "label": "design patterns"
  }]
}
```

Cytoscape rendering: nodes colored by role (reuse current badge palette), sized by token
budget, border thickness by depth; edges colored by type (`feeds_into`=green,
`receives_from`=blue, `parent`=purple, `sibling`=gray) with arrows, dashed for optional;
force-directed layout default, tree layout option; click→detail panel, drag, right-click
context menu, node search/filter.

---

## Write-mode security (≈40 lines, gates ALL mutations, mandatory because public)

A localhost server that writes files is reachable by any webpage in the browser via
DNS-rebinding/CSRF. One `_guard()` runs on every `PUT/POST/DELETE`:

1. `Origin`/`Host` must be `127.0.0.1:<port>` — kills DNS-rebinding.
2. CSRF token: server prints it on start, injects into the page, requires it as a request
   header on mutations.
3. Path containment: resolve target, assert it's inside the configured root, reject `../`.
4. No `rm` — `move-to-limbo` only.

This gates Phase C. Do not build editors before the guard exists.

---

## Tests (pytest — the only dev-dependency; fixtures = `examples/`)

- `core.scan` finds all three example folders.
- `ops.validate` flags a deliberately-broken folder; passes a good one.
- `ops.audit` efficiency math matches expected on a known fixture.
- `templates.render` round-trips placeholders.
- `schema` loads roles + bounds; falls back cleanly if schema missing.
- API handler returns valid JSON for each read endpoint.
- `_guard` rejects bad Origin and missing CSRF token; accepts valid.

A phase is "done" only when its tests are green.

---

## Sequence and gates

| Phase | Deliverable | Gate to next |
|-------|-------------|--------------|
| **0 — Engine** | `smartfolders/` package, `templates/`, CLI scripts rewired to `ops.*`, `init.sh` shim, dashboard imports ops, pytest green | tests pass; CLI output byte-identical to current |
| **A — Lite extraction** | `dashboard/` static files, `dashboard.py` as API server, read-only `/api/*` | Lite dashboard matches current behavior |
| **B — Control OS (read)** | `control-os/` Vite app, Cytoscape graph, read-only detail panel | graph renders the 3 examples correctly |
| **C — Write-mode** | `_guard`, schema-driven `settings.json` editor, then md/laws/ignore editors, create wizard, live validate-on-save | mutation + security tests pass |
| **D — Layers & polish** | tree / token-heatmap / role-distribution / law-coverage layers (re-skins of `ops` data), cross-folder search, graph PNG/SVG export, persisted layout (localStorage), auto-refresh poll | — |

**Phase 0 is pure win and commits to nothing downstream:** dashboard 7× smaller, duplication
gone, test net in place, and every later phase depends on `smartfolders/` + the API. If work
stops after Phase 0, the repo is strictly better.

---

## What does NOT change

- All existing CLI usage (`make ...`, `python scripts/*.py`) works identically.
- `smart-folder.md` template structure stays compatible.
- `settings-schema.json` remains the schema authority (now consumed by *all* scripts, not just validate).
- Zero external Python dependencies in core and Lite.

## Doc fixes bundled into this work

- `ARCHITECTURE.md:106` "~150 line frontend" — true again after extraction.
- README — add the two-tier table + `control-os/` opt-in; keep quickstart `npm`-free.
- Roadmap — fold these phases into v0.2.0; note Cytoscape graph + write-mode landed here.

## Corrections to the original analysis

- The repo **does** eat its own dogfood — `smart-folder.md` exists at root (the "issue #10"
  claim is wrong); only nuance is it isn't converted to `AGENTS.md`.
- "Shared library already violated" overstates it — loading a JSON schema and shelling out
  are not a shared library. The *recommendation* (build `smartfolders/`) stands; the premise was thin.
