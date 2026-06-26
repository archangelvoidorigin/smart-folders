from __future__ import annotations

from datetime import date
from pathlib import Path

SMART_FOLDERS_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SMART_FOLDERS_DIR / "templates"


class TemplateRenderer:
    def __init__(self, templates_dir: Path = TEMPLATES_DIR):
        self.templates_dir = templates_dir

    def render(self, template_name: str, **kwargs) -> str:
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        content = template_path.read_text()
        for key, val in kwargs.items():
            placeholder = "{{" + key + "}}"
            content = content.replace(placeholder, str(val))
        return content

    def render_law(self, law_name: str, **kwargs) -> str:
        return self.render(f"laws/{law_name}", **kwargs)


def render_template(template_name: str, **kwargs) -> str:
    return TemplateRenderer().render(template_name, **kwargs)


def create_folder_structure(
    folder_name: str,
    role: str = "Custom",
    depth: str = "medium",
    purpose: str = "[Describe what this folder does]",
    author: str = "[your name]",
    agents: list[str] | None = None,
    output_dir: Path | None = None,
) -> Path:
    if agents is None:
        agents = ["claude", "gemini", "codex", "cursor", "kilo", "aider"]

    renderer = TemplateRenderer()
    today = date.today().isoformat()
    target = (output_dir or Path.cwd()) / folder_name

    target.mkdir(parents=True, exist_ok=True)

    smart_content = renderer.render("smart-folder.md", name=folder_name, role=role, depth=depth, date=today)
    (target / "smart-folder.md").write_text(smart_content)

    settings_content = renderer.render(
        "settings.json",
        name=folder_name,
        role=role,
        depth=depth,
        date=today,
        purpose=purpose,
        author=author,
        agents=json_dumps(agents),
    )
    (target / "settings.json").write_text(settings_content)

    ignore_template = TEMPLATES_DIR / ".smartignore"
    if ignore_template.exists():
        (target / ".smartignore").write_text(ignore_template.read_text())

    laws_dir = target / "laws"
    laws_dir.mkdir(exist_ok=True)
    for law_file in ("never-rules.md", "always-rules.md"):
        src = TEMPLATES_DIR / "laws" / law_file
        if src.exists():
            (laws_dir / law_file).write_text(src.read_text())

    subs = {"deep": 3, "medium": 2, "shallow": 0}.get(depth, 0)
    for i in range(1, subs + 1):
        sub = target / f"sub-folder-{i}"
        sub.mkdir(exist_ok=True)
        sub_content = renderer.render(
            "sub-folder.md", name=f"sub-folder-{i}", role=role, date=today
        )
        (sub / "smart-folder.md").write_text(sub_content)

    chron_dir = target / "chronicles"
    chron_dir.mkdir(exist_ok=True)
    (chron_dir / "README.md").write_text(
        "# Chronicles\n\nDocument everything significant:\n\n```\n[Session YYYY-MM-DD]\n"
        "What happened:\nWhy it matters:\nWhat was learned:\nWhat changed:\n```\n"
    )

    return target


def json_dumps(data: list) -> str:
    items = ", ".join(f'"{a}"' for a in data)
    return f"[{items}]"
