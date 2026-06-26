import tempfile
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from smartfolders.templates import create_folder_structure
from smartfolders.core import scan


def test_create_folder_structure_creates_files():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        name = "my-agent"
        create_folder_structure(root / name, name, "Creator", "Build things")
        assert (root / name / "smart-folder.md").exists()
        assert (root / name / "settings.json").exists()
        assert (root / name / ".smartignore").exists()


def test_create_folder_round_trip():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        name = "round-trip"
        create_folder_structure(name, "Architect", "medium", "Design systems", output_dir=root)
        folders = scan(root)
        folders_by_name = {f.name: f for f in folders}
        assert name in folders_by_name
        assert folders_by_name[name].role == "Architect"
        assert "Design systems" in folders_by_name[name].purpose


def test_create_folder_settings_valid():
    import json
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        name = "valid-settings"
        create_folder_structure(name, "Knowledge Keeper", "medium", "Organize knowledge", output_dir=root)
        settings = json.loads((root / name / "settings.json").read_text())
        assert settings["folder"]["name"] == name
        assert settings["folder"]["role"] == "Knowledge Keeper"
        assert "boundaries" in settings
        assert "can_see" in settings["boundaries"]
