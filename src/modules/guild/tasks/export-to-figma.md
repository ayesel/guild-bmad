# Export to Figma

## Purpose
Push Guild design artifacts directly into Figma as native, editable elements — not screenshots.
Uses Figma's Plugin API via Playwright to create real frames, text layers, auto-layout,
components, and styles.

## Pre-flight Checks

### 0. Load BMAD Project State (BEFORE all other checks)
- Read `{output_root}/implementation-artifacts/sprint-status.yaml` if it exists
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
Guild artifacts in {output_root}/guild-artifacts/ are ALWAYS the source of truth.
When BMAD documents (PRD, architecture, UX_Design.md) need design content:
- Write the FULL artifact to {output_root}/guild-artifacts/ using Guild templates
- Write a SUMMARY in the BMAD document with key findings inline
- REFERENCE the full artifact: "See full details: {output_root}/guild-artifacts/[filename].md"
- NEVER duplicate the full Guild artifact content inside a BMAD document
- The summary should be enough for a PM to understand; the full artifact is for designers and developers

### 1. Prerequisites Check
Before exporting, verify:
1. Figma Desktop is open with a target file
2. Playwright MCP is available
3. The source artifact exists in {output_root}/guild-artifacts/

If any prerequisite fails, tell the user what's missing and how to fix it.

## Execution Modes

### Mode: Healer Handoff Spec → Figma
Creates an annotated handoff frame in Figma with:
- Screen frame with proper dimensions (375x812 for mobile, 1440x900 for desktop)
- Component annotations as sticky-note-style frames positioned next to elements
- Spacing callouts (red lines with pixel values)
- Color/token callouts (labeled swatches)
- Typography specs (font, size, weight, line-height)
- State documentation (tabs or adjacent frames showing all states)
- Developer notes as text blocks below the frame

Figma structure:
```
📦 Handoff — [Feature Name]
├── 📱 Screen — [Screen Name]
│   ├── [Component frames with auto-layout]
│   └── [Content layers]
├── 📝 Annotations
│   ├── Spacing callouts
│   ├── Color tokens
│   └── Typography specs
├── 🔄 States
│   ├── Empty State
│   ├── Loading State
│   ├── Error State
│   └── Populated State
└── 📋 Dev Notes
    ├── Acceptance Criteria
    ├── Edge Cases
    └── API Requirements
```

### Mode: Rogue Flow → Figma
Creates a visual flow diagram in Figma with:
- Rounded rectangle nodes for start/end (green/red fills)
- Rectangle nodes for actions (white fill, dark border)
- Diamond shapes for decision points (yellow fill)
- Connector lines between nodes (with arrows)
- Labels on all connectors
- Auto-layout frames grouping related nodes
- Color-coded error paths (red) and success paths (green)

### Mode: Sage QA Annotations → Figma
Overlays QA findings on existing Figma frames:
- Red annotation markers on issue locations
- Severity badges (P0 red, P1 orange, P2 yellow, P3 blue)
- Issue description in sticky-note frames
- Checkmark overlays on passing elements

### Mode: Warlock Copy → Figma
Updates text layers in existing Figma frames:
- Finds text layers by name or content match
- Updates with approved copy
- Creates annotation frames for copy that needs new layers
- Adds character count and reading level notes

## Figma Plugin API Execution Pattern

All Figma operations use this pattern via Playwright:

```javascript
// Execute in Figma's browser context via Playwright
await page.evaluate(async () => {
  // Access the Figma Plugin API
  const page = figma.currentPage;

  // Create a frame with auto-layout
  const frame = figma.createFrame();
  frame.name = "Guild — [Artifact Name]";
  frame.layoutMode = 'VERTICAL';
  frame.primaryAxisSizingMode = 'AUTO';
  frame.counterAxisSizingMode = 'FIXED';
  frame.resize(375, 0);
  frame.paddingLeft = 24;
  frame.paddingRight = 24;
  frame.paddingTop = 24;
  frame.paddingBottom = 24;
  frame.itemSpacing = 16;
  frame.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];

  // Add text
  const text = figma.createText();
  await figma.loadFontAsync({ family: "Inter", style: "Regular" });
  text.characters = "Component Name";
  text.fontSize = 16;
  text.fills = [{ type: 'SOLID', color: { r: 0.1, g: 0.1, b: 0.1 } }];
  frame.appendChild(text);

  // Add annotation frame
  const annotation = figma.createFrame();
  annotation.name = "Annotation — Spacing";
  annotation.layoutMode = 'HORIZONTAL';
  annotation.primaryAxisSizingMode = 'AUTO';
  annotation.counterAxisSizingMode = 'AUTO';
  annotation.paddingLeft = 8;
  annotation.paddingRight = 8;
  annotation.paddingTop = 4;
  annotation.paddingBottom = 4;
  annotation.cornerRadius = 4;
  annotation.fills = [{ type: 'SOLID', color: { r: 1, g: 0.92, b: 0.23 } }];

  const annotationText = figma.createText();
  await figma.loadFontAsync({ family: "Inter", style: "Medium" });
  annotationText.characters = "padding: 24px";
  annotationText.fontSize = 11;
  annotation.appendChild(annotationText);

  // Position annotation next to the frame
  annotation.x = frame.x + frame.width + 20;
  annotation.y = frame.y;

  // Select the created elements
  figma.currentPage.selection = [frame];
  figma.viewport.scrollAndZoomIntoView([frame]);
});
```

## Color Palette for Guild .igma Elements

Use consistent colors across all Guild-generated Figma elements:
- Guild .rame background: #FFFFFF (white)
- Annotation background: #FFF3CD (warm yellow)
- Error/P0 annotations: #F8D7DA (light red)
- Success indicators: #D4EDDA (light green)
- Info annotations: #D1ECF1 (light blue)
- Spacing callout lines: #FF0000 (red)
- Section headers: #2C3E50 (dark blue-gray)
- Body text: #1A1A1A (near black)
- Secondary text: #6C757D (gray)
- Token labels: #6F42C1 (purple)

## Font Loading
ALWAYS load fonts before setting characters:
```javascript
await figma.loadFontAsync({ family: "Inter", style: "Regular" });
await figma.loadFontAsync({ family: "Inter", style: "Medium" });
await figma.loadFontAsync({ family: "Inter", style: "Bold" });
```

## Naming Convention
All Guild-created elements use this naming pattern:
- Top-level: "Guild — [Agent] — [Artifact Type] — [Feature Name]"
- Sections: "[Section Type] — [Label]"
- Annotations: "Annotation — [Type] — [Target]"

## Output
After creating elements, report:
1. What was created (frame count, layer count)
2. Where it is in the Figma file (page, coordinates)
3. Link to the Figma file
4. Any elements that couldn't be created and why

## Post-Export
Save a log to {output_root}/guild-artifacts/figma-export-log-[date].md documenting
what was pushed to Figma, when, and the file URL.
