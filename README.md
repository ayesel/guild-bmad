# Guild — AI-Powered Design Framework

**7 specialized design agents for the full product design lifecycle.**

Guild gives product designers a team of AI agents for research, interaction design, visual polish, content strategy, design QA, and developer handoff. One command runs the full pipeline — from user research to sprint-ready stories.

Guild works **standalone** or **with BMAD v6**. It auto-detects your setup and adapts.

Built for designers who want structured, repeatable AI collaboration. The AI handles systematic, data-driven work. You provide the human judgment, empathy, and creative direction.

---

## The agents

| Agent | Role | Commands | What it does |
|-------|------|----------|-------------|
| **Ranger 🔍** | UX Researcher | ~21 | Heuristic evaluations, competitive audits, persona generation, journey maps, interview scripts, research synthesis, usability test plans, accessibility audits, JTBD mapping, card sorting, A/B tests, surveys, stakeholder interviews, workshops, affinity diagrams, service blueprints, empathy maps, story maps, diary studies, method recommendations |
| **Rogue 🔀** | Interaction Designer | ~12 | User flows, swim lanes, site maps, state diagrams, task analyses, wireframes, interaction maps, visual audits, flow audits, states audits, React export, Figma export |
| **Warlock ✍️** | Content Strategist | ~8 | Microcopy, error message systems, voice/tone guidelines, empty states, onboarding copy, content audits, naming, UX spec |
| **Sage 🛡️** | Design QA | ~10 | Design review, design system compliance, responsive checks, accessibility QA, implementation fidelity, consistency audits, pattern checks, pre-handoff quality gates, system foundation audit |
| **Healer 📦** | Design Ops | ~10 | Developer handoff specs, Jira stories (Given/When/Then), design tokens (W3C DTCG), component specs, annotations, changelogs, release notes, watch mode, fix loop, UX_Design.md BMAD export |
| **Mage 🎨** | Visual Designer | ~11 | Design direction brief, visual critique, component polish, visual hierarchy, spacing, color refinement, typography, auto-capture critique, responsive scans, visual diffs, before/after comparison |
| **Tinker 🔧** | Design System Engineer | ~12 | Figma component architecture, atomic decomposition, variant systems, design tokens (W3C DTCG), variable binding, naming taxonomy, Storybook story coverage, Code Connect mapping, WCAG token audits, workspace reconnaissance |
| **Cartographer 🗺️** | Information Architect & System Mapper | ~11 | Information architecture, sitemaps, content models, FigJam whiteboard composition, system maps for stakeholders, ADR diagrams, conceptual models, navigation audits, card sort design, tree test design, zone layout |
| **Guild Master 🎯** | Orchestrator | ~6 | Full pipeline, quick sprint, solo quest, party quest, master raid. Auto-detects greenfield vs brownfield and BMAD presence |

**118+ commands · 47+ templates · 9 sidecar knowledge bases**

---

## Multi-model

Guild extends naturally into multi-model workflows. Three modes — Raid, Quest, and Tavern — map to distinct collaboration patterns.

| Mode | What it is | Command(s) | Requires |
|------|-----------|------------|---------|
| **Raid** | Same brief, all three engines (Claude / Codex / Gemini) do the work in parallel and talk to each other, then synthesize. Collaborative same-task dialogue. | `guild-raid`, `guild-master-raid`, `ranger-raid`, `rogue-raid`, `mage-raid`, `warlock-raid`, `sage-raid`, `healer-raid` | Atrium |
| **Quest** | Full multi-phase pipeline. Solo: one model runs all 15 steps. Party: three engines divide specialized labor across phases. | `guild-quest` (solo), `guild-party-quest` (party) | Atrium (party only) |
| **Tavern** | Open conversation around a topic — no fixed deliverable. Brainstorming, critique, exploration. | `bmad-party-mode` | Atrium |

### Raids in detail

Each agent has its own raid command for targeted 3-model comparison. Use these when you want three independent takes on the same design problem — then let the engines synthesize:

```
ranger-raid    rogue-raid    mage-raid
warlock-raid   sage-raid     healer-raid
guild-raid     guild-master-raid
```

### Quests in detail

