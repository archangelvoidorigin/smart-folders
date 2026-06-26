import json
import tempfile
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from smartfolders.ops import validate_folder, audit_all
from smartfolders.templates import create_folder_structure


EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_validate_passes_good_folder():
    errors, warnings = validate_folder(EXAMPLES / "api-service")
    assert len(errors) == 0, f"Unexpected errors: {errors}"


def test_validate_three_examples():
    for name in ("api-service", "knowledge-base", "web-app"):
        errors, warnings = validate_folder(EXAMPLES / name)
        assert len(errors) == 0, f"{name}: {errors}"


def test_validate_flags_broken_folder():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        bad = root / "bad-folder"
        bad.mkdir()
        errors, warnings = validate_folder(bad)
        assert len(errors) > 0


def test_validate_flags_missing_settings():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        bad = root / "bad-folder"
        bad.mkdir()
        (bad / "smart-folder.md").write_text("# Bad\n\n## Purpose\n\nTest")
        errors, warnings = validate_folder(bad)
        assert any("settings.json" in e for e in errors) or any("settings.json" in w for w in warnings)


def test_audit_returns_data():
    results = audit_all(EXAMPLES)
    assert len(results) > 0
    for r in results:
        assert "name" in r
        assert "efficiency" in r
        assert "file_count" in r
        assert "token_budget" in r


def test_validate_passes_created_folder():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        name = "test-created"
        create_folder_structure(name, "Custom", "medium", "Test", output_dir=root)
        errors, warnings = validate_folder(root / name)
        assert len(errors) == 0, f"Created folder has errors: {errors}"
