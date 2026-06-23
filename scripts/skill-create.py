#!/usr/bin/env python3
"""
Smart Folder Skill: Folder Creator
Interactive assistant for creating properly structured Smart Folders.

Usage:
  python scripts/skill-create.py                              # interactive
  python scripts/skill-create.py --name my-folder --role Creator --depth medium
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROLES = {
    "1": ("Knowledge Keeper", "Stores and organizes information"),
    "2": ("Creator",          "Builds and creates things"),
    "3": ("Architect",        "Designs systems and schemas"),
    "4": ("Connector",        "Links tools and workflows"),
    "5": ("Chronicler",       "Documents everything"),
    "6": ("Enabler",          "Provides tools and utilities"),
    "7": ("Archive",          "Preserves history"),
    "8": ("Staging",          "Experiments safely"),
    "9": ("Custom",           "Define your own role"),
}

DEPTHS = {
    "1": ("shallow", "1–2 levels, simple projects"),
    "2": ("medium",  "3–4 levels, standard projects"),
    "3": ("deep",    "5+ levels, complex systems"),
}

TODAY = date.today().isoformat()


def ask(prompt: str, default: str = None) -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        val = input(f"{prompt}{suffix}: ").strip()
        if val:
            return val
        if default:
            return default
        print("Required.")


def choose(prompt: str, options: dict, default: str = None) -> str:
    print(f"\n{prompt}")
    for key, (label, desc) in options.items():
        print(f"  {key}. {label} — {desc}")
    suffix = f" [{default}]" if default else ""
    while True:
        val = input(f"Choice (1–{len(options)}){suffix}: ").strip() or default
        if val in options:
            return options[val][0]
        print(f"Enter a number 1–{len(options)}.")


def ask_agents() -> list:
    print("\nWhich agents will use this folder?")
    print("  Options: claude, gemini, codex, cursor, kilo, aider  (comma-separated, or 'all')")
    val = input("Agents [all]: ").strip().lower()
    if not val or val == "all":
        return ["claude", "gemini", "codex", "cursor", "kilo", "aider"]
    return [a.strip() for a in val.split(",") if a.strip()]


def create(name: str, role: str, depth: str, purpose: str, agents: list) -> bool:
    folder = Path(name)

    if folder.exists():
        confirm = input(f"\nFolder '{name}' already exists. Overwrite? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return False

    print(f"\nCreating: {name}/")
    folder.mkdir(parents=True, exist_ok=True)

    # smart-folder.md
    (folder / "smart-folder.md").write_text(f"""# Smart Folder: {name}

## Purpose
{purpose}

