# Guild + BMAD Pipeline Guide

---

## What this is

Guild and BMAD are two separate frameworks that cover different parts of the product development lifecycle. This guide explains how they connect, who does what, and in what order.

**BMAD** handles the business and engineering layers: requirements (Analyst), product strategy (PM), system architecture (Architect), sprint planning (SM), development (Dev), testing strategy (TEA), and documentation (Tech Writer).

**Guild** handles product design: research (Ranger), interaction design (Rogue), visual design (Mage), content strategy (Warlock), design QA (Sage), developer handoff (Healer), and design system engineering (Tinker).

The pipeline is the integration point — it orchestrates both frameworks in the right order so their outputs feed each other. Guild reads BMAD's PRD and architecture to ground design decisions. BMAD's dev loop reads Guild's UX spec and stories to implement them correctly.

---

## The rule

**BMAD plans → Guild designs → BMAD builds.**

Never go from PM straight to Dev on UI-facing work. Guild is the required layer between planning and building. Stories created without a Guild design sprint will be missing component specs, interaction states, copy, and accessibility requirements — the build loop fills those gaps with guesses, which become bugs.

---

## How to run it

| Command | When to use |
|---------|-------------|
| `/guild-quest` | Full pipeline from scratch — BMAD planning through Guild design through build and documentation. One command. |
| `/guild-design-sprint` | Design only — research through handoff. Stops before build. Use when you want to review artifacts before dev starts. |
| `/guild-agent-guild-master QS` | Skip research — design through sprint planning. Use when research already exists. |
| `/bmad-autonomous-build` | Build only — picks up from wherever sprint-status.yaml left off. Use when design is done and you just need to build. |

---

## The full pipeline

### Phase Pre — "The Charter" · BMAD Planning (Greenfield only)

Skip if PRD, Architecture, and Epics already exist. For brownfield, check what's missing and start from there.

This phase is **interactive** — BMAD workflows ask clarifying questions and require input. You stay engaged.

| Step | Agent | Output |
|------|-------|--------|
| Pre-1 | Analyst | Project brainstorm + context document |
| Pre-2 | Analyst | Market and domain research document |
| Pre-3 | PM | Product Requirements Document (PRD) — *required* |
| Pre-4 | Architect | Architecture Document — *required* |
| Pre-5 | PM | Epics and User Stories |

Nothing in Guild starts until PRD, Architecture, and Epics exist. These are the foundation every downstream agent reads.

---

### Phase 0 — "Set the Compass" · Design Direction Gate

**Command:** `/guild-design-direction` (interactive — run in main conversation, not as subagent)

Mage asks 6 questions before any visual work begins:

1. **Anchor reference** — a product whose visual style you admire
2. **Personality adjectives** — 3–5 words that describe the feel
3. **Density preference** — dense / balanced / airy
4. **Motion energy** — static / subtle / expressive
5. **Color story** — the emotional role of color in this product
6. **What to avoid** — patterns, styles, or references that are off-limits

Mage synthesizes the answers into a **Design Direction Brief**. Every downstream Guild agent receives the full brief and executes against it. This is what prevents the pipeline from averaging competitors into generic output.

**Gate:** If any section is missing or vague, Mage pushes back once before continuing.

---

### Phase 0.5 — "Pour the Slab" · Foundation Gate

**Command:** `/guild-agent-sage DSF` (design-system foundation)

Sage audits the token and primitive layer before page-level work starts.

| Verdict | What happens |
|---------|-------------|
| **PASS** | Proceed to Phase 1 |
| **CONDITIONAL** | Proceed, but Healer's first stories must fix missing tokens/primitives before page stories |
| **FAIL** | Stop. Tinker fixes the foundation. Page-level work cannot start. |

---

### Phase 1 — "Scouting" · Research

**Step 1 — Visual Audit (Ranger)**
Real browser required. Ranger visits competitors and searches Dribbble/Behance, filtered through the design direction brief. Gate: 3+ competitors must have real screenshot evidence before proceeding.

**Step 2 — Research Synthesis (Ranger)**
Combines visual audit with existing interviews, stakeholder feedback, and Confluence docs into a single synthesis document.

---

### Phase 2 — "Crafting" · Design

| Step | Agent | Output |
|------|-------|--------|
| 3 | Warlock | All screen copy, labels, empty states, error messages — before layout |
| 4 | BMAD Editorial (Prose) | Polished copy |
| 5 | Rogue | User flows, wireframes, state diagrams, interaction maps |
| 6 | Mage | Visual design applied against direction brief |
| 7 | Sage | Design QA — GO / CONDITIONAL GO / NO-GO |

Sage NO-GO halts the pipeline and loops back to Rogue.

---

### Phase 3 — "Trial by Fire" · Review

Four lenses in sequence — each catches different failure modes:

| Step | Tool | What it catches |
|------|------|----------------|
| 8 | `bmad-party-mode` (Tavern) | Gaps, contradictions, missed edge cases across multiple agent perspectives |
| 9 | `bmad-review-edge-case-hunter` | Boundary conditions and unhandled paths |
| 9b | `bmad-review-adversarial-general` | Challenges every design decision cynically — assumptions, risks, things that will break |
| 9c | `bmad-editorial-review-structure` | Structural issues in artifacts — cuts, reorganization, simplification |

