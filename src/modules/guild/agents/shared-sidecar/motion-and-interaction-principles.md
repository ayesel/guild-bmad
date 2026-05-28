# Motion & Micro-interaction Principles — the foundation layer (v2, research-grounded)

Motion is the most-skipped layer of a design system and the one most responsible for whether a product
feels **crafted or generic**. Default symmetric `ease-in-out` at 200ms on everything is the "AI did it" tell.
These principles make motion *yours*, consistent across screens, and portable across every app built on this
foundation.

> **Provenance.** v2 is grounded in a 3-model Ranger research raid (Claude / Codex / Gemini, independent,
> cited) — see `shared-sidecar/motion-research-synthesis.md`. Findings that all three models reached
> independently are HIGH confidence; the exact *signature curve* is a design-direction decision (set in the
> brief), not a research finding. Companion to Mage's `micro-interactions-reference.md` (behavior catalog).

## The invariant

The spine is always active regardless of design surface: **tokens + primitives + contrast gate + coherence
gate + this motion layer.** The foundation gate (`design-system-foundation.md` step 4c) enforces the
tokenized parts; this doc governs the judgment parts.

## The 11 principles

1. **Motion has a job, or it's cut.** Every motion serves **feedback** (action received), **continuity**
   (object identity across a change), **orientation** (spatial/hierarchical relationship), **status**
   (loading/progress), or **personality** (brand — lowest priority, *only* optional job, rationed). No job =
   decoration = drift. *[All 3 models; Apple HIG, Material informative/focused/expressive, Carbon, Atlassian.]*

2. **One signature easing identity, expressed as a family of 3.** Easing is the brand carrier and the
   highest-leverage portability decision. But one curve can't serve both enters and exits — so the signature
   is a *family*: `standard` (within-screen), `enter` (decelerate), `exit` (accelerate), plus an `emphasized`
   curve for rare hero moments. Both Material 3 and Carbon ship exactly this shape. **The actual curve values
   are chosen in the design-direction brief** — the structure is fixed here, the identity there.

