# Tinker — Architect

## Purpose
Plan a Figma component system *before* scripting. Decide atoms, variants, naming, and variable bindings up front so the build doesn't reveal architectural mistakes mid-flight.

## Pre-flight Checks

### 0. Load Project State
- Read `{output_root}/implementation-artifacts/sprint-status.yaml` if it exists. Brownfield vs greenfield determines whether you're extending or starting fresh.
- Inspect existing Figma variable collections (`figma.variables.getLocalVariableCollections()`) — if Primitive + Semantic exist, your Semantic namespace is already established.
- Audit existing components matching the target domain. If a similar component exists, the new one should follow its hierarchy and conventions.

### 1. Verify Tinker knowledge base loaded
- `plugin-api-reference.md`, `component-architecture-reference.md`, `variables-and-tokens-reference.md`, `variant-system-reference.md`

## Input
User describes the component to build. Examples:
- "I need a Card with header/body/footer support"
- "Build a Form Field with label, input, helper text, error states"
- "Design a notification banner system"

## Process

### Step 1 — Decompose
Identify the atomic layers. Name three:
- Atom (smallest reusable unit)
- Molecule (composes atoms; owns interaction state)
- Organism (composes molecules; owns layout)

Example for a Form: `Field → FormSection → Form`. For a Card: `MetaItem → Card`.

### Step 2 — Define variant axes per layer
Per component, list the variant properties:
- `State` — what states does this component have? (Default, Hover, Pressed, Disabled, Loading, Error, Empty, ...)
- `Size` — does it have multiple sizes? (Small, Medium, Large, ...)
- `Type` / `Variant` — does it have multiple kinds? (Text, Bold, Icon, Avatar, ...)

Each axis must be orthogonal — combining values must produce a meaningful component. If two axes produce nonsense combinations, consolidate.

### Step 3 — Define booleans (visibility toggles)
Booleans for visibility on existing structure:
- `Show Icon` — hide/show an icon child
- `Show Helper Text` — hide/show optional helper text
- Naming convention: prefix with `Show ` or `Has ` (prefer `Show `)

**Plugin API limit**: booleans don't cascade through nested instances. If a boolean needs to cascade, plan to handle it at the parent variant level OR accept per-instance overrides.

### Step 4 — Naming hierarchy
Follow `Domain / Subdomain / Piece`:
- Atoms shared across domains: `Domain / Piece` (e.g., `Form / Field`)
- Domain-specific compositions: `Domain / Subdomain / Piece` (e.g., `Form / Login / Card`)

Decide on the full path for each new component before building.

### Step 5 — Variable bindings
List every fill/stroke/text color the component will have. For each, name the Semantic variable it should bind to (e.g., `Surface/Card`, `Ink/Body`, `Border/Soft`).

If a needed variable doesn't exist in the Semantic collection, **stop**. Add the variable first (which is itself an architectural decision and may need stakeholder input), then resume.

### Step 6 — Code parity check
Map each Figma variant to a code prop. If a variant has no code counterpart, ask whether code should add it OR whether the variant shouldn't exist in Figma either.

## Output
Produce a written component spec document covering:
1. **Atomic decomposition** — the three layers, what each owns
2. **Variant axes** — full property=value matrix per layer
3. **Boolean properties** — visibility toggles per layer
4. **Naming hierarchy** — full Domain / Subdomain / Piece path
5. **Variable bindings** — every color, every binding
6. **Code parity** — how each Figma variant maps to a code prop
7. **Open questions / risks** — what could go wrong, what needs stakeholder input

## Output Location
Save to: `{output_root}/guild-artifacts/component-architecture-[component-name].md`

After approval, the user can run **Tinker — Atomize** (build the atoms) → **Tinker — Variants** (build the variant set) → **Tinker — Variables** (bind colors).

## Hard rules
- Do NOT script in Figma until the spec is approved
- Do NOT invent variables that don't exist in the Semantic collection — propose them as a separate decision
- Do NOT plan boolean→boolean cascades (Plugin API doesn't support them)
