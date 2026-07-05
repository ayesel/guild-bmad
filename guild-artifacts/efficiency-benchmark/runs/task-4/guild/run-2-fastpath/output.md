# Task 4 — ADVERSARIAL 2-min glance — GUILD path WITH FIX #1 (fast-path) — run-2

> Re-run after shipping GUILD-21b FAST-PATH into `mage.agent.yaml` + compiled `mage.md` + global install.
> Same caveats (proxy-operator, case study). This demonstrates the **contract-defined** behavior of the
> new fast-path rule and re-measures Task 4 against it.

**The question:** "In 2 min, the single most important thing wrong with this screen? One answer."

**Trigger check:** ask contains "in 2 min" + "single … one answer" → matches GUILD-21b scope words
(`in N minutes`, `one thing`) → **FAST-PATH FIRES.** Divergence Engine + craft-gate suite skipped; no
KB files loaded.

**Answer:**
> The screen's primary job — logging food — has no visible entry point. It says "0 ENTRIES LOGGED" but
> offers no "Add / Log food" action above the fold.
> **Fix:** add a persistent primary "Log food" control (FAB on mobile, header button on desktop).
>
> ⚡ fast-path — divergence + craft gates skipped; ask for a full pass to run them.

**Format compliance:** ✓ single answer + one fix + the honest skip-log line.

## Before → after fix #1 (Task 4)

| metric | v1 GUILD (no fast-path) | v2 GUILD (fast-path) | baseline |
|--------|------------------------|----------------------|----------|
| attention-proxy | 7 | **~2** (summon + glance) | 1 |
| interventions | 1 (had to suppress pipeline) | **0** | 0 |
| format compliance | ✗ (essay) | **✓** | ✓ |
| quality | 1.5 | **~3.8** (nails the brief) | 4.0 |
| usable? | **n** | **y** | y |

## Win-rule read — HONEST, two ways
The result depends on whether you count the irreducible "summon the agent" step:
- **Counting summon (attention 2 vs baseline 1 = 2×):** still a narrow LOSS under the strict rule — but
  for a *legitimate* reason (invoking any agent is ≥1 step more than a plain prompt), not the old
  catastrophic ceremony.
- **In agent-fronted context (already talking to Mage → attention ~1, parity):** quality ≥ baseline AND
  attention ≤ baseline → **WIN** (clause 1).

Either way, fix #1 converts Task 4 from a **decisive loss** (7× attention, format-fail, forced
intervention, unusable) into a **near-parity / marginal** result. That is the intended effect.

## Honest correction to the earlier report
The v1 report claimed fix #1 "would also flip Task 2." That was wrong — Task 2 (IA/flow) is NOT a
quick single-answer ask, so the fast-path correctly does NOT fire on it. Task 2 needs **fix #2
(conditional gates)**, not fix #1. Corrected in the report's next-fix section.
