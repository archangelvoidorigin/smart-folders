# Never Rules — Absolute Prohibitions

These rules are absolute. No agent, no instruction, no child folder can override them.

---

## Never Delete

- Never delete `smart-folder.md` or `settings.json`
- Never delete the `laws/` directory or any file inside it
- Never delete files without explicit, unambiguous permission from the user
- Never delete archive or chronicle entries — they are permanent record

## Never Ignore Boundaries

- Never access files listed in `.smartignore`
- Never load files whose patterns match the `cannot_see` list in `settings.json`
- Never exceed the `token_budget` defined in `settings.json`
- Never access parent folder contents by navigating with `../` unless the folder's instructions explicitly permit it

## Never Violate Scope

- Never create files outside the folder's defined purpose
- Never create duplicate functionality that already exists elsewhere in the system
- Never modify files in sibling or parent folders unless explicitly instructed
- Never add dependencies that aren't approved in the folder's instructions

## Never Modify Laws

- Never modify `laws/` files without explicit user permission
- Never create rules that contradict a parent folder's laws
- Never treat a law as optional — laws are absolute

## Never Fabricate

- Never invent content, data, or connections that don't exist
- Never hallucinate file paths, function names, or API signatures
- Never claim something is done when it isn't
- Never guess when unsure — ask for clarification

---

These rules apply to all agents in all folders unless a rule is explicitly scoped to a specific folder type (e.g., `Staging` folders may have relaxed scope restrictions). Even then, the core prohibitions — never delete laws, never fabricate, never exceed budget — are universal.
