# Tinker — Atomize

## Purpose
Take a flat (non-atomic) Figma component and decompose it into atomic structure: extract the smallest reusable units into their own components, then recompose the original from instances.

## Pre-flight Checks

### 0. Load Project State
- Identify which file/page contains the component to atomize
- Confirm the architectural plan (typically from a previous Tinker — Architect task)

### 1. Verify knowledge base loaded
- `component-architecture-reference.md`
- `plugin-api-reference.md` (createComponentFromNode, combineAsVariants gotchas)

## Input
User points to a flat component that has internal structure that should be extracted. Examples:
- "Atomize Contracts/Table — extract Cell and Row components"
- "Atomize the Modal — extract Modal Footer as a separate component"

## Process

### Step 1 — Identify the atoms
List the structural units inside the flat component that:
- Repeat (used multiple times within the same component)
- Could be reused in other contexts (a Cell could appear in any table)
- Have their own variants worth defining (Cell has Type=Text/Bold/Number/...)

Each repeating + reusable unit is a candidate atom.

### Step 2 — Plan the extraction
For each atom:
1. Decide the atom's variant axes (refer to architectural plan)
2. Decide the atom's name in the hierarchy (e.g., `Table / Cell`)
3. Decide what variant axes the parent (now a composer of atoms) needs

### Step 3 — Build the atom components
For each atom:
1. Find one instance of the unit inside the flat component
2. Clone it to the page (`node.clone()`, then `page.appendChild(clone)`)
3. Convert to component (`figma.createComponentFromNode(clone)`)
4. Rename to `Domain / AtomName`
5. If the atom needs variants, build the other variants the same way and combine them via `figma.combineAsVariants([components], page)`

**Important**: `createComponentFromNode` fails on nodes inside variant components. Always clone to the page first, then convert.

### Step 4 — Replace inline units with atom instances in the parent
Inside the original (flat) component, find each occurrence of the inline unit and replace it with an instance of the new atom:

```javascript
const atomComp = figma.getNodeById('atom-id');
for (const inlineUnit of inlineUnits) {
  const inst = atomComp.createInstance();
  // Insert at the same position in parent
  const parent = inlineUnit.parent;
  const idx = parent.children.indexOf(inlineUnit);
  parent.insertChild(idx, inst);
  // Apply same sizing
  if (inlineUnit.layoutSizingHorizontal === 'FILL') {
    inst.layoutSizingHorizontal = 'FILL';
  } else {
    inst.resize(inlineUnit.width, inlineUnit.height);
  }
  // Migrate text content via instance overrides
  const oldText = inlineUnit.findOne(n => n.type === 'TEXT');
  const newText = inst.findOne(n => n.type === 'TEXT');
  if (oldText && newText) newText.characters = oldText.characters;
  // Remove original
  inlineUnit.remove();
}
```

### Step 5 — Audit alignment
After replacement, run the alignment audit (see `tinker-audit.md`). The flat component is now an organism composing atoms — verify cells/children align correctly.

### Step 6 — Visual verification
Take a screenshot before and after. The visual output should be identical — atomization changes the underlying structure, not the rendering.

### Step 7 — Update existing instances
Existing instances of the original component should still work (their content was preserved via instance overrides). Verify each one.

## Output
Report:
1. List of atoms created (name, ID, variant axes)
2. Confirmation original component now composes atom instances
3. Visual verification screenshots (before/after)
4. Any caveats (e.g., "Stack cell type identified but not extracted — recommend separate task")

## Output Location
Save to: `{output_root}/guild-artifacts/atomize-[component-name].md`

## Hard rules
- DO NOT atomize prematurely. If a unit appears in only one context, leave it inline. Atomize only when reuse is real.
- DO NOT touch existing instances of the parent component beyond what's required for the refactor
- If an atom you're extracting already exists in the file (under a similar name), use it instead of creating a duplicate
- Visual output before == visual output after. Any drift is a bug.
