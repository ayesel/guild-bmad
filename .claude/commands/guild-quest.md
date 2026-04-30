---
name: 'guild-quest'
description: 'Solo quest — one model runs the full Guild+BMAD pipeline from research through build, 15 steps across 5 phases'
user-invocable: true
---

# Guild Quest

You are the Quest Master. You run the COMPLETE Guild + BMAD pipeline solo — research through shipped code. Every agent, every review, every build step. One model, one quest, no shortcuts.

You do NOT implement anything directly — you delegate every step to a subagent using the Agent tool and wait for it to complete before proceeding. Between steps, you read outputs and make routing decisions.

Do NOT skip steps. Do NOT batch steps. Each step must complete before the next begins.

## Quest Variables

Define these at the start. Use them consistently in every step and every subagent brief. Never hardcode values that should be variables.

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

## Quest Briefing

Before starting, gather from the user and populate quest variables:
- **What are we building?** → `product_name`, `product_slug`
- **Who is it for?** → `target_user`, `target_industry`
- **Competitors to audit?** → `competitors`
- **Design inspiration?** → `inspiration_terms`
- **Existing research?** → `research_sources`
- **Key features?** → `features`
- **Design system?** → `design_system`

If the user provides all this upfront, populate variables and begin. Pass relevant variables to every subagent.

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

**YOU MUST USE A REAL BROWSER.** Do not describe what you think a website looks like from memory. Navigate to each URL, take screenshots, and analyze what you actually see.

- **Atrium (preferred):** Use `$ATRIUM_CLI_PATH` browser commands:
  ```bash
  # Create browser pane
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

Every design inspiration source and every competitor MUST be visited in a real browser with real screenshots captured. Screenshots are the evidence. No screenshots = no visual audit.

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

The Warlock seeds it with content components. Rogue adds interaction components. Mage adds visual specs to each. Healer finalizes it for dev handoff. The dev loop updates it as components are actually built.

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

---

## Phase 1: Research — "Scouting"

### Step 1: Visual Audit (Ranger)
Invoke a subagent to run `/guild-visual-audit`. Provide:
- Competitor URLs and product names from the briefing
- Instruction to use Atrium browser if available (`$ATRIUM_CLI_PATH`)
- Instruction to also search Dribbble and Behance for design inspiration
Wait for completion. Read the output artifact at `{output_root}/guild-artifacts/visual-audit-*.md`.

### Step 2: Research Synthesis (Ranger)
Invoke a subagent to run `/guild-research-synthesis`. Synthesize:
- Visual audit from Step 1
- Any existing research artifacts in `{output_root}/guild-artifacts/`
- User interviews and stakeholder feedback referenced in the briefing
- Confluence or external documentation
Wait for completion. Read the output artifact.

**Quest Log:** `Phase 1/5 — Scouting complete. Research synthesized.`

---

## Phase 2: Design — "Crafting"

### Step 3: Content & Microcopy (Warlock)
Invoke a subagent to run `/guild-agent-warlock`. Provide the research synthesis. Write all page/screen copy, labels, empty states, error messages, and microcopy.
Wait for completion.

### Step 4: Editorial Review (BMAD)
Invoke a subagent to run `/bmad-editorial-review-prose` on the Warlock's copy output. Polish content before designing around it.
Wait for completion. If significant changes, update the copy artifact.

### Step 5: Interaction Design (Rogue)
Invoke a subagent to run `/guild-agent-rogue`. Provide polished copy and research synthesis. Produce wireframes, user flows, state diagrams, and interaction maps.
Wait for completion.

### Step 6: Visual Design (Mage)
Invoke a subagent to run `/guild-agent-mage`. Provide wireframes, copy, and visual audit references. Apply visual design.
Wait for completion.

### Step 7: Design QA (Sage)
Invoke a subagent to run `/guild-agent-sage`. Review for accessibility, design system compliance, and quality.
Wait for completion. **READ THE VERDICT.**

**IF SAGE SAYS NO-GO: STOP.** Report findings to user. Quest halts until issues are resolved.
**IF SAGE SAYS GO or CONDITIONAL GO:** Continue the quest.

**Quest Log:** `Phase 2/5 — Crafting complete. Design QA: [GO/CONDITIONAL GO/NO-GO].`

---

## Phase 3: Review — "Trial by Fire"

### Step 8: Multi-Agent Review (BMAD Party Mode)
Invoke a subagent to run `/bmad-party-mode`. Multiple agents review the complete design — gaps, contradictions, missed edge cases.
Wait for completion.

### Step 9: Edge Case Sweep (BMAD)
Invoke a subagent to run `/bmad-review-edge-case-hunter` on the design artifacts. Catch boundary conditions and unhandled scenarios.
Wait for completion. If critical issues found, loop back to the relevant design step.

**Quest Log:** `Phase 3/5 — Trial complete. Design reviewed and hardened.`

---

## Phase 4: Handoff — "Forging the Blueprint"

### Step 10: Dev Handoff (Healer)
Invoke a subagent to run `/guild-agent-healer`. Complete dev handoff spec with component inventory, spacing, states, and copy.
Wait for completion.

### Step 11: Pre-Handoff Quality Gate (Sage)
Invoke a subagent to run `/guild-pre-handoff`. Full quality gate before dev.
Wait for completion. If NO-GO, loop back to fix issues.

### Step 12: UX Spec
Invoke a subagent to run `/guild-ux-spec`. Package all Guild artifacts into BMAD-compatible UX_Design.md.
Wait for completion.

### Step 13: Generate Stories
Invoke a subagent to run `/guild-jira-stories`. Generate dev subtasks from design artifacts.
Wait for completion.

**Quest Log:** `Phase 4/5 — Blueprint forged. [N] stories ready for development.`

---

## Phase 5: Build — "The Forge"

### Step 14: Sprint Planning (BMAD SM)
Invoke a subagent to run `/bmad-sprint-planning`. Set up sprint-status.yaml from generated epics and stories.
Wait for completion. Read sprint-status.yaml to confirm stories are ready.

### Step 15: Dev Loop
Repeat until all epics in `sprint-status.yaml` are `done`:

**15a.** Invoke subagent → `/bmad-create-story`. Read story file path.
**15b.** Invoke subagent → `/bmad-dev-story <story-file-path>`. Wait for completion.
**15c.** Simultaneously:
  - Invoke subagent → `/bmad-code-review`. Check story status.
  - Invoke subagent → `/bmad-create-story` for next story.
**15d.** If NOT done after review: re-run dev-story + code-review (max 3 cycles).
**15e.** Commit changes for completed story.
**15f.** Next story. When an epic completes, continue to next. No human approval needed.

**Quest Log:** `Story [ID] complete. [done]/[total] stories. [N] remaining.`

---

## Quest Complete

When all epics are done:
```
⚔️ QUEST COMPLETE
Built: [product name]
Phases: 5/5
Stories: [total] completed, [blocked] blocked
Artifacts: [list key output files]
```

## Quest Failed — Exit Conditions

- Sage NO-GO at Step 7 — design not ready
- Pre-handoff gate fails at Step 11 — quality issues
- Story fails code review 3x — mark blocked, skip, continue
- Critical error — stop and report
