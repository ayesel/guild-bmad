# PDX Design Sprint Workflow

## Trigger
User invokes this workflow with a feature or improvement area:
- "Run a design sprint on the packing screen"
- "Design sprint: add social features"
- "PDX sprint: improve onboarding"

## Step 0: Project Detection

Check for these files in order:

1. `_bmad-output/implementation-artifacts/sprint-status.yaml` — exists?
2. `_bmad-output/planning-artifacts/prd.md` — exists?
3. `_bmad-output/planning-artifacts/architecture.md` — exists?
4. `_bmad-output/pdx-artifacts/` — any files exist?

**If sprint-status.yaml exists → BROWNFIELD**
This is an active project with existing sprints. Reference existing artifacts, continue numbering.
Pipeline: Nova → Kai → Lux → Echo → Sage → Relay → PM → SM (8 phases)

**If prd.md exists but no sprint-status.yaml → MID-PROJECT**
Planning happened but implementation hasn't started. Skip Analyst, include Architect.
Pipeline: PM → Nova → Kai → Lux → Echo → Architect → Sage → Relay → PM → SM (10 phases)

**If nothing exists → GREENFIELD**
Brand new project. Run full pipeline including Analyst, PM, and Architect.
Pipeline: Analyst → PM → Nova → Kai → Lux → Echo → Architect → Sage → Relay → PM → SM (12 phases)

Report detection to user:
"Detected: [GREENFIELD/BROWNFIELD/MID-PROJECT]. Running [X]-phase pipeline."

## Pre-flight (after detection)
1. Read any existing BMAD artifacts identified during detection
2. Read `_bmad-output/planning-artifacts/project-context.md` if it exists
3. Read existing `_bmad-output/pdx-artifacts/` — don't repeat prior work
4. Ask user ONE clarifying question if scope is ambiguous
5. Confirm: "I'll run the [GREENFIELD/BROWNFIELD/MID-PROJECT] pipeline on [scope]. Ready?"

## Core Rule: Artifact Source of Truth

All PDX artifacts are standalone documents in _bmad-output/pdx-artifacts/.
When the pipeline interacts with BMAD documents (PRD, architecture, sprint-status.yaml):
- PDX agents write FULL artifacts to pdx-artifacts/
- BMAD agents receive SUMMARIES with references to PDX artifacts
- If a PM or Architect asks for journey maps, personas, flows, etc. — generate the full PDX artifact AND provide a summary for their document
- This prevents duplication and ensures one source of truth
- When PDX artifacts are updated, BMAD documents don't need to be rewritten — the references still point to the current version

---

## GREENFIELD Pipeline (12 phases)
For brand new projects with no existing BMAD artifacts.

### Phase 0: Analyst (BMAD)
Brainstorm and create product brief:
- Interactive discovery session with user
- Capture product vision, target users, core problem, key features
- Output: `product-brief.md` → `_bmad-output/planning-artifacts/`
- Report: "Phase 0 complete — product brief created"

### Phase 1: PM (BMAD)
Create PRD from product brief:
- Functional requirements, non-functional requirements
- Epics and high-level story mapping
- User types and success metrics
- Output: `prd.md` → `_bmad-output/planning-artifacts/`
- Report: "Phase 1 complete — PRD created with [n] epics"

### Phase 2: Nova 🔍 — Research (Smart Skip)

Before running any research, check what already exists:

1. Check _bmad-output/pdx-artifacts/ for:
   - personas*.md — If personas exist AND were created within this sprint cycle, SKIP persona generation. Reference existing.
   - journey-map*.md — If journey maps exist AND cover the feature scope, SKIP journey mapping. Reference existing.
   - competitive-audit*.md — If competitive audit exists AND is recent, SKIP. Reference existing.
   - heuristic-eval*.md — If heuristic eval exists for this feature, SKIP. Reference existing.
   - jtbd*.md — If JTBD mapping exists AND covers the feature scope, SKIP. Reference existing.

2. Check _bmad-output/planning-artifacts/ for:
   - prd*.md — Read for context (always)

3. For each research method, Nova decides:
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

