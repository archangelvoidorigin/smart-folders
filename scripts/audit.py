#!/usr/bin/env python3
"""
Smart Folder Audit
Analyzes token usage and efficiency across all smart folders.

Usage:
  python scripts/audit.py [folder_path] [--output report.json]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

BUDGET_THRESHOLDS = {"low": 4000, "medium": 8000, "high": 15000, "very_high": 25000}


def analyze(folder: Path) -> dict | None:
    if not folder.exists():
        return None

    settings_file = folder / "settings.json"
    settings = {}
    if settings_file.exists():
        try:
            settings = json.loads(settings_file.read_text())
        except json.JSONDecodeError:
            pass

    boundaries = settings.get("boundaries", {})
    token_budget = boundaries.get("token_budget", 8000)
    file_limit = boundaries.get("file_limit", 500)

    # Count visible files (excluding hidden and common noise)
    file_count = sum(
        1 for f in folder.iterdir()
        if f.is_file() and not f.name.startswith(".")
    )

    # Estimate tokens from smart-folder.md content
    smart = folder / "smart-folder.md"
    content_tokens = len(smart.read_text()) // 4 if smart.exists() else 0

    ignore_count = 0
    smartignore = folder / ".smartignore"
    if smartignore.exists():
        ignore_count = sum(
            1 for line in smartignore.read_text().splitlines()
            if line.strip() and not line.startswith("#")
        )

    # Efficiency score (100 = optimal)
    efficiency = 100
    if token_budget > BUDGET_THRESHOLDS["very_high"]:
        efficiency -= 30
    elif token_budget > BUDGET_THRESHOLDS["high"]:
        efficiency -= 20
    elif token_budget > BUDGET_THRESHOLDS["medium"]:
        efficiency -= 10

    if not smartignore.exists():
        efficiency -= 15
    if not settings_file.exists():
        efficiency -= 25
    if file_count > file_limit:
        efficiency -= 20

    efficiency = max(0, min(100, efficiency))

    return {
        "path": str(folder),
        "name": folder.name,
        "token_budget": token_budget,
        "file_limit": file_limit,
        "file_count": file_count,
        "content_tokens": content_tokens,
        "ignore_patterns": ignore_count,
        "has_settings": settings_file.exists(),
        "has_smartignore": smartignore.exists(),
        "has_laws": (folder / "laws").exists(),
        "efficiency": efficiency,
    }


def eff_color(score: int) -> str:
    if score >= 80:
        return f"\033[92m{score}%\033[0m"
    elif score >= 60:
        return f"\033[93m{score}%\033[0m"
    return f"\033[91m{score}%\033[0m"


def print_audit(results: list):
    if not results:
        print("No smart folders found.")
        return

    total_budget = sum(r["token_budget"] for r in results)
    total_files = sum(r["file_count"] for r in results)
    avg_eff = sum(r["efficiency"] for r in results) / len(results)

    print(f"\n{'=' * 70}")
    print("SMART FOLDER AUDIT")
    print(f"{'=' * 70}")
    print(f"  Folders : {len(results)}")
    print(f"  Tokens  : {total_budget:,} total budget")
    print(f"  Files   : {total_files} (counted)")
    print(f"  Avg eff : {avg_eff:.0f}%")
    print(f"{'=' * 70}\n")

    for r in results:
        print(f"  {r['name']}  ({r['path']})")
        print(f"    token_budget : {r['token_budget']:,}  |  file_limit : {r['file_limit']}  |  actual files : {r['file_count']}")
        print(f"    settings : {'yes' if r['has_settings'] else 'NO'}  |  .smartignore : {'yes' if r['has_smartignore'] else 'NO'}  |  laws/ : {'yes' if r['has_laws'] else 'NO'}")
        print(f"    efficiency   : {eff_color(r['efficiency'])}")

        if r["token_budget"] > BUDGET_THRESHOLDS["high"]:
            print(f"    WARN  High token budget — consider reducing to 8k–12k")
        if not r["has_smartignore"]:
            print(f"    WARN  No .smartignore — cognitive boundaries not enforced")
        if not r["has_settings"]:
            print(f"    WARN  No settings.json — using defaults everywhere")
        if r["file_count"] > r["file_limit"]:
            print(f"    WARN  {r['file_count']} files exceed limit of {r['file_limit']}")
        print()

    # Suggestions
    issues = {
        "high token budget (>15k)": [r for r in results if r["token_budget"] > BUDGET_THRESHOLDS["high"]],
        "missing .smartignore": [r for r in results if not r["has_smartignore"]],
        "missing settings.json": [r for r in results if not r["has_settings"]],
        "file count exceeds limit": [r for r in results if r["file_count"] > r["file_limit"]],
        "low efficiency (<60%)": [r for r in results if r["efficiency"] < 60],
    }
    has_issues = any(v for v in issues.values())
    if has_issues:
        print("Suggestions:")
        for label, affected in issues.items():
            if affected:
                names = ", ".join(r["name"] for r in affected[:3])
                suffix = f" (and {len(affected) - 3} more)" if len(affected) > 3 else ""
                print(f"  - {len(affected)} folder(s) with {label}: {names}{suffix}")
    else:
        print("No optimization suggestions — folders are well configured.")

    print(f"\n{'=' * 70}")


def main():
    parser = argparse.ArgumentParser(description="Audit Smart Folder token usage")
    parser.add_argument("folder", nargs="?", default=".", help="Root folder to audit")
    parser.add_argument("--output", "-o", help="Write JSON report to file")
    args = parser.parse_args()

    root = Path(args.folder).resolve()
    results = [
        r for p in root.rglob("smart-folder.md")
        if (r := analyze(p.parent)) is not None
    ]

    if not results:
        print("No smart folders found. Run: bash scripts/init.sh")
        return 0

    print_audit(results)

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
