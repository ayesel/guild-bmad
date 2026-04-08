# Fix Typography

## Purpose
Establish a clear typography hierarchy with minimal sizes and weights.

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

## Typography Rules
- MAX 3 font sizes per screen: primary (16-18px), secondary (14px), tertiary (12px)
- MAX 2 font weights: medium/semibold for emphasis, regular for body
- Line height: 1.4-1.6 for body, 1.2-1.3 for headings
- Letter spacing: 0 for body, slight tracking for ALL CAPS labels
- Muted text: use opacity or secondary color, not a lighter font weight

## Process
1. Inventory every text style on screen
2. Identify: too many sizes? Too many weights? Inconsistent line heights?
3. Map to a 3-tier system and provide fixes

## Output
```
Current text styles (too many):
[list current styles]

Simplified to 3 tiers:
- Primary: 16px medium — [what uses it]
- Secondary: 14px regular — [what uses it]
- Tertiary: 12px regular, secondary color — [what uses it]

[specific code fixes for each text element]
```

## Output Location
Save to: `_bmad-output/guild-artifacts/fix-typography-[scope].md`
