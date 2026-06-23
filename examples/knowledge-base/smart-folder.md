# Smart Folder: Knowledge Base

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

## Context
- **Parent folder**: ../../smart-folder.md
- **Child folders**:
  - `ai-agents/` — Research on specific agent frameworks and tools
  - `tools/` — Tool comparisons, benchmarks, and documentation
  - `patterns/` — Reusable patterns and architectures
  - `research/` — Raw research and unprocessed sources
- **Related folders**: None (this folder is a source, not a consumer)
- **Tools available**: search, summarize, compare, cross-reference

## Connections
- **Feeds into**: `../web-app/`, `../api-service/`
- **Receives from**: External research, user-provided documents
- **Siblings**: None at this level

## Laws
- [ ] Never: delete existing research documents
- [ ] Never: add content without a source reference
- [ ] Always: update index.md when adding new content
- [ ] Always: assign a quality score (1–10) in the metadata header
- [ ] If: a document's quality score is below 7, mark it as draft and note why

## Metadata
- **Created**: 2026-06-23
- **Author**: ArchangelVoidOrigin
- **Version**: 1
- **Quality score**: 9
- **Last modified**: 2026-06-23
