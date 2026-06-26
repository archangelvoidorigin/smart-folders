from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Folder:
    path: Path
    relative_path: str
    name: str
    role: str
    depth: int
    token_budget: int
    file_limit: int
    purpose: str
    has_settings: bool
    has_ignore: bool
    has_laws: bool
    connections: dict = field(default_factory=dict)
    settings: dict = field(default_factory=dict)
    file_count: int = 0


_MTIME_CACHE: dict[str, tuple[float, list[Folder]]] = {}


def _get_mtime(root: Path) -> float:
    try:
        return root.stat().st_mtime
    except OSError:
        return 0


def scan(root: Path, *, use_cache: bool = True) -> list[Folder]:
    root = root.resolve()
    if not root.exists():
        return []

    mtime = _get_mtime(root)
    cache_key = str(root)

    if use_cache and cache_key in _MTIME_CACHE:
        cached_mtime, cached_folders = _MTIME_CACHE[cache_key]
        if cached_mtime == mtime:
            return cached_folders

    smart_mds = sorted(root.rglob("smart-folder.md"))
    folders: list[Folder] = []

    for sm_path in smart_mds:
        folder_path = sm_path.parent
        rel = str(folder_path.relative_to(root)) if folder_path != root else "."
        name = folder_path.name if folder_path != root else "(root)"

        settings_data: dict = {}
        sf = folder_path / "settings.json"
        if sf.exists():
            try:
                settings_data = json.loads(sf.read_text())
            except (json.JSONDecodeError, OSError):
                pass

        fd = settings_data.get("folder", {})
        bd = settings_data.get("boundaries", {})
        conns = settings_data.get("connections", {})

        role = fd.get("role", "Custom")
        token_budget = bd.get("token_budget", 8000)
        file_limit = bd.get("file_limit", 500)
        purpose_val = fd.get("purpose", "")

        file_count = 0
        if folder_path.exists():
            file_count = sum(
                1 for f in folder_path.iterdir()
                if f.is_file() and not f.name.startswith(".")
            )

        folders.append(Folder(
            path=folder_path,
            relative_path=rel,
            name=name,
            role=role,
            depth=len(folder_path.relative_to(root).parts),
            token_budget=token_budget,
            file_limit=file_limit,
            purpose=purpose_val,
            has_settings=sf.exists(),
            has_ignore=(folder_path / ".smartignore").exists(),
            has_laws=(folder_path / "laws").exists(),
            connections=conns,
            settings=settings_data,
            file_count=file_count,
        ))

    _MTIME_CACHE[cache_key] = (mtime, folders)
    return folders


def invalidate_cache(root: Path | None = None) -> None:
    if root is None:
        _MTIME_CACHE.clear()
    else:
        _MTIME_CACHE.pop(str(root.resolve()), None)
