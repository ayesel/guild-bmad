# IA Factors Research — Reconciled Verdict (v1, 2026-07-06)

Reconciliation of three independent deep-research runs of
`docs/guild/IA-FACTORS-RESEARCH-PROMPT.md` (v1). This document is the spec for
the next generation of Cartographer gates (and the IA-shaped slice of Sage's
QA), per the prompt's contract. Sibling of `ui-factors-research.md` (SPACE);
this is STRUCTURE.

**Provenance.** Raw reports in
`guild-output/guild-artifacts/research/ia-factors/reports/`: ChatGPT Deep
Research (16 factors, strongest primary-source citations), Claude Research
(17 factors, strongest on LLM-simulation reliability evidence and rubrics),
Gemini Deep Research (14 factors, strongest formalization — explicit formulas
and protocols, weakest sourcing). Reconciled by Fable from direct reads of all
three primary reports (extraction subagents cross-contaminated and were
discarded — a process note recorded in workspace memory). Rule: disagreements
surfaced, never averaged.

---

## 1. Verdict (reconciled)

All three runs converge on the same shape: **IA quality is more human-bound
than rendered-surface quality.** Where UI factors are overwhelmingly MEASURE,
IA distributes roughly one-third MEASURE (deterministic over artifact graphs,
vocabulary, and DOM), one-third LOOK (model judgment explicitly labeled as a
*simulation* of a human test), and one-third ASK (card sorts, tree tests,
first-click tests, blind comprehension) — because findability and
comprehension are facts about human minds, not artifacts.

**The single highest-leverage gap in a provenance-only practice — unanimous —
is the missing artifact-time semantic gate**: nothing between "IA decided" and
"IA shipped" asks *does this label predict its destination to a naive reader?*
Provenance gates prove a structure was researched; they cannot prove the
shipped labels, category boundaries, and truncated titles still yield the
right first click. That is precisely the Hall blind-test round-1 failure
(ambiguous cards, jargon, truncation), and all three runs independently
identify its components as checkable before build. Anchor (all three, with a
replication caveat — §6.2): first click on an optimal path → ~87% eventual
task success vs. ~46% otherwise (Bailey & Wolfson 2006–2009; replications show
the direction robustly, the magnitude smaller).

**The honesty constraint is load-bearing:** LOOK-tier IA checks (LLM
first-click prediction, simulated card sorts, trunk-test simulation) are
*measurably unreliable as predictors of human behavior* (§5) and therefore
NEVER block autonomously — they escalate to ASK. Only deterministic checks
block. This resolves the one place two reports drifted toward tier inflation
(§6.1) and matches the standing ui-factors rule: LOOK never blocks.

## 2. Reconciled ranked taxonomy

Merged across reports (three-way agreement unless noted). Tier is the
*stricter honest* tier. "House" = deterministic proxy, cutoff is Guild policy.

