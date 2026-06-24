# Design Skills Inventory — 148 Skills Installed

> All skills live in `~/.agents/skills/`. Auto-discovered by OpenCode and 40+ agents.

---

## Tier 1 — Major Design Frameworks (Core Systems)

| Skill | Source | Stars | What It Does |
|-------|--------|-------|-------------|
| **design-taste-frontend** | Taste Skill (Leonxlnx) | 37.4k | 3-param design equalizer: variance(1-10), motion(1-10), density(1-10) |
| **high-end-visual-design** | Taste Skill variant | — | Aggressive typography, premium portfolios, landing pages |
| **gpt-taste** | Taste Skill variant | — | Strict anti-slop rules, opinionated design for GPT/Codex |
| **minimalist-ui** | Taste Skill variant | — | Editorial clean UI, Notion/Linear-inspired restraint |
| **industrial-brutalist-ui** | Taste Skill variant | — | Swiss typography, sharp contrast, raw mechanical layout |
| **stitch-design-taste** | Taste Skill variant | — | Google Stitch-compatible semantic design rules |
| **full-output-enforcement** | Taste Skill variant | — | Forces complete code, no placeholders or skip patterns |
| **image-to-code** | Taste Skill variant | — | Generates premium design image → analyzes → faithful code |
| **redesign-existing-projects** | Taste Skill variant | — | Audits existing UI, fixes layout/spacing/hierarchy |
| **impeccable** | Paul Bakaus | 35.8k | Shared design vocabulary, 23 commands (polish/audit/critique/etc) |
| **interface-design** | Dammyjay93 | 5k | Persistent design decisions across sessions, zero stylistic drift |
| **frontend-design-pro** | claudekit | 232 | 11 distinct aesthetics with master prompts + ready code |
| **theme-factory** | Anthropic official | — | 10 curated themes with CSS vars, typographic scales, color combos |

## Tier 2 — Anthropic Official Skills

| Skill | Purpose |
|-------|---------|
| **figma** | Figma → production code with 1:1 fidelity |
| **brand-guidelines** | Applies brand colors/fonts/spacing/tone to all output |
| **canvas-design** | Visual art, posters, compositions → PNG/PDF export |
| **skill-creator** | Meta-skill: create custom skills from your design system |

## Tier 3 — Animation & Micro-Interaction

| Skill | Focus |
|-------|-------|
| **emil-design-eng** | Emil Kowalski's animation patterns, page transitions, micro-interactions |
| **review-animations** | Animation code review and quality checks |
| **animation-principles** | Core animation theory applied to UI |
| **motion-system** | Design system motion specs and choreography |
| **gesture-patterns** | Touch/gesture interaction patterns |

## Tier 4 — Designer Skills (63 skills, full design cycle)

### Strategy & Research
`a-b-test-design`, `affinity-diagram`, `card-sort-analysis`, `competitive-analysis`, `design-brief`, `design-principles`, `design-sprint-plan`, `diary-study-plan`, `empathy-map`, `experience-map`, `interview-script`, `jobs-to-be-done`, `journey-map`, `north-star-vision`, `opportunity-framework`, `service-blueprint`, `stakeholder-alignment`, `summarize-interview`, `survey-design`, `user-persona`

### UX & Usability
`accessibility-audit`, `accessibility-test-plan`, `aesthetic-usability`, `click-test-plan`, `design-critique`, `design-debt-audit`, `design-qa-checklist`, `design-review-process`, `error-handler-ux`, `heuristic-evaluation`, `prototype-strategy`, `search-ux`, `test-scenario`, `usability-test-plan`, `user-flow-diagram`

### UI & Visual Design
`color-system`, `critique-color`, `critique-typography`, `critique-visual-hierarchy`, `critique-composition`, `critique-brand-consistency`, `critique-information-density`, `dark-mode-design`, `data-visualization`, `form-design`, `icon-system`, `illustration-style`, `layout-grid`, `loading-states`, `localization-design`, `navigation-patterns`, `onboarding-design`, `responsive-design`, `spacing-system`, `theming-system`, `typography-scale`, `visual-hierarchy`, `wireframe-spec`

### Design Systems & Handoff
`component-spec`, `design-impact-reporting`, `design-negotiation`, `design-rationale`, `design-system-adoption`, `design-system-governance`, `design-token`, `design-token-audit`, `documentation-template`, `handoff-spec`, `naming-convention`, `pattern-library`, `state-machine`, `version-control-strategy`

### Design Ops
`business-design`, `case-study`, `content-strategy`, `design-system-governance`, `metrics-definition`, `presentation-deck`, `research-repository`, `team-workflow`, `ux-writing`

## Tier 5 — Vercel Agent Skills (Technical Quality)

`deploy-to-vercel`, `vercel-cli-with-tokens`, `vercel-composition-patterns`, `vercel-optimize`, `vercel-react-best-practices`, `vercel-react-native-skills`, `vercel-react-view-transitions`, `web-design-guidelines`, `writing-guidelines`

## Tier 6 — Image Generation (Taste Skill bundle)

`brandkit` — Brand identity boards: logos, colors, typography, mockups
`imagegen-frontend-web` — Awwwards-level reference images
`imagegen-frontend-mobile` — iOS/Android mockup concepts

---

## Architecture Notes for Future System

### Layering Strategy
```
Layer 1: TASTE / IMPECCABLE — aesthetic direction (the "eye")
Layer 2: DESIGNER SKILLS — process & research (the "method")
Layer 3: VERCEL — technical quality (the "engineer")
Layer 4: EMIL KOWALSKI — animation polish (the "soul")
Layer 5: INTERFACE DESIGN — persistence (the "memory")
```

### Key Insight
Skills are just SKILL.md files with frontmatter. To combine them:
1. **Merge SKILL.md files** from different sources into a meta-skill
2. **Layer by priority** — some skills give aesthetic rules, others give process
3. **Create a composer skill** that loads specific sub-skills per task type

### Potential Conflict Areas
- Taste Skill and Impeccable both set design direction — use one per project
- Multiple critique skills may produce conflicting reports
- Some skills set font/color rules that override others

### Storage Location
All 148 skills: `~/.agents/skills/`
Project-level overrides: `.opencode/skills/`
