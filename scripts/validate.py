#!/usr/bin/env python3
"""
Smart Folder Validator
Checks folder health: smart-folder.md presence and sections, settings.json schema,
laws, .smartignore, child references, and adapter files.

Usage:
  python scripts/validate.py [folder_path]
  python scripts/validate.py [folder_path] --recursive
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent.parent / "settings-schema.json"

# Defaults used only if settings-schema.json is missing or unreadable.
_FALLBACK_ROLES = {
    "Knowledge Keeper", "Creator", "Architect", "Connector",
    "Chronicler", "Enabler", "Archive", "Staging", "Custom",
}
_FALLBACK_BOUNDS = {"token_budget": (1000, 50000), "file_limit": (10, 10000)}


def _load_schema_rules() -> tuple[set, dict]:
    """Derive valid roles and numeric bounds from settings-schema.json so the
    schema is the single source of truth. Falls back to hardcoded defaults."""
    try:
        schema = json.loads(SCHEMA_PATH.read_text())
        props = schema["properties"]
        roles = set(props["folder"]["properties"]["role"]["enum"])
        bprops = props["boundaries"]["properties"]
        bounds = {
            key: (bprops[key]["minimum"], bprops[key]["maximum"])
            for key in ("token_budget", "file_limit")
        }
        return roles, bounds
    except (OSError, KeyError, json.JSONDecodeError):
        return _FALLBACK_ROLES, dict(_FALLBACK_BOUNDS)


VALID_ROLES, BOUNDS = _load_schema_rules()

ADAPTER_FILES = {"AGENTS.md", "CLAUDE.md", "GEMINI.md", "CURSOR.md", "KILO.md", "AIDER.md"}
REQUIRED_SMART_SECTIONS = {"Purpose", "Role", "Scope", "Boundaries", "Instructions"}

# Reserved sub-directories that are part of a folder, not child smart folders.
RESERVED_DIRS = {"laws", "chronicles", "adapters"}


def validate_folder(folder_path: Path) -> tuple[list, list]:
    errors = []
    warnings = []

    if not folder_path.exists():
        errors.append(f"Folder does not exist: {folder_path}")
        return errors, warnings

    # smart-folder.md
    smart = folder_path / "smart-folder.md"
    if not smart.exists():
        errors.append("Missing smart-folder.md")
    else:
        content = smart.read_text()
        for section in REQUIRED_SMART_SECTIONS:
            if f"## {section}" not in content:
                warnings.append(f"smart-folder.md missing section: {section}")

    # settings.json
    settings_file = folder_path / "settings.json"
    settings = {}
    if not settings_file.exists():
        warnings.append("Missing settings.json (optional for Level 1)")
    else:
        try:
            settings = json.loads(settings_file.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"settings.json is not valid JSON: {e}")
            settings = {}

        if settings:
            folder_data = settings.get("folder", {})
            if not folder_data:
                errors.append("settings.json missing 'folder' section")
            else:
                if not folder_data.get("name"):
                    errors.append("settings.json folder.name is missing")
                role = folder_data.get("role")
                if not role:
                    errors.append("settings.json folder.role is missing")
                elif role not in VALID_ROLES:
                    errors.append(f"settings.json folder.role is invalid: '{role}' — must be one of: {', '.join(sorted(VALID_ROLES))}")

            boundaries = settings.get("boundaries", {})
            if not boundaries:
                errors.append("settings.json missing 'boundaries' section")
            else:
                if "can_see" not in boundaries:
                    warnings.append("settings.json boundaries missing 'can_see'")
                if "cannot_see" not in boundaries:
                    warnings.append("settings.json boundaries missing 'cannot_see'")
                bmin, bmax = BOUNDS["token_budget"]
                budget = boundaries.get("token_budget", 8000)
                if not (bmin <= budget <= bmax):
                    errors.append(f"settings.json token_budget out of range [{bmin}–{bmax}]: {budget}")
                lmin, lmax = BOUNDS["file_limit"]
                limit = boundaries.get("file_limit", 500)
                if not (lmin <= limit <= lmax):
                    errors.append(f"settings.json file_limit out of range [{lmin}–{lmax}]: {limit}")

    # .smartignore
    if not (folder_path / ".smartignore").exists():
        warnings.append("Missing .smartignore (optional but recommended)")

    # laws/
    laws_dir = folder_path / "laws"
    if not laws_dir.exists():
        warnings.append("Missing laws/ directory (optional for Level 1–2)")
    else:
        law_files = list(laws_dir.glob("*.md"))
        if not law_files:
            warnings.append("laws/ exists but contains no .md files")

    # Child folders — check for missing smart-folder.md and parent references
    for child in folder_path.iterdir():
        if child.is_dir() and not child.name.startswith(".") and child.name not in RESERVED_DIRS:
            child_smart = child / "smart-folder.md"
            if not child_smart.exists():
                warnings.append(f"Child folder '{child.name}' has no smart-folder.md")
            else:
                text = child_smart.read_text().lower()
                if "parent" not in text:
                    warnings.append(f"Child folder '{child.name}/smart-folder.md' has no parent reference")

    # Adapter files
    found = [a for a in ADAPTER_FILES if (folder_path / a).exists()]
    if not found:
        warnings.append("No adapter file found (AGENTS.md, CLAUDE.md, etc.) — agents may not receive Smart Folder instructions")

    return errors, warnings


def print_result(folder_path: Path, errors: list, warnings: list) -> bool:
    prefix = str(folder_path)
    print(f"\n{prefix}")
    print("-" * min(60, len(prefix) + 2))

    if errors:
        for e in errors:
            print(f"  ERROR   {e}")
    if warnings:
        for w in warnings:
            print(f"  WARN    {w}")
    if not errors and not warnings:
        print("  OK      All checks passed")

    return len(errors) == 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate Smart Folder structure")
    parser.add_argument("folder", nargs="?", default=".", help="Folder to validate")
    parser.add_argument("--recursive", "-r", action="store_true",
                        help="Recursively validate all smart folders under this path")
    args = parser.parse_args()

    root = Path(args.folder).resolve()
    all_passed = True

    if args.recursive:
        folders = [p.parent for p in root.rglob("smart-folder.md")]
        if not folders:
            print(f"No smart folders found under {root}")
            sys.exit(1)
        folders.sort()
    else:
        folders = [root]

    print(f"Validating {len(folders)} folder(s)...")

    for folder in folders:
        errors, warnings = validate_folder(folder)
        passed = print_result(folder, errors, warnings)
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("Result: PASS")
        sys.exit(0)
    else:
        print("Result: FAIL — fix errors above")
        sys.exit(1)


if __name__ == "__main__":
    main()
