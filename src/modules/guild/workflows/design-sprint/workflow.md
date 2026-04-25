# Guild Design Sprint Workflow

## Trigger
User invokes this workflow with a feature or improvement area:
- "Run a design sprint on the packing screen"
- "Design sprint: add social features"
- "Guild sprint: improve onboarding"

## Step -1: Mode Detection

Determine whether Guild is running standalone or with BMAD:

1. Read `guild.config.yaml` at {project-root} for `bmad_mode` setting
2. If `bmad_mode: auto` → check if `{project-root}/_bmad/core/config.yaml` exists
   - If YES → **bmad_mode = true**, `{output_root}` = `_bmad-output`
   - If NO → **bmad_mode = false**, `{output_root}` = `guild-output`
3. If `bmad_mode: true` or `bmad_mode: false` → use explicit setting
4. If `guild.config.yaml` doesn't exist → default to auto-detection

## Step 0: Project Detection

Check for these files in order:

1. `{output_root}/implementation-artifacts/sprint-status.yaml` — exists?
2. `{output_root}/planning-artifacts/prd.md` — exists?
3. `{output_root}/planning-artifacts/architecture.md` — exists?
4. `{output_root}/guild-artifacts/` — any files exist?

**If sprint-status.yaml exists → BROWNFIELD**
This is an active project with existing sprints. Reference existing artifacts, continue numbering.
- With BMAD: Ranger → Rogue → Mage → Warlock → Sage → Healer → PM → SM (8 phases)
- Standalone: Ranger → Rogue → Warlock → Sage → Healer (5 phases)

**If prd.md exists but no sprint-status.yaml → MID-PROJECT**
Planning happened but implementation hasn't started.
- With BMAD: PM → Ranger → Rogue → Mage → Warlock → Architect → Sage → Healer → PM → SM (10 phases)
- Standalone: Ranger → Rogue → Mage → Warlock → Sage → Healer (6 phases)

**If nothing exists → GREENFIELD**
Brand new project.
- With BMAD: Analyst → PM → Ranger → Rogue → Mage → Warlock → Architect → Sage → Healer → PM → SM (12 phases)
- Standalone: Ranger → Rogue → Mage → Warlock → Sage → Healer (6 phases)

Report detection to user:
"Detected: [GREENFIELD/BROWNFIELD/MID-PROJECT], mode: [BMAD/Standalone]. Running [X]-phase pipeline."

## Pre-flight (after detection)
1. Read any existing artifacts identified during detection
2. Read `{output_root}/planning-artifacts/project-context.md` if it exists
3. Read existing `{output_root}/guild-artifacts/` — don't repeat prior work
4. Ask user ONE clarifying question if scope is ambiguous
5. Confirm: "I'll run the [GREENFIELD/BROWNFIELD/MID-PROJECT] pipeline on [scope]. Ready?"

## Core Rule: Artifact Source of Truth

All Guild artifacts are standalone documents in {output_root}/guild-artifacts/.

**When BMAD is present** and the pipeline interacts with BMAD documents (PRD, architecture, sprint-status.yaml):
- Guild agents write FULL artifacts to guild-artifacts/
- BMAD agents receive SUMMARIES with references to Guild artifacts
- If a PM or Architect asks for journey maps, personas, flows, etc. — generate the full Guild artifact AND provide a summary for their document
- This prevents duplication and ensures one source of truth

**When running standalone:**
- Guild artifacts in {output_root}/guild-artifacts/ are the only output
- No BMAD document integration needed

---

## GREENFIELD Pipeline (12 phases)
For brand new projects with no existing BMAD artifacts.

### Phase 0: Analyst (BMAD)
Brainstorm and create product brief:
- Interactive discovery session with user
- Capture product vision, target users, core problem, key features
- Output: `product-brief.md` → `{output_root}/planning-artifacts/`
- Report: "Phase 0 complete — product brief created"

### Phase 1: PM (BMAD)
Create PRD from product brief:
- Functional requirements, non-functional requirements
- Epics and high-level story mapping
- User types and success metrics
- Output: `prd.md` → `{output_root}/planning-artifacts/`
- Report: "Phase 1 complete — PRD created with [n] epics"

### Phase 2: Ranger 🔍 — Research (Smart Skip)

Before running any research, check what already exists:

