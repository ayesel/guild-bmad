# Create Handoff

## Purpose
Generate developer-ready handoff artifacts using the specified template. This task is the
core handoff engine for the Guild Design Ops agent.

## Pre-flight Checks

Before creating any handoff artifact, perform these checks in order:

### 0. Detect Mode and Load Project State (BEFORE all other checks)

**Mode detection:**
- Read `guild.config.yaml` for `bmad_mode` setting
- If `bmad_mode: auto` → check if `_bmad/core/config.yaml` exists
  - If YES → bmad_mode = true, use jira-stories-template.yaml (BMAD dev-story format)
  - If NO → bmad_mode = false, use stories-template.yaml (standard format)

**Load project state:**
- Read `{output_root}/implementation-artifacts/sprint-status.yaml` if it exists
  - Note current sprint number
  - Note existing story count and highest story ID (e.g., STORY-47)
  - Note which epics are active and highest epic ID
  - Note what's TODO vs IN PROGRESS vs DONE
- Read `{output_root}/planning-artifacts/` for existing PRD, architecture docs, and epic files
- **Brownfield vs Greenfield determination:**
  - IF sprint-status.yaml exists → this is BROWNFIELD. Continue from existing state. NEVER start numbering from 1. Adapt all output to fit the existing structure.
  - IF sprint-status.yaml does NOT exist → this is GREENFIELD. Start from STORY-1, EPIC-1.
- This context is CRITICAL for handoff — it determines:
  - Story numbering (new stories start after the highest existing ID)
  - Sprint assignment (current sprint, or next if current is full — bmad_mode only)
  - Epic assignment (existing epic or new epic continuing the numbering)
  - What's already been built (don't hand off work that's DONE)

### Artifact Source of Truth Rule
Guild artifacts in {output_root}/guild-artifacts/ are ALWAYS the source of truth.
When BMAD documents (PRD, architecture, UX_Design.md) need design content:
- Write the FULL artifact to {output_root}/guild-artifacts/ using Guild templates
- Write a SUMMARY in the BMAD document with key findings inline
- REFERENCE the full artifact: "See full details: {output_root}/guild-artifacts/[filename].md"
- NEVER duplicate the full Guild artifact content inside a BMAD document
- The summary should be enough for a PM to understand; the full artifact is for designers and developers

### 1. Load ALL Prior Guild .rtifacts
- Read `{output_root}/planning-artifacts/project-context.md` if it exists
- Read `{output_root}/planning-artifacts/prd.md` if it exists
- Read any flows or wireframes from Rogue in `{output_root}/guild-artifacts/`
- Read any research or personas from Ranger in `{output_root}/guild-artifacts/`
- Read any QA reports from Sage in `{output_root}/guild-artifacts/`
- Read any content from Warlock in `{output_root}/guild-artifacts/`
- Read `{output_root}/guild-artifacts/design-tokens.json` if it exists

### 2. Gather Handoff Parameters from User
Ask the user for the following (skip any already provided):

**Required:**
- What feature, screen, or component are we handing off?
- What is the target sprint or release?
- What framework is engineering using? (React, React Native, Vue, etc.)

**Contextual (ask if relevant to handoff type):**
- What state management approach? (useState, Redux, Zustand, etc.)
- What design token format? (W3C DTCG, Style Dictionary, CSS custom properties)
- What component library is in use? (MUI, Radix, Shadcn, custom)
- What Jira project key and epic structure?
- What is the existing component naming convention?

### 3. Confirm Scope
Before generating, restate the scope back to the user:
- "Here's what I'll create: [handoff type] for [feature/screen],
  targeting [framework] in [sprint/release]. I'll reference [n] existing
  artifacts from [Rogue/Ranger/Sage/Warlock]. Sound right?"

### When generating stories from Guild artifacts:
- Each story's design_artifacts field should reference the specific Guild artifact files
- Example: design_artifacts: ["{output_root}/guild-artifacts/user-flow-onboarding.md", "{output_root}/guild-artifacts/wireframe-onboarding.md"]
- The dev agent follows these references to get full design context
- Don't inline the entire design spec in the story — reference it

### Story Format Rules (CRITICAL — BMAD Compatibility)

Every story file MUST match BMAD's dev-story template exactly. The dev agent
expects these sections in this order:

1. `# Story {epic}.{story}: {title}` — H1 header
2. `## Story` — User story in As a/I want to/So that format + description
3. `## Acceptance Criteria` — Strict BDD (Given/When/Then), numbered, no named ACs
4. `## Tasks / Subtasks` — Checkboxes with AC references in parentheses
5. `## Dev Notes` — Technical guidance
   - `### Project Structure Notes` — File paths for new/modified files
   - `### References` — Links to PRD, architecture, Guild artifacts, related stories
