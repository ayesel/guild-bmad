# Tinker — Align

## Purpose
Fix alignment issues in a Figma component set: matching cell widths across variants, locking HUG cells that drift, ensuring sibling variants in the same set share dimensions exactly.

## Pre-flight Checks

### 0. Load Project State
- Identify the target component set
- Confirm which variants should align (typically all of them)

### 1. Verify knowledge base loaded
- `component-architecture-reference.md` (HUG trap)
- `plugin-api-reference.md` (resize, layoutSizingHorizontal)

## Input
User points to a misaligned component:
- "Header and Default rows in Contracts/Row aren't aligning"
- "The Card variants are different widths"
- "Fix the column drift in Users/Row"

Or runs Tinker — Audit first and gets a report flagging alignment issues.

## Process

### Step 1 — Identify the canonical variant
The "source of truth" widths typically live in the most-used variant (usually `State=Default`). Use that variant's widths as the reference.

### Step 2 — Inspect each variant
Walk every variant in the set, list the cell widths and total:

```javascript
function findCells(node) {
  if (!('children' in node)) return [];
  const cells = node.children.filter(c => c.name?.includes('Cell'));
  if (cells.length >= 5) return cells;
  for (const c of node.children) {
    if ('children' in c) {
      const found = findCells(c);
      if (found.length >= 5) return found;
    }
  }
  return [];
}

const set = figma.getNodeById(setId);
for (const v of set.children) {
  const cells = findCells(v);
  const total = cells.reduce((s, c) => s + Math.round(c.width), 0);
  console.log(`${v.name}: ${cells.length} cells, sum=${total}, master=${Math.round(v.width)}`);
}
```

### Step 3 — Apply canonical widths to all variants
Use the reference variant's widths to update the others:

```javascript
const reference = set.children.find(v => v.name === 'State=Default');
const refCells = findCells(reference);

for (const variant of set.children) {
  if (variant === reference) continue;
  const cells = findCells(variant);
  if (cells.length !== refCells.length) {
    console.warn(`${variant.name}: different cell count — needs structural fix, not just width sync`);
    continue;
  }
  for (let i = 0; i < cells.length; i++) {
    const refCell = refCells[i];
    const cell = cells[i];
    cell.layoutSizingHorizontal = refCell.layoutSizingHorizontal;
    if (refCell.layoutSizingHorizontal === 'FIXED') {
      cell.resize(Math.round(refCell.width), cell.height);
    }
  }
  // Match variant master width
  variant.resize(Math.round(reference.width), variant.height);
}
```

### Step 4 — Handle HUG drift
If a cell is HUG and the content varies between variants (e.g., Header has text 'Supplier ↑↓' = 100px, Data has logo = 90px), HUG produces drift.

Fix by locking to FIXED at the larger width:

```javascript
// Lock cell 0 to FIXED at the largest HUG width across variants
let maxHugWidth = 0;
for (const v of set.children) {
  const cells = findCells(v);
  if (cells[0].layoutSizingHorizontal === 'HUG') {
    maxHugWidth = Math.max(maxHugWidth, Math.round(cells[0].width));
  }
}
for (const v of set.children) {
  const cells = findCells(v);
  cells[0].layoutSizingHorizontal = 'FIXED';
  cells[0].resize(maxHugWidth, cells[0].height);
}
```

### Step 5 — Handle missing cells
If one variant has fewer cells than others (e.g., Header has 8 cells, Default has 9 with a hidden action cell):
1. **If the missing cell SHOULD be present**, add it to the deficient variants. Clone from the reference variant.
2. **If the cell SHOULDN'T be present in some variants** (e.g., Action chevron only in expandable rows), keep them missing and accept the misalignment OR consider if hidden/empty cells would be cleaner.

Adding a missing cell:
```javascript
const refCell = refCells[8]; // the missing cell index
const newCell = refCell.clone();
deficientRowContent.appendChild(newCell);
// Apply the canonical width
newCell.layoutSizingHorizontal = 'FIXED';
newCell.resize(Math.round(refCell.width), newCell.height);
// Hide content if this variant shouldn't show the cell's purpose
const texts = newCell.findAll(n => n.type === 'TEXT');
for (const t of texts) t.visible = false;
```

### Step 6 — Verify
Re-run inspection. Every variant should have:
- Same cell count
- Same width per cell index
- Same total width
- Same variant master width

```javascript
function audit(set) {
  const variants = set.children.map(v => ({
    name: v.name,
    widths: findCells(v).map(c => Math.round(c.width)),
    total: findCells(v).reduce((s, c) => s + Math.round(c.width), 0),
    masterW: Math.round(v.width),
  }));
  const ref = variants[0];
  return variants.slice(1).filter(v =>
    v.total !== ref.total ||
    v.masterW !== ref.masterW ||
    v.widths.some((w, i) => w !== ref.widths[i])
  );
}
```

If `audit()` returns empty array, alignment is clean.

### Step 7 — Visual verification
Take a screenshot of the component set with all variants stacked. Visually verify column edges line up across variants.

## Output
Report:
1. Initial state (which variants drifted, by how much)
2. Fix applied (which widths were synced, which HUG cells were locked, which missing cells were added)
3. Final state (audit result — should be clean)
4. Visual verification screenshots

## Output Location
Save to: `{output_root}/guild-artifacts/align-[component-name]-[YYYY-MM-DD].md`

## Hard rules
- DO NOT change the canonical variant's widths just because they're inconvenient — fix the drifters, not the source of truth
- DO NOT add cells to variants without confirming they belong there (might be intentional structural difference)
- ALWAYS verify visually, not just by code passing
- Sibling variants in the same component set MUST share dimensions where the design intends visual lockstep
