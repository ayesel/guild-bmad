# Brand System & Handoff Reference

How brand identity is encoded once and rendered everywhere — tokens, the three-tier model, and the surface-agnostic handoff including the Guild gate role over Claude Design.

## The Encoding Layer: Design Tokens (W3C DTCG)

- Brand identity is encoded surface-agnostically as **design tokens** in the **W3C Design Tokens Community Group (DTCG)** format. First **stable version (2025.10) shipped 2025-10-28**.
- Tokens are the **single source of truth** for colors, typography, spacing, and other decisions; **one token file generates platform-specific code for iOS, Android, web, and Flutter.**
- **File format:** JSON documents. MIME `application/design-tokens+json`; extensions `.tokens` or `.tokens.json`. `$`-prefixed keys: `$value` (the value), `$type` (the type), `$description` (docs).
- **Normative token types** include Color, Dimension, Font family, Font weight, Duration, Cubic Bézier, Number, plus composites Border, Shadow, Stroke style, Transition, Gradient, and Typography.
- Caveat: DTCG is a **Community Group spec, not a formal W3C Recommendation** — names/conventions are current but could still evolve. Verify against designtokens.org before encoding.

## The Three-Tier Token Model

Each tier builds on the last (Figma):

1. **Primitive / global** — raw values (`blue-500: #1A73E8`). No meaning, just the palette.
2. **Semantic / alias** — meaning-bearing, references a primitive (`action-color → blue-500`). The middle layer; "semantic" and "alias" are used synonymously.
3. **Component** — scoped to a component (`button-bg → action-color`). Often optional.

- **Brand-level decisions live at primitive + semantic.** The brand defines the palette and the *roles*; product teams extend into component tier.
- **Brand color role ≠ functional/semantic role:** brand roles (primary/secondary/accent) express identity; functional roles (success/warning/danger/info) express system state. Keep them distinct token sets — a brand accent is not a "success" color.

## Cross-Surface Handoff (how tokens actually travel)

- **DTCG JSON** is the vendor-neutral interchange — shares the visual language reliably across design tools, codebases, and platforms; unlocks interoperability and theming that cascades global → semantic → component.
- **Figma Dev Mode** emits CSS custom properties (`color/action/primary` → `--color-action-primary`); **REST API** pulls current values (Variables API is Enterprise-gated).
- The Enchanter produces tokens at the brand tier; downstream surfaces (Figma, code, AI design tools) consume them.

## The Claude Design Contract (Guild-specific — DECIDED)

Brand source-of-truth flow, to avoid two competing brand authorities:

```
Enchanter (brand intent / DNA)
   → seeds Claude Design onboarding
       → Claude Design emits the concrete token set
           → Guild consumes & GATES it
               → implementation
```

- **Enchanter defines brand *intent*, not the final tokens.** Claude Design auto-applies team colors/typography/components during onboarding and emits the concrete token set. Enchanter is the upstream authority; Claude Design materializes it. They are **not two independent brand authorities.**
- **Guild's role is the GATE, not the generator.** Auto-generation is a *defect amplifier* — a failing-contrast token gets faithfully stamped across every artifact (consistency ≠ correctness). Claude Design's a11y review is **opt-in**; Guild turns it into a hard checkpoint.
- **Two gate checkpoints:**
  1. **At Claude Design onboarding** — run the contrast-aware foundation audit on the auto-built system *before* it propagates to artifacts. Catch the bad token at source.
  2. **At handoff bundle → Claude Code** — the bundle is a **tar archive + README** (machine-readable component spec, the tokens actually used, layout hierarchy, referenced assets; reads CSS tokens / Radix / Tailwind scales). Validate it materializes as real tokens + primitives, screens compose them at 0-drift, and it clears contrast.
- Caveat: as a research-preview web product, the Claude Design handoff is currently a **manual export → import** step, not yet an automated `/guild-quest` stage.

## Brand Guideline Document & Asset Library

- The brand guideline doc is the human-readable companion to the tokens: positioning + attributes, logo usage & clear-space, color (with roles + contrast notes), type (with licensing), iconography & illustration rules, voice & tone.
- The asset library organizes the actual files (logo lockups, icon set, illustration components) with naming + versioning so handoff is unambiguous.

---

### Sources
- W3C DTCG announcement (2025-10-28) + designtokens.org Format Module (primary)
- Style Dictionary — DTCG support (primary)
- Figma — Design tokens / three-tier model & Dev Mode (primary)
- Guild project memory — Claude Design integration decision (gate harness role, tar bundle, onboarding/handoff checkpoints)
