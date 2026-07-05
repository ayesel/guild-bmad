# Task 1 — Baseline (manual AI, no Guild) — CASE-STUDY run 1

> **Operator = autonomous agent (proxy), not human.** This is a CASE STUDY, not proof. Operator-attention
> is proxied by operator decision-points (see logs). Quality scored by the same agent that knows the
> source → treat as *suggestive, not clean* (rubric blinding clause).
> **Input:** `today-1440.png` + `today-390.png` (populated `/today`). **Prompt:** "Critique this screen's
> UX. Prioritized, with concrete fixes." **Timebox:** 20 min.

## Prioritized critique

1. **Massive wasted space on desktop; the layout is a phone column stranded in a 1440 viewport.** The
   content sits in a ~448px centered column with huge empty margins L/R. *Why:* desktop users get a
   lonely strip; the screen doesn't use the canvas. *Fix:* at ≥768 introduce a 2-col layout (rings left,
   entry list / quick-add right) or cap-and-center with a purposeful side panel.

2. **The primary job of the screen — logging — has no obvious entry point.** Header says "0 ENTRIES
   LOGGED" but there's no visible "Add food / Log meal" button above the fold. *Why:* the one action the
   user came to do is missing/hidden. *Fix:* a persistent primary "Log food" CTA (FAB on mobile, header
   button on desktop).

3. **Calorie data is duplicated.** "2100 kcal remaining" appears in the ring AND again as a "REMAINING
   2100 kcal / of 2100 target" card below; protein shows "0/160 g" in its ring and again as "PROTEIN
   LEFT 160 g / of 160 target." *Why:* the same number twice = visual noise and scroll cost. *Fix:*
   drop the redundant cards, or make them a different cut (e.g. trend), not a restatement.

4. **"Room to spare" printed four times** (calorie ring + each of 3 macro rings). *Why:* repeated filler
   copy adds weight and says nothing incremental. *Fix:* show it once (or only when a value is near/over
   target); at 0-logged it's noise.

5. **"Today" appears twice** — the h1 and the centered date-nav pill both say "Today." *Why:* redundant;
   the h1 wastes the most prominent slot. *Fix:* h1 could carry the date ("Thursday, Jul 4") and the nav
   pill stays "Today," or vice-versa.

6. **Orphan "N" avatar floats bottom-left** with no clear affordance or grouping. *Why:* reads as debug
   cruft / misplaced profile chip. *Fix:* move into a header/profile slot or a proper nav bar.

7. **Rings at 0 with a filled leading dot may read as "1% done / stuck," not empty.** *Why:* ambiguous
   0-state. *Fix:* render the track only (no progress dot) until value > 0, plus the existing text.

8. **Mobile (390): macro card subtitles wrap to 3 lines** ("0 / 160 g · Room to spare"), crowding the
   3-up. *Why:* cramped, uneven card heights. *Fix:* shorten to "0 / 160 g" under the ring; drop the
   "Room to spare" tail on mobile.

## Self-flagged
- No design-system-token audit performed (not asked). a11y: rings need verified text alternatives —
  present as subtitle text, looks OK, not contrast-measured here.
