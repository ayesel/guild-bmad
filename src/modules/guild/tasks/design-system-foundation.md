# Design System Foundation Check

## Purpose
Audit the project's design system foundation BEFORE any page-level visual work. Verify that the **token layer** (spacing, motion, shadow, typography, color, radius) and the **base primitive layer** (Button, Input, Select, ChipGroup, Field, Card, Badge, IconButton) exist and are reusable. Without this gate, agents inline ad-hoc components on every page and the system fragments.

This is Sage's "is the foundation poured?" check, run alongside Mage. It's a **HARD GATE** — the quest does not proceed to page-level visual design until the foundation passes or the gaps are explicitly accepted by the user.

## When to run
- After Phase 0 (Design Direction Brief), before Phase 1 (research) of any quest — so research is anchored AND the foundation is known
- Standalone via `/guild-agent-sage SC` at any time
- After every quest's design phase, to refresh the audit

## Output
Save to `{output_root}/guild-artifacts/design-system-foundation.md` using the structure below. This becomes the `design_system_foundation` Quest Variable.

## Execution

Run as Sage (Design QA). Stay in character.

### 1. Discover the project's style location

Look for, in order:
1. `app/globals.css` (Next.js / Tailwind v4 — `@theme` block)
2. `tailwind.config.{ts,js}` (Tailwind v3)
3. `styles/tokens.{ts,js,json}`, `theme/`, `design-system/`
4. `src/styles/`, `src/theme/`
5. The `arise-storybook` repo (referenced in `guild.config.yaml` if present)

If none found, declare the project **token-less** and proceed to gap report.

### 2. Audit token layer

For each category, check whether the project defines named tokens (vars / theme keys). For each missing category, the agent later cannot avoid inlining raw values.

| Category | What to look for | Pass criteria |
|---|---|---|
| **Color** | surface, ink, border, brand, status, chart roles | ≥6 named roles per family, ≥4 status states |
| **Spacing** | scale tokens (4/8/12/16/24/32/48/64) | Documented scale, even if mapped to Tailwind defaults |
| **Typography** | font-family, scale (xs→4xl), weights, line-heights | All sizes named; 2-3 family roles (display/sans/num) |
| **Radius** | sm, md, lg, xl | At least 3 sizes named |
| **Shadow** | elevation tokens (sm, md, lg, glass, focus) | At least 3 elevations |
| **Motion** | role-based duration scale (`instant/micro/short/medium/long`), easing set incl. a **signature curve** (`--ease-signature`) + out/in/emphasis/linear, `--stagger`, and a defined `prefers-reduced-motion` branch | Tokens present per `shared-sidecar/motion-and-interaction-principles.md`; no raw `transition-all` or hardcoded durations in components. Audited in depth at step 4c. |

### 3. Audit base primitive layer

Look in `components/ui/`, `src/components/ui/`, or whatever the project's primitive folder is. For each primitive, check: (a) does the file exist, (b) does it accept variant/size/state props, (c) is it used in more than one place.

Required primitives:
- `Button` (variants: primary, secondary, ghost, danger, link)
- `Input` (text input with label, error, helper text slots)
- `Select` (custom — not a bare `<select>`)
- `ChipGroup` / `SegmentedControl` (multi-option single-select)
- `Field` (label + input wrapper with error/helper text)
- `Card` (surface container with optional header/footer)
- `Badge` / `Pill` (status/label small chip)
- `IconButton` (square icon-only button)
- `Tooltip`
- `Skeleton` / loading state primitive

Recommended (flag missing but don't block):
- `Modal` / `Dialog`
- `Drawer` / `Sheet`
- `Tabs`
- `Toast`
- `Table` (with sort/filter scaffolding)
- `EmptyState`

### 4. Audit usage discipline

Run grep to detect violations of system discipline:

| Violation | Grep pattern | Threshold |
|---|---|---|
| Inline `<select>` instead of custom Select | `<select\b` | 0 outside `components/ui/Select.tsx` |
| Hardcoded hex colors | `#[0-9A-Fa-f]{6}\|#[0-9A-Fa-f]{3}\b` (in app/components, not tokens) | <5 occurrences |
| Raw `transition-all` without duration token | `transition-all\b(?!.*duration)` | <3 occurrences |
| Inline `style={{` for visual properties | `style=\{\{[^}]*(color\|background\|padding\|margin\|font)` | <5 occurrences |
| Inline component definitions in pages | `^function [A-Z]\w* ?\(` inside `app/**/page.tsx` (excluding the page component itself) | 0 — extract them |

### 4b. Audit contrast (WCAG AA) — the correctness check the discipline greps miss

Token *presence* and *consistency* (steps 2–4) say nothing about whether the tokens are **legible**. A
system can bind every value to a token, pass every grep, and still ship a status color that fails WCAG
— "the Green trap" (Green/500 on Green/100) and the Amber/Yellow trap are the classic cases. A coherent
system that is uniformly inaccessible still fails users. So the foundation gate computes contrast, it does
not eyeball it.

This is the **code-side** twin of Tinker's `tinker-wcag.md` (which audits the same pairs in Figma
variables). Same WCAG formula; the only difference is the resolver — here we walk **CSS custom-property
alias chains** (`var(--…)` → … → hex) instead of Figma variable aliases.

