# Design Direction Brief

## Purpose
Elicit the designer's taste and visual direction BEFORE any agent generates research, wireframes, or visuals. This is Mage's "interview the human" step — the equivalent of how BMAD's PM and Architect ask structured questions before drafting. Without this gate, agents synthesize from competitor research and produce an averaged "AI dashboard" look. With this gate, they execute against an explicit point of view.

This task is a HARD GATE: do not generate any design artifacts (visual research, wireframes, components, copy direction) until this brief exists.

## When to run
- At the start of `/guild-quest` and `/guild-party-quest` (Phase 0, before Ranger visual audit)
- Standalone via `/guild-design-direction` when the user wants to (re)anchor a project's visual direction
- Re-run if the brief is older than 30 days or the project pivots

## Output
Save to `{output_root}/guild-artifacts/design-direction-brief.md` using the structure below.
This file becomes the `design_direction_brief` Quest Variable referenced by all downstream subagents.

## Execution

Run as Mage. Stay in character. Do NOT generate any visual output during elicitation — this step only collects the user's direction.

### Step 0 — Load existing context FIRST (do not re-ask what's already known) — GUILD-1
Before asking anything, LOAD `docs/guild/context.yaml` (and `{output_root}/guild-artifacts/design-direction-brief.md` if it exists).
- If `context.yaml` `taste_anchors` / `tokens` are populated (design-direction pointer, references, token source), **confirm them in one line ("Using your locked direction: <summary> — still right?") instead of re-eliciting.** Only ask the questions whose answers are missing.
- The Product Baseline is already in `context.yaml` `baseline` (laws + triggers + domain_packs) — never ask the user about generic UX defaults that are encoded there; apply them silently.
- Re-elicit from scratch ONLY when no context.yaml taste_anchors exist or the user says the direction changed. This is the anti-"too-much-prompting" rule: spec once, reuse.
- **GUILD-14 taste model:** also load `docs/guild/taste-model.yaml` (visual density, tone, motion tolerance, brand vocabulary, layout dislikes, reference anchors, a11y priorities) and apply it as retrieved context. As the run infers NEW preferences from accept/reject, write them to `pending_inferred` — they must be confirmed in the GUILD-11 batch review BEFORE they move into durable `preferences` (no silent taste drift). The owner can view/edit/purge the file directly.

### Opening
Greet the user as Mage, briefly explain why this brief exists ("So I'm executing your taste, not averaging from competitors"), and tell them this takes ~3 minutes.

### Elicitation — Ask all 6 questions

Present each question as a numbered prompt. Allow free-form answers OR multiple choice — accept whichever the user prefers. Do NOT batch all 6 in one message; ask one at a time, acknowledge the answer, then proceed to the next. This pacing is what makes the answers thoughtful instead of rushed.

For each question, if the user gives a vague answer ("modern", "clean", "professional"), push once with a clarifying probe ("Modern like Linear-precise or modern like Vercel-playful?"). Do not push twice — the user knows what they want.

---

#### 1. Anchor reference
> "Pick ONE product whose UI you'd be happy to be compared to. Just one — not a list of 5. Could be a competitor, could be totally outside the industry. What's the anchor?"

Capture: product name, optional URL, why it resonates (1-2 sentences).

#### 2. Personality — three adjectives
> "Give me three adjectives that describe how this product should *feel* to use. Avoid vague words like 'modern' or 'clean.' Reach for specifics — confident, restrained, editorial, technical, warm, surgical, cinematic, industrial, gentle, urgent, etc."

Capture: 3 adjectives. If the user gives generic words, probe once.

#### 3. Density preference
> "Where on this spectrum: dense like Linear/Bloomberg/Notion-power-user (information-rich, tight spacing, lots on screen) — or airy like Stripe/Apple/Vercel-marketing (generous whitespace, fewer things per screen, focus on hierarchy)?"

Capture: dense / balanced / airy + 1-line rationale.

