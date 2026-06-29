# Novelty Sieve + Fresh/Valid Scoring

**GUILD-24 · P2 novelty.** Measuring diversity is useless if the UI is broken.
Score novelty ONLY among candidates that already pass quality — otherwise the
system rewards weird-but-unusable artifacts. Extends GUILD-13 (tournament) +
GUILD-4 (QA gate); consumes GUILD-21's candidate batch.

## Sieve (runs right after divergence, before any novelty scoring)
For each candidate, in order:
1. **DS-grammar check** — legal per `docs/guild/ds-grammar.yaml`.
2. **WCAG / component a11y** — deterministic tier (`qa-tiers.yaml`).
3. **Usability-convention check** — honors locked fields (`novelty-zones.yaml`).
4. **Component-API feasibility** — implementable with the real DS components.
5. **Repair 1–2 rounds** — fix in place if close.
6. **DISCARD if still invalid** — no hand-waving; an invalid candidate is never scored.

## Two-stage scoring on survivors (`docs/guild/scoring.yaml`)
1. **Validity floor** (pass/fail): WCAG, DS tokens, component API, state coverage, responsiveness, convention fit.
2. **Fresh+Valid rank:** `0.35·Novelty + 0.25·Usefulness + 0.20·BrandFit + 0.20·Feasibility`; **−0.25** if too close to a `baseline-patterns.yaml` generic; **−0.50** if novelty lands in a locked zone.

**Novelty signal** = embedding/structural distance from the baseline pattern library + effective semantic diversity across the surviving pool.

## Multi-judge Pareto selection
Mage-judge (distinctiveness/memorability) + Sage-judge (standards/usability risk) + Tinker-judge (feasibility). Winner must be **Pareto-good**, not best-average. **No candidate is selectable on novelty alone.**

## Novelty memory
Penalize structures GUILD keeps approving (`baseline-patterns.yaml` novelty_memory) so future raids don't re-converge on the same "fresh" answer.

## Done when
- Validity floor blocks any candidate before novelty is scored.
- Baseline library exists; anti-generic + locked-zone penalties applied.
- Multi-judge Pareto selection (no single judge dominates).
- TEST: an invalid candidate is discarded before novelty scoring; the winner is fresh AND valid.