1. Check {output_root}/guild-artifacts/ for:
   - personas*.md — If personas exist AND were created within this sprint cycle, SKIP persona generation. Reference existing.
   - journey-map*.md — If journey maps exist AND cover the feature scope, SKIP journey mapping. Reference existing.
   - competitive-audit*.md — If competitive audit exists AND is recent, SKIP. Reference existing.
   - heuristic-eval*.md — If heuristic eval exists for this feature, SKIP. Reference existing.
   - jtbd*.md — If JTBD mapping exists AND covers the feature scope, SKIP. Reference existing.

2. Check {output_root}/planning-artifacts/ for:
   - prd*.md — Read for context (always)

3. For each research method, Ranger decides:
   - EXISTS + CURRENT + COVERS SCOPE → Skip, reference existing artifact
   - EXISTS + OUTDATED → Update/extend existing artifact, don't recreate
   - EXISTS + DIFFERENT SCOPE → Run for the new scope, keep both
   - DOESN'T EXIST → Run as normal

4. Report to user:
   "Found existing artifacts:
   - ✅ [artifact] — will reference, not recreate
   - 🔍 [artifact] — not found, will generate

   Running [n] research methods, skipping [m] (already exist)."

**Greenfield foundation (run if not already present):**
- `/persona-gen` — generate personas from PRD user descriptions
- `/competitive-audit` — competitive analysis of similar products
- `/jtbd` — map core user jobs with functional, emotional, and social dimensions

**Run if needed (based on scope and complexity):**
- `/journey-map` — if the feature involves multi-step user flows
- `/heuristic-eval` — if redesigning an existing product or feature
- `/interview-script` — if user research sessions are planned
- `/stakeholder-interview` — if multiple stakeholders have input on this feature

**Run if requested:**
- `/card-sort` — if information architecture decisions are needed
- `/survey` — if quantitative validation is needed before design
- `/empathy-map` — if user segments need deeper emotional analysis
- `/ab-test` — if comparing design approaches quantitatively

If the PM already created personas and journey maps during PRD creation, those count as valid Guild artifacts — Ranger skips redundant work and moves straight to what's missing.

- Output: new/updated artifacts → `{output_root}/guild-artifacts/`
- Report: "Phase 2 complete — [n] research artifacts ([m] new, [k] referenced existing) using [methods list]"

### Phase 3: Rogue (Guild .esign)
Create full product design from research:
- Site map / information architecture for full product
- User flows for each epic
- Wireframes for key screens
- State diagrams for complex components
- Output: `site-map.md`, `user-flow-*.md`, `wireframe-*.md` → `{output_root}/guild-artifacts/`
- Report: "Phase 3 complete — [n] design artifacts produced"

### Phase 4: Mage 🎨 — Visual Polish

After Rogue produces structural designs (flows, wireframes, state diagrams),
the Visual Designer reviews and polishes the visual treatment before Warlock
writes copy for the screens.

The Visual Designer:
1. Reads Rogue's wireframes and flow artifacts
2. IF the app is running (simulator or localhost):
   - Auto-captures screens via Playwright/xcrun simctl
   - Runs visual critique using vision analysis
3. IF working from wireframe specs only:
   - Reviews the wireframe descriptions for visual hierarchy issues
4. For each screen/component in Rogue's output:
   - Checks visual hierarchy (is the primary element clear?)
   - Checks spacing rhythm (on the 4/8/12/16/24/32/48 scale?)
   - Checks typography (max 3 sizes, clear weight hierarchy?)
   - Checks color usage (every color earns its place?)
   - Checks visual noise (can anything be removed?)
5. Outputs:
   - Visual polish recommendations with code fixes
   - Updated style specs for Warlock to reference when writing copy
   - Spacing/typography/color refinements as design tokens if new
6. Save to {output_root}/guild-artifacts/visual-polish-[scope].md

The Visual Designer does NOT block the pipeline with subjective opinions.
It focuses on objective visual quality: hierarchy, spacing, consistency, noise.
If everything looks clean, it passes through with "No visual issues found."

This phase is SKIPPABLE if:
- The project is in early prototyping and visual polish is premature
- The orchestrator receives a --skip-visual flag
- User explicitly says "skip visual polish"

- Output: `visual-polish-[scope].md` → `{output_root}/guild-artifacts/`
- Report: "Phase 4 complete — visual polish [applied/skipped/no issues found]"

### Phase 5: Warlock (Guild Content)
Write all product content:
- Voice and tone guidelines
- All screen microcopy
- Error message system
- Empty states for all screens
- Onboarding copy
- Output: `voice-tone.md`, `microcopy-*.md`, `error-messages.md`, `empty-states.md` → `{output_root}/guild-artifacts/`
- Report: "Phase 5 complete — [n] content artifacts produced"

