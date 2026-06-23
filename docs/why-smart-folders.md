# Why Smart Folders

## The Problem

AI coding agents are powerful and getting lost constantly.

They create files in the wrong directories. They duplicate functionality that already exists elsewhere. They violate project conventions because they don't know what the conventions are. They load 150,000 tokens of irrelevant context to answer a question about one component. They do things they weren't supposed to, because no one told them not to.

The larger the codebase, the worse this gets.

## What Exists

**DOX** (2025) proved that hierarchical `AGENTS.md` files work. Give an agent a tree of instruction files coupled to your code structure, and it navigates better. The proof is in production — Agent Zero built Space Agent with this system.

**MWP** proved that folder-based context loading saves tokens and improves focus. Load only what's relevant to the current task.

**AgentFS** (Turso) provides a filesystem abstraction for agents with a SQLite backend — a storage layer, not an instruction system.

**SKILL.md / AGENTS.md** is an emerging standard recognized by Claude Code, Codex, Copilot, and others.

## The Gap

None of these combine:

1. **One file format that works with every agent.** DOX is `AGENTS.md`. Claude uses `CLAUDE.md`. Cursor uses `.cursorrules`. Gemini uses `GEMINI.md`. Aider uses `AIDER.md`. You either pick one and lock yourself to one tool, or maintain six different files.

2. **Three levels of depth.** DOX is all-or-nothing. There's no "beginner" path that works with just one file and no configuration, and there's no "power user" path that adds laws, cognitive boundaries, and session chronicles.

3. **Cognitive boundaries.** `.gitignore` tells git what to ignore. `.smartignore` tells agents what not to *think about*. Not just file exclusion — enforced cognitive scope. DOX has no equivalent.

4. **Per-folder role semantics.** Telling an agent "you are in a Knowledge Keeper folder, not a Creator folder" changes how it interprets ambiguous instructions. Role inheritance lets parent folders set the outer boundary while child folders add specificity.

5. **A visual dashboard.** The system is designed to be used by humans who aren't writing config files. The dashboard shows folder health, role distribution, token budgets, and connections — no code required.

6. **AI skills that guide the system.** `skill-create.py` walks you through creating a folder interactively. `skill-navigate.py` takes a task description and tells you exactly which folder to work in.

## What Smart Folders Adds

Smart Folders is DOX plus:

- Universal adapter system (one source, convert to any format)
- Three levels of depth with a clear upgrade path
- Cognitive boundaries via `.smartignore`
- Role system with semantic inheritance
- Settings system with JSON Schema validation
- Visual web dashboard (no dependencies)
- Two AI skills for folder creation and navigation
- Laws system (absolute rules that no agent can override)
- Chronicles (session documentation built into the structure)
- Token audit tooling

## The Philosophy

> "People don't create from facts. They create from imagination."

Smart Folders are not about adding more rules to constrain agents. They are about making organization explicit enough that any AI model — large or small, any provider — can follow it precisely.

The minimum viable use is one file: `smart-folder.md`. Drop it in any folder. That's all you need.

The full system unlocks when you need it. Not before.
