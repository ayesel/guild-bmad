# WCAG Token Contrast Reference

Status colors are the most common failure point in design tokens. This reference covers what passes WCAG AA and the gotchas that make tokens look right but fail audits.

---

## The thresholds

WCAG 2.2 AA requires:
- **Normal text** (under 18px regular, or under 14px bold): **4.5:1**
- **Large text** (18px+ regular, or 14px+ bold): **3:1**
- **Non-text contrast** (UI elements, icons, focus indicators): **3:1**

Status tags typically render at 14px medium (500 weight). That's NOT bold (700+), so status tags need **4.5:1 contrast**, not 3:1. Don't take the large-text exception unless your tag uses 14px bold or 18px+ regular.

---

## Calculating contrast in plugin scripts

```javascript
function luminance({ r, g, b }) {
  const lin = v => v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
}

function contrast(fg, bg) {
  const l1 = luminance(fg), l2 = luminance(bg);
  const hi = Math.max(l1, l2), lo = Math.min(l1, l2);
  return ((hi + 0.05) / (lo + 0.05));
}

// Pass: ratio >= 4.5 (normal text), >= 3 (large text or UI)
```

Resolve a variable's RGB through the alias chain:
```javascript
function varColor(variableId) {
  const collections = figma.variables.getLocalVariableCollections();
  function resolve(id) {
    const v = figma.variables.getVariableById(id);
    const collection = collections.find(c => c.variableIds.includes(id));
    const modeId = collection?.modes[0].modeId;
    const val = v.valuesByMode[modeId];
    if (val?.type === 'VARIABLE_ALIAS') return resolve(val.id);
    return val;  // RGB object {r, g, b}
  }
  return resolve(variableId);
}
```

---

## The Green trap (universal)

The single most common mistake across design systems: using a vibrant mid-tone green for the success/Ok foreground on a light green background. Green's luminance contribution to perceived brightness is high (0.7152 weight in the WCAG formula vs 0.2126 for red and 0.0722 for blue), so even a "500" weight green typically fails AA on a "100" weight green background.

Illustrative example (using common Tailwind-like values — your palette may differ):

| Combination | Approx. hex | Approx. ratio | AA |
|---|---|---|---|
| Mid green (~500, e.g. `#16A34A`) on light green (~100, e.g. `#DCFCE7`) | — | ~3.00:1 | ❌ FAIL |
| Dark green (~700, e.g. `#15803D`) on light green (~100, e.g. `#DCFCE7`) | — | ~4.57:1 | ✓ PASS |
| Deeper green (~800, e.g. `#166534`) on light green (~100, e.g. `#DCFCE7`) | — | ~7:1 | ✓ AAA |

**Rule**: For green text on light green backgrounds, push the foreground darker than you'd intuitively expect — typically two steps deeper than the eyeballed midpoint. Always verify with the contrast formula, not your eyes. Don't trust visual judgment on green.

The same trap exists for **yellow/amber** (similar luminance issues against light tints). Treat any warm hue with a high green/yellow component as suspect until measured.

---

## Reference: an example status palette that passes AA

Below is **one example** of a Status FG/BG palette where every pair clears 4.5:1. The exact hex values are illustrative, not prescriptive — your project's palette will have its own values, and the WCAG audit script (further down) is what validates *your* palette, not this table.

| Status | FG (illustrative) | BG (illustrative) | Approx. ratio |
|---|---|---|---|
| Ok | `#15803D` (dark green) | `#DCFCE7` (light green) | 4.57:1 ✓ |
| Warn | `#B45309` (dark amber) | `#FEF3C7` (light amber) | 4.51:1 ✓ |
| Danger | `#B91C1C` (dark red) | `#FEE2E2` (light red) | 5.30:1 ✓ |
| Info | `#0369A1` (dark blue) | `#E0F2FE` (light blue) | 5.17:1 ✓ |
| Neutral | `#475569` (dark neutral) | `#F1F5F9` (light neutral) | 6.92:1 ✓ |

### Process for picking your own status pairs

When you set up a new Status palette:
1. Pick the BG (light tint) first — usually `~100` weight of the hue
2. Calculate which weight of the same hue passes 4.5:1 on that BG
3. Start at `~700`. If it doesn't pass, go to `~800` or darker
4. Don't pick FG and BG independently — the pair is what matters
5. If your palette uses non-Tailwind weights (e.g., 50/200/400/800), the same logic applies — pick BG first, then walk darker on FG until the math passes

---

## Audit script for a tag system

Generic — works against any Semantic collection that has Status FG/BG variables. Adjust the variable name strings to match your project's naming.

```javascript
const pairs = [
  { name: 'Ok',      fg: 'Status/OkFg',      bg: 'Status/OkBg' },
  { name: 'Warn',    fg: 'Status/WarnFg',    bg: 'Status/WarnBg' },
  { name: 'Danger',  fg: 'Status/DangerFg',  bg: 'Status/DangerBg' },
  { name: 'Info',    fg: 'Status/InfoFg',    bg: 'Status/InfoBg' },
  { name: 'Neutral', fg: 'Status/NeutralFg', bg: 'Status/NeutralBg' },
];

const collections = figma.variables.getLocalVariableCollections();
const sem = collections.find(c => c.name === 'Semantic');
const v = (name) => sem.variableIds
  .map(id => figma.variables.getVariableById(id))
  .find(x => x.name === name);

for (const { name, fg, bg } of pairs) {
  const fgVar = v(fg);
  const bgVar = v(bg);
  if (!fgVar || !bgVar) { console.log(`${name}: variable missing`); continue; }
  const fgRgb = resolveVariableRGB(fgVar.id);
  const bgRgb = resolveVariableRGB(bgVar.id);
  const ratio = contrast(fgRgb, bgRgb);
  const grade = ratio >= 4.5 ? 'AA ✓' : ratio >= 3 ? 'AA Large ⚠️' : 'FAIL ✗';
  console.log(`${name}: ${ratio.toFixed(2)}:1 ${grade}`);
}
```

Run this before declaring any status palette done.

---

## Non-status text contrast (example pairings)

The same audit pattern applies to text-on-surface pairs. Example expected pairings (using the example Semantic namespace from `variables-and-tokens-reference.md` — your project may name them differently):

| | FG variable | BG variable | Should pass |
|---|---|---|---|
| Body text | `Ink/Body` (~neutral 700) | `Surface/Card` (White) | 4.5:1+ |
| Muted text | `Ink/Muted` (~neutral 500) | `Surface/Card` (White) | 4.5:1+ at 14px+, may fail at smaller sizes |
| Header / strong | `Ink/Primary` (~neutral 900) | `Surface/Card` (White) | 7:1+ (AAA easily) |
| Body on subtle bg | `Ink/Body` (~neutral 700) | `Surface/Base` (~neutral 50) | 4.5:1+ |

If `Ink/Muted` (typical `~neutral 500` like `#94a3b8`) doesn't pass on white at small sizes, either downgrade `Ink/Muted` darker (e.g., `~600`, ~4.5:1) or restrict its usage to 14px+ regular / 18px+ regular.

---

## Color blindness consideration

Beyond contrast, status indicators should communicate state by more than color:
- ✓ Status tags include a label ("Active", "Expiring Soon") — the label is the primary signal
- ✓ Optional: an icon (FA6 `circle-check`, `circle-info`, `triangle-exclamation`, `circle-xmark`) reinforces the color signal

A status that's color-only (e.g., a row tinted red with no label) is inaccessible. The text label is the accessibility floor; icons are an enhancement.