If the PM already created personas and journey maps during PRD creation, those count as valid PDX artifacts — Nova skips redundant work and moves straight to what's missing.

- Output: new/updated artifacts → `_bmad-output/pdx-artifacts/`
- Report: "Phase 2 complete — [n] research artifacts ([m] new, [k] referenced existing) using [methods list]"

### Phase 3: Kai (PDX Design)
Create full product design from research:
- Site map / information architecture for full product
- User flows for each epic
- Wireframes for key screens
- State diagrams for complex components
- Output: `site-map.md`, `user-flow-*.md`, `wireframe-*.md` → `_bmad-output/pdx-artifacts/`
- Report: "Phase 3 complete — [n] design artifacts produced"

### Phase 4: Lux 🎨 — Visual Polish

After Kai produces structural designs (flows, wireframes, state diagrams),
the Visual Designer reviews and polishes the visual treatment before Echo
writes copy for the screens.

The Visual Designer:
1. Reads Kai's wireframes and flow artifacts
2. IF the app is running (simulator or localhost):
   - Auto-captures screens via Playwright/xcrun simctl
   - Runs visual critique using vision analysis
3. IF working from wireframe specs only:
   - Reviews the wireframe descriptions for visual hierarchy issues
4. For each screen/component in Kai's output:
   - Checks visual hierarchy (is the primary element clear?)
   - Checks spacing rhythm (on the 4/8/12/16/24/32/48 scale?)
   - Checks typography (max 3 sizes, clear weight hierarchy?)
   - Checks color usage (every color earns its place?)
   - Checks visual noise (can anything be removed?)
5. Outputs:
   - Visual polish recommendations with code fixes
   - Updated style specs for Echo to reference when writing copy
   - Spacing/typography/color refinements as design tokens if new
6. Save to _bmad-output/pdx-artifacts/visual-polish-[scope].md

The Visual Designer does NOT block the pipeline with subjective opinions.
It focuses on objective visual quality: hierarchy, spacing, consistency, noise.
If everything looks clean, it passes through with "No visual issues found."

This phase is SKIPPABLE if:
- The project is in early prototyping and visual polish is premature
- The orchestrator receives a --skip-visual flag
- User explicitly says "skip visual polish"

- Output: `visual-polish-[scope].md` → `_bmad-output/pdx-artifacts/`
- Report: "Phase 4 complete — visual polish [applied/skipped/no issues found]"

### Phase 5: Echo (PDX Content)
Write all product content:
- Voice and tone guidelines
- All screen microcopy
- Error message system
- Empty states for all screens
- Onboarding copy
- Output: `voice-tone.md`, `microcopy-*.md`, `error-messages.md`, `empty-states.md` → `_bmad-output/pdx-artifacts/`
- Report: "Phase 5 complete — [n] content artifacts produced"

### Phase 6: Architect (BMAD)
Create technical architecture:
- System architecture based on PRD + PDX design artifacts
- Tech stack decisions informed by component specs
- Data model, API design, infrastructure
- Output: `architecture.md` → `_bmad-output/planning-artifacts/`
- Report: "Phase 6 complete — architecture document created"

### Phase 7: Sage (PDX QA)
Quality gate on all design work:
- Design review on all Kai artifacts
- Accessibility audit
- Content QA on all Echo output
- Pre-handoff quality gate
- IF NO-GO → loop back to relevant phase with issues
- IF GO/CONDITIONAL → continue
- Output: `qa-report.md` → `_bmad-output/pdx-artifacts/`
- Report: "Phase 7 complete — verdict: [GO/CONDITIONAL/NO-GO]"

### Phase 8: Relay (PDX Handoff)
Generate all implementation artifacts:
- Generate epic and story files from design artifacts
- Component specs for all new components
- Design tokens in W3C DTCG format
- Output: stories → `_bmad-output/implementation-artifacts/stories/`
- Output: `component-specs.md`, `design-tokens.json` → `_bmad-output/pdx-artifacts/`

