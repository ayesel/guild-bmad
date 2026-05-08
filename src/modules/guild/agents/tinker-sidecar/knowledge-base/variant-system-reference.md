# Variant System Reference

How to design variant axes that scale and don't explode combinatorially.

---

## When to use a variant axis vs a boolean property

| Concern | Use | Why |
|---|---|---|
| Structural change (different layout, added drawer, different cells) | **Variant axis** | Each variant is a separate frame that can be edited independently |
| Visibility toggle on existing structure | **Boolean property** | Bind to `visible` field, no duplication needed |
| Data content (text, image, status tag selection) | **Instance override** | Override at the instance level — don't bake data into variants |
| Themed appearance (light/dark) | **Variable mode** | Variables already support modes; don't model theme as a variant axis |

**The trade-off**: variants give you a clean dropdown in the right panel and clear visual differentiation at the master level. Booleans are flexible and don't duplicate, but they can't cascade through nested instances (Plugin API limitation: `componentPropertyReferences` only supports `mainComponent`/`visible`/`characters`).

---

## Variant naming conventions

Always `Property=Value`. Never bare values, never with slashes (slashes break `combineAsVariants`).

**Standard property names:**
- `State` — interaction or display state (Default, Expanded, Selected, Header, Loading, Empty)
- `Size` — sizing (Small, Medium, Large)
- `Type` — kind/category (Text, Bold, Status, Number, Action, Logo)
- `Sort` — sort indicator (None, Ascending, Descending)
- `Status` — status color (Default, Info, Warning, Error, Success)
- `Variant` — fallback when nothing else fits (avoid if possible — use a more specific name)

**Standard variant values for State:**
- `Default` — the unmodified base
- `Expanded` — opened/revealed
- `Header` — column-header treatment
- `Selected` — multi-select indicator
- `Hover`, `Pressed`, `Focused` — interaction states
- `Loading`, `Empty`, `Error` — data states
- `Disabled` — non-interactive

---

## Variant explosion math

If you have `n` independent variant axes with `k` values each, you have `k^n` total variants. This grows fast:

| Axes | Values per axis | Total variants |
|---|---|---|
| 1 axis (State only) | 3 | 3 |
| 2 axes (State + Size) | 3 × 3 | 9 |
| 3 axes (State + Size + Type) | 3 × 3 × 6 | 54 |

Avoid 3+ axes if possible. Three signs you should consolidate:
1. Most combinations are nonsensical (e.g., "Empty + Hover" — empty isn't hoverable)
2. Designers complain about the sidebar dropdown being too long
3. Variants are mostly identical with minor changes that could be a boolean property

**Refactoring out of variant explosion:**
- Merge orthogonal axes into one "State" axis if they're rarely combined
- Move appearance toggles (color theme) to variable modes
- Move visibility toggles to boolean properties
- Move data content to instance overrides

---

## Boolean property patterns

```javascript
// Add a boolean property to a component set
const propKey = componentSet.addComponentProperty('Show Renewal Status', 'BOOLEAN', true);
// propKey is something like 'Show Renewal Status#abc:0'

// Bind a node's visibility to that property
node.componentPropertyReferences = { visible: propKey };
```

**Naming convention**: start with `Show ` for visibility toggles. Other patterns:
- `Show {Thing}` — visibility (e.g., Show Icon, Show Renewal Status, Show Footer)
- `Has {Thing}` — presence variant (less common; usually use Show)
- `Is {State}` — state boolean (less common; usually use a State variant)

**Avoid** booleans that gate structural changes. If toggling a boolean would change the layout dramatically (add a drawer, swap a row for a chart), use a variant axis instead.

---

## The cascade problem

```
Table Set (has property "Show X")
└── Row instances inside (each Row has property "Show X")
```

Toggling the Table's `Show X` does **not** propagate to the Row instances' `Show X`. The Plugin API doesn't support boolean→boolean references. Three workarounds:

### Workaround 1: Variant axis on the Table
Make the Table set have variants like `X=Visible | Hidden`, where each variant has Row instances with the right boolean already set. Pro: works statically. Con: variant explosion, manual to maintain.

### Workaround 2: Multi-select rows in Figma
Designers select all Row instances at once and toggle the boolean. Pro: no variant explosion. Con: requires designer awareness, easy to miss rows.

### Workaround 3: Don't model in Figma
Skip the Table-level toggle. The Row-level boolean is the source of truth. In code (Storybook/React), the toggle is just a prop that cascades trivially. Document the limitation: "Visibility toggles per row in Figma; cascades via prop in code."

For most cases, Workaround 3 is right. Figma is a tool for showing static designs; complex toggles belong in code.

---

## When to merge separate components into a variant set

**Symptoms that you should merge:**
- Two components with nearly identical structure but different styling/state (Default Row + Header Row)
- You find yourself updating two places when changing column widths
- Designers manually keep them in sync

**Procedure:**
1. Rename each component to ONLY the variant pair (e.g., `State=Default`, `State=Header`). No slashes — slashes confuse `combineAsVariants`.
2. Use `figma.combineAsVariants([components], page)` to merge.
3. Rename the new set to the proper hierarchy (`Table / Contracts / Row`).
4. Verify each variant got the right name. If `combineAsVariants` mangles them (e.g., `=Table, =Contracts, =Row, =Header`), rename them manually.
5. Update existing instances — they should auto-migrate to the new variant via Figma's instance-swap behavior, but verify each one.

**Don't** merge components that represent fundamentally different things just because they happen to share some visual styling. (E.g., don't merge `Tag` and `Button` even if both are pill-shaped.)

---

## Variant set health checks

Run these audits periodically:

1. **All variants have matching frame width** — set master width should be consistent across variants
2. **All variants have matching cell widths** — column N should be the same width in every variant of a Row set
3. **Property names follow `Property=Value`** — `componentPropertyDefinitions` should not throw
4. **No hidden orphan variants** — variants should be reachable from the set, not floating outside
5. **Boolean props bind to actual nodes** — `addComponentProperty` returns a key; that key should be referenced by at least one node's `componentPropertyReferences`
