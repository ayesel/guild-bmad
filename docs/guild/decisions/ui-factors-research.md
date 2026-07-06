# UI Factors Research — Reconciled Verdict (v1, 2026-07-05)

Reconciliation of two independent deep-research runs of
`docs/guild/UI-FACTORS-RESEARCH-PROMPT.md` (v1). This document is the spec for
the next generation of Mage/Sage audit gates, per the prompt's contract.

**Provenance.** Raw reports:
`guild-output/guild-artifacts/research/ui-factors/reports/report-A-audit-factors.md`
(report A, deep-research surface w/ live citations) and
`report-B-factor-taxonomy.md` (report B, F1–F19 taxonomy w/ verbatim quotes +
adversarial confidence notes). Both are single-surface runs, not the
multi-agent adversarial workflow that produced `ui-mental-model-research.md` —
their self-reported vote counts are taken as directional, not verified.
Reconciled by Fable. Rule followed: disagreements are surfaced, never averaged.

---

## 1. Verdict (reconciled)

Both reports independently converge on the same three-shell structure:

1. **MEASURE** — deterministic, gateable: contrast (alpha-composited), target
   size, reflow incl. mid-bands, geometry (overlap/rhythm/alignment/nesting),
   type metrics, spacing scale, craft vocabulary, focus/keyboard a11y,
   reduced-motion presence, theme role parity.
2. **LOOK** — screenshot + model judgment against explicit rubrics: saliency/
   hierarchy, affordance honesty, full state-matrix plausibility, color
   harmony, motion purpose, microcopy quality, density.
3. **ASK** — human-only: blind comprehension, emotional/reflective resonance,
   felt trust, whether the *right* thing is primary for the business context.

**The single highest-leverage gap after contrast+geometry — both reports agree —
is visual hierarchy/saliency plus signifier (affordance) honesty.** A framed it
as "hierarchy-plus-signifiers"; B ranked "saliency squint test" #1 and
"affordance honesty" #2. This is exactly the class of failure an owner spots
instantly while deterministic audits pass: the eye lands on the wrong thing, or
an interactive element doesn't announce itself. It is partially machine-
approximable today (blur + saliency blob vs. semantic primary action) but
honestly LOOK-tier — and **miscategorizing LOOK as MEASURE is the root cause of
every past audit embarrassment**. The tier label is the load-bearing part of
this spec.

## 2. Reconciled ranked taxonomy

Factors merged across reports (A-name ≡ B-code). Score shown is the higher of
the two where they differ; tier is the *stricter honest* tier where they
disagree. "House" = deterministic proxy exists but the numeric cutoff is Guild
policy, not a standards number.

