# AGENTS.md — Smart Folder Adapter (Universal)

This folder is configured with the Smart Folder system. Read this file first.

## How to Navigate This Folder

1. Read this file completely
2. Read `smart-folder.md` if it exists — it has the folder's specific instructions
3. Read `settings.json` if it exists — it defines boundaries and configuration
4. Read `.smartignore` if it exists — these files and directories are off-limits
5. Read all files in `laws/` before doing any work — these are absolute rules

## Folder Hierarchy

Smart Folders use hierarchical instruction resolution:
- Parent folder instructions apply to all children unless explicitly overridden
- Child folder instructions add specificity and narrow scope
- Closer instructions win — child rules take precedence over parent rules in conflicts
- Laws are absolute — no child can override a law from a parent

## Working Rules

1. Read before acting — understand the folder's purpose and boundaries first
2. Stay in scope — only create, edit, or delete files within this folder's defined purpose
3. Respect the token budget — do not load more context than `settings.json` allows
4. Document changes — note what you did and why in `chronicles/` if it exists
5. Never modify `laws/` files without explicit permission
6. Never ignore `.smartignore` — those boundaries exist for security and focus

## Quality Checklist

Before finishing work in this folder:
- [ ] Does my output follow the folder's purpose and instructions?
- [ ] Did I respect all laws?
- [ ] Did I stay within the token budget?
- [ ] Did I maintain connections to other folders this one feeds into?
- [ ] Would a reviewer understand what I did and why?

## Need Help?

If instructions are unclear or contradictory, ask for clarification. Do not guess. Smart Folders are designed to be explicit — if something is not stated, it is not permitted.
