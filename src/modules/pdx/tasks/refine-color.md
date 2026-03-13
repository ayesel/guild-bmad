# Refine Color

## Purpose
Clean up color usage — reduce noise, improve semantic meaning, fix contrast.

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

## Color Rules
- Every color MUST have a job (status, action, emphasis, category)
- Max 2-3 semantic colors per screen beyond neutrals
- If something is colored and doesn't need to be, make it neutral
- Status colors: red = error/critical, amber = warning, green = success, blue = info
- Never use color as the ONLY indicator — always pair with text or icon

## Process
1. Inventory every color on screen and its purpose
2. Identify colors without a clear job (noise)
3. Identify competing colors (too many saturated elements)
4. Identify contrast failures
5. Provide simplified color map

## Output
```
Color audit:

[color] on [element] — KEEP (reason)
[color] on [element] — REMOVE (redundant with [other element])

Simplified:
[description of simplified color scheme]

[specific code fix]
```

## Output Location
Save to: `_bmad-output/pdx-artifacts/refine-color-[scope].md`
