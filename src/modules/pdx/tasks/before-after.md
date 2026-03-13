# Before/After Comparison

## Purpose
Show a visual before/after comparison of a proposed fix.
Helps the designer see the impact before committing.

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

## Process
1. Capture current state (screenshot or code render)
2. Apply proposed fixes temporarily
3. Capture after state
4. Present side by side with annotations

## For React Native / Expo
Use the simulator to capture before/after screenshots.

## For Web
Use Playwright to capture before/after screenshots.

## Output
Present with clear annotations:
```
BEFORE:
[screenshot or description]
Issues: [list what's wrong]

AFTER:
[screenshot or description with fixes applied]
Changes: [list what changed and why]
```

## Output Location
Save to: `_bmad-output/pdx-artifacts/before-after-[scope].md`
