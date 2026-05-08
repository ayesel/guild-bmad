# Variables & Design Tokens Reference

Variables are the source of truth for color in Figma. Paint styles are legacy and should not be used for color in any modern component system.

---

## Variables vs paint styles vs hex

| | When to use | API |
|---|---|---|
| **Variable** (Semantic collection alias to Primitive) | Always for color | `figma.variables.setBoundVariableForPaint(paint, 'color', variable)` |
| **Paint style** | Never for color — only legacy systems | `node.fillStyleId = 'S:abc...'` |
| **Hardcoded hex** | Never in production components | `node.fills = [{ type: 'SOLID', color: { r:1, g:0, b:0 } }]` |

**The rule**: every fill, every stroke, every text fill must be bound to a variable. Audit before declaring done:

```javascript
const all = component.findAll(n => true);
for (const n of all) {
  if ('fillStyleId' in n && n.fillStyleId && n.type !== 'TEXT') {
    issues.push(`${n.name}: paint style on fill`);
  }
  if ('strokeStyleId' in n && n.strokeStyleId) {
    issues.push(`${n.name}: paint style on stroke`);
  }
  // Text styles (textStyleId) are fine — those are typography, not color
}
```

---

## The two-collection model

Modern Figma variable systems use two collections:

### Primitive collection
Raw color values. Named by hue + scale. Typically a hue family with a numeric ramp (e.g., 50, 100, 200 … 900). One example shape:

```
Primitive /
├── <Hue A> / 50, 100, 200, 300, 400, 500, 600, 700, 900
├── <Hue B> / 50, 100, 200, 300, 500, 600, 700, 900
├── <Status hues> / 100, 500, 700, 800
├── White
└── Shadow / Inset
```

The exact hues, ramp granularity, and naming are project-specific. Some systems use Tailwind palette names directly; others use brand-specific hue names. What matters is that primitives stay raw — they describe appearance, not usage.

### Semantic collection
Aliases to Primitive. Named by **usage**, not appearance. Below is **one example** of how a Semantic collection might be organized — your project's skill or design system docs may use different group names, different leaf nodes, or a different depth.

```
Semantic /                              # EXAMPLE — not prescriptive
├── Surface /
│   ├── Base       → <neutral 50>       (page background)
│   ├── Card       → White              (raised card surfaces)
│   ├── Warm       → <accent 200>       (highlight surface)
│   └── Nested     → <neutral 50>       (recessed sub-section bg)
├── Border /
│   ├── Soft       → <neutral 200>      (dividers, subtle borders)
│   ├── Default    → <neutral 300>      (visible borders)
│   └── Strong     → <neutral 400>      (emphasis borders)
├── Ink /
│   ├── Primary    → <neutral 900>      (headings, prominent text)
│   ├── Body       → <neutral 700>      (body text)
│   ├── Secondary  → <neutral 600>      (secondary text)
│   ├── Muted      → <neutral 500>      (captions, helper text)
│   └── OnBrand    → White              (text on brand-colored surfaces)
├── Brand /
│   ├── Primary       → <brand 500>     (primary buttons, links)
│   ├── PrimaryHover  → <brand 600>
│   ├── PrimarySoft   → <brand 50>
│   └── Secondary     → <accent 500>
├── Status /
│   ├── OkFg       → <green 700>        ⚠️ usually NOT 500 — see WCAG ref
│   ├── OkBg       → <green 100>
│   ├── WarnFg     → <amber 700>
│   ├── WarnBg     → <amber 100>
│   ├── DangerFg   → <red 700>
│   ├── DangerBg   → <red 100>
│   ├── InfoFg     → <blue 700>
│   ├── InfoBg     → <blue 100>
│   ├── NeutralFg  → <neutral 600>
│   └── NeutralBg  → <neutral 100>
├── Chart /
│   ├── 1, 2, 3, 4, 5
│   └── Grid
└── Shadow /
    └── <Inset/Drop variants>
```

