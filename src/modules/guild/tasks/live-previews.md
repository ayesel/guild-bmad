# Executable Prototypes Early (live previews)

**GUILD-7 · P3.** Bolt/Lovable/v0 prove running artifacts beat static mockups for
critique + stakeholder confidence. Guild already has Playwright/atrium capture —
feed it real prototypes. Owner: Rogue + Mage + Healer. Treat every artifact as
executable as early as possible.

## What
1. **Designate "key flows"** (Rogue) — the handful that carry the product.
2. **Emit a runnable artifact ASAP** (Mage) — a prototype via `/guild-agent-rogue EX` (export-react) or a Storybook story — before polishing static mocks.
3. **Record the preview** — `preview_uri` in `docs/guild/artifacts.yaml` + the story's `guild.preview_url` (GUILD-17).
4. **Auto-capture + QA the RUNNING artifact** — Playwright/atrium captures it (`/guild-agent-mage AC`, auto-critique); Sage runs calibrated QA (GUILD-4) against the live prototype, measuring real computed values, not eyeballing a PNG.
5. **Critique references the running artifact**, not just a static image.

## Done when
- Designated key flows emit a runnable prototype or Storybook story.
- The prototype is auto-captured by Playwright and run through Sage QA.
- Critique references the running artifact, not a static image.
- TEST: an ephemeral dev server / Storybook serves the flow; preview_url lands on the story; Playwright captures it for QA.
