#!/usr/bin/env python3
"""
Smart Folder Converter
Converts smart-folder.md to agent-specific instruction files.

Usage:
  python scripts/convert.py [folder_path] [--agent all|claude|gemini|cursor|kilo|aider|agents]
"""

from __future__ import annotations

import argparse
from pathlib import Path

AGENT_FILES = {
    "agents":  "AGENTS.md",
    "claude":  "CLAUDE.md",
    "gemini":  "GEMINI.md",
    "cursor":  "CURSOR.md",
    "kilo":    "KILO.md",
    "aider":   "AIDER.md",
}

AGENT_HEADERS = {
    "agents": "# AGENTS.md — Smart Folder Adapter (Universal)",
    "claude": "# CLAUDE.md — Smart Folder Adapter (Claude)",
    "gemini": "# GEMINI.md — Smart Folder Adapter (Gemini)",
    "cursor": "# CURSOR.md — Smart Folder Adapter (Cursor)",
    "kilo":   "# KILO.md — Smart Folder Adapter (Kilo Code)",
    "aider":  "# AIDER.md — Smart Folder Adapter (Aider)",
}

AGENT_TIPS = {
    "claude": [
        "- Use **extended thinking** for complex reasoning and architecture decisions",
        "- Create **artifacts** for substantial file outputs",
        "- Use **vision** when analyzing images or diagrams in this folder",
        "- Respect token_budget even with large context — focused context produces better output",
    ],
    "gemini": [
        "- Use **search grounding** for research tasks — do not rely on cached knowledge",
        "- Use **code execution** to verify data analysis results",
        "- Use **multimodal** capabilities for visual, audio, or video content",
        "- Respect token_budget even with 1M+ context window",
    ],
    "cursor": [
        "- Use **Composer** for all multi-file changes",
        "- Use **@ mentions** to load only the files this folder's instructions reference",
        "- In **Agent Mode**, stay strictly within this folder's scope",
        "- Respect context limits — do not load the entire codebase",
    ],
    "kilo": [
        "- Generate **complete, working implementations** — no stubs",
        "- Write **tests** for all code you create or modify",
        "- Follow the coding conventions defined in this folder's instructions",
        "- Respect token_budget — load only what is needed",
    ],
    "aider": [
        "- Use `/add` and `/drop` to keep context limited to this folder's files",
        "- Use **Architect mode** for design decisions before implementing",
        "- **Commit** every meaningful change with a descriptive message",
        "- Explain what you are about to do before making changes",
    ],
    "agents": [
        "- Read this file first, then smart-folder.md",
        "- Follow hierarchical instruction resolution — parent rules apply to children",
        "- Respect all boundaries and laws",
        "- Document significant changes",
    ],
}

HIERARCHY_NOTE = """
## Folder Hierarchy

Smart Folders use hierarchical instruction resolution:
- **Parent** folder instructions apply to all children unless explicitly overridden
- **Child** folder instructions add specificity and narrow scope
- **Closer instructions win** — child rules take precedence in conflicts
- **Laws are absolute** — no folder can override a law from an ancestor
""".strip()

READING_ORDER = """
## How to Navigate This Folder

1. Read this adapter file first (you are doing this now)
2. Read `smart-folder.md` — purpose, scope, role, and specific instructions
3. Read `settings.json` — boundaries, token budget, and agent configuration
4. Read `.smartignore` — files and directories that are off-limits
5. Read all files in `laws/` before making any changes
""".strip()

QUALITY_CHECKLIST = """
## Quality Checklist

Before finishing work in this folder:
- [ ] Output follows the folder's instructions and stated purpose
- [ ] All laws are respected
- [ ] Token budget is not exceeded
- [ ] Connections to downstream folders are maintained
- [ ] Work is complete — no stubs, no placeholders
""".strip()


def parse_sections(content: str) -> dict:
    sections = {}
    current = None
    lines = []
    for line in content.splitlines():
        if line.startswith("## "):
            if current:
                sections[current] = "\n".join(lines).strip()
            current = line[3:].strip()
            lines = []
        elif current:
            lines.append(line)
    if current:
        sections[current] = "\n".join(lines).strip()
    return sections


def build_adapter(smart_content: str, agent: str) -> str:
    sections = parse_sections(smart_content)
    header = AGENT_HEADERS[agent]
    tips = AGENT_TIPS.get(agent, [])
    filename = AGENT_FILES[agent]

    parts = [header, ""]
    parts.append("This folder is configured with the Smart Folder system. Read this file first.")
    parts.append("")

    if tips:
        parts.append(f"## {agent.capitalize()} Configuration" if agent != "agents" else "## Configuration")
        parts.extend(tips)
        parts.append("")

    parts.append(READING_ORDER)
    parts.append("")
    parts.append(HIERARCHY_NOTE)
    parts.append("")

    # Include key sections from smart-folder.md
    for section in ("Purpose", "Role", "Scope", "Boundaries", "Instructions", "Laws"):
        if section in sections and sections[section]:
            parts.append(f"## {section}")
            parts.append(sections[section])
            parts.append("")

    parts.append(QUALITY_CHECKLIST)
    parts.append("")
    parts.append("---")
    parts.append("*If instructions are unclear, ask for clarification. Do not guess. Smart Folders are explicit — if something is not stated, it is not permitted.*")

    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Convert smart-folder.md to agent formats")
    parser.add_argument("folder", nargs="?", default=".", help="Folder path")
    parser.add_argument("--agent", "-a", default="all",
                        choices=["all"] + list(AGENT_FILES.keys()),
                        help="Target agent (default: all)")
    args = parser.parse_args()

    folder = Path(args.folder)
    smart = folder / "smart-folder.md"

    if not smart.exists():
        print(f"Error: smart-folder.md not found in {folder}")
        return 1

    content = smart.read_text()
    agents = list(AGENT_FILES.keys()) if args.agent == "all" else [args.agent]

    for agent in agents:
        output_path = folder / AGENT_FILES[agent]
        output_path.write_text(build_adapter(content, agent))
        print(f"  [ok] {AGENT_FILES[agent]}")

    print(f"\nConverted to {len(agents)} format(s) in {folder}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
