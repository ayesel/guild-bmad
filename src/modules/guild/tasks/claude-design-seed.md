# Claude Design Seed

**Purpose.** Emit a paste-ready brief that seeds **Claude Design** (or any external generator — Quad, Figma Make, v0) so it generates UI that already conforms to the Guild **Product Baseline** and the project's brand/tokens. This is the *generate* side of Guild's Claude Design integration; `claude-design-handoff-gate.md` is the *gate* side. Same source of truth, two ends:

```
Enchanter/brand intent + repo tokens ──▶ [THIS: seed brief] ──▶ Claude Design generates ──▶ [handoff-gate] audits the bundle ──▶ build
```

Without the seed, Claude Design regresses to generic output and the gate has to reject more. Seeding makes the gate a backstop instead of a bottleneck (auto-generation is a defect *amplifier* — a missing filter or a failing-contrast token gets stamped across every artifact).

## When to run
- `design_surface` is `claude-design` or `both` (read `guild.config.yaml`; resolve `auto` via `shared-sidecar/design-surface-modes.md`). If `figma`/`greenfield`, tell the user this seed targets Claude Design and stop unless they want it anyway.
- Run BEFORE the first Claude Design generation / "Set up your design system" onboarding, and re-run whenever the Baseline or brand tokens change.

## Inputs (gather, don't invent)
1. **Product Baseline** — `src/modules/guild/agents/shared-sidecar/product-baseline.md` (the mandatory defaults).
2. **Brand kernel / tokens** — in priority order: `docs/design-direction.md` (if present) → repo design tokens (DTCG / `tailwind.config` / CSS custom props) → Figma variables. Capture the LOCKED palette (hex + role), type families + scale, radius token, motion language, density. If a brand authority/Enchanter brief exists, use it as the source of brand intent; never fabricate palette or voice.
3. **Foundation constraints** — anything from a prior `design-system-foundation` audit (contrast-safe pairs, the green-trap note, token names).

## Procedure
1. Resolve design surface + load the three inputs above.
2. **Translate the Baseline into imperative generation directives** — Claude Design follows instructions, not a rulebook, so convert each fired-relevant rule into a "MUST" line (see template). Include the data-shape triggers (T1–T8) and the cross-cutting laws (legible data, one shape language, consistent iconography, restrained elevation, action hierarchy, etc.).
3. **Bind the brand block to measured values** — exact hexes with contrast notes (reuse `design-system-foundation` if available), the radius token, type families. Tell CD to apply these in onboarding (team colors/typography/components), NOT to invent its own.
4. **State the contract** — the resulting handoff bundle WILL be audited by `claude-design-handoff-gate.md` (contrast + 0-drift coherence + Baseline triggers); generating off-spec just gets rejected, so conform now.
5. Write the artifact to `{output_root}/guild-artifacts/claude-design-seed.md` and tell the user to paste it into Claude Design's onboarding / generation prompt.
6. Note the limitation honestly: Claude Design is a research-preview web product, so this is a MANUAL export→paste step, not yet an automated `/guild-quest` stage.

## Output template — `{output_root}/guild-artifacts/claude-design-seed.md`

```markdown
# Claude Design Seed — {Project}
*Paste this into Claude Design onboarding ("Set up your design system") and prepend it to generation prompts. Output will be gated against these rules before build.*

## Brand (apply these exactly — do not invent)
- **Palette (LOCKED):** {token — #hex — role}, … (with contrast notes: body text pair ≥ 4.5:1; large/headers ≥ 3:1)
- **Type:** Display = {family}; Body/UI = {family}; scale discipline: one display + one body + one small per view.
- **Shape:** one radius token = {value} ("square with rounded corners"); full-pill reserved for avatars only.
- **Motion / density:** {e.g. slow warm 400–600ms; generous spacing scale 4/8/12/16/24/32/48}.

## Non-negotiable UX defaults (apply BY DATA SHAPE, first render)
- **Comparison data** (estimate vs actual, budget vs spent): show both + variance (Δ and %) + a totals row. Mark not-yet-known as TBD, exclude from confirmed totals.
- **Any growable collection** (>~10 items): search + filter (every low-cardinality field) + sort + result count + empty / zero-results / error states.
- **Categorizable records:** group by the category by default with per-group subtotals; user-authored categories are renameable in place.
- **Status rollups:** count EVERY enum value incl. terminal states (declined/cancelled) — never a curated subset.
- **Navigation:** text labels always (never icon-only), grouped, clear active state, ≤7 top-level.
- **Every data container:** initial/skeleton, populated, empty (with CTA), zero-results, error (with retry).
- **Forms:** labels above inputs, inline validation on blur, disabled-until-valid submit, success/error feedback.

## Cross-cutting laws
- Legible data: metric/KPI numerals use a clear tabular face, never a decorative serif; never truncate values/controls to fit.
- One shape language (single radius), consistent iconography (one icon set, no icon-only actions), restrained elevation (soft neutral-warm shadows, never a saturated brand-hue drop shadow).
- Action hierarchy: at most one primary (filled) action per view; secondary quiet; rarely-used/destructive utilities in an overflow, never bare in chrome. No two visible controls share an ambiguous label.
- Surface content, sink empties; keep contextual action bars reachable (fixed/sticky).
- Direct manipulation: if a value is shown, it's actionable where it sits.

## Contract
The handoff bundle you produce will be audited by Guild's Claude Design Handoff Gate (contrast, 0-drift token coherence, and the triggers above). Off-spec output is rejected — conform here.
```

## Done when
- `{output_root}/guild-artifacts/claude-design-seed.md` exists, brand block bound to real measured tokens (not placeholders), Baseline directives present, and the user has the paste instruction. Pairs with `claude-design-handoff-gate.md` for the return trip.
