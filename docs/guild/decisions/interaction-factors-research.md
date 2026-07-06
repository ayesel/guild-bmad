# Interaction Factors Research — Reconciled Verdict (v1, 2026-07-06)

Reconciliation of the deep-research runs of
`docs/guild/INTERACTION-FACTORS-RESEARCH-PROMPT.md` (v1). This is the spec for
the next generation of Rogue/Mage interaction gates AND the required fields on
Rogue's flow artifacts. Final leg of the factors triptych:
`ui-factors-research.md` = SPACE, `ia-factors-research.md` = STRUCTURE, this =
TIME.

**Provenance.** Raw reports in
`guild-output/guild-artifacts/research/interaction-factors/reports/`: Gemini
Deep Research (15 factors, protocol-heavy, some invented numeric precision)
and Claude Research (20 factors, strongest sourcing — WCAG/APG/web.dev/Saffer
verbatims — and honest disagreement handling). Reconciled from direct reads of
both primaries. The ChatGPT run was redispatched after a silent
viewport-related death and had not completed at reconcile time — its report
folds in as an addendum if/when collected (manifest tracks status honestly).
Two-report reconciliation meets the expedition minimum. Rule: disagreements
surfaced, never averaged.

---

## 1. Verdict (reconciled)

Both runs converge hard, and on the most important point they converge to the
*same protocol independently*: **most of what teams call "feel" is MEASURE-tier
under an agent that can drive the app.** Acknowledgment latency, input
blocking, focus movement, layout shift, modality parity, pointer cancellation,
form-error semantics, reduced-motion feedback preservation, and transition
coverage are all deterministic under scripted driving. The genuinely human
residue is small and nameable (§5).

**The single highest-leverage gap in a tokens+envelope-only practice — both
runs, independently:** the envelope verifies motion is *legal* (tokenized,
within duration bounds, reduced-motion branch present) but never that it is
**complete or non-harmful**. Three defects produce the "clunky" feel and are
invisible to the envelope:

1. **Transition coverage** — reachable state pairs that were never designed,
   defaulting to browser jump-cuts. Both reports independently propose the
   same fix: a **state-pair matrix diff** between the flow artifact and the
   observed/compiled transitions, where any pair classified neither
   {designed-motion} nor {explicit-cut} fails the build. This single gate
   makes "motion as a post-hoc polish pass" *structurally impossible* — an
   undesigned transition becomes a build defect instead of a vibe.
2. **Input-blocking during animation** — both reports specify the identical
   probe: dispatch a pointer/keyboard event at t≈50ms into a transition and
   assert it registers. `pointer-events:none` windows and click-swallowing
   fades are binary defects.
3. **Acknowledgment latency** — every action visually acknowledged ≤100ms
   (Nielsen/Miller perceptual limit) even when the operation is slow; INP's
   200ms "good" is an achievability-adjusted field threshold, not the
   perceptual target (keep both, conflate neither — and keep both distinct
   from the 400/500ms *duration* envelope; the Doherty 400ms is a different
   research tradition entirely).

## 2. Reconciled taxonomy (grouped; C=Claude report, G=Gemini report)

**Latency & feedback**
| Factor | Tier | Agreement | Blocking contract |
|---|---|---|---|
| Input acknowledgment ≤100ms | MEASURE | C+G | First visual change ≤100ms of input (PerformanceObserver event timing + frame diff); slow async needs pressed-state/optimistic/skeleton acknowledgment |
| Latency choreography | MEASURE + LOOK order | C+G | Indicator within 1s of >1s waits (existing); skeleton geometry ≈ final layout (ties to CLS); skip placeholders entirely when resolution ≤200ms (G — adopted as house default, prevents flicker); progressive most-important-first = LOOK |
| CLS as interaction defect | MEASURE | C+G | ≤0.1 (web.dev); any unexpected interaction-adjacent shift is a defect regardless of aggregate |
| Optimistic vs pessimistic | MEASURE pattern + ASK policy | C+G, boundary contested §6 | MEASURE: detect pattern, verify rollback-on-failure under injected error; policy per action stakes is ASK |

**Choreography**
| Factor | Tier | Agreement | Blocking contract |
|---|---|---|---|
| Transition coverage (state-pair matrix) | MEASURE | C+G — the flagship | 100% of reachable pairs classified {designed-motion \| explicit-cut}; artifact-vs-build diff; any gap blocks |
| Animation never blocks input | MEASURE | C+G identical probe | Event at any frame of a standard transition must register; no `pointer-events:none` on interactives mid-transition |
| Choreography & stagger | MEASURE timing + LOOK rhythm | C+G, magnitudes disagree §6 | Nonzero stagger when cascade declared; order encodes reading direction; magnitude = house token, consistency asserted |
| Spatial continuity / shared elements | MEASURE geometry + LOOK model | C+G | Declared shared element interpolates continuously (no >1-frame discontinuity, no aspect warp) |
| Signature-moment budget | MEASURE count + ASK pick | C+G | ≤1 expressive/hero motion per surface (house); 0 decorative animation on high-frequency controls |

