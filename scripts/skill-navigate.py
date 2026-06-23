#!/usr/bin/env python3
"""
Smart Folder Skill: Navigation Orchestrator
Analyzes a task and guides you to the optimal folder.

Usage:
  python scripts/skill-navigate.py                              # interactive
  python scripts/skill-navigate.py --task "build a button" --agent claude --location .
"""

import argparse
import json
from pathlib import Path

AGENT_STRENGTHS = {
    "claude":  ["reasoning", "analysis", "documentation", "long-form writing"],
    "gemini":  ["multimodal", "search", "coding", "data analysis"],
    "codex":   ["coding", "refactoring", "testing", "code generation"],
    "cursor":  ["multi-file editing", "refactoring", "UI work"],
    "kilo":    ["code generation", "testing", "documentation"],
    "aider":   ["pair programming", "git-based workflow", "architecture"],
}

KEYWORD_MAP = {
    "design":        ["ui", "design", "component", "button", "layout", "color", "style", "css", "visual"],
    "backend":       ["api", "endpoint", "server", "backend", "database", "sql", "query"],
    "frontend":      ["frontend", "react", "vue", "angular", "html", "css", "jsx", "tsx"],
    "testing":       ["test", "testing", "spec", "jest", "pytest", "coverage", "qa"],
    "documentation": ["doc", "document", "readme", "guide", "tutorial", "explain"],
    "architecture":  ["schema", "model", "architecture", "pattern", "design system", "struct"],
    "research":      ["research", "analyze", "study", "investigate", "explore", "find"],
    "data":          ["data", "csv", "json", "transform", "pipeline", "etl", "parse"],
    "deploy":        ["deploy", "infra", "docker", "ci", "cd", "pipeline", "build"],
}

ROLE_KEYWORD_AFFINITY = {
    "Knowledge Keeper": ["research", "documentation", "data"],
    "Creator":          ["design", "frontend", "backend"],
    "Architect":        ["architecture", "backend", "deploy"],
    "Connector":        ["deploy", "data", "backend"],
    "Chronicler":       ["documentation"],
    "Enabler":          ["testing", "deploy"],
    "Archive":          ["documentation", "data"],
    "Staging":          ["research", "design", "architecture"],
}


def find_folders(root: Path) -> list:
    folders = []
    for sm in sorted(root.rglob("smart-folder.md")):
        folder = sm.parent
        settings = {}
        sf = folder / "settings.json"
        if sf.exists():
            try:
                settings = json.loads(sf.read_text())
            except Exception:
                pass

        purpose = ""
        try:
            content = sm.read_text()
            if "## Purpose" in content:
                purpose = content.split("## Purpose")[1].split("##")[0].strip()
        except Exception:
            pass

        folders.append({
            "path":     str(folder.relative_to(root)) if folder != root else ".",
            "name":     folder.name if folder != root else "(root)",
            "purpose":  purpose,
            "settings": settings,
        })
    return folders


def extract_keywords(task: str) -> list:
    task_lower = task.lower()
    return [cat for cat, words in KEYWORD_MAP.items() if any(w in task_lower for w in words)]


def score_folder(folder: dict, keywords: list, agent: str) -> int:
    score = 0
    fd = folder["settings"].get("folder", {})
    bd = folder["settings"].get("boundaries", {})
    ag = folder["settings"].get("agents", {})
    role = fd.get("role", "Custom")
    purpose = folder["purpose"].lower()

    # Keyword match against purpose text
    for kw in keywords:
        if kw in purpose:
            score += 40
        for word in KEYWORD_MAP.get(kw, []):
            if word in purpose:
                score += 10

    # Role affinity
    role_keywords = ROLE_KEYWORD_AFFINITY.get(role, [])
    for kw in keywords:
        if kw in role_keywords:
            score += 30

    # Agent compatibility
    allowed = ag.get("allowed", [])
    if agent in allowed:
        score += 20
    if ag.get("preferred") == agent:
        score += 15

    return score


def navigate(task: str, agent: str, folders: list) -> str:
    keywords = extract_keywords(task)
    scored = sorted(
        [(score_folder(f, keywords, agent), f) for f in folders],
        key=lambda x: x[0], reverse=True
    )

    lines = ["", "=" * 60, "NAVIGATION ORCHESTRATOR", "=" * 60,
             f"Task  : {task}", f"Agent : {agent}",
             f"Scanned {len(folders)} folder(s) | Keywords: {', '.join(keywords) or 'none matched'}", ""]

    if not scored or scored[0][0] == 0:
        lines += ["No matching folders found.",
                  "Consider creating a new folder with: python scripts/skill-create.py"]
        return "\n".join(lines)

    best_score, best = scored[0]
    bd = best["settings"].get("boundaries", {})
    budget = bd.get("token_budget", 8000)

    lines += [f"Recommended: {best['path']}/", f"Confidence : {min(100, best_score)}%", ""]
    lines += ["Steps:", "-" * 40]
    steps = [
        f"1. Navigate to: {best['path']}/",
        "2. Read: smart-folder.md",
        "3. Read: settings.json (check token budget and boundaries)",
    ]
    if (Path(best["path"]) / "laws").exists():
        steps.append("4. Read: laws/ (absolute guardrails)")
        steps.append("5. Begin work")
    else:
        steps.append("4. Begin work")
    lines += steps
    lines += ["", f"Token budget : {budget:,}  (~{int(budget * 0.6):,} estimated use)"]

    strengths = AGENT_STRENGTHS.get(agent, [])
    if strengths:
        lines += [f"", f"{agent.capitalize()} strengths for this task:"]
        lines += [f"  - {s}" for s in strengths[:3]]

    if len(scored) > 1 and scored[1][0] > 0:
        lines += ["", "Alternatives:"]
        for s, f in scored[1:3]:
            if s > 0:
                lines.append(f"  - {f['path']} ({s}% match)")

    lines += ["", "=" * 60]
    return "\n".join(lines)


def interactive():
    print("\nNavigation Orchestrator")
    print("=" * 40)

    location = input("Root folder [.]: ").strip() or "."
    root = Path(location).resolve()
    folders = find_folders(root)

    if not folders:
        print(f"No smart folders found in {root}")
        print("Run: bash scripts/init.sh")
        return

    print(f"Found {len(folders)} folder(s).")
    task = input("\nWhat is your task? ").strip()
    if not task:
        print("Task required.")
        return

    print("Agent? [claude, gemini, codex, cursor, kilo, aider]")
    agent = input("Agent [claude]: ").strip() or "claude"

    print(navigate(task, agent, folders))

    if input("\nProceed with this path? [Y/n]: ").strip().lower() in ("", "y", "yes"):
        print("\nPath confirmed. Begin navigation.")
    else:
        print("\nTry a different task description or create a new folder.")


def main():
    parser = argparse.ArgumentParser(description="Smart Folder Navigation Orchestrator")
    parser.add_argument("--task",     "-t", help="Task description")
    parser.add_argument("--agent",    "-a", default="claude",
                        choices=list(AGENT_STRENGTHS.keys()))
    parser.add_argument("--location", "-l", default=".")
    args = parser.parse_args()

    if args.task:
        root = Path(args.location).resolve()
        folders = find_folders(root)
        if not folders:
            print(f"No smart folders found in {root}")
            return
        print(navigate(args.task, args.agent, folders))
    else:
        interactive()


if __name__ == "__main__":
    main()