After generating stories, Relay also compiles all PDX artifacts into
`_bmad-output/planning-artifacts/UX_Design.md` for BMAD dev agent compatibility.
This ensures the dev agent has a consolidated UX spec in the format it expects,
replacing Sally's output with PDX's richer pipeline output. Run task
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
- Output: updated story files, `pm-review-[scope].md` → `_bmad-output/pdx-artifacts/`
- Report: "Phase 9 complete — PM review: [APPROVED/APPROVED WITH CHANGES/FLAGGED]"

### Phase 10: SM (BMAD) — Sprint Planning
Plan and assign sprints:
- Read team velocity and capacity
- Assign stories to sprints (P0 first)
- Sequence work within sprints
- IF total points exceed capacity → split across sprints
- Output: updated `sprint-status.yaml`, `sprint-plan-[sprint-number].md` → `_bmad-output/implementation-artifacts/`
- Report: "Phase 10 complete — stories assigned to Sprint [number], [points] points planned"

### Phase 11: Dev (BMAD) — Implementation
Stories are ready for development:
- Pick up stories with `/ds`
- All design context available in `pdx-artifacts/`
- Architecture available in `planning-artifacts/`

---

## BROWNFIELD Pipeline (8 phases)
For existing projects with sprint-status.yaml.

### Phase 2: Nova 🔍 — Research (Smart Skip)

Before running any research, check what already exists in _bmad-output/pdx-artifacts/:

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

   Skipping to Kai with existing research as context."

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

If the PM already created PDX-format artifacts during PRD creation, those are valid — Nova skips redundant work.

- Output: new/updated artifacts → `_bmad-output/pdx-artifacts/`
- Report: "Phase 2 complete — [n] research artifacts ([m] new, [k] referenced existing) using [methods list]"

### Phase 3: Kai (PDX Design)
Design solutions for the feature:
- User flows for the specific feature
- State diagrams for complex components
- Wireframes for new/changed screens only
- Output → `_bmad-output/pdx-artifacts/`
- Report: "Phase 3 complete — [n] design artifacts produced"

### Phase 4: Lux 🎨 — Visual Polish
Same as greenfield Phase 4. Reviews Kai's brownfield designs for visual quality.
Skippable with --skip-visual flag.

- Output: `visual-polish-[scope].md` → `_bmad-output/pdx-artifacts/`
- Report: "Phase 4 complete — visual polish [applied/skipped/no issues found]"

### Phase 5: Echo (PDX Content)
Content for new/changed screens:
- Microcopy for new screens
- Error messages for new error states
- Empty states for new screens
- Output → `_bmad-output/pdx-artifacts/`
- Report: "Phase 5 complete — [n] content artifacts produced"

### Phase 6: Sage (PDX QA)
Focused QA on new designs:
- Design review on new designs only
- Accessibility check on new/changed screens
- IF NO-GO → loop back to Kai
- Output → `_bmad-output/pdx-artifacts/`
- Report: "Phase 6 complete — verdict: [GO/CONDITIONAL/NO-GO]"

### Phase 7: Relay (PDX Handoff)
Handoff continuing from existing state:
- Stories continue from existing numbering
- Append to existing epics or create new ones
- Component specs for new components only
- Tokens added to existing token file
- Output: stories → `_bmad-output/implementation-artifacts/stories/`

After generating stories, Relay also updates
`_bmad-output/planning-artifacts/UX_Design.md` with the new/changed sections.
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

### Phases 2-5: Nova → Kai → Lux → Echo
Same as greenfield Phases 2-5.

### Phase 6: Architect (BMAD)
Same as greenfield Phase 6.

### Phases 7-10: Sage → Relay → PM → SM
Same as greenfield Phases 7-10.

---

## Post-Pipeline Report
After all phases complete, output a summary:
```
PDX Design Sprint Complete — [Feature/Scope]

Detected: [GREENFIELD/BROWNFIELD/MID-PROJECT]
Pipeline: Nova → Kai → Lux → Echo → Sage → Relay → PM → SM

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
Skip research phase. Runs: Kai → Lux → Echo → Sage → Relay → PM → SM.
Triggered by `/quick-sprint`.

## Research Only Variant
Run only Nova. Save findings for later pipeline execution.
Triggered by `/research-only`.

## Handoff Only Variant
Run Relay → PM → SM against existing pdx-artifacts/.
Triggered by `/handoff-only`.
