#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from smartfolders.ops import build_map, render_tree, render_stats, render_connections


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

    folders = build_map(root)
    if not folders:
        print(f"No smart folders found in {root}")
        print("Run: bash scripts/init.sh to create one")
        return 0

    output_parts = [render_tree(folders, root)]
    if args.stats:
        output_parts.append(render_stats(folders))
    if args.connections:
        output_parts.append(render_connections(folders))

    result = "\n".join(output_parts)

    if args.output:
        Path(args.output).write_text(result)
        print(f"Map written to: {args.output}")
    else:
        print(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
