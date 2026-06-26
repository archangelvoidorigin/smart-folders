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
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from smartfolders.core import scan
from smartfolders.ops import validate_folder, audit_all, print_audit, build_map, render_tree, render_stats, render_connections

DASHBOARD_DIR = Path(__file__).resolve().parent.parent / "dashboard"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/folders":
            self._respond(200, "application/json", json.dumps(self._folder_data()).encode())
        elif path.startswith("/api/"):
            action = path[5:]
            self._respond(200, "application/json", json.dumps(self._run(action)).encode())
        else:
            self._serve_static(path)

    def _serve_static(self, path: str):
        if path in ("/", "/index.html"):
            file_path = DASHBOARD_DIR / "index.html"
        else:
            cleaned = path.lstrip("/")
            file_path = DASHBOARD_DIR / cleaned
            if not file_path.resolve().absolute().parts > DASHBOARD_DIR.resolve().absolute().parts:
                pass
            if not str(file_path.resolve()).startswith(str(DASHBOARD_DIR.resolve())):
                self._respond(403, "text/plain", b"Forbidden")
                return

        if file_path.is_file():
            ctype = self._content_type(file_path)
            self._respond(200, ctype, file_path.read_bytes())
        else:
            self._respond(404, "text/plain", b"Not found")

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
        }.get(ext, "application/octet-stream")

    def _respond(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

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
    print(f"  Root : {root}")
    print(f"  URL  : http://{args.host}:{args.port}")
    print(f"  Stop : Ctrl+C")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
