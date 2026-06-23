# Token Optimization Guide

## Why Token Budget Matters

More context is not always better. An agent with 150,000 tokens of mostly-irrelevant context makes worse decisions than an agent with 8,000 tokens of precisely relevant context.

Token budget in Smart Folders is not a hard technical limit — it is a design constraint that forces you to be precise about what agents need to know.

## Setting the Budget

| Folder Type | Recommended Budget | Why |
|-------------|-------------------|-----|
| Root / global context | 12,000–20,000 | Sets system-wide context |
| Domain folder (OMNI, CORTEX) | 8,000–12,000 | Domain-level instructions |
| Work folder | 6,000–8,000 | Task-focused, specific |
| Leaf / sub-folder | 2,000–6,000 | Narrow scope |

Start at 8,000. Audit with `audit.py`. Raise only when validation shows content is being truncated.

## The `.smartignore` Multiplier

Every pattern in `.smartignore` extends the effective value of your token budget. An agent that ignores `node_modules/` (often 50,000+ tokens of lock files and minified code) gets 50,000 tokens back for useful work.

Mandatory `.smartignore` entries:
```
node_modules/
dist/
build/
.cache/
*.log
*.lock
*.min.js
*.map
```

## Hierarchical Loading

Smart Folders use lazy loading by design: an agent in `src/components/Button/` should not load `src/pages/Dashboard/` unless explicitly instructed. The folder hierarchy is the loading hierarchy.

How agents should load context:
1. Root adapter file (CLAUDE.md / AGENTS.md) — always
2. Current folder's smart-folder.md — always
3. Current folder's settings.json — always
4. Current folder's laws/ — before making changes
5. Parent folder's smart-folder.md — when current instructions reference it
6. Child folder contents — only when the task requires going deeper

This pattern means a 150,000-token context window can span 15+ folders without each folder needing to load all of its contents.

## Token Audit

Run the audit tool to see your current budget allocation:

```bash
python scripts/audit.py /path/to/project/
```

Efficiency score formula:
- Start at 100
- Budget > 25k: -30
- Budget > 15k: -20
- Budget > 8k: -10
- Missing .smartignore: -15
- Missing settings.json: -25
- File count exceeds limit: -20

Target: 80%+ across all folders.

## Practical Tips

**Compress instructions.** An instruction like "Always ensure that all files created within this folder adhere to the team's established coding conventions as documented in the project's contributing guide" can be "Follow conventions in CONTRIBUTING.md." Same meaning, 60% fewer tokens.

**Use cross-references, not copies.** If a law appears in both a parent and child folder, remove it from the child. The parent's law already applies.

**Split verbose folders.** A folder whose smart-folder.md needs more than 2,000 tokens to explain is probably doing too many things. Split it into sub-folders with focused purposes.

**Set `depth_limit`.** A folder with `depth_limit: 2` prevents agents from recursively loading all descendants. Combine with precise Instructions about when to go deeper.
