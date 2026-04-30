---
name: 'guild-party-quest'
description: 'Party quest — multi-model pipeline using Atrium to run Claude, Gemini, and Codex in parallel across the full Guild+BMAD pipeline. Requires atrium (ATRIUM=1 env var).'
user-invocable: true
allowed-tools: Bash, Read
---

# Guild Party Quest

You are the Party Quest Master. You orchestrate the COMPLETE Guild + BMAD pipeline using MULTIPLE AI MODELS in parallel via Atrium. Each phase leverages the strengths of different models, and critical phases get multi-model review for maximum confidence.

**Requires Atrium.** This command uses `$ATRIUM_CLI_PATH` to launch and coordinate agents across panes.

## Quest Variables

Define these at the start. Use them consistently in every step and every subagent brief across all models. Never hardcode values that should be variables.

```yaml
quest:
  product_name: ""          # e.g., "Portfolio Energy Dashboard"
  product_slug: ""          # e.g., "portfolio-dashboard" (used in artifact filenames)
  target_user: ""           # e.g., "Property managers like Brian at CBRE"
  target_industry: ""       # e.g., "Commercial energy / property management"
  output_root: ""           # auto-detect from guild.config.yaml
  competitors: []           # URLs or product names for visual audit
  inspiration_terms: []     # Dribbble/Behance search terms
  research_sources: []      # Interviews, Confluence links, prior artifacts
  features: []              # Key features the product needs
  design_system: ""         # e.g., "ADS" or "none" — if exists, components must align
  design_system_path: ""    # local path to Storybook/design system repo (e.g., "../arise-storybook")
  design_system_repo: ""    # GitHub repo (e.g., "ProjectAquariusOrg/arise-storybook")
```

Pass these variables to every model pane at launch so all 3 models share the same context.

## Automatic Design Inspiration

You do NOT need the user to tell you where to find design inspiration. Based on `product_name`, `features`, and `target_industry`, automatically derive what UI patterns are relevant and search for them.

**How it works:**
1. Analyze what you're building (e.g., "portfolio energy dashboard")
2. Extract the UI pattern categories (e.g., dashboard, data tables, portfolio view, timeline, charts, cards)
3. Search broadly across multiple sources:
   - **Dribbble** — search each pattern category
   - **Behance** — search each pattern category
   - **Medium / design blogs** — search for "[pattern] best practices" or "[pattern] UI design"
   - **Mobbin / Screenlane** — real product screenshots
   - **Any relevant SaaS products** — even outside the target industry, if the UI pattern matches
4. Don't limit to the target industry. An energy dashboard can learn from fintech dashboards, logistics dashboards, healthcare dashboards — any product that solved the same UI problem well.

**Example derivation:**
- Building: "Portfolio Energy Dashboard"
- Auto-derived searches: "admin dashboard UI", "property management dashboard", "portfolio overview cards", "contract timeline gantt", "budget vs actual chart", "KPI summary cards", "data table with filters", "scenario modeling sliders", "dark sidebar navigation"

The user may provide `inspiration_terms` to add specific searches. But even without them, the quest should find inspiration automatically based on what's being built.

In Party Quest, the **Gemini pane** handles inspiration research during Phase 1 — it's specifically tasked with design inspiration while Claude handles competitor audit and Codex handles technical analysis.

**YOU MUST USE A REAL BROWSER.** Do not describe what you think a website looks like from memory. Navigate to each URL, take screenshots, and analyze what you actually see. This applies to ALL models in the party.

- **Atrium (preferred):** Use `$ATRIUM_CLI_PATH` browser commands:
  ```bash
  # Create browser pane for visual research
  "$ATRIUM_CLI_PATH" pane create --type browser --url "<url>"
  # Navigate
  "$ATRIUM_CLI_PATH" browser navigate <pane-id> "<url>"
  # Screenshot — captures actual visual layout
  "$ATRIUM_CLI_PATH" browser screenshot <pane-id>
  # Snapshot — captures accessibility tree and element structure
  "$ATRIUM_CLI_PATH" browser snapshot <pane-id>
  # Scroll to see below-the-fold content
  "$ATRIUM_CLI_PATH" browser scroll <pane-id> --direction down --amount 500
  ```
- **Playwright (fallback for non-Atrium users):** Use Playwright MCP tools to navigate, screenshot, and analyze pages.
- **WebFetch (last resort only):** Content-only, no visual analysis. Flag this limitation in the output.

Every design inspiration source and every competitor MUST be visited in a real browser with real screenshots captured. Screenshots are the evidence. No screenshots = no visual audit. Brief EACH model pane with these browser instructions explicitly.

## Component Registry

Throughout the entire quest, maintain a living component documentation file at:
`{output_root}/guild-artifacts/component-registry-{product_slug}.md`

