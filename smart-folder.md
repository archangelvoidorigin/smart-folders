# Smart Folder: [Folder Name]

## Purpose
What this folder contains and what it does. Be specific — one sentence minimum.

## Role
- **Name**: [Knowledge Keeper / Creator / Architect / Connector / Chronicler / Enabler / Archive / Staging / Custom]
- **Description**: What this folder's function is in the system
- **Level**: [0–10, how deep in the hierarchy — 0 is root]
- **Depth**: [shallow / medium / deep]

## Scope
**CAN do**:
- [List what agents are allowed to do here]

**CANNOT do**:
- [List what agents must never do here]

## Boundaries
- **CAN see**: [*.md, *.json, *.py — file patterns agents may read]
- **CANNOT see**: [*.log, node_modules/, secrets/ — cognitive boundary]
- **Token budget**: [8000 — max tokens to load from this folder]
- **File limit**: [500 — max files agent should index]

## Instructions
Step-by-step guidance for working in this folder. Be explicit. Agents do not infer — they follow.

## Context
- **Parent folder**: [relative path to parent smart-folder.md]
- **Child folders**: [list of immediate sub-folders with one-line purpose each]
- **Related folders**: [sibling or distant folders this one depends on]
- **Tools available**: [search, summarize, compare, generate — what agents can use here]

## Connections
- **Feeds into**: [which folders consume output from this one]
- **Receives from**: [which folders this one depends on for input]
- **Siblings**: [related folders at the same level]

## Agents
- **Allowed**: [claude, gemini, codex, cursor, kilo, aider]
- **Preferred**: [the agent best suited for this folder's work]
- **Restricted**: [agents that should not access this folder]

## Laws
- [ ] **Never**: [what agents must NEVER do — absolute prohibition]
- [ ] **Always**: [what agents must ALWAYS do — absolute requirement]
- [ ] **If**: [conditional rules — if X then Y]

## Metadata
- **Created**: [YYYY-MM-DD]
- **Author**: [name]
- **Version**: [1]
- **Quality score**: [1–10]
- **Last modified**: [YYYY-MM-DD]

---
*Smart Folder v0.1.0 — github.com/ArchangelVoidOrigin/smart-folders*
