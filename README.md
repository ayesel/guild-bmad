# Guild — a design framework for AI coding agents

**You provide the taste. Guild does the structured work.** A team of specialized
AI design agents (research, IA, interaction, visual, content, QA, dev handoff)
running inside your coding-agent CLI, producing real artifacts you can ship —
not generic mockups. Built for product designers who want AI to handle the
mechanical work without taking the wheel.

> [![status: research preview](https://img.shields.io/badge/status-research%20preview-orange)]() &nbsp;
> Guild is in active development. The internals are validated (`scripts/validate.sh`
> passes 8/8) but the public install story is still being smoothed. See
> [Quickstart](docs/quickstart.md) for what works today.

---

## Why Guild?

Three things every product designer keeps doing manually that Guild absorbs:

- **Audit your design system's foundations before page work** — Guild's *Sage*
  measures every semantic token pair against WCAG AA, catches the "green-trap"
  (greens that look fine but fail contrast), and checks that every primitive has
  hover/focus/active/disabled + a `prefers-reduced-motion` branch. You get a
  PASS/FAIL with reasons, not a vibe.
- **Generate dev-ready specs without rewriting them in Jira** — Guild's *Healer*
  produces handoff bundles in BMAD dev-story format (Given/When/Then, component
  specs with props/states/ARIA, design tokens in W3C DTCG). Stories are
  immediately consumable by an autonomous dev loop.
- **Run heuristic evals against real personas you didn't write yourself** —
  Guild's *Ranger* generates evidence-grounded personas from your project
  context, then runs Nielsen's 10 against your actual screens — and Guild's
  multi-model **Raid** mode runs that same audit through Claude / Codex /
  Antigravity in parallel so different engines surface different findings
  ([empirical evidence](docs/multi-model-bakeoff.md)).

---

## Quickstart

The fastest way to *see what Guild produces* without installing anything:
**[examples/streak-habit-tracker/](examples/streak-habit-tracker/)** — a small
React habit-tracker app with Guild's foundation-first artifacts in place
(`guild-output/guild-artifacts/`). Skim it. That's what comes out the other end.

To install it into your own project, follow the
**[15-minute Quickstart guide](docs/quickstart.md)**. TL;DR:

```bash
# Published as @ayesel/guild — if npx errors with "package not found",
# the publish is in flight; use the manual install below.
cd /path/to/your-project
npx @ayesel/guild
```

Then open Claude Code (`claude`) in that directory and try `/guild-design-direction`
— Guild's *direction-first* gate. It's 6 short questions about taste; 90 seconds
of your time. The next phase (`/guild-agent-sage DSF` — the design-system foundation gate) materializes a real
token set + 3 primitive components binding only to those tokens, and runs the
WCAG + motion gate against them.

**Manual install** (guaranteed to work today, no npm dependency):

```bash
git clone https://github.com/ayesel/guild-bmad.git
cd guild-bmad
bash scripts/install.sh /path/to/your-project --mode guild
```

That's the same installer the npm package wraps — same outcome.

---

## What Guild produces (concretely)

A `/guild-design-sprint` run on a brand-new project generates, in order:

| Phase | Artifact |
|---|---|
| **Discover** (Ranger) | Personas · journey maps · competitive audits · heuristic evals · visual audits (with measured contrast, not eyeballed) |
| **Define** (Cartographer, Mage) | Sitemap · content model · design direction brief (taste locked) · system foundation (DTCG tokens + primitives + gate report) |
| **Design** (Rogue, Mage, Warlock) | User flows (Mermaid) · wireframes · state diagrams · microcopy · error messages · empty states |
| **Quality + Handoff** (Sage, Healer) | Pre-handoff gate report · accessibility audit · component registry · design tokens (DTCG) · BMAD-format Jira stories (G/W/T) |

**Real-world example:** Guild produced **14 artifacts (6,532 lines)** for a
React Native ski-trip app in a single run — 4 personas, 3 redesigned flows, 31
error messages, 15 empty states, 12 sprint-ready stories across 3 epics. See
[examples/streak-habit-tracker/](examples/streak-habit-tracker/) for a smaller,
public reference.

---

## How the pipeline thinks

```
Discover  →  Define  →  Design  →  Quality  →  Handoff
 (Ranger)    (Carto +    (Rogue +    (Sage)      (Healer)
             Mage P0)    Mage +
              Sage P0.5)  Warlock)
```

Two gates frame the visual work:

- **Phase 0 — Design Direction (Mage):** elicits anchor reference, personality,
  density, motion energy, color story, and what to avoid *before* any visuals
  exist. Without this, AI design averages competitors into a generic dashboard
  look. With it, every downstream agent filters its work through your direction.
- **Phase 0.5 — System Foundation (Sage backed by Tinker):** audits the token
  and primitive layer *before* any page-level work begins. If the foundation
  fails contrast or motion coverage, the pipeline stops. Agents cannot inline
  ad-hoc components if the system layer is already solid.

Sage acts as a quality gate throughout: if it returns NO-GO, the pipeline
loops back to the relevant phase.

When [BMAD v6](https://github.com/bmad-code-org/BMAD-METHOD) is detected, the
pipeline extends with PM (story review) → SM (sprint planning) → Dev
(autonomous build), so the design output flows straight into a dev loop.

Full pipeline walkthrough: **[docs/pipeline.md](docs/pipeline.md)**.

---

## The agents

8 specialists plus an orchestrator. Each agent has a focused remit and a
sidecar knowledge base it consults during work.

| Agent | Role | What it does |
|-------|------|--------------|
| **Ranger 🔍** | UX Researcher | Heuristic evals, personas, journey maps, usability tests, competitive + accessibility audits |
| **Cartographer 🗺️** | Information Architect | Sitemaps, content models, navigation models, FigJam composition |
| **Rogue 🔀** | Interaction Designer | User flows, wireframes, state diagrams, task analyses, swim lanes |
| **Mage 🎨** | Visual Designer | Visual hierarchy, spacing, typography, color, micro-interactions, before/after |
| **Warlock ✍️** | Content Strategist | Microcopy, error messages, voice/tone, empty states, onboarding copy |
| **Sage 🛡️** | Design QA | WCAG audits, design-system compliance, pre-handoff gate, Claude Design handoff gate |
| **Healer 📦** | Design Ops | Jira stories (G/W/T), component specs, design tokens (DTCG), handoff bundles |
| **Tinker 🔧** | Design System Engineer | Figma component architecture, variants, variable binding, Storybook/Code Connect parity |
| **Guild Master 🎯** | Orchestrator | Runs the full pipeline; auto-detects greenfield/brownfield, with or without BMAD |

> Tinker and Cartographer are **on-demand specialists** — invoked when the work
> needs design-system or IA work specifically, not fixed steps in the
> sequential pipeline.

Each agent ships with a slash command — `/guild-agent-mage`, `/guild-agent-sage`,
etc. Individual capabilities (like Mage's `/guild-critique` or Ranger's
`/guild-persona-gen`) are also exposed as direct commands, so you don't have to
load an agent just to run one task.

---

## Multi-model — Raid, Quest, Tavern

Guild extends naturally into multi-model workflows. Three patterns:

| Mode | What it is | Command(s) | Requires |
|------|-----------|------------|---------|
| **Raid** | Same brief, multiple engines (Claude / Codex / Antigravity) work in parallel and synthesize. Different engines surface different findings (see [the empirical evidence](docs/multi-model-bakeoff.md)). | `guild-raid`, `mage-raid`, `ranger-raid`, ... | [Atrium](https://atrium.sh) |
| **Quest** | The full multi-phase pipeline. Solo: one model runs all phases. Party: three engines divide labor across phases. | `guild-quest`, `guild-party-quest` | Atrium (party only) |
| **Tavern** | Open multi-model conversation around a topic — brainstorming, critique, exploration. | `bmad-party-mode` | Atrium |

**When raid pays off (empirically):** the 2026-06 bake-off found that for
**visual critique** (`mage-raid`) and **research synthesis** (`ranger-raid`),
different engines surface materially different findings — the union is richer
than any solo run. For taste/prose/orchestration phases (Warlock, Sage,
Healer, Cartographer, Guild Master), solo Claude was as good or better.
**Recommended composition for visual work:** Claude (judgment) + Antigravity
(in-CLI browser → measured/DOM evidence + responsive probing the others can't
do) + Codex (IA/structural framing). The biggest lever for visual quality
isn't model tier — it's whether the agent *measures* values vs eyeballs them.

Full evidence + per-phase engine-fit matrix: **[docs/multi-model-bakeoff.md](docs/multi-model-bakeoff.md)**.

---

## Manual install paths

### Standalone (no BMAD)

```bash
git clone https://github.com/ayesel/guild-bmad.git
cd guild-bmad
bash scripts/install.sh /path/to/your-project --mode guild
# or, fully manual:
cp -r _bmad/guild/ /path/to/your-project/_bmad/guild/
cp -r src/modules/guild/ /path/to/your-project/src/modules/guild/
cp -r .claude/commands/guild-*.md /path/to/your-project/.claude/commands/
cp guild.config.yaml /path/to/your-project/
```

Guild auto-detects that BMAD is not present and runs in standalone mode. Output
goes to `guild-output/`.

**Optional BMAD bundle** (sprint tracking + PM/SM review without a full BMAD install):

```bash
cp -r bmad-bundle/_bmad/core /path/to/your-project/_bmad/core
cp -r bmad-bundle/_bmad/_config /path/to/your-project/_bmad/_config
cp -r bmad-bundle/.claude/commands/bmad-*.md /path/to/your-project/.claude/commands/
```

### Into an existing BMAD project

```bash
git clone https://github.com/ayesel/guild-bmad.git
cd guild-bmad

# Copy ONLY Guild files — do NOT copy bmad-bundle/ (you already have BMAD)
cp -r _bmad/guild/ /path/to/your-project/_bmad/guild/
cp -r src/modules/guild/ /path/to/your-project/src/modules/guild/
cp -r .claude/commands/guild-*.md /path/to/your-project/.claude/commands/
cp guild.config.yaml /path/to/your-project/
```

Then add the Guild override to your project's CLAUDE.md:

```bash
cat src/modules/guild/install/claude-md-snippet.md >> CLAUDE.md
```

Guild auto-detects BMAD and integrates: stories use BMAD format, output goes to
`_bmad-output/`, PM and SM agents are included in the pipeline. Sally is
replaced.

**Safe to copy** — Guild's repo keeps BMAD core files in `bmad-bundle/`, not at
root. Copying `_bmad/guild/` will never overwrite your existing `_bmad/core/`.

### Requirements

- Claude Code CLI (or compatible IDE: Cursor, Windsurf, Codex, Gemini CLI, Antigravity)
- Optional: [BMAD Method v6](https://github.com/bmad-code-org/BMAD-METHOD) for sprint tracking and PM/SM integration
- Optional: Figma Pro + [Figma MCP](https://help.figma.com/hc/en-us/articles/32132100833559) for design tool integration
- Optional: [Atrium](https://atrium.sh) for Raid, Quest (party), and Tavern multi-model skills

---

## Integrations

### Figma MCP

Guild connects to Figma for reading design context, pushing live UI to Figma,
and creating native Figma components. All agents have an `/export-figma` command.

```bash
claude plugin install figma@claude-plugins-official
```

### BMAD Integration (optional)

When BMAD v6 is detected, Guild automatically:
- Reads `sprint-status.yaml` and continues existing story numbering
- Outputs stories in BMAD dev-story format to `_bmad-output/implementation-artifacts/stories/`
- Includes BMAD's PM and SM agents in the pipeline for story review and sprint planning
- Replaces BMAD's built-in UX Designer (Sally) with 8 specialized design agents
- Stories are immediately consumable by BMAD's `/dev-story` workflow

Without BMAD, Guild outputs standard stories to `guild-output/` and runs a
Guild-only pipeline.

### Claude Design

When you generate visuals in [Claude Design](https://www.anthropic.com/news/claude-design-anthropic-labs)
and hand them off to Claude Code as a bundle, Guild's **Sage Handoff Gate**
parses the bundle, resolves tokens, runs WCAG contrast + design-system
coherence checks, and FAILs the handoff before code is built if the system
is inaccessible or incoherent (e.g. the green-trap). Catches it at the seam,
once, instead of after it's stamped into the codebase.

### Atrium

[Atrium](https://atrium.sh) is required for multi-model Raid and party Quest
skills. With Atrium running, Guild opens parallel engine panes, passes the same
brief to each, and orchestrates synthesis across Claude, Codex, and Antigravity
simultaneously. Tavern (open multi-model conversation via `bmad-party-mode`)
also uses Atrium.

### Skyfleet / Gas Town

Guild is designed to integrate with multi-agent orchestration systems. Healer
outputs structured artifacts with YAML frontmatter (status, version, references)
that can be consumed as Beads in Gas Town or workflow units in Skyfleet. The
handoff format is configurable.

---

## Pipeline modes (the full list)

**Standalone · Greenfield** (6 phases): Ranger → Rogue → Mage → Warlock → Sage → Healer

**Standalone · Brownfield** (5 phases): Ranger → Rogue → Warlock → Sage → Healer

**With BMAD · Greenfield** (12 phases): Analyst → PM → Ranger → Rogue → Mage → Warlock → Architect → Sage → Healer → PM → SM → Dev

**With BMAD · Brownfield** (8 phases): Ranger → Rogue → Mage → Warlock → Sage → Healer → PM → SM

**With BMAD · Mid-project** (10 phases): PM → Ranger → Rogue → Mage → Warlock → Architect → Sage → Healer → PM → SM

Every agent saves structured artifacts to `{output_root}/guild-artifacts/`.
Each downstream agent reads what came before — context flows automatically.

---

## Module structure

```
src/modules/guild/
├── module.yaml
├── agents/
│   ├── ranger.agent.yaml                # Ranger 🔍 UX Researcher
│   ├── ranger-sidecar/knowledge-base/
│   ├── rogue.agent.yaml                 # Rogue 🔀 Interaction Designer
│   ├── rogue-sidecar/knowledge-base/
│   ├── mage.agent.yaml                  # Mage 🎨 Visual Designer
│   ├── mage-sidecar/knowledge-base/
│   ├── warlock.agent.yaml               # Warlock ✍️ Content Strategist
│   ├── warlock-sidecar/knowledge-base/
│   ├── sage.agent.yaml                  # Sage 🛡️ Design QA
│   ├── sage-sidecar/knowledge-base/
│   ├── healer.agent.yaml                # Healer 📦 Design Ops
│   ├── healer-sidecar/knowledge-base/
│   ├── tinker.agent.yaml                # Tinker 🔧 Design System Engineer
│   ├── tinker-sidecar/knowledge-base/
│   ├── cartographer.agent.yaml          # Cartographer 🗺️ Information Architect
│   ├── cartographer-sidecar/knowledge-base/
│   ├── guild-master.agent.yaml          # Guild Master 🎯 Orchestrator
│   └── shared-sidecar/                  # artifact-rules, bmad-integration, figma-api-reference
├── tasks/                                # one .md per task (~50)
├── templates/                            # 47+ structured output templates
├── workflows/
│   └── design-sprint/
│       ├── workflow.md
│       └── config.yaml
├── checklists/
└── data/
```

---

## Design philosophy

**Research-driven** — Every design decision traces back to evidence from Ranger.
No assumptions, no "I think users want..."

**Direction-first** — Phase 0 elicits designer taste before any synthesis happens.
The design direction brief is the lens through which every downstream agent
filters its work. Without it, pipelines average competitors into generic output.

**Foundation before pages** — Phase 0.5 audits tokens and primitives before
page-level work begins. Agents cannot inline ad-hoc components if the system
layer is already solid.

**Measure, don't eyeball** — Visual critique requires measured values (computed
contrast, computed CSS), not perceptual claims. Baked into Mage's
`critical_actions`; see [docs/multi-model-bakeoff.md](docs/multi-model-bakeoff.md)
for why.

**Artifact state machine** — Every artifact has a status (draft → in-review →
approved) tracked in YAML frontmatter. Quality gates enforce transitions.

**Context flows downstream** — Ranger's personas inform Rogue's flows. Rogue's
wireframes get polished by Mage. Mage's refined specs give Warlock copy context.
Sage checks everything. Healer packages it all. No agent works in isolation.

**Error-first design** — Rogue designs the error state before the happy path.
Every flow includes edge cases, offline behavior, and recovery paths.

**Accessibility is not optional** — Ranger includes accessibility needs in
personas. Rogue specifies ARIA and keyboard behavior. Sage runs WCAG checks.
Warlock writes screen-reader-friendly copy.

**Brownfield-first** — Guild assumes every project has existing context. It
reads before it writes. It continues, not restarts.

---

## Roadmap

- [x] npm package distribution — `npx @ayesel/guild` installs Guild into any project
- [x] Integrity validator (`scripts/validate.sh`) — catches compiler-drop regressions
- [x] Design-system coherence linter (`scripts/coherence-check.sh`) — drift gate
- [x] Claude Design handoff gate — contrast + coherence check on the export bundle
- [x] Multi-model bake-off evidence + engine-fit guidance
- [ ] Storybook MCP integration (auto-generate stories for components)
- [ ] Design-token MCP server (bridge Figma Variables ↔ W3C DTCG ↔ Style Dictionary)
- [ ] Figma-native artifact output for all agents (flows as Figma diagrams, not just markdown)
- [ ] Skyfleet integration (Guild agents as Skyfleet workflow modules)
- [ ] List Guild as a selectable module in BMAD's own `npx bmad-method install` flow

---

## Inspiration

Guild draws direct inspiration from the [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD)
which proved that structured AI agents with phased workflows and quality gates
can transform AI-assisted software development. Guild applies that same
philosophy to the product design discipline.

Also inspired by [Whiteport Design Studio (WDS)](https://github.com/bmad-code-org/bmad-method-wds-expansion)
for demonstrating that design-specific agents can be built on the BMAD
foundation, and Steve Yegge's
[Gas Town](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04)
for multi-agent orchestration patterns.

---

## Author

**Ayrehl Davis** — Senior UI/UX Designer & Design Technologist

---

## License

MIT — see [LICENSE](LICENSE) for details.
