# PDX Integration Spec for Asmar Inc Pipeline

## Overview

This document maps PDX Design Framework into Asmar Inc's existing BMAD pipeline, quality gates, artifact flow, issue chain, and KB structure. PDX replaces Sally (UX Designer) with a 7-agent design sprint that produces richer artifacts in the same locations Jonny's system expects.

---

## 1. Pipeline Integration

### Current Asmar BMAD Pipeline
```
CEO (Atlas) → Analyst (Mary) → PM (John) → [Sally] → Architect (Winston) → SM (Bob) → Dev (Amelia) → Review (Priya) → QA (Quinn) → Release
```

### With PDX Replacing Sally
```
CEO (Atlas) → Analyst (Mary) → PM (John) → [Guild Design Sprint] → Architect (Winston) → SM (Bob) → Dev (Amelia) → Review (Priya) → QA (Quinn) → Release
```

### What PDX Does in That Slot

The `[Guild Design Sprint]` expands into:

```
PM (John) hands off PRD
    |
Nova --- Research (if needed)
    | validates/extends PM's personas and journey maps
Kai --- Interaction Design
    | flows, wireframes, state diagrams
Visual Designer --- Visual Polish
    | hierarchy, spacing, color, typography
Echo --- Content
    | microcopy, errors, empty states
Sage --- QA Gate
    | GO / CONDITIONAL / NO-GO
Relay --- Handoff
    | UX spec, component specs, tokens
Architect (Winston) picks up
```

If Sage says NO-GO, the pipeline loops back to Kai — it never reaches Winston with broken designs.

### Pipeline Type Mapping

| Asmar Pipeline Type | PDX Involvement |
|---------------------|----------------|
| **Full BMAD** | Full PDX design sprint (all 7 agents) |
| **RFC / Quick-Spec** | PDX quick sprint (Kai -> Visual Designer -> Echo -> Sage -> Relay, skip Nova) |
| **Quick-Dev** | No PDX (too small for design work) |
| **Hotfix** | No PDX (emergency path) |

### CEO Classification Update

Add to the CEO classification decision tree:

```
New goal/initiative received
    |
    +-- New product or major feature?
    |     +-- Has UI components? --> Full BMAD with Guild Design Sprint
    |     +-- Backend only? --> Full BMAD without PDX
    |
    +-- Moderate enhancement to existing system?
    |     +-- UI changes needed? --> RFC with PDX Quick Sprint
    |     +-- Backend only? --> RFC without PDX
    |
    +-- Simple, well-defined change?
    |     +-- Quick-Dev (no PDX)
    |
    +-- Production emergency?
          +-- Hotfix (no PDX)
```

---

## 2. Artifact Flow Integration

### Current Asmar Artifact Table

| Phase | Role | Artifact | KB Path |
|-------|------|----------|---------|
| Discovery | Analyst (Mary) | Product Brief | `projects/{name}/brief.md` |
| Requirements | PM (John) | PRD | `projects/{name}/prd.md` |
| UX Design | ~~Sally~~ | ~~UX Specification~~ | ~~`projects/{name}/ux-spec.md`~~ |
| Architecture | Architect (Winston) | Architecture Decision Document | `projects/{name}/architecture.md` |
| Planning | SM (Bob) | Epic Breakdowns | `projects/{name}/epics/` |

### Updated with PDX

