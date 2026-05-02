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

## Phase 0: Direction — "Set the Compass" (Mage elicitation gate)

**Why this exists:** Without a designer-supplied direction, the pipeline averages competitor research and produces a generic AI-dashboard look. This gate forces the human to declare taste BEFORE any synthesis happens.

### Step 0: Design Direction Brief (Mage)

Run `/guild-design-direction` directly in the main conversation (this is interactive elicitation — do NOT delegate to a subagent, the user must answer the questions in real time).

The brief asks 6 questions: anchor reference, personality adjectives, density, motion energy, color story, what to avoid. Mage synthesizes the answers into `{output_root}/guild-artifacts/design-direction-brief.md`.

**GATE CHECK:** Before proceeding to Phase 1, verify the artifact exists and contains all 6 sections. If the user skipped or rushed any section, push back once: "We need this to be specific or downstream agents will guess."

**Quest Variable:** Once locked, the brief becomes `design_direction_brief` — pass the FULL artifact contents into every Mage/Rogue/Warlock/Ranger subagent prompt in subsequent phases. Visual research weights the anchor reference heavily; visual design executes against the personality + density + motion + color story; copy executes against the personality.

---

## Phase 0.5: Foundation — "Pour the Slab" (Sage system-foundation gate)

**Why this exists:** Even with a great direction brief, agents will inline ad-hoc components (bare `<select>`, hardcoded hex colors, raw `transition-all`) on every page if the token layer and base primitives aren't already present. This gate prevents the system from fragmenting page-by-page.

### Step 0.5: Design System Foundation Audit (Sage)

Invoke a subagent to run `/guild-system-foundation`. Sage audits:
- **Token layer:** color, spacing, motion, shadow, typography (scale + weights), radius
- **Primitive layer:** Button, Input, Select, ChipGroup, Field, Card, Badge, IconButton, Tooltip, Skeleton
- **Usage discipline:** inline `<select>`, hardcoded hex, raw `transition-all`, inline component definitions in pages

Sage produces a verdict: **PASS / CONDITIONAL / FAIL** plus a Remediation Plan.

**GATE CHECK:**
- **PASS** → proceed to Phase 1
- **CONDITIONAL** → minor gaps; quest may proceed but Healer's first stories in Phase 4 must be the missing tokens/primitives BEFORE any page-level story
- **FAIL** → STOP. The next agent task is to add the missing tokens and primitives. Page-level work cannot start.

Show the verdict + plan to the user. If FAIL, ask: "Fix foundation now (recommended), or accept the debt and proceed?" Save the user's decision in the artifact.

**Quest Variable:** The audit becomes `design_system_foundation` — pass the artifact path and PASS/CONDITIONAL/FAIL status to Mage/Rogue/Healer in subsequent phases. Healer's sprint planning prioritizes any unfinished Remediation Plan items as Sprint 1 stories.

**Quest Log:** `Phase 0.5/5 — Foundation: [PASS/CONDITIONAL/FAIL]. Tokens missing: [N]. Primitives missing: [N].`

---

## Phase 1: Research — "Scouting"

### Step 1: Visual Audit (Ranger)
Invoke a subagent to run `/guild-visual-audit`. Provide:
- **Full contents of `{output_root}/guild-artifacts/design-direction-brief.md`** — Ranger MUST weight the anchor reference heavily and use the personality/density/color signals to evaluate competitor patterns through the designer's lens, not as a neutral averaging exercise
- Competitor URLs and product names from the briefing
- Instruction to use Atrium browser if available (`$ATRIUM_CLI_PATH`)
- Instruction to also search Dribbble and Behance for design inspiration aligned with the brief's anchor and personality
- Instruction to use `--timeout 30000` on all browser screenshot commands
- Instruction to retry screenshots up to 3 times before falling back
Wait for completion. Read the output artifact at `{output_root}/guild-artifacts/visual-audit-*.md`.

**GATE CHECK:** Before proceeding to Step 2, verify that the visual audit artifact contains real screenshot references (file paths or base64 data) for at least 3 competitor products. If the audit fell back to DOM-only analysis with zero screenshots, DO NOT PROCEED. Re-run the visual audit with explicit browser pane creation and longer timeouts. Visual design quality depends entirely on having actually seen the competitors.

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
Invoke a subagent to run `/guild-agent-warlock`. Provide:
- **Full contents of `{output_root}/guild-artifacts/design-direction-brief.md`** — voice and tone must execute against the personality adjectives in the brief; do not default to generic SaaS voice
- The research synthesis
Write all page/screen copy, labels, empty states, error messages, and microcopy.
Wait for completion.

### Step 4: Editorial Review (BMAD)
Invoke a subagent to run `/bmad-editorial-review-prose` on the Warlock's copy output. Polish content before designing around it.
Wait for completion. If significant changes, update the copy artifact.

### Step 5: Interaction Design (Rogue)
Invoke a subagent to run `/guild-agent-rogue`. Provide:
- **Full contents of `{output_root}/guild-artifacts/design-direction-brief.md`** — density preference governs layout choices (dense/balanced/airy), motion energy governs transition style; deviate from the brief only with explicit reasoning
- Polished copy and research synthesis
Produce wireframes, user flows, state diagrams, and interaction maps.
Wait for completion.

### Step 6: Visual Design (Mage)
Invoke a subagent to run `/guild-agent-mage`. Provide:
- **Full contents of `{output_root}/guild-artifacts/design-direction-brief.md`** — anchor reference, color story, and personality drive every visual choice; when picking between two valid options, choose the one closer to the anchor
- Wireframes, copy, and visual audit references
Apply visual design.
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

### Step 15: Dev Loop (Autonomous Build)

