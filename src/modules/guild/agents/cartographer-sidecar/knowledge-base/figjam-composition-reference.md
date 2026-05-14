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
