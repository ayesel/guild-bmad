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
  "$ATRIUM_CLI_PATH" browser scroll <pane-id> --direction subtab --amount 500
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
# MUST include: use --timeout 30000 on all browser screenshot commands, retry up to 3x, open a separate browser pane per competitor
```

**Gemini pane:** Visual audit of design inspiration (Dribbble, Behance, best-in-class dashboards)
```bash
"$ATRIUM_CLI_PATH" pane create --type terminal --split "$ATRIUM_PANE_ID"
# Launch Gemini, brief it to search Dribbble/Behance for design patterns
# MUST open browser panes for each search, take real screenshots, not describe from memory
```

**Codex pane:** Analyze existing codebase and technical constraints
```bash
"$ATRIUM_CLI_PATH" pane create --type terminal --split "$ATRIUM_PANE_ID"
# Launch Codex, brief it to analyze the project's tech stack, existing components, patterns
```

**IMPORTANT — Browser instructions for Claude and Gemini panes:**
Each pane doing visual research MUST:
1. Create a separate browser pane per URL: `"$ATRIUM_CLI_PATH" pane create --type browser --url "<url>" --split "$ATRIUM_PANE_ID"`
2. Wait for page load (5s), then screenshot with `--timeout 30000`
3. Retry screenshots up to 3x on timeout before falling back to snapshot
4. Scroll down and capture below-the-fold content
5. Save screenshot evidence — file paths or confirmation that base64 was captured
6. If zero screenshots succeed after retries, STOP and report failure

Wait for all 3 to complete. Read their outputs.

### Step 1b: Screenshot Verification Gate

Before proceeding to synthesis, verify:
- Claude's visual audit contains real screenshot references for at least 3 competitors
- Gemini's inspiration research contains real screenshot references from Dribbble/Behance
- If either pane fell back to DOM-only with zero screenshots, re-run that pane with explicit browser pane creation and `--timeout 30000`
- DO NOT proceed to Phase 2 without visual evidence. The entire visual design phase depends on having actually seen the competitors and inspiration sources.

### Step 2: Research Synthesis — Claude synthesizes all 3 outputs
Invoke a subagent to run `/guild-research-synthesis`. Feed it:
- Claude's competitor visual audit (with screenshot evidence)
- Gemini's design inspiration findings (with screenshot evidence)
- Codex's technical analysis
- Any existing research artifacts and interview data

**Party Log:** `Phase 1/5 — Scouting Party complete. 3 models contributed. Screenshots: [N] captured, [N] failed.`

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

### Step 15: Parallel Dev Loop (Autonomous Build)

Core rules:
- `sprint-status.yaml` is the source of truth. Reload it after every story review, review-fix cycle, retrospective, and course-correction run.
- Track the active epic number, active story identifier, active story file path, and any prefetched next story file path.
- Do not ask for or wait for human approval during autonomous build. When a delegated BMAD workflow asks for confirmation, mode selection, approval, or facilitation input, instruct the subagent to choose the conservative autonomous default and document its assumption.
- Do not create or develop a story from the next epic until the current epic's retrospective and course-correction gate has completed.
- If a next story was prefetched and course correction changes the relevant epic, story, PRD, architecture, or UX artifacts, discard that prefetched story and create a fresh one from the corrected documents.
- Commit completed story work separately from epic-transition documentation work.

Split stories across models for parallel development:

**Claude:** Handles UI components, layouts, styling stories
**Codex:** Handles logic, data, API, state management stories
**Gemini:** Handles tests, documentation, accessibility stories

Cross-model code review ensures no model reviews its own work (Claude builds → Codex reviews, Codex builds → Claude reviews).

Repeat until all epics and their retrospective entries in `sprint-status.yaml` are `done`:

**15a. Select or Create Story**
Load `sprint-status.yaml` and select the next non-retrospective story that is not `done`.
- If a valid prefetched story file path already exists for that story, use it.
- Otherwise, invoke subagent → `/bmad-create-story`. Read story file path.

**15b. Dev Story**
Assign story to the appropriate model based on story type. Send to model pane for implementation. Wait for completion.

**15c. Code Review + Prefetch**
Simultaneously:
- A DIFFERENT model reviews the implementation (cross-model review).
- If there is another story remaining in the same epic, create the next story (prefetch).
- If the active story is the final story in the current epic, do NOT prefetch a next-epic story — the epic-transition gate may change the next epic's source documents.

**15d. Review Fix Loop**
If the story status is NOT `done` after review:
1. Send back to the implementing model for fixes (it auto-detects review follow-ups). DO NOT attempt to fix the problem yourself.
2. Send to reviewing model again. Wait for completion.
3. Repeat until `done` or 3 review cycles reached.

**15e. Commit**
Commit all changes for the completed story. Do not include the prefetched next story in this commit.

**15f. Epic Transition Gate**
After committing a story, reload `sprint-status.yaml`. If all non-retrospective stories in the active epic are `done`, run this gate before starting the next epic. This gate also runs for the final epic before exiting.

**15f-i. Autonomous Retrospective**
Invoke subagent → `/bmad-retrospective` for the active epic with non-interactive instructions:

> Run the retrospective fully autonomously for Epic [active-epic-number].
> Do not wait for the user at any prompts. Synthesize from completed story files, dev notes, review notes, implementation artifacts, commit history, test results, and project documents.
> If evidence is missing, record "not verified" with a concrete action item instead of asking the user.
> Save the retrospective document and update sprint-status.yaml.

**15f-ii. Autonomous Course Correction**
Invoke subagent → `/bmad-correct-course` using the retrospective as the change trigger with non-interactive instructions:

> Run correct-course fully autonomously in Batch mode.
> Change trigger: "Epic [active-epic-number] retrospective findings need to be synthesized into project artifacts before the next epic begins."
> Auto-approve factual documentation updates supported by retrospective findings and implementation evidence.
> Update impacted PRD, epic/story, architecture, UX/spec, and project-knowledge documents when the edit is clear.
> If a finding is not concrete enough to safely edit, capture it in the Sprint Change Proposal instead.
> Save the Sprint Change Proposal, return its path, list all changed files.

**15f-iii. Transition Decision**
- Commit retrospective, sprint-status.yaml, Sprint Change Proposal, and any doc changes.
- If course correction changes the next epic or prefetched story's source docs, discard the prefetched story.
- If course correction reports a major unresolved ambiguity or fundamental replan, STOP and report to user.
- Otherwise, continue to the next epic without asking for approval.

**15g. Next Story**
Return to 15a. Continue through all epics. Do not ask for or wait for human approval.

**Party Log:** `Story [ID] complete (built by [model], reviewed by [model]). [done]/[total].`

---

## Quest Complete

When all epics and their retrospective entries are done:
```
⚔️ PARTY QUEST COMPLETE
Built: [product name]
Party: Claude + Gemini + Codex
Phases: 5/5
Stories: [total] completed, [blocked] blocked
Epics: [N] completed with retrospectives
Course corrections: [N] applied
Multi-model checkpoints: [N] convergence points, [N] divergences resolved
Confidence: [HIGH — all models agreed on critical decisions]
Artifacts: [list key output files]
```

## Quest Failed — Exit Conditions

- 3-model QA NO-GO at Step 7 — design not ready
- Pre-handoff gate fails at Step 11 — quality issues
- Story fails cross-model review 3x consecutively — stop and report to user
- Autonomous retrospective finds the active epic is incomplete
- Course correction reports a major unresolved ambiguity, missing required PRD/epic artifacts, or a fundamental replan that cannot be completed autonomously
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
