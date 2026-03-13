# Generate Fix

## Purpose
Generate a specific CSS/React Native style fix and apply it directly.
This is the "just fix it" command — minimal conversation, maximum action.

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
1. User describes or shows what needs fixing
2. Read the component file
3. Generate the fix
4. Show the diff
5. Ask: "Apply this?" — if yes, write the file

## Output Format
Show as a clean diff:
```diff
// [filename]
- paddingHorizontal: 14,
+ paddingHorizontal: 16,

- fontSize: 13,
- fontWeight: '600',
+ fontSize: 12,
+ fontWeight: '400',
+ color: theme.colors.textSecondary,
```
Apply? (y/n)
