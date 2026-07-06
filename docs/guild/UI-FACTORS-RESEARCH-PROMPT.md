# GUILD UI-FACTORS RESEARCH (v1 — 2026-07-05)

The prompt that maps the FULL factor-space of superb UI — everything an AI must
consider (and, wherever possible, MEASURE) to design and audit interfaces at the
level of a top-tier human designer. Paste into a deep-research session (or run as
an adversarially-verified multi-agent workflow like the one that produced
`docs/guild/decisions/ui-mental-model-research.md`). Output lands at
`docs/guild/decisions/ui-factors-research.md`; its verdict becomes the spec for
the next generation of Mage/Sage audit gates.

---

## THE QUESTION

**What is the complete set of factors an AI needs to consider to create a superb
UI — and for each factor, how can an AI with DOM access, computed styles, and
screenshots verify it programmatically?**

Not "what makes good design" as prose. The deliverable is an *operational factor
taxonomy*: every factor carries evidence, a machine-measurable proxy, threshold
values, and a check tier. The end state is an audit spec Guild can wire into
gates the way it wired contrast and responsive scanning.

## WHY (the motivating case — calibrate against this)

Guild's Mage agent audits real UIs with measured sweeps. The audit evolved one
embarrassment at a time, each round passing while the owner still saw problems
instantly:

1. **Round 1:** raw contrast strings → wrong (rgba treated as opaque). Fixed with
   alpha-composited contrast, walking gradients to the worst stop.
2. **Round 2:** contrast clean → layout still broke at ~1100px. Fixed by auditing
   at multiple widths *including the awkward 900–1200 band*.
3. **Round 3 (2026-07-05):** contrast + target-size + overflow all passed, zero
   AA failures — and the owner said "there are clear issues with the sidebars,
   you should recognize that without me saying anything." The issues were all
   **geometric**: a collapse toggle overlapping a panel corner by 6px, one nav
   row wrapping to 54px in a 40px rhythm, card-in-card-in-panel nesting, ragged
   content-start lines across panes (107/91/105px).

Pattern: each round, the *measurable* audit was necessary but not sufficient,
and the missing dimension was knowable in advance. This research exists to stop
discovering dimensions one round at a time. Assume there are MORE dimensions we
have not hit yet; your job is to enumerate the space.

## ALREADY KNOWN (baseline — do not re-derive; extend past it)

Guild already measures: alpha-composited WCAG 2.2 AA contrast (gradient
worst-stop); target sizes (2.5.8, 24px min / 44px touch); horizontal overflow at
multiple widths; type-ramp discipline (whole-px, bounded scale); spacing-scale
conformance (4/8/12/16/24/32/48); token drift (stale hex literals vs tokens);
reduced-motion presence; and — new this round — geometry (sibling-rect overlap,
row-height rhythm outliers, content-start alignment across panes, border-nesting
depth ≥3). Mental-model/IA factors (Jakob's law, recognition-over-recall,
delegated-work inbox) are already researched and shipped — reference
`ui-mental-model-research.md`, do not repeat it. Your scope is the *rendered
surface*: what makes the pixels themselves superb.

## THE FACTOR SPACE (starting scaffold — extend, reorganize, and prune with evidence)

Cover at least these dimensions; add any the literature shows we're missing:

1. **Visual hierarchy** — scan order, size/weight/contrast deltas between levels,
   saliency (would a squint test / blur pass find the primary action first?).
2. **Typography craft** — line length (measure), line-height ratios, modular
   scale ratios, weight pairing, letterspacing at small sizes, widows/rag.
3. **Spacing & proximity** — Gestalt grouping (related closer than unrelated —
   is intra-group gap < inter-group gap, measurably?), whitespace ratios,
   padding symmetry.
4. **Alignment & grids** — count of distinct left-edge x-positions per region,
   optical vs mathematical alignment (icons, quotes), baseline rhythm.
5. **Color systems** — semantic role coverage, state-color derivation, hue
   harmony, neutrals temperature consistency, dark-mode parity.
6. **Gestalt principles as measurable proxies** — proximity, similarity,
   common-region, continuity; which have DOM-computable analogs?
