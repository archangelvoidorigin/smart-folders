# Role Definitions

Each Smart Folder has a semantic role. The role shapes how agents interpret the folder's purpose, what they are allowed to do, and how they prioritize their work.

---

## Knowledge Keeper

**Metaphor:** The library  
**Function:** Stores, organizes, and surfaces information. Does not create — curates.

**Default behaviors:**
- Agents read before they write
- New content is indexed and connected to existing knowledge
- Quality standards are high — garbage in, garbage out
- Connections to other folders are documented

**Good for:** Documentation, research archives, knowledge bases, wikis, references

---

## Creator

**Metaphor:** The workshop  
**Function:** Builds and creates things. This is where raw materials become products.

**Default behaviors:**
- Agents have broader permissions to create new files
- Output is the primary concern — ship working things
- Iteration is expected — drafts, revisions, and versions are normal
- Connections to Knowledge Keeper folders for source material

**Good for:** Source code, design files, written content, prototypes, product work

---

## Architect

**Metaphor:** The blueprint room  
**Function:** Designs systems, schemas, and patterns. Defines how things are built, not what they build.

**Default behaviors:**
- Agents think before they act — design decisions are deliberate
- Changes here affect everything downstream — proceed carefully
- Schemas are versioned and backward-compatible by default
- Connections to Creator folders that implement the designs

**Good for:** System architecture, data schemas, API contracts, design systems, infrastructure

---

## Connector

**Metaphor:** The switchboard  
**Function:** Links tools, workflows, and systems. Manages integrations and data flow.

**Default behaviors:**
- Agents focus on interfaces, not implementations
- Changes are validated against both sides of each connection
- Logging and observability are required
- Connections to all folders this one bridges

**Good for:** Integration configs, pipeline definitions, webhook handlers, data transforms

---

## Chronicler

**Metaphor:** The scribe  
**Function:** Documents everything. Turns activity into permanent, searchable record.

**Default behaviors:**
- Agents append, never overwrite historical entries
- Format is consistent: date, event, reasoning, outcome
- Nothing is deleted — everything is archived
- Connections to every folder being chronicled

**Good for:** Session logs, decision records, changelogs, post-mortems, chronicles

---

## Enabler

**Metaphor:** The toolbox  
**Function:** Provides tools, utilities, and capabilities that other folders use.

**Default behaviors:**
- Agents maintain backward compatibility — breaking changes require version bumps
- Tools are documented with examples
- Performance matters — these tools run frequently
- Connections to all folders that depend on this one

**Good for:** Scripts, utilities, shared libraries, CLI tools, helper functions

---

## Archive

**Metaphor:** The vault  
**Function:** Preserves history and past states. Read-mostly.

**Default behaviors:**
- Agents read freely, write rarely
- Nothing is deleted from an Archive — only added
- Content is timestamped and immutable once written
- Connections to the folders this archive preserves

**Good for:** Old versions, historical snapshots, deprecated code, past projects

---

## Staging

**Metaphor:** The sandbox  
**Function:** Experiments safely. Ideas that are not yet real live here.

**Default behaviors:**
- Agents have maximum freedom — this is where things can break
- Nothing in Staging is production — do not depend on it
- Content moves to another role folder once validated
- Connections to Creator or Architect folders it graduates to

**Good for:** Experiments, prototypes, drafts, untested ideas, playground code

---

## Custom

**Metaphor:** Yours to define  
**Function:** For roles that don't fit the above. Define your own in the folder's `smart-folder.md`.

**Default behaviors:**
- No defaults — all behavior must be explicit in `smart-folder.md`
- Agents treat undefined behavior as not permitted
- Document the role's logic in `role-definitions.md` inside the folder

---

## Role Inheritance

When a child folder has a different role than its parent, both roles apply:
- Parent role sets the **outer boundary** (what the space permits)
- Child role sets the **inner behavior** (how the agent works within that space)

A `Creator` inside a `Knowledge Keeper` creates content, but only content that belongs in the Knowledge Keeper's domain.

A `Staging` inside a `Creator` experiments freely, but only with things the Creator folder is meant to build.

If the roles conflict (e.g., a `Staging` inside an `Archive`), the parent's absolute constraints win. An Archive's immutability law cannot be overridden by a child's freedom.
