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
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from smartfolders.templates import create_folder_structure

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
        target = create_folder_structure(name, role, depth, purpose, agents=agents)
        print(f"\nDone. Smart Folder created at: {target}")
        print(f"\nNext: python scripts/validate.py {target}/")
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
        target = create_folder_structure(args.name, args.role, args.depth, args.purpose, agents=args.agents.split(","))
        print(f"Smart Folder created at: {target}")
        print(f"  python scripts/validate.py {target}/")
    else:
        interactive()


if __name__ == "__main__":
    main()
