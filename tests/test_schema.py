from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from smartfolders.schema import load_roles, load_bounds, get_defaults, validate_settings


def test_load_roles_contains_architect():
    roles = load_roles()
    assert "Architect" in roles
    assert "Creator" in roles
    assert len(roles) >= 8


def test_load_bounds_has_token_budget():
    bounds = load_bounds()
    assert "token_budget" in bounds
    lo, hi = bounds["token_budget"]
    assert lo >= 1000
    assert hi <= 50000
    assert lo < hi


def test_get_defaults():
    defaults = get_defaults()
    assert "token_budget" in defaults
    assert "file_limit" in defaults
    assert "depth_limit" in defaults


def test_validate_valid_settings():
    valid = {
        "folder": {"name": "test", "role": "Architect"},
        "boundaries": {"can_see": ["*.py"], "cannot_see": [".env"]},
    }
    errors = validate_settings(valid)
    assert len(errors) == 0, f"Unexpected errors: {errors}"


def test_validate_missing_folder():
    errors = validate_settings({"boundaries": {"can_see": ["*"]}})
    assert any("folder" in e for e in errors)


def test_validate_invalid_role():
    errors = validate_settings({
        "folder": {"name": "test", "role": "NotARealRole"},
        "boundaries": {"can_see": ["*"], "cannot_see": []},
    })
    assert any("role" in e for e in errors)


def test_validate_missing_boundaries():
    errors = validate_settings({"folder": {"name": "test", "role": "Custom"}})
    assert any("boundaries" in e for e in errors)


def test_validate_token_budget_out_of_range():
    errors = validate_settings({
        "folder": {"name": "test", "role": "Architect"},
        "boundaries": {"can_see": ["*"], "cannot_see": [], "token_budget": 999999},
    })
    assert any("token_budget" in e for e in errors)


def test_validate_not_a_dict():
    errors = validate_settings([])
    assert len(errors) > 0
