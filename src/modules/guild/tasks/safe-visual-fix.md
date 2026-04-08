# Safe Visual Fix

## Purpose
Apply visual changes WITHOUT breaking existing functionality. Every fix
follows a strict before/after verification process.

## Process

### Step 0: Understand Before Touching
1. Read the ENTIRE file you're about to modify
2. Identify:
   - What framework/styling approach is used (StyleSheet, inline, Tailwind, styled-components)
   - What state management exists (useState, context, redux)
   - What props the component receives
   - What event handlers are attached
   - What conditional rendering exists
3. Map what you're going to change vs what you MUST NOT touch

### Step 1: Capture Before State
If the app is running:
- Screenshot the current screen (Playwright or xcrun simctl)
- Note what currently works: "button navigates to X, list renders Y items, pull to refresh works"

### Step 2: Plan the Change
Write out what you're going to change BEFORE changing it:

```
File: src/components/PackingItem.tsx
Change: Reduce padding from 16px to 12px on the container
Lines affected: 47 (style prop only)
Risk: None — style-only change, no logic affected
NOT touching: onPress handler (line 23), checkbox state (line 15), swipe actions (lines 31-42)
```

If the change affects more than styles, STOP and tell the user:
"This fix requires changing component structure, not just styles. Here's what I need to do and why: [explanation]. Want me to proceed?"

### Step 3: Make the Minimal Change
- Change ONLY the specific properties needed
- Match the existing code style (semicolons, quotes, indentation)
- Match the existing styling approach (don't switch from inline to StyleSheet)
- Don't add new imports unless absolutely required
- Don't remove any existing code unless it's the specific thing being fixed

### Step 4: Verify After Change
1. Check for syntax errors: does the file parse correctly?
2. Check for import errors: are all imports still valid?
3. Check for type errors: do all props still match?
4. If the app is running: capture a screenshot and compare
5. Verify the fix actually addressed the issue
6. Verify nothing else changed visually (compare before/after)

### Step 5: Report
```
Fix applied: [what changed]
File: [path]
Lines changed: [count]
Before: [screenshot or description]
After: [screenshot or description]
Verified: [yes/no + what was checked]
Side effects: None detected
```

## Red Flags — STOP and Ask
- The file uses a pattern you don't recognize
- The component has complex conditional rendering you might break
- The style is computed from state or props (dynamic styles)
- Multiple files need to change for one visual fix
- You need to change the JSX structure to fix a visual issue
- The component renders inside a FlatList, SectionList, or VirtualizedList (performance implications)
- There's animation code (Animated, Reanimated, LayoutAnimation) near your change