| # | Factor (A ≡ B) | Score | Tier | Agreement | Machine proxy (reconciled) | Block / advise |
|---|---|---:|---|---|---|---|
| 1 | Geometric layout integrity (≡F2, shipped) | 25 | MEASURE | Full | Sibling overlap >0; row-rhythm outlier >20%; content-start spread >4px; nesting ≥3 | BLOCK (nesting ADVISE) |
| 2 | Alpha-composited contrast (≡F3, shipped) | 25 | MEASURE | Full | WCAG 2.2 AA: 4.5:1 text, 3:1 large/non-text; gradient worst-stop | BLOCK |
| 3 | Focus visibility + keyboard narrative (≡F13) | 25 | MEASURE (SR narrative ASK) | Full | Tab/Shift-Tab sweep; focus order vs. visual order; indicator 3:1 + WCAG 2.4.13 size; focus-not-obscured; keyboard reach; landmarks/heading order | BLOCK (heading order ADVISE) |
| 4 | Responsive edge reflow + modality (≡F5) | 25 | MEASURE | Full | Breakpoint-edge sweeps (±32px + 900–1200 band in ~50px steps), 320px reflow (WCAG 1.4.10), 200% text, long-locale strings, coarse-pointer/no-hover | BLOCK |
| 5 | State-matrix completeness (≡F12) | 25(A)/12(B) | **Split** — see §5.5 | **Disagree on checkability** | Pseudo-state forcing (`:hover/:focus/:active/:disabled` computed-style delta) = MEASURE; empty/loading/error coverage needs app exercise = LOOK | BLOCK zero-delta focus; ADVISE rest |
| 6 | Target size (≡F4, shipped) | 20 | MEASURE | Full | 24×24 CSS px AA + spacing exception; 44/48 advise for touch | BLOCK at 24 |
| 7 | Craft vocabulary (≡F10) | 20 | MEASURE | Full (B explicit, A via depth budget) | Distinct radii ≤3–4; single shadow light direction; border weights ≤2–3; peer-icon size variance ≤15%; fill/elevation nesting | ADVISE (house) |
| 8 | Text-block readability (≡F6) | 20 | MEASURE (rag/widows LOOK) | Thresholds disagree — §5.1 | CPL from rendered width/glyph advance; line-height ratio; justified-without-hyphenation; scale conformance | BLOCK outside 45–90 CPL or 1.2–1.45 leading; FLAG outside 45–75 |
| 9 | Loading/progress honesty (≡F17) | 20 | MEASURE (felt speed ASK) | Full | Nielsen 0.1/1/10s buckets; indicator presence + scope; skeleton vs. spinner; stuck/competing indicators | BLOCK >1s no feedback, >10s no determinate progress; ADVISE rest |
| 10 | Theme semantics + dark parity (≡F9) | 20 | MEASURE (harmony LOOK) | Full | Role coverage in both modes; dark-mode contrast diff; role order/purpose flips; neutral temperature-sign consistency (B); unthemed literals | BLOCK dark-mode AA loss + role flips; ADVISE temperature/literals |
| 11 | Alignment + shared starts (≡F8) | 20 | MEASURE (optical LOOK) | Full | Left-edge clusters per region (≤3–4); peer-pane start divergence >8px block, repeated rows >4px flag; baseline rhythm advisory | BLOCK >8px peer panes (house) |
| 12 | Grouping/proximity (≡F7) | 16 | MEASURE | Ratio disagrees — §5.4 | Median intra-group gap vs. nearest inter-group gap; common-region compensation | FLAG intra > 0.75× inter (house) |
| 13 | Data scanability + disclosure (≡F14) | 16 | MEASURE (density LOOK) | Full incl. Hick's-cap rejection | Numeric-column digit alignment (blockable); >3 persistent row actions flag; permanent second-level detail flag | BLOCK misaligned numerics; ADVISE rest |
| 14 | Hierarchy/saliency — squint test (≡F1) | 15 | **LOOK** | Full — the #1 gap | Blur σ≈8–16px → saliency map → top blob(s) vs. semantic primary action; text-emphasis tier count 3–5; secondary within 10% saliency of primary flag | ADVISE (strong warn), annotated screenshots |
| 15 | Signifier parity / affordance honesty (≡F11) | 15 | LOOK (cross-ref MEASURE) | Full | Two-way: styled-but-inert (dead button) and interactive-but-unsignified (cursor/hover/role/handler cross-ref) | BLOCK clear dead button + high-salience false affordance above fold; FLAG >5% unsignified per region |
| 16 | Motion comfort + purpose (≡F15) | 12 | MEASURE (purpose LOOK) | Duration norms disagree — §5.2 | Duration/easing parse; reduced-motion block present AND neutralizing; frequent-interaction motion inventory | BLOCK reduced-motion noncompliance + WCAG pause/stop/hide; ADVISE >400ms, soft-block >500ms (house) |
| 17 | Microcopy surface shape (≡F16) | 12 | LOOK/ASK (presence MEASURE) | Full | Empty state has guidance + next-step CTA; errors carry cause + recovery; generic-label clusters ("Manage/View/Learn more"); errors >2 lines | BLOCK empty state w/ no next step; FLAG rest |
| 18 | Trust/provenance/anti-deception (≡F19) | 12 | MEASURE subset + ASK intent | Full | Unlabeled AI/sponsored regions; disclosure adjacency; preselected opt-ins; consent style-asymmetry (contrast/size delta between paired choices); cancel-vs-signup friction | BLOCK unlabeled AI decision support + non-adjacent disclosure; FLAG asymmetry |
| 19 | Aesthetic credibility (≡F18) | 8(A)/3(B) | ASK (inputs MEASURE) | Full | 50ms/500ms blinded screenshot trials; the measurable *inputs* are #1/7/8/11/12 above. Anchor: r=0.589 (Kurosu & Kashimura) — the circulating "r>0.9" is unsourced | Never a solo blocker |

## 3. The audit spec — ordered gate system

