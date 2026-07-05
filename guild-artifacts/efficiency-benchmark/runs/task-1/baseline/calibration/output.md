# Task 1 — Baseline (manual AI, no Guild) — CALIBRATION RUN

> **CALIBRATION ONLY — not a scored data point.** Purpose: prove the harness produces a real,
> gradeable artifact. Limitations vs. a real run: (1) input was the **source file**, not a live
> rendered screenshot at 1440/390 — so responsive/visual findings are inferred from markup, not seen;
> (2) produced autonomously, so operator-attention ≈ 0 and is **not** a valid attention measurement.
> The real run must use a live render and a human operator.

**Method:** same model, plain prompt — "Critique this screen's UX. Prioritized, with concrete fixes.
No Guild commands." · **Surface:** `/today` cold-start branch (no active profile).

## Prioritized critique

1. **Two competing "get started" signals compete for the primary action.** The cold-start shows a
   rich hero (calorie + macro rings at 0) AND a "Set up a profile" CTA card AND four meal-slot cards
   that each look tappable (`+` affordance, "Ready when you are"). *Why it matters:* the one thing the
   user CAN do is set up a profile, but the meal slots imply they can log now — they can't. *Fix:* mute
   the meal-slot cards (reduce elevation/opacity) until a profile exists, or make the CTA visually
   dominant so there's one obvious next step.

2. **Meal slots are affordance-lying.** Each slot renders a `+` and "Ready when you are," which reads
   as "tap to add" — but in cold-start there's no profile to log against. *Why:* false affordance =
   dead taps = erodes trust on first run. *Fix:* remove the `+` in cold-start, or wire the tap to route
   into profile setup so the affordance is honest.

3. **The hero rings at 0 with no target may read as "broken/empty," not "designed."** Rings at 0/no
   target can look like a failed load. *Why:* first impression risk. *Fix:* add a one-line caption under
   the ring ("Your targets appear once you set up a profile") so 0-state reads intentional.

4. **Heading hierarchy is thin.** `h1 "Today"` then multiple `h2`s ("Set up a profile", "Your day")
   with an eyebrow system — on a cold screen the h1 "Today" is the least useful word. *Why:* the most
   prominent text isn't the most useful. *Fix:* consider a cold-start-specific h1 or a subhead that
   states what Today will become.

5. **Accessibility: the `+` is `aria-hidden` but the card has no actionable role/label.** Slots are
   `div`s that look interactive but aren't buttons/links. *Why:* SR users get a visual-only affordance
   with no operable target; sighted users get a hover/tap that does nothing. *Fix:* if non-interactive
   in cold-start, ensure they don't read as controls; if interactive, make them real buttons with labels.

6. **Responsive (inferred from markup, not seen): fixed `max-w-md` + 3-col macro grid.** At 390 the
   3-up macro rings (size 92) in `grid-cols-3` may crowd. *Why:* mobile is the primary width. *Fix:*
   verify the 3-up rings don't clip labels < 360; consider 3-up→wrap. **[NEEDS LIVE RENDER TO CONFIRM]**

7. **Copy: "Ready when you are" on four identical slots is repetitive filler.** *Why:* four identical
   subtitles add visual weight without information. *Fix:* drop the subtitle in cold-start, or vary it.

## Self-flagged limitations
- Findings 6 marked as needing live render — honest gap, not a confident claim.
- No design-system-token compliance check performed (baseline plain prompt wasn't asked for it) —
  this is exactly the coverage gap GUILD's gates should fill if they earn their keep (see Task 3).