### Phase 6: Architect (BMAD)
Create technical architecture:
- System architecture based on PRD + Guild design artifacts
- Tech stack decisions informed by component specs
- Data model, API design, infrastructure
- Output: `architecture.md` → `{output_root}/planning-artifacts/`
- Report: "Phase 6 complete — architecture document created"

### Phase 7: Sage (Guild .A)
Quality gate on all design work:
- Design review on all Rogue artifacts
- Accessibility audit
- Content QA on all Warlock output
- Pre-handoff quality gate
- IF NO-GO → loop back to relevant phase with issues
- IF GO/CONDITIONAL → continue
- Output: `qa-report.md` → `{output_root}/guild-artifacts/`
- Report: "Phase 7 complete — verdict: [GO/CONDITIONAL/NO-GO]"

### Phase 8: Healer (Guild Handoff)
Generate all implementation artifacts:
- Generate epic and story files from design artifacts
- Component specs for all new components
- Design tokens in W3C DTCG format
- Output: stories → `{output_root}/implementation-artifacts/stories/`
- Output: `component-specs.md`, `design-tokens.json` → `{output_root}/guild-artifacts/`

After generating stories, Healer also compiles all Guild artifacts into
`{output_root}/planning-artifacts/UX_Design.md` for BMAD dev agent compatibility.
This ensures the dev agent has a consolidated UX spec in the format it expects,
replacing Sally's output with Guild's richer pipeline output. Run task
`export-ux-design.md` automatically — no separate command needed.

- Report: "Phase 8 complete — [n] stories generated ([story range]), UX_Design.md compiled"

### Phase 9: PM (BMAD) — Story Review
Validate stories against PRD:
- Check story alignment with PRD and product goals
- Validate prioritization (P0/P1/P2)
- Verify acceptance criteria are complete and testable
- Identify missing or out-of-scope stories
- IF APPROVED → continue
- IF FLAGGED → pause for user confirmation
- Output: updated story files, `pm-review-[scope].md` → `{output_root}/guild-artifacts/`
- Report: "Phase 9 complete — PM review: [APPROVED/APPROVED WITH CHANGES/FLAGGED]"

### Phase 10: SM (BMAD) — Sprint Planning
Plan and assign sprints:
- Read team velocity and capacity
- Assign stories to sprints (P0 first)
- Sequence work within sprints
- IF total points exceed capacity → split across sprints
- Output: updated `sprint-status.yaml`, `sprint-plan-[sprint-number].md` → `{output_root}/implementation-artifacts/`
- Report: "Phase 10 complete — stories assigned to Sprint [number], [points] points planned"

### Phase 11: Dev (BMAD) — Implementation
Stories are ready for development:
- Pick up stories with `/ds`
- All design context available in `guild-artifacts/`
- Architecture available in `planning-artifacts/`

---

## BROWNFIELD Pipeline (8 phases)
For existing projects with sprint-status.yaml.

### Phase 2: Ranger 🔍 — Research (Smart Skip)

Before running any research, check what already exists in {output_root}/guild-artifacts/:

1. Scan for existing artifacts matching this feature scope:
   - personas*.md, journey-map*.md, competitive-audit*.md, heuristic-eval*.md, jtbd*.md

2. For each artifact found:
   - EXISTS + CURRENT + COVERS SCOPE → Skip, reference existing
   - EXISTS + OUTDATED → Update/extend, don't recreate
   - EXISTS + DIFFERENT SCOPE → Run for new scope, keep both
   - DOESN'T EXIST → Run as normal

3. Report what was found and what will be skipped:
   "Found existing artifacts from PM phase:
   - ✅ Personas — will reference, not recreate
   - ✅ Journey map — will reference, not recreate
   - 🔍 No heuristic eval found — will run targeted eval on [scope]

   Skipping to Rogue with existing research as context."

**Brownfield baseline (run if not already present):**
- Reference existing personas — update if the feature introduces new user types
- `/heuristic-eval` or `/journey-map` for the specific feature area

**Run if needed (based on feature scope):**
- `/competitive-audit` — only if the feature is entirely new to the product
- `/usability-test` — if redesigning an existing flow with known pain points
- `/empathy-map` — if the feature targets a user segment not well-covered by existing personas

**Skip unless requested:**
- `/persona-gen` — personas already exist, only update
- `/jtbd` — existing JTBD likely covers this scope
- `/stakeholder-interview` — only if new stakeholders are involved

If the PM already created Guild-format artifacts during PRD creation, those are valid — Ranger skips redundant work.

