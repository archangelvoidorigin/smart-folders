# Contributing

## Before You Start

Check open issues before opening a new one. Check the roadmap before building a feature — if it's planned for v0.2.0, coordinate rather than duplicate.

## Issues

**Bug reports:** Include the output of `python scripts/validate.py <folder>` and the contents of your `settings.json`. State what you expected and what happened.

**Feature requests:** Explain the problem you're solving, not the solution you want. "I need X because Y" is more useful than "add feature X."

## Pull Requests

1. One PR per concern — don't bundle unrelated changes
2. Run `make validate-examples` before submitting — examples must pass validation
3. If you add a new role, update `settings-schema.json`, `roles/role-definitions.md`, `map.py` (ROLE_COLORS), and `skill-navigate.py` (ROLE_KEYWORD_AFFINITY)
4. If you add a new agent, update `convert.py`, `adapters/`, and `settings-schema.json`
5. If you change the `settings-schema.json`, bump the version in the schema `$id`

## Code Style

- Python 3.8+ compatible
- No external dependencies in scripts
- Type hints on all function signatures
- No comments that restate what the code does — only explain why
- Scripts are standalone — no imports between scripts

## Testing

Smart Folders has no test runner beyond `validate.py` on the examples. New features should include or update an example that demonstrates the feature working.

```bash
make validate-examples
```

This must pass before any PR is merged.
