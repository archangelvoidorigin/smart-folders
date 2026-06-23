# KILO.md — Smart Folder Adapter (Kilo Code)

This folder is configured with the Smart Folder system, optimized for Kilo Code. Read this file first.

## Kilo-Specific Capabilities

Use these Kilo Code features where appropriate:
- **Code generation**: generate complete, working implementations — not stubs
- **Refactoring**: improve existing code without changing behavior
- **Test generation**: write tests for all code you create or modify
- **Documentation**: generate inline docs and README sections

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

## Kilo Working Rules

1. Read before generating — understand the folder's purpose before writing code
2. Generate tests for all code you create in this folder
3. Stay in scope — only generate files this folder's purpose covers
4. Follow coding conventions defined in the folder's instructions
5. Respect the token budget — load only what is needed for the current task
6. Never modify `laws/` without explicit user permission

## Quality Checklist

Before finishing work in this folder:
- [ ] Does my output follow the folder's instructions and purpose?
- [ ] Did I respect all laws?
- [ ] Did I write tests for all generated code?
- [ ] Is the generated code complete and runnable — not stubbed?
- [ ] Did I maintain connections to folders this one feeds into?

## Need Help?

If instructions are unclear, ask for clarification. Do not generate placeholder code. Smart Folders are explicit — if something is not stated, it is not permitted.
