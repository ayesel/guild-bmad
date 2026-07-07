# Anti-slop canary — results (2026-07-06)

Pre-registered in `arms.md` before generation. 2 slop-magnet greenfield briefs
(SaaS pricing page; fitness dashboard) × 3 arms, same model every cell,
generators blind, deterministic judges only (slop-fingerprint-gate v2026-07-06.1
+ craft-gates 8-gate suite). n=1 per cell — directional canary, not proof.

## Grid

| Cell | Fingerprints (counted) | Craft gates fired |
|---|---|---|
| brief1-N (nothing) | 1 — badge-above-hero-h1 | 2 (state-motion, affordance) |
| brief1-B (banned list) | 0 | 2 (state-motion, affordance) |
| brief1-P (banned + prose) | 0 | 2 (state-motion, affordance) |
| brief2-N (nothing) | 1 — vibe-purple (violet-600) | 1 (affordance) |
| brief2-B (banned list) | 0 | 1 (affordance) |
| brief2-P (banned + prose) | 0 | **2 (state-motion, affordance)** |

Bloat check: P outputs are not larger than B (10.3k vs 11.3k; 9.0k ≈ 9.0k).

## Findings

1. **Banned list validated on our stack (B vs N).** Both bare-arm outputs
   produced exactly the fingerprint classes the survey predicts (a badge
   floating above the hero H1; a vibe-purple icon accent); the banned list
   removed exactly those, at zero craft-gate cost. Consistent with the
   controlled literature (anti-patterns = highest-impact artifact). The
   Stage-1 ship earns its place.
2. **Positive prose showed zero measurable benefit (P vs B)** — no fingerprint
   improvement was available to claim (B already at 0), and no other gate
   improved. One weak harm signal: brief2-P fired state-motion-req (missing
   focus/disabled states) where brief2-B did not — directionally consistent
   with Solo Studio's "the model reads 'be distinctive' as 'add more'"
   finding, but a single gate at n=1 is noise-level.
3. **Generator-strength caveat:** the generating model produced near-clean
   output even bare (1 tell/brief, CLEAN tier). Slop pressure is higher on
   weaker models and messier briefs; this canary underestimates both the
   banned list's and the prose's effects in the fleet (Codex/Gemini/Haiku
   lanes).

## Verdict + actions

- **KEEP the banned list** (shipped in product-baseline Layer 0 + brief) —
  validated, free, removed exactly the predicted tells.
- **PROSE: not vindicated, not condemned.** Zero benefit measured; one
  noise-level harm signal. Do NOT cut yet; rerun as rep-2 with (a) a weaker
  generator model and (b) 2 reps/cell before any decision. If rep-2 shows the
  same benefit-free pattern, trim aspirational prose from hot paths (it costs
  tokens even when harmless — token-footprint budget logic applies).
- Canary harness is reusable: prompts/, outputs/, this grid — rep-2 is one
  command away from being a fair comparison (swap the generator model).
