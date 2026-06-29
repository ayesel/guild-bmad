# Raid Tournament Mode

**GUILD-13 · P2/autonomy.** Guild's raids already generate parallel candidates —
but they end by making the owner pick. That's a human pass. **Self-score instead.**

## Flow (default for raids)
1. **Generate variants in parallel** — Ranger/Rogue/Mage approaches + Mage's
   divergence batch (GUILD-21), each constrained by the DS grammar (GUILD-22).
2. **Sieve + self-score** — run the Novelty Sieve (GUILD-24): validity floor →
   Fresh+Valid → multi-judge Pareto (Mage/Sage/Tinker), scored against the Raid
   Charter (GUILD-11) acceptance criteria + calibrated QA tiers (GUILD-4).
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