| # | Factor | Tier | Agreement | Machine proxy (reconciled) | Block / advise |
|---|---|---|---|---|---|
| 1 | Terminology consistency | MEASURE | 3/3, top-ranked by all | Entity→label map across nav/title/breadcrumb/button/URL/email; flag any entity with >1 normalized label, any label reused for 2 concepts, verb drift (Delete/Remove/Trash) | BLOCK: 0 unresolved variants on critical concepts; FLAG noncritical drift |
| 2 | Content-model / sitemap graph health | MEASURE | 3/3 | Directed-graph analysis: orphans (in-degree 0), dead ends (no forward/hub path), illegal cycles, list+detail coverage per entity type, child-bearing categories without landing/overview | BLOCK: 0 / 0 / 0 / 100% |
| 3 | Addressability & durable state | MEASURE | 3/3 | Per IA node/state: stable URL exists, cold-load reproduces state (Gemini's rehydration protocol: set state → capture URL → fresh context → diff), refresh + back-stack integrity | BLOCK: 0 canonical states failing |
| 4 | Label clarity & information scent | MEASURE parts + LOOK + ASK | 3/3 on impact; tier split resolved §6.1 | MEASURE: generic-label set {Click here, Learn more, Explore, Details…}, CTAs without noun object, first-token front-loading; LOOK: LLM first-click simulation per core task (labels only); ASK: real first-click/tree test | BLOCK deterministic parts; LOOK escalates to ASK, never blocks alone |
| 5 | Meaning-hiding truncation | MEASURE | 2/3 explicit (Claude artifact-time simulation; ChatGPT under scent), no dissent | Simulate clipping at rendered char budget; surviving prefix must stay unique among siblings and retain the head noun | BLOCK sibling collisions / lost distinguishing token |
| 6 | Jargon / reading level | MEASURE + LOOK | 2/3 explicit | Flesch-Kincaid over labels/microcopy; unexpanded acronyms; tokens outside declared controlled vocabulary | BLOCK > grade 8 on core microcopy (NN/g error-message standard) + unexpanded acronyms; FLAG jargon judgment |
| 7 | Wayfinding / you-are-here | MEASURE (+LOOK trunk test) | 3/3 | Exactly one active-nav marker (`aria-current`); marked location == sitemap node; breadcrumb trail == graph ancestor path (IA, never history); local-nav siblings match artifact | BLOCK missing/contradicting cues; trunk-test simulation ADVISE |
| 8 | Recovery paths | MEASURE (+LOOK copy quality) | 3/3 | Every empty/error/404/403/no-result state has ≥1 in-IA forward link; no raw-code-only states; permission walls carry request-access or browse fallback | BLOCK dead ends; FLAG copy constructiveness |
| 9 | Classification & grouping | MEASURE parts + ASK | 3/3 | Junk-drawer regex {More/Other/Misc/General…}; duplicate membership vs declared scheme (polyhierarchy must be declared); LLM cohesion/overlap scoring (LOOK, e.g. pairwise label-embedding similarity per Gemini) | BLOCK junk labels + undeclared duplicates; cohesion ADVISE→ASK (card sort owns truth) |
| 10 | Structural semantics / outline fidelity | MEASURE agreement + LOOK story | 3/3 with tier split resolved | MEASURE: title, H1, breadcrumb, active nav, URL all reference the SAME canonical node (deterministic identity check — ChatGPT's contribution); well-formedness owned by focus-gate; LOOK: does the outline alone tell the right story | BLOCK node-identity disagreement; fidelity ADVISE |
| 11 | Task-flow efficiency | MEASURE structure + ASK | 3/3 | Flow-graph: shortest path, backtrack edges, detours vs optimal, dead ends; Gemini's lostness formula L=√((N/S−1)²+(U/S−1)²) as the run metric | BLOCK unrecoverable dead ends (0 tolerated); step counts advisory — click caps are dead |
| 12 | Metadata / controlled vocabulary / facets | MEASURE | 1/3 (ChatGPT unique; no dissent) | Synonym rings resolve to same destination set; facet orthogonality; missing required metadata on core entities; empty facet combinations surfaced | BLOCK missing required metadata + synonym collisions on high-frequency concepts |
| 13 | Progressive-disclosure architecture | MEASURE consistency + LOOK | 3/3 | Siblings disclosed alike (deterministic); primary/mandatory content hidden behind ambiguous disclosure (LOOK); Gemini's nesting-depth count | BLOCK hidden mandatory next-steps; rest ADVISE (Gemini's 0.15–0.40 disclosure ratio REJECTED as invented precision) |
| 14 | Search ↔ browse balance | MEASURE + ASK | 3/3 | No browse-only or search-only critical destinations; zero-result states have forward paths; index coverage of public entities | BLOCK route asymmetries + zero-result dead ends; ratios advisory (domain-dependent per Baymard) |
| 15 | Depth vs breadth | MEASURE geometry, advisory | 3/3 measured; thresholds contested §6.3 | Click-depth to core tasks, per-level breadth, orphan depth | ADVISE only; gate via scent + tree test, never via click/level/width caps |
| 16 | Cross-surface consistency | MEASURE | 2/3 explicit | Entity labels, hierarchy, primary actions diffed across web/mobile/email/notification artifact models (Gemini adds graph-edit-distance as the metric) | BLOCK critical concept/route drift; house parity targets |
| 17 | Mental-model conformance | LOOK + ASK | 3/3 | Pattern classification vs convention library (inbox/editor/feed/checkout/dashboard) + canonical-affordance checklist (an inbox has list, read/unread, detail, return-to-list); novelty flag | Never blocks; high novelty triggers mandatory ASK |

## 3. Gate spec — Cartographer (artifact time) and Sage (render time)

All three reports agree on the two-phase split and on artifact-time as the
prize: structure defects caught before anything is built. Order: provenance
(existing spine/ia-evidence — untouched) → artifact structure → render
conformance → human validation.

**ARTIFACT TIME — Cartographer, BLOCKING (all MEASURE):**
1. Graph health (0 orphans / 0 illegal cycles / 0 unintended dead ends / 100%
   list+detail) — extends completeness-gate
2. Terminology: 0 unresolved label variants per critical entity
3. Generic-label + junk-drawer scan: 0 banned labels without declared rationale
4. Recovery-path presence in the flow model: ≥1 in-IA forward link per
   empty/error/permission state
5. Addressability: every distinct IA node/state has a declared shareable URL
6. Truncation simulation: clipped labels stay unique + keep head noun
7. Reading level: Flesch-Kincaid ≤ grade 8 on core microcopy; acronyms expanded
8. Required metadata present; synonym rings resolve consistently

**ARTIFACT TIME — Cartographer, ADVISE + ESCALATE (LOOK, never auto-block):**
9. Label-scent / first-click simulation per core task — wrong or low-confidence
   branch ESCALATES that task to the human gate (it does not block by itself;
   see §6.1 — this is where two reports flirted with tier inflation and their
   own evidence refutes them)
10. Category cohesion, mental-model conformance/novelty, progressive-disclosure
    appropriateness, depth-to-core-task

**RENDER TIME — Sage, BLOCKING (MEASURE):**
11. Canonical-node identity: title == H1 == breadcrumb == active nav == URL
    node (deterministic identity, not judgment)
12. You-are-here + breadcrumb integrity on the rendered DOM
13. Terminology + truncation re-run against rendered text
14. Error/empty/zero-result dead-end check as rendered

**RENDER TIME — Sage, ADVISE (LOOK):** trunk-test simulation, outline story
fidelity (extends focus-gate's well-formedness, does not duplicate it),
cross-surface parity.

**HUMAN GATE (ASK — bounded, named, mandatory where flagged):**
- **Card sort** when primary categories/labels change — open ≥15 participants,
  closed 20–30 (Gemini's protocol); agreement bands ≥60%/≥80% are
  vendor-sourced calibration guides, not law (§6)
- **Tree test / first-click** for critical-task navigation changes — 50–100
  sessions; house policy: critical task <67% blocks ship, ≥80% is the target
  (published as versioned Guild policy, explicitly NOT industry law)
- **Blind comprehension test** — the formalized final ship-gate, N≥5 naive
  participants, five-point rubric per card/screen: (1) identification,
  (2) action clarity, (3) outcome prediction, (4) restate-without-jargon,
  (5) meaning intact at rendered size. Any card failing (1)–(3) blocks. This
  is the check that, run between "IA decided" and "IA shipped," catches the
  Hall round-1 class.

## 4. Artifact requirements (what Cartographer artifacts must now carry)

The gates above are only computable if the artifacts declare:
- **Entity registry**: entity id → canonical label + declared synonyms
  (controlled vocabulary); required metadata fields per entity type
- **Sitemap as a real graph**: nodes typed (list/detail/hub/terminal), core
  tasks flagged, declared polyhierarchy where used, landing pages for
  child-bearing categories
- **Flow graphs** with error/empty/permission states and their recovery edges
- **URL map**: every node/state → its shareable route
- **Label budgets**: max rendered characters per label slot (enables the
  truncation simulation at artifact time)
- **Surface variants** declared (web/mobile/email/notification) for parity diffs

## 5. Eyes-only residue (bounded by quantitative evidence)

What only humans can verify — with the 2024–2026 numbers that prove the LOOK
simulations cannot be promoted (Claude report's distinctive contribution,
corroborating sources independent):

1. **Category validity** — LLM card sorts: 68% item-placement match, κ=.60
   (MeasuringU 2024); NMI ≈0.68, ~11–12 of 34 cards misplaced (Kuric et al.
   2025). Supplement, not replacement.
2. **Findability** — LLMs find ~90% of tree-test paths vs ~51% human baseline:
   they *overshoot* and cannot estimate human success. Valid only as an
   expert lower-bound screen ("if the model gets lost, humans will too").
3. **First-click correctness** — 71% hotspot alignment, .16 rank-order
   agreement, significant distribution difference in 53% of tasks (Kuric et
   al. 2026): "inaccurate and unreliable as a predictor."
4. **Comprehension of task-defining copy** — naive human interpretation;
   LLMs are sycophantic approximations (NN/g 2024).
5. **Mental-model acceptability of novel structures** and real task
   efficiency/satisfaction — moderated testing.

Validated simulation uses (screens only): task-difficulty prediction
(SEQ r=.62) and the expert lower bound. Nothing else downgrades today.

## 6. What didn't survive + genuine disagreements

**Killed by all three runs:**
- **Three-click rule** — no supporting data in any published study; Porter
  (620 tasks/44 users): no dropoff correlation; UIE: users click 25 times
  happily with strong scent; Nielsen: findability +600% at 4 clicks vs 3.
- **7±2 / magic menu caps** — Miller's span is short-term memory; menus are
  recognition. Larson & Czerwinski: 16/32-wide beat 8-wide on ~500-item trees.
- **"Breadcrumbs fix bad IA"** — secondary aid, never a structural remedy.
- **Card sort as final IA** (Spencer: formative input), **search replaces
  navigation** (NN/g + Baymard), **progressive disclosure always good**,
  **polyhierarchy dogma either way** (use sparingly, validate), **"200 pages
  need search"** (advisory smell only).

**Disagreements (kept, with house resolutions):**
1. **Can the scent simulation block?** Claude/Gemini position it as an
   artifact-time (soft) blocker; the very evidence they cite (Kuric 71%/.16)
   says LLM first-click prediction is unreliable; ChatGPT positions LOOK as
   escalation-to-ASK. **House: LOOK never blocks — it escalates.** The
   deterministic sub-parts (generic labels, front-loading, truncation,
   junk-drawer) carry the blocking load.
2. **First-click effect size** — 87/46 (Bailey & Wolfson) vs 70/24 vs a
   13-point gap (MeasuringU replications). Direction robust, magnitude
   contested; cite the range, never 87% as settled.
3. **Depth/breadth numbers** — Miller/Kiger ~8/level vs Larson & Czerwinski
   depth-dominates; Miller & Remington: *scent dominates shape*. Gemini's
   ≤4 depth / ≤7 top-nav / ≤13 side-nav caps are REJECTED as gates — and
   Gemini's ≤7 "Miller's Law" cap contradicts its own folklore section
   debunking exactly that. Geometry is measured, advisory only.
4. **Invented numeric precision (Gemini)** — scent cosine ≥0.70, category
   overlap ≤0.70/0.75, disclosure ratio 0.15–0.40, lostness ≤0.40. The
   *formulas* (drift cardinality, lostness, graph-edit-distance, label-set
   intersection) are adopted as implementable proxies; the *universal
   thresholds* are not literature-backed and enter as house-tunable
   parameters, calibrated on our own runs (NN/g: "the best frame of
   reference is your own previous data").
5. **Classic IA richness vs design-system flatness** (Gemini's genuinely
   novel find): Rosenfeld/Morville faceted, polyhierarchical access vs
   Atlassian/Polaris flat single-surface mandates. **House: flat
   single-surface for admin/transactional products (the Hall class); faceted
   structures reserved for large information-dense catalogs.**
6. **Vendor-sourced thresholds** — card-sort/tree-test bands (60/80;
   61–80/80–90/>90) trace to tool-vendor docs citing Albert & Tullis (whose
   own review shows median 62%, IQR 37–83%); the Kuric studies are
   UXtweak-affiliated. Used as calibration guides, flagged as
   practitioner-tier.

## 7. Thin-slice build pick (per the standing build strategy)

The structure leg's first cut, matching effort to §2's agreement × checkability:
1. **`ia-graph-gate.py`** — graph health + addressability over the sitemap
   artifact (factors 2–3): pure graph analysis, unanimous, zero-threshold.
2. **`terminology-gate.py`** — entity→label drift + generic/junk-drawer +
   truncation simulation + Flesch (factors 1, 4-deterministic, 5, 6): the
   semantic-defect scanner that catches the Hall class deterministically.
3. **Artifact-field requirements (§4) added to Cartographer's templates** —
   entity registry, typed graph, URL map, label budgets — so 1–2 have
   something to compute over. This is the process fix, not a gate.
The scent simulation (LOOK) and human-gate wiring follow after calibration
labels exist; both are ADVISE/escalate from day one, per §6.1.

---

*Reconciled 2026-07-06 (Fable) from three primary reports read directly.
Triptych: `ui-factors-research.md` = SPACE (shipped), this = STRUCTURE,
`interaction-factors-research.md` = TIME (reports collected, reconcile
pending).*
