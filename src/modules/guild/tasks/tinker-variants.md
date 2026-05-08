# Tinker — Variants

## Purpose
Add or restructure variant axes on a Figma component set. Merge separate components into a set, split a set with too many axes, or rename property axes.

## Pre-flight Checks

### 0. Load Project State
- Identify the target component or component set
- Check for existing instances on the canvas — variant changes can break instance references

### 1. Verify knowledge base loaded
- `variant-system-reference.md` (variant naming, when variants vs booleans)
- `plugin-api-reference.md` (combineAsVariants gotchas)

## Input
User describes the variant change:
- "Merge Card Light and Card Dark into one set with a Theme variant"
- "Split the Button set — too many State variants, separate Size into its own axis"
- "Rename the State axis to Display State across all sets"

## Process

### Adding a new variant axis to an existing set

1. **Plan the new axis** — name (e.g., `Theme`), values (e.g., `Light | Dark`)
2. **Calculate the total variants needed** — existing variants × new axis values. Watch for explosion.
3. For each existing variant, **clone and modify** to produce variants for each value of the new axis. E.g., if you have State=Default | Hover and you add Theme=Light | Dark, you need 4 total: State=Default & Theme=Light, State=Default & Theme=Dark, etc.
4. The component set's `componentPropertyDefinitions` will automatically include the new axis once variants matching the new format exist.

### Merging separate components into a variant set

1. **Rename each source component to ONLY its variant pair** (e.g., `State=Default`, `State=Header`). No slashes — `combineAsVariants` parses slashes as separators.
2. **Move components to the same parent** (typically the page). They must be siblings.
3. **Combine**:
```javascript
const newSet = figma.combineAsVariants([component1, component2, component3], page);
newSet.name = 'Domain / Subdomain / Piece'; // hierarchy goes on the SET name
```
4. **Verify variant names** in the new set. If `combineAsVariants` mangled them, rename manually:
```javascript
for (const v of newSet.children) {
  if (hasFooFeature(v)) v.name = 'State=Foo';
  else                  v.name = 'State=Default';
}
```
5. **Update existing instances** of the now-merged components. They should auto-migrate to the new set, but verify each one renders correctly.

### Splitting a variant set

When a set has too many axes (3+ axes producing 50+ total variants):
1. **Identify which axis to extract**. Usually the one most independent from the others.
2. **For each value of that axis**, gather the existing variants that have it
3. **Move those variants out** to become a separate component set
4. **Update existing instances** to point to the new set + their old prop values

### Renaming a variant axis

1. **Rename each variant** in the set to use the new property name (e.g., `Mode=Default` instead of `State=Default`)
2. The component set will pick up the new property name automatically
3. **Existing instances** pointing to the old property name will break — they need to be re-mapped via `setProperties()` or manually re-selected

## Verification

After any variant change:
1. **Run audit** (`tinker-audit.md`) — check naming, alignment, paint styles
2. **Take screenshots** of each variant and the set as a whole
3. **Find instances** in the file — confirm they render correctly with the new structure
4. **Check `componentPropertyDefinitions`** doesn't throw "Component set has existing errors"

## Output
Report:
1. The variant axis change made (added / merged / split / renamed)
2. Final variant inventory (names, IDs, dimensions)
3. Property definitions on the set
4. List of in-canvas instances and their state after the change
5. Visual verification screenshots

## Output Location
Save to: `{output_root}/guild-artifacts/variants-[component-name]-[YYYY-MM-DD].md`

## Hard rules
- ALWAYS rename source components to bare `Property=Value` before `combineAsVariants` — slashes break it
- ALWAYS verify variant names after merging — mangled names cause silent breakage
- DO NOT add a new axis without checking variant count math (3 axes × 5 values = 125 variants)
- For visibility toggles, use a boolean property — NOT a variant axis
- For data content (text, image), use instance overrides — NOT a variant axis