7. **Density & information design** — data-ink ratio, progressive disclosure,
   choice count vs Hick's law, table/label scannability.
8. **Affordance & signifiers** — the two-way audit: things that look clickable
   but aren't, things that are clickable but don't look it.
9. **State completeness** — hover/focus/active/disabled/loading/empty/error/
   skeleton per interactive component; the state-matrix as a coverage check.
10. **Motion** — duration/easing norms, purpose taxonomy, interruptibility,
    reduced-motion, when motion *hurts*.
11. **Accessibility beyond contrast** — focus order vs visual order, visible
    focus indicators, keyboard reachability, landmark/heading structure, the
    screen-reader narrative as a coherence test.
12. **Responsiveness** — breakpoint coverage strategy, reflow-not-truncate,
    the awkward mid-bands, pointer vs touch affordances.
13. **Microcopy & content shape** — label clarity, error-message quality,
    empty-state guidance, front-loaded scannable text.
14. **Consistency & craft polish** — corner-radius vocabulary size, shadow
    coherence (single light source), border weight vocabulary, icon optical
    sizing, the measurable difference between "polished" and "template."
15. **Perceived performance** — 0.1/1/10s thresholds, skeletons vs spinners,
    optimistic UI, honest progress.
16. **Aesthetic-usability effect & emotional design** — how much do aesthetics
    causally matter, per actual studies? Visceral/behavioral/reflective tiers.
17. **Trust & honesty** — provenance visibility, indicator honesty, dark-pattern
    avoidance as a checkable list.

## PER-FACTOR CONTRACT (every factor in the output carries ALL five)

- **(a) Evidence** — primary sources with verbatim quotes (NN/g, WCAG, Apple HIG,
  Material, IBM Carbon, Shopify Polaris, Refactoring UI, Butterick's Practical
  Typography, Tufte, Norman, peer-reviewed studies). Blog-post-only claims get
  flagged as weak.
- **(b) Machine proxy** — the concrete computation an AI with DOM + computed
  styles + screenshots can run (e.g., "rhythm outlier = any list row whose
  height deviates >20% from the modal row height"). If no proxy exists, say so
  explicitly — that is a finding, not a gap to paper over.
- **(c) Thresholds** — numeric pass/flag values with their source, or "no
  agreed threshold" stated plainly.
- **(d) Check tier** — MEASURE (deterministic, gateable) / LOOK (screenshot +
  model judgment against stated criteria) / ASK (requires a human or user test —
  e.g., blind comprehension). Be honest about which tier a factor truly sits in;
  miscategorizing LOOK as MEASURE is how audits pass while owners see failures.
- **(e) The failure it catches** — a concrete named failure mode this check
  would have flagged (use the motivating case where it applies).

## SYNTHESIS DELIVERABLES (in this order)

1. **Verdict** — one paragraph: the shape of the complete factor space and the
   single highest-leverage gap in a contrast+geometry-only audit.
2. **Ranked taxonomy** — every factor scored on (impact on perceived quality ×
   machine-checkability), with the per-factor contract above.
3. **The audit spec** — an ordered gate list Guild can implement: which checks
   run in which order, what blocks (NO-GO) vs advises, and which existing Guild
   gates (auto-critique, responsive-scan, completeness-gate) each extends.
4. **The eyes-only residue** — the explicit list of qualities NO machine proxy
   covers, so the LOOK/ASK passes have a defined scope instead of "vibes."
5. **What didn't survive** — claims that failed verification, and where
   authoritative sources contradict each other (typography and motion norms
   disagree across design systems — surface the disagreements, don't average
   them away).

## DISCIPLINE (same bar as the mental-model run)

- Adversarial verification: no claim ships without independent verifiers trying
  to refute it; report vote counts and confidence per finding.
- Primary sources over summaries; verbatim quotes for every load-bearing claim;
  note publication/update dates — design-system guidance drifts.
- Prefer factors that generalize across surfaces (dashboard, form, marketing,
  mobile) — flag any factor that is surface-specific.
- Do not pad: a factor without a real (b) machine proxy or honest (d) tier is
  reported as such. The residue list (deliverable 4) is a first-class output —
  Guild needs to know exactly where human eyes remain mandatory.
