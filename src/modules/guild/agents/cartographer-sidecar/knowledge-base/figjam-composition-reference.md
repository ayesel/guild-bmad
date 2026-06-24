# FigJam Composition Reference

**Load on:** every Cartographer task (always loaded at activation)

---

## The core principle

A FigJam board is a composed communication artifact, not a dump. Every element — sticky color, connector weight, zone label, text size — carries meaning. If it doesn't carry meaning, it adds noise. When in doubt, remove it.

---

## Sticky note taxonomy

**Color = category. Always. No exceptions.**

Assign one color per semantic category before starting any board. Document the legend in a text block at the top-left of every board. Never use color for emphasis, status, or decoration — those get their own encoding system (shape, border, or badge).

Recommended starting palette (customize per project, but document it):
| Color | Common use |
|-------|-----------|
| Yellow | Default / general note |
| Blue | User needs / insights |
| Green | Opportunities / solutions |
| Red | Problems / risks / blockers |
| Purple | Decisions / ADRs |
| Pink | Questions / unknowns |
| Orange | Actions / next steps |

**If you need a 7th color, you have too many categories.** Merge or split your taxonomy.

---

## Zone and section delineation

**Zones define the reading structure of the board.** Use FigJam sections (the native Section component) for major zones. Use labeled rectangles or text headers for sub-zones within sections.

Zone conventions:
- **Section titles:** Large, bold, left-aligned within the section header. Should answer "what is this area for?"
- **Zone borders:** Use sections or rectangles with low-opacity fills and no stroke, or a single-pixel stroke. High contrast borders compete with content.
- **Zone spacing:** More whitespace between zones than within zones. The gap tells the eye where one cluster ends and another begins.
- **Zone order:** Left-to-right or top-to-bottom reading order. Most important zone top-left. Time flows left-to-right. Hierarchy flows top-to-bottom.

---

## Connector conventions

**Line weight = relationship strength or importance.**
- Heavy stroke (3px+): primary relationships, critical dependencies
- Medium stroke (2px): standard relationships
- Light stroke (1px): supporting, supplemental, or weak relationships

**Line style = relationship type.**
- Solid: direct relationship, dependency, or data flow
- Dashed: indirect relationship, optional connection, or proposed link
- Dotted: temporal or conditional relationship

**Arrowheads:**
- One arrowhead: directional relationship (A informs B)
- Two arrowheads: bidirectional (A and B inform each other)
- No arrowhead: association without direction

**Label connectors** when the relationship type is not self-evident. Keep connector labels to 1–3 words. Position them at the midpoint of the connector, not near an endpoint.

**Crossing connectors are a design problem.** If connectors cross frequently, the layout is wrong. Reorganize zones before adding more connectors.

---

## Text hierarchy on whiteboards

Five levels, used consistently across the board:

| Level | Use | Style |
|-------|-----|-------|
| **Board title** | Name of the board | 32–40px, bold |
| **Section/zone title** | Major area label | 20–24px, bold |
| **Sub-zone or group label** | Sub-area within a zone | 16px, medium weight |
| **Node label** | Sticky, shape, or element label | 14px, regular |
| **Annotation** | Supporting detail, context, source | 12px, italic or light weight |

Never mix levels for emphasis. If something feels like it needs to be bigger for emphasis, the hierarchy is wrong — fix the structure, not the font size.

---

## Visual hierarchy for explanatory artifacts

Explanatory diagrams (system maps, IA diagrams, ADR visualizations) follow different rules than product UI:

**In product UI:** visual hierarchy guides action. Primary = what to do next.
**In explanatory diagrams:** visual hierarchy guides comprehension. Primary = what to understand first.

Hierarchy encoding in explanatory diagrams (in priority order):
1. **Size** — larger = more important or more general (parent nodes bigger than child nodes)
2. **Position** — top-left = first in reading order; center = focal point
3. **Weight** — bold labels for higher-level nodes
4. **Color saturation** — more saturated = more prominent
5. **Whitespace** — more space around = higher importance

**The 'engineer-made' failure mode:** Everything the same size, same weight, same spacing. No visual hierarchy. The reader must decode the diagram rather than read it. This is what happens when IA diagrams are built by people who think in data structures, not communication.

**The 'designer-made' standard:** A first-time reader can identify the most important element, the reading order, and the primary groupings within 5 seconds — without reading any labels.

---

## Common FigJam IA mistakes

1. **Same sticky color for different categories** — destroys the color-as-category convention and forces the reader to read every label before understanding the structure
2. **No zone labels** — zones without titles look like decorative boxes; the reader cannot orient
3. **Connectors crossing everywhere** — signals layout failure; reorganize before connecting
4. **All text the same size** — no visual hierarchy; reader cannot identify what matters
5. **No legend for color** — forces the reader to reverse-engineer your encoding
6. **Overcrowded zones** — whitespace is not wasted space; it is the signal that separates clusters
7. **Scope not stated** — the reader cannot know what the diagram is trying to show vs. what it intentionally omits
8. **Labels that require context to decode** — internal acronyms, org-specific shorthand, jargon; always write for the least-informed reader in the room

---

## User-flow boards — house style (screen-mockup flows)

