from __future__ import annotations

import json
from pathlib import Path

SMART_FOLDERS_DIR = Path(__file__).resolve().parent.parent

_SCHEMA_PATH = SMART_FOLDERS_DIR / "settings-schema.json"

_FALLBACK_ROLES = frozenset({
    "Knowledge Keeper", "Creator", "Architect", "Connector",
    "Chronicler", "Enabler", "Archive", "Staging", "Custom",
})
_FALLBACK_BOUNDS = {"token_budget": (1000, 50000), "file_limit": (10, 10000)}

_ROLES_CACHE = None
_BOUNDS_CACHE = None


def load_roles() -> frozenset:
    global _ROLES_CACHE
    if _ROLES_CACHE is not None:
        return _ROLES_CACHE
    try:
        schema = json.loads(_SCHEMA_PATH.read_text())
        roles = set(schema["properties"]["folder"]["properties"]["role"]["enum"])
        _ROLES_CACHE = frozenset(roles)
        return _ROLES_CACHE
    except (OSError, KeyError, json.JSONDecodeError):
        return _FALLBACK_ROLES


def load_bounds() -> dict[str, tuple[int, int]]:
    global _BOUNDS_CACHE
    if _BOUNDS_CACHE is not None:
        return _BOUNDS_CACHE
    try:
        schema = json.loads(_SCHEMA_PATH.read_text())
        bprops = schema["properties"]["boundaries"]["properties"]
        bounds = {
            key: (bprops[key]["minimum"], bprops[key]["maximum"])
            for key in ("token_budget", "file_limit")
        }
        _BOUNDS_CACHE = bounds
        return bounds
    except (OSError, KeyError, json.JSONDecodeError):
        return dict(_FALLBACK_BOUNDS)


def validate_settings(settings: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(settings, dict):
        return ["settings must be a JSON object"]

    folder = settings.get("folder")
    if not isinstance(folder, dict):
        errors.append("Missing required 'folder' object")
    else:
        name = folder.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append("folder.name: required, must be non-empty string")
        role = folder.get("role")
        valid_roles = load_roles()
        if role not in valid_roles:
            errors.append(f"folder.role: must be one of {sorted(valid_roles)}")

    boundaries = settings.get("boundaries")
    if not isinstance(boundaries, dict):
        errors.append("Missing required 'boundaries' object")
    else:
        bounds = load_bounds()
        tb = boundaries.get("token_budget")
        if tb is not None:
            lo, hi = bounds.get("token_budget", (1000, 50000))
            if not isinstance(tb, int) or tb < lo or tb > hi:
                errors.append(f"boundaries.token_budget: must be int between {lo}–{hi}")
        fl = boundaries.get("file_limit")
        if fl is not None:
            lo, hi = bounds.get("file_limit", (10, 10000))
            if not isinstance(fl, int) or fl < lo or fl > hi:
                errors.append(f"boundaries.file_limit: must be int between {lo}–{hi}")
        if "can_see" not in boundaries:
            errors.append("boundaries: missing 'can_see' array")

    conn = settings.get("connections", {})
    if not isinstance(conn, dict):
        errors.append("connections: must be an object")

    agents = settings.get("agents", {})
    if not isinstance(agents, dict):
        errors.append("agents: must be an object")

    return errors


def get_defaults() -> dict:
    try:
        schema = json.loads(_SCHEMA_PATH.read_text())
        bprops = schema["properties"]["boundaries"]["properties"]
        return {
            "token_budget": bprops["token_budget"].get("default", 8000),
            "file_limit": bprops["file_limit"].get("default", 500),
            "depth_limit": bprops["depth_limit"].get("default", 5),
        }
    except (OSError, KeyError, json.JSONDecodeError):
        return {"token_budget": 8000, "file_limit": 500, "depth_limit": 5}
