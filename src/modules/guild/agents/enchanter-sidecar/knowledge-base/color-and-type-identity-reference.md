# Color & Type Identity Reference

Brand color and typography craft, plus the accessibility floor that brand assets must clear. Color/type *roles* and token encoding live in `brand-system-and-handoff-reference`.

## Typography — Selection & Pairing

- **Exhaust the primary family before adding a secondary.** Add a second typeface *only* when the primary genuinely cannot do the job — missing weights/italics, missing language coverage, or a context/personality the primary can't carry. (Google Fonts)
- **Pairing = balance distinction and harmony.** Faces should not compete so much they clash, nor be so similar they're indistinguishable.
- **Judge complementarity by shared structure + mood** — x-height, stroke contrast, width, plus mood/style (Hische's relatedness model):
  - **Siblings** (share x-height/contrast/width/mood) → many can pair safely.
  - **Cousins** (share 2–3 traits) → pair 2–3 carefully.
  - **Distant relatives** (share ~1 trait) → pair only 1; high risk.
- **Reliable default heuristic:** a serif + a sans "nearly guarantees sufficient variation" — but it still needs calibration (it's a starting point, not a finished pairing).

## Typography — Type Scale

- Use a **modular scale** (a ratio applied stepwise) for a coherent hierarchy rather than arbitrary sizes. Pick the ratio from the brand's personality (tighter ratio = calmer, larger ratio = more dramatic).

## Typography — Licensing (load-bearing, frequently missed)

- **Font licenses are split by usage and are NOT interchangeable** (Monotype):
  - **Desktop** license = print/InDesign use; **cannot** embed web fonts.
  - **Web** license = embedding via CSS `@font-face`; required for sites.
  - **Application** license = embedding in phone/tablet apps and SaaS products — a *separate* license again.
- A brand shipping a website + an app + print collateral typically needs **all three**. The Enchanter must surface licensing as a deliverable, not assume one license covers every surface.

## Color — Accessibility Floor (non-negotiable)

- **Contrast minimums (WCAG):**
  - AA: **4.5:1** normal text, **3:1** large text.
  - AAA: **7:1** normal, **4.5:1** large.
  - Large text = **18pt (~24px), or 14pt bold (~18.67px)** and up.
  - **UI components & graphical objects: 3:1** against adjacent colors (SC 1.4.11).
- **Color is never the sole carrier of meaning** (SC 1.4.1). Pair color with text, icon, or pattern. Test in grayscale — does it still make sense?
- **Logotype exemption:** WCAG explicitly **exempts text that is part of a logo or brand name** from contrast minimums. The brand mark is not held to body-text contrast — but anything functional around it is. Record this so a contrast gate doesn't false-flag the logo.

## Non-Color-Dependent Identity

- A brand mark should stay identifiable in **monochrome** — design it to work in one color first, add color second. This is both an accessibility property and a durability property (favicons, embossing, fax-grade reproduction).

---

### Sources
- Google Fonts — Pairing typefaces (primary)
- Monotype — Font licensing explained (primary); corroborated by Process Type Foundry, Adobe Fonts
- WebAIM / W3C WCAG SC 1.4.3, 1.4.6, 1.4.11, 1.4.1; Section 508; UCLA Brand — color & type accessibility (primary)
