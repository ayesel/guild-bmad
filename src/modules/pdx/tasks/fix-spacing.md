# Fix Spacing

## Purpose
Fix spacing and alignment issues to create consistent visual rhythm.

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

### 1. Load Project Context
- Read `_bmad-output/pdx-artifacts/design-tokens.json` if it exists

## Spacing Scale
Always use this scale — no arbitrary values:
- 4px — tight (icon to label)
- 8px — compact (related inline elements)
- 12px — comfortable (list item internal padding)
- 16px — standard (section padding, card padding)
- 24px — spacious (between groups)
- 32px — section breaks
- 48px — major section breaks

## Process
1. Identify spacing violations (values not on scale)
2. Identify grouping issues (related things too far apart, unrelated too close)
3. Provide a spacing map with fixes

## Output
```
Spacing issues found:

1. [Element] — currently 14px, should be 16px (standard)
   fix: marginBottom: 16

2. [Element group] — items 24px apart but they're related, should be 12px
   fix: gap: 12

3. [Sections] — only 16px between major sections, needs breathing room
   fix: marginTop: 32
```

## Output Location
Save to: `_bmad-output/pdx-artifacts/fix-spacing-[scope].md`