#### 4. Motion language (three parts)
> "(a) **Energy** — how alive should this feel? Still and surgical (instant state changes, Bloomberg-terminal) — subtle and refined (transitions, hover states, nothing showy) — or expressive and animated (loaders that delight, things that move)?
> (b) **Signature feel** — is there a motion *fingerprint* you love and want to borrow? e.g. 'Linear's snap,' 'iOS spring/overshoot,' 'Stripe's restraint,' 'macOS genie.' This becomes the `--ease-signature` curve — the single biggest lever against generic feel.
> (c) **Where delight is earned** — which 1–2 moments deserve personality motion (a reward landing, a streak, the comparison reveal), and what should stay quiet? And do you want a strong reduced-motion posture (some users/contexts prefer near-still)?"

Capture: energy (still/subtle/expressive); signature reference (→ proposed easing direction); the 1–2 hero/delight moments; reduced-motion posture. These map directly onto `src/modules/guild/agents/shared-sidecar/motion-and-interaction-principles.md` — the brief sets the taste, that doc + the foundation gate enforce the consistency.

#### 5. Color story
> "Two parts: (a) what's the dominant feeling — warm, cool, neutral, high-contrast, monochrome, color-rich? (b) Are there 1-2 reference palettes I should pull from? Could be 'Arcadia's blues,' 'Stripe's lavenders,' 'Linear's near-black,' a specific Pantone, or a color from a non-software thing you love."

Capture: temperature/feeling, reference palettes (1-2).

#### 6. What to avoid
> "Last one — what would make you cringe if I shipped it? Be specific. Could be a pattern (modal-everything, neumorphism, rainbow gradients), a vibe (corporate-PowerPoint, crypto-bro, generic-SaaS), or a competitor's exact look you don't want."

Capture: 2-4 specific anti-patterns or anti-vibes.

---

### After elicitation

1. Synthesize the answers into the artifact below
2. Show the synthesized brief to the user
3. Ask: "Does this match what's in your head? Anything to refine before I lock this as the direction?"
4. Iterate once if they want changes
5. Save the final version to `{output_root}/guild-artifacts/design-direction-brief.md`
6. Confirm: "Locked. This brief is now the source of truth for Mage, Rogue, and Warlock."

## Output structure

```markdown
# Design Direction Brief — {product_name}

**Date:** {date}
**Designer:** {user_name}
**Status:** Locked

## Anchor reference
- Product: {product_name}
- URL: {url}
- Why it resonates: {1-2 sentences}

## Personality
{adjective 1} · {adjective 2} · {adjective 3}

## Density
**{dense | balanced | airy}** — {rationale}

## Motion language
- Energy: **{still | subtle | expressive}**
- Signature feel: {reference, e.g. "Linear's snap"} → proposed `--ease-signature` direction
- Hero/delight moments: {the 1–2 moments that earn personality motion}
- Reduced-motion posture: {strong | standard}

## Color story
- Temperature: {warm | cool | neutral | high-contrast | monochrome | color-rich}
- Reference palettes: {palette 1}, {palette 2}

## What to avoid
- {anti-pattern 1}
- {anti-pattern 2}
- {anti-pattern 3}

## How downstream agents should use this

**Mage (visual design):** Anchor visual choices in the reference + adjectives. When choosing between two patterns, pick the one closer to the anchor.

**Rogue (interaction):** Density + motion language govern layout, transition style, and choreography. The signature feel and hero moments map to `shared-sidecar/motion-and-interaction-principles.md`; apply its choreography/continuity principles. Default to the user's stated preference; deviate only with explicit reasoning.

**Mage (motion craft):** Translate the signature feel into the `--ease-signature` curve + duration scale, and the hero moments into rationed personality motion, per `shared-sidecar/motion-and-interaction-principles.md`. Apply the micro-interaction state-coverage standards to every primitive.

**Warlock (content):** Personality adjectives govern voice. Avoid generic SaaS tone unless explicitly asked.

**Ranger (research):** Use the anchor reference as the primary visual benchmark in competitive audits — don't average across 5 products, weight the anchor heavily.
```

## Quality checks
- [ ] All 6 questions answered
- [ ] Anchor reference is ONE product (not a list)
- [ ] Personality adjectives are specific (not "modern", "clean")
- [ ] Density chosen; motion language captured (energy + signature feel + hero moments + reduced-motion posture)
- [ ] At least 2 anti-patterns captured
- [ ] User has explicitly approved the synthesized brief
- [ ] Artifact saved to `{output_root}/guild-artifacts/design-direction-brief.md`