```javascript
// 1. Parse the token layer (tokens.css / globals @theme / tailwind config) into a flat map,
//    then resolve each semantic var through its alias chain to a final hex.
function resolveVar(name, vars) {            // vars: { '--color-positive-text': 'var(--color-positive-600)', ... }
  let v = vars[name];
  while (v && /^var\(\s*(--[\w-]+)\s*\)$/.test(v)) v = vars[v.match(/^var\(\s*(--[\w-]+)\s*\)$/)[1]];
  return v; // final hex, e.g. '#0b7c44'
}

// 2. WCAG relative luminance + contrast (identical to tinker-wcag)
const lin = c => (c /= 255, c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const L = hex => { const [r,g,b] = hex.replace('#','').match(/../g).map(h => parseInt(h,16));
                   return 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b); };
const contrast = (fg,bg) => { const a=L(fg), b=L(bg), hi=Math.max(a,b), lo=Math.min(a,b);
                              return (hi + 0.05) / (lo + 0.05); };
```

**Pairs to audit** — every semantic foreground/background that renders together. At minimum:
- Each status family's text on its own subtle/solid bg: `*-text`/`on-*` on `*-subtle`/`*` (positive, danger, warn, info, neutral — whatever the project defines).
- `on-accent` on `accent`; `on-danger` on `danger` (button labels).
- `fg` and `fg-muted` on `bg` and `bg-subtle` (body + muted text on every surface).

