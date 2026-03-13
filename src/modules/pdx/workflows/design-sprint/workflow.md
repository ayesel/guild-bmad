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
Pipeline: Nova → Kai → Echo → Sage → Relay → PM → SM (7 phases)

**If prd.md exists but no sprint-status.yaml → MID-PROJECT**
Planning happened but implementation hasn't started. Skip Analyst, include Architect.
Pipeline: PM → Nova → Kai → Echo → Architect → Sage → Relay → PM → SM (9 phases)

**If nothing exists → GREENFIELD**
Brand new project. Run full pipeline including Analyst, PM, and Architect.
Pipeline: Analyst → PM → Nova → Kai → Echo → Architect → Sage → Relay → PM → SM (11 phases)

Report detection to user:
"Detected: [GREENFIELD/BROWNFIELD/MID-PROJECT]. Running [X]-phase pipeline."

## Pre-flight (after detection)
1. Read any existing BMAD artifacts identified during detection
2. Read `_bmad-output/planning-artifacts/project-context.md` if it exists
3. Read existing `_bmad-output/pdx-artifacts/` — don't repeat prior work
4. Ask user ONE clarifying question if scope is ambiguous
5. Confirm: "I'll run the [GREENFIELD/BROWNFIELD/MID-PROJECT] pipeline on [scope]. Ready?"

---

## GREENFIELD Pipeline (11 phases)
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

### Phase 2: Nova (PDX Research)
Generate foundational research from PRD:
- Generate personas from PRD user descriptions
- Competitive audit of similar products
- JTBD mapping for core user jobs
- Output: `personas.md`, `competitive-audit.md`, `jtbd.md` → `_bmad-output/pdx-artifacts/`
- Report: "Phase 2 complete — [n] research artifacts produced"

### Phase 3: Kai (PDX Design)
Create full product design from research:
- Site map / information architecture for full product
- User flows for each epic
- Wireframes for key screens
- State diagrams for complex components
- Output: `site-map.md`, `user-flow-*.md`, `wireframe-*.md` → `_bmad-output/pdx-artifacts/`
- Report: "Phase 3 complete — [n] design artifacts produced"

### Phase 4: Echo (PDX Content)
Write all product content:
- Voice and tone guidelines
- All screen microcopy
- Error message system
- Empty states for all screens
- Onboarding copy
- Output: `voice-tone.md`, `microcopy-*.md`, `error-messages.md`, `empty-states.md` → `_bmad-output/pdx-artifacts/`
- Report: "Phase 4 complete — [n] content artifacts produced"

### Phase 5: Architect (BMAD)
Create technical architecture:
- System architecture based on PRD + PDX design artifacts
- Tech stack decisions informed by component specs
- Data model, API design, infrastructure
- Output: `architecture.md` → `_bmad-output/planning-artifacts/`
- Report: "Phase 5 complete — architecture document created"

### Phase 6: Sage (PDX QA)
Quality gate on all design work:
- Design review on all Kai artifacts
- Accessibility audit
- Content QA on all Echo output
- Pre-handoff quality gate
- IF NO-GO → loop back to relevant phase with issues
- IF GO/CONDITIONAL → continue
- Output: `qa-report.md` → `_bmad-output/pdx-artifacts/`
- Report: "Phase 6 complete — verdict: [GO/CONDITIONAL/NO-GO]"

### Phase 7: Relay (PDX Handoff)
Generate all implementation artifacts:
- Generate epic and story files from design artifacts
- Component specs for all new components
- Design tokens in W3C DTCG format
- Output: stories → `_bmad-output/implementation-artifacts/stories/`
- Output: `component-specs.md`, `design-tokens.json` → `_bmad-output/pdx-artifacts/`
- Report: "Phase 7 complete — [n] stories generated ([story range])"

### Phase 8: PM (BMAD) — Story Review
Validate stories against PRD:
- Check story alignment with PRD and product goals
- Validate prioritization (P0/P1/P2)
- Verify acceptance criteria are complete and testable
- Identify missing or out-of-scope stories
- IF APPROVED → continue
- IF FLAGGED → pause for user confirmation
- Output: updated story files, `pm-review-[scope].md` → `_bmad-output/pdx-artifacts/`
- Report: "Phase 8 complete — PM review: [APPROVED/APPROVED WITH CHANGES/FLAGGED]"

### Phase 9: SM (BMAD) — Sprint Planning
Plan and assign sprints:
- Read team velocity and capacity
- Assign stories to sprints (P0 first)
- Sequence work within sprints
- IF total points exceed capacity → split across sprints
- Output: updated `sprint-status.yaml`, `sprint-plan-[sprint-number].md` → `_bmad-output/implementation-artifacts/`
- Report: "Phase 9 complete — stories assigned to Sprint [number], [points] points planned"

### Phase 10: Dev (BMAD) — Implementation
Stories are ready for development:
- Pick up stories with `/ds`
- All design context available in `pdx-artifacts/`
- Architecture available in `planning-artifacts/`

---

## BROWNFIELD Pipeline (7 phases)
For existing projects with sprint-status.yaml.

### Phase 2: Nova (PDX Research)
Targeted research on the feature scope:
- Reference existing personas (update if needed)
- Heuristic eval or journey map for the specific feature
- Skip competitive audit unless feature is entirely new
- Output → `_bmad-output/pdx-artifacts/`
- Report: "Phase 2 complete — [n] research artifacts produced"

### Phase 3: Kai (PDX Design)
Design solutions for the feature:
- User flows for the specific feature
- State diagrams for complex components
- Wireframes for new/changed screens only
- Output → `_bmad-output/pdx-artifacts/`
- Report: "Phase 3 complete — [n] design artifacts produced"

### Phase 4: Echo (PDX Content)
Content for new/changed screens:
- Microcopy for new screens
- Error messages for new error states
- Empty states for new screens
- Output → `_bmad-output/pdx-artifacts/`
- Report: "Phase 4 complete — [n] content artifacts produced"

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
- Report: "Phase 7 complete — [n] stories generated ([story range])"

### Phase 8: PM (BMAD) — Story Review
Same as greenfield Phase 8.

### Phase 9: SM (BMAD) — Sprint Planning
Fit new stories into current or next sprint.

---

## MID-PROJECT Pipeline (9 phases)
PRD exists but no sprints yet. Skip Analyst, include Architect.

### Phase 1: PM (BMAD) — PRD Review
Review existing PRD (validate, don't recreate):
- Confirm PRD is current and complete
- Flag any gaps or outdated sections
- Output: updated `prd.md` if changes needed
- Report: "Phase 1 complete — PRD validated"

### Phases 2-4: Nova → Kai → Echo
Same as greenfield Phases 2-4.

### Phase 5: Architect (BMAD)
Same as greenfield Phase 5.

### Phases 6-9: Sage → Relay → PM → SM
Same as greenfield Phases 6-9.

---

## Post-Pipeline Report
After all phases complete, output a summary:
```
PDX Design Sprint Complete — [Feature/Scope]

Detected: [GREENFIELD/BROWNFIELD/MID-PROJECT]
Pipeline: [phase sequence]

Artifacts produced: [count]
Research: [list]
Designs: [list]
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
Skip research phase. Runs: Kai → Echo → Sage → Relay → PM → SM.
Triggered by `/quick-sprint`.

## Research Only Variant
Run only Nova. Save findings for later pipeline execution.
Triggered by `/research-only`.

## Handoff Only Variant
Run Relay → PM → SM against existing pdx-artifacts/.
Triggered by `/handoff-only`.