6. `## Dev Agent Record` — Empty scaffolding (dev agent fills this in)
   - `### Agent Model Used`
   - `### Debug Log References`
   - `### Completion Notes List`
   - `### File List`

DO NOT:
- Add a ## Context section (fold into Dev Notes)
- Use named ACs ("AC1 — Schema Migration") — use Given/When/Then only
- Skip the Dev Agent Record section — it's required scaffolding
- Skip Project Structure Notes — dev agent needs file paths
- Skip References — dev agent needs artifact links

## Execution

### Output Format
All handoff deliverables must include:

1. **Header Block** — Title, handoff type, version, date, target sprint, framework
2. **Source Artifacts** — Links to all referenced Rogue/Ranger/Sage/Warlock artifacts
3. **Specification Content** — Per template structure
4. **Code-Ready References** — Token names, component props, ARIA attributes
5. **Acceptance Criteria** — Given/When/Then for every scenario
6. **Edge Cases** — From Rogue's flows and Sage's QA reports
7. **Open Questions** — Anything engineering needs to clarify
8. **Next Steps** — Follow-up handoff artifacts needed

### Handoff State
Set the frontmatter status field:
```yaml
---
artifact: [handoff type]
status: draft
version: 1.0
created: [date]
author: Healer (Design Ops)
target_sprint: "[sprint identifier]"
engineering_framework: "[React|React Native|Vue|etc.]"
source_artifacts:
  - [list all referenced Guild artifacts]
references:
  - [list design system, component library, Jira project]
---
```

### Quality Checks Before Delivery
- [ ] All states specified (empty, loading, error, populated, disabled)
- [ ] Responsive behavior documented for all breakpoints
- [ ] Design tokens referenced by name (not raw values)
- [ ] Acceptance criteria in Given/When/Then format
- [ ] ARIA roles and attributes specified for interactive elements
- [ ] Copy is final (from Warlock) not placeholder
- [ ] Edge cases documented (from Rogue and Sage)
- [ ] API/data requirements noted
- [ ] Dependencies identified (blocked-by / blocks)
- [ ] A developer can implement without asking a designer

## BMAD-Compatible Story Generation

When generating stories (via jira-stories template or as part of handoff), stories MUST
integrate with existing BMAD sprint state:

### Story Numbering
- Read the highest story ID from `{output_root}/implementation-artifacts/sprint-status.yaml`
- New stories start at the next sequential ID (e.g., if STORY-47 exists, start at STORY-48)
- Never reuse or conflict with existing story IDs

### Story Format
Stories must be compatible with BMAD's dev-story workflow:
```yaml
story_id: "STORY-XX"
title: "As a [persona], I want [action], so that [outcome]"
status: "TODO"  # TODO | IN PROGRESS | READY FOR REVIEW | DONE
epic: "EPIC-XX"
points: X
priority: "P0"  # P0 | P1 | P2
acceptance_criteria:
  - "Given [context], When [action], Then [result]"
design_artifacts:
  - "{output_root}/guild-artifacts/[referenced-file].md"
```

### Sprint Assignment
- If the current sprint has capacity, assign stories to the current sprint
- If the current sprint is full (>20 story points remaining), assign to the next sprint
- If sprint-status.yaml doesn't exist, generate stories without sprint assignment and warn the user

### Epic Numbering
- Continue from existing epic numbering (e.g., if EPIC-5 exists, new epics start at EPIC-6)
- Assign to existing epics when the scope matches

### Output Locations
- Story files: `{output_root}/implementation-artifacts/stories/STORY-XX-[slug].yaml`
- Update sprint-status.yaml: APPEND new stories to the existing file (never overwrite)
- Stories should be immediately consumable by BMAD's `/dev-story` workflow

## Output Location

Output paths are configurable via `kb_output_path` in module.yaml:
- If `kb_output_path` is set to a KB project path (e.g., `projects/auth-system/`):
  - Guild artifacts: `{kb_output_path}/guild/`
  - UX spec: `{kb_output_path}/ux-spec.md`
- If `kb_output_path` is default (`{output_root}/guild-artifacts/`):
  - Handoff specs: `{output_root}/guild-artifacts/handoff-[type]-[scope].md`
  - UX spec: `{output_root}/planning-artifacts/UX_Design.md`
- Stories always write to: `{output_root}/implementation-artifacts/stories/` (BMAD needs these locally)

## Post-Execution
After delivering the handoff artifact:
1. Summarize what was handed off and its completeness
2. Flag any gaps that need designer or PM input
3. List any dependent stories or follow-up specs needed
4. Confirm whether Sage's pre-handoff QA has been run
5. Report story IDs generated and sprint assignment
6. Confirm sprint-status.yaml was updated
