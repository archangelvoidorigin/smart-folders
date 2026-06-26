from __future__ import annotations

import json
from pathlib import Path

from smartfolders.core import Folder, scan
from smartfolders.schema import load_roles, load_bounds

BUDGET_THRESHOLDS = {"low": 4000, "medium": 8000, "high": 15000, "very_high": 25000}
ADAPTER_FILES = {"AGENTS.md", "CLAUDE.md", "GEMINI.md", "CURSOR.md", "KILO.md", "AIDER.md"}
REQUIRED_SMART_SECTIONS = {"Purpose", "Role", "Scope", "Boundaries", "Instructions"}
RESERVED_DIRS = {"laws", "chronicles", "adapters"}

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


def colored(role: str, text: str | None = None) -> str:
    c = ROLE_COLORS.get(role, ROLE_COLORS["Custom"])
    r = ROLE_COLORS["_reset"]
    return f"{c}{text or role}{r}"


def eff_color(score: int) -> str:
    if score >= 80:
        return f"\033[92m{score}%\033[0m"
    elif score >= 60:
        return f"\033[93m{score}%\033[0m"
    return f"\033[91m{score}%\033[0m"


def validate_folder(folder_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    valid_roles = load_roles()
    bounds = load_bounds()

    if not folder_path.exists():
        errors.append(f"Folder does not exist: {folder_path}")
        return errors, warnings

    smart = folder_path / "smart-folder.md"
    if not smart.exists():
        errors.append("Missing smart-folder.md")
    else:
        content = smart.read_text()
        for section in REQUIRED_SMART_SECTIONS:
            if f"## {section}" not in content:
                warnings.append(f"smart-folder.md missing section: {section}")

    settings_file = folder_path / "settings.json"
    settings: dict = {}
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
                elif role not in valid_roles:
                    errors.append(f"settings.json folder.role is invalid: '{role}'")

            boundaries = settings.get("boundaries", {})
            if not boundaries:
                errors.append("settings.json missing 'boundaries' section")
            else:
                if "can_see" not in boundaries:
                    warnings.append("settings.json boundaries missing 'can_see'")
                if "cannot_see" not in boundaries:
                    warnings.append("settings.json boundaries missing 'cannot_see'")
                bmin, bmax = bounds["token_budget"]
                budget = boundaries.get("token_budget", 8000)
                if not (bmin <= budget <= bmax):
                    errors.append(f"settings.json token_budget out of range [{bmin}–{bmax}]: {budget}")
                lmin, lmax = bounds["file_limit"]
                limit = boundaries.get("file_limit", 500)
                if not (lmin <= limit <= lmax):
                    errors.append(f"settings.json file_limit out of range [{lmin}–{lmax}]: {limit}")

    if not (folder_path / ".smartignore").exists():
        warnings.append("Missing .smartignore (optional but recommended)")

    laws_dir = folder_path / "laws"
    if not laws_dir.exists():
        warnings.append("Missing laws/ directory (optional for Level 1–2)")
    else:
        law_files = list(laws_dir.glob("*.md"))
        if not law_files:
            warnings.append("laws/ exists but contains no .md files")

    for child in folder_path.iterdir():
        if child.is_dir() and not child.name.startswith(".") and child.name not in RESERVED_DIRS:
            child_smart = child / "smart-folder.md"
            if not child_smart.exists():
                warnings.append(f"Child folder '{child.name}' has no smart-folder.md")
            else:
                text = child_smart.read_text().lower()
                if "parent" not in text:
                    warnings.append(f"Child folder '{child.name}/smart-folder.md' has no parent reference")

    found = [a for a in ADAPTER_FILES if (folder_path / a).exists()]
    if not found:
        warnings.append("No adapter file found (AGENTS.md, CLAUDE.md, etc.)")

    return errors, warnings


def audit_folder(folder: Folder) -> dict:
    efficiency = 100
    if folder.token_budget > BUDGET_THRESHOLDS["very_high"]:
        efficiency -= 30
    elif folder.token_budget > BUDGET_THRESHOLDS["high"]:
        efficiency -= 20
    elif folder.token_budget > BUDGET_THRESHOLDS["medium"]:
        efficiency -= 10

    if not folder.has_ignore:
        efficiency -= 15
    if not folder.has_settings:
        efficiency -= 25
    if folder.file_count > folder.file_limit:
        efficiency -= 20

    efficiency = max(0, min(100, efficiency))

    return {
        "path": str(folder.path),
        "name": folder.name,
        "token_budget": folder.token_budget,
        "file_limit": folder.file_limit,
        "file_count": folder.file_count,
        "has_settings": folder.has_settings,
        "has_smartignore": folder.has_ignore,
        "has_laws": folder.has_laws,
        "efficiency": efficiency,
    }


def audit_all(root: Path) -> list[dict]:
    folders = scan(root)
    return [audit_folder(f) for f in folders]


def print_audit(results: list[dict]) -> str:
    if not results:
        return "No smart folders found."

    lines: list[str] = []
    total_budget = sum(r["token_budget"] for r in results)
    total_files = sum(r["file_count"] for r in results)
    avg_eff = sum(r["efficiency"] for r in results) / len(results)

    lines.append("=" * 70)
    lines.append("SMART FOLDER AUDIT")
    lines.append("=" * 70)
    lines.append(f"  Folders : {len(results)}")
    lines.append(f"  Tokens  : {total_budget:,} total budget")
    lines.append(f"  Files   : {total_files} (counted)")
    lines.append(f"  Avg eff : {avg_eff:.0f}%")
    lines.append("=" * 70)
    lines.append("")

    for r in results:
        eff = eff_color(r["efficiency"])
        lines.append(f"  {r['name']}  ({r['path']})")
        lines.append(f"    token_budget : {r['token_budget']:,}  |  file_limit : {r['file_limit']}  |  actual files : {r['file_count']}")
        lines.append(f"    settings : {'yes' if r['has_settings'] else 'NO'}  |  .smartignore : {'yes' if r['has_smartignore'] else 'NO'}  |  laws/ : {'yes' if r['has_laws'] else 'NO'}")
        lines.append(f"    efficiency   : {eff}")

        if r["token_budget"] > BUDGET_THRESHOLDS["high"]:
            lines.append("    WARN  High token budget -- consider reducing to 8k-12k")
        if not r["has_smartignore"]:
            lines.append("    WARN  No .smartignore -- cognitive boundaries not enforced")
        if not r["has_settings"]:
            lines.append("    WARN  No settings.json -- using defaults everywhere")
        if r["file_count"] > r["file_limit"]:
            lines.append(f"    WARN  {r['file_count']} files exceed limit of {r['file_limit']}")
        lines.append("")

    issues = {
        "high token budget (>15k)": [r for r in results if r["token_budget"] > BUDGET_THRESHOLDS["high"]],
        "missing .smartignore": [r for r in results if not r["has_smartignore"]],
        "missing settings.json": [r for r in results if not r["has_settings"]],
        "file count exceeds limit": [r for r in results if r["file_count"] > r["file_limit"]],
        "low efficiency (<60%)": [r for r in results if r["efficiency"] < 60],
    }
    has_issues = any(v for v in issues.values())
    if has_issues:
        lines.append("Suggestions:")
        for label, affected in issues.items():
            if affected:
                names = ", ".join(r["name"] for r in affected[:3])
                suffix = f" (and {len(affected) - 3} more)" if len(affected) > 3 else ""
                lines.append(f"  - {len(affected)} folder(s) with {label}: {names}{suffix}")
    else:
        lines.append("No optimization suggestions -- folders are well configured.")

    lines.append("")
    lines.append("=" * 70)
    return "\n".join(lines)


def build_map(root: Path) -> list[dict]:
    folders = scan(root)
    result = []
    for f in folders:
        result.append({
            "path": f.relative_path,
            "name": f.name,
            "role": f.role,
            "depth": f.depth,
            "settings": f.settings,
        })
    return sorted(result, key=lambda x: x["path"])


def render_tree(folders: list[dict], root: Path) -> str:
    lines: list[str] = []
    lines.append("")
    lines.append("=" * 60)
    lines.append("SMART FOLDER MAP")
    lines.append("=" * 60)
    lines.append(f"Root: {root}")
    lines.append(f"Folders: {len(folders)}")
    lines.append("")

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
    return "\n".join(lines)


def render_stats(folders: list[dict]) -> str:
    if not folders:
        return ""
    lines: list[str] = []
    lines.append("")
    lines.append("=" * 60)
    lines.append("STATISTICS")
    lines.append("=" * 60)

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
    return "\n".join(lines)


def render_connections(folders: list[dict]) -> str:
    lines: list[str] = []
    lines.append("")
    lines.append("=" * 60)
    lines.append("CONNECTIONS")
    lines.append("=" * 60)
    lines.append("")

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
    return "\n".join(lines)