**Reversibility & safety**
| Factor | Tier | Agreement | Blocking contract |
|---|---|---|---|
| Undo over confirm | MEASURE presence + ASK severity | C+G | Destructive ⇒ undo affordance (toast window ~5–10s, practitioner-tier); truly irreversible ⇒ explicit confirm; confirm-walls on reversible actions flagged as smell |
| Pointer cancellation / mid-gesture abort | MEASURE | C (WCAG 2.5.2) + G partial | Actions fire on up-event; drags abortable via Esc/release-outside with full state revert |
| Reduced-motion preserves feedback | MEASURE | C explicit + G compatible | Under `prefers-reduced-motion`, every feedback-bearing interaction still acknowledges (opacity/color swap, not deletion); `*{animation:none}` is a defect |

**Accessibility through time**
| Factor | Tier | Agreement | Blocking contract |
|---|---|---|---|
| Focus management through time | MEASURE | C+G | APG contracts: focus into modal on open, return-to-trigger on close, Tab trapped, Esc closes, SPA route change moves focus to landmark/heading (never `<body>`), scroll restoration deliberate |
| Modality parity | MEASURE + LOOK discoverability | C+G | Keyboard path for every pointer path (WCAG 2.1.1); single-pointer alternative per gesture (2.5.1/2.5.7); hover content focus-reachable + dismissable (1.4.13); ≥24px targets |
| Feedback channel parity (sound/haptics) | MEASURE parity + ASK choice | C+G | Haptic/audio ⇒ co-occurring visual change; web audio never autoplays; mute-by-default |

**Input feel & flows**
| Factor | Tier | Agreement | Blocking contract |
|---|---|---|---|
| Micro-interaction completeness (Saffer) | MEASURE presence + LOOK meaning | C+G | Trigger→rules→feedback→loops present per declared interactive element; browser-default behavior where a designed interaction was declared = defect |
| Direct-manipulation feel | MEASURE thresholds + ASK feel | C+G, thresholds are library values not standards | Activation dead-zone consistent app-wide; drag-follow lag measured; snap deterministic; "weighted" feel is ASK |
| Form interaction timing | MEASURE semantics + ASK policy | C+G, blur-vs-submit contested §6 | No errors mid-keystroke on a clean field; errors programmatically associated (`aria-invalid`/`describedby`); focus-to-first-error on submit; clear-on-correct instantly; forgiving formats accepted |
| Flow-level dynamics | MEASURE | C+G | Back preserves entered data; refresh restores declared state; steps never skip/duplicate; step transitions consistent; auto-advance vs continue is ASK |

## 3. Gate spec (BLOCK vs ADVISE vs LOOK)

**BLOCK — static (artifact/DOM):**
1. Artifact completeness (§4): any state pair or interactive element with
   unfilled transition/feedback/reversibility/modality fields blocks.
2. Token/envelope (existing, unchanged): raw values, >500ms standard, missing
   reduced-motion branch.
3. Layout-thrashing lint (G): animating height/width/margin/padding instead
   of transform/opacity — ADVISE-strength but statically checkable.

**BLOCK — driven (the new interaction-gate suite):**
4. Acknowledgment ≤100ms; 5. Input-never-blocked (t=50ms probe);
6. Transition-coverage diff; 7. Focus-through-time (APG set);
8. Modality parity + pointer cancellation; 9. CLS ≤0.1 + zero unexpected
interaction-adjacent shifts; 10. Reduced-motion feedback preservation;
11. Form-error semantics (association, focus-to-error, clear-on-correct).

**ADVISE:** skeleton geometry/sequencing, drag-activation consistency,
stagger timing/order, shared-element continuity, back-integrity details,
signature budget count, optimistic-pattern detection + rollback verify,
web-audio autoplay, spring-only-for-spatial lint (G).

**LOOK (routes to the mage WA watch/critique lane, never blocks):**
motion-suits-the-relationship, progressive order, stagger rhythm as
hierarchy, spatial model survival, feedback meaningfulness.

Wire the driven suite through the conditional craft-gate mechanism (FIX #2
green-collapse) — eleven blocking checks must not become eleven log walls.

## 4. The artifact spec (the process fix — required Rogue template fields)

Both reports demand the same thing; merged schema. Per **state pair** in every
state-diagram / user-flow / interaction-map:
- `transition`: {motion: {pattern (container-transform | shared-axis |
  fade-through | fade | exit/enter pair), duration_token, easing_token,
  reduced_motion_variant} | cut: intentional} — **no blank allowed**
- `feedback`: acknowledgment channel + latency budget (default ≤100ms)
- `reversibility`: reversible | soft-reversible(undo_window, undo_action_id) |
  irreversible(confirm_gate)
- `focus_handoff`: target element/landmark after the transition
- `interruptible`: must be true for standard transitions
- `modality_parity`: keyboard equivalent + single-pointer alternative +
  touch/hover degradation

