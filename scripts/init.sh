#!/usr/bin/env bash
# Smart Folder Init Script
# Creates a smart folder structure in any directory.
# Usage: bash scripts/init.sh [folder_name] [role] [depth]
# Example: bash scripts/init.sh my-project Creator medium

set -e

FOLDER_NAME=${1:-"my-folder"}
ROLE=${2:-"Custom"}
DEPTH=${3:-"medium"}
DATE=$(date +%Y-%m-%d)

VALID_ROLES="Knowledge Keeper|Creator|Architect|Connector|Chronicler|Enabler|Archive|Staging|Custom"
VALID_DEPTHS="shallow|medium|deep"

echo "Smart Folder Init"
echo "  Folder : $FOLDER_NAME"
echo "  Role   : $ROLE"
echo "  Depth  : $DEPTH"
echo ""

mkdir -p "$FOLDER_NAME"
cd "$FOLDER_NAME"

# smart-folder.md — use unquoted heredoc so DATE expands
cat > smart-folder.md << EOF
# Smart Folder: $FOLDER_NAME

## Purpose
[Describe what this folder contains and what it does — be specific]

## Role
- **Name**: $ROLE
- **Description**: [What this folder's function is in the system]
- **Level**: 0
- **Depth**: $DEPTH

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
- **Created**: $DATE
- **Author**: [your name]
- **Version**: 1
EOF

echo "  [ok] smart-folder.md"

# settings.json
cat > settings.json << EOF
{
  "folder": {
    "name": "$FOLDER_NAME",
    "role": "$ROLE",
    "sub_role": null,
    "level": 0,
    "depth": "$DEPTH",
    "purpose": "[Describe what this folder does]"
  },
  "boundaries": {
    "can_see": ["*.md", "*.json", "*.py", "*.js", "*.ts"],
    "cannot_see": ["*.log", "node_modules/", ".cache/", "*.tmp", ".git/", "secrets/"],
    "token_budget": 8000,
    "file_limit": 500,
    "depth_limit": 5
  },
  "connections": {
    "parent": null,
    "children": [],
    "siblings": [],
    "tools": ["search", "summarize"],
    "feeds_into": [],
    "receives_from": []
  },
  "agents": {
    "allowed": ["claude", "gemini", "codex", "cursor", "kilo", "aider"],
    "preferred": "claude",
    "restricted": []
  },
  "metadata": {
    "created": "$DATE",
    "author": "[your name]",
    "last_modified": "$DATE",
    "quality_score": 1.0,
    "version": 1
  }
}
EOF

echo "  [ok] settings.json"

# .smartignore
cat > .smartignore << 'EOF'
# .smartignore — Cognitive Boundaries
*.log
*.tmp
*.temp
*.cache
.cache/
node_modules/
vendor/
dist/
build/
*.lock
.git/
.svn/
.hg/
.env
.env.*
*.secret
*.key
*.pem
*.cert
credentials/
secrets/
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
*.zip
*.tar
*.gz
*.rar
*.7z
*.db
*.sqlite
*.sqlite3
EOF

echo "  [ok] .smartignore"

# laws/
mkdir -p laws

cat > laws/never-rules.md << 'EOF'
# Never Rules

- Never delete smart-folder.md, settings.json, or the laws/ directory
- Never delete files without explicit user permission
- Never access files listed in .smartignore or settings.json cannot_see
- Never exceed the token_budget in settings.json
- Never create files outside this folder's defined purpose
- Never modify laws/ files without explicit user permission
- Never fabricate content, paths, or API signatures
EOF

cat > laws/always-rules.md << 'EOF'
# Always Rules

- Always read smart-folder.md before doing any work
- Always check settings.json for boundaries and token budget
- Always read laws/ before making changes
- Always stay within this folder's stated purpose
- Always document significant changes
- Always ask for clarification rather than guessing
EOF

echo "  [ok] laws/never-rules.md"
echo "  [ok] laws/always-rules.md"

# Sub-folders based on depth
if [ "$DEPTH" = "deep" ]; then
    SUBS="sub-folder-1 sub-folder-2 sub-folder-3"
elif [ "$DEPTH" = "medium" ]; then
    SUBS="sub-folder-1 sub-folder-2"
else
    SUBS=""
fi

for SUB in $SUBS; do
    mkdir -p "$SUB"
    cat > "$SUB/smart-folder.md" << EOF
# Smart Folder: $SUB

## Purpose
[Sub-folder purpose]

## Role
- **Name**: [Inherited from parent: $ROLE]
- **Sub-role**: [Specific to this sub-folder]

## Scope
[What this sub-folder does]

## Instructions
[Specific instructions for this sub-folder]

## Context
- **Parent**: ../smart-folder.md
- **Siblings**: [other sub-folders at this level]
EOF
    echo "  [ok] $SUB/smart-folder.md"
done

# chronicles/
mkdir -p chronicles
cat > chronicles/README.md << 'EOF'
# Chronicles

Document everything that happens in this folder using this format:

```
[Session YYYY-MM-DD]
What happened:
Why it matters:
What was learned:
What changed:
```
EOF

echo "  [ok] chronicles/README.md"
echo ""
echo "Done. Smart Folder created at: $(pwd)"
echo ""
echo "Next steps:"
echo "  1. Edit smart-folder.md — define your folder's purpose and instructions"
echo "  2. Edit settings.json  — configure boundaries and connections"
echo "  3. python scripts/validate.py $(pwd)"