Both reports agree the audit is **ordered passes, not a flat checklist**, and
agree on the blocking rule: **BLOCK only on cited standards (WCAG) or
calibrated house geometry with low false-positive risk; everything model-judged
ADVISES with annotated-screenshot evidence.** Merged order (A's stages ×
B's pass structure), mapped to existing Guild gates:

| Stage | Checks | Verdict class | Extends |
|---|---|---|---|
| 0. Preflight inventory | DOM role map, landmarks, focusables, interactive-state map, token map, viewport plan | NO-GO if regions/interactives can't be classified (later passes untrustworthy) | completeness-gate |
| 1. Perception + operability | Contrast, target size, **focus/keyboard suite (NEW)**, **state-delta subset (NEW)** | NO-GO | craft suite, responsive-scan |
| 2. Reflow integrity | **Breakpoint-edge sweeps, 200% text, long-locale, coarse-pointer (NEW)** + existing overflow/geometry | NO-GO | responsive-scan |
| 3. Readability floor | **CPL/leading/justification/numeric-alignment (NEW)**, empty-state next-step, error shape | NO-GO on hard minima, else advise | type-ramp gate |
| 4. Latency + trust floor | **Indicator-honesty rules (NEW)**, disclosure adjacency, unlabeled AI, consent asymmetry (NEW) | NO-GO on severe deception / missing feedback | completeness-gate |
| 5. Structural craft | Alignment starts, grouping ratio, depth budget, **craft vocabulary (NEW)**, **theme parity (NEW)**, scanability | ADVISE, house-block on budget overrun | craft-gates.py conditional suite |
| 6. Visual judgment (LOOK) | **Saliency/squint (NEW — flagship)**, affordance honesty, state-matrix plausibility, harmony, motion purpose, density | ADVISE with scored screenshot rubrics, explicitly labeled LOOK | auto-critique |
| 7. Human pass (ASK) | Blind comprehension on critical flows, label meaning, provenance trust | ASK — recorded, never build-blocking | completeness-gate records coverage |

### Gate build order (the actual next work)

Priority = score × automatability × distance-from-shipped:

1. **focus-gate.py** (NEW) — the only top-scoring factor with zero current
   coverage and full determinism. Tab-sweep, order-vs-visual, indicator
   3:1/size, not-obscured, reach, landmarks.
2. **responsive-scan v2** — breakpoint-edge widths, 200% text, long-locale,
   coarse-pointer profiles bolted onto the shipped sweep.
3. **state-delta-gate.py** (NEW) — pseudo-state computed-style deltas; dead
   hover/focus detection. (Full matrix stays LOOK until the harness can force
   empty/error/loading data states.)
4. **readability-gate.py** (NEW) — CPL, leading, justification, numeric-column
   alignment.
5. **craft-gates v2** — radius/shadow-direction/border-weight/icon-variance
   vocabulary + fill/elevation nesting (extends the conditional suite).
6. **theme-parity-gate.py** (NEW) — role coverage diff, dark-mode contrast
   diff, temperature-sign consistency.
7. **affordance-check v2** — two-way clickability cross-ref (dead buttons,
   unsignified controls) on top of the shipped bounded/dangerous logic.
8. **saliency LOOK pass** — blur + blob-vs-primary in auto-critique with a
   scored rubric. Flagship new Mage capability; ships as ADVISE forever.
9. **latency-honesty + trust checks** — indicator rules; consent asymmetry.

## 4. Eyes-only residue (union, deduplicated)

No machine proxy fully covers these; the LOOK/ASK passes are bounded to exactly
this list — anything else claimed unmeasurable is padding:

1. Whether the *right* action is primary for the business/task context
   (saliency proves dominance, not correctness).
2. Blind comprehension — does a first-time user know what the screen is for
   and what words like "Archive"/"Resolve" mean here.
3. Emotional/reflective resonance; premium feel; brand fit and taste
   legitimacy (coherence is measurable, rightness is not).
4. The causal aesthetic-usability effect itself (inputs measurable, felt
   credibility human).
5. Optical exceptions — deliberate cheats (hanging punctuation, icon
   compensation, asymmetry for balance) that mathematical checks flag wrongly.
6. Motion purpose — whether animation aids understanding in practice.
7. Screen-reader narrative coherence (structure measurable, story ASK).
8. Trust from real-world context (fees/AI labels checkable; institutional
   trust not), incl. dark-pattern *intent* (a countdown's honesty).
9. Felt performance tolerance for *this* audience.
10. Cultural/contextual appropriateness of aesthetics (documented
    cross-cultural variance).

## 5. What didn't survive + where sources genuinely disagree

**Killed by both reports (do not gate on these):**
- **Hick's-law choice caps** — modern review literature explicitly rejects
  "less is better" as a rule; measure grouping/clutter, never a magic max-N.
- **A single authoritative motion-duration range** — Material, Carbon, NN/g
  and Apple all disagree; hard-block only WCAG/reduced-motion.
- **Hue harmony / neutral temperature as hard gates** — role parity gates,
  harmony stays LOOK (temperature-sign consistency is the one deterministic
  sliver, ADVISE only).
- **Beauty as a deterministic NO-GO** — aesthetic-usability is real
  (r=0.589 anchor) but boundary-conditioned; ASK tier only.
- **Baseline grids as universally required** (A) — advisory craft check.
- **Data-ink ratio thresholds** (B) — Tufte's own caveat + Inbar 2007
  (users often *prefer* chartjunk); ADVISE/LOOK only.
- **Marketing percentages** (B) — "300% more clicks," "30% faster skeletons"
  etc. trace to unsourced blogs; direction kept (skeletons > spinners, per
  peer-reviewed Mejtoft ECCE'18), numbers discarded.

**Genuine source contradictions (surfaced, not averaged):**
1. **Line length** — Butterick 45–90 vs. Bringhurst 45–75 (66 ideal; 40–50
   multi-column). House resolution: BLOCK outside 45–90, FLAG outside 45–75.
2. **Motion numbers** — Material short1=50ms vs. Carbon fast-01=70ms; Carbon
   caps 700ms, Material runs to 1000ms; NN/g "400ms very slow / 500ms a drag";
   Carbon micro-interactions 90–120ms. House resolution: NN/g bound as the
   audit envelope (advise >400, soft-block >500); token scales are reference.
3. **Target size** — WCAG AA 24px vs. AAA/Apple 44 vs. Material 48; WCAG
   issue #1831 disputes the 24px basis. House: block at 24 (the AA line),
   advise 44/48 for touch-primary.
4. **Proximity ratio** — A: intra ≤ 0.75× inter; B: inter ≥ ~2× intra. Both
   are house heuristics with no literature number. House: flag at 0.75×
   (A, the conservative bound); treat 2× as the craft target.
5. **State-matrix tier** — A calls completeness blockable (25, MEASURE); B
   scores checkability 3 (LOOK) because empty/error/loading require exercising
   the app. Resolution (the honest split): the pseudo-state delta subset is
   MEASURE and blockable; matrix *completeness* is LOOK until the harness can
   synthesize data states. A's tier claim repeated the exact miscategorization
   sin this research exists to stop.
6. **Carbon motion guidance drifts between versions** (B) — always cite the
   dated current page; design-system numbers are moving targets.

## 6. Addendum (2026-07-05) — token/component-layer enforcement (Tinker mapping)

Prevention beats detection: a factor enforced at the design-system layer never
fires at render time, which serves the ALIVE test directly ("first render was
right; gates were backstop"). This maps each §2 factor to its upstream
enforcement point. Wired into `tasks/design-system-foundation.md` step 4d
(code side); when `design_surface` is figma/both the same checks run on Figma
variables via Tinker `WC`/`TK`.

| §2 factor | Upstream enforcement | Where | Status |
|---|---|---|---|
| 2 Contrast | Token-pair contrast incl. alias-chain resolution | foundation 4b / tinker-wcag | shipped |
| 3 Focus/keyboard | Focus-indicator token (3:1 + 2.4.13 area) bound by every interactive primitive | foundation 4d.8 | NEW |
| 5 State matrix | Component variants enumerate states — **MEASURE at DS layer** (LOOK at app level; the §5.5 split resolves upstream) | foundation 4c.3 + Storybook (tinker SB) | shipped, sharpened |
| 6 Target size | Primitive hit-rect floor ≥24px (44 touch advise) | foundation 4d.8 | NEW |
| 7 Craft vocabulary | Radius ≤4, single shadow light direction, border weights ≤3, icon size props ±15% | foundation 4d.1–4 | NEW |
| 8 Readability | Type-scale + leading tokens (CPL stays page-level → Mage) | foundation step 2 | shipped (partial) |
| 10 Theme parity | Role diff across modes, dark-mode contrast re-run, luminance-order stability, neutral temperature sign | foundation 4d.5+7 | NEW |
| 11/12 Alignment/grouping | Spacing-scale + grid tokens (pane-level alignment stays Mage) | foundation step 2 | shipped (partial) |
| 16 Motion | Duration envelope on tokens (flag >400ms, none >500ms std); signature easing; reduced-motion branch | foundation 4c + 4d.6 | extended |

Not token-expressible (remain render-time Mage/Sage or LOOK): geometry (1),
reflow (4), loading honesty (9), scanability (13), saliency (14), affordance
(15), microcopy (17), trust (18), aesthetics (19).

---

*Next actions: build order in §3; wire stages 1–5 into the conditional
craft-gate suite (green-collapse per FIX #2) so the expanded audit doesn't
regress the operator-attention win; saliency LOOK pass lands in auto-critique
with its rubric stored beside `jury.yaml`. Upstream half wired 2026-07-05 (§6).
IA sibling: `docs/guild/IA-FACTORS-RESEARCH-PROMPT.md` (Cartographer).*
