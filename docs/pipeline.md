# Guild + BMAD Pipeline Guide

How Guild and BMAD work together — from the first design question to shipped code.

---

## The rule

**PM scopes the change → Guild runs the design sprint → Dev implements.**

Never go straight from PM to Dev on any UI-facing work. Guild is the required step between planning and building. Stories generated without a Guild design sprint will be missing component specs, interaction states, copy, and accessibility requirements — the dev loop will fill in those gaps with guesses.

---

## Two ways to run the pipeline

| Command | What it does |
|---------|-------------|
| `/guild-design-sprint` | Runs the design pipeline only (research through handoff). Stops before build. Use when you want to review artifacts before handing off to dev. |
| `/guild-quest` | Runs the full pipeline end-to-end — design questions through autonomous build. One command, no human in the loop after the opening questions. |

`/guild-quick-sprint` skips research and goes straight to design if you already have research artifacts.

---

## The full pipeline — 15 steps across 5 phases

### Before anything starts: the opening questions

`/guild-quest` begins by gathering context. It asks:

- **What are we building?** — product name and slug
- **Who is it for?** — target user and industry
- **Competitors to audit?** — URLs or product names for visual research
- **Key features?** — what the product needs to do
- **Design system?** — whether an existing system (e.g., Storybook repo) should be respected

Once answered, quest variables are locked and passed to every downstream agent. You won't be asked again.

---

### Phase 0 — "Set the Compass" · Design Direction Gate

**Command:** `/guild-design-direction` (run interactively, not as a subagent)

Mage asks 6 questions before any visual work begins:

1. **Anchor reference** — a product whose visual style you admire (not necessarily a competitor)
2. **Personality adjectives** — 3–5 words that describe the feel (e.g., "precise, calm, technical")
3. **Density preference** — dense / balanced / airy
4. **Motion energy** — static / subtle / expressive
5. **Color story** — the emotional role of color in this product
6. **What to avoid** — patterns, styles, or references that are explicitly off-limits

Mage synthesizes the answers into a **Design Direction Brief** saved to `{output_root}/guild-artifacts/design-direction-brief.md`. Every downstream agent — Ranger, Rogue, Mage, Warlock — receives the full brief and executes against it. This is what prevents the pipeline from averaging competitors into a generic AI-dashboard result.

**Gate:** If any of the 6 sections is missing or vague, Mage pushes back once before continuing.

---

### Phase 0.5 — "Pour the Slab" · Foundation Gate

**Command:** `/guild-system-foundation`

Sage audits the token and primitive layer before any page-level work starts. It checks:

- **Token layer** — color, spacing, motion, shadow, typography (scale + weights), radius
- **Primitive layer** — Button, Input, Select, ChipGroup, Field, Card, Badge, IconButton, Tooltip, Skeleton
- **Usage discipline** — inline `<select>`, hardcoded hex colors, raw `transition-all`, inline component definitions in pages

Sage returns one of three verdicts:

| Verdict | What happens |
|---------|-------------|
| **PASS** | Proceed to Phase 1 |
| **CONDITIONAL** | Proceed, but Healer's first sprint stories must fix the missing tokens/primitives before any page-level stories |
| **FAIL** | Stop. Add missing tokens and primitives. Page-level work cannot start. |

If FAIL, the quest asks: "Fix foundation now (recommended), or accept the debt and proceed?" Your answer is recorded in the artifact.

---

### Phase 1 — "Scouting" · Research

**Step 1 — Visual Audit (Ranger)**
Ranger opens a real browser (Atrium preferred, Playwright fallback), visits competitor products, searches Dribbble and Behance, and captures screenshots. The design direction brief filters the audit — Ranger evaluates what it finds through the lens of your anchor and personality, not as a neutral survey.

Gate: at least 3 competitors must have real screenshot evidence. If screenshots fail, the audit re-runs before proceeding. No screenshots = no visual audit.

**Step 2 — Research Synthesis (Ranger)**
Ranger synthesizes the visual audit with any existing research artifacts, interviews, and Confluence documentation into a single research synthesis document.

---

### Phase 2 — "Crafting" · Design

**Step 3 — Content & Microcopy (Warlock)**
Warlock writes all screen copy, labels, empty states, error messages, and microcopy — before any flows are designed, so Rogue designs around real words, not lorem ipsum.

**Step 4 — Editorial Review (BMAD)**
`/bmad-editorial-review-prose` polishes the copy before it gets locked into layouts.

**Step 5 — Interaction Design (Rogue)**
Rogue produces user flows, swim lanes, wireframes, state diagrams, and interaction maps. Density and motion preferences from the design direction brief govern layout and transition choices.

**Step 6 — Visual Design (Mage)**
Mage applies visual design. The anchor reference, color story, and personality adjectives drive every visual choice. When two options are equally valid, the one closer to the anchor wins.

**Step 7 — Design QA (Sage)**
Sage reviews for accessibility, design system compliance, and quality.

| Sage verdict | What happens |
|-------------|-------------|
| **GO** | Continue |
| **CONDITIONAL GO** | Continue with noted conditions |
| **NO-GO** | Quest halts. Report findings to user. Pipeline loops back to Rogue. |

