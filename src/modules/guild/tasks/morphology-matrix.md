# Morphology Matrix + Design-System Grammar

**GUILD-22 · P2 novelty.** "Enumerate a design space, then sample it systematically"
beats "be creative" — and standards work as a GENERATIVE GRAMMAR (vary the allowed
axes), not prose applied after the fact. Depends on GUILD-1/16 (tokens).

## Two linked pieces
1. **Component Morphology Matrix** (`docs/guild/morphology-matrix.yaml`) — per component class: the invariant function (the locked contract) + variant axes with discrete legal values (information-shape × interaction × density × feedback × metaphor × a11y-mode). Mage samples **far-apart cells** (GUILD-21 lane 3), not adjacent variants.
2. **Design-System Grammar** (`docs/guild/ds-grammar.yaml`, **Tinker-owned, machine-readable**) — allowed components, anatomy, required roles/states, variant axes, token constraints, responsive rules, motion limits, a11y invariants, do/don't. Generation draws only from legal values; candidates are checked back against the same grammar.

## Novelty-safe zones
Reuse `docs/guild/novelty-zones.yaml` (GUILD-23): high (visual treatment, layout, empty states, motion, grouping metaphors), moderate (secondary nav, filtering, dashboards, card anatomy), low (forms, auth, destructive, checkout, core keyboard, error recovery, a11y).

## Who
- **Rogue** sets the invariant (locked contract) per component.
- **Tinker** maintains `ds-grammar.yaml` (the legal space) + keeps it in sync with tokens.
- **Mage** generates from legal axis values (GUILD-21); **Sage** checks candidates against the grammar (GUILD-24).

## Done when
- Matrix schema (axes + legal values) defined per component class.
- DS Grammar is machine-readable + Tinker-maintained.
- Novelty-safe zones classified per surface.
- TEST: distinct cells exist; the grammar lists legal tokens/components; a candidate can be validated against it.
