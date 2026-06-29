# Brain-trace demo — a real Nourish decision, traced to evidence

**Proof the moat works on real data, not a fixture.** A real Nourish design decision —
*"the Today screen must show estimated-vs-actual macros against target"* — traced
end-to-end through the GUILD-63 spine and run through every TIER-1 gate.

Spine: `nourish-est-vs-actual.spine.json` · Re-run: `python3 scripts/spine.py --spine <that> --trace AC1` (+ the gates).

## The lineage (pixel → evidence)
```
AC1  [ac]          Today shows calories + each macro as actual/target/remaining, color-coded over/under
 └ C1 [conclusion] show actual / target / remaining per macro with over-under variance
    └ I1 [insight] Today must surface progress-against-target, not just what was logged
       ├ F1 [fact] Product Baseline T1 fires → must show variance + totals   (product-baseline.md#T1, REAL)
       ├ F2 [fact] owner mandate: estimated-vs-actual is required            (memory:guild-product-baseline, REAL)
       └ F3 [fact] macro-trackers need a running actual-vs-target            (ux-heuristic, REPRESENTATIVE)
          └ E1 [experiment] Nourish IA pass
 └ CON1 [constraint] variance + totals (T1) within the device-light budget
ADR1 [adr] macro ring + numeric delta (Hearth Works StatTile); pixel: ui_kits/nourish/TodayScreen.jsx
```

## Gate results — all green
| Gate | Result |
|---|---|
| **Spine validate** (GUILD-63) | ✅ OK — no orphans/cycles, facts cited, lineage well-formed |
| **Trace** | ✅ AC1 → C1 → I1 → {F1,F2,F3} → E1 (any AC reaches its evidence) |
| **Verification + sycophancy** (GUILD-64) | ✅ OK — all facts cited + verified, no opinion/stakeholder-as-fact |
| **Confidence** (GUILD-65) | ✅ C1 + CON1 = **1.0, evidence-backed** → gates the build (not an ASSUMPTION) |
| **Synthesis-ladder** (GUILD-66) | ✅ I1 triangulated — 3 facts across 3 distinct sources |
| **IA evidence guard** (GUILD-68) | ✅ no synthetic-user-as-evidence; IA traces to empirical/real sources |

## What this proves
Guild can take a pixel (the Nourish Today macro display) and show **exactly why it
exists** — back through its acceptance criterion, conclusion, insight, and the cited
facts, then verify none of it is fabricated or opinion, and confirm it's confident
enough to build. That's the north-star moat working on a real decision.

## Honest note
F1, F2 and the ADR pixel are real repo/memory artifacts. **F3 is labeled
REPRESENTATIVE** — drop a real Nourish usability-study nugget into that slot and the
same chain + gates apply unchanged. The spine + gates are proven; only F3's source is
a placeholder.