Critical findings from any lens loop back to the relevant design step before proceeding.

---

### Phase 4 — "Forging the Blueprint" · Handoff

| Step | Agent/Tool | Output |
|------|-----------|--------|
| 10 | Healer | Dev handoff spec — component inventory, spacing, states, copy, ARIA |
| 11 | Sage `/guild-agent-sage PR` | Pre-handoff quality gate — NO-GO loops back |
| 12 | Healer `/guild-agent-healer UX` | UX_Design.md — BMAD-compatible, consumed by dev-story |
| 13 | Healer `/guild-agent-healer JS` | Dev subtasks with Given/When/Then acceptance criteria |
| 13b | Architect `/implementation-readiness` | **Gate:** validates PRD + UX + Architecture + Epics are aligned before build starts |

The implementation readiness check is **interactive**. It uses an adversarial approach to find gaps before they become build-loop bugs. A FAIL here stops the quest.

---

### Phase 5 — "The Forge" · Autonomous Build

From here, no human input is required. The build loop runs autonomously until all stories are done.

**Step 14 — Sprint Planning (SM)**
Creates `sprint-status.yaml` — the source of truth for the entire build loop.

**Step 15 — Dev Loop**

```
For each story:
  15a. Create story (or use prefetched)
  15b. Dev story — implement
  15c. Code review + prefetch next story
  15d. Review-fix loop (up to 3 cycles)
  15e. Commit completed story

At each epic boundary:
  15f-i.  Retrospective — synthesize what happened
  15f-ii. Course correction — update PRD, architecture, UX spec from findings
  15f-iii. Transition — commit and continue
```

Stop conditions: 3 consecutive review failures, unresolvable course correction blocker, missing required artifact, fundamental design flaw in tests.

---

### Phase 6 — "Chronicle & Seal" · Test Architecture + Documentation

These steps use BMAD agents, not Guild agents. Guild owns product design. BMAD owns quality engineering and technical writing. Keeping them in BMAD means their knowledge bases stay current automatically when BMAD ships updates.

**Step 16 — Test Architecture Review (BMAD TEA)**

TEA reviews what was built against what should be tested. This project uses Atrium's built-in browser for UI testing — TEA is briefed accordingly and skips Playwright-specific tooling.

TEA produces:
- Test level coverage gaps (unit / integration / e2e)
- Priority gaps (P0–P3) — what must exist before production
- Contract testing needs (API boundaries requiring Pact verification)
- CI pipeline recommendations
- Risk governance verdict: **GO / CONDITIONAL / NO-GO**

TEA NO-GO halts the quest. Conditional items become follow-up stories.

**Step 17 — Developer Documentation (BMAD Tech Writer / Paige)**

Paige documents the completed product for developers. Inputs: component registry, UX spec, handoff specs, test architecture review, retrospectives.

Produces: developer README, component reference, architecture notes, test guide.

---

## Running just the build loop

If design is done and stories are ready:

```bash
/bmad-autonomous-build
```

Reads `sprint-status.yaml` and runs the dev loop from wherever it left off. No design steps, no questions.

---

## Component registry

Maintained throughout the quest at `{output_root}/guild-artifacts/component-registry-{product_slug}.md`. Every component is documented with props, states, design tokens, ARIA notes, and Storybook/Figma readiness. Status tracks whether each component is `existing`, `extended`, `proposed`, or `built`.

The registry is the design-to-development contract. Warlock seeds it. Rogue adds interaction components. Mage adds visual specs. Healer finalizes for handoff. Dev updates it as components are built.

---

## Design system integration

Provide `design_system_path` (local Storybook repo) or `design_system_repo` (GitHub repo) and every agent checks it before creating components. Existing components are reused. Extensions are flagged. New components are proposed as system additions. Tinker manages the design system layer.

---

## Agent ownership

| Domain | Owner |
|--------|-------|
| Requirements, PRD | BMAD Analyst + PM |
| Architecture | BMAD Architect |
| Sprint planning | BMAD SM |
| Product design (all phases) | Guild |
| Design system engineering (Figma components, tokens, Storybook/Code Connect parity) | Guild Tinker 🔧 |
| Information architecture & stakeholder system maps | Guild Cartographer 🗺️ |
| Development | BMAD Dev |
| Test architecture | BMAD TEA |
| Technical documentation | BMAD Tech Writer |
| Multi-model raids | Atrium (Raid / Quest / Tavern) |

**On-demand specialists.** Tinker and Cartographer aren't fixed steps in the sequential phase list — they're called when the work needs them. Tinker backs the Phase 0.5 foundation gate (and any design-system/component work); Cartographer is invoked whenever a product area needs information architecture (sitemaps, content models, navigation models) or a stakeholder-facing system map. Both can be run directly (`/guild-agent-tinker`, `/guild-agent-cartographer`) or pulled in by the Guild Master mid-pipeline.