**`guild-quest`** — Solo quest. One model runs the complete Guild + BMAD pipeline from design direction through build. 15 steps across 5 phases. Every agent, every review gate, no shortcuts.

**`guild-party-quest`** — Party quest. Three engines in Atrium, divided by specialization across phases. Research engine handles Ranger phases. Design engine handles Rogue/Mage/Warlock. QA/handoff engine handles Sage/Healer/BMAD. Engines compare at synthesis points.

---

## The pipeline

> **Full walkthrough:** [Guild + BMAD Pipeline Guide](docs/pipeline.md) — design questions, phase gates, autonomous build loop, component registry, and design system integration explained in detail.

```
Phase 0   → Mage:  Design Direction Brief (taste/vision gate)
Phase 0.5 → Sage:  System Foundation Audit (token/primitive gate)
Phase 1   → Ranger: Research & Visual Audit
Phase 2   → Rogue: Interaction Design
Phase 3   → Mage:  Visual Design
Phase 4   → Warlock: Content Strategy
Phase 5   → Sage:  Design QA
Phase 6   → Healer: Dev Handoff
```

When BMAD is present, the pipeline extends: `→ PM (review) → SM (sprint planning) → Dev (build)`

### Phase 0: Design Direction

`/guild-design-direction` — Mage asks 6 questions before any visual work begins: anchor reference, personality adjectives, density preference, motion energy, color story, what to avoid. Synthesizes a locked direction brief. Every downstream agent receives the full brief and executes against it — this prevents the pipeline from averaging competitors into a generic AI-dashboard result.

### Phase 0.5: System Foundation

`/guild-system-foundation` — Sage audits the token and primitive layer before any page-level work begins. Checks color, spacing, motion, shadow, typography, and radius tokens, plus base primitives (Button, Input, Select, Field, Card, Badge, etc.). Returns PASS / CONDITIONAL / FAIL. A FAIL stops the pipeline until the foundation is solid.

### Modes

**Standalone · Greenfield** (6 phases):
Ranger → Rogue → Mage → Warlock → Sage → Healer

**Standalone · Brownfield** (5 phases):
Ranger → Rogue → Warlock → Sage → Healer

**With BMAD · Greenfield** (12 phases):
Analyst → PM → Ranger → Rogue → Mage → Warlock → Architect → Sage → Healer → PM → SM → Dev

**With BMAD · Brownfield** (8 phases):
Ranger → Rogue → Mage → Warlock → Sage → Healer → PM → SM

**With BMAD · Mid-project** (10 phases):
PM → Ranger → Rogue → Mage → Warlock → Architect → Sage → Healer → PM → SM

Every agent saves structured artifacts to `{output_root}/guild-artifacts/`. Each downstream agent reads what came before — context flows automatically. Sage acts as a quality gate: if it says NO-GO, the pipeline loops back to Rogue.

---

## How it works

```bash
# Load the orchestrator
@guild-master

# Run the full pipeline
/guild-design-sprint improve the checkout flow

# Run with pre-pipeline gates
/guild-design-direction    # Phase 0: lock taste before anything
/guild-system-foundation   # Phase 0.5: audit tokens before page work
/guild-design-sprint       # Then run the full pipeline

# Skip research, go straight to design
/guild-quick-sprint        # Rogue → Warlock → Sage → Healer → PM → SM

# Run a full solo quest (research through build)
/guild-quest

# Run a party quest (3 engines, Atrium required)
/guild-party-quest

# Load individual agents
@ux-researcher             # Ranger
@interaction-designer      # Rogue
@visual-designer           # Mage
@content-strategist        # Warlock
@design-qa                 # Sage
@design-ops                # Healer

# Run multi-model raids
/ranger-raid               # 3-model UX research comparison
/guild-raid                # All agents, 3-model comparison
/guild-master-raid         # Guild Master 3-model orchestration
```

The orchestrator detects your project state, continues from existing story numbering if present, and outputs dev-ready stories. With BMAD, stories are immediately consumable by `/dev-story`.

---

## What Guild produces

A single `/guild-quest` or `/guild-design-sprint` run generates:

- **Direction artifacts** — design direction brief locking taste, personality, density, motion, and color before any visual work
- **Research artifacts** — personas, journey maps, competitive audits, heuristic evaluations, visual audits with real screenshots
- **Design artifacts** — user flows with Mermaid diagrams, swim lanes, wireframes, state diagrams
- **Visual design** — hierarchy, spacing, typography, and color refinements with code fixes
- **Content artifacts** — all microcopy, error messages, empty states, onboarding copy
- **QA reports** — design review, accessibility audit, system foundation audit, pre-handoff quality gate verdict
- **Dev handoff** — Jira stories with acceptance criteria, component specs with props/states/ARIA, design tokens in W3C DTCG format, component registry

Real-world test: Guild produced 14 artifacts (6,532 lines) for a React Native ski trip app in a single run — including 4 personas, 3 redesigned flows, 31 error messages, 15 empty states, and 12 sprint-ready stories across 3 epics.

---

## Installation

### Standalone (no BMAD)

```bash
git clone https://github.com/ayesel/guild-bmad.git
cd guild-bmad

# Copy Guild into your project
cp -r _bmad/guild/ /path/to/your-project/_bmad/guild/
cp -r src/modules/guild/ /path/to/your-project/src/modules/guild/
cp -r .claude/commands/guild-*.md /path/to/your-project/.claude/commands/
cp guild.config.yaml /path/to/your-project/
```

Guild auto-detects that BMAD is not present and runs in standalone mode. Output goes to `guild-output/`.

**Optional:** Want BMAD features (sprint tracking, PM/SM review) without a full BMAD install? Copy the bundle:
```bash
cp -r bmad-bundle/_bmad/core /path/to/your-project/_bmad/core
cp -r bmad-bundle/_bmad/_config /path/to/your-project/_bmad/_config
cp -r bmad-bundle/.claude/commands/bmad-*.md /path/to/your-project/.claude/commands/
```

Then open Claude Code and type `/guild-master` to get started.

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

Guild auto-detects BMAD and integrates: stories use BMAD format, output goes to `_bmad-output/`, PM and SM agents are included in the pipeline. Sally is replaced.

**Safe to copy** — Guild's repo keeps BMAD core files in `bmad-bundle/`, not at root. Copying `_bmad/guild/` will never overwrite your existing `_bmad/core/`.

### Requirements