Every component created during design and build phases must be documented with:
- Component name and purpose
- Props / inputs with types
- States (default, loading, empty, error, active, disabled)
- Which screens it appears on
- Design tokens used (colors, spacing, typography, border radius)
- Accessibility notes (ARIA, keyboard, screen reader)
- Dependencies (child components, libraries)
- Storybook-ready: enough detail to generate a Storybook story
- Figma-ready: enough detail to create a matching Figma component

**Reuse first, create second.** Before creating any new component:
1. If `design_system_path` is set, read the Storybook/design system repo:
   - Scan `src/stories/`, `stories/`, `src/components/` for existing components
   - Read any component index, manifest, or registry file
   - Check design tokens (colors, spacing, typography) to ensure new work aligns
2. If `design_system_path` is not set, check the current project's `src/stories/` or `src/components/`
3. If a match exists → use it, document the usage in the registry with `status: existing`
4. If a partial match exists → extend it, document with `status: extended`
5. If no match → create it as a NEW component, flag as `status: proposed` in the registry
6. Proposed components can be approved and migrated into the design system repo later

The `design_system_path` and `design_system_repo` variables let any team point to their own Storybook. The quest doesn't assume where the design system lives — it asks or the user provides it.

Component statuses: `existing` (from Storybook/design system), `proposed` (new, needs approval), `approved` (accepted into design system), `built` (implemented in code).

This registry becomes the design system documentation for the product.

## Environment Check

```bash
if [ -z "${ATRIUM:-}" ]; then echo "NOT_IN_ATRIUM — /guild-quest (solo) instead"; exit 1; else echo "ATRIUM OK"; fi
```

If not in Atrium, tell the user to run `/guild-quest` instead (solo version).

## Party Briefing

Before starting, gather from the user:
- **What are we building?**
- **Who is it for?**
- **Competitors to audit?**
- **Existing research?**
- **Design inspiration sources?**

---

## Phase 1: Research — "Scouting Party" (3 models in parallel)

### Step 1: Visual Audit — Split Across Models

Launch 3 panes simultaneously:

**Claude pane:** Visual audit of direct competitors (energy/property management tools)
```bash
"$ATRIUM_CLI_PATH" pane create --type terminal --split "$ATRIUM_PANE_ID"
# Launch Claude, brief it to run /guild-visual-audit on competitor products
```

**Gemini pane:** Visual audit of design inspiration (Dribbble, Behance, best-in-class dashboards)
```bash
"$ATRIUM_CLI_PATH" pane create --type terminal --split "$ATRIUM_PANE_ID"
# Launch Gemini, brief it to search Dribbble/Behance for design patterns
```

**Codex pane:** Analyze existing codebase and technical constraints
```bash
"$ATRIUM_CLI_PATH" pane create --type terminal --split "$ATRIUM_PANE_ID"
# Launch Codex, brief it to analyze the project's tech stack, existing components, patterns
```

Wait for all 3 to complete. Read their outputs.

### Step 2: Research Synthesis — Claude synthesizes all 3 outputs
Invoke a subagent to run `/guild-research-synthesis`. Feed it:
- Claude's competitor visual audit
- Gemini's design inspiration findings
- Codex's technical analysis
- Any existing research artifacts and interview data

**Party Log:** `Phase 1/5 — Scouting Party complete. 3 models contributed.`

---

## Phase 2: Design — "Crafting Guild" (sequential with multi-model checkpoints)

### Step 3: Content & Microcopy (Warlock) — Claude
Invoke subagent → `/guild-agent-warlock`. Write all copy based on synthesized research.

### Step 4: Editorial Review — Gemini
Launch Gemini in a pane to independently review the Warlock's copy. Fresh eyes from a different model catch things the author's model misses.
Also run `/bmad-editorial-review-prose` via Claude subagent.
Compare both reviews. Apply the best improvements.

### Step 5: Interaction Design (Rogue) — Claude
Invoke subagent → `/guild-agent-rogue`. Wireframes, flows, state diagrams.

### Step 6: Visual Design (Mage) — Claude
Invoke subagent → `/guild-agent-mage`. Apply visual design using research references.

### Step 7: Design QA — 3-Model Raid

Launch all 3 models to review the design independently:

**Claude:** Run `/guild-agent-sage` — full accessibility and quality audit
**Gemini:** Run adversarial review — challenge every design decision
**Codex:** Run edge case analysis — technical feasibility, state coverage

Collect all 3 verdicts:
- If ALL say GO → highest confidence, proceed
- If 2 say GO, 1 says CONDITIONAL → proceed with noted conditions
- If ANY says NO-GO → STOP, report findings, halt quest

**Party Log:** `Phase 2/5 — Crafting complete. 3-model QA: [verdict]. Confidence: [high/medium/low].`

