# Product Baseline — Guild's Non-Negotiable UX Defaults

> **What this is.** The defaults a senior product designer applies *without being asked*. Most of Guild's quality knowledge has lived as values ("simplify ruthlessly") or as Mage-only visual reference. Values are inert at generation time and reference is discretionary — so obvious things (filtering, categorization, estimated-vs-actual, labeled nav) only appear after the user iterates. This file converts those values into **triggered, mandatory defaults** that fire off the *shape of the data and the type of the artifact*, applied at GENERATION time, not caught at the gate.
>
> **Three consumers, one source of truth:**
> 1. **Generators** (Rogue, Mage, and any build agent) — load this BEFORE producing an artifact and apply every matching trigger as a default. First render is already good.
> 2. **Gate** (Sage) — uses the same trigger table as a pass/fail rubric. A triggered-but-absent pattern is a finding.
> 3. **External-generator seed** (Claude Design / Quad, per [[claude-design-product]]) — this is the priors text you paste into the design-system / generation prompt so auto-generated output inherits the same defaults instead of regressing to generic.
>
> **The rule for every default below:** apply it silently when its trigger fires. If you deliberately omit one, you must say which and why in one line. Omission-by-forgetting is a defect.

---

## Layer 0 — Universal laws (always on, the *why* behind the triggers)

