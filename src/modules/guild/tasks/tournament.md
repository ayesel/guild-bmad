# Raid Tournament Mode

**GUILD-13 · P2/autonomy.** Guild's raids already generate parallel candidates —
but they end by making the owner pick. **Score with a diverse-vendor jury instead**
(GUILD-40) — the old single-model self-score was the bottleneck: it underrated the
distinctive candidates the novelty engine produces (median bias).

## Flow (default for raids)
1. **Generate variants in parallel** — Ranger/Rogue/Mage approaches + Mage's
   divergence batch (GUILD-21), each constrained by the DS grammar (GUILD-22).
2. **Sieve, then diverse-jury score** — run the Novelty Sieve (GUILD-24) validity
   floor first, then score survivors with the **pairwise diverse-vendor jury**
   (GUILD-40 / `jury-tournament.md` / `scripts/bradley-terry.py`): ≥3 disjoint-vendor
   judges, **generator excluded**, both orders (order-swap), **Bradley-Terry**
   aggregated, against the decomposed rubric + Raid Charter (GUILD-11) + calibrated QA
   tiers (GUILD-4). The Mage/Sage/Tinker personas remain DIVERSITY/routing lenses, NOT
   the correctness judges (persona ≠ correctness). Surface quality × novelty as a
   Pareto front (GUILD-41), never one scalar.
3. **Synthesize ONE recommendation** — Guild Master returns the winner + the
   rejected alternatives each with a one-line reason.
4. **Owner sees the final slate ONCE** — in the GUILD-11 batched review, not each
   half-baked draft. Adjudication is **optional**, never required to proceed.

## Keep (from GUILD-9, passive)
Replay / trace of the tournament is recorded for audit — useful, not a gate.
Explicit human voting becomes **opt-in**, not required.

## Done when
- Variants generate in parallel; an automated rubric scores them against charter + QA tiers.
- Guild Master returns one recommendation + rejected alternatives + rationale.
- Owner adjudication is optional, not required to proceed.
- TEST: a high-ambiguity decision returns 1 rec + alternates + rejected-with-reason, with no forced human pick.
