# Illustration Systems Reference

How to define a reusable illustration style that survives multiple illustrators and scales across surfaces. Grounded in IBM Design Language, Indeed, and GitLab Pajamas.

## Define the Style as a Named Principle Set

- An illustration *system* is governed by a small set of **named principles** that constrain all output regardless of size or medium — not a folder of one-off drawings.
- IBM's five: **Engineered, Clear, Nimble, Diverse, Delightful.** Each is a rule the artist applies, not a mood word.
  - **Engineered** = built on a precise grid with consistent shapes, angles, and corner radii (angles in 15°–90° increments); only essential, non-decorative elements.
  - **Clear** = level-of-detail discipline is explicit — strip anything that doesn't carry meaning.

## Construction Rules (the part that keeps illustrators consistent)

- **One base grid across all canvas sizes.** IBM line style: a **4px base unit, snap-to-grid on every canvas size.** This is what makes two illustrators' output look like one system.
- **Cap the line-weight vocabulary.** IBM: **no more than four distinct line weights**, and avoid weights "too similar" to each other (they read as inconsistency, not nuance).
- **Define discrete named styles under one aesthetic.** IBM codifies Line / Flat / Isometric as named, reusable styles that still share the parent look.
- **Three governance pillars** (Indeed): every illustration is checked against **style, location, and purpose** — does it match the style rules, does it belong where it's used, does it serve a purpose.

## Color & Shading Inside Illustration

- **Keep shading on-palette.** Indeed replaced blending modes with **two-step palette gradients** so illustrations can never drift off the brand color set.
- **Codify shadows as a shared effect-style library.** Indeed keeps shadow as a Figma effect style (blur + directional X/Y), which makes "translation to code much simpler" (per their engineer). Encode lighting as styles, not per-illustration choices.

## Scaling & Reuse

- **Use fixed, named size tiers — never arbitrary scaling.**
  - Indeed spot tiers: 100×80 / 150×120 / 200×160 / 300×240.
  - GitLab Pajamas: 288 / 144 / 72 / 36, each tied to a usage context. (Exact numbers are studio-specific — adopt the *pattern*, set your own tiers.)
- **One-to-many modular components, not one-to-one.** GitLab builds dozens of small reusable Figma components composed into illustrations, rather than drawing each scene from scratch. This is what makes a system scale.

## Handoff Notes

- Illustration travels to code through: the shared Figma effect-style library (shadows/lighting), the on-palette gradient rules, and the named size tiers as component variants.
- The level-of-detail discipline matters most at the smallest tier — define what gets dropped as the illustration shrinks.

---

### Sources
- IBM Design Language — Illustration overview & Line style (primary)
- Indeed Design — Building a scalable illustration system (primary)
- GitLab Pajamas — Illustration (primary)
