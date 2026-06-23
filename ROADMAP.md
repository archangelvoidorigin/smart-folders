# Roadmap

## Current: v0.1.0

**Released:** 2026-06-23  
**Status:** MVP — core functionality complete, ready for community use

### What's in v0.1.0

- Universal template (`smart-folder.md`)
- 6 agent adapters (Claude, Gemini, Codex, Cursor, Kilo, Aider)
- Settings system with JSON Schema validation
- 9 predefined roles with inheritance
- 3 levels of depth
- 8 scripts: init, validate, convert, map, dashboard, audit, skill-create, skill-navigate
- Web dashboard (pure stdlib, no dependencies)
- Laws system (never-rules, always-rules, quality-gates)
- 3 working examples (knowledge-base, web-app, api-service)

---

## v0.2.0 — Q3 2026

### Smart Ignore Auto-generation

Detect project type from existing files (package.json → Node, requirements.txt → Python, go.mod → Go) and suggest optimal `.smartignore` patterns.

### Batch Init

Initialize smart folder hierarchies from a YAML spec:

```yaml
# smart-folders.yaml
root:
  role: Knowledge Keeper
  depth: deep
  children:
    - name: research
      role: Knowledge Keeper
    - name: src
      role: Creator
      children:
        - name: components
          role: Creator
```

```bash
python scripts/batch-init.py smart-folders.yaml
```

### Migration Tool

Import from DOX (`AGENTS.md` hierarchy) or MWP configurations into Smart Folder format.

### Dashboard Improvements

- Real-time token usage monitoring during agent sessions
- Click-to-edit folder settings from the browser
- Connection graph visualization

---

## v0.3.0 — Q4 2026

### Knowledge Integration

- Auto-generate index files from folder contents
- Cross-folder semantic search
- Knowledge pyramid (100% raw → 5% refined) tooling

### Multi-agent Coordination

- Task decomposition across multiple folders
- Conflict detection when two agents target the same folder
- Session locking to prevent concurrent edits

### CI/CD Integration

GitHub Actions workflow that:
1. Validates all smart folders on every push
2. Checks that connections point to existing folders
3. Flags token budget violations

---

## v1.0.0 — 2027

### Universal Standard

The goal: become the default way developers organize AI-assisted projects. Every major agent natively reads Smart Folders. Every IDE has a plugin. Every CI/CD system has a validation step.

### Plugin System

Third-party roles, law templates, and skill libraries distributed via a registry.

### Enterprise Features

Team permissions, approval workflows for law modifications, audit trails.

---

## Non-goals

Things Smart Folders will not do:

- **Execute code on behalf of agents.** The system organizes and instructs — execution is the agent's job.
- **Replace project management tools.** Chronicles are not JIRA. Smart Folders document AI work, not human work.
- **Enforce agent behavior technically.** Laws are instructions, not sandbox walls. The system trusts agents to follow explicit rules.
- **Add heavy dependencies.** If a feature requires a database, a vector store, or a web framework, it belongs in a separate integration layer, not the core.
