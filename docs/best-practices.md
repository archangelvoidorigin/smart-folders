# Best Practices

## Folder Design

**One role per folder.** A folder that is both a Knowledge Keeper and a Creator is a folder without a clear purpose. Split it.

**Purpose in one sentence.** If you can't describe a folder's purpose in one sentence, it's trying to do too many things. The sentence forces clarity.

**Shallow hierarchies first.** Start flat. Add depth only when a folder's contents genuinely split into distinct concerns. A folder with 200 files of the same type doesn't need sub-folders — it needs better naming.

**Name folders for what they contain, not what they do.** `components/` not `create-components/`. The role field covers the "what it does" — the name covers the "what's in it".

## Token Budget

**8,000 tokens is the right default.** It's enough for a focused task. If a folder's instructions alone exceed this, the folder is either too broad or the instructions need pruning.

**Raise the budget at the root, lower it at the leaf.** Root-level folders can have higher budgets (12k–20k) because they set context. Leaf folders doing specific work should be tighter (4k–8k).

**Budget the instructions, not the contents.** The budget is for what the agent loads, not what the folder contains. A folder can have 500 files and a 4,000-token budget if the instructions are precise about what to load.

## Laws

**Keep laws short and absolute.** A law with exceptions isn't a law — it's a guideline. Move exceptions into the Instructions section.

**Three categories only:** Never, Always, If-Then. Anything else is a preference, not a law.

**Test your laws.** After writing a law, ask: "Could an agent misinterpret this?" If yes, rewrite it. Ambiguous laws get ignored.

## Connections

**Document what you know, not what you guess.** If you're not sure a folder feeds into another, leave it blank. A wrong connection is worse than no connection — it misleads routing.

**Connections are read by agents, not enforced by the system.** The system validates that connection targets exist. It does not enforce data flow. Use clear Purpose and Instructions to make connections meaningful.

## Adapters

**Use `smart-folder.md` as source, convert to agent formats.** Don't maintain six files manually. Write `smart-folder.md`, run `convert.py`, commit the generated files.

**Put adapter files at the root of the folder they describe.** `CLAUDE.md` in `src/components/` describes `src/components/`. Don't put it one level up.

## Anti-Slop Checklist

Before calling any work in a Smart Folder complete:

- No placeholder text left (`[your name]`, `[describe purpose]`)
- No duplicate instructions — if the parent says it, the child doesn't need to repeat it
- No laws that say the same thing twice in different words
- No connections that point to non-existent folders
- No token budgets set to 50,000 "just in case"
- No instructions that start with "You might want to consider..."

## The Minimum Viable Smart Folder

If you have five minutes:

1. Create `smart-folder.md`
2. Fill in Purpose (one sentence)
3. Fill in Role (pick from the list)
4. Fill in two Instructions

That's a working smart folder. Everything else is optional depth.
