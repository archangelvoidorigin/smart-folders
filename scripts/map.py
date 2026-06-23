#!/usr/bin/env python3
"""
Smart Folder Map
Generates a visual tree of all smart folders with roles, connections, and stats.

Usage:
  python scripts/map.py [folder_path] [--stats] [--connections] [--output file.txt]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROLE_COLORS = {
    "Knowledge Keeper": "\033[94m",
    "Creator":          "\033[91m",
    "Architect":        "\033[93m",
    "Connector":        "\033[95m",
    "Chronicler":       "\033[92m",
    "Enabler":          "\033[96m",
    "Archive":          "\033[90m",
    "Staging":          "\033[35m",
    "Custom":           "\033[97m",
    "_reset":           "\033[0m",
}


def colored(role: str, text: str = None) -> str:
    c = ROLE_COLORS.get(role, ROLE_COLORS["Custom"])
    r = ROLE_COLORS["_reset"]
    return f"{c}{text or role}{r}"


def load_folder_info(smart_md: Path, root: Path) -> dict:
    folder = smart_md.parent
    relative = str(folder.relative_to(root)) if folder != root else "."

    settings = {}
    settings_file = folder / "settings.json"
    if settings_file.exists():
        try:
            settings = json.loads(settings_file.read_text())
        except json.JSONDecodeError:
            pass

    role = settings.get("folder", {}).get("role", "Custom")

    # Fallback: try to read role from smart-folder.md
    if role == "Custom":
        try:
            for line in smart_md.read_text().splitlines():
                if "**Name**:" in line:
                    candidate = line.split("**Name**:")[1].strip()
                    if candidate in ROLE_COLORS:
                        role = candidate
                    break
        except Exception:
            pass

    return {
        "path": relative,
        "name": folder.name if folder != root else "(root)",
        "role": role,
        "depth": len(folder.relative_to(root).parts),
        "settings": settings,
    }


def find_folders(root: Path) -> list:
    folders = [load_folder_info(p, root) for p in root.rglob("smart-folder.md")]
    return sorted(folders, key=lambda f: f["path"])


def render_tree(folders: list, root: Path) -> list[str]:
    lines = ["", "=" * 60, "SMART FOLDER MAP", "=" * 60, f"Root: {root}", f"Folders: {len(folders)}", ""]

    role_counts: dict[str, int] = {}
    for f in folders:
        role_counts[f["role"]] = role_counts.get(f["role"], 0) + 1

    lines.append("Role distribution:")
    for role, count in sorted(role_counts.items()):
        lines.append(f"  {colored(role)}: {count}")
    lines.append("")
    lines.append("Tree:")
    lines.append("")

    for f in folders:
        depth = f["depth"]
        indent = "  " * depth
        prefix = "└── " if depth > 0 else ""
        role_label = colored(f["role"])
        lines.append(f"{indent}{prefix}{f['name']} [{role_label}]")

        conns = f["settings"].get("connections", {})
        if conns.get("feeds_into"):
            lines.append(f"{indent}{'    ' if depth > 0 else '  '}-> {', '.join(conns['feeds_into'])}")

    lines.append("")
    lines.append("=" * 60)
    return lines


def render_stats(folders: list) -> list[str]:
    if not folders:
        return []

    lines = ["", "=" * 60, "STATISTICS", "=" * 60]

    total = len(folders)
    max_depth = max(f["depth"] for f in folders)
    role_counts: dict[str, int] = {}
    total_tokens = 0

    for f in folders:
        role_counts[f["role"]] = role_counts.get(f["role"], 0) + 1
        total_tokens += f["settings"].get("boundaries", {}).get("token_budget", 8000)

    lines.append(f"Total folders : {total}")
    lines.append(f"Max depth     : {max_depth}")
    lines.append(f"Total tokens  : {total_tokens:,}")
    lines.append(f"Avg tokens    : {total_tokens // total:,}")
    lines.append("")
    lines.append("By role:")
    for role, count in sorted(role_counts.items(), key=lambda x: -x[1]):
        pct = count / total * 100
        lines.append(f"  {colored(role)}: {count} ({pct:.0f}%)")

    lines.append("")
    lines.append("=" * 60)
    return lines


def render_connections(folders: list) -> list[str]:
    lines = ["", "=" * 60, "CONNECTIONS", "=" * 60, ""]

    for f in folders:
        conns = f["settings"].get("connections", {})
        if not any([conns.get("parent"), conns.get("children"), conns.get("feeds_into"), conns.get("receives_from")]):
            continue

        lines.append(f"{f['name']} ({f['path']})")
        if conns.get("parent"):
            lines.append(f"  <- parent      : {conns['parent']}")
        for child in conns.get("children", []):
            lines.append(f"  -> child       : {child}")
        for feed in conns.get("feeds_into", []):
            lines.append(f"  -> feeds into  : {feed}")
        for recv in conns.get("receives_from", []):
            lines.append(f"  <- receives    : {recv}")
        lines.append("")

    lines.append("=" * 60)
    return lines


def main():
    parser = argparse.ArgumentParser(description="Generate Smart Folder map")
    parser.add_argument("folder", nargs="?", default=".", help="Root folder")
    parser.add_argument("--stats", "-s", action="store_true")
    parser.add_argument("--connections", "-c", action="store_true")
    parser.add_argument("--output", "-o", help="Write output to file")
    args = parser.parse_args()

    root = Path(args.folder).resolve()
    if not root.exists():
        print(f"Error: folder not found: {root}")
        return 1

    folders = find_folders(root)
    if not folders:
        print(f"No smart folders found in {root}")
        print("Run: bash scripts/init.sh to create one")
        return 0

    output_lines: list[str] = []
    output_lines.extend(render_tree(folders, root))
    if args.stats:
        output_lines.extend(render_stats(folders))
    if args.connections:
        output_lines.extend(render_connections(folders))

    result = "\n".join(output_lines)

    if args.output:
        Path(args.output).write_text(result)
        print(f"Map written to: {args.output}")
    else:
        print(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
