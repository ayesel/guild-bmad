# Responsive Scan

## Purpose
Capture the same screen at multiple viewports and identify responsive issues.

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

## Process

### For Web Apps
Use Playwright to capture at each viewport:

```javascript
const viewports = [
  { name: 'iPhone SE', width: 375, height: 667 },
  { name: 'iPhone 15', width: 393, height: 852 },
  { name: 'iPad', width: 768, height: 1024 },
  { name: 'Desktop', width: 1440, height: 900 },
];

for (const vp of viewports) {
  await page.setViewportSize({ width: vp.width, height: vp.height });
  await page.waitForTimeout(500);
  await page.screenshot({
    path: `_bmad-output/guild-artifacts/captures/${screenName}-${vp.name}.png`,
    fullPage: true
  });
}
```

### For React Native
React Native apps are typically mobile-only, so capture from:
1. iPhone SE simulator (smallest supported)
2. iPhone 15 Pro simulator (standard)
3. iPhone 15 Pro Max simulator (largest)
4. iPad simulator (if tablet is supported)

Switch simulators: `xcrun simctl boot [device-uuid]`

## Analysis Checklist
At each viewport, check:
- [ ] Text truncation (labels cut off?)
- [ ] Image scaling (distorted, cropped, or tiny?)
- [ ] Touch targets (still 44x44 minimum?)
- [ ] Spacing (does rhythm hold or collapse?)
- [ ] Navigation (does it adapt or overflow?)
- [ ] Content priority (does hierarchy shift appropriately?)
- [ ] Scrolling (does content that shouldn't scroll now scroll?)
- [ ] Orientation (landscape behavior if applicable)

## Output
Side-by-side comparison with issues flagged:

```
Responsive Scan: [Screen Name]

375px (iPhone SE):
- ⚠️ Priority label truncates to "Essent..."
- ⚠️ Add item FAB overlaps last list item

393px (iPhone 15): ✅ Clean

768px (iPad):
- ⚠️ List items don't use available width — feels sparse
- Suggestion: switch to 2-column grid at this breakpoint

[Code fixes for each issue]
```

## Screenshot Storage
Save all captures to: `_bmad-output/guild-artifacts/captures/`
Naming: `[screen-name]-[viewport]-[timestamp].png`
