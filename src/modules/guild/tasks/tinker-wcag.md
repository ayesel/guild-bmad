# Tinker — WCAG

## Purpose
Verify that status token Fg/Bg pairs in a design system pass WCAG AA contrast (4.5:1 for normal body text). Catch the Green trap and similar luminance issues before they ship.

> **Two surfaces, one formula.** This task audits the **Figma** variable layer (resolver below walks Figma
> variable aliases). The **code/CSS** twin lives in Sage's foundation gate (`design-system-foundation.md`,
> step 4b), which walks `var(--…)` custom-property alias chains instead. The WCAG luminance/contrast math is
> identical — keep the two resolvers in sync. Run this one when the source of truth is Figma; rely on the DSF
> gate when the source of truth is code tokens. Neither is optional: a token-only project still gets contrast
> checked at the foundation gate, before any screen is built.

## Pre-flight Checks

### 0. Load Project State
- Confirm the file has Semantic variables for Status colors (or whatever your project's status token namespace is)

### 1. Verify knowledge base loaded
- `wcag-tokens-reference.md`

## Input
User asks for a contrast audit:
- "Verify all Status tokens pass AA"
- "Check the new tag colors"
- "Audit our design system for contrast issues"

## Process

### Step 1 — Identify the token pairs to audit
List every Fg/Bg pair that appears together in the design. Standard set:
- `Status/OkFg` on `Status/OkBg`
- `Status/WarnFg` on `Status/WarnBg`
- `Status/DangerFg` on `Status/DangerBg`
- `Status/InfoFg` on `Status/InfoBg`
- `Status/NeutralFg` on `Status/NeutralBg`
- Plus any project-specific Status pairs

Also include text-on-surface pairs:
- `Ink/Body` on `Surface/Card`
- `Ink/Muted` on `Surface/Card`
- `Ink/Primary` on `Surface/Base`

### Step 2 — Resolve each variable to its actual RGB
Variables can alias other variables (Semantic → Primitive). Walk the alias chain to get the final RGB.

```javascript
function varColor(variableId) {
  const collections = figma.variables.getLocalVariableCollections();
  function resolve(id) {
    const v = figma.variables.getVariableById(id);
    const collection = collections.find(c => c.variableIds.includes(id));
    const modeId = collection?.modes[0].modeId;
    const val = v.valuesByMode[modeId];
    if (val?.type === 'VARIABLE_ALIAS') return resolve(val.id);
    return val; // {r, g, b}
  }
  return resolve(variableId);
}
```

### Step 3 — Calculate contrast ratios
```javascript
function luminance({ r, g, b }) {
  const lin = v => v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
}

function contrast(fg, bg) {
  const l1 = luminance(fg), l2 = luminance(bg);
  const hi = Math.max(l1, l2), lo = Math.min(l1, l2);
  return (hi + 0.05) / (lo + 0.05);
}

const ratio = contrast(fgRgb, bgRgb);
```

### Step 4 — Grade each pair
- **`>= 7.0`** → AAA ✓ (passes both AAA and AA)
- **`>= 4.5`** → AA ✓ (passes for normal body text, fails AAA for normal)
- **`>= 3.0`** → AA Large ⚠️ (passes only for 18px+ regular or 14px+ bold)
- **`< 3.0`** → FAIL ✗

For status tags rendered at 14px medium (NOT bold), require `>= 4.5`. The 3:1 large-text exception doesn't apply unless the text is genuinely 14px BOLD or 18px+.

### Step 5 — Report failures with fix recommendations
For each failing pair, identify what to do:
- **The Green trap**: Green/500 on Green/100 fails. Fix by walking foreground darker (Green/700, possibly Green/800).
- **Yellow / Amber trap**: similar issue with high-luminance hues. Walk foreground darker.
- **Muted text on subtle backgrounds**: if `Ink/Muted` on `Surface/Base` fails at small text sizes, restrict `Ink/Muted` to 14px+ or use `Ink/Secondary` instead.

If a primitive doesn't exist at the needed darkness, **propose adding one**:
- "Green/700 (#15803D) needs to be added to the Primitive collection. Status/OkFg should alias it instead of Green/500."

This is an architectural decision — don't just add primitives without confirmation.

## Output
Produce a contrast report:

```
=== WCAG CONTRAST AUDIT ===

Pair                              Ratio    Grade
─────────────────────────────────────────────
Status/OkFg on OkBg              4.57:1   AA ✓
Status/WarnFg on WarnBg          4.51:1   AA ✓
Status/DangerFg on DangerBg      5.30:1   AA ✓
Status/InfoFg on InfoBg          5.17:1   AA ✓
Status/NeutralFg on NeutralBg    6.92:1   AA ✓
Ink/Body on Surface/Card         12.6:1   AAA ✓
Ink/Muted on Surface/Card        4.4:1    AA Large ⚠️
─────────────────────────────────────────────
PASSING: 6 / 7
FAILING: Ink/Muted on Surface/Card — 4.4:1 fails for body text under 18px

RECOMMENDATIONS:
- Either downgrade Ink/Muted from Slate/500 (#94A3B8) to Slate/600 (#475569) to clear AA at all sizes
- Or restrict Ink/Muted to 14px+ regular / 18px+ regular usage (document this constraint)
```

## Output Location
Save to: `{output_root}/guild-artifacts/wcag-audit-[YYYY-MM-DD].md`

## Hard rules
- ALWAYS use the WCAG formula, not visual judgment. Especially for green and yellow.
- DO NOT take the large-text exception unless the actual rendered text qualifies (18px+ or 14px+ bold)
- Status indicators must communicate state via more than color — confirm tags include a label and optionally an icon
- If a pair fails, propose a fix (not just the failure). Acceptable fixes: walk fg darker, walk bg lighter, swap the variable alias to a darker primitive, add a new primitive.