| Phase | Role | Artifact | KB Path |
|-------|------|----------|---------|
| Discovery | Analyst (Mary) | Product Brief | `projects/{name}/brief.md` |
| Requirements | PM (John) | PRD | `projects/{name}/prd.md` |
| **UX Research** | **Nova** | **Personas** | **`projects/{name}/guild/personas.md`** |
| **UX Research** | **Nova** | **Journey Maps** | **`projects/{name}/guild/journey-maps.md`** |
| **UX Research** | **Nova** | **Competitive Audit** | **`projects/{name}/guild/competitive-audit.md`** |
| **UX Design** | **Kai** | **User Flows** | **`projects/{name}/guild/user-flows.md`** |
| **UX Design** | **Kai** | **Wireframes** | **`projects/{name}/guild/wireframes.md`** |
| **UX Design** | **Kai** | **State Diagrams** | **`projects/{name}/guild/state-diagrams.md`** |
| **Visual Polish** | **Visual Designer** | **Visual Polish Report** | **`projects/{name}/guild/visual-polish.md`** |
| **Content** | **Echo** | **Microcopy + Errors** | **`projects/{name}/guild/content.md`** |
| **Design QA** | **Sage** | **QA Report** | **`projects/{name}/guild/qa-report.md`** |
| **UX Spec** | **Relay** | **UX Specification (compiled)** | **`projects/{name}/ux-spec.md`** |
| **Handoff** | **Relay** | **Component Specs** | **`projects/{name}/guild/component-specs.md`** |
| **Handoff** | **Relay** | **Design Tokens** | **`projects/{name}/guild/design-tokens.json`** |
| Architecture | Architect (Winston) | Architecture Decision Document | `projects/{name}/architecture.md` |
| Planning | SM (Bob) | Epic Breakdowns | `projects/{name}/epics/` |

### Key Points:
- Guild artifacts live in `projects/{name}/guild/` subdirectory in the KB
- Relay compiles the UX Specification to `projects/{name}/ux-spec.md` — the same path Sally used
- Winston (Architect) reads `ux-spec.md` the same way he always did — he doesn't need to know PDX generated it
- Individual Guild artifacts (personas, flows, etc.) are available for deeper reference

---

## 3. Quality Gate Integration

### New Gate: Gate 2.5 — Design to Architecture (PDX to Architect)

Insert between Gate 2 (Requirements to Architecture) and Gate 3 (Architecture to Stories):

**Gate 2.5: Design to Architecture (PDX Sage -> Architect)**

**Artifact:** UX Specification + PDX Design Artifacts

