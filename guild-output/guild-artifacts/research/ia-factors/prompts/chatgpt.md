You are running in Deep Research mode. Do NOT ask me any clarifying questions — the scope is fully specified below. Where something is genuinely ambiguous, state your assumption in one line and proceed. Browse widely, prefer primary and recent sources, and cite every non-obvious claim.

# GUILD IA-FACTORS RESEARCH (v1 — 2026-07-05)

The prompt that maps the FULL factor-space of superb information architecture —
everything an AI must consider (and, wherever possible, MEASURE) to structure,
label, and organize a product at the level of a top-tier human IA. Sibling of
`UI-FACTORS-RESEARCH-PROMPT.md` (rendered surface) using the same per-factor
contract. Paste into a deep-research session or run as an adversarially-verified
multi-agent workflow. Output lands at `docs/guild/decisions/ia-factors-research.md`;
its verdict becomes the spec for the next generation of Cartographer gates (and
the IA-shaped slice of Sage's QA).

---

## THE QUESTION

**What is the complete set of factors an AI needs to consider to produce superb
information architecture — and for each factor, how can an AI with access to the
artifact model (sitemaps, content models, user flows, spines), the rendered
DOM (headings, landmarks, nav trees, URLs), and the product's vocabulary verify
it programmatically?**

Not "what makes good IA" as prose. The deliverable is an *operational factor
taxonomy*: every factor carries evidence, a machine-measurable proxy, threshold
values, and a check tier. The end state is a gate spec Guild can wire the way
it wired contrast, geometry, and (next) saliency for the rendered surface.

## WHY (the motivating case — calibrate against this)

Guild's owner-facing Hall was designed on top of dedicated mental-model research
(`docs/guild/decisions/ui-mental-model-research.md` — 110 agents, adversarially
verified). The IA was "done": one primitive, inbox model, view lenses. Then the
blind comprehension test came back **FAIL on round 1** — decision cards read as
ambiguous, copy was jargon, truncation hid meaning
(`docs/guild/decisions/hall-blind-test.md`). The research was right and the
structure still confused a first-time viewer. That is the IA version of the
rendered-surface failure class ("audit passed, owner saw the problem
instantly"): **research produced design decisions, but no gates** — nothing ran
between "IA decided" and "IA shipped" to catch the miss.

The rendered-surface research (`ui-factors-research.md`) fixed this for pixels
with a taxonomy of MEASURE/LOOK/ASK factors. IA needs the same. Assume there
are dimensions we have not hit yet; enumerate the space.

## ALREADY KNOWN (baseline — do not re-derive; extend past it)

- **Mental-model findings are shipped** — Jakob's law / mental-model inertia,
  recognition-over-recall, the delegated-work-inbox + run-timeline model, steps
  completed/remaining for long waits (`ui-mental-model-research.md`). Reference,
  don't repeat.
- **The IA evidence lane exists** — spine / verification / confidence /
  ia-evidence gates already require every IA claim to trace to research
  artifacts. Those gate *provenance*, not *structural quality* — a fully-cited
  IA can still confuse users. Your scope is the structural-quality gap.
- **From the rendered-surface run** (shared substrate, don't re-derive):
  heading/landmark structure and focus-order-vs-reading-order land in
  focus-gate; grouping/proximity, scanability/progressive disclosure are
  render-time gates; the Hick's-law choice cap is DEAD — measure grouping and
  clutter, never a magic option count.
- Blind comprehension testing exists as a practice (hall-blind-test) but is
  ad-hoc — one goal of this research is to give it a rubric and a place in the
  gate order.

## THE FACTOR SPACE (starting scaffold — extend, reorganize, and prune with evidence)

Cover at least these dimensions; add any the literature shows we're missing:

1. **Labeling & information scent** — do link/section labels predict what's
   behind them; specific-over-generic; front-loaded first words; scent decay
   across levels.
2. **Terminology consistency** — one concept, one name, everywhere (nav label ==
   page title == breadcrumb == button verb); synonym drift as a measurable
   defect.
3. **Classification & grouping schemes** — exact vs ambiguous schemes; category
   mutual exclusivity; the "junk drawer" (Misc/Other/More) smell; card-sort
   agreement as the ground-truth proxy.
4. **Depth vs breadth** — click depth to core tasks; tree shape norms; when
   deep beats broad and vice versa; orphan depth.
5. **Wayfinding & you-are-here** — current-location marking, breadcrumbs,
   consistent nav placement, back-behavior integrity.
6. **Mental-model conformance** — does the structure pattern-match a model the
   user already has (inbox, editor, feed, checkout); bespoke-structure cost.
7. **Task-flow efficiency** — steps/decisions/inputs per core task; detour and
   backtrack counts in the flow graph; dead ends without recovery.
8. **Search vs browse balance** — findability by both routes; zero-result and
   no-search dead ends.
9. **Progressive disclosure architecture** — what's primary vs behind a click;
   disclosure depth consistency; premature detail.
10. **Content-model coverage** — every entity has a home (list + detail);
    orphan pages, dead ends, circular references in the sitemap graph.
11. **Addressability** — URLs/deep links map to the structure; sharable state;
    refresh survives.
12. **Cross-surface consistency** — same structure/names across web, mobile
    layouts, notifications, emails.
13. **Recovery paths** — from empty states, errors, 404s, permission walls back
    into the structure.
14. **Structural semantics as rendered** — heading hierarchy and landmarks
    *as an IA artifact* (the outline test: does the heading tree alone tell the
    page's story). (Shared with focus-gate; here the question is whether the
    outline is a faithful map of the IA, not whether it exists.)

## PER-FACTOR CONTRACT (every factor in the output carries ALL five)

- **(a) Evidence** — primary sources with verbatim quotes (NN/g IA & navigation
  research, Rosenfeld/Morville/Arango *Information Architecture* (polar bear),
  Spencer's card-sorting and tree-testing literature, Krug, Covert, Norman,
  GOV.UK / Shopify Polaris / Atlassian IA guidelines, peer-reviewed findability
  studies). Blog-only claims flagged weak.
- **(b) Machine proxy** — the concrete computation an AI with the artifact
  model + DOM + vocabulary extraction can run (e.g., "terminology drift = the
  same entity id rendered under ≥2 distinct labels across nav/title/breadcrumb";
  "junk-drawer smell = any category whose label is in {More, Other, Misc,
  General} or whose members share no extractable common attribute"). If the
  only real proxy is a tree test or card sort with humans, say so — that is a
  finding.
- **(c) Thresholds** — numeric pass/flag values with source (e.g., click-depth
  norms, tree-test success benchmarks), or "no agreed threshold" stated plainly.
- **(d) Check tier** — MEASURE (deterministic over artifacts/DOM) / LOOK (model
  judgment against a stated rubric, e.g. simulated first-click or label-scent
  scoring) / ASK (real humans: tree test, card sort, blind comprehension).
  Be honest: **expect MORE of this space to be ASK than the rendered-surface
  run** — findability and comprehension are human phenomena. Naming that
  residue precisely is the point; a LOOK proxy (an LLM predicting first-clicks)
  must be labeled a *simulation* of ASK, never promoted to MEASURE.
- **(e) The failure it catches** — a concrete named failure mode (use the Hall
  blind-test round-1 misses where they apply).

## SYNTHESIS DELIVERABLES (in this order)

1. **Verdict** — the shape of the complete IA factor space and the single
   highest-leverage gap in a provenance-only (spine-gated) IA practice.
2. **Ranked taxonomy** — every factor scored (impact × machine-checkability)
   with the full per-factor contract.
3. **The gate spec** — ordered checks Cartographer/Sage can run: what blocks vs
   advises, what runs at artifact time (sitemap/content model, before build) vs
   render time (DOM), and which existing gates (spine/ia-evidence,
   completeness-gate, blind-test) each extends. Artifact-time checks are the
   prize — they catch structure defects before anything is built.
4. **The eyes-only residue** — what only humans can verify (and which existing
   practice covers each: tree test, card sort, blind comprehension), so ASK has
   a bounded, named scope.
5. **What didn't survive** — IA folklore that fails verification (e.g., the
   three-click rule; magic menu-size numbers) and where authoritative sources
   genuinely disagree — surface disagreements, don't average them.

## DISCIPLINE (same bar as the mental-model and ui-factors runs)

- Adversarial verification: no claim ships without independent verifiers trying
  to refute it; report vote counts and confidence per finding.
- Primary sources over summaries; verbatim quotes for load-bearing claims; note
  dates — guidance drifts.
- Prefer factors that generalize across product types (dashboard app, content
  site, commerce, tool); flag surface-specific ones.
- Do not pad: a factor without a real machine proxy or honest tier is reported
  as such. The residue list is a first-class output — Guild needs to know
  exactly where tree tests and blind comprehension remain mandatory.

---
REQUIRED OUTPUT: follow the SYNTHESIS DELIVERABLES order in the specification
above EXACTLY (verdict -> ranked taxonomy with the full five-part per-factor
contract -> gate spec -> eyes-only residue -> what didn't survive /
source contradictions). End with a numbered Sources list; every load-bearing
claim cite-linked. Markdown. Length: whatever rigor requires - do not pad,
do not truncate.
