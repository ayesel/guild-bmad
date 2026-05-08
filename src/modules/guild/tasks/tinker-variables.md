# Tinker — Variables

## Purpose
Bind a Figma component's fills and strokes to Semantic variables. Strip paint styles. Verify every color in the component is variable-bound.

## Pre-flight Checks

### 0. Load Project State
- Confirm the file has Primitive + Semantic variable collections
- Identify the target component

### 1. Verify knowledge base loaded
- `variables-and-tokens-reference.md`

## Input
User points to a component or component set, optionally specifying which variables to use:
- "Bind Card to Surface/Card and Border/Soft"
- "Strip paint styles from Button and rebind to Semantic variables"
- "Convert all fills in Modal to variable bindings"

## Process

### Step 1 — Get the variables
```javascript
const collections = figma.variables.getLocalVariableCollections();
const semantic = collections.find(c => c.name === 'Semantic');
const v = (name) => semantic.variableIds
  .map(id => figma.variables.getVariableById(id))
  .find(x => x.name === name);

const surfaceCard = v('Surface/Card');
const borderSoft  = v('Border/Soft');
const inkBody     = v('Ink/Body');
// ... etc
```

If a needed variable doesn't exist in the Semantic collection, **stop**. Adding a variable is an architectural decision — discuss with the user before proceeding.

### Step 2 — Walk the component
For every descendant node with a fill or stroke:
1. Determine which Semantic variable it should bind to (based on what the node is — body text, card background, divider, etc.)
2. Bind it via `setBoundVariableForPaint`
3. Strip any paint style (`fillStyleId`, `strokeStyleId`)

```javascript
function bindFill(node, variable) {
  const base = node.fills?.[0]?.type === 'SOLID'
    ? node.fills[0]
    : { type: 'SOLID', color: { r: 1, g: 1, b: 1 } };
  // Strip paint style first if present
  if ('fillStyleId' in node && node.fillStyleId) {
    node.fillStyleId = '';
  }
  node.fills = [figma.variables.setBoundVariableForPaint(base, 'color', variable)];
}

function bindStroke(node, variable) {
  const base = node.strokes?.[0]?.type === 'SOLID'
    ? node.strokes[0]
    : { type: 'SOLID', color: { r: 0, g: 0, b: 0 } };
  if ('strokeStyleId' in node && node.strokeStyleId) {
    node.strokeStyleId = '';
  }
  node.strokes = [figma.variables.setBoundVariableForPaint(base, 'color', variable)];
}
```

### Step 3 — Default mapping rules
If the user doesn't specify variable choices, use these defaults based on node role:

| Node role | Variable |
|---|---|
| Card / row background (raised surface) | `Surface/Card` |
| Page / panel background | `Surface/Base` |
| Recessed sub-section background | `Surface/Nested` |
| Divider / subtle border | `Border/Soft` |
| Visible border | `Border/Default` |
| Body text | `Ink/Body` |
| Muted / secondary text | `Ink/Muted` |
| Headings / strong text | `Ink/Primary` |
| Text on brand surface | `Ink/OnBrand` |
| Status tag fg/bg | `Status/{Type}Fg` / `Status/{Type}Bg` |

These are example names — adjust to your project's actual Semantic namespace.

### Step 4 — Effect (shadow) bindings
Shadows can also bind their color:
```javascript
const shadowVar = v('Shadow/Drawer Inset');
const baseShadow = {
  type: 'INNER_SHADOW',
  color: { r: 0, g: 0, b: 0, a: 0.05 },
  offset: { x: 0, y: 6 }, radius: 28, spread: 0,
  visible: true, blendMode: 'NORMAL',
};
const bound = figma.variables.setBoundVariableForEffect(baseShadow, 'color', shadowVar);
node.effects = [bound];
```

### Step 5 — Verify
Walk descendants again, confirm:
- Every fill has `boundVariables.color` set
- Every stroke (if present) has `boundVariables.color` set
- No `fillStyleId` or `strokeStyleId` on non-text nodes (text styles are fine)

```javascript
const all = component.findAll(n => true);
const issues = [];
for (const n of all) {
  if ('fillStyleId' in n && n.fillStyleId && n.type !== 'TEXT') {
    issues.push(`${n.name}: paint style still on fill`);
  }
  if ('strokeStyleId' in n && n.strokeStyleId) {
    issues.push(`${n.name}: paint style still on stroke`);
  }
}
```

### Step 6 — Visual verification
Screenshot before and after. The visual output should be identical IF the paint style and the variable have matching colors. If they differ:
- The visual change is the paint style → variable shift, which may be intentional (paint style was wrong, variable is right)
- Or the wrong variable was picked — re-do step 2 with the correct variable

## Output
Report:
1. Variables used (with paths)
2. Count of fills/strokes converted from paint styles → variables
3. Count of unbound colors fixed
4. Visual verification (before/after screenshots)
5. Any nodes that couldn't be bound (e.g., needed a variable that doesn't exist)

## Output Location
Save to: `{output_root}/guild-artifacts/variables-bind-[component-name]-[YYYY-MM-DD].md`

## Hard rules
- NEVER use paint styles for color
- ALWAYS bind through Semantic, not directly to Primitive (Semantic exists for Primitive to alias)
- If a variable doesn't exist for a needed binding, STOP and ask before adding it (architectural decision)
- After binding, audit (Tinker — Audit) to confirm zero paint styles remain
