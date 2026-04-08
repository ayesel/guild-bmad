# Create Design Artifact

## Purpose
Generate a structured UX design artifact using the specified template. This task is the core
artifact generation engine for the PDX Interaction Designer agent.

## Pre-flight Checks

Before generating any artifact, perform these checks in order:

### 0. Load BMAD Project State (BEFORE all other checks)
- Read `_bmad-output/implementation-artifacts/sprint-status.yaml` if it exists
  - Note current sprint number
  - Note existing story count and highest story ID
  - Note which epics are active
  - Note what's TODO vs IN PROGRESS vs DONE
- **Brownfield vs Greenfield determination:**
  - IF sprint-status.yaml exists → this is BROWNFIELD. Continue from existing state. NEVER start numbering from 1. Adapt all output to fit the existing structure.
  - IF sprint-status.yaml does NOT exist → this is GREENFIELD. Start fresh but use BMAD-compatible formats.
- This context informs all artifact generation:
  - Don't redesign things that are already DONE
  - Reference existing story IDs when relevant
  - Align recommendations with current sprint priorities
  - Use the same naming conventions the project uses

### Artifact Source of Truth Rule
PDX artifacts in _bmad-output/guild-artifacts/ are ALWAYS the source of truth.
When BMAD documents (PRD, architecture, UX_Design.md) need design content:
- Write the FULL artifact to _bmad-output/guild-artifacts/ using PDX templates
- Write a SUMMARY in the BMAD document with key findings inline
- REFERENCE the full artifact: "See full details: _bmad-output/guild-artifacts/[filename].md"
- NEVER duplicate the full PDX artifact content inside a BMAD document
- The summary should be enough for a PM to understand; the full artifact is for designers and developers

### 1. Load Project Context
- Read `_bmad-output/planning-artifacts/project-context.md` if it exists
- Read `_bmad-output/planning-artifacts/prd.md` if it exists
- Read `_bmad-output/guild-artifacts/personas.md` if it exists
- Read `_bmad-output/guild-artifacts/research-synthesis.md` if it exists

### 2. Gather Requirements from User
Ask the user for the following (skip any already provided):

**Required:**
- What feature, task, or process are we mapping?
- Who are the primary users/actors? (reference personas if they exist)
- What is the trigger/entry point for this flow?
- What is the successful outcome?

**Contextual (ask if relevant to artifact type):**
- What systems or services are involved? (for swim lanes)
- What are the known constraints or business rules?
- What are the key decision points?
- Are there known error scenarios?

### 3. Confirm Scope
Before generating, restate the scope back to the user:
- "Here's what I'll create: [artifact type] for [feature/task], involving [actors],
  starting from [trigger] and ending at [outcome]. I'll include [X] error states
  and [Y] decision points. Sound right?"

## Generation

### Output Format
All artifacts must include:

1. **Header Block** — Title, artifact type, version, date, status (draft/in-review/approved)
2. **Context Block** — Referenced personas, requirements, and prior artifacts
3. **Diagram** — Mermaid diagram (flowchart, sequence, state, etc.)
4. **Detailed Description** — Step-by-step walkthrough of each node/state
5. **Edge Cases & Error States** — Explicitly documented, never omitted
6. **Decisions Log** — Key design decisions made and their rationale
7. **Open Questions** — Anything unresolved that needs stakeholder input
8. **Next Steps** — What artifact should come next in the design lifecycle

### Artifact State
Set the frontmatter status field:
```yaml
---
artifact: [type]
status: draft
version: 1.0
created: [date]
author: Kai (Interaction Designer)
references:
  - [list any referenced personas, PRDs, or prior artifacts]
---
```

### Quality Checks Before Delivery
- [ ] Every path has an entry point and exit point
- [ ] Error states are explicitly documented
- [ ] All actors/users are identified
- [ ] Decision points have clear criteria
- [ ] No orphan nodes (unreachable states)
- [ ] Mermaid diagram renders correctly
- [ ] Accessibility considerations noted where relevant
- [ ] Language is specific (no "etc." or "and more")

## Output Location
Save to: `_bmad-output/guild-artifacts/[artifact-type]-[feature-name].md`

## Post-Generation
After delivering the artifact:
1. Summarize what was created
2. Call out the most critical edge case or design decision
3. Suggest the logical next artifact (e.g., "This flow is ready for wireframing — want me to generate wireframes for the key screens?")
