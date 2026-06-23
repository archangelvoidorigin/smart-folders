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
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

SCRIPTS_DIR = Path(__file__).parent

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smart Folder Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,monospace;background:#0f0f1a;color:#e2e2e2;min-height:100vh}
.topbar{background:#16213e;padding:16px 24px;border-bottom:1px solid #1e3a6e;display:flex;align-items:center;gap:16px}
.topbar h1{font-size:18px;color:#4fa3ff;letter-spacing:.5px}
.topbar .root{font-size:12px;color:#6b7280;margin-left:auto}
.stats{display:flex;gap:0;border-bottom:1px solid #1e3a6e}
.stat{flex:1;padding:12px 20px;border-right:1px solid #1e3a6e;text-align:center}
.stat:last-child{border-right:none}
.stat-val{font-size:22px;font-weight:700;color:#4fa3ff}
.stat-lbl{font-size:11px;color:#6b7280;text-transform:uppercase;letter-spacing:.5px;margin-top:2px}
.main{display:flex;height:calc(100vh - 101px)}
.sidebar{width:260px;background:#12192e;border-right:1px solid #1e3a6e;overflow-y:auto;padding:12px}
.sidebar h3{font-size:11px;color:#6b7280;text-transform:uppercase;letter-spacing:.5px;padding:4px 8px 8px}
.folder-item{padding:8px 12px;border-radius:6px;cursor:pointer;margin-bottom:2px;border:1px solid transparent;transition:.15s}
.folder-item:hover{background:#1e3a6e;border-color:#2d4f8e}
.folder-item.active{background:#1e3a6e;border-color:#4fa3ff}
.folder-name{font-size:13px;font-weight:500}
.folder-role{font-size:11px;margin-top:2px}
.role-badge{display:inline-block;padding:1px 6px;border-radius:10px;font-size:10px;margin-left:4px;font-weight:600}
.content{flex:1;padding:24px;overflow-y:auto;display:flex;flex-direction:column;gap:16px}
.panel{background:#12192e;border:1px solid #1e3a6e;border-radius:8px;padding:20px}
.panel h2{font-size:14px;color:#4fa3ff;margin-bottom:14px;text-transform:uppercase;letter-spacing:.5px}
.row{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a2a4a;font-size:13px}
.row:last-child{border-bottom:none}
.row-label{color:#9ca3af}
.row-val{color:#e2e2e2;font-weight:500}
.health{display:flex;gap:8px;flex-wrap:wrap}
.h-item{padding:4px 12px;border-radius:4px;font-size:12px;font-weight:600}
.h-pass{background:#14532d;color:#4ade80}
.h-warn{background:#451a03;color:#fb923c}
.h-fail{background:#450a0a;color:#f87171}
.actions{display:flex;gap:10px;flex-wrap:wrap}
.btn{padding:8px 16px;border:1px solid #2d4f8e;border-radius:6px;background:#1e3a6e;color:#e2e2e2;cursor:pointer;font-size:13px;transition:.15s}
.btn:hover{background:#2d4f8e;border-color:#4fa3ff;color:#4fa3ff}
.output-panel{background:#080c14;border:1px solid #1e3a6e;border-radius:6px;padding:16px;font-family:monospace;font-size:12px;white-space:pre-wrap;max-height:320px;overflow-y:auto;color:#a3e635;display:none}
.connections{display:flex;gap:8px;flex-wrap:wrap}
.conn-node{background:#1e3a6e;border:1px solid #2d4f8e;border-radius:6px;padding:6px 12px;font-size:12px}
.empty{color:#6b7280;font-size:12px;font-style:italic}
/* Role colors */
.r-knowledge{background:#1e40af;color:#93c5fd}
.r-creator{background:#7f1d1d;color:#fca5a5}
.r-architect{background:#713f12;color:#fcd34d}
.r-connector{background:#4a044e;color:#e879f9}
.r-chronicler{background:#14532d;color:#86efac}
.r-enabler{background:#164e63;color:#67e8f9}
.r-archive{background:#1f2937;color:#9ca3af}
.r-staging{background:#3b0764;color:#d8b4fe}
.r-custom{background:#1f2937;color:#e2e2e2}
</style>
</head>
<body>
<div class="topbar">
  <h1>Smart Folder Dashboard</h1>
  <span class="root" id="root-path"></span>
</div>
<div class="stats">
  <div class="stat"><div class="stat-val" id="s-folders">0</div><div class="stat-lbl">Folders</div></div>
  <div class="stat"><div class="stat-val" id="s-roles">0</div><div class="stat-lbl">Roles</div></div>
  <div class="stat"><div class="stat-val" id="s-tokens">0</div><div class="stat-lbl">Total Token Budget</div></div>
  <div class="stat"><div class="stat-val" id="s-avg">0</div><div class="stat-lbl">Avg Budget</div></div>
</div>
<div class="main">
  <div class="sidebar">
    <h3>Folders</h3>
    <div id="folder-list"></div>
  </div>
  <div class="content">
    <div class="panel">
      <h2>Health Check</h2>
      <div class="health" id="health-checks"></div>
    </div>
    <div class="panel" id="folder-detail" style="display:none">
      <h2 id="detail-name">Folder Details</h2>
      <div id="detail-rows"></div>
    </div>
    <div class="panel">
      <h2>Connections</h2>
      <div class="connections" id="connections"></div>
    </div>
    <div class="panel">
      <h2>Actions</h2>
      <div class="actions">
        <button class="btn" onclick="runScript('validate')">Validate All</button>
        <button class="btn" onclick="runScript('audit')">Audit Tokens</button>
        <button class="btn" onclick="runScript('map')">Show Map</button>
      </div>
      <div class="output-panel" id="output"></div>
    </div>
  </div>
</div>
<script>
let data = null;
let selected = null;

function roleClass(role) {
  const map = {
    'Knowledge Keeper': 'r-knowledge', 'Creator': 'r-creator',
    'Architect': 'r-architect', 'Connector': 'r-connector',
    'Chronicler': 'r-chronicler', 'Enabler': 'r-enabler',
    'Archive': 'r-archive', 'Staging': 'r-staging', 'Custom': 'r-custom'
  };
  return map[role] || 'r-custom';
}

async function load() {
  const res = await fetch('/api/data');
  data = await res.json();
  render();
}

function render() {
  document.getElementById('root-path').textContent = data.root;
  document.getElementById('s-folders').textContent = data.folders.length;
  document.getElementById('s-roles').textContent = new Set(data.folders.map(f => f.role)).size;
  const total = data.folders.reduce((s, f) => s + f.token_budget, 0);
  document.getElementById('s-tokens').textContent = total.toLocaleString();
  document.getElementById('s-avg').textContent = data.folders.length ? Math.round(total / data.folders.length).toLocaleString() : '0';

  // Sidebar
  const list = document.getElementById('folder-list');
  list.innerHTML = data.folders.map((f, i) => `
    <div class="folder-item" onclick="selectFolder(${i})" id="fi-${i}">
      <div class="folder-name">${f.name}</div>
      <div class="folder-role"><span class="role-badge ${roleClass(f.role)}">${f.role}</span></div>
    </div>`).join('');

  // Health
  const hc = document.getElementById('health-checks');
  const total_f = data.folders.length;
  const checks = [
    ['smart-folder.md', data.folders.filter(f => f.has_smart).length, total_f],
    ['settings.json', data.folders.filter(f => f.has_settings).length, total_f],
    ['.smartignore', data.folders.filter(f => f.has_ignore).length, total_f],
    ['laws/', data.folders.filter(f => f.has_laws).length, total_f],
  ];
  hc.innerHTML = checks.map(([label, ok, tot]) => {
    const cls = ok === tot ? 'h-pass' : ok === 0 ? 'h-fail' : 'h-warn';
    return `<div class="h-item ${cls}">${label} ${ok}/${tot}</div>`;
  }).join('');

  // Default connections
  renderConnections(null);
}

function selectFolder(i) {
  selected = i;
  document.querySelectorAll('.folder-item').forEach(el => el.classList.remove('active'));
  document.getElementById(`fi-${i}`).classList.add('active');

  const f = data.folders[i];
  document.getElementById('folder-detail').style.display = 'block';
  document.getElementById('detail-name').textContent = f.name;
  document.getElementById('detail-rows').innerHTML = [
    ['Role', f.role], ['Purpose', f.purpose || '—'],
    ['Token Budget', f.token_budget.toLocaleString()],
    ['File Limit', f.file_limit], ['Depth', f.depth || '—'],
    ['Path', f.path],
  ].map(([l, v]) => `<div class="row"><span class="row-label">${l}</span><span class="row-val">${v}</span></div>`).join('');

  renderConnections(f);
}

function renderConnections(f) {
  const el = document.getElementById('connections');
  if (!f) { el.innerHTML = '<span class="empty">Select a folder to see its connections</span>'; return; }
  const conns = f.connections || {};
  const nodes = [];
  if (conns.parent) nodes.push(`<- ${conns.parent}`);
  (conns.children || []).forEach(c => nodes.push(`-> child: ${c}`));
  (conns.feeds_into || []).forEach(c => nodes.push(`-> feeds: ${c}`));
  (conns.receives_from || []).forEach(c => nodes.push(`<- from: ${c}`));
  el.innerHTML = nodes.length
    ? nodes.map(n => `<div class="conn-node">${n}</div>`).join('')
    : '<span class="empty">No connections defined in settings.json</span>';
}

async function runScript(action) {
  const out = document.getElementById('output');
  out.style.display = 'block';
  out.textContent = `Running ${action}...`;
  try {
    const res = await fetch(`/api/${action}`, {method: 'POST'});
    const d = await res.json();
    out.textContent = d.output || d.error || 'No output';
  } catch(e) {
    out.textContent = `Error: ${e.message}`;
  }
}

load();
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._respond(200, "text/html", HTML.encode())
        elif path == "/api/data":
            self._respond(200, "application/json", json.dumps(self._folder_data()).encode())
        else:
            self._respond(404, "text/plain", b"Not found")

    def do_POST(self):
        path = urlparse(self.path).path
        if path.startswith("/api/"):
            action = path[5:]
            self._respond(200, "application/json", json.dumps(self._run(action)).encode())
        else:
            self._respond(404, "text/plain", b"Not found")

    def _respond(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _run(self, action: str) -> dict:
        script_map = {
            "validate": ["python", str(SCRIPTS_DIR / "validate.py"), "--recursive", str(self.server.root)],
            "audit":    ["python", str(SCRIPTS_DIR / "audit.py"),    str(self.server.root)],
            "map":      ["python", str(SCRIPTS_DIR / "map.py"),      str(self.server.root), "--stats", "--connections"],
        }
        cmd = script_map.get(action)
        if not cmd:
            return {"error": f"Unknown action: {action}"}
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return {"output": result.stdout + (("\n" + result.stderr) if result.stderr else "")}
        except subprocess.TimeoutExpired:
            return {"error": "Script timed out"}
        except Exception as e:
            return {"error": str(e)}

    def _folder_data(self) -> dict:
        root = self.server.root
        folders = []
        for sm in sorted(root.rglob("smart-folder.md")):
            folder = sm.parent
            settings = {}
            sf = folder / "settings.json"
            if sf.exists():
                try:
                    settings = json.loads(sf.read_text())
                except Exception:
                    pass
            fd = settings.get("folder", {})
            bd = settings.get("boundaries", {})
            conns = settings.get("connections", {})
            rel = str(folder.relative_to(root)) if folder != root else "."
            folders.append({
                "path":         rel,
                "name":         folder.name if folder != root else "(root)",
                "role":         fd.get("role", "Custom"),
                "purpose":      fd.get("purpose", ""),
                "depth":        fd.get("depth", ""),
                "token_budget": bd.get("token_budget", 8000),
                "file_limit":   bd.get("file_limit", 500),
                "connections":  conns,
                "has_smart":    sm.exists(),
                "has_settings": sf.exists(),
                "has_ignore":   (folder / ".smartignore").exists(),
                "has_laws":     (folder / "laws").exists(),
            })
        return {"root": str(root), "folders": folders}

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

    server = HTTPServer((args.host, args.port), Handler)
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
