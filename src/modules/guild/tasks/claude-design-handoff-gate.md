# Sage — Claude Design Handoff Gate

## Purpose
Audit a **Claude Design handoff bundle** *before* Claude Code builds from it. Claude Design applies the org
design system consistently and offers accessibility review **only when asked** ("Claude can review your
design for accessibility, contrast ratios…" — opt-in, never enforced). This task is the **enforced** gate
that the opt-in review is not: it parses the bundle's tokens + component spec, runs the same WCAG contrast
and coherence checks as the foundation gate, and FAILs the handoff if the system that's about to be built
is inconsistent or inaccessible. Catch the green-trap once, at the seam, before it's stamped into code.

This is the `claude-design`-mode (and `both`-mode) **input adapter** for the DS Foundation gate
(`design-system-foundation.md`). The contrast + coherence math is identical to that gate's step 4b — only
the *source artifact* differs (a tar bundle instead of repo CSS or Figma variables).

## When to run
- `design_surface` is `claude-design` or `both` (see `shared-sidecar/design-surface-modes.md`).
- After Claude Design produces a handoff bundle, BEFORE the "Send to Claude Code" build is accepted as done.
- Standalone via Sage's menu, or delegated from `design-system-foundation.md` when the mode's input adapter is the bundle.

## Input
A handoff bundle. Per public docs it arrives as a **tar archive** containing a README plus a machine-readable
component spec, the design tokens used on the canvas, the layout hierarchy, and referenced assets. The user
provides the path (or it is dropped in a known location).

> ⚠️ **Format not yet verified against a real bundle.** The locators in Step 2 are best-effort against the
> documented shape. The FIRST time a real bundle is gated, confirm the actual file layout and token
> serialization and correct the locators below — everything downstream (resolver, contrast, coherence) is
> format-independent and will not need to change.

## Process

### Step 1 — Unpack and read intent
```bash
mkdir -p .guild-handoff && tar -xf "$BUNDLE" -C .guild-handoff
cat .guild-handoff/README*            # the intent + build instructions Claude Design wrote
find .guild-handoff -maxdepth 3 -type f   # discover the real layout (tokens, spec, assets)
```
Note what you actually find; reconcile against the assumed layout in Step 2.

### Step 2 — Locate + parse the design tokens (assumed locators — verify)
Look, in order, for the token source inside the bundle:
1. `**/tokens.json` / `**/*.tokens.json` (W3C DTCG `$value`)
2. `**/theme.{json,js,ts}` or a Tailwind/`@theme` blob
3. CSS custom properties in `**/*.css`

Resolve every token through its alias chain to a final value (DTCG `{group.name}` refs, CSS `var(--x)`, or
theme aliases) into one flat map `{ name: '#rrggbb' | value }`. This is the same resolver shape used by
`design-system-foundation.md` step 4b and `tinker-wcag.md` — keep them in sync.

```javascript
// DTCG: resolve {group.name} refs.  CSS: resolve var(--x).  Either way → flat hex map.
function resolveAll(raw, kind) {
  const flat = flatten(raw, kind);                  // → { name: rawValueOrRef }
  const deref = name => {
    let v = flat[name], guard = 0;
    while (v && /(\{[\w.-]+\}|var\(\s*--[\w-]+\s*\))/.test(v) && guard++ < 20)
      v = flat[v.replace(/[{}]/g,'').replace(/^var\(\s*(--[\w-]+)\s*\)$/,'$1')];
    return v;
  };
  return Object.fromEntries(Object.keys(flat).map(n => [n, deref(n)]));
}
```

### Step 3 — Parse the component spec → extract rendered pairs
From the machine-readable component spec, for each component/text node, extract the **foreground/background
token pair** and the **rendered text size + weight**. Build the audit list: every fg-on-bg combination that
actually renders, with the size it renders at.

### Step 4 — Contrast audit (delegated math, identical to the foundation gate)
Apply the WCAG luminance/contrast formula from `design-system-foundation.md` step 4b to every pair:
- normal text → require **≥ 4.5:1**; AAA at ≥ 7.0
- large text (≥ 18.66px, or ≥ 14px **bold**) → may use **≥ 3.0:1** — badge/tag text at 12–14px medium does NOT qualify
- below required → **FAIL ✗**; for each failure propose walking the fg token to the next-darker primitive
  (e.g. positive.500 → positive.600) at the **canonical source**, never a per-component override.

### Step 5 — Coherence / drift check at the seam
- **Token-reference integrity:** every color/space/radius/type value in the spec is a *token reference*, not
  a raw literal. Raw hex/px in the spec = drift entering at handoff → flag with the component path.
- **Token existence:** every token the spec references resolves in Step 2's map (no dangling references).

### Step 6 — Canonical-source reconciliation (anti-drift)
Read `canonical_source` from `guild.config.yaml`.
- `tokens` → the bundle's tokens must match the repo's canonical DTCG. Diff them; flag any divergence (the
  bundle drifted from truth, or the repo is stale).
- `figma` → the bundle's tokens must match the Figma-exported DTCG (`tinker-tokens` output). Flag divergence.
- This is where a `both`-mode three-way split surfaces. Report divergences as FAIL — do not silently accept.

### Step 7 — Verdict
- **PASS** — every rendered pair clears AA, zero raw values in the spec, no dangling tokens, bundle matches
  canonical source. Handoff proceeds to Claude Code.
- **FAIL** — any contrast failure, raw value, dangling token, or canonical divergence. The build is blocked;
  the next action is to fix the **canonical source** and re-export from Claude Design, NOT to patch the
  generated code after the fact.

## Output
Save to `{output_root}/guild-artifacts/handoff-gate-[YYYY-MM-DD].md`:
```markdown
# Claude Design Handoff Gate — {bundle name}
**Date:** {date} · **Auditor:** Sage · **Mode:** claude-design|both · **Canonical:** {source}
**Verdict:** PASS | FAIL

## Contrast (WCAG AA)
{table — each rendered fg/bg pair: resolved hex, ratio, grade vs rendered size; failures first, each with fix}

## Coherence at the seam
{raw values in spec (path), dangling token refs}

## Canonical reconciliation
{bundle-vs-canonical token diffs, or ✅ in sync}

## Remediation
{ordered token-level fixes at the canonical source, with proposed new aliases}
```

## Hard rules
- ALWAYS compute contrast with the WCAG formula, never visual judgment (especially green/amber).
- DO NOT take the large-text exception unless the rendered text genuinely qualifies (≥18.66px, or ≥14px bold).
- Fixes target the **canonical source** and re-export — never a one-off override in the handed-off code.
- A FAIL blocks the build. This gate is the enforcement Claude Design's opt-in review intentionally is not.
- On first contact with a real bundle, verify the Step 2 locators + token serialization and correct them;
  leave a note in the output recording the actual format observed.
