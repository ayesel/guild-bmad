# Figma Plugin API Reference (via MCP)

The Figma Plugin API is exposed through `mcp__figma__use_figma` (executes JS against the active file). This file documents the gotchas — the things that look like they should work but don't, and the patterns that prevent re-discovering them.

---

## Required setup before any mutation

```javascript
// Load every font you'll touch BEFORE setting characters
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });
await figma.loadFontAsync({ family: 'Inter', style: 'Medium' });
await figma.loadFontAsync({ family: 'Inter', style: 'Semi Bold' });
// Inter "Semi Bold" has a SPACE — not "SemiBold". Same for "Extra Bold".
await figma.loadFontAsync({ family: 'Roboto', style: 'Medium' });
await figma.loadFontAsync({ family: 'Font Awesome 6 Free', style: 'Solid' });
```

If you skip this, `node.characters = "..."` throws: `Cannot write to node with unloaded font`.

## Setting the current page

```javascript
// ❌ Doesn't work — setter not supported
figma.currentPage = page;

// ✓ Use the async setter
await figma.setCurrentPageAsync(page);
```

## Plugin data

```javascript
// ❌ Web-plugin-only (requires a manifest plugin id)
node.getPluginData(key);
node.setPluginData(key, value);

// ✓ Use shared plugin data with a stable namespace
node.getSharedPluginData('your.namespace', key);
node.setSharedPluginData('your.namespace', key, value);
```

---

## The append-before-FILL trap

```javascript
// ❌ Throws "FILL can only be set on children of auto-layout frames"
const cell = makeCell();
cell.layoutSizingHorizontal = 'FILL';
parent.appendChild(cell);

// ✓ Append first, then size
const cell = makeCell();
parent.appendChild(cell);
cell.layoutSizingHorizontal = 'FILL';
cell.layoutSizingVertical = 'FILL';
```

This is the single most common Plugin API trap. If your script throws on a FILL line, check that the node is parented first.

## Layout sizing valid values

```javascript
// primaryAxisSizingMode (the auto-layout direction)
frame.primaryAxisSizingMode = 'FIXED'; // or 'AUTO'
frame.primaryAxisSizingMode = 'HUG';   // ❌ INVALID — throws

// counterAxisAlignItems (cross-axis alignment)
frame.counterAxisAlignItems = 'MIN' | 'CENTER' | 'MAX' | 'BASELINE';
frame.counterAxisAlignItems = 'STRETCH'; // ❌ INVALID — throws

// To make children stretch to fill cross axis:
//   parent.counterAxisAlignItems = 'MIN'
//   child.layoutSizingVertical = 'FILL'  // (when parent is HORIZONTAL)
```

## layoutSizingHorizontal/Vertical

```javascript
// Valid values: 'FIXED' | 'HUG' | 'FILL'
// Setting these is the modern way to control sizing.
// Setting raw width via .resize() implies FIXED.

cell.layoutSizingHorizontal = 'FILL';   // grow to fill parent
cell.layoutSizingHorizontal = 'HUG';    // shrink to fit content
cell.layoutSizingHorizontal = 'FIXED';
cell.resize(120, 44);                    // explicit size
```

---

## componentPropertyReferences ceiling

The Plugin API only supports binding nested-instance properties to parent component properties for **three** node properties:

```javascript
// ✓ Supported references
node.componentPropertyReferences = {
  visible: 'Show Renewal Status#44357:0',  // boolean prop on parent
  characters: 'Title Text#abc:1',          // text prop on parent
  mainComponent: 'Variant#xyz:2',          // variant prop on parent
};

// ❌ NOT supported: boolean → boolean property cascade
// You CANNOT bind a nested instance's boolean property to a parent's boolean.
// E.g., if a Row has "Show X" boolean and the Table has "Show X" boolean,
// toggling the Table boolean does NOT propagate. The user must toggle each row.
```

