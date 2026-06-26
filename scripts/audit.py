#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from smartfolders.ops import audit_all, print_audit


def main():
    parser = argparse.ArgumentParser(description="Audit Smart Folder token usage")
    parser.add_argument("folder", nargs="?", default=".", help="Root folder to audit")
    parser.add_argument("--output", "-o", help="Write JSON report to file")
    args = parser.parse_args()

    root = Path(args.folder).resolve()
    if not root.exists():
        print(f"Error: folder not found: {root}")
        return 1

    results = audit_all(root)
    if not results:
        print("No smart folders found. Run: bash scripts/init.sh")
        return 0

    print(print_audit(results))

    if args.output:
        report = {
            "summary": {
                "total_folders": len(results),
                "total_token_budget": sum(r["token_budget"] for r in results),
                "average_efficiency": sum(r["efficiency"] for r in results) / len(results),
            },
            "folders": results,
        }
        Path(args.output).write_text(json.dumps(report, indent=2))
        print(f"Report written to: {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
