# Iconography Reference

Icon & mark-system craft: keyline grids, stroke/corner standards, optical consistency, handoff.

> **⚠ GROUNDING STATUS — MOSTLY PENDING EXPERT REVIEW.** Only the base-sizing rule below survived adversarial verification. The keyline/optical-correction craft was not verifiable to the project's citation bar (and one specific formula was *refuted* — flagged inline). Treat `[PENDING REVIEW]` items as practitioner consensus for **your** sign-off as the domain expert.

## Base Sizing & Grid  ✅ VERIFIED

- **Build icons on the design system's grid increment.** With an 8-grid, build at **16 / 24 / 32px**. (designsystems.com; corroborated by Material's 24×24.)
- **Pick one common build size, let engineering scale it.** Don't hand-draw every size — author at the canonical size, scale at render.

## Keyline Grid & Live Area  `[PENDING REVIEW]`

- `[PENDING REVIEW]` Inside the icon canvas, a **keyline grid** defines a *live area* (the safe drawing region) plus **padding/trim** so icons don't touch the edges and read at a consistent visual weight.
- `[PENDING REVIEW]` Standard keyline shapes (square, circle, vertical/horizontal rectangle) give different glyph footprints a **consistent optical size** — a circle glyph fills the circle keyline, a square glyph the square keyline, so a "full" icon and a "round" icon look the same size.

## Optical Consistency  `[PENDING REVIEW]` / ⚠ one rule REFUTED

- `[PENDING REVIEW]` General principle (sound): **curved/circular glyphs optically read smaller than squares**, so round forms are drawn slightly larger to balance perceived weight.
- ⚠ **REFUTED — do not encode as a rule:** the specific formula "*intrinsic edge padding equal to the stroke weight (or double for a 1px stroke)*" did **not** survive verification (1-2). The *principle* of optical balancing is real; this exact measurement is not established. Flag for expert judgment.

## Stroke & Corner Standards  `[PENDING REVIEW]`

- `[PENDING REVIEW]` Fix a **single stroke weight** across the set at the build size (e.g. 2px at 24px), and a **consistent corner radius** — these two choices carry most of an icon set's visual cohesion.
- `[PENDING REVIEW]` Standardize **terminals and joins** (how strokes end and meet) — rounded vs. butt caps, consistent join treatment — or the set looks like it came from multiple hands.

## Consistency & Handoff  `[PENDING REVIEW]`

- `[PENDING REVIEW]` Keep the set **named and organized** with a consistent convention (category/name/size) so icons are findable and unambiguous at handoff.
- `[PENDING REVIEW]` Ship as components/variants with the grid + stroke + radius rules documented, so new icons added later stay on-system.

---

### Sources
- **Verified:** designsystems.com iconography guide; Material icon grid (24×24)
- **Pending (craft):** designproject.io icon grids & keylines; nikitisza.com icon design
- **Refuted (excluded):** the stroke-weight-padding optical formula