**Implication**: when you want a Table-level toggle that hides a column across all rows, you have three options:
1. Add a variant axis on the Table (`Show=Yes | No`) — explodes variants
2. Bind the cell's `visible` to a Table property — but the cell is inside a nested instance, so its binding points at the Row, not the Table
3. Accept per-row toggling and document it (often the right answer)

If a structural pattern can't cascade in Figma but can in code (where it's just a prop), **don't model it in Figma**.

---

## combineAsVariants name-mangling

```javascript
// ❌ Components named with slashes get parsed as multiple Property=Value pairs
// e.g. a component named "Table / Contracts / Row > State=Default" combined
// into a set produces variant names like "=Table, =Contracts, =Row, =Default"

// ✓ Before combining, rename each component to ONLY the variant pair
component1.name = 'State=Default';
component2.name = 'State=Expanded';
component3.name = 'State=Header';

const set = figma.combineAsVariants([component1, component2, component3], page);
set.name = 'Table / Contracts / Row';  // hierarchy on the SET name, not variant names
```

If you forget, the symptom is mangled variant names visible in the right panel and `componentPropertyDefinitions` throwing "Component set has existing errors". To recover:

```javascript
for (const v of set.children) {
  // Detect what each variant actually is by content, then rename
  if (hasHeaderCells(v)) v.name = 'State=Header';
  else if (hasDrawer(v))  v.name = 'State=Expanded';
  else                    v.name = 'State=Default';
}
```

---

## createComponentFromNode restrictions

```javascript
// ❌ Fails: "Cannot create component from node"
//    when the node is inside a variant (a child of a COMPONENT or COMPONENT_SET)
const clone = sourceVariantInsideSet.clone();
const comp = figma.createComponentFromNode(clone);  // throws

// ✓ Move the clone to the page first
const clone = sourceVariantInsideSet.clone();
page.appendChild(clone);  // detach from the variant context
const comp = figma.createComponentFromNode(clone);
```

## Cannot appendChild into instance children

```javascript
// ❌ Fails: "Cannot move node. New parent is an instance or is inside of an instance"
nestedRowContent.appendChild(newCell);  // nestedRowContent is inside an instance

// ✓ Modify the master component, not the instance
const masterRowContent = rowSetMaster.findOne(n => n.name === 'Row content');
masterRowContent.appendChild(newCell);  // works — propagates to all instances
```

---

## Inspection patterns

```javascript
// Get all variables for a node (recursively)
const variables = figma.variables.getLocalVariableCollections();
const semanticCol = variables.find(c => c.name === 'Semantic');
const v = (name) => semanticCol.variableIds
  .map(id => figma.variables.getVariableById(id))
  .find(x => x.name === name);
const surfaceCard = v('Surface/Card');

// Bind a fill to a variable
function bindFill(node, variable) {
  const base = node.fills?.[0]?.type === 'SOLID'
    ? node.fills[0]
    : { type: 'SOLID', color: { r: 1, g: 1, b: 1 } };
  node.fills = [figma.variables.setBoundVariableForPaint(base, 'color', variable)];
}

// Find cells regardless of nesting depth
function findCells(node) {
  if (!('children' in node)) return [];
  const cells = node.children.filter(c => c.name?.includes('Cell'));
  if (cells.length >= 5) return cells;
  for (const c of node.children) {
    const found = findCells(c);
    if (found.length >= 5) return found;
  }
  return [];
}
```

---

## Verification discipline

After any mutation, verify visually with `mcp__figma__get_screenshot`. Code that runs without throwing can still produce wrong output (mismatched widths, hidden styles, broken bindings). Plugin API errors are a low bar for correctness.

After a structural change, audit:

```javascript
// Walk all descendants, flag paint styles (color should be variable-bound)
const all = node.findAll(n => true);
const issues = [];
for (const n of all) {
  if ('fillStyleId' in n && n.fillStyleId && n.type !== 'TEXT') {
    issues.push(`${n.name}: paint style on fill instead of variable`);
  }
  if ('strokeStyleId' in n && n.strokeStyleId) {
    issues.push(`${n.name}: paint style on stroke instead of variable`);
  }
}
```
