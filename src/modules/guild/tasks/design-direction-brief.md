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

#### 4. Motion energy
> "How alive should this feel? Still and surgical (no motion, instant state changes, Bloomberg-terminal feel) — subtle and refined (transitions, hover states, but nothing showy) — or expressive and animated (loaders that delight, micro-interactions, things that move)?"

Capture: still / subtle / expressive.

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

## Motion energy
**{still | subtle | expressive}**

## Color story
- Temperature: {warm | cool | neutral | high-contrast | monochrome | color-rich}
- Reference palettes: {palette 1}, {palette 2}

## What to avoid
- {anti-pattern 1}
- {anti-pattern 2}
- {anti-pattern 3}

## How downstream agents should use this

**Mage (visual design):** Anchor visual choices in the reference + adjectives. When choosing between two patterns, pick the one closer to the anchor.

**Rogue (interaction):** Density + motion energy directly govern layout decisions and transition style. Default to the user's stated preference; deviate only with explicit reasoning.

**Warlock (content):** Personality adjectives govern voice. Avoid generic SaaS tone unless explicitly asked.

**Ranger (research):** Use the anchor reference as the primary visual benchmark in competitive audits — don't average across 5 products, weight the anchor heavily.
```

## Quality checks
- [ ] All 6 questions answered
- [ ] Anchor reference is ONE product (not a list)
- [ ] Personality adjectives are specific (not "modern", "clean")
- [ ] Density and motion explicitly chosen
- [ ] At least 2 anti-patterns captured
- [ ] User has explicitly approved the synthesized brief
- [ ] Artifact saved to `{output_root}/guild-artifacts/design-direction-brief.md`