- **Hick's / Miller** — cap simultaneous choices; chunk and group. More than ~7 peer items → group or paginate, don't list flat.
- **Recognition over recall** — label everything. **No icon-only controls** (nav, toolbar, table actions) without a visible text label or, at absolute minimum, a tooltip + aria-label. The user should never have to remember what a glyph means.
- **Jakob's law** — use the conventional pattern for the job. Don't invent a novel interaction where a standard one exists (tables sort by clicking headers; lists filter from a toolbar; tabs switch peer views). Novelty is a cost you must justify.
- **Progressive disclosure** — show what's needed now; defer the rest behind expand / detail / "more". Don't dump every field on first paint.
- **Match the data, not the request** — design for the data's real *shape*, not the literal words of the ask. "Show the budget" with plan+actual data means a comparison view, even if the user only said "show."
- **Every collection earns its management UI** — the moment data can grow, the controls to find/sort/group within it are part of the feature, not an enhancement.
- **Legible data, always** — numeric/metric content (KPI & stat figures, table numbers, dense tabular data) must use a clear, unambiguous face and never get clipped. Decorative display serifs where a single digit reads as a letter (Cormorant "1" → "I") are a defect for *data* — reserve display faces for headings, use a legible/tabular face for metrics. Likewise, controls and values inside table cells must be sized to their content, not truncated to fit.
- **No clipped type** — large/display text must be given a line-height tall enough for its glyphs. NEVER combine `leading-none` (line-height:1) with `truncate` / `overflow:hidden` on a display or serif face: line-height 1 makes the line-box shorter than the font's ascenders/descenders and the overflow clip then shaves the top and bottom of the text. `truncate` is for *horizontal* overflow and only when the line-box already fits the glyph height (use `leading-tight`+ or add vertical padding). (Learned 2026-06-30, wedding-hub: the "Planning Hub" top-bar title was vertically smashed — `leading-none` + `truncate` on the display serif clipped it.)
- **Direct manipulation — obvious logic is the default** — if a value is shown, the expectation is you can act on it where it sits (rename, edit, change status, reorder). Don't make users hunt a separate screen or delete-and-recreate to change something the UI already displays. When a user says "logic things like that should be obvious," it means an expected affordance is missing, not that they want a tutorial.
- **Action hierarchy, not a button row** — chrome must not line up many equal-weight buttons. Per view: at most ONE primary (filled) action; secondary actions stay quiet (ghost/text); rarely-used or destructive utilities (import, reset, download-backup) collapse into an overflow / ▾ menu — never bare in persistent chrome, and a destructive action (Reset / Delete-all) is never always-visible and unguarded. No two visible controls may share an ambiguous label — an "Export" (snapshot) next to "Export CSV" is a defect; name by outcome. Global/admin tools don't belong in per-screen page chrome. **Controls in one group share ONE height and shape** — express hierarchy through fill/variant (primary filled vs secondary ghost), NEVER by shrinking a secondary (no `sm` button beside an `md` primary); a search field and the menu button next to it in the same utility bar must also match height. (Learned 2026-06-26, wedding-hub admin header: 6 equal outline buttons incl. duplicate Export + a bare Reset. Learned 2026-06-30, wedding-hub: Search 36px vs Data 44px in the top bar; Manage-categories `sm` vs Add-contact `md` in the page header — different heights side-by-side read as broken.)
- **Keep contextual action bars reachable** — a selection / bulk-action bar (or any toolbar that appears in response to state) must stay in view (fixed/sticky, e.g. bottom-center), never anchored where it scrolls out of reach. If the user has to scroll to find the action they just enabled by selecting, it's misplaced. (Learned 2026-06-26, wedding-hub guests bulk-action bar.)
- **Surface content, sink empties** — default ordering puts populated/actionable items first and pushes empty / placeholder / zero-state items to the bottom; never interleave empty boards, columns, or rows among full ones. The user shouldn't scroll past blanks to reach real content. (Learned 2026-06-26, wedding-hub inspiration boards.)
- **Consistent iconography** — interactive affordances (nav, row actions, toolbars, empty states) carry icons from ONE icon set per app, used consistently; text-only action cells ("Edit"/"Delete") are weak affordances. Adopt a single modern library (Lucide recommended — MIT, ~1500 tree-shakeable React icons, clean stroke that suits editorial UIs; Phosphor/Tabler are fine alternates) and reuse it — don't hand-roll one-off inline SVGs that drift in weight and style.
- **Restrained elevation** — shadows convey depth, not drama. Keep them soft, low-opacity, and tinted toward the ink/neutral (a warm brown or grey), **not a saturated brand hue**. A burgundy/red-tinted or high-opacity drop shadow reads as heavy ("heady"). One subtle resting shadow, a slightly stronger hover/focal — never stack heavy coloured shadows. (Learned 2026-06-26, wedding-hub: the focal card shadow was burgundy-tinted + heavy → de-tinted to warm-brown and lightened.)
- **One shape language (consistent radius)** — pick a single corner-radius token and apply it coherently. Don't pair fully-rounded pills (radius ∞) with near-square cards — cards, buttons, inputs, and chips should share the same moderate rounded-rectangle radius so the UI reads as one system ("square with rounded corners"). A full-pill capsule is a deliberate, sparing exception (avatars, one tag style), never accidental drift. Radius is part of the [[hearth-works-company]] structural kernel, so this is a kernel-level consistency rule. (Learned 2026-06-26, wedding-hub: rounded pills vs square cards.)

---

## Layer 1 — Trigger table (THE CORE — deterministic, keyed off data shape & artifact type)

Read the data shape first. Each trigger that matches contributes MANDATORY elements to the design.

### T1 — Comparison data (two related quantities for the same row)
**Triggers when** a record holds a planned value AND an actual value — `estimate`/`amount`, `budget`/`spent`, `target`/`current`, `planned`/`actual`, `quoted`/`paid`, `forecast`/`real`.
**Mandatory defaults:**
- Show **both** quantities side by side. Never show one and bury the other.
- Show **variance**: absolute delta **and** percentage, with direction encoded (over = warning color, under/on = positive/neutral). Color is redundant with a sign/label — never color alone.
- A **totals / summary row** that sums each column and the variance. The number people actually want is the rollup.
- Handle the **not-yet-known** state explicitly (TBD / pending invoice) — don't render it as 0 or blank silently; mark it and exclude it from "confirmed" totals (or footnote it).
- Mixed units (currencies, etc.) are never summed raw — convert to one display unit and note the rate, or sum per-unit.