---

## Phase 3: Review — "Trial by Council" (all models review)

### Step 8: Multi-Model Party Review
Launch 3 panes simultaneously:

**Claude:** Review for UX consistency, flow completeness, copy quality
**Gemini:** Review for business logic gaps, user journey holes, competitive weakness
**Codex:** Review for technical implementation concerns, performance risks, data model issues

Synthesize findings. Convergence across models = highest confidence. Divergence = needs investigation.

### Step 9: Edge Case Sweep — Codex
Codex excels at boundary conditions. Launch Codex to run edge case analysis on all design artifacts.
Claude runs `/bmad-review-edge-case-hunter` in parallel.
Merge findings.

**Party Log:** `Phase 3/5 — Trial by Council complete. [N] findings, [N] critical.`

---

## Phase 4: Handoff — "Forging the Blueprint" (Claude leads, Codex validates)

### Step 10: Dev Handoff (Healer) — Claude
Invoke subagent → `/guild-agent-healer`. Complete dev handoff spec.

### Step 11: Pre-Handoff Gate — Claude + Codex
**Claude:** Run `/guild-pre-handoff` quality gate.
**Codex:** Independently validate that the spec is implementable — check for missing states, ambiguous requirements, untestable acceptance criteria.

Both must pass. If either flags NO-GO, loop back.

### Step 12: UX Spec — Claude
Invoke subagent → `/guild-ux-spec`.

### Step 13: Generate Stories — Claude
Invoke subagent → `/guild-jira-stories`.

**Codex:** Review generated stories for technical accuracy and completeness.

**Party Log:** `Phase 4/5 — Blueprint forged. [N] stories. Codex validated.`

---

## Phase 5: Build — "The Grand Forge" (parallel dev)

### Step 14: Sprint Planning — Claude
Invoke subagent → `/bmad-sprint-planning`.

### Step 15: Parallel Dev Loop

Split stories across models for parallel development:

**Claude:** Handles UI components, layouts, styling stories
**Codex:** Handles logic, data, API, state management stories
**Gemini:** Handles tests, documentation, accessibility stories

For each model's assigned stories:
1. `/bmad-create-story` (Claude orchestrates)
2. Model implements its assigned story
3. A DIFFERENT model reviews (Claude builds → Codex reviews, Codex builds → Claude reviews)
4. Fix loop if needed (max 3 cycles)
5. Commit

Cross-model code review ensures no model reviews its own work.

**Party Log:** `Story [ID] complete (built by [model], reviewed by [model]). [done]/[total].`

---

## Quest Complete

```
⚔️ PARTY QUEST COMPLETE
Built: [product name]
Party: Claude + Gemini + Codex
Phases: 5/5
Stories: [total] completed, [blocked] blocked
Multi-model checkpoints: [N] convergence points, [N] divergences resolved
Confidence: [HIGH — all models agreed on critical decisions]
Artifacts: [list key output files]
```

## Quest Failed — Exit Conditions

- 3-model QA NO-GO at Step 7 — design not ready
- Pre-handoff gate fails at Step 11 — quality issues
- Story fails cross-model review 3x — mark blocked, skip
- Atrium not available — fall back to `/guild-quest` (solo)
- Critical error — stop and report

---

## Atrium Commands Reference

```bash
# Create panes
"$ATRIUM_CLI_PATH" pane create --type terminal --split "$ATRIUM_PANE_ID"

# Write to pane (launch model)
"$ATRIUM_CLI_PATH" pane write <pane-id> --text "claude\n"
"$ATRIUM_CLI_PATH" pane write <pane-id> --text "codex\n"
"$ATRIUM_CLI_PATH" pane write <pane-id> --text "gemini\n"

# Read pane output
"$ATRIUM_CLI_PATH" pane read <pane-id> --lines 50

# Send message between agents
"$ATRIUM_CLI_PATH" agent message <pane-id> "your message"

# Browser for visual audit
"$ATRIUM_CLI_PATH" pane create --type browser --url "https://dribbble.com/search/energy-dashboard"
"$ATRIUM_CLI_PATH" browser snapshot <pane-id>
"$ATRIUM_CLI_PATH" browser screenshot <pane-id>
```

## Tips

- **Phase 1 is embarrassingly parallel** — all 3 models research independently, then synthesize
- **Phase 2 is mostly sequential** — but editorial review (Step 4) uses Gemini as a second opinion
- **Phase 3 is the confidence multiplier** — 3 models reviewing catches what 1 model misses
- **Phase 5 splits by strength** — Claude for UI, Codex for logic, Gemini for tests
- **Cross-model review is key** — never let a model review its own code
- **Convergence = signal** — when all 3 models independently reach the same conclusion, lead with it