Per **interactive element**: Saffer four-part declaration; optimistic vs
pessimistic for async actions; signature-moment flag (counts against budget).

An artifact field left blank blocks at artifact time; a built transition that
contradicts its declared field blocks at the coverage diff (§3.6). Interaction
design becomes a flow-authoring-time activity — this is what retires the
post-hoc motion pass.

## 5. Eyes-only residue (bounded, named, routed)

1. Whether motion *feels* weighted/physical (latency is MEASURE; feel is ASK).
2. Whether an action is catastrophic enough for a confirm wall.
3. Optimistic-safety for a given action's stakes (genuinely domain-dependent).
4. Validation-timing policy (blur vs submit — unresolved in the literature;
   declare per product, then MEASURE against the declaration).
5. Rhythm/tempo elegance, vestibular comfort, repetition fatigue over
   high-frequency use (G's three) → owner watch sessions (mage WA) + user
   tests.
6. Which single hero moment deserves the signature budget; channel
   appropriateness per event class.

Everything else is MEASURE under driving and must NOT be routed to eyes.

## 6. What didn't survive + genuine disagreements

**Killed:**
- **"Validate on blur is settled best practice"** — it is not. Baymard:
  inline-but-not-premature; Silver/UX Movement: blur is itself premature,
  validate on submit + focus-to-first-error. Gemini presents blur as settled —
  overclaim. House: policy is declared per product (default blur), gates
  check the *semantics* (no mid-keystroke errors, association,
  clear-on-correct), never a universal timing.
- **"Skeletons ~30% faster perceived"** — blog-tier number; the peer-reviewed
  anchor (Mejtoft ECCE'18) is positive but small-scale. Geometry/CLS gates
  stay; the magnitude claim dies.
- **"100ms and 400ms are the same 'instant'"** — different traditions
  (Miller/Nielsen perceptual acknowledgment vs Doherty productivity). The
  acknowledgment contract (≤100ms) and the duration envelope (400/500ms) stay
  distinct.
- **"Reduced motion = remove animation"** — deletes essential feedback;
  contradicts WCAG 2.3.3 intent.
- **"Confirmation dialogs prevent errors"** — routine confirm-walls train
  click-through; confirmation is for consequential/irreversible only.
- **Gemini's invented precision** — focus handoff ≤50ms, undo window
  5000–8000ms, stagger 15–30ms, spring bounce 0.1–0.3, drag dead-zone ≥10px,
  ≤110ms content fade: none are literature-backed as universals. The useful
  ones (≤200ms skip-skeleton, dead-zone consistency) enter as house-tunable
  defaults; the rest are dropped.

**Genuine disagreements (kept):**
1. **Duration norms** — Material m1 150–200ms desktop / m3 scale to 600ms+
   for container transforms vs Carbon productive 70–240ms vs Apple "no
   numbers." Resolution stands from ui-factors: NN/g envelope as audit bound,
   task-context scaling (fast for high-frequency, longer distance-scaled for
   large spatial moves), tokens as reference.
2. **Stagger magnitude** — Material legacy ceiling ≤20ms vs library examples
   ~100ms vs physics-based none vs Gemini's 15–30ms. House: a stagger token,
   consistency asserted, magnitude calibrated per product; Material's 20ms
   ceiling noted as legacy/weak.
3. **Optimistic-UI boundary** — Mishunov (optimistic when reversible,
   <2s, 97–99% success) vs Ströer (reverted wholesale to pessimistic) vs
   "never except when failure doesn't matter." Contested and domain-bound:
   MEASURE the pattern + rollback; the policy is an owner call per action.
4. **Drag thresholds** — dnd-kit 5px/200–250ms vs Android touch-slop vs iOS
   implicit: library configs, not standards. Assert app-internal consistency,
   report the values, no universal gate.
5. **INP 200ms vs perceptual 100ms** — differ by design (achievability vs
   perception), not by error; keep both, label both.

## 7. Thin-slice build pick (TIME leg)

1. **Rogue template fields (§4)** — the process fix, pure authoring-time,
   no new runtime needed. Ships first.
2. **`interaction-gate.py` v1** — the three flagship driven checks:
   acknowledgment ≤100ms, input-never-blocked (t=50ms probe), focus-through-
   time (APG set). Playwright-driven, wired via craft-gates conditional suite.
3. **Transition-coverage diff** — needs §4 fields populated on one real flow
   first; lands as v2 once a Rogue artifact carries the matrix (candidate:
   the Nourish D3/D4 flows, which also closes the comment→regenerate loop).
CLS/reduced-motion/form-semantics checks fold in behind these; LOOK items
route to the existing WA lane from day one.

---

*Reconciled 2026-07-06 (Fable) from two primary reports read directly (Gemini,
Claude); ChatGPT run pending → addendum on collection. Triptych complete:
SPACE / STRUCTURE / TIME all reconciled.*
