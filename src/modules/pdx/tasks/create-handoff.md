# Create Handoff

## Purpose
Generate developer-ready handoff artifacts using the specified template. This task is the
core handoff engine for the PDX Design Ops agent.

## Pre-flight Checks

Before creating any handoff artifact, perform these checks in order:

### 1. Load ALL Prior PDX Artifacts
- Read `_bmad-output/planning-artifacts/project-context.md` if it exists
- Read `_bmad-output/planning-artifacts/prd.md` if it exists
- Read any flows or wireframes from Kai in `_bmad-output/pdx-artifacts/`
- Read any research or personas from Nova in `_bmad-output/pdx-artifacts/`
- Read any QA reports from Sage in `_bmad-output/pdx-artifacts/`
- Read any content from Echo in `_bmad-output/pdx-artifacts/`
- Read `_bmad-output/pdx-artifacts/design-tokens.json` if it exists

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
  artifacts from [Kai/Nova/Sage/Echo]. Sound right?"

## Execution

### Output Format
All handoff deliverables must include:

1. **Header Block** — Title, handoff type, version, date, target sprint, framework
2. **Source Artifacts** — Links to all referenced Kai/Nova/Sage/Echo artifacts
3. **Specification Content** — Per template structure
4. **Code-Ready References** — Token names, component props, ARIA attributes
5. **Acceptance Criteria** — Given/When/Then for every scenario
6. **Edge Cases** — From Kai's flows and Sage's QA reports
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
author: Relay (Design Ops)
target_sprint: "[sprint identifier]"
engineering_framework: "[React|React Native|Vue|etc.]"
source_artifacts:
  - [list all referenced PDX artifacts]
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
- [ ] Copy is final (from Echo) not placeholder
- [ ] Edge cases documented (from Kai and Sage)
- [ ] API/data requirements noted
- [ ] Dependencies identified (blocked-by / blocks)
- [ ] A developer can implement without asking a designer

## Output Location
Save to: `_bmad-output/pdx-artifacts/handoff-[type]-[scope].md`

## Post-Execution
After delivering the handoff artifact:
1. Summarize what was handed off and its completeness
2. Flag any gaps that need designer or PM input
3. List any dependent stories or follow-up specs needed
4. Confirm whether Sage's pre-handoff QA has been run
