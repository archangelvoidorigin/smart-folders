import sys
import argparse
from pathlib import Path

from smartfolders.templates import create_folder_structure


def main():
    parser = argparse.ArgumentParser(description="Smart Folders — init")
    parser.add_argument("command", choices=["init"])
    parser.add_argument("name", nargs="?", default="my-folder")
    parser.add_argument("--role", "-r", default="Custom")
    parser.add_argument("--depth", "-d", default="medium")
    parser.add_argument("--purpose", "-p", default="[Describe purpose]")
    parser.add_argument("--output", "-o", type=Path, default=None)
    args = parser.parse_args()

    if args.command == "init":
        target = create_folder_structure(
            folder_name=args.name,
            role=args.role,
            depth=args.depth,
            purpose=args.purpose,
            output_dir=args.output,
        )
        print(f"Smart Folder created at: {target}")
        print(f"  python scripts/validate.py {target}/")


if __name__ == "__main__":
    main()
