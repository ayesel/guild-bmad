# Task 1 — GUILD path (Mage / CR critique) — CALIBRATION RUN

> **CALIBRATION ONLY — not a scored data point.** Same limitations as the baseline calibration:
> source-only (no live 3-viewport Playwright capture), produced autonomously so operator-attention ≈ 0
> is NOT a valid attention measurement. What this DOES capture honestly: the **coverage delta** vs.
> baseline and the **objective ceremony cost** the GUILD path demands (logged below).

**Method:** Mage agent (`guild-critique` → mage.md → CR menu item). **Surface:** `/today` cold-start.

## Ceremony cost incurred to produce this (objective, autonomously countable)

| Step the GUILD path required | Baseline equivalent |
|------------------------------|---------------------|
| Load mage.md persona (130 lines) | none |
| Load 6 sidecar KB files (visual/ui-patterns/a11y/design-principles/micro-interactions/safe-coding) | none |
| Check greenfield/brownfield project state | none |
| Divergence engine (GUILD-21, never single-shot) | none |
| Product-baseline trigger table load + apply | none |
| 8 craft-gate scripts mandated before "GO" | none |
| 3-viewport Playwright capture mandated | none |
| **Then** report | single plain prompt → report |

**Observation for the report:** the GUILD path's floor is ~7–8 file loads + ~8 script runs before its
first finding; the baseline's floor is one prompt. If any of that requires an operator prompt/confirm,
each is a logged intervention. This is the core thing the benchmark measures — recorded here as the
first live signal (calibration-grade).

## Critique (Mage 9-area framework)

**1. UI patterns** — Cold-start uses hero + CTA card + meal-slot scaffold. The scaffold pattern (show
the day's shape before data) is a *good* pattern choice; the risk is the slots reading as interactive
(see states). Product-baseline T-anti-empty: cold-start correctly avoids a bare headline. ✓

**2. Accessibility** — Meal-slot cards are `div`s with a visual `+` (`aria-hidden`) and text; they look
tappable but expose no role/label. SR users get no operable target; if they're meant to be actionable,
they must be `button`s with labels. **Blocking a11y finding.** (Baseline caught this too — #5.)

**3. Visual hierarchy** — Three attention magnets compete: hero rings, "Set up a profile" CTA, and 4
slot cards at `elevation="raised"`. The one available action (profile setup) does not clearly win.
*Fix:* demote slots (lower elevation/opacity) in cold-start so the CTA is the single focal point.
(Overlaps baseline #1.)

**4. Spacing/rhythm** — Uses token scale (`--space-*`) consistently; `gap-[var(--space-6)]` column
rhythm is fine. No raw px. ✓ (token-lint would pass — but NOTE: not actually run in calibration.)

**5. Typography** — h1 "Today" is the largest text but least useful word on a cold screen; eyebrow+title
SectionHeaders are consistent. *Fix:* cold-start subhead stating what Today becomes. (Overlaps baseline #4.)

**6. Color** — Rings render at 0/no-target; risk of reading as broken. *Fix:* caption clarifying the
0-state. (Overlaps baseline #3.)

**7. States coverage** — Cold-start (no profile) is handled; but the slots have no
default/empty/loading/error distinction and imply an add-state that doesn't exist yet. **Missing-state
finding.** (Partially overlaps baseline #2 affordance-lie.)

**8. Platform compliance** — Touch targets: the `size-[var(--space-8)]` (~32px) `+` glyph is decorative,
but if slots become buttons the target must be ≥44dp. Flag for the interactive version. **[Needs live
render to confirm dp.]**

**9. Interaction quality** — No feedback defined for the (false) slot affordance. If non-interactive,
remove the affordance; if interactive, route to profile setup with press feedback.

## Honest accounting for the report (do not hide)
- **Coverage delta:** GUILD covered platform touch-targets (#8) + explicit states audit (#7) that the
  baseline did NOT — real added coverage from the framework. This is a point FOR GUILD on quality.
- **Overlap:** findings 2,3,5,6 substantially duplicate baseline findings 5,1,4,3 — same core issues.
  The framework added breadth, not a different core diagnosis.
- **Unverified claims:** items 4 and 8 assert gate/dp outcomes that were NOT actually measured in
  calibration (scripts + live render not run) — these are exactly the evidence-grounding failures the
  rubric Q4 penalizes. In a real run the scripts must actually run or the claim is a false "checked."
- **Ceremony:** materially higher than baseline (table above) — the attention cost the headline weighs.