> **Note**: The namespace above is one valid way to organize a Semantic collection. Project-specific skills (or your team's existing design system) may use different group names — e.g., `bg/`, `text/`, `fg/`, `accent/` — different depth, or domain-specific groupings (e.g., `Form/`, `Nav/`). The two-collection split (Primitive + Semantic) and the **alias-by-usage** principle are what matter, not the exact leaf names.

**Why two layers**: components bind to Semantic. If you need to change "Body text is too dark," you change `Ink/Body` from `<neutral 700>` to `<neutral 600>` once and every component updates. If components bound directly to a primitive, you'd have to chase down every reference.

---

## Component binding pattern

```javascript
// 1. Get the variable
const collections = figma.variables.getLocalVariableCollections();
const semanticCol = collections.find(c => c.name === 'Semantic');
const v = (name) => semanticCol.variableIds
  .map(id => figma.variables.getVariableById(id))
  .find(x => x.name === name);

const surfaceCard = v('Surface/Card');
const inkBody    = v('Ink/Body');

// 2. Bind it via setBoundVariableForPaint
function bindFill(node, variable) {
  const base = node.fills?.[0]?.type === 'SOLID'
    ? node.fills[0]
    : { type: 'SOLID', color: { r: 1, g: 1, b: 1 } };
  node.fills = [figma.variables.setBoundVariableForPaint(base, 'color', variable)];
}

bindFill(cardFrame, surfaceCard);
bindFill(textNode, inkBody);

// 3. Same for strokes
function bindStroke(node, variable) {
  const base = node.strokes?.[0]?.type === 'SOLID'
    ? node.strokes[0]
    : { type: 'SOLID', color: { r: 0, g: 0, b: 0 } };
  node.strokes = [figma.variables.setBoundVariableForPaint(base, 'color', variable)];
}
```

To verify the binding survived:
```javascript
const fill = node.fills[0];
if (fill.boundVariables?.color) {
  const boundVar = figma.variables.getVariableById(fill.boundVariables.color.id);
  console.log(boundVar.name);  // 'Surface/Card'
}
```

---

## Effect (shadow) bindings

Shadows can also bind their color to variables:
```javascript
const baseShadow = {
  type: 'INNER_SHADOW',
  color: { r: 0, g: 0, b: 0, a: 0.05 },
  offset: { x: 0, y: 6 },
  radius: 28,
  spread: 0,
  visible: true,
  blendMode: 'NORMAL',
};

const shadowVariable = v('Shadow/Inset');
const bound = figma.variables.setBoundVariableForEffect(baseShadow, 'color', shadowVariable);
node.effects = [bound];
```

The alpha component of the color stays in the effect's `color.a` field (variables only carry hue, not alpha).

---

## Mode considerations (light/dark)

Each variable in a collection can have different values per mode (Light, Dark, etc.). When you alias `Surface/Card` to `White` in Light mode, in Dark mode it should alias to a dark surface (e.g., `<neutral 900>`).

Tinker should flag any variable that exists in only one mode if dark mode is on the roadmap. Adding a dark mode value isn't optional — if you alias once and forget the second mode, the variable will silently fall back to its single value.

---

## Code parity (Storybook / tokens)

Figma variables map cleanly to:
- **CSS custom properties** (`--surface-card`, `--ink-body`)
- **Tailwind theme** (`theme.extend.colors.surface.card`)
- **Style Dictionary tokens** (W3C DTCG format)
- **Token Studio plugin** (handles bidirectional sync)

The parity rule: **every Figma variable has a matching code token**. If they drift, designers and engineers stop speaking the same vocabulary.

For exporting from Figma → code:
1. Use Token Studio plugin or build a Plugin API script that walks variables and emits JSON
2. Run through Style Dictionary or a similar tool to generate platform-specific tokens
3. CI verifies the generated tokens match what's in source control (so Figma changes can't silently drift)

---

## Anti-patterns (don't do these)

- **Hardcoded hex in fills** — `{ type: 'SOLID', color: { r: 0.96, g: 0.97, b: 0.98 } }` with no variable. Find and replace with a Surface variable.
- **Paint styles for color** — `node.fillStyleId = 'S:abc...'`. Strip and rebind to variables.
- **Mixed binding within a component set** — variant 1 bound to `Surface/Card`, variant 2 hardcoded white. Audit fixes drift like this.
- **Tailwind values not matching local primitives** — if your local `<neutral 500>` is `#94a3b8` but Tailwind's slate-500 is `#64748b` and the file mixes both, document explicitly which palette is canonical and align the rest.
- **Binding components to Primitive instead of Semantic** — defeats the alias layer. Components should never bind directly to `<hue>/<weight>`; always go through a Semantic alias.
