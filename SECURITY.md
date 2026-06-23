# Security Policy

## Scope

Smart Folders is a set of configuration files and pure-stdlib Python scripts with
no external dependencies and no network surface — except `dashboard.py`, which
runs a local HTTP server bound to `localhost` by default. The relevant risk areas
are therefore:

- `dashboard.py` — runs whitelisted scripts via `subprocess` in response to local
  HTTP requests. Do not expose it to untrusted networks (avoid `--host 0.0.0.0`
  on shared machines).
- Any script that reads `settings.json` / `smart-folder.md` from an untrusted
  source — treat folders you didn't author as untrusted input.

## Reporting a Vulnerability

If you find a security issue, **do not open a public issue**. Instead, open a
[GitHub security advisory](https://github.com/ArchangelVoidOrigin/smart-folders/security/advisories/new)
or contact the maintainer directly.

Please include:

- A description of the issue and its impact
- Steps to reproduce
- The affected script(s) and version

You can expect an initial response within a few days. Fixes for confirmed issues
will be released as soon as practical, with credit to the reporter unless you
prefer to remain anonymous.

## Supported Versions

This project is pre-1.0; only the latest `main` is supported. Upgrade to the
newest commit before reporting.