## Role
- **Name**: {role}
- **Description**: [What this folder's function is in the system]
- **Level**: 0
- **Depth**: {depth}

## Scope
**CAN do**:
- [What agents are allowed to do here]

**CANNOT do**:
- [What agents must never do here]

## Boundaries
- **CAN see**: ["*.md", "*.json", "*.py", "*.js"]
- **CANNOT see**: ["*.log", "node_modules/", ".cache/", "*.tmp"]
- **Token budget**: 8000
- **File limit**: 500

## Instructions
[Step-by-step guidance for working in this folder]

## Context
- **Parent folder**: [relative path to parent or "root"]
- **Child folders**: [list sub-folders with purpose]
- **Related folders**: [other folders this depends on]

## Connections
- **Feeds into**: []
- **Receives from**: []

## Laws
- [ ] Never: [absolute prohibitions]
- [ ] Always: [absolute requirements]

## Metadata
- **Created**: {TODAY}
- **Author**: [your name]
- **Version**: 1
""")
    print("  [ok] smart-folder.md")

    # settings.json
    (folder / "settings.json").write_text(json.dumps({
        "folder": {
            "name": name, "role": role, "sub_role": None,
            "level": 0, "depth": depth, "purpose": purpose
        },
        "boundaries": {
            "can_see": ["*.md", "*.json", "*.py", "*.js", "*.ts"],
            "cannot_see": ["*.log", "node_modules/", ".cache/", "*.tmp", ".git/"],
            "token_budget": 8000, "file_limit": 500, "depth_limit": 5
        },
        "connections": {
            "parent": None, "children": [], "siblings": [],
            "tools": ["search", "summarize"], "feeds_into": [], "receives_from": []
        },
        "agents": {"allowed": agents, "preferred": "claude", "restricted": []},
        "metadata": {
            "created": TODAY, "author": "[your name]",
            "last_modified": TODAY, "quality_score": 1.0, "version": 1
        }
    }, indent=2))
    print("  [ok] settings.json")

    # .smartignore
    (folder / ".smartignore").write_text("""# .smartignore — Cognitive Boundaries
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
.env
.env.*
*.secret
*.key
credentials/
secrets/
.vscode/
.idea/
*.swp
*.swo
.DS_Store
*.zip
*.tar
*.gz
""")
    print("  [ok] .smartignore")

    # laws/
    laws = folder / "laws"
    laws.mkdir(exist_ok=True)
    (laws / "never-rules.md").write_text("""# Never Rules
- Never delete smart-folder.md, settings.json, or laws/
- Never access files in .smartignore or settings.json cannot_see
- Never exceed the token_budget
- Never create files outside this folder's purpose
- Never fabricate content, paths, or API signatures
""")
    (laws / "always-rules.md").write_text("""# Always Rules
- Always read smart-folder.md before doing any work
- Always check settings.json for boundaries
- Always read laws/ before making changes
- Always document significant changes
- Always ask for clarification rather than guessing
""")
    print("  [ok] laws/")

    # Sub-folders
    subs = {"deep": 3, "medium": 2, "shallow": 0}.get(depth, 0)
    for i in range(1, subs + 1):
        sub = folder / f"sub-folder-{i}"
        sub.mkdir(exist_ok=True)
        (sub / "smart-folder.md").write_text(f"""# Smart Folder: sub-folder-{i}

## Purpose
[Sub-folder purpose]

## Role
- **Name**: [Inherited from parent: {role}]
- **Sub-role**: [Specific to this sub-folder]

## Scope
[What this sub-folder does]

## Instructions
[Specific instructions]

## Context
- **Parent**: ../smart-folder.md
""")
        print(f"  [ok] sub-folder-{i}/")

    # chronicles/
    chron = folder / "chronicles"
    chron.mkdir(exist_ok=True)
    (chron / "README.md").write_text("""# Chronicles

Document everything significant:

```
[Session YYYY-MM-DD]
What happened:
Why it matters:
What was learned:
What changed:
```
""")
    print("  [ok] chronicles/")

    print(f"\nDone. Smart Folder created at: {folder.resolve()}")
    print(f"\nNext: python scripts/validate.py {folder}/")
    return True


def interactive():
    print("\nSmart Folder Creator")
    print("=" * 40)

    name = ask("Folder name")
    role = choose("Role:", ROLES, default="2")
    if role == "Custom":
        role = ask("Custom role name")
    purpose = ask("Purpose (one sentence)")
    depth = choose("Depth:", DEPTHS, default="2")
    agents = ask_agents()

    print(f"\nSummary")
    print(f"  name    : {name}")
    print(f"  role    : {role}")
    print(f"  purpose : {purpose}")
    print(f"  depth   : {depth}")
    print(f"  agents  : {', '.join(agents)}")

    if input("\nCreate? [Y/n]: ").strip().lower() in ("", "y", "yes"):
        create(name, role, depth, purpose, agents)
    else:
        print("Cancelled.")


def main():
    parser = argparse.ArgumentParser(description="Interactive Smart Folder Creator")
    parser.add_argument("--name",    "-n", help="Folder name")
    parser.add_argument("--role",    "-r", default="Creator")
    parser.add_argument("--depth",   "-d", default="medium", choices=["shallow", "medium", "deep"])
    parser.add_argument("--purpose", "-p", default="[Describe purpose]")
    parser.add_argument("--agents",  "-a", default="claude,gemini,codex,cursor,kilo,aider")
    args = parser.parse_args()

    if args.name:
        create(args.name, args.role, args.depth, args.purpose, args.agents.split(","))
    else:
        interactive()


if __name__ == "__main__":
    main()