**Load when composing a USER FLOW / process / JTBD board in FigJam.** Rogue produces the flow logic; Cartographer renders it in THIS established house style. Match it exactly — do NOT emit plain labeled boxes, generic flowcharts, or Mermaid. A user-flow board pairs the flow spine with **real low-fi screen mockups** and trigger-labeled transitions.

### Board structure
- **One FigJam SECTION per use-case**, stacked top-to-bottom. Section name = `uc.<domain>.<n> · <short title>` (e.g. `uc.cp.01 · See my coverage`); the code shows in a pill at the section's top-left.
- **USER STORY line** at the top of each section: *"As a `<role>`, I want `<goal>`, so `<reason>`."*
- **Legend** once at the top of the board defining the node vocabulary below.
- Flow reads **left→right** (or top→down for long flows). Screen mockups sit adjacent to the node that produces them. **No crossing connectors.**

### Node vocabulary — match these shapes + RGB exactly
| Element | `shapeType` | Fill (r,g,b · 0–1) | Stroke | Size | Meaning |
|---|---|---|---|---|---|
| **Start / End** | `ROUNDED_RECTANGLE` (cornerRadius 28) | green `0.65,0.83,0.63` | gray `0.46` w4 | ~230×70 | entry / exit |
| **Action** | `PARALLELOGRAM_RIGHT` | blue `0.44,0.69,0.91` | gray `0.46` w4 | ~230×70 | a user/system action |
| **Screen (UI state)** | low-fi MOCKUP (see below); legend swatch = `SQUARE` yellow `0.99,0.92,0.63` | — | gray `0.46` w3 | ~460×430 | a real screen |
| **Decision** | `DIAMOND` | red `0.91,0.61,0.59` | gray `0.46` w4 | ~150×150 | a branch |
| **Acceptance criteria** | `SQUARE` (cornerRadius 6) | gray `0.89,0.90,0.91` | gray `0.46` w4 | ~360×160 | testable AC for the flow |
| **Connector** | `ELBOWED`, cornerRadius 24 | — | gray `0.46` w4 | — | a transition — LABEL with the trigger |
| **Annotation sticky** | `STICKY` | pink `0.97,0.74,0.83` | — | — | behavior/edge/rule note (a row beneath the flow) |
| **Author note sticky** | `STICKY` | purple | — | — | personal note / open question (signed) |

### Screens are REAL low-fi mockups, not labeled boxes
A "Screen (UI state)" is a **yellow FRAME built like the actual UI**: a blue title bar with white text (`Section › Screen`), an optional left sub-nav, white rounded **field rows** with labels, and a blue **button**. Recognizable at a glance. A plain yellow box with a screen name is WRONG and is the most common failure.

### Triggers
Triggers are the **labels on connectors** — what causes each transition (`Yes`, `No match`, `clicks a site`, `renewal < 90d`, `logs in`). Every branch out of a Decision carries its trigger. Add one pink sticky listing the flow's **entry triggers** ("enters from: renewal < 90d · email link · clicking a site").

### Acceptance criteria + sticky rows
End each flow with the gray **Acceptance Criteria** box (testable rules). Place a **row of pink stickies** beneath the flow — one idea per sticky — for behavior, edge cases, and rules.

### use_figma build recipe (FigJam)
```js
const C={green:{r:.65,g:.83,b:.63},red:{r:.91,g:.61,b:.59},blue:{r:.44,g:.69,b:.91},yellow:{r:.99,g:.92,b:.63},gray:{r:.89,g:.9,b:.91},pink:{r:.97,g:.74,b:.83},stroke:{r:.46,g:.46,b:.46}};
// node (load Inter Medium/Regular/Semi Bold first)
function shp(type,fill,w,h,x,y,txt){const s=figma.createShapeWithText();s.shapeType=type;s.fills=[{type:'SOLID',color:fill}];s.strokes=[{type:'SOLID',color:C.stroke}];s.strokeWeight=4;s.resize(w,h);s.x=x;s.y=y;s.text.fontName={family:'Inter',style:'Medium'};s.text.characters=txt;page.appendChild(s);return s;}
// connector — label IS the trigger
function conn(a,b,trigger){const c=figma.createConnector();c.connectorStart={endpointNodeId:a.id,magnet:'AUTO'};c.connectorEnd={endpointNodeId:b.id,magnet:'AUTO'};c.connectorLineType='ELBOWED';c.strokes=[{type:'SOLID',color:C.stroke}];c.strokeWeight=4;if(trigger){c.text.characters=trigger;}page.appendChild(c);return c;}
// screen mockup = yellow FRAME + blue title-bar rect + white field-row rects + blue button (createFrame/createRectangle/createText)
// wrap each flow's nodes in a SECTION named `uc.<domain>.<n> · <title>`
```
Reuse beats rebuild: when a needed screen already exists on a flow board, **clone the existing mockup** and re-text it rather than building a new one.

### Canonical reference
The Arise **"RFP-Execution · AC & User Flow"** board (`fileKey ioHvu6WStQAUA8FzAsR3vS`, page `03 · User Flows · RFP Execution`) is the canonical example — study a `uc.*` section before composing a new flow.
