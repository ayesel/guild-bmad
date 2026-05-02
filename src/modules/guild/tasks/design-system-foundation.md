# Design System Foundation Check

## Purpose
Audit the project's design system foundation BEFORE any page-level visual work. Verify that the **token layer** (spacing, motion, shadow, typography, color, radius) and the **base primitive layer** (Button, Input, Select, ChipGroup, Field, Card, Badge, IconButton) exist and are reusable. Without this gate, agents inline ad-hoc components on every page and the system fragments.

This is Sage's "is the foundation poured?" check, run alongside Mage. It's a **HARD GATE** — the quest does not proceed to page-level visual design until the foundation passes or the gaps are explicitly accepted by the user.

## When to run
- After Phase 0 (Design Direction Brief), before Phase 1 (research) of any quest — so research is anchored AND the foundation is known
- Standalone via `/guild-system-check` at any time
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
| **Motion** | duration (fast/base/slow), easing (in/out/inOut) | Named tokens, not raw `transition-all` |

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
```

### 6. Verdict + remediation plan

Choose ONE:

- **PASS** — All required tokens present, all required primitives extracted with variants, usage discipline within thresholds. Quest proceeds.
- **CONDITIONAL** — Minor gaps (1-2 tokens missing, 1-2 primitives missing). Quest may proceed but the gaps become Healer's first stories before any page-level work.
- **FAIL** — Significant gaps (3+ token categories missing, 3+ required primitives missing, OR usage discipline violations exceed thresholds). Quest **STOPS**. The next agent task is to add the missing tokens and primitives BEFORE the next page touches the screen.

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
- [ ] Remediation plan is specific (file:line, proposed token names, proposed file paths) — not generic ("improve tokens")
- [ ] User decision captured verbatim
- [ ] Artifact saved to `{output_root}/guild-artifacts/design-system-foundation.md`
