# Quickstart — Guild in 15 minutes

You're going to install Guild into a small React app, run one phase of its
foundation-first pipeline, and see real, machine-checkable design artifacts come
out. No prior reading required.

By the end you'll have:
- A real `tokens.json` (W3C DTCG) in your project, with measured contrast pairs
- Three primitive components (`Button`, `Input`, `Card`) binding only to those
  tokens — never raw hex/px
- A foundation-gate report — pass/fail with reasons
- A clear next step into the rest of the pipeline

Total active time: ~15 minutes. (The rest is the agent thinking.)

If you'd rather *just look at the output* before installing anything, jump to
[examples/streak-habit-tracker/](../examples/streak-habit-tracker/) — that's a
finished Guild run on a small habit-tracker app. Skim its
`guild-output/guild-artifacts/` and you'll see what Guild actually produces.

---

## 0. What you need

- **Claude Code** installed (the CLI). Cursor/Gemini also work but Claude Code
  is what this walkthrough assumes — fewest moving parts.
- **Node 18+** (for the npm installer).
- A project to install Guild into. **A fresh empty folder is fine** — the
  installer creates everything Guild needs without touching the rest of your
  codebase.
- **No** Figma or BMAD subscription required for this quickstart.

## 1. Install Guild into your project

```bash
cd /path/to/your-project   # or any empty folder for now
npx @ayesel/guild
```

The installer auto-detects whether BMAD is present (it won't be — that's fine)
and installs Guild in standalone mode. It creates:
- `_bmad/guild/agents/` — the 8 specialist agents + Guild Master
- `.claude/commands/` — slash commands for everything
- `src/modules/guild/` — task files, templates, workflows
- `guild.config.yaml` — the one knob you might tune

It does **not** modify anything else.

Verify it landed:

```bash
ls .claude/commands/ | grep guild- | head
cat guild.config.yaml
```

> **Heads up:** if you don't have Claude Code installed yet, install it first
> (`npm install -g @anthropic-ai/claude-code` or per your platform). Guild is
> a framework that runs *inside* a coding-agent CLI; it isn't a standalone tool.

## 2. Open Claude Code in your project

```bash
claude
```

You should see Claude Code's TUI. Type `/help` and you'll see Guild commands
mixed with Claude's built-ins. If you see `guild-master`, `guild-design-direction`,
`guild-design-sprint`, etc. — install worked.

## 3. Run **Phase 0 — Design Direction**

This is the only phase you'll do in the quickstart. It elicits taste before
*anything* visual is generated, so the system isn't generic averaging.

In Claude Code:

```
/guild-design-direction
```

Mage (Guild's visual designer agent) will load and ask you 6 short questions:
- Anchor reference — the product you'd love to feel like (e.g. Linear, Notion,
  Stripe). Skipped if you don't have one.
- Personality — three adjectives (e.g. "focused, crisp, calm").
- Density — sparse / balanced / dense.
- Motion energy — minimal / subtle / lively / playful.
- Color story — your one anchor hue, the temperature, and what to avoid.
- What to avoid — three things you've seen in bad products that you don't want.

Answer them like you'd answer a senior designer over coffee. Two-line answers
are fine.

When you're done, Mage writes
`guild-output/guild-artifacts/design-direction-brief.md`. **Open it.** That's
the artifact every downstream agent reads before doing any visual work.

## 4. Run **Phase 0.5 — System Foundation**

Now build the system the rest of the pipeline binds to:

```
/guild-agent-sage DSF
```

Tinker (design system engineer) reads your design-direction brief and produces:
- `src/system/tokens.json` (DTCG, primitive + semantic tiers)
- `src/system/tokens.css` (CSS custom properties for the same tokens)
- `src/system/primitives/` — `Button`, `Input`, `Card`, `Badge` (variants
  drawn from your direction brief)

Then Sage (design QA) runs the **foundation gate**:
- **Contrast audit** on every semantic fg/bg pair (with the "green-trap" check
  for accessible-looking-but-failing greens)
- **Motion coverage** on every primitive's interactive states (default / hover
  / focus / active / disabled, + a `prefers-reduced-motion` branch)

If the gate **fails**, Sage tells you exactly which token pair fails and why,
and recommends the fix at the **canonical source** (the token), not patched
on a component. If it **passes**, you're set.

The gate report lands at
`guild-output/guild-artifacts/design-system-foundation.md`. Open it. That's
the moment Guild's value proposition becomes concrete — a measured,
machine-checked design system you'd defend to a senior reviewer.

## 5. From here

You can stop here and use the tokens + primitives in any UI you build. Or
keep going:

```
/guild-design-sprint
```

Runs the full adaptive pipeline — Phase 0 → 0.5 → research → interaction →
visual → content → QA → dev handoff. ~15 steps. Auto-detects whether your
project is greenfield or brownfield, with or without BMAD.

Other useful next moves:
- `/guild-quest` — a more guided variant that does the same with verbose
  checkpoint-resume and fail-loud phase verification.
- `/guild-agent-mage` — load the visual-designer agent directly for ad-hoc
  critique or polish (try `/guild-critique` against a running app — Mage will
  use Playwright or your in-CLI browser to *measure* values, not eyeball them
  — that's a deliberate discipline, see
  [docs/multi-model-bakeoff.md](multi-model-bakeoff.md)).
- `/guild-agent-cartographer` — for information architecture work (sitemaps,
  content models).

## When something doesn't work

- **`npx @ayesel/guild` fails with "package not found":** check that the
  package is published (it's a recent ship — if you get this, the install
  step in the README is what you want as a fallback: `git clone` + `cp -r`).
- **Slash commands don't appear in Claude Code:** make sure you're running
  `claude` from the directory you installed into. Slash commands are
  per-project.
- **Foundation gate fails contrast:** that's working as intended. Read the
  report — it'll tell you which semantic token pair fails and recommend a
  token-level fix. Don't patch the component.
- **Compiled agent menu items missing a `target=`:** an external BMAD compiler
  has historically dropped these. Run `./scripts/validate.sh` — it'll catch
  the regression. See CLAUDE.md's *Maintenance* section.
- **Designed for Cursor or Gemini, not Claude Code:** the same `.claude/`
  commands are mirrored to `.cursor/` (`.md`) and `.gemini/` (`.toml`). They
  should work identically; the install script auto-syncs.

## Next reads

- [Pipeline guide](pipeline.md) — full walkthrough of the 12-phase
  (greenfield + BMAD) pipeline with quality gates explained.
- [Multi-model bake-off](multi-model-bakeoff.md) — empirical evidence for
  when to raid (mage-raid / ranger-raid) vs run solo, and which engine for
  what (Claude / Codex / Antigravity).
- [examples/streak-habit-tracker/](../examples/streak-habit-tracker/) — a
  finished Guild run on a small React app. Skim the
  `guild-output/guild-artifacts/` folder to see real Guild output.