Core rules:
- `sprint-status.yaml` is the source of truth. Reload it after every story review, review-fix cycle, retrospective, and course-correction run.
- Track the active epic number, active story identifier, active story file path, and any prefetched next story file path.
- Do not ask for or wait for human approval during autonomous build. When a delegated BMAD workflow asks for confirmation, mode selection, approval, or facilitation input, instruct the subagent to choose the conservative autonomous default and document its assumption.
- Do not create or develop a story from the next epic until the current epic's retrospective and course-correction gate has completed.
- If a next story was prefetched and course correction changes the relevant epic, story, PRD, architecture, or UX artifacts, discard that prefetched story and create a fresh one from the corrected documents.
- Commit completed story work separately from epic-transition documentation work.

Repeat until all epics and their retrospective entries in `sprint-status.yaml` are `done`:

**15a. Select or Create Story**
Load `sprint-status.yaml` and select the next non-retrospective story that is not `done`.
- If a valid prefetched story file path already exists for that story, use it.
- Otherwise, invoke subagent → `/bmad-create-story`. Read story file path.

**15b. Dev Story**
Invoke subagent → `/bmad-dev-story <story-file-path>`. Wait for completion.

**15c. Code Review + Prefetch**
Simultaneously:
- Invoke subagent → `/bmad-code-review`. Check story status in `sprint-status.yaml`.
- If there is another story remaining in the same epic, invoke subagent → `/bmad-create-story` for that next story (prefetch).
- If the active story is the final story in the current epic, do NOT prefetch a next-epic story — the epic-transition gate may change the next epic's source documents.

**15d. Review Fix Loop**
If the story status is NOT `done` after code review:
1. Invoke subagent → `/bmad-dev-story <story-file-path>` on the same story (it auto-detects review follow-ups). DO NOT attempt to fix the problem yourself.
2. Invoke subagent → `/bmad-code-review`. Wait for completion.
3. Repeat until `done` or 3 review cycles reached.

**15e. Commit**
Commit all changes for the completed story with a descriptive message. Do not include the prefetched next story in this commit.

**15f. Epic Transition Gate**
After committing a story, reload `sprint-status.yaml`. If all non-retrospective stories in the active epic are `done`, run this gate before starting the next epic. This gate also runs for the final epic before exiting.

**15f-i. Autonomous Retrospective**
Invoke subagent → `/bmad-retrospective` for the active epic. Give the subagent these non-interactive instructions:

> Run the retrospective fully autonomously for Epic [active-epic-number].
> Do not wait for the user at confirmation, facilitation, readiness, approval, or final-reflection prompts.
> Use sprint-status.yaml to confirm the epic number.
> Synthesize participant input from completed story files, dev notes, review notes, implementation artifacts, commit history, test results, and the project documents.
> For readiness questions, inspect available repository state and artifacts. If evidence is missing, record "not verified" with a concrete action item instead of asking the user.
> Choose conservative defaults, document every assumption, save the retrospective document, and update the epic retrospective status in sprint-status.yaml.
> Return the retrospective file path, significant findings, action items, and any candidate documentation updates.

Read the retrospective document before proceeding.

**15f-ii. Autonomous Course Correction**
Invoke subagent → `/bmad-correct-course` using the retrospective as the change trigger. Give the subagent these non-interactive instructions:

> Run correct-course fully autonomously in Batch mode.
> Change trigger: "Epic [active-epic-number] retrospective findings need to be synthesized into project artifacts before the next epic begins."
> Use the retrospective document, completed story files, review notes, sprint-status.yaml, PRD, epics/stories, architecture, UX/spec, and project knowledge as evidence.
> Do not ask the user for the issue description, mode preference, edit approval, proposal approval, or handoff confirmation.
> Auto-approve factual documentation updates that are directly supported by retrospective findings and completed implementation evidence.
> Update impacted PRD, epic/story, architecture, UX/spec, and project-knowledge documents when the required edit is clear.
> If a finding is important but not concrete enough to safely edit source documents, capture it in the Sprint Change Proposal and action items instead of inventing scope.
> Save the Sprint Change Proposal, return its path, list all changed files, and summarize any remaining risks.

Read the Sprint Change Proposal and changed-files list before proceeding.

**15f-iii. Transition Decision**
- Commit the retrospective, `sprint-status.yaml`, Sprint Change Proposal, and any documentation/planning changes with a descriptive epic-transition message.
- If course correction changes the next epic or any prefetched story's source documents, discard the prefetched story and create a fresh story after this gate.
- If course correction reports a major unresolved ambiguity, missing required PRD/epic artifacts, or a fundamental replan that cannot be completed autonomously, STOP and report the blocker to the user.
- Otherwise, continue to the next epic without asking for approval.

**15g. Next Story**
Return to 15a. When you complete an epic, continue to the next epic after the transition gate. Do not ask for or wait for human approval.

**Quest Log:** `Story [ID] complete. [done]/[total] stories. [N] remaining.`

---

## Quest Complete

When all epics and their retrospective entries are done:
```
⚔️ QUEST COMPLETE
Built: [product name]
Phases: 5/5
Stories: [total] completed, [blocked] blocked
Epics: [N] completed with retrospectives
Course corrections: [N] applied
Artifacts: [list key output files]
```

## Quest Failed — Exit Conditions

- Sage NO-GO at Step 7 — design not ready
- Pre-handoff gate fails at Step 11 — quality issues
- Story fails code review 3x consecutively — stop and report to user
- Autonomous retrospective finds the active epic is incomplete
- Course correction reports a major unresolved ambiguity, missing required PRD/epic artifacts, or a fundamental replan that cannot be completed autonomously
- Critical error — stop and report
