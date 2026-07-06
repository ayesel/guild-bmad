You are running in Deep Research mode. Do NOT ask me any clarifying questions — the scope is fully specified below. Where something is genuinely ambiguous, state your assumption in one line and proceed. Browse widely, prefer primary and recent sources, and cite every non-obvious claim.

# GUILD INTERACTION-FACTORS RESEARCH (v1 — 2026-07-05)

The prompt that maps the FULL factor-space of superb interaction — everything an
AI must consider (and, wherever possible, MEASURE) about what happens **over
time** when a user acts: micro-interactions, motion as communication, flow
dynamics, feedback loops. Third leg of the factors triptych: `UI-FACTORS` =
space (the rendered surface), `IA-FACTORS` = structure, this = **time**. Same
per-factor contract. Paste into a deep-research session or run as an
adversarially-verified multi-agent workflow. Output lands at
`docs/guild/decisions/interaction-factors-research.md`; its verdict becomes the
spec for the next generation of Rogue/Mage interaction gates AND the required
fields on Rogue's flow artifacts.

---

## THE QUESTION

**What is the complete set of factors an AI needs to consider to design superb
interaction — behavior over time — and for each factor, how can an AI that can
DRIVE the interface (event-listener introspection, runtime traces, frame
captures, scripted input) verify it programmatically?**

Not "what makes interactions feel good" as prose. The deliverable is an
*operational factor taxonomy*: evidence, machine proxy, thresholds, honest
tier, named failure. Note the widened instrument set: unlike the rendered-
surface run (DOM + styles + screenshots), this domain's proxies may drive the
app — dispatch events, record frame sequences, diff state before/after input,
trace focus. A check that requires driving is still MEASURE if deterministic;
needing to *judge* the frames makes it LOOK; needing to *feel* it makes it ASK.

## WHY (the motivating case — calibrate against this)

Guild has an 11-principle motion foundation
(`shared-sidecar/motion-and-interaction-principles.md` v2, 3-model-raid
grounded), motion tokens with an enforcement gate (foundation 4c), an audit-side
envelope (ui-factors factor 16), and a behavior catalog
(`micro-interactions-reference.md`). **And the owner still reports products
that feel clunky, and rates motion / micro-interactions / flow interactions as
Guild's weakest layer.** The rendered-surface research already named this
failure class: principles without per-factor contracts don't gate anything.
Today nothing verifies:

- that every state transition in a shipped flow was *designed* (motion or an
  explicit cut) rather than defaulted;
- that animation never blocks input;
- that focus lands correctly after a route/modal/accordion change;
- that a destructive action offers undo instead of a confirm wall;
- that an async action acknowledges input within ~100ms;
- that a drag can be cancelled mid-gesture.

Motion is applied as a polish pass after static design instead of specified
with the flow — the Nourish D3 motion micro-pass had to generate variants
post-hoc for exactly this reason. Assume more dimensions exist than listed
below; enumerate the space so interaction stops being the last-designed,
never-gated layer.

## ALREADY KNOWN (baseline — do not re-derive; extend past it)

- **The 11 motion principles** (sidecar v2): job-or-cut purpose taxonomy,
  signature easing family (standard/enter/exit/emphasized), duration scales
  with distance, asymmetric enter/exit (exit ≈ enter × 0.75), linear only for
  loops. Reference, don't repeat — your job is the *contract layer* on top.
- **Token + envelope enforcement**: foundation 4c (tokenized motion, no raw
  transitions, reduced-motion branch, per-primitive state coverage) and 4d.6
  (duration envelope: flag >400ms, none >500ms standard).
- **Audit-side factors already reconciled** (`ui-factors-research.md`): factor
  16 (durations/easing/reduced-motion presence — MEASURE; purpose — LOOK) and
  factor 9 (loading/progress honesty, Nielsen 0.1/1/10s). Extend into
  *choreography*; don't re-gate presence.
- **LOOK surface exists**: `/guild-agent-mage WA` (watch) captures and
  critiques motion on the running artifact.
- **Artifact fields exist but are ungated**: state-diagram / user-flow /
  interaction-map templates carry transition/motion fields; nothing requires
  they be filled or checks them against the build.

## THE FACTOR SPACE (starting scaffold — extend, reorganize, and prune with evidence)

1. **Micro-interaction anatomy** — Saffer's trigger → rules → feedback →
   loops/modes as a completeness check per interactive element; designed vs
   browser-default detection.
2. **Feedback immediacy & channels** — input acknowledged <100ms (even when
   the operation is slow); optimistic vs pessimistic UI decision rules; which
   channel (visual/haptic/audio) per event class.
3. **Undo over confirm & forgiveness** — reversibility architecture;
   destructive-action patterns (undo window, soft delete, type-to-confirm
   reserved for catastrophic); confirm-wall smell.
4. **Direct manipulation feel** — drag thresholds, momentum/physics, snap
   targets, mid-gesture cancel affordances, drop-target signifiers.
5. **Choreography & stagger** — order of appearance encodes hierarchy;
   origin-aware motion (things come from where they live and return there);
   stagger presence and rhythm on list/grid entrances.
6. **Spatial continuity & shared elements** — object permanence across
   screens; container transforms; does the spatial model survive navigation.
7. **Transition coverage — the state-pair matrix** — for every reachable state
   pair in the flow artifact: designed motion, explicit cut, or UNSPECIFIED
   (the defect). The artifact-to-build diff: transitions specified in the
   state diagram vs present in the build.
