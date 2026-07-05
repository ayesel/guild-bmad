# Task 2 — IA/flow (plan→recipes→grocery) — Baseline — CASE-STUDY run 1

> Operator = proxy agent. CASE STUDY. Input: 3 route list + intent paragraph. Timebox 30 min.

**Proposed flow:** `/plan` (week grid, meal slots) → tap a slot → `/recipes` (pick, opens in
select-mode with "add to {day}/{meal}" CTA) → recipe's ingredients auto-append to a derived
grocery list → `/grocery` (grouped by aisle, checkable, shows which meal each item traces to).

**What changes vs today:** (1) recipes gains a "select-for-plan" mode invoked from a slot, vs. today's
standalone browse; (2) grocery becomes a *projection* of planned recipes (derived, not hand-entered) —
one source of truth = the plan; (3) a persistent "week → list" affordance ties the three.

**Top 3 structural risks:** (1) grocery de-dup/aggregation across recipes (2 recipes both need onions →
one line, summed) — needs a merge rule; (2) editing a planned meal must ripple to the grocery list
(stale-list risk); (3) manual grocery additions vs. derived ones need to coexist without the derive
step wiping manual entries.
