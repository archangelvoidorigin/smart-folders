# AIDER.md — Smart Folder Adapter (Aider)

This folder is configured with the Smart Folder system, optimized for Aider. Read this file first.

## Aider-Specific Capabilities

Use these Aider features where appropriate:
- **Pair programming**: treat every change as a collaborative decision — explain before acting
- **Git commits**: all changes must be committed with a descriptive message
- **Context management**: use `/add` and `/drop` to keep context focused on this folder
- **Architect mode**: for high-level design decisions, use Architect mode before implementation
- **Code map**: use Aider's repo map to understand how this folder connects to others

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

## Aider Working Rules

1. Add only the files from this folder to context — use `/add` selectively
2. Drop unrelated files with `/drop` before starting work
3. Use Architect mode for design decisions, then implement
4. Commit every meaningful change with a descriptive message
5. Explain what you are about to do before making changes
6. Respect the token budget — Aider's repo map can bloat context quickly
7. Never modify `laws/` without explicit user permission

## Quality Checklist

Before finishing work in this folder:
- [ ] Does my output follow the folder's instructions and purpose?
- [ ] Did I respect all laws?
- [ ] Did I commit all changes with descriptive messages?
- [ ] Is context limited to only the files this folder needs?
- [ ] Did I maintain connections to folders this one feeds into?

## Need Help?

If instructions are unclear, ask for clarification. Do not make changes without explaining them first. Smart Folders are explicit — if something is not stated, it is not permitted.
