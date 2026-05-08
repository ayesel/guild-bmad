# Component Architecture Reference

How to decompose any compound component in Figma so it scales, stays consistent with code, and survives growth.

---

## The atomic decomposition principle

A component should do exactly one job. If it has multiple responsibilities, decompose it.

**The mental model**:
- **Atom** — smallest unit, no internal composition. (e.g., a button, a form field, a single avatar)
- **Molecule** — composes atoms. Has its own state. (e.g., a form row = field + label + helper text)
- **Organism** — composes molecules. Owns its layout and data shape. (e.g., a form, a list, a card with header/body/footer)

The names "atom/molecule/organism" come from Atomic Design (Brad Frost), but you don't have to use that vocabulary. The point is: name the layers, build a component for each, compose upward.

**The rules:**
- An atom never knows about the molecule it sits in
- A molecule never knows about the organism that contains it
- Each layer's concerns stay at its layer

This separation is what makes design systems scale. Add a new state to molecules? Edit one component, every organism updates.

---

## When you should decompose

Three signs you're under-decomposed:
1. The same visual unit appears in multiple components, copy-pasted (e.g., the same status pill exists in three different places as a duplicate)
2. A small change requires editing multiple places (e.g., button radius update — scattered)
3. Designers can't reason about the component without seeing the whole thing — too many concerns in one place

Three signs you're over-decomposed:
1. Most "atoms" are used by exactly one parent component (premature abstraction)
2. The component tree is deeper than the visual hierarchy warrants
3. Designers spend more time finding components than designing screens

The rule of thumb: if a unit appears in 3+ contexts, it deserves its own component. If it's only in one place, keep it inline until a second use case appears.

---

## When to use variants vs boolean properties vs instance overrides

| Concern | Use | Example |
|---|---|---|
| Structural change (different layout, added drawer, different children) | **Variant axis** | `State=Default | Loading | Empty` |
| Visibility toggle on existing structure | **Boolean property** | `Show Icon` on a button |
| Data content (text, color, image, status) | **Instance override** | Per-instance text content |
| Themed appearance (light/dark) | **Variable mode** | Don't model theme as a variant |

**The trade-off**: variants are cleaner in the right-panel dropdown but explode combinatorially. Booleans are flexible but don't cascade through nested instances (Plugin API limit: `componentPropertyReferences` only supports `mainComponent` / `visible` / `characters`).

---

## Naming hierarchy

```
Domain / Subdomain / Piece
```

Examples for various component families:
```
# Buttons
Button / Primary
Button / Secondary
Button / Icon

# Forms
Form / Field
Form / Field Group
Form / Section

# Navigation
Nav / Top Bar
Nav / Side Panel
Nav / Breadcrumb

# Cards
Card / Header
Card / Footer
Card / Body
```

**Rules:**
- Atoms shared across domains live at the top level of their family (`Button / Primary`, not `Forms / Button / Primary`)
- Domain-specific compositions nest under their domain (`Form / Field` is a Form-domain piece, not a Button)
- The piece name comes last; never lead with it

**Variant property naming:**
- Always `Property=Value`
- Never bare values
- Never with slashes (slashes break `combineAsVariants` — it parses them as separators)

Common property names:
- `State` — interaction or display state (Default, Hover, Pressed, Disabled, Loading, Empty, Error)
- `Size` — sizing (Small, Medium, Large, XL)
- `Type` / `Variant` — kind/category (Text, Bold, Icon, Avatar, Status)
- `Status` — semantic color (Default, Info, Success, Warning, Error)
- `Sort` — sortable indicator (None, Ascending, Descending) — used for table headers, but reusable

---

## Layout: when to use FILL, FIXED, HUG

Per child of an auto-layout frame:

| Sizing | Use for | Example |
|---|---|---|
| `FILL` | Variable-length content that should absorb extra space | A name field that should grow with longer names |
| `FIXED` | Bounded content with known max width | An icon, a fixed-width status badge |
| `HUG` | Content where the parent shrinks to fit exactly | A button that wraps tightly around its label |

**The HUG trap**: HUG cells take different widths based on content. If two siblings use HUG with different content widths, sibling alignment breaks across instances. Lock to FIXED at the larger width when this matters.

**For responsiveness**: pick ONE FILL child per parent (typically the most variable content). When the parent width changes, that child absorbs the difference. Multiple FILL children split space proportionally — sometimes desired, often unequal.

---

## Header / Body / Footer composition

A common organism pattern:

```
Card (vertical auto-layout)
├── Card Header (atomic, with title + optional actions)
├── Card Body (organism's main content; usually FILL)
└── Card Footer (atomic, optional)
```

When the same composition appears across multiple organisms (Card, Modal, Section), extract the Header / Footer atoms and let each organism compose them. The organism's job is layout; the header/footer's job is its own internal arrangement.

---

## Expandable / Drawer pattern

A row or item that can expand to reveal additional content:

```
Item (variant State=Expanded)
└── (vertical auto-layout)
    ├── Item content (the visible row, looks identical to State=Default)
    └── Drawer frame (additional context, only visible in this variant)
        ├── (optional) caption / label
        └── Sub-content (often an instance of another component)
```

**Drawer styling principles:**
- No separate visual frame around the inner content (would create a "card-in-card" floating feel)
- Subtle background tint to distinguish from main rows OR no tint and use spacing alone
- Optional 1px top + bottom border to demarcate
- Caption is optional and should be small/quiet
- An icon (chevron, arrow) in the parent's action area should flip direction to signal expansion

**Don't** add inset shadow as a "depth" cue on inner content — atmospheric inset shadows on inner content read as decorative, not informational. The tint + borders communicate "nested" without the shadow theatrics.

---

## When to merge separate components into a variant set

**Symptoms that you should merge:**
- Two components with nearly identical structure but different styling/state
- You find yourself updating two places when changing layout
- Designers manually keep them in sync

**Procedure:**
1. Rename each component to ONLY the variant pair (e.g., `State=Default`, `State=Header`). No slashes — slashes confuse `combineAsVariants`.
2. Use `figma.combineAsVariants([components], page)` to merge.
3. Rename the new set to the proper hierarchy (`Domain / Subdomain / Piece`).
4. Verify each variant got the right name. If `combineAsVariants` mangles them, rename them manually.
5. Update existing instances — they should auto-migrate via Figma's instance-swap behavior, but verify each one.

**Don't** merge components that represent fundamentally different things just because they happen to share visual styling. (E.g., don't merge `Tag` and `Button` even if both are pill-shaped.)

---

## Relationship to code

Every Figma component should map to a code component (React, Vue, etc.). Every Figma variant should be reachable as a prop value in code. Every Figma variable should be a code token.

When this 1:1 holds, designers and engineers speak the same vocabulary. When it drifts, you get bugs like "Figma says Active should be green but the implementation uses Indigo."

The rule isn't "Figma drives code" or "code drives Figma" — it's "they stay in lockstep." Whoever changes their side first commits the change to source control, and the other side updates to match.
