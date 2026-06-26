# Smart Folder: {{name}}

## Purpose
[Describe what this folder contains and what it does — be specific]

## Role
- **Name**: {{role}}
- **Description**: [What this folder's function is in the system]
- **Level**: 0
- **Depth**: {{depth}}

## Scope
**CAN do**:
- [What agents are allowed to do here]

**CANNOT do**:
- [What agents must never do here]

## Boundaries
- **CAN see**: ["*.md", "*.json", "*.py", "*.js", "*.ts"]
- **CANNOT see**: ["*.log", "node_modules/", ".cache/", "*.tmp", "secrets/"]
- **Token budget**: 8000
- **File limit**: 500

## Instructions
[Step-by-step guidance for working in this folder]

## Context
- **Parent folder**: [relative path to parent smart-folder.md or "root"]
- **Child folders**: [list sub-folders with one-line purpose each]
- **Related folders**: [other folders this one depends on]

## Connections
- **Feeds into**: [folders that consume output from this one]
- **Receives from**: [folders this one depends on for input]

## Laws
- [ ] Never: [what agents must NEVER do]
- [ ] Always: [what agents must ALWAYS do]

## Metadata
- **Created**: {{date}}
- **Author**: [your name]
- **Version**: 1