- Claude Code CLI (or compatible IDE: Cursor, Windsurf, Codex, Gemini CLI)
- Optional: [BMAD Method v6](https://github.com/bmad-code-org/BMAD-METHOD) for sprint tracking and PM/SM integration
- Optional: Figma Pro + [Figma MCP](https://help.figma.com/hc/en-us/articles/32132100833559) for design tool integration
- Optional: [Atrium](https://atrium.sh) for Raid, Quest (party), and Tavern multi-model skills

---

## Integrations

### Figma MCP

Guild connects to Figma for reading design context, pushing live UI to Figma, and creating native Figma components. All agents have an `/export-figma` command.

```bash
claude plugin install figma@claude-plugins-official
```

### BMAD Integration (optional)

When BMAD v6 is detected, Guild automatically:
- Reads `sprint-status.yaml` and continues existing story numbering
- Outputs stories in BMAD dev-story format to `_bmad-output/implementation-artifacts/stories/`
- Includes BMAD's PM and SM agents in the pipeline for story review and sprint planning
- Replaces BMAD's built-in UX Designer (Sally) with 7 specialized design agents
- Stories are immediately consumable by BMAD's `/dev-story` workflow

Without BMAD, Guild outputs standard stories to `guild-output/` and runs a Guild-only pipeline.

### Atrium

[Atrium](https://atrium.sh) is required for multi-model Raid and party Quest skills. With Atrium running, Guild opens parallel engine panes, passes the same brief to each, and orchestrates synthesis across Claude, Codex, and Gemini simultaneously. Tavern (open multi-model conversation via `bmad-party-mode`) also uses Atrium.

### Skyfleet / Gas Town

Guild is designed to integrate with multi-agent orchestration systems. Healer outputs structured artifacts with YAML frontmatter (status, version, references) that can be consumed as Beads in Gas Town or workflow units in Skyfleet. The handoff format is configurable.

---

## Module structure

```
src/modules/guild/
├── module.yaml
├── agents/
│   ├── interaction-designer.agent.yaml  # Rogue 🔀
│   ├── interaction-designer-sidecar/
│   │   └── knowledge-base/
│   ├── ux-researcher.agent.yaml         # Ranger 🔍
│   ├── ux-researcher-sidecar/
│   │   └── knowledge-base/
│   ├── content-strategist.agent.yaml    # Warlock ✍️
│   ├── content-strategist-sidecar/
│   │   └── knowledge-base/
│   ├── design-qa.agent.yaml             # Sage 🛡️
│   ├── design-qa-sidecar/
│   │   └── knowledge-base/
│   ├── design-ops.agent.yaml            # Healer 📦
│   ├── design-ops-sidecar/
│   │   └── knowledge-base/
│   ├── visual-designer.agent.yaml       # Mage 🎨
│   ├── visual-designer-sidecar/
│   │   └── knowledge-base/
│   ├── guild-master.agent.yaml          # Guild Master 🎯
│   └── shared-sidecar/
│       └── figma-api-reference.md
├── tasks/
│   ├── create-artifact.md
│   ├── run-research.md
│   ├── write-content.md
│   ├── run-qa.md
│   ├── create-handoff.md
│   ├── export-react.md
│   ├── export-to-figma.md
│   └── audit-flow.md
├── templates/                           # 47+ structured templates
│   ├── user-flow-template.yaml
│   ├── swim-lane-template.yaml
│   ├── persona-template.yaml
│   ├── heuristic-eval-template.yaml
│   ├── journey-map-template.yaml
│   └── ... (and 40+ more)
├── workflows/
│   └── design-sprint/
│       ├── workflow.md
│       └── config.yaml
├── checklists/
└── data/
```

---

## Design philosophy

**Research-driven** — Every design decision traces back to evidence from Ranger. No assumptions, no "I think users want..."

**Direction-first** — Phase 0 elicits designer taste before any synthesis happens. The design direction brief is the lens through which every downstream agent filters its work. Without it, pipelines average competitors into generic output.

**Foundation before pages** — Phase 0.5 audits tokens and primitives before page-level work begins. Agents cannot inline ad-hoc components on every page if the system layer is already solid.

**Artifact state machine** — Every artifact has a status (draft → in-review → approved) tracked in YAML frontmatter. Quality gates enforce transitions.

**Context flows downstream** — Ranger's personas inform Rogue's flows. Rogue's wireframes get polished by Mage. Mage's refined specs give Warlock copy context. Sage checks everything. Healer packages it all. No agent works in isolation.

**Error-first design** — Rogue designs the error state before the happy path. Every flow includes edge cases, offline behavior, and recovery paths.

**Accessibility is not optional** — Ranger includes accessibility needs in personas. Rogue specifies ARIA and keyboard behavior. Sage runs WCAG checks. Warlock writes screen-reader-friendly copy.

**Brownfield-first** — Guild assumes every project has existing context. It reads before it writes. It continues, not restarts.

---

## Roadmap

- [ ] Storybook MCP integration (auto-generate stories for components)
- [ ] Design token MCP server (bridge Figma Variables ↔ W3C DTCG ↔ Style Dictionary)
- [ ] Figma native artifact output for all agents (flows as Figma diagrams, not just markdown)
- [ ] Skyfleet integration (Guild agents as Skyfleet workflow modules)
- [ ] npm package distribution (`npx bmad-method install` with Guild as selectable module)

---

## Inspiration

Guild draws direct inspiration from the [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) which proved that structured AI agents with phased workflows and quality gates can transform AI-assisted software development. Guild applies that same philosophy to the product design discipline.

Also inspired by [Whiteport Design Studio (WDS)](https://github.com/bmad-code-org/bmad-method-wds-expansion) for demonstrating that design-specific agents can be built on the BMAD foundation, and Steve Yegge's [Gas Town](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) for multi-agent orchestration patterns.

---

## Author

**Ayrehl Davis** — Senior UI/UX Designer & Design Technologist

---

## License

MIT — see [LICENSE](LICENSE) for details.