### T2 — Collection that can exceed ~10 items
**Triggers when** a list/table/grid is backed by a collection whose count is user-driven or unbounded (guests, vendors, todos, line items, files…).
**Mandatory defaults:**
- **Search** (text filter) on the primary identifying field.
- **Filter** on every field with low-cardinality values (status, category, owner, paid/unpaid, event). Filters are visible controls, not hidden.
- **Sort** — at least on the columns/values people compare by (amount, date, name, status).
- **Result count** ("24 of 60") and a one-tap **clear filters**.
- **Empty, loading (skeleton), and zero-results** states — zero-results is distinct from empty and must explain *why* (filters too narrow) with a clear-filters action.
- **Default sort/grouping is meaningful**, never insertion order by accident.

### T3 — Categorizable records
**Triggers when** records carry a `category` / `type` / `group` / `event` / `stage` field.
**Mandatory defaults:**
- **Group by that field by default**, with a per-group **subtotal/count** in the group header. When the records carry a status, the header should surface the *actionable* count too (e.g. "3 to contact", "2 booked"), not a bare number alone — a lone count is weak indication. (Learned 2026-06-30, wedding-hub outreach: category headers showed only a bare "7".)
- Collapse/expand per group when groups are many or long — and when **≥2 groups are collapsible, provide a bulk Expand all / Collapse all control** (a set of collapsibles with no bulk toggle is a defect; it's part of "every collection earns its management UI"). (Learned 2026-06-30, wedding-hub outreach: collapsible category drawers had no expand/collapse-all.)
- Offer "group by" as a switchable control if more than one grouping field exists.
- Don't make the user mentally bucket a flat list the system already knows how to bucket.
- **Color-code groups** when grouping is the primary view — a *stable* swatch per group value (hashed so the same group is always the same colour). Keep the at-rest signal **restrained**: a header dot/chip is usually enough to identify the group. Draw group swatches from the app's **own hue family (on-palette)** — don't hash to arbitrary colours that include hues foreign to the brand (e.g. cool blues/teals/plums in a warm parchment palette read as off-system). A persistent full-height row/block colour RAIL tends to read as noise ("meaningless when always on") — prefer revealing the stronger accent on **hover/focus** — and reveal it at the granularity the user is pointing at (the individual **row** on row-hover), not a group-wide flood when the whole section is hovered. Or use a rail only when group boundaries are otherwise unclear. (Learned 2026-06-25→26, wedding-hub guests: kept the per-family header dot at rest; left-spine is per-row hover-only — group-wide hover reveal was too much.)
- **User-defined categories are renameable in place** (editable-taxonomy rule, learned 2026-06-25): if the *user* authored the category/group/label, they MUST be able to rename it — and ideally merge it — directly, never read-only. "Why can't I rename a category?" is a direct-manipulation failure; don't force delete-and-recreate.

### T4 — Navigation (any nav: sidebar, tabs, bottom bar, menu)
**Mandatory defaults:**
- **Text labels always.** Icon-only nav is prohibited (see Layer 0). Icon + label, or label alone.
- **Group destinations by task/domain** when there are more than ~5; add section headers.
- **Active/current state** is unmistakable (weight + color + indicator, not color alone).
- **≤7 top-level destinations**; overflow goes into grouped sub-nav or a "more", not a flat row of 12.
- Every destination label is a real noun/verb a user would say — not internal jargon.

### T5 — Quantity over time / dated records
**Triggers when** records have dates or a value changes over time.
**Mandatory defaults:** sort/segment by time by default; surface "upcoming/overdue/recent" framing where relevant; consider a trend or timeline view, not just a raw table; relative dates ("in 3 days") alongside absolute.

### T6 — Status-bearing records
**Triggers when** records have a lifecycle field (todo/done, paid/unpaid, booked/pending, draft/published).
**Mandatory defaults:** status is **filterable** and **visually encoded** (badge/chip with label + color, never color alone); progress rollup where a set has a completion notion ("12 of 18 booked"); status changeable inline where it's the primary action.
**Rollup completeness rule (learned 2026-06-25, wedding-hub vendors):** a status rollup MUST count **every** value in the status enum, including terminal/negative states (declined, cancelled, archived). Never display a curated subset of counts — a hidden status makes records silently vanish from the totals and the numbers stop reconciling to the list length. If a terminal state is intentionally de-emphasized, still show its count *legibly* (muted ≠ ghosted — `/40` opacity is invisible; keep it readable).
**Editable-status control rule (learned 2026-06-25, wedding-hub vendors):** when status is editable *inside a collection row/cell*, the control must be **tone-coded and consistent with how the same status renders elsewhere** (e.g. the detail view's pill) — never a bare grey `<select>` that clips the value ("de…" for "declined"). Use a tone-colored select sized to its longest option, or a pill that opens the editor on tap. A colored pill in the detail view paired with a truncated dropdown in the table is a consistency + legibility defect.

### T7 — Any data container (baseline, always)
Every container that renders data has all states: **initial/skeleton, populated, empty (with CTA to add the first item), zero-results, refreshing, error (with retry)**. Empty ≠ zero-results ≠ error. (Mage's `ui-patterns-reference.md` has the visual spec for each.)

### T8 — Forms & creation
One column; group related fields; progressive disclosure; inline validation on blur; labels above inputs (never placeholder-as-label); disabled submit until valid; loading state on submit; explicit success/error. (Full spec: `ui-patterns-reference.md`.)

### T9 — Installable app surface (PWA / desktop / store build)
Fires whenever the artifact is installable (web manifest, service worker, PWA scope, Electron/Tauri, store submission). MANDATORY: a complete icon set — favicon (SVG or .ico), app icon(s) at the platform's required sizes, and a maskable icon for the manifest; a themed `theme-color`; and an install-surface identity check (name/short_name match the product). An installable app with a 404 favicon or a default placeholder icon fails this trigger. (Origin: Nourish v1 shipped an installable PWA with NO favicon — caught live 2026-07-01; the gap survived 859 green tests because no trigger owned it.)

---

## Layer 2 — Domain pattern packs (grow this library over time)

Domain-specific expectations that ride on top of Layers 0–1. Add a pack whenever a domain recurs.

- **Budget / finance** → T1 + T3 are mandatory together: line items grouped by category, estimate vs actual + variance per line, subtotal per category, grand total with a confirmed-vs-pending split. Deposit/paid tracking. Per-vendor rollup. (Validated against the wedding-hub budget: `category` + `estimate` + `amount` + `paid`/`paidAmount` + `estimateTbd` is exactly this shape.)
- **Scheduling / events** → T5 + grouping by day; conflict/overlap surfacing; relative + absolute times; timezone clarity for multi-location.
- **People / CRM / guests** → T2 + T6; dedup affordance; bulk actions with selection count; group by household/segment.
- **Outreach / contact capture** (learned 2026-06-26, wedding-hub vendor outreach) → never assume a public email exists. A contact/prospect record must accept **email OR social handle OR inquiry-form URL** — at least one, none individually required — because many businesses (wedding vendors, studios, creators) only take inquiries via forms or DMs. Track an outreach **status** (to-contact / contacted / replied) and render contact methods as the right link type (mailto / IG / external form), not a bare email column.
- _(append new packs here as verticals prove out under Hearth Works)_

---

## How to apply (generator checklist)

1. Look at the **data shape** (the types / seed data), not just the prose ask.
2. List which triggers (T1–T8) fire and which domain pack applies.
3. Treat every fired trigger's defaults as **already in scope** — design them in on the first pass.
4. Defer to `ui-patterns-reference.md` for the *visual* spec of each pattern; this file decides *which patterns are mandatory*, that file decides *how they look*.
5. For anything you intentionally drop, add one line: "Omitted T_x because …".

This is the upstream contract. Mage's knowledge base is the downstream visual detail. Sage gates against this list. Claude Design is seeded from it.