**Checklist (Sage's pre-handoff quality gate):**

- [ ] All user flows have complete state coverage (empty, loading, error, populated, disabled)
- [ ] All error paths have recovery actions
- [ ] Accessibility requirements documented (WCAG AA minimum)
- [ ] Visual hierarchy is clear on every screen (squint test)
- [ ] Spacing follows consistent scale
- [ ] Typography uses max 3 sizes per screen
- [ ] Color usage is semantic (every color has a purpose)
- [ ] All microcopy is final (no placeholder text)
- [ ] Error messages follow "what happened + what to do" pattern
- [ ] Component specs include props, states, and ARIA attributes
- [ ] Design tokens defined for all new visual values
- [ ] UX Specification compiled and saved to KB path
- [ ] All Guild artifacts saved to KB `projects/{name}/guild/` directory

**Sage Verdict:**
- **GO** -> Create Architecture issue, hand off to Winston
- **CONDITIONAL** -> List conditions, proceed with Architecture but flag items for resolution during implementation
- **NO-GO** -> Loop back to Kai, do not proceed to Architecture

### Updated Gate 2 (Requirements to Architecture)

Add to existing checklist:
- [ ] If project has UI components: PDX design sprint completed with GO or CONDITIONAL verdict
- [ ] UX Specification exists at `projects/{name}/ux-spec.md`
- [ ] PDX personas and journey maps informed the PRD (reference check)

### Updated Gate 4 (Stories to Implementation)

Add to per-story checklist:
- [ ] If story involves UI: PDX design artifacts referenced in story's References section
- [ ] Component specs from PDX included for new UI components
- [ ] Design tokens referenced (not hardcoded values)

---

## 4. Issue Chain Integration

### Current Pattern
```
ASM-1:  [CEO] Initiative: Build User Auth System          -> Atlas
ASM-2:  [ANALYST] Discovery: User Auth System              -> Mary
ASM-3:  [PM] Create PRD: User Auth System                  -> John
ASM-4:  [UX] Design UX: User Auth System                   -> Sally
ASM-5:  [ARCH] Create Architecture: User Auth System        -> Winston
```

### With PDX
```
ASM-1:  [CEO] Initiative: Build User Auth System          -> Atlas
ASM-2:  [ANALYST] Discovery: User Auth System              -> Mary
ASM-3:  [PM] Create PRD: User Auth System                  -> John
ASM-4:  [PDX] Design Sprint: User Auth System              -> PDX Orchestrator
        +-- Nova: Research (personas, journey maps)
        +-- Kai: Interaction design (flows, wireframes)
        +-- Visual Designer: Visual polish
        +-- Echo: Content (copy, errors)
        +-- Sage: QA gate -> GO
        +-- Relay: UX spec + component specs + tokens
ASM-5:  [ARCH] Create Architecture: User Auth System        -> Winston
ASM-6:  [SM] Create Epics & Stories: User Auth System       -> Bob
```

The Guild design sprint is ONE issue (ASM-4) that internally runs 7 agents. The issue description includes:
- Input: KB path to PRD
- Output: KB paths to all Guild artifacts + UX spec
- Sage verdict: GO / CONDITIONAL / NO-GO
- Summary of key design decisions

### Issue Description Template for PDX

```markdown
## [PDX] Design Sprint: {Feature Name}

**Pipeline:** Full BMAD -> Guild Design Sprint
**Input PRD:** projects/{name}/prd.md
**Parent Issue:** ASM-{N} (PM PRD)

### PDX Pipeline Status

| Phase | Agent | Status | Artifact |
|-------|-------|--------|----------|
| Research | Nova | --- | projects/{name}/guild/personas.md |
| Design | Kai | --- | projects/{name}/guild/user-flows.md |
| Visual | Visual Designer | --- | projects/{name}/guild/visual-polish.md |
| Content | Echo | --- | projects/{name}/guild/content.md |
| QA | Sage | --- | projects/{name}/guild/qa-report.md |
| Handoff | Relay | --- | projects/{name}/ux-spec.md |

### Sage Verdict
{GO / CONDITIONAL / NO-GO}

### Conditions (if CONDITIONAL)
{List of conditions to address during implementation}

### Key Design Decisions
{Top 3-5 design decisions with rationale}

### Next Step
Create issue: [ARCH] Create Architecture: {Feature Name} -> Winston
Reference: projects/{name}/ux-spec.md
```

---

## 5. Artifact Commit Convention

Following Asmar's existing pattern:

```bash
# PDX design artifacts
docs({project}): add PDX personas
docs({project}): add PDX journey maps
docs({project}): add PDX user flows
docs({project}): add PDX wireframes
docs({project}): add PDX content spec
docs({project}): add PDX QA report
docs({project}): add UX specification

# Combined (if committing all at once after design sprint)
docs({project}): add PDX design sprint artifacts
```

---

## 6. KB Directory Structure

### Per-Project PDX Artifacts

```
projects/{name}/
+-- brief.md                    # Analyst (Mary)
+-- prd.md                      # PM (John)
+-- ux-spec.md                  # Relay (compiled UX spec -- replaces Sally's output)
+-- architecture.md             # Architect (Winston)
+-- epics/                      # SM (Bob)
|   +-- epic-1-auth.md
|   +-- epic-2-dashboard.md
+-- guild/                        # Guild Design Sprint artifacts
    +-- personas.md             # Nova
    +-- journey-maps.md         # Nova
    +-- competitive-audit.md    # Nova (if run)
    +-- heuristic-eval.md       # Nova (if run)
    +-- user-flows.md           # Kai
    +-- wireframes.md           # Kai
    +-- state-diagrams.md       # Kai (if needed)
    +-- site-map.md             # Kai (if needed)
    +-- visual-polish.md        # Visual Designer
    +-- content.md              # Echo (microcopy, errors, empty states)
    +-- qa-report.md            # Sage
    +-- component-specs.md      # Relay
    +-- design-tokens.json      # Relay
```

---

## 7. Phase Transition — PDX Handoff Protocol

When PDX completes a design sprint, the handoff follows Asmar's existing convention:

1. **Commit artifacts** to KB repo at `projects/{name}/guild/` and `projects/{name}/ux-spec.md`
2. **Comment on the PDX issue** with completion summary:
   ```
   Guild Design Sprint Complete -- {Feature Name}

   Pipeline: Nova -> Kai -> Visual Designer -> Echo -> Sage -> Relay
   Sage Verdict: {GO/CONDITIONAL}
   Artifacts: projects/{name}/guild/ (7 files)
   UX Spec: projects/{name}/ux-spec.md

   Key findings:
   - {finding 1}
   - {finding 2}
   - {finding 3}

   Ready for: [ARCH] Architecture phase -> Winston
   ```
3. **Mark the PDX issue** as done
4. **Create the next-phase issue** for Architecture, assigned to Winston
5. **Include context** in the Architecture issue: KB path to ux-spec.md, summary of key design decisions, reference to PDX issue for traceability
6. **Self-sufficient handoff** — Winston should be able to work from ux-spec.md without reading the full Guild artifact chain (though he can reference guild/ for details)

---

## 8. Relay Output Configuration

To support Asmar's KB structure, Relay needs a configurable output path. The Guild module.yaml config section includes:

```yaml
config:
  kb_output_path:
    prompt: "KB artifact path (e.g., projects/auth-system/):"
    default: "_bmad-output/guild-artifacts/"
    result: "{value}"
  kb_ux_spec_path:
    prompt: "UX spec output path:"
    default: "_bmad-output/planning-artifacts/UX_Design.md"
    result: "{value}"
```

When `kb_output_path` is set to a KB project path:
- All Guild artifacts write to `{kb_output_path}/guild/`
- UX spec writes to `{kb_output_path}/ux-spec.md`
- Stories still write to `_bmad-output/implementation-artifacts/stories/` (BMAD needs these locally)

When `kb_output_path` is default:
- Everything writes to `_bmad-output/guild-artifacts/` as normal
- UX spec writes to `_bmad-output/planning-artifacts/UX_Design.md`

This means PDX works both standalone (BMAD default paths) and integrated (Asmar KB paths) with one config change.

---

## 9. Paperclip Integration (Future)

If/when Paperclip manages the ticket system:

- PDX design sprint becomes a Paperclip task assigned to the PDX Orchestrator agent
- Each PDX sub-agent (Nova, Kai, etc.) could be a Paperclip agent with heartbeats
- Sage's QA verdict maps to Paperclip's governance approval flow
- Relay's stories become Paperclip tickets assigned to Dev agents
- Cost tracking per design sprint via Paperclip's budget system

This is future state — requires Jonny to configure Guild agents in Paperclip's org chart.

---

## 10. Implementation Steps

When Jonny is ready to integrate:

### Step 1: Install PDX in the project
```bash
cp -r /path/to/guild-bmad/src/modules/guild/ ./src/modules/guild/
cat src/modules/guild/install/claude-md-snippet.md >> CLAUDE.md
```

### Step 2: Configure KB output path
Set `kb_output_path` in Guild module config to match the KB project path.

### Step 3: Update Asmar KB pipeline docs
- Replace Sally with PDX in BMAD Pipeline page
- Add Gate 2.5 to Quality Gates page
- Update Pipeline Types to reference PDX for Full BMAD and RFC
- Add PDX issue template to issue chain conventions

### Step 4: Test end-to-end
Run a PDX design sprint on one feature, verify:
- Artifacts appear in correct KB paths
- ux-spec.md is readable by Winston (Architect)
- Stories are in BMAD format for Amelia (Dev)
- Quality gate passes Sage's checklist

### Step 5: Update CEO classification
Atlas should route UI-heavy work through PDX automatically.
