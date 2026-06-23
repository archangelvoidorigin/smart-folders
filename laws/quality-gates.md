# Quality Gates

Quality gates are checks that must pass before work in a folder is considered complete. They are not suggestions — they are the definition of done.

---

## Gate 1: Completeness

- [ ] All requested changes are implemented — no stubs, no TODOs left behind
- [ ] All files created are syntactically valid (code compiles/parses, JSON is valid, etc.)
- [ ] All cross-references and connections point to folders/files that exist

## Gate 2: Scope Compliance

- [ ] Every file created or modified belongs within this folder's stated purpose
- [ ] No files were created outside this folder without explicit permission
- [ ] Token budget was not exceeded

## Gate 3: Law Compliance

- [ ] No files were deleted without permission
- [ ] No boundaries in `.smartignore` or `settings.json` were violated
- [ ] No `laws/` files were modified
- [ ] No fabricated content, paths, or API signatures were introduced

## Gate 4: Legibility

- [ ] A developer unfamiliar with this session can understand what changed and why
- [ ] If a `chronicles/` directory exists, the session's changes are documented there
- [ ] `smart-folder.md` reflects the current state of the folder if its purpose changed

## Gate 5: Connection Integrity

- [ ] Folders this one feeds into are not broken by the changes made here
- [ ] If the output format changed, downstream connections are updated or flagged

---

## Anti-AI-Slop Checklist

Before submitting output, verify:
- [ ] No generic boilerplate was added that doesn't serve this folder's specific purpose
- [ ] No duplicate content that already exists elsewhere
- [ ] No vague language ("this could be improved later", "TODO: add real logic")
- [ ] No hallucinated dependencies or tools
- [ ] No unnecessary complexity added beyond what the task required

---

Failing any gate means the work is not complete. Fix the issue before reporting done.