- Output: new/updated artifacts → `{output_root}/guild-artifacts/`
- Report: "Phase 2 complete — [n] research artifacts ([m] new, [k] referenced existing) using [methods list]"

### Phase 3: Rogue (Guild .esign)
Design solutions for the feature:
- User flows for the specific feature
- State diagrams for complex components
- Wireframes for new/changed screens only
- Output → `{output_root}/guild-artifacts/`
- Report: "Phase 3 complete — [n] design artifacts produced"

### Phase 4: Mage 🎨 — Visual Polish
Same as greenfield Phase 4. Reviews Rogue's brownfield designs for visual quality.
Skippable with --skip-visual flag.

- Output: `visual-polish-[scope].md` → `{output_root}/guild-artifacts/`
- Report: "Phase 4 complete — visual polish [applied/skipped/no issues found]"

### Phase 5: Warlock (Guild Content)
Content for new/changed screens:
- Microcopy for new screens
- Error messages for new error states
- Empty states for new screens
- Output → `{output_root}/guild-artifacts/`
- Report: "Phase 5 complete — [n] content artifacts produced"

### Phase 6: Sage (Guild .A)
Focused QA on new designs:
- Design review on new designs only
- Accessibility check on new/changed screens
- IF NO-GO → loop back to Rogue
- Output → `{output_root}/guild-artifacts/`
- Report: "Phase 6 complete — verdict: [GO/CONDITIONAL/NO-GO]"

### Phase 7: Healer (Guild Handoff)
Handoff continuing from existing state:
- Stories continue from existing numbering
- Append to existing epics or create new ones
- Component specs for new components only
- Tokens added to existing token file
- Output: stories → `{output_root}/implementation-artifacts/stories/`

After generating stories, Healer also updates
`{output_root}/planning-artifacts/UX_Design.md` with the new/changed sections.
If UX_Design.md doesn't exist yet, generate it fresh. If it exists, update
only the sections affected by this sprint's design work.

- Report: "Phase 7 complete — [n] stories generated ([story range]), UX_Design.md updated"

### Phase 8: PM (BMAD) — Story Review
Same as greenfield Phase 9.

### Phase 9: SM (BMAD) — Sprint Planning
Fit new stories into current or next sprint.

---

## MID-PROJECT Pipeline (10 phases)
PRD exists but no sprints yet. Skip Analyst, include Architect.

### Phase 1: PM (BMAD) — PRD Review
Review existing PRD (validate, don't recreate):
- Confirm PRD is current and complete
- Flag any gaps or outdated sections
- Output: updated `prd.md` if changes needed
- Report: "Phase 1 complete — PRD validated"

### Phases 2-5: Ranger → Rogue → Mage → Warlock
Same as greenfield Phases 2-5.

### Phase 6: Architect (BMAD)
Same as greenfield Phase 6.

### Phases 7-10: Sage → Healer → PM → SM
Same as greenfield Phases 7-10.

---

## Post-Pipeline Report
After all phases complete, output a summary:
```
Guild Design Sprint Complete — [Feature/Scope]

Detected: [GREENFIELD/BROWNFIELD/MID-PROJECT]
Pipeline: Ranger → Rogue → Mage → Warlock → Sage → Healer → PM → SM

Artifacts produced: [count]
Research: [list]
Designs: [list]
Visual polish: [applied/skipped/no issues found]
Content: [list]
QA verdict: [GO/CONDITIONAL/NO-GO]
PM review: [APPROVED/APPROVED WITH CHANGES/FLAGGED]
Stories generated: [count] ([story range])
Sprint assignment: Sprint [number]
Total points: [sum]
Sprint capacity: [points assigned] / [velocity]
Conditions (if any): [list]

Ready for: @dev to pick up [first story ID] with /ds
```

## Error Handling
- If any phase fails, save what was completed and report where it stopped
- If sprint-status.yaml doesn't exist in brownfield, fall back to mid-project pipeline
- If scope is too broad (>20 stories generated), suggest breaking into multiple sprints
- If Sage issues NO-GO, loop back to the relevant phase with specific issues
- If PM flags stories as fundamentally misaligned, pause for user confirmation before continuing

## Quick Sprint Variant
Skip research phase. Runs: Rogue → Mage → Warlock → Sage → Healer → PM → SM.
Triggered by `/quick-sprint`.

## Research Only Variant
Run only Ranger. Save findings for later pipeline execution.
Triggered by `/research-only`.

## Handoff Only Variant
Run Healer → PM → SM against existing guild-artifacts/.
Triggered by `/handoff-only`.
