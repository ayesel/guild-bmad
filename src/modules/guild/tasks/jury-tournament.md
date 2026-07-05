# Jury Tournament (GUILD-40) — pairwise diverse-jury scorer

The judgment keystone. GUILD's generator is fine; the median self-judge was the
bottleneck — it underrated the distinctive candidates the novelty engine produces.
This replaces the holistic self-score with a pairwise, diverse-vendor jury.

Config: `docs/guild/jury.yaml`. Scorer + guards: `scripts/bradley-terry.py`.

## Protocol
1. **Candidates in.** From `/guild-agent-mage DV` (divergence engine — Verbalized Sampling + morphology) and/or
   the GUILD-34 prototype lane. Do NOT merge them (merging regresses to the mean).
2. **Guard the jury.** `validate_jury(jury.yaml)` must pass: ≥3 judges, **disjoint
   vendors**, **generator vendor EXCLUDED** from its own jury, **order-swap on**.
   A failed guard blocks scoring (no silent self-judge).
3. **Pairwise, both orders.** For every candidate pair, each judge compares them
   **twice** — (A,B) and (B,A) — against the **decomposed rubric** (hierarchy /
   spacing / contrast / consistency / affordance / clarity), grounded in the charter +
   bold exemplars. Judges run as Atrium raids (disjoint vendors).
4. **Aggregate.** Feed every verdict to `bradley-terry.py` → strengths → ranking.
   Order-swap cancels position bias (proven: naive single-order corrupts the ranking).
   **Report inter-judge agreement** every time.
5. **Anti-gaming.** Run ONE pointwise pass; flag any candidate whose pointwise rank
   disagrees sharply with its BT rank (pairwise is more gameable under distractors).
6. **Two axes, not one.** The jury gives the QUALITY strength. Pair it with the
   novelty axis and surface a **Pareto front** (rec + bold alternatives) — never one
   scalar (GUILD-41).
7. **Screen, not ship.** The jury narrows options; the owner pick + real signal decide.
   Log owner overrides to the calibration set (GUILD-44).

## Test gate
`python3 scripts/bradley-terry.py --selftest` — proves BT recovers a known ranking
under heavy position bias (order-swap), the naive single-order is corrupted, and the
jury guards reject <3 judges / non-disjoint vendors / generator-on-its-own-jury /
order-swap-off.

## Replaces
The single-model self-score in `tournament.md` (GUILD-13). The tournament's
rec+rejected SHAPE is kept; only the scorer changes (self-score → diverse jury).
