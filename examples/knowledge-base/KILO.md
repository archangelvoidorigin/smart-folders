# KILO.md — Smart Folder Adapter (Kilo Code)

This folder is configured with the Smart Folder system. Read this file first.

## Kilo Configuration
- Generate **complete, working implementations** — no stubs
- Write **tests** for all code you create or modify
- Follow the coding conventions defined in this folder's instructions
- Respect token_budget — load only what is needed

## How to Navigate This Folder

1. Read this adapter file first (you are doing this now)
2. Read `smart-folder.md` — purpose, scope, role, and specific instructions
3. Read `settings.json` — boundaries, token budget, and agent configuration
4. Read `.smartignore` — files and directories that are off-limits
5. Read all files in `laws/` before making any changes

## Folder Hierarchy

Smart Folders use hierarchical instruction resolution:
- **Parent** folder instructions apply to all children unless explicitly overridden
- **Child** folder instructions add specificity and narrow scope
- **Closer instructions win** — child rules take precedence in conflicts
- **Laws are absolute** — no folder can override a law from an ancestor

## Purpose
Store, organize, and surface research on AI agent systems, tools, and patterns. This folder is the source of truth for all research that feeds into the project's design decisions.

## Role
- **Name**: Knowledge Keeper
- **Description**: The library — curates and surfaces research, does not create products
- **Level**: 1
- **Depth**: deep

## Scope
**CAN do**:
- Add new research documents, summaries, and analysis
- Organize existing content into sub-categories
- Synthesize findings across multiple sources
- Create index files and cross-references

**CANNOT do**:
- Write code (code belongs in Creator folders)
- Make design decisions (those belong in Architect folders)
- Delete existing research documents

## Boundaries
- **CAN see**: ["*.md", "*.txt", "*.json", "*.pdf"]
- **CANNOT see**: ["*.py", "*.js", "*.ts", "node_modules/", ".git/", "secrets/"]
- **Token budget**: 12000
- **File limit**: 200

## Instructions
1. Before adding content, check the existing index to avoid duplication
2. Every new document must include a metadata header (date, source, quality score)
3. Organize by category: `ai-agents/`, `tools/`, `patterns/`, `research/`
4. Cross-reference related documents using relative links
5. Maintain `index.md` at the folder root — it is the map agents use to navigate here
6. Quality threshold: only add content that scores 7+ on the 1–10 scale

## Laws
- [ ] Never: delete existing research documents
- [ ] Never: add content without a source reference
- [ ] Always: update index.md when adding new content
- [ ] Always: assign a quality score (1–10) in the metadata header
- [ ] If: a document's quality score is below 7, mark it as draft and note why

## Quality Checklist

Before finishing work in this folder:
- [ ] Output follows the folder's instructions and stated purpose
- [ ] All laws are respected
- [ ] Token budget is not exceeded
- [ ] Connections to downstream folders are maintained
- [ ] Work is complete — no stubs, no placeholders

---
*If instructions are unclear, ask for clarification. Do not guess. Smart Folders are explicit — if something is not stated, it is not permitted.*