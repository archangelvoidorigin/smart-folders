from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from smartfolders.core import scan


EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_scan_finds_example_folders():
    folders = scan(EXAMPLES)
    names = {f.name for f in folders}
    assert "api-service" in names
    assert "knowledge-base" in names
    assert "web-app" in names


def test_scan_returns_folder_dataclass():
    folders = scan(EXAMPLES)
    for f in folders:
        assert f.name
        assert f.role
        assert f.path
        assert isinstance(f.token_budget, int)
        assert isinstance(f.file_count, int)
        assert isinstance(f.has_settings, bool)
        assert isinstance(f.has_laws, bool)
        assert isinstance(f.has_ignore, bool)


def test_scan_returns_root_when_scanning_inner():
    smart_folder = EXAMPLES / "api-service"
    folders = scan(smart_folder)
    assert len(folders) == 1
    assert folders[0].name == "(root)"
    assert folders[0].relative_path == "."


def test_scan_caches():
    f1 = scan(EXAMPLES)
    f2 = scan(EXAMPLES)
    assert len(f1) == len(f2)
