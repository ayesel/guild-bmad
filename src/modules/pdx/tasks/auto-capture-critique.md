# Auto-Capture Visual Critique

## Purpose
Autonomously capture screenshots of the running app and perform a visual
critique — no manual screenshots required from the designer.

## Detection: How to capture

### For React Native / Expo (iOS Simulator)
1. Check if iOS simulator is running: `xcrun simctl list devices booted`
2. Capture screenshot: `xcrun simctl io booted screenshot /tmp/pdx-capture-[timestamp].png`
3. If specific screen needed, tell user to navigate there first (or use deep link if available)
4. Read the captured image using vision

### For Web Apps (localhost / staging / production)
1. Use Playwright MCP to navigate to the URL
2. Set viewport size (start with 375x812 for mobile)
3. Capture screenshot: `await page.screenshot({ path: '/tmp/pdx-capture-[timestamp].png', fullPage: true })`
4. Analyze using vision
5. Repeat at additional viewports if responsive check requested

### For Figma
1. Use Figma MCP to get a frame screenshot
2. Analyze using vision

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
PDX artifacts in _bmad-output/pdx-artifacts/ are ALWAYS the source of truth.
When BMAD documents (PRD, architecture, UX_Design.md) need design content:
- Write the FULL artifact to _bmad-output/pdx-artifacts/ using PDX templates
- Write a SUMMARY in the BMAD document with key findings inline
- REFERENCE the full artifact: "See full details: _bmad-output/pdx-artifacts/[filename].md"
- NEVER duplicate the full PDX artifact content inside a BMAD document
- The summary should be enough for a PM to understand; the full artifact is for designers and developers

## Capture Modes

### Single Screen Critique
Capture one screen at the current viewport. Analyze and return top 3 fixes.

```
User: "critique the packing screen"

Agent:
1. Capture screenshot from simulator/browser
2. Analyze visual hierarchy, spacing, noise, typography, color
3. Return top 3 fixes with code
```

### Multi-Viewport Scan
Capture the same screen at 3-5 viewports. Identify responsive issues.

```
User: "check the packing screen across breakpoints"

Agent:
1. Capture at 375px (iPhone SE)
2. Capture at 390px (iPhone 15)
3. Capture at 768px (iPad)
4. Capture at 1440px (desktop — if web)
5. Compare layouts across captures
6. Identify: truncation, overflow, spacing breaks, touch target issues
7. Return responsive-specific fixes
```

### Before/After Comparison
Capture current state, apply a fix, capture again, show comparison.

```
User: "fix the spacing on the packing items and show me before/after"

Agent:
1. Capture BEFORE screenshot
2. Identify the file(s) to modify
3. Apply the spacing fix to the code
4. Wait for hot reload / rebuild
5. Capture AFTER screenshot
6. Present both with annotations:
   "BEFORE: items had 14px gap, inconsistent with 8px scale"
   "AFTER: items at 12px gap, aligned to spacing scale"
7. Ask: "Keep this change or revert?"
```

### Screen Recording Analysis (Advanced)
For animation and transition review.

```
User: "watch the packing swipe-to-delete animation"

Agent:
1. Start screen recording (xcrun simctl io booted recordVideo)
2. Tell user to perform the interaction
3. Stop recording
4. Analyze key frames for: timing, easing, visual feedback, state transitions
5. Suggest animation improvements
```

## Output Format

Same as visual-critique.md — keep it SHORT:

```
**Screen: [name]** (captured at [viewport])

[Embedded screenshot or reference to saved file]

Your goal: [restate what they told you]

**Fix 1 (highest impact): [issue name]**
[1-2 sentence description + what I see in the screenshot]
```[code fix]```

**Fix 2: [issue name]**
[1-2 sentence description]
```[code fix]```

**Fix 3: [issue name]**
[1-2 sentence description]
```[code fix]```

Apply these fixes? I'll capture a before/after to verify.
```

## Screenshot Storage
Save all captures to: `_bmad-output/pdx-artifacts/captures/`
Naming: `[screen-name]-[viewport]-[timestamp].png`
Keep the last 10 captures. Clean up older ones.

## Error Handling
- If no simulator running: "No iOS simulator detected. Start your app in the simulator, or give me a URL to capture via Playwright."
- If no Playwright MCP: "Playwright MCP isn't connected. Upload a screenshot instead and I'll critique it."
- If screen is loading/transitioning: Wait 2 seconds and retry. If still loading, capture anyway and note "screen appears to be in loading state."