3. **Duration scales with distance and surface — not taste.** Bigger move / larger surface → longer, capped.
   Role-based bands (see tokens). *[Material & Carbon both mandate dynamic duration; "adjust by distance,
   velocity, surface change."]*

4. **Enters and exits are asymmetric.** Enter = ease-**out** (decelerate in, fast pickup reads responsive);
   exit = ease-**in** (accelerate out, get out of the way); `linear` **only** for continuous loops (spinners).
   Symmetric `ease` is banned as a default. Exits run faster than enters (**≈ enter × 0.75**). *[CSS-Tricks,
   animations.dev, Material, Carbon, Atlassian — unanimous.]*

5. **Choreograph: stagger, don't dogpile.** Multiple elements entering (lists, the comparison cards) stagger
   ~20–50ms in reading order, total bounded by the ceiling. Surfaces **emerge from their trigger** (origin-
   aware), not a center fade. One focal/shared element per transition. *[Material & Carbon choreography.]*

6. **Two registers, one identity.** Expose a **functional/fast** register and an **expressive/slow** register
   (Carbon productive/expressive; Material standard/emphasized). Product teams choose *register*, not raw ms.

7. **Feedback is instant; delight is occasional.** Acknowledge input ≤100ms (RAIL/Nielsen 0.1s); routine
   interaction feedback <150ms; it's never skippable. Personality motion (reward, streak, comparison reveal)
   is rationed to meaningful moments. *[RAIL, NN/g response limits, Atlassian "high-frequency <150ms".]*

8. **State coverage is non-negotiable.** Every interactive element defines `default, hover, focus-visible,
   active/pressed, disabled, loading` (+ `selected`/`error` where relevant). Missing states are the #1 source
   of "unfinished/janky." Hover is desktop-only and never the sole signal; focus must be visible *without*
   motion (WCAG 2.4.7). *[Saffer model; Apple/Atlassian/Carbon component guidance.]*

9. **Reduced motion is a designed branch, not a kill switch.** Honor `prefers-reduced-motion`: replace
   movement/scale/parallax with an **opacity cross-fade (≤120ms)** — preserve the *fact* of the change, remove
   the vestibular trigger. Kill outright: parallax, auto-advancing carousels, spin/zoom/3D, scroll-jacking.
   Keep: instant feedback, focus rings, essential progress. *[W3C 2.3.3, MDN, Apple reduced-motion criteria.]*

10. **Animate compositor-only properties.** `transform` + `opacity` for anything that moves or repeats; never
    animate layout (width/height/top/left) or `transition: all`. 60fps or it reads cheap. *[web.dev smoothness.]*

11. **Tokenize all of it, semantic over primitive.** Durations, easings (incl. signature), stagger, and the
    reduced-motion branch are tokens, bound *in primitives*, never re-authored per screen. Choose by intent
    (`motion.surface.enter`) over raw values. Motion drift = inconsistent timing/feel across screens; the cure
    is the same as color. *[Atlassian semantic tokens, Carbon, Salesforce, W3C DTCG.]*

## Required motion tokens (the enforceable substrate)

Primitive duration ladder — compact, role-based, **hard ceiling ~400–500ms** for discrete UI motion
(Material: ">400ms feels too slow"; NN/g: "500ms is a real drag"):
```
--duration-instant  70ms    press / hover / toggle / checkbox      (Nielsen 0.1s; Carbon fast-01 = 70ms)
--duration-fast     150ms   tooltip / dropdown / small expand      (Atlassian interaction band 50–150ms)
--duration-base     250ms   modal / sheet / card enter             (NN/g 200–300; Material medium)
--duration-slow     350ms   large / complex on-screen change       (Material 375ms full-screen)
--duration-slowest  500ms   full-screen / route — HARD CEILING
rule: exits ≈ enter × 0.75; duration steps UP with travel distance/area.
```
Easing family (cubic-bezier for CSS/Android/iOS portability; **actual signature set chosen in the brief** —
these are evidence-based defaults from the Material/Carbon families):
```
--ease-standard   cubic-bezier(0.2, 0, 0.2, 1)    within-screen moves  (the signature, used ~90%)
--ease-enter      cubic-bezier(0, 0, 0.2, 1)       decelerate in  (X1=0 → instant pickup)
--ease-exit       cubic-bezier(0.4, 0, 1, 1)       accelerate out (X2=1 → snappy departure)
--ease-emphasized cubic-bezier(0.2, 0, 0, 1)       hero / expressive moments only
--ease-linear     linear                           continuous loops ONLY (spinners, shimmer)
--stagger         20–50ms                          list/card sequence offset
```
**Springs:** opt-in token group for **gesture-driven / interruptible** surfaces only (swipe-to-dismiss, drag).
Do NOT use for routine discrete transitions — spring params don't port 1:1 across CSS/native, so bezier is the
portable default. *(Open question per the raid.)*

## Micro-interaction standards (component layer)

| Element | Required motion |
|---|---|
| Button | press feedback (scale/opacity) ≤120ms; loading spinner state; disabled inert |
| Toggle / Switch | thumb travels on `--ease-standard`; state reads instant |
| Input | focus-ring transition; error transition; helper/error reveal (motion never the sole error signal) |
| Dialog | backdrop fade + content scale-from-~96% & fade in; **exit faster** |
| Sheet / Drawer | slide on signature ease + backdrop fade; exit accelerates |
| List / Cards (comparisons) | staggered enter; reorder via FLIP/transform; selection feedback |
| Toast | enter from edge (signature), auto-dismiss exit; reduced-motion → fade only; >5s auto needs pause/stop/hide |
| Skeleton | shimmer is `--ease-linear`/looping; swap to content via crossfade |

## Accessibility is Level A, not a nicety

- **WCAG 2.2.2 Pause/Stop/Hide (Level A — mandatory):** auto-starting motion that lasts >5s and runs alongside
  other content MUST have a pause/stop/hide control (spinners that loop, carousels). This is baseline conformance.
- **WCAG 2.3.3 Animation from Interactions (AAA):** non-essential interaction-triggered motion must be disable-able.
- Provide an **in-app reduce-motion control**, don't rely solely on the OS setting.
- Motion is **never the sole carrier of meaning** — pair with color/text/icon/state.

## Who reads this

- **design-direction-brief** — captures the *taste* (signature feel → actual curve values, hero moments,
  reduced-motion posture, register lean: functional-Carbon vs expressive-Atlassian).
- **Mage** — applies the micro-interaction standards + state coverage when designing/critiquing.
- **Rogue** — choreography/continuity in flows + state diagrams.
- **Sage (foundation gate, step 4c)** — enforces: motion tokens present (incl. a real signature, not default
  ease-in-out), bound in primitives (no raw transitions), full state coverage, reduced-motion branch exists,
  auto-motion >5s has pause/stop/hide.
