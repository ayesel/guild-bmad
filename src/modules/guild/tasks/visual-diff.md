# Visual Diff

## Purpose
Compare two states of a screen and highlight what changed.
Used for: before/after fixes, design review of code changes,
regression checking after updates.

## Pre-flight

### 0. Load BMAD Project State (BEFORE all other checks)
- Read `{output_root}/implementation-artifacts/sprint-status.yaml` if it exists
  - Note current sprint number
  - Note existing story count and highest story ID
  - Note which epics are active
  - Note what's TODO vs IN PROGRESS vs DONE
- **Brownfield vs Greenfield determination:**
  - IF sprint-status.yaml exists → this is BROWNFIELD. Continue from existing state. NEVER start numbering from 1. Adapt all output to fit the existing structure.
  - IF sprint-status.yaml does NOT exist → this is GREENFIELD. Start fresh but use BMAD-compatible formats.

### Artifact Source of Truth Rule
Guild artifacts in {output_root}/guild-artifacts/ are ALWAYS the source of truth.
When BMAD documents (PRD, architecture, UX_Design.md) need design content:
- Write the FULL artifact to {output_root}/guild-artifacts/ using Guild templates
- Write a SUMMARY in the BMAD document with key findings inline
- REFERENCE the full artifact: "See full details: {output_root}/guild-artifacts/[filename].md"
- NEVER duplicate the full Guild artifact content inside a BMAD document
- The summary should be enough for a PM to understand; the full artifact is for designers and developers

## Modes

### Before/After Fix
1. Capture current state
2. Apply code change
3. Wait for reload (2-3 seconds for hot reload)
4. Capture new state
5. Compare and annotate differences

### PR Review
1. Capture current main branch state
2. Checkout PR branch
3. Capture PR state
4. Compare and flag visual changes (intentional or regression)

### Design vs Implementation
1. Get design from Figma MCP (screenshot of frame)
2. Capture implementation from simulator/browser
3. Overlay and identify deviations:
   - Spacing differences (in pixels)
   - Color differences (hex values)
   - Typography differences (size, weight)
   - Missing elements
   - Extra elements not in design

## Comparison Output
```
Visual Diff: [Screen Name]

Changes detected: [count]

1. [Element] — spacing changed from 14px to 16px ✅ (matches design)
2. [Element] — color is #6B7280, design shows #6C757D ⚠️ (close but not exact)
3. [Element] — missing bottom border that exists in design ❌

Overall fidelity: 94%

[Code fixes for discrepancies]
```

## Storage
Save diff captures to: `{output_root}/guild-artifacts/captures/diff/`
Save as: `[screen]-before.png`, `[screen]-after.png`, `[screen]-diff-annotated.png`
