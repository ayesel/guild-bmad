---
artifact: ranger-raid-comparison
status: synthesized
created: 2026-05-27
author: Ranger (3-Model Raid — Claude / Codex / Gemini)
method: Research synthesis + competitive/standards review (secondary)
confidence: high (structure/values) · medium (exact signature curve + stagger numbers)
models: [claude, codex, gemini]
sources_files: [~/motion-raid-claude.md, ~/Developer/motion-raid-codex.md, ~/Developer/motion-raid-gemini.md]
---

# 🔍 Ranger Raid: Motion Design & Micro-interactions for UX

## Model comparison

| Dimension | Claude (283 ln, 51 URLs) | Codex (233 ln, 156 URLs) | Gemini (84 ln, 16 URLs) |
|---|---|---|---|
| Strongest at | The *why* — FINDING vs INSIGHT discipline, confidence labels, pulled Material 3 + Carbon token values from **source code** | The *what* — most concrete token system (primitive + semantic tables), widest first-party sourcing (Material, Carbon, Atlassian token changelog, Salesforce, MDN) | The *frame* — memorable synthesis ("100ms Gold Window", "spring physics pivot") |
| Easing stance | bezier family is portable default; **springs opt-in for gesture/interruptible only** | bezier family (Carbon productive curves + Atlassian bold curve as emphasis signature) | **springs as the cross-product signature** (`{stiffness:180,damping:20}`) |
| Duration scale | 5-step (70/150/250/350/500, hard 500 ceiling) | 9-step (0/50/100/150/200/250/300/375/400) | 3-step (100/200/400) |
| Notable caveat | flags Doherty 400ms as contested folklore; no proven "optimal duration" | cited Material **m1** (legacy) for some ms values | leanest depth |

## Converging findings (all 3 agreed independently — HIGH confidence)

1. **Motion is functional-first.** Every motion must claim a job (feedback / continuity / orientation / status) before brand/personality (optional, rationed). [Material, Apple HIG, Carbon, Atlassian]
2. **Timing bands:** acknowledge input ≤100ms (RAIL/Nielsen); micro-feedback <150ms; routine transitions ≤~400ms (Material: ">400ms feels too slow"); Doherty ~400ms as a contested *upper bound*. [RAIL, NN/g, Material, Atlassian]
3. **Duration scales with distance/size** — never one constant. [Material, Carbon]
4. **Easing asymmetry:** ease-**out** for entrances, ease-**in** for exits, standard for visible-to-visible, **linear only** for continuous loops (spinners). [Carbon, Atlassian, Material, Apple SwiftUI]
5. **A 3-curve easing family** (standard / enter / exit) + an emphasized/signature curve — both Material and Carbon ship exactly this shape.
6. **Two registers:** a fast/functional vs slow/expressive split (Carbon productive/expressive; Material standard/emphasized).
7. **Choreography:** stagger entrances ~20–50ms, one focal/shared element per transition, surfaces emerge from their trigger (origin-aware). [Material, Carbon, Atlassian]
8. **Saffer micro-interaction model** (trigger/rules/feedback/loops&modes) + full interaction-state coverage (default/hover/focus/active/disabled/loading/selected/error).
9. **Accessibility is architectural, not a toggle:** WCAG **2.2.2 Pause/Stop/Hide is Level A** (auto-motion >5s) and **2.3.3** (AAA, interaction-triggered); honor `prefers-reduced-motion`; reduced-motion **replaces movement with opacity — never deletes feedback**. Vestibular harm is real (parallax/scroll-jack/large zoom). [W3C, MDN, Apple, NN/g]
10. **"AI-default" feel = un-tokenized motion:** `transition: all`, symmetric `ease`, one duration everywhere, center-fades instead of origin-aware, over-animation, animating layout props. Fix = transform/opacity only + tokens. [web.dev, NN/g, practitioner consensus]
11. **Tokenize semantic-over-primitive:** duration scale + easing set as named tokens; choose by intent (`motion.surface.enter`) not raw ms. [Atlassian, Carbon, Salesforce, W3C DTCG]

## Diverging findings (a call was needed)

- **Springs vs bezier as the signature.** Gemini pushes spring-physics as *the* cross-product signature; Claude argues bezier-family is the portable default with springs **opt-in for gesture/interruptible surfaces only**; Codex stays bezier. **Resolution:** go with Claude's framing — bezier family is portable across CSS/Android/iOS (spring params don't translate 1:1, which all three flag as an open question); reserve springs for gesture surfaces. The "spring pivot" is real but is a native-platform trend, not a portable-token decision.
- **Scale granularity.** Resolution: a compact role-based ladder (Claude's 5-step) is more usable as a *foundation* than Codex's 9-step; keep Codex's semantic layer on top.
- **Exact signature curve.** All three differ — because there is no universal answer. **This is a design-direction decision, not a research finding.** The research fixes the *structure* (standard/enter/exit + emphasis) and the *bands*; the actual curve values get chosen in the design-direction brief (step 2).

## Synthesis rationale

Took Claude's rigor + register/ceiling framing as the spine, Codex's concrete semantic-token layer + cited values, and Gemini's spring-opt-in flag and "responsiveness > smoothness" emphasis. Where they diverged (springs, granularity, curve), defaulted to the most *portable* and best-evidenced option, and explicitly punted the one genuinely subjective choice (the signature curve) to the design brief.

## How this changes the draft principles

The research **validated** the draft's structure (signature easing, asymmetric enter/exit, role durations, stagger, motion budget, state coverage, reduced-motion-as-branch, compositor-only, tokenize). It **adds/sharpens:** cited concrete values; the explicit **two-register** model; the cited **≤400ms ceiling**; **WCAG 2.2.2 Level A** auto-motion rule; **semantic-over-primitive** token tiers; signature-as-a-**family-of-3**; **springs opt-in** for gestures; **exits = enter × ~0.75**. → folded into `shared-sidecar/motion-and-interaction-principles.md` v2.

## Open questions (combined)
Spring token portability across CSS/native; empirical duration optimum (no RCT exists — worth a first-party A/B); Doherty primary-source verification; choreography under-tokenized industry-wide; reduced-motion default direction; motion telemetry (frame drops, reduced-motion adoption, time-to-ack).
