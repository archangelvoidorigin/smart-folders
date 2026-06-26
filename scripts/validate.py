#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from smartfolders.ops import validate_folder


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
    parser = argparse.ArgumentParser(description="Validate Smart Folder structure")
    parser.add_argument("folder", nargs="?", default=".", help="Folder to validate")
    parser.add_argument("--recursive", "-r", action="store_true")
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
