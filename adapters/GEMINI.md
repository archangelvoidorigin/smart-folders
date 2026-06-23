# GEMINI.md — Smart Folder Adapter (Gemini / Antigravity)

This folder is configured with the Smart Folder system, optimized for Gemini. Read this file first.

## Gemini-Specific Capabilities

Use these Gemini features where appropriate:
- **Multimodal**: if this folder contains images, audio, or video, use multimodal analysis
- **Search grounding**: for research tasks, ground responses in real-time search results
- **Code execution**: for data analysis, run code to verify results rather than estimating
- **Long context**: Gemini's 1M+ context window is powerful — but focused context still outperforms bloated context. Respect the token budget.

## How to Navigate This Folder

1. Read this file completely
2. Read `smart-folder.md` — folder-specific purpose, scope, and instructions
3. Read `settings.json` — role, boundaries, token budget, agent configuration
4. Read `.smartignore` — files and directories agents must not access
5. Read all files in `laws/` before doing any work

## Folder Hierarchy

Smart Folders use hierarchical instruction resolution:
- Parent folder instructions apply to all children unless explicitly overridden
- Child folder instructions add specificity and narrow scope
- Closer instructions win — child rules take precedence in conflicts
- Laws are absolute — no folder can override a law from an ancestor

## Gemini Working Rules

1. Read before acting — understand the folder's purpose fully before making changes
2. Use search grounding for research tasks, not cached knowledge
3. Use code execution to verify data analysis results
4. Use multimodal capabilities for visual content in this folder
5. Stay in scope — only operate within this folder's defined boundaries
6. Respect the token budget even with a large context window
7. Never modify `laws/` without explicit user permission

## Quality Checklist

Before finishing work in this folder:
- [ ] Does my output follow the folder's instructions and purpose?
- [ ] Did I respect all laws?
- [ ] Am I within the token budget?
- [ ] Did I use search grounding where appropriate?
- [ ] Did I verify data analysis with code execution?
- [ ] Did I maintain connections to folders this one feeds into?

## Need Help?

If instructions are unclear, ask for clarification. Do not guess or hallucinate answers. Smart Folders are explicit — if something is not stated, it is not permitted.
