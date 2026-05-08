# Tinker — Naming

## Purpose
Rename a Figma component or component set to follow the canonical `Domain / Subdomain / Piece` hierarchy and `Property=Value` variant naming. Catch and repair drift.

## Pre-flight Checks

### 0. Load Project State
- Identify the target component(s)
- Map the existing naming convention in the file (so you don't accidentally introduce inconsistency)

### 1. Verify knowledge base loaded
- `component-architecture-reference.md` (naming hierarchy)
- `variant-system-reference.md` (variant naming)

## Input
User describes the rename:
- "Rename Contracts Table → Table / Contracts / Table"
- "Fix variant names that got mangled by combineAsVariants"
- "Audit naming across the file and fix drift"

## Process

### Step 1 — Inspect current names
List the current names and identify what needs to change:

```javascript
const components = page.findAll(n =>
  n.type === 'COMPONENT' || n.type === 'COMPONENT_SET'
);
for (const c of components) {
  console.log(`${c.id}: "${c.name}"`);
  if (c.type === 'COMPONENT_SET') {
    for (const v of c.children) {
      console.log(`  variant: "${v.name}"`);
    }
  }
}
```

### Step 2 — Apply naming rules

**Component names** follow `Domain / Subdomain / Piece`:
- Atoms shared across domains: `Domain / Piece` (e.g., `Form / Field`)
- Domain-specific compositions: `Domain / Subdomain / Piece` (e.g., `Form / Login / Card`)
- Use `/` with single spaces around it: ` / ` (consistent across the system)

**Variant names** follow `Property=Value`:
- Always Property=Value, no bare values
- No slashes inside variant names (slashes break `combineAsVariants`)
- PascalCase for property names: `State`, `Sort`, `Type`, `Size`, `Status`
- PascalCase for values: `Default`, `Hover`, `Header`, `Ascending`

**Common malformations to fix:**
- `=Domain, =Subdomain, =Piece, =Default` → `State=Default` (this happens when `combineAsVariants` parses slashes as separators)
- `default | hover` → `State=Default` and `State=Hover` (each variant should have one Property=Value pair)
- `Default` (bare value) → `State=Default`
- `state=Default` (lowercase property) → `State=Default`

### Step 3 — Apply renames
```javascript
// Component name
component.name = 'Table / Contracts / Table';

// Variant names within a set
const set = figma.getNodeById(setId);
for (const variant of set.children) {
  // Detect what variant this actually is by content, then rename
  if (hasHeaderCells(variant)) variant.name = 'State=Header';
  else if (hasDrawer(variant)) variant.name = 'State=Expanded';
  else                          variant.name = 'State=Default';
}
```

### Step 4 — Verify component set health
After renames, check that the component set's `componentPropertyDefinitions` is healthy:

```javascript
const defs = set.componentPropertyDefinitions;
for (const [key, def] of Object.entries(defs)) {
  console.log(`${key}: type=${def.type}, default=${JSON.stringify(def.defaultValue)}`);
}
```

If this throws "Component set has existing errors," the variant names are still malformed — re-run Step 3.

### Step 5 — Update existing instances
After component rename, instances should auto-migrate (they reference by ID, not name). But verify:
- `mcp__figma__get_screenshot` of a few in-canvas instances
- Confirm they still render

For variant changes, instances may need their `properties` re-mapped if a property name changed:
```javascript
// If 'state' was renamed to 'State', existing instances pointing to 'state=Default' break
instance.setProperties({ 'State': 'Default' });
```

### Step 6 — Visual verification
Screenshot the component set in the assets panel (sort order should now make sense alphabetically by domain).

## Output
Report:
1. Renames applied (before → after, per component)
2. Variant renames applied
3. Property definition health check (clean or errors)
4. In-canvas instances verified
5. Any caveats (e.g., "X instance had a hardcoded state override that needed manual update")

## Output Location
Save to: `{output_root}/guild-artifacts/naming-rename-[YYYY-MM-DD].md`

## Hard rules
- ALWAYS use ` / ` (slash with single spaces) as the hierarchy separator — consistent
- NEVER put slashes inside a variant name — breaks `combineAsVariants`
- ALWAYS use `Property=Value` for variant names, never bare values
- VERIFY component set health after renames — `componentPropertyDefinitions` should not throw
- DO NOT rename existing in-canvas instances — they reference master by ID, the rename propagates through
