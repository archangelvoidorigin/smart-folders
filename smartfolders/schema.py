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