---

### Phase 3 — "Trial by Fire" · Review

**Step 8 — Multi-Agent Review**
`/bmad-party-mode` brings multiple BMAD agents into a review conversation — gaps, contradictions, and missed edge cases surface here.

**Step 9 — Edge Case Sweep**
`/bmad-review-edge-case-hunter` sweeps every branching path and boundary condition. Critical findings loop back to the relevant design step.

---

### Phase 4 — "Forging the Blueprint" · Handoff

**Step 10 — Dev Handoff (Healer)**
Healer produces the complete dev handoff spec — component inventory, spacing specs, state coverage, copy, and ARIA notes.

**Step 11 — Pre-Handoff Gate (Sage)**
Full quality gate. NO-GO loops back to fix issues before stories are created.

**Step 12 — UX Spec**
`/guild-ux-spec` packages all Guild artifacts into a single `UX_Design.md` compatible with BMAD's dev-story workflow.

**Step 13 — Story Generation**
`/guild-jira-stories` generates dev subtasks from the design artifacts with Given/When/Then acceptance criteria.

---

### Phase 5 — "The Forge" · Autonomous Build

From here, no human input is required. The quest runs the dev loop autonomously until all stories are done.

**Step 14 — Sprint Planning (BMAD SM)**
`/bmad-sprint-planning` creates `sprint-status.yaml` from the generated epics and stories. This file is the source of truth for the entire build loop.

**Step 15 — Dev Loop**

The loop runs until every epic and its retrospective are marked `done` in `sprint-status.yaml`:

```
For each story:
  1. Create story (or use prefetched)
  2. Dev story — implement
  3. Code review + prefetch next story
  4. Review-fix loop (up to 3 cycles)
  5. Commit completed story

At each epic boundary:
  6a. Retrospective — synthesize what happened
  6b. Course correction — update PRD, architecture, UX spec from retrospective findings
  6c. Transition — commit, then continue to next epic
```

The loop stops and reports to you if:
- 3 review cycles fail on the same story
- Course correction finds an unresolvable blocker
- A required artifact (PRD, architecture, UX spec) is missing
- Tests fail in a way that suggests a fundamental design flaw

When everything is done:
```
⚔️ AUTONOMOUS BUILD COMPLETE
Stories: [N] completed
Epics: [N] completed with retrospectives
Course corrections: [N] applied
```

---

### Phase 6 — "Chronicle & Seal" · Test Architecture + Documentation

Runs after all epics and retrospectives are complete. These are BMAD agents, not Guild agents — the boundary is intentional. Guild owns product design. BMAD owns everything else including quality engineering and technical writing.

**Step 16 — Test Architecture Review (BMAD TEA)**

TEA reviews what was built against what should be tested. Because this project uses Atrium's built-in browser for UI testing rather than Playwright, TEA is briefed to apply its strategy knowledge in that context and skip Playwright-specific tooling recommendations.

TEA produces:
- Test level coverage assessment (unit / integration / e2e gaps)
- Priority gaps by P0–P3 — what must exist before production
- Contract testing needs (API boundaries requiring Pact verification)
- CI pipeline recommendations
- Risk governance verdict: **GO / CONDITIONAL / NO-GO**

A NO-GO halts the quest. Conditional items become follow-up stories.

**Step 17 — Developer Documentation (BMAD Tech Writer / Paige)**

Paige documents the completed product for developers. Inputs: component registry, UX spec, handoff specs, test architecture review, retrospectives.

Paige produces:
- Developer README (setup, env vars, how to run and test)
- Component reference (public API of each component from the registry)
- Architecture notes (key design decisions, data flow, integrations)
- Test guide (how to run tests, what CI checks, how to add coverage)

---

**Why BMAD, not Guild, for Phase 6:**
TEA and Paige live in BMAD's bundle. When BMAD ships updates to TEA's test knowledge base or Paige's documentation standards, those flow in automatically. Merging them into Guild agents would mean owning that maintenance forever. Guild = product design. BMAD = everything else.

---

## Running just the dev loop

If design is already done and stories are ready, you can skip to the build loop directly:

```bash
/bmad-autonomous-build
```

This reads `sprint-status.yaml` and runs the dev loop from wherever you are — no design steps, no questions.

---

## Component registry

Throughout the quest, a living component registry is maintained at `{output_root}/guild-artifacts/component-registry-{product_slug}.md`. Each component is documented with props, states, design tokens, ARIA notes, and Storybook/Figma readiness. Status tracks whether each component is `existing` (from design system), `extended`, `proposed` (new, needs approval), or `built` (implemented).

The registry is the design-to-development contract. Healer writes it. Dev updates it as components are built.

---

## Design system integration

If you provide a `design_system_path` (local Storybook repo) or `design_system_repo` (GitHub repo), every agent that creates components checks it first. Existing components are reused. Extensions are flagged. Only genuinely new components get proposed as additions to the system.

This keeps the quest output aligned with your design system instead of generating a parallel set of one-off components.
