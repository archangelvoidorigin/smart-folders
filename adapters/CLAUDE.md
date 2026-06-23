# CLAUDE.md — Smart Folder Adapter (Claude)

This folder is configured with the Smart Folder system, optimized for Claude. Read this file first.

## Claude-Specific Capabilities

Use these Claude features where appropriate for this folder's work:
- **Extended thinking**: for complex reasoning, architecture decisions, or multi-step analysis
- **Artifacts**: for substantial outputs — code files, documents, designs — create as artifacts rather than inline responses
- **Vision**: if this folder contains images, diagrams, or screenshots, use vision to analyze them
- **Long context**: Claude's large context window does not remove the need to respect token budgets — focused context produces better output than bloated context

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

## Claude Working Rules

1. Read before acting — understand the folder's purpose fully before making changes
2. Use extended thinking for complex decisions within this folder
3. Create artifacts for all substantial file outputs
4. Stay in scope — only operate within this folder's defined boundaries
5. Respect the token budget in `settings.json` even with a large context window
6. Document reasoning in chronicles/ if it exists
7. Never modify `laws/` without explicit user permission

## Quality Checklist

Before finishing work in this folder:
- [ ] Does my output follow the folder's instructions and purpose?
- [ ] Did I respect all laws?
- [ ] Am I within the token budget?
- [ ] Did I use extended thinking for complex decisions?
- [ ] Are substantial outputs created as artifacts?
- [ ] Did I maintain connections to folders this one feeds into?

## Need Help?

If instructions are unclear or contradictory, ask for clarification before acting. Do not guess. Smart Folders are explicit — if something is not stated, it is not permitted.