**Grade each pair against the size it actually renders at** (read the binding primitive's CSS):
- `>= 4.5` → AA ✓ for normal text. `>= 7.0` → AAA.
- `>= 3.0` → AA Large ⚠️ — **only** valid if the text is genuinely ≥18.66px, or ≥14px **bold**. Badge/tag text (12–14px medium) does NOT qualify; require 4.5.
- `< required` → **FAIL ✗**. For every failure, propose the fix (walk fg darker to the next primitive step, e.g. positive.500 → positive.600; re-alias the semantic token — never inline an override on a screen).

**APCA supplement (dark themes / thin type):** WCAG's ratio under-detects on dark
backgrounds. For any dark theme, ALSO run `python3 ~/.claude/guild/scripts/apca-contrast.py
--fg <hex> --bg <hex>` (fallback: scripts/) on the same pairs: target Lc ≥75 body,
≥45 large/bold, ≥30 non-text (anti-slop-survey.md). WCAG AA remains the blocking
line; APCA failures on a WCAG-passing dark pair are CONDITIONAL-class findings.

A failing status or body-text pair is a **hard gate failure** (see step 6), not a warning — it is a shipping
accessibility defect, and the whole point of the gate is to catch it before any screen is built on top of it.

### 4c. Audit motion + interaction-state coverage — the "crafted vs. generic" check

The discipline greps and contrast check say nothing about whether the product *feels* finished. Motion is the
layer most responsible for crafted-vs-generic, and the layer most often skipped. Audit it against
`shared-sidecar/motion-and-interaction-principles.md`:

1. **Motion tokens present.** Role-based duration scale, the easing set including a real `--ease-signature`
   `cubic-bezier` (NOT a generic symmetric ease-in-out used as the default), `--stagger`, and a defined
   `prefers-reduced-motion` branch. Missing signature easing or reduced-motion branch = the two most common gaps.
2. **Motion is tokenized, not inlined.** Components reference motion tokens; no hardcoded durations
   (`grep` for `transition:.*[0-9]+ms|[0-9.]+s` and `transition-all` in component files) and no per-screen
   easing. Raw transition values = motion drift, same class of defect as raw hex.
3. **State coverage on every interactive primitive.** For Button/Input/Toggle/Select/etc., verify all required
   states exist: `default, hover, focus-visible, active/pressed, disabled, loading` (+ `selected`/`error` where
   relevant). Missing states are the #1 source of "janky/unfinished." List any element missing states.
   (This is the MEASURE-tier half of ui-factors factor 5: at the component layer the state matrix is
   deterministic — variants enumerate states — whereas at app level it is only LOOK-tier. Gate it here.)
4. **Reduced-motion is a designed branch.** A `@media (prefers-reduced-motion: reduce)` path exists and
   preserves feedback (doesn't just delete it).

Failures here are **CONDITIONAL → FAIL** depending on severity: a missing signature easing or absent
reduced-motion branch, or interactive primitives with no pressed/focus/loading states, block the gate — a
generic-feeling or half-stated foundation propagates to every screen. For each gap, propose the token or state to add.

### 4d. Audit craft vocabulary + theme parity — ui-factors upstream enforcement

Per `docs/guild/decisions/ui-factors-research.md` (§2 factors 3, 6, 7, 9, 10, 16 and §6 mapping):
these rendered-surface audit factors are cheapest to enforce at the token/primitive layer, where they
are pure MEASURE. Mage's render-time gates are the backstop; this step is the prevention — a factor
enforced here should never fire downstream.

**Vocabulary discipline (CONDITIONAL-class flags, propose consolidations):**
1. **Radius vocabulary** — count distinct non-zero radius token values: ≤4 passes; >4 = sprawl. Also
   grep components for raw `border-radius` values (same defect class as raw hex).
2. **Shadow light source** — parse every elevation token's `box-shadow` offsets: all y-offsets must
   share one sign (single implied light source, conventionally down). Mixed directions = flag with the
   offending tokens.
3. **Border-weight vocabulary** — ≤3 distinct border widths across tokens + components.
4. **Icon sizing** — the icon primitive enforces size props (no freeform); peer icons in one context
   render within ±15% of each other.
5. **Neutral temperature** — convert near-gray tokens to HSL; all should share one hue-temperature
   sign (all cool or all warm). Mixed-temperature neutrals on one surface = flag.
6. **Motion envelope** — standard-transition duration tokens: flag >400ms; none >500ms (NN/g audit
   bound). Long durations are reserved for large-scale moves and named as such.

**Hard items (FAIL — same class as 4b contrast):**
7. **Theme parity** — if a second theme exists: every semantic role defined in BOTH modes (diff the
   token maps; a role present in one and missing in the other = FAIL); re-run the step-4b contrast
   pairs in dark mode (dark-mode AA loss = FAIL); role luminance order must not invert between modes
   (`bg` vs `bg-subtle` etc.).
8. **Focus + target primitives** — a focus-indicator token/style exists meeting WCAG 2.4.13 (≥3:1
   focused-vs-unfocused delta, area ≥ a 1px-perimeter equivalent) and every interactive primitive
   binds it; interactive primitives' default hit-rect ≥24px (advise 44px for touch-primary actions).

When `design_surface` is figma/both, the same checks run on Figma variables via Tinker's `WC`
(tinker-wcag) and `TK` (tinker-tokens) — this step is the code-side twin.

### 5. Generate gap report

Produce a clear pass/fail per category with specifics:

```markdown
## Token layer

✅ Color — 24 tokens across 6 families (surface, ink, border, brand, status, chart)
❌ Spacing — no named scale; 47 raw Tailwind values found across 12 files
❌ Motion — no duration/easing tokens; 8 raw `transition-all` uses
✅ Typography (font families) — 3 roles defined
❌ Typography (scale) — sizes inline (text-2xl, text-3xl); no scale tokens
✅ Radius — 4 tokens
⚠️  Shadow — only `--color-glass-shadow`; missing elevation scale

## Primitive layer

✅ Button (5 variants, used in 8 places)
❌ Select — not extracted; bare `<select>` used in app/scenarios/page.tsx
❌ ChipGroup — defined inline at app/scenarios/page.tsx:191 as `RadioRow`; misnamed
❌ Field — defined inline at app/scenarios/page.tsx:180; not extracted
✅ Card (used in 4 pages)
⚠️  Badge — exists but no `tone` prop; status colors inlined

## Usage discipline

❌ 3 inline `<select>` elements outside components/ui/
❌ 14 hardcoded hex colors in component files
⚠️  6 raw `transition-all` without duration
✅ 0 inline page-level component definitions in components/ui/

## Contrast (WCAG AA)

✅ on-accent on accent — 6.29:1 AA
✅ on-danger on danger — 4.83:1 AA
❌ positive-text on positive-subtle — 3.30:1 FAIL (Badge text 12px needs 4.5) → re-alias positive-text to positive.600 (#0b7c44 → 4.96:1)
✅ fg on bg — 18.6:1 AAA
⚠️  fg-muted on bg-subtle — 4.55:1 AA (thin; restrict to ≥14px)
```

### 6. Verdict + remediation plan

Choose ONE:

- **PASS** — All required tokens present, all required primitives extracted with variants, usage discipline within thresholds, **and every status/body-text contrast pair clears its WCAG AA threshold**. Quest proceeds.
- **CONDITIONAL** — Minor gaps (1-2 tokens missing, 1-2 primitives missing). Quest may proceed but the gaps become Healer's first stories before any page-level work. **Contrast failures are never CONDITIONAL** — a sub-threshold pair is a shipping a11y defect; downgrade to FAIL.
- **FAIL** — Significant gaps (3+ token categories missing, 3+ required primitives missing, usage discipline violations exceed thresholds, **any status/body-text pair fails WCAG AA contrast**, **motion fails step 4c** — no signature easing, no reduced-motion branch, raw transitions in components, or interactive primitives missing pressed/focus/loading states — **OR a 4d hard item fails** — theme-parity role gap, dark-mode AA loss, or missing/unbound focus-indicator token). Quest **STOPS**. The next agent task is to add the missing tokens/primitives, re-alias failing color tokens, and complete the motion + state layer BEFORE the next page touches the screen.

> Scale the primitive checklist to the product. The 10-primitive list is sized for a full app; for a small
> surface (≤ a handful of screens) treat `Tooltip`/`Skeleton`/`IconButton`/`Select` as *recommended, not
> blocking* if the product has no use for them. Do not FAIL a 3-screen app for lacking a `Skeleton` while a
> real contrast defect ships — the contrast gate is the non-negotiable one.

For CONDITIONAL or FAIL, generate a remediation plan: ordered list of (a) tokens to add (with proposed values), (b) primitives to extract (with proposed file paths), (c) usage cleanups (with file:line references).

### 7. Confirm with user

Show the verdict + remediation plan. Ask:
- "Proceed with quest after fixing these?" (recommended for FAIL)
- "Proceed in parallel — Healer fixes tokens while Mage starts page work?" (acceptable for CONDITIONAL)
- "Acknowledge gaps and proceed anyway?" (only when user explicitly accepts technical debt)

Save the user's decision in the artifact. Whatever was chosen becomes the binding constraint for downstream agents.

## Output structure

```markdown
# Design System Foundation Audit — {project_name}

**Date:** {date}
**Auditor:** Sage
**Verdict:** PASS | CONDITIONAL | FAIL

## Discovery
- Style location: {path}
- Primitive folder: {path}
- Storybook detected: {yes/no, path}

## Token Layer
{table — pass/fail per category with counts}

## Primitive Layer
{table — exists/missing/incomplete per primitive}

## Usage Discipline
{table — violations found vs thresholds}

## Contrast (WCAG AA)
{table — each status + body-text Fg/Bg pair: resolved hex, ratio, grade vs the size it renders at; failures first}

## Motion & interaction (step 4c)
{motion tokens present? signature easing? reduced-motion branch? raw transitions in components? per-primitive state coverage — list any element missing pressed/focus/loading/disabled}

## Craft vocabulary & theme parity (step 4d)
{radius/border/shadow-direction/icon vocabulary counts vs budgets; neutral temperature sign; motion envelope; theme-parity role diff + dark-mode contrast re-run; focus-indicator token + target floor — hard items first}

## Remediation Plan
{ordered list of tokens to add, primitives to extract, cleanups to apply, with file:line references}

## User Decision
{fix-first | parallel | accept-debt — captured verbatim}

## How downstream agents should use this

**Mage:** Use only the documented tokens. If a token is missing for a need you have, escalate to Healer instead of inlining a raw value.

**Rogue:** Use only the documented primitives. If a primitive is missing, escalate to Healer to extract it before referencing the pattern in a wireframe.

**Healer:** Tokens and primitives in the Remediation Plan are your first stories — they get done before any page-level story.

**Sage:** Re-run this audit at the end of every quest. Verdict can only get better, never worse.
```

## Quality checks
- [ ] Style location discovered or declared missing
- [ ] All 6 token categories audited
- [ ] All 10 required primitives checked
- [ ] Usage discipline grep run on actual codebase
- [ ] Contrast computed (not eyeballed) via WCAG formula for every status + body-text pair; each failure listed with a concrete token-level fix
- [ ] Verdict downgraded to FAIL if any status/body-text pair fails AA
- [ ] Motion audited (step 4c): signature easing + role-based durations + stagger + reduced-motion branch present; no raw transitions in components
- [ ] Interaction-state coverage checked on every interactive primitive (default/hover/focus/active/disabled/loading)
- [ ] Craft vocabulary counted (step 4d): radii ≤4, single shadow light direction, border weights ≤3, icon variance ≤15%, neutral temperature consistent, motion envelope respected
- [ ] Theme parity + focus/target hard items checked (step 4d): role diff across modes, dark-mode contrast re-run, focus-indicator token bound, ≥24px primitive hit-rects; any hard failure downgrades verdict to FAIL
- [ ] Remediation plan is specific (file:line, proposed token names, proposed file paths) — not generic ("improve tokens")
- [ ] User decision captured verbatim
- [ ] Artifact saved to `{output_root}/guild-artifacts/design-system-foundation.md`
