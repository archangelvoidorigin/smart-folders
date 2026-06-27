#!/usr/bin/env python3
"""
Smart Folder Dashboard
Web UI for visualizing and managing smart folders. No external dependencies.

Usage:
  python scripts/dashboard.py [folder_path] [--port 8080]
  Then open http://localhost:8080
"""

from __future__ import annotations

import argparse
import json
import secrets
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from smartfolders.core import scan, invalidate_cache
from smartfolders.ops import validate_folder, audit_all, print_audit, build_map, render_tree, render_stats, render_connections
from smartfolders.schema import validate_settings

DASHBOARD_DIR = Path(__file__).resolve().parent.parent / "dashboard"
CONTROL_OS_DIR = Path(__file__).resolve().parent.parent / "control-os" / "dist"
CSRF_TOKEN = secrets.token_hex(32)


def _within(child: Path, parent: Path) -> bool:
    """True only if child is inside parent. Uses relative_to instead of string
    prefix matching, which is bypassable by a sibling sharing the name prefix
    (e.g. /proj/app vs /proj/app-secrets)."""
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/csrf-token":
            self._respond(200, "application/json", json.dumps({"token": CSRF_TOKEN}).encode())
        elif path == "/api/folders":
            self._respond(200, "application/json", json.dumps(self._folder_data()).encode())
        elif path == "/api/graph":
            self._respond(200, "application/json", json.dumps(self._graph_data()).encode())
        elif path == "/api/stats":
            self._respond(200, "application/json", json.dumps(self._stats_data()).encode())
        elif path.startswith("/api/search/"):
            term = path[len("/api/search/"):]
            # Decode URL-encoded term
            try:
                from urllib.parse import unquote
                term = unquote(term)
            except Exception:
                pass
            self._respond(200, "application/json", json.dumps(self._search(term)).encode())
        elif path == "/api/poll":
            import time
            self._respond(200, "application/json", json.dumps({"timestamp": time.time()}).encode())
        elif path.startswith("/api/folders/"):
            self._handle_folder_read(path)
        elif path.startswith("/api/"):
            action = path[5:]
            self._respond(200, "application/json", json.dumps(self._run(action)).encode())
        else:
            self._serve_static(path)

    def do_PUT(self):
        path = urlparse(self.path).path
        guard = self._guard()
        if guard:
            return

        if not path.startswith("/api/folders/"):
            self._respond(400, "application/json", json.dumps({"error": "Invalid path"}).encode())
            return

        folder_path, resource, sub = self._parse_folder_resource(path)
        if not resource:
            self._respond(400, "application/json", json.dumps({"error": "No resource specified"}).encode())
            return

        abs_folder = (self.server.root / folder_path).resolve()
        if not _within(abs_folder, self.server.root) or not abs_folder.is_dir():
            self._respond(404, "application/json", json.dumps({"error": "Folder not found"}).encode())
            return

        content = self._read_body()
        if content is None:
            return

        try:
            if resource == "settings":
                settings_data = json.loads(content)
                schema_errors = validate_settings(settings_data)
                if schema_errors:
                    self._respond(422, "application/json", json.dumps({"error": "Schema validation failed", "details": schema_errors}).encode())
                    return
                target = abs_folder / "settings.json"
            elif resource == "smart-folder":
                target = abs_folder / "smart-folder.md"
            elif resource == "smartignore":
                target = abs_folder / ".smartignore"
            elif resource == "laws" and sub:
                laws_dir = abs_folder / "laws"
                laws_dir.mkdir(parents=True, exist_ok=True)
                target = laws_dir / sub
                if not _within(target, laws_dir):
                    self._respond(403, "application/json", json.dumps({"error": "Forbidden"}).encode())
                    return
            else:
                self._respond(400, "application/json", json.dumps({"error": "Unknown resource"}).encode())
                return

            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
            self._respond(200, "application/json", json.dumps({"ok": True, "path": str(target)}).encode())
        except json.JSONDecodeError:
            self._respond(400, "application/json", json.dumps({"error": "Invalid JSON for settings"}).encode())
        except Exception as e:
            self._respond(500, "application/json", json.dumps({"error": str(e)}).encode())

    def do_POST(self):
        path = urlparse(self.path).path
        guard = self._guard()
        if guard:
            return

        if path == "/api/folders":
            self._handle_create_folder()
        elif path.startswith("/api/folders/") and path.endswith("/delete"):
            self._handle_delete(path)
        elif path == "/api/validate-settings":
            self._handle_validate_settings()
        else:
            self._respond(400, "application/json", json.dumps({"error": "Unknown POST endpoint"}).encode())
            return

    def _guard(self) -> bool:
        origin = self.headers.get("Origin", "")
        host = self.headers.get("Host", "")
        csrf = self.headers.get("X-CSRF-Token", "")

        allowed_hosts = (f"127.0.0.1:{self.server.server_address[1]}", f"localhost:{self.server.server_address[1]}")
        host_ok = host in allowed_hosts
        origin_ok = not origin or origin in (
            f"http://127.0.0.1:{self.server.server_address[1]}",
            f"http://localhost:{self.server.server_address[1]}",
        )
        csrf_ok = csrf == CSRF_TOKEN

        if not host_ok or not csrf_ok or not origin_ok:
            self._respond(403, "application/json", json.dumps({"error": "Forbidden"}).encode())
            return True
        return False

    def _read_body(self) -> str | None:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            self._respond(400, "application/json", json.dumps({"error": "Empty body"}).encode())
            return None
        try:
            return self.rfile.read(length).decode("utf-8")
        except Exception as e:
            self._respond(400, "application/json", json.dumps({"error": f"Invalid body: {e}"}).encode())
            return None

    def _parse_folder_resource(self, path: str) -> tuple[str, str | None, str | None]:
        rest = path[len("/api/folders/"):]
        known_resources = {"settings", "smart-folder", "smartignore", "laws"}
        parts = rest.split("/")
        for i, part in enumerate(parts):
            if part in known_resources:
                folder_path = "/".join(parts[:i])
                sub = "/".join(parts[i + 1:]) if i + 1 < len(parts) else None
                return folder_path, part, sub
        return rest, None, None

    def _handle_validate_settings(self):
        body = self._read_body()
        if body is None:
            return
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._respond(400, "application/json", json.dumps({"error": "Invalid JSON"}).encode())
            return
        from smartfolders.schema import validate_settings
        errors = validate_settings(data)
        self._respond(200, "application/json", json.dumps({"valid": len(errors) == 0, "errors": errors}).encode())

    def _handle_folder_read(self, path: str):
        rest = path[len("/api/folders/"):]
        known_resources = {"settings", "smart-folder", "smartignore", "laws"}
        parts = rest.split("/")
        resource = None
        sub = None
        folder_path_str = rest
        for i, part in enumerate(parts):
            if part in known_resources:
                folder_path_str = "/".join(parts[:i])
                resource = part
                sub = "/".join(parts[i + 1:]) if i + 1 < len(parts) else None
                break

        root = self.server.root
        abs_folder = (root / folder_path_str).resolve()
        if not _within(abs_folder, root) or not abs_folder.exists():
            self._respond(404, "text/plain", b"Folder not found")
            return

        if resource is None:
            folder = self._find_folder(folder_path_str)
            if folder:
                self._respond(200, "application/json", json.dumps(folder).encode())
            else:
                self._respond(404, "text/plain", b"Folder not found")
            return

        if resource == "settings":
            self._serve_raw_file(abs_folder / "settings.json")
        elif resource == "smart-folder":
            self._serve_raw_file(abs_folder / "smart-folder.md")
        elif resource == "smartignore":
            self._serve_raw_file(abs_folder / ".smartignore")
        elif resource == "laws":
            laws_dir = abs_folder / "laws"
            if sub:
                law_file = laws_dir / sub
                if not _within(law_file, laws_dir):
                    self._respond(403, "text/plain", b"Forbidden")
                    return
                self._serve_raw_file(law_file)
            else:
                self._list_law_files(laws_dir)

    def _handle_create_folder(self):
        body = self._read_body()
        if body is None:
            return
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._respond(400, "application/json", json.dumps({"error": "Invalid JSON"}).encode())
            return

        name = data.get("name", "").strip()
        role = data.get("role", "Custom").strip()
        purpose = data.get("purpose", "").strip()

        if not name:
            self._respond(400, "application/json", json.dumps({"error": "Name is required"}).encode())
            return

        root = self.server.root
        folder_path = root / name
        if folder_path.exists():
            self._respond(409, "application/json", json.dumps({"error": "Folder already exists"}).encode())
            return

        try:
            from smartfolders.templates import create_folder_structure
            create_folder_structure(name, role, "medium", purpose, output_dir=root)
            self._respond(201, "application/json", json.dumps({"ok": True, "path": name}).encode())
        except Exception as e:
            self._respond(500, "application/json", json.dumps({"error": str(e)}).encode())

    def _handle_delete(self, path: str):
        """Soft-delete: move the folder to a .trash/ directory inside the root.
        Never an rm — the folder stays recoverable. .trash/ is excluded from scans."""
        rest = path[len("/api/folders/"):]
        folder_path_str = rest.replace("/delete", "").rstrip("/")
        root = self.server.root
        abs_folder = (root / folder_path_str).resolve()
        if not _within(abs_folder, root) or not abs_folder.exists():
            self._respond(404, "application/json", json.dumps({"error": "Folder not found"}).encode())
            return

        if abs_folder == root.resolve():
            self._respond(400, "application/json", json.dumps({"error": "Cannot delete root"}).encode())
            return

        trash = self._get_trash_dir()
        try:
            import shutil
            dest = trash / folder_path_str
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                import time
                dest = trash / f"{folder_path_str}_{int(time.time())}"
            shutil.move(str(abs_folder), str(dest))
            invalidate_cache(root)
            self._respond(200, "application/json", json.dumps({"ok": True, "trashed_to": str(dest)}).encode())
        except Exception as e:
            self._respond(500, "application/json", json.dumps({"error": str(e)}).encode())

    def _get_trash_dir(self) -> Path:
        """.trash/ lives inside the served root so deletes never escape it."""
        trash = self.server.root / ".trash"
        trash.mkdir(parents=True, exist_ok=True)
        return trash

    def _serve_raw_file(self, file_path: Path):
        if file_path.is_file():
            ctype = self._content_type(file_path)
            self._respond(200, ctype, file_path.read_bytes())
        else:
            self._respond(404, "text/plain", b"Not found")

    def _list_law_files(self, laws_dir: Path):
        if laws_dir.is_dir():
            files = [f.name for f in sorted(laws_dir.iterdir()) if f.is_file()]
            self._respond(200, "application/json", json.dumps({"files": files}).encode())
        else:
            self._respond(200, "application/json", json.dumps({"files": []}).encode())

    def _find_folder(self, folder_path: str) -> dict | None:
        root = self.server.root
        for f in scan(root):
            if f.relative_path == folder_path:
                return {
                    "path":         f.relative_path,
                    "name":         f.name,
                    "role":         f.role,
                    "purpose":      f.purpose,
                    "depth":        str(f.depth),
                    "token_budget": f.token_budget,
                    "file_limit":   f.file_limit,
                    "file_count":   f.file_count,
                    "connections":  f.connections,
                    "has_smart":    True,
                    "has_settings": f.has_settings,
                    "has_ignore":   f.has_ignore,
                    "has_laws":     f.has_laws,
                }
        return None

    def _graph_data(self) -> dict:
        root = self.server.root
        folders = scan(root)
        # Pre-compute max token budget for heatmap calculation
        max_budget = max((f.token_budget for f in folders), default=1)
        # Pre-compute efficiency per folder via audit_all
        audit_map = {entry["path"]: entry.get("efficiency", 0) for entry in audit_all(root)}
        nodes = []
        edges = []
        for f in folders:
            # Compute token usage percentage for heatmap layer
            token_pct = round((f.token_budget / max_budget) * 100, 2) if max_budget else 0
            # Retrieve efficiency from audit map (fallback to 0)
            efficiency = audit_map.get(str(f.path), 0)
            nodes.append({
                "id": f.relative_path,
                "label": f.name,
                "role": f.role,
                "depth": f.depth,
                "token_budget": f.token_budget,
                "file_count": f.file_count,
                "has_settings": f.has_settings,
                "has_smartignore": f.has_ignore,
                "has_laws": f.has_laws,
                "purpose": f.purpose or "",
                "efficiency": efficiency,
                "token_usage_pct": token_pct,
            })
        for f in folders:
            c = f.connections or {}
            source = f.relative_path
            if c.get("parent"):
                edges.append({"id": f"{c['parent']}->{source}", "source": c["parent"], "target": source, "type": "parent", "label": "parent"})
            for child in c.get("children") or []:
                edges.append({"id": f"{source}->{child}", "source": source, "target": child, "type": "child", "label": "child"})
            for target in c.get("feeds_into") or []:
                edges.append({"id": f"{source}->{target}", "source": source, "target": target, "type": "feeds_into", "label": "feeds into"})
            for target in c.get("receives_from") or []:
                edges.append({"id": f"{target}->{source}", "source": target, "target": source, "type": "receives_from", "label": "receives from"})
        return {"nodes": nodes, "edges": edges}
    def _stats_data(self) -> dict:
        root = self.server.root
        folders = scan(root)
        total = len(folders)
        if not total:
            return {"folders": 0, "total_budget": 0, "avg_budget": 0, "avg_files": 0, "roles": {}}
        total_budget = sum(f.token_budget for f in folders)
        total_files = sum(f.file_count for f in folders)
        roles = {}
        for f in folders:
            roles[f.role] = roles.get(f.role, 0) + 1
        return {
            "folders": total,
            "total_budget": total_budget,
            "avg_budget": round(total_budget / total) if total else 0,
            "avg_files": round(total_files / total, 1) if total else 0,
            "roles": roles,
            "has_settings": sum(1 for f in folders if f.has_settings),
            "has_ignore": sum(1 for f in folders if f.has_ignore),
            "has_laws": sum(1 for f in folders if f.has_laws),
        }

    def _serve_static(self, path: str):
        file_path = self._resolve_static_path(path)
        if file_path and file_path.is_file():
            ctype = self._content_type(file_path)
            self._respond(200, ctype, file_path.read_bytes())
        else:
            self._respond(404, "text/plain", b"Not found")

    def _resolve_static_path(self, path: str) -> Path | None:
        if path in ("/", "/index.html"):
            control_os_index = CONTROL_OS_DIR / "index.html"
            if CONTROL_OS_DIR.is_dir() and control_os_index.is_file():
                return control_os_index
            return DASHBOARD_DIR / "index.html"
        cleaned = path.lstrip("/")
        for base in (CONTROL_OS_DIR, DASHBOARD_DIR):
            if not base.is_dir():
                continue
            candidate = (base / cleaned).resolve()
            if _within(candidate, base) and candidate.is_file():
                return candidate
        if CONTROL_OS_DIR.is_dir():
            candidate = (CONTROL_OS_DIR / cleaned).resolve()
            if _within(candidate, CONTROL_OS_DIR) and not candidate.exists() and not candidate.suffix:
                index = CONTROL_OS_DIR / "index.html"
                if index.is_file():
                    return index
        return None

    def _content_type(self, path: Path) -> str:
        ext = path.suffix.lower()
        return {
            ".html": "text/html",
            ".js": "application/javascript",
            ".css": "text/css",
            ".json": "application/json",
            ".png": "image/png",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
            ".md": "text/markdown",
        }.get(ext, "application/octet-stream")

    def _allowed_origin(self) -> str | None:
        """Reflect the request Origin only when it is a localhost origin. Never
        emit a wildcard: ACAO:* would let any website read folder data and file
        contents cross-origin (GET endpoints carry no CSRF). Same-origin requests
        need no ACAO; control-os dev (localhost:5173) is still permitted."""
        origin = self.headers.get("Origin", "")
        if origin and urlparse(origin).hostname in ("127.0.0.1", "localhost"):
            return origin
        return None

    def _cors_headers(self):
        allowed = self._allowed_origin()
        if allowed:
            self.send_header("Access-Control-Allow-Origin", allowed)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "GET, PUT, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-CSRF-Token")

    def _respond(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self._cors_headers()
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

    def _folder_data(self) -> dict:
        root = self.server.root
        folders = scan(root)
        result = []
        for f in folders:
            result.append({
                "path":         f.relative_path,
                "name":         f.name,
                "role":         f.role,
                "purpose":      f.purpose,
                "depth":        str(f.depth),
                "token_budget": f.token_budget,
                "file_limit":   f.file_limit,
                "file_count":   f.file_count,
                "connections":  f.connections,
                "has_smart":    True,
                "has_settings": f.has_settings,
                "has_ignore":   f.has_ignore,
                "has_laws":     f.has_laws,
            })
        return {"root": str(root), "folders": result}

    def _run(self, action: str) -> dict:
        root = self.server.root
        try:
            if action == "validate":
                folders = [p.parent for p in sorted(root.rglob("smart-folder.md"))]
                output_lines = []
                all_passed = True
                for folder in folders:
                    errors, warnings = validate_folder(folder)
                    prefix = str(folder)
                    output_lines.append(f"\n{prefix}")
                    output_lines.append("-" * min(60, len(prefix) + 2))
                    if errors:
                        for e in errors:
                            output_lines.append(f"  ERROR   {e}")
                    if warnings:
                        for w in warnings:
                            output_lines.append(f"  WARN    {w}")
                    if not errors and not warnings:
                        output_lines.append("  OK      All checks passed")
                    if errors:
                        all_passed = False
                output_lines.append("")
                output_lines.append("Result: PASS" if all_passed else "Result: FAIL")
                return {"output": "\n".join(output_lines)}
            elif action == "audit":
                results = audit_all(root)
                return {"output": print_audit(results)}
            elif action == "map":
                folders = build_map(root)
                parts = [render_tree(folders, root), render_stats(folders), render_connections(folders)]
                return {"output": "\n".join(parts)}
            else:
                return {"error": f"Unknown action: {action}"}
        except Exception as e:
            return {"error": str(e)}

    def _search(self, term: str) -> list[dict]:
        root = self.server.root
        term_lower = term.lower()
        results = []
        for f in scan(root):
            if term_lower in f.name.lower() or term_lower in f.role.lower() or term_lower in (f.purpose or "").lower():
                results.append({
                    "path": f.relative_path,
                    "name": f.name,
                    "role": f.role,
                    "purpose": f.purpose,
                    "depth": str(f.depth),
                    "token_budget": f.token_budget,
                    "file_limit": f.file_limit,
                    "file_count": f.file_count,
                    "connections": f.connections,
                    "has_smart": True,
                    "has_settings": f.has_settings,
                    "has_ignore": f.has_ignore,
                    "has_laws": f.has_laws,
                })
        return results

    def log_message(self, *_):
        pass


def main():
    parser = argparse.ArgumentParser(description="Smart Folder Dashboard")
    parser.add_argument("folder", nargs="?", default=".", help="Root folder to visualize")
    parser.add_argument("--port", "-p", type=int, default=8080)
    parser.add_argument("--host", default="localhost")
    args = parser.parse_args()

    root = Path(args.folder).resolve()
    if not root.exists():
        print(f"Error: folder not found: {root}")
        return 1

    if not (DASHBOARD_DIR / "index.html").exists():
        print(f"Error: dashboard/index.html not found at {DASHBOARD_DIR}")
        return 1

    try:
        server = HTTPServer((args.host, args.port), Handler)
    except OSError as e:
        if e.errno == 98:
            print(f"Port {args.port} is already in use.")
            print(f"  Another dashboard may be running.")
            print(f"  Use: python scripts/dashboard.py --port {args.port + 1}")
            print(f"  Or:  kill $(lsof -ti:{args.port}) && python scripts/dashboard.py {args.folder}")
        else:
            print(f"Socket error: {e}")
        return 1
    server.root = root

    print(f"Smart Folder Dashboard")
    print(f"  Root   : {root}")
    print(f"  URL    : http://{args.host}:{args.port}")
    print(f"  CSRF   : {CSRF_TOKEN[:16]}... (included in page via /api/csrf-token)")
    print(f"  Stop   : Ctrl+C")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
