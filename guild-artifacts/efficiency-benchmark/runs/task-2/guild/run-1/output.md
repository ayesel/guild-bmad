# Task 2 — IA/flow — GUILD path (Cartographer/Rogue + pattern-store) — CASE-STUDY run 1

> Operator = proxy agent. CASE STUDY. Path: IA framework + pattern-store match run for real.

**pattern-store match** — RUN, real hit: returned `slot-list-inline-add` ("Slotted List with Subtotals
and Inline Add") with provenance `nourish:src/app/today/TodaySurface.tsx (shipped)` — the owner's OWN
shipped pattern (per-slot count+subtotal, dashed empty state, accessible "Add to {slot}" buttons,
inline search picker, zero-results). **This is real differentiated value:** it tells the flow to reuse a
proven in-repo pattern for the meal-slot UI instead of inventing one. The plain baseline structurally
CANNOT do this — it has no memory of the owner's shipped work. **Strongest GUILD-only win in the study.**

**Proposed flow:** same spine as baseline (plan → select-mode recipes → derived grocery), plus GUILD
framework additions:
- **Conceptual model made explicit:** PlanEntry is the single source (matches Nourish rule D1 —
  unified PlanEntry, no separate Plan/Log table). Grocery = a *pure projection* over PlanEntry+recipes.
  This grounds the flow in the actual data contract — baseline implied it, GUILD names it.
- **State coverage:** empty (no plan → grocery shows "plan meals to build a list"), partial, stale
  (plan edited after list generated → re-derive banner), manual-merge conflict states enumerated.
- **Nav/wayfinding:** breadcrumb scent plan→grocery both directions.

**Top risks:** same 3 as baseline (aggregation/de-dup, ripple-on-edit, manual vs derived) + a 4th:
**Phase-2 seam discipline** — don't wire FoodTag/RecipeTag (Nourish rule 8 says leave unwritten in MVP);
a naive "filter grocery by tag" flow would violate scope. **GUILD-only catch, grounded in repo rules.**

## Honest accounting
- **Added over baseline:** explicit conceptual-model/data-contract grounding, fuller state coverage,
  the Phase-2 scope catch (real, repo-grounded). ~2–3 genuine additions.
- **Overlap:** the core flow + top-3 risks are identical to baseline.
- **Cost:** framework + pattern-store run + rule cross-referencing = materially more steps.
