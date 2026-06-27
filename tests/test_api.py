import json
import shutil
import threading
import time
import urllib.request
import urllib.parse
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from scripts.dashboard import Handler, CSRF_TOKEN
from http.server import HTTPServer


PORT = 18993
BASE = f"http://127.0.0.1:{PORT}"
EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


@pytest.fixture(scope="module")
def server(tmp_path_factory):
    # Operate on a throwaway copy — mutation tests must never write to the
    # version-controlled examples/ fixtures.
    root = tmp_path_factory.mktemp("examples_copy") / "examples"
    shutil.copytree(EXAMPLES, root)
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    server.root = root
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    time.sleep(0.2)
    yield server
    server.shutdown()


def _get(path: str) -> dict:
    resp = urllib.request.urlopen(f"{BASE}{path}")
    return json.loads(resp.read())


def _req(method: str, path: str, body: bytes | None = None,
         headers: dict | None = None, *, csrf: bool = True) -> tuple[int, dict]:
    hdrs = headers or {}
    hdrs.setdefault("Host", f"127.0.0.1:{PORT}")
    hdrs.setdefault("Origin", f"http://127.0.0.1:{PORT}")
    if csrf:
        hdrs.setdefault("X-CSRF-Token", CSRF_TOKEN)
    data = body
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=data,
        headers=hdrs,
        method=method,
    )
    try:
        resp = urllib.request.urlopen(req)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


class TestReadEndpoints:
    def test_folders(self, server):
        d = _get("/api/folders")
        assert "folders" in d
        names = {f["name"] for f in d["folders"]}
        assert "api-service" in names
        assert "knowledge-base" in names
        assert "web-app" in names

    def test_graph(self, server):
        d = _get("/api/graph")
        assert "nodes" in d
        assert "edges" in d
        assert len(d["nodes"]) > 0

    def test_stats(self, server):
        d = _get("/api/stats")
        assert isinstance(d, dict)

    def test_csrf_token(self, server):
        d = _get("/api/csrf-token")
        assert "token" in d
        assert d["token"] == CSRF_TOKEN

    def test_folder_detail(self, server):
        d = _get("/api/folders/api-service")
        assert "name" in d
        assert d["name"] == "api-service"

    def test_settings(self, server):
        d = _get("/api/folders/api-service/settings")
        assert "folder" in d
        assert d["folder"]["name"] == "api-service"

    def test_smart_folder_md(self, server):
        resp = urllib.request.urlopen(f"{BASE}/api/folders/api-service/smart-folder")
        content = resp.read().decode()
        assert len(content) > 0

    def test_smartignore(self, server):
        resp = urllib.request.urlopen(f"{BASE}/api/folders/knowledge-base/smartignore")
        content = resp.read().decode()
        assert len(content) > 0


class TestSecurityGuard:
    def test_rejects_missing_csrf(self, server):
        status, data = _req("PUT", "/api/folders/api-service/settings",
                            body=json.dumps({}).encode(),
                            headers={"Host": f"127.0.0.1:{PORT}",
                                     "Origin": f"http://127.0.0.1:{PORT}"},
                            csrf=False)
        assert status == 403

    def test_rejects_wrong_host(self, server):
        status, data = _req("PUT", "/api/folders/api-service/settings",
                            body=json.dumps({}).encode(),
                            headers={"Host": "evil.com:9999",
                                     "Origin": f"http://127.0.0.1:{PORT}",
                                     "X-CSRF-Token": CSRF_TOKEN})
        assert status == 403

    def test_rejects_wrong_origin(self, server):
        status, data = _req("PUT", "/api/folders/api-service/settings",
                            body=json.dumps({}).encode(),
                            headers={"Host": f"127.0.0.1:{PORT}",
                                     "Origin": "http://evil.com:9999",
                                     "X-CSRF-Token": CSRF_TOKEN})
        assert status == 403


class TestMutationEndpoints:
    def test_put_settings_validates_schema(self, server):
        bad = {"folder": {"name": "x", "role": "InvalidRole"}}
        status, data = _req("PUT", "/api/folders/api-service/settings",
                            body=json.dumps(bad).encode())
        assert status == 422
        assert "details" in data

    def test_put_settings_valid(self, server):
        before = _get("/api/folders/api-service/settings")
        valid = {
            "folder": {"name": "api-service", "role": "Architect"},
            "boundaries": {"can_see": ["*"], "cannot_see": [".env"]},
        }
        status, data = _req("PUT", "/api/folders/api-service/settings",
                            body=json.dumps(valid).encode())
        assert status == 200
        assert data["ok"] is True
        after = _get("/api/folders/api-service/settings")
        assert after.get("folder", {}).get("role") == "Architect"

    def test_put_settings_missing_boundaries_fails(self, server):
        incomplete = {"folder": {"name": "x", "role": "Architect"}}
        status, data = _req("PUT", "/api/folders/api-service/settings",
                            body=json.dumps(incomplete).encode())
        assert status == 422

    def test_delete_rejects_root(self, server):
        status, data = _req("POST", "/api/folders/./delete")
        assert status != 200

    def test_delete_moves_to_trash_and_hides(self, server):
        # api-service exists before delete...
        assert "api-service" in {f["name"] for f in _get("/api/folders")["folders"]}
        status, data = _req("POST", "/api/folders/api-service/delete")
        assert status == 200
        assert data["ok"] is True
        assert "/.trash/" in data["trashed_to"]
        # ...and is gone from the live listing (trash is excluded from scans)
        assert "api-service" not in {f["name"] for f in _get("/api/folders")["folders"]}
        # the folder is recoverable on disk, not rm'd
        assert (server.root / ".trash" / "api-service" / "smart-folder.md").exists()

    def test_validate_settings_endpoint(self, server):
        status, data = _req("POST", "/api/validate-settings",
                            body=json.dumps({
                                "folder": {"name": "ok", "role": "Architect"},
                                "boundaries": {"can_see": ["*"], "cannot_see": []},
                            }).encode())
        assert status == 200
        assert data["valid"] is True

    def test_validate_settings_reports_errors(self, server):
        status, data = _req("POST", "/api/validate-settings",
                            body=json.dumps({
                                "folder": {"name": "", "role": "BadRole"}
                            }).encode())
        assert status == 200
        assert data["valid"] is False
        assert len(data["errors"]) > 0
