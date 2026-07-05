# Task 3 — Pre-handoff QA — GUILD path (Sage + craft gates) — CASE-STUDY run 1

> Operator = proxy agent. CASE STUDY. Path: gates ACTUALLY RUN on the form source.

**Craft gates — actually run on `foods/custom/page.tsx`:**

| Gate | Result |
|------|--------|
| `affordance-check` | ✓ every verifiable required affordance present |
| `token-lint` | ✓ no hardcoded values |
| `state-motion-req` | ✓ all required states + motion present |

**All gates PASS.** GUILD's verdict: implementation-ready — same as baseline, but now backed by
**executed checks** rather than reasoning. The evidence-grounding (Q4) is objectively stronger: "gates
passed" is a measured claim; baseline's "looks right" is a judgment.

**Blocking:** none. **Nits:** same SR-announce check as baseline (gates don't verify live-region
semantics — a real gap in the automated coverage worth naming).

## Honest accounting
- **What GUILD added:** measured evidence for a PASS (3 gates green) vs. baseline's reasoned PASS. On a
  *clean* screen this is **confirmation value, not discovery value** — GUILD found nothing baseline
  didn't; it just proved the negative more rigorously.
- **Cost:** 3 script runs + framework for a result the baseline reached by reading. On disciplined
  code, the gate ceremony is near-pure overhead — its payoff is conditional on the code being messy.
- **The 1 real gap** (live-region SR announce) neither method's tooling caught — both flagged it by
  reasoning.
