# Export UX Design Specification (BMAD Compatibility)

## Purpose
Compile PDX artifacts into BMAD's expected UX_Design.md format so the dev
agent receives everything it needs in the file format it expects. This replaces
Sally's output with a richer, PDX-generated version.

## When to Use
- After a design sprint completes (all PDX phases done)
- Before kicking off BMAD dev stories
- When the dev agent or architect needs a consolidated UX spec

## Pre-flight

### 0. Load BMAD Project State (BEFORE all other checks)
- Read `_bmad-output/implementation-artifacts/sprint-status.yaml` if it exists
  - Note current sprint number
  - Note existing story count and highest story ID
  - Note which epics are active
  - Note what's TODO vs IN PROGRESS vs DONE
- **Brownfield vs Greenfield determination:**
  - IF sprint-status.yaml exists → this is BROWNFIELD. Continue from existing state. NEVER start numbering from 1. Adapt all output to fit the existing structure.
  - IF sprint-status.yaml does NOT exist → this is GREENFIELD. Start fresh but use BMAD-compatible formats.

### Artifact Source of Truth Rule
PDX artifacts in _bmad-output/guild-artifacts/ are ALWAYS the source of truth.
When BMAD documents (PRD, architecture, UX_Design.md) need design content:
- Write the FULL artifact to _bmad-output/guild-artifacts/ using PDX templates
- Write a SUMMARY in the BMAD document with key findings inline
- REFERENCE the full artifact: "See full details: _bmad-output/guild-artifacts/[filename].md"
- NEVER duplicate the full PDX artifact content inside a BMAD document
- The summary should be enough for a PM to understand; the full artifact is for designers and developers

### Read all PDX artifacts from _bmad-output/guild-artifacts/:
- personas.md
- journey-map-*.md
- user-flow-*.md
- wireframe-*.md
- state-diagram-*.md
- site-map-*.md
- interaction-map-*.md
- microcopy-*.md
- error-messages.md
- empty-states.md
- voice-tone.md
- qa-report.md
- component-specs.md
- design-tokens.json

## Output Structure

Generate `_bmad-output/planning-artifacts/UX_Design.md` with this structure:

```markdown
---
artifact: UX Design Specification
generated_by: PDX Design Framework
agents: [Nova, Kai, Echo, Sage, Relay, Lux]
status: approved
version: 1.0
created: [date]
qa_verdict: [GO/CONDITIONAL/NO-GO from Sage]
---

# UX Design Specification

## 1. Design Overview
[One paragraph summary of the design direction, key decisions, and scope]

## 2. User Personas
[Compiled from Nova's personas.md — summary table + key details]
[Include: name, archetype, primary goal, device, accessibility needs]

## 3. User Journeys
[Compiled from Nova's journey maps — key phases and pain points]
[Include emotional arc highlights and moments of truth]

## 4. Information Architecture
[From Kai's site-map — navigation structure, page hierarchy]

## 5. User Flows
[From Kai's user-flow files — Mermaid diagrams for each key flow]
[Include: entry points, exit points, decision points, error paths]

## 6. Screen Specifications
[From Kai's wireframes — for each screen:]
- Layout description
- Component inventory
- Content hierarchy
- Interaction notes
- State variations (empty, loading, error, populated, disabled)

## 7. Interaction Patterns
[From Kai's interaction maps and state diagrams]
- Triggers and responses
- State transitions
- Micro-interactions
- Keyboard/accessibility interactions

## 8. Content & Copy
[From Echo's work:]
### Voice & Tone
[Summary of voice-tone.md]

### Screen Copy
[All microcopy organized by screen]

### Error Messages
[Complete error message system from error-messages.md]

### Empty States
[All empty states from empty-states.md]

## 9. Component Specifications
[From Relay's component specs:]
For each component:
- Props and variants
- States
- Accessibility (ARIA, keyboard)
- Design token references

## 10. Design Tokens
[From Relay's design tokens:]
- Color tokens (semantic names)
- Spacing scale
- Typography scale
- Border/shadow tokens
- Motion/animation tokens

## 11. Accessibility Requirements
[Compiled from Sage's QA report + Nova's accessibility audit:]
- WCAG level target (AA/AAA)
- Key accessibility requirements per screen
- Screen reader behavior
- Keyboard navigation spec
- Color contrast requirements

## 12. Design Decisions Log
[Compiled from all agents — key decisions and rationale]
| Decision | Rationale | Agent | Artifact Reference |

## 13. Quality Gate Status
[From Sage's QA report]
- Verdict: [GO/CONDITIONAL/NO-GO]
- Conditions (if any)
- Open items

## 14. Implementation Notes
[Specific guidance for the dev agent:]
- Start with these screens first: [priority order]
- These components are shared across screens: [list]
- These states are the most complex: [list]
- Watch out for: [edge cases, tricky interactions]
```

## Compilation Rules
- PDX artifacts are the source of truth — UX_Design.md is a COMPILED SUMMARY, not a copy
- For each section, include:
  - Key findings and decisions inline (enough for a developer to work with)
  - Reference link to full artifact: "Full details: _bmad-output/guild-artifacts/[file].md"
- Personas section: include summary table + key design implications, reference full persona cards
- Journey maps: include phases + top 3 pain points + moments of truth, reference full journey maps
- Flows: include Mermaid diagrams inline (these are compact enough), reference full flow docs for edge cases
- Copy: include final copy strings inline (developers need these), reference Echo's full content docs for rationale
- Tokens: include token names and values inline (developers need these), reference full token file for descriptions
- Component specs: include props table inline, reference full spec for states/ARIA/responsive details
- NEVER exceed 2000 lines — if the summary is too long, you're including too much detail. Summarize more, link more.
- When referencing stories in UX_Design.md's Implementation Notes section, note that all stories follow BMAD's dev-story template with BDD acceptance criteria, project structure notes, and dev agent record scaffolding.

## Output Location

Output path is configurable via `kb_ux_spec_path` in module.yaml:
- Default: `_bmad-output/planning-artifacts/UX_Design.md`
- Asmar KB integration: `projects/{name}/ux-spec.md`

Check module.yaml config for the correct path. If `kb_ux_spec_path` is set,
use that path. Otherwise, use the default.

This is the same location Sally would have written to, so BMAD's dev workflow
finds it automatically.

## Post-Export
Report:
1. "UX_Design.md generated — [X] sections, [Y] lines"
2. "Compiled from [Z] PDX artifacts"
3. "Dev agent can now reference this via /dev-story"
