# Convention Lock + Expression Layer

**GUILD-23 · P2 novelty.** Resolves the novelty-vs-usability tension by ALLOCATING
it: lock the interaction contract, free the expression. Generic output and
unusable "creative" output are both failures — this routes novelty to where it
delights and bans it where it hurts.

## Rule
Every component spec splits two layers (taxonomy in `docs/guild/novelty-zones.yaml`):
- **LOCKED (Convention)** — role, keyboard model, focus order, input/output contract, error recovery, labeling, responsive collapse, states, a11y semantics. **Generation may NEVER vary these.**
- **FLEXIBLE (Expression)** — visual metaphor, spatial grouping, density, progressive disclosure, motion style, hierarchy, microcopy voice, surface treatment. Mage explores here.

## Who does what
- **Rogue** locks the interaction contract (the LOCKED fields) in the component spec.
- **Mage** explores expression within FLEXIBLE only (GUILD-21 divergence).
- **Tinker/Sage** gate implementation; Sage applies the **−0.50** penalty (GUILD-24) when a candidate's novelty lands in a locked zone.

## Surface defaults
Core interactions — forms, auth, destructive actions, checkout — default **convention-first** (zone: low). Expressive surfaces — visual treatment, layout, empty states, motion, grouping metaphors — are **high-novelty** zones.

## Done when
- Every component spec declares its Locked vs Flexible fields.
- Generation is forbidden from varying Locked fields; a violation is penalized/rejected in GUILD-24 scoring.
- TEST: a spec marks locked vs flexible; a candidate that varies a locked field is rejected.