8. **Interruptibility & input-blocking** — animations never gate input;
   pointer/keyboard events land mid-animation; rapid-fire input coalesces
   sanely; no `pointer-events: none` windows on standard transitions.
9. **Focus & accessibility through time** — focus handoff on route/modal/
   disclosure transitions; scroll restoration; reduced-motion as a *designed
   choreography branch* (preserves feedback, not deletes it); live-region
   announcement timing; WCAG 2.3.3 animation-from-interaction.
10. **Latency choreography** — beyond indicator presence (already gated):
    skeleton→content sequencing, progressive rendering order (most important
    first), layout stability during arrival (CLS as an interaction defect).
11. **Input-modality parity** — keyboard equivalents for every pointer flow;
    gesture ↔ visible-control parity; hover-dependent interactions degrade on
    touch.
12. **Form interaction timing** — validate on blur vs keystroke vs submit;
    error appearance/clearance timing; forgiving input formats; focus-to-error
    behavior on failed submit.
13. **Flow-level dynamics** — momentum across steps (auto-advance vs explicit
    continue), context preservation (entered data survives back/refresh),
    back-button integrity, step-transition consistency.
14. **Signature-moment budget** — where personality motion is *spent*; one
    hero moment per surface vs ambient everywhere; the rationing rule as a
    countable budget.
15. **Sound & haptics** — event classes that warrant them; parity with visual
    feedback; mute-by-default norms. (Flag surface-specific.)

## PER-FACTOR CONTRACT (every factor carries ALL five)

- **(a) Evidence** — primary sources with verbatim quotes (Saffer
  *Microinteractions*, Norman, Material motion spec, IBM Carbon motion, Apple
  HIG (Motion + Feedback), W3C WCAG 2.3.3/2.2.2, NN/g animation & response-time
  research, Val Head, Willenskomer's UI-animation principles, Emil
  Kowalski/animations.dev, peer-reviewed perceived-performance and gesture
  studies). Blog-only claims flagged weak.
- **(b) Machine proxy** — the concrete runtime computation (e.g.,
  "interruptibility = dispatch pointerdown at t=50ms into every entrance
  transition; defect if the event does not reach the target"; "transition
  coverage = state-pair matrix from the flow artifact diffed against observed
  DOM mutations under scripted traversal"). If the only proxy is human feel,
  say so.
- **(c) Thresholds** — numeric pass/flag values with source (100ms
  acknowledgment, envelope bounds, stagger bands), or "no agreed threshold"
  stated plainly.
- **(d) Check tier** — MEASURE (deterministic, incl. deterministic-under-
  driving) / LOOK (frame sequences judged against a rubric — the `/guild-agent-
  mage WA` lane) / ASK (felt quality). Be honest: "feels responsive" is ASK;
  "acknowledged <100ms" is MEASURE. Miscategorizing is how motion audits pass
  while products feel clunky.
- **(e) The failure it catches** — a concrete named failure (use the clunk
  reports and the post-hoc Nourish D3 motion pass where they apply).

## SYNTHESIS DELIVERABLES (in this order)

1. **Verdict** — the shape of the interaction factor space and the single
   highest-leverage gap in a tokens-plus-envelope-only motion practice.
2. **Ranked taxonomy** — every factor scored (impact × machine-checkability)
   with the full contract.
3. **The gate spec** — ordered checks: what blocks vs advises; which run
   static (artifact/DOM), which require driving the app, which are frame-judged
   LOOK; which existing gates each extends (foundation 4c/4d, responsive-scan,
   auto-critique/WA, completeness-gate).
4. **The artifact spec** — what Rogue's state-diagram / user-flow /
   interaction-map artifacts must REQUIRE per state pair and per interactive
   element (transition spec, feedback spec, reversibility class, modality
   parity note) so interaction is designed at flow time, not applied as
   polish. This is the process fix: fields become required, and the
   artifact-to-build diff becomes gateable.
5. **The eyes-only residue** — what only humans can feel (and which practice
   covers each: WA watch session, owner pick, user test), bounded and named.
6. **What didn't survive** — interaction folklore that fails verification, and
   where authoritative sources genuinely disagree (duration norms already
   documented as contradictory — extend to gesture thresholds, validation
   timing, optimistic-UI boundaries). Surface disagreements, don't average.

## DISCIPLINE (same bar as the ui-factors and mental-model runs)

- Adversarial verification: no claim ships without independent verifiers
  trying to refute it; vote counts and confidence per finding.
- Primary sources over summaries; verbatim quotes; note dates — motion
  guidance drifts across design-system versions (already caught once).
- Prefer factors that generalize across surfaces; flag surface-specific ones
  (sound/haptics, gesture-heavy mobile).
- Do not pad: no real proxy or honest tier = reported as such. The residue
  list is a first-class output — Guild needs to know exactly where a human
  watching the running artifact remains mandatory.

---
REQUIRED OUTPUT: follow the SYNTHESIS DELIVERABLES order in the specification
above EXACTLY (verdict -> ranked taxonomy with the full five-part per-factor
contract -> gate spec -> artifact spec -> eyes-only residue -> what didn't survive /
source contradictions). End with a numbered Sources list; every load-bearing
claim cite-linked. Markdown. Length: whatever rigor requires - do not pad,
do not truncate.
