# Fix Visual Hierarchy

## Purpose
Restructure the visual hierarchy of a screen so the user's eye goes to
the right place in the right order.

## Pre-flight Checks

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
- Read `_bmad-output/guild-artifacts/design-tokens.json` if it exists

## Process
1. Identify current reading order (what does the eye see first, second, third?)
2. Ask: "What SHOULD the user see first on this screen?"
3. Map desired hierarchy: Primary (one thing) → Secondary (2-3 things) → Tertiary (everything else)
4. Provide fixes to achieve that hierarchy

## Hierarchy Tools (in order of power)
1. **Size** — bigger = more important
2. **Weight** — bolder = more important
3. **Color** — saturated/contrasting = more important, muted = less important
4. **Position** — top/center = more important, bottom/edges = less important
5. **Whitespace** — more space around it = more important
6. **Detail** — simpler elements recede, detailed elements attract

## Output
Provide a hierarchy map and the fixes:
```
Current hierarchy:
1st: [what eye sees first now]
2nd: [second]
3rd: [third]

Desired hierarchy:
1st: [what should be first]
2nd: [second]
3rd: [third]

Fixes:
[specific code changes to achieve desired hierarchy]
```

## Output Location
Save to: `_bmad-output/guild-artifacts/fix-hierarchy-[scope].md`
