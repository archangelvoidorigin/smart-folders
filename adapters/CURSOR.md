# CURSOR.md — Smart Folder Adapter (Cursor)

This folder is configured with the Smart Folder system, optimized for Cursor. Read this file first.

## Cursor-Specific Capabilities

Use these Cursor features where appropriate:
- **Composer**: for multi-file changes, use Composer to coordinate edits across files
- **Agent Mode**: for autonomous multi-step tasks within this folder's scope
- **@ mentions**: reference specific files with @ to keep context focused
- **Tab**: use Cursor Tab for inline completions that respect the folder's conventions

## How to Navigate This Folder

1. Read this file completely
2. Read `smart-folder.md` — folder-specific purpose, scope, and instructions
3. Read `settings.json` — role, boundaries, token budget, agent configuration
4. Read `.smartignore` — files and directories agents must not access
5. Read all files in `laws/` before doing any work

## Folder Hierarchy

Smart Folders use hierarchical instruction resolution:
- Parent folder instructions apply to all children unless explicitly overridden
- Child folder instructions add specificity and narrow scope
- Closer instructions win — child rules take precedence in conflicts
- Laws are absolute — no folder can override a law from an ancestor

## Cursor Working Rules

1. Read before acting — understand the folder's purpose before opening Composer
2. Use @ mentions to load only the files this folder's instructions reference
3. In Agent Mode, stay within this folder's scope boundaries
4. Use Composer for all multi-file changes — do not edit files scattered across the project
5. Respect the token budget — do not load the entire codebase when only this folder is relevant
6. Never modify `laws/` without explicit user permission

## Quality Checklist

Before finishing work in this folder:
- [ ] Does my output follow the folder's instructions and purpose?
- [ ] Did I respect all laws?
- [ ] Did I use @ mentions to keep context focused?
- [ ] Did I use Composer for multi-file changes?
- [ ] Did I maintain connections to folders this one feeds into?

## Need Help?

If instructions are unclear, ask for clarification. Do not guess. Smart Folders are explicit — if something is not stated, it is not permitted.
