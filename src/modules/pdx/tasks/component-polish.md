# Component Polish

## Purpose
Take a specific component and simplify/refine it. Remove visual noise,
clarify hierarchy, tighten spacing.

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

## Input
User points to a component — by screenshot, file path, or description.

## Process
1. Read the component code (if file path given)
2. Identify what the component is trying to communicate
3. Ask: "What's the most important thing this component should convey?"
4. Provide a polished version with specific changes

## Polish Checklist
For each component, check:
- [ ] Can any visual element be removed without losing meaning?
- [ ] Is there redundant information (icon + color + text all saying the same thing)?
- [ ] Is the spacing on the scale (4, 8, 12, 16, 24, 32, 48)?
- [ ] Is the touch target at least 44x44?
- [ ] Does the component have too many visual weights competing?
- [ ] Is the border/background earning its place or just adding noise?

## Output
Provide the polished component code with comments explaining each change.

## Output Location
Save to: `_bmad-output/pdx-artifacts/component-polish-[component-name].md`
