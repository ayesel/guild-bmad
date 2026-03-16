# PDX — Product Design Experience Framework

**AI-powered product design framework with 6 specialized agents for the full design lifecycle.**

PDX is a BMAD-compatible module that gives product designers a team of AI agents for research, interaction design, content strategy, design QA, and developer handoff. One command runs the full pipeline — from user research to sprint-ready Jira stories.

Built for designers who want structured, repeatable AI collaboration. The AI handles systematic, data-driven work. You provide the human judgment, empathy, and creative direction.

---

## The agents

| Agent | Role | Commands | What it does |
|-------|------|----------|-------------|
| **Nova 🔍** | UX Researcher | 22 | Heuristic evaluations, competitive audits, persona generation, journey maps, interview scripts, research synthesis, usability test plans, accessibility audits, JTBD mapping, card sorting, A/B tests, surveys, stakeholder interviews, workshops, affinity diagrams, service blueprints, empathy maps, story maps, diary studies, method recommendations |
| **Kai 🔀** | Interaction Designer | 11 | User flows, swim lanes, site maps, state diagrams, task analyses, wireframes, interaction maps, flow audits, React export, Figma export |
| **Echo ✍️** | Content Strategist | 9 | Microcopy, error message systems, voice/tone guidelines, empty states, onboarding copy, content audits, naming |
| **Sage 🛡️** | Design QA | 9 | Design review, design system compliance, responsive checks, accessibility QA, implementation fidelity, consistency audits, pre-handoff quality gates |
| **Relay 📦** | Design Ops | 10 | Developer handoff specs, Jira stories (Given/When/Then), design tokens (W3C DTCG), component specs, annotations, changelogs, release notes, UX_Design.md BMAD export |
| **Lux 🎨** | Visual Designer | 14 | Visual critique, component polish, visual hierarchy, spacing, color refinement, typography, auto-capture critique (Playwright/Simulator), responsive scans, visual diffs, animation review, Figma export |
| **PDX 🎯** | Orchestrator | 6 | Coordinates all agents through the full pipeline with one command. Auto-detects greenfield vs brownfield projects |

**82+ commands · 47+ templates · 7 sidecar knowledge bases**

---

## The pipeline

```
Nova (research) → Kai (design) → Lux (visual polish) → Echo (content) → Sage (QA) → Relay (handoff) → PM (review) → SM (sprint planning) → Dev (build)
```

PDX auto-detects your project state and adapts:

**Greenfield** (new project — 12 phases):
Analyst → PM → Nova → Kai → Lux → Echo → Architect → Sage → Relay → PM → SM → Dev

**Brownfield** (existing project — 8 phases):
Nova → Kai → Lux → Echo → Sage → Relay → PM → SM

**Mid-project** (PRD exists, no sprints — 10 phases):
PM → Nova → Kai → Lux → Echo → Architect → Sage → Relay → PM → SM

Every agent saves structured artifacts to `_bmad-output/pdx-artifacts/`. Each downstream agent reads what came before — context flows automatically. Sage acts as a quality gate: if it says NO-GO, the pipeline loops back to Kai.

---

## How it works

```bash
# Load the orchestrator
@pdx-orchestrator

# Run the full pipeline on a feature
/design-sprint improve the checkout flow

# Or run individual agents
@ux-researcher          # Load Nova
@interaction-designer   # Load Kai
@visual-designer        # Load Lux
@content-strategist     # Load Echo
@design-qa              # Load Sage
@design-ops             # Load Relay
```

The orchestrator reads `sprint-status.yaml`, continues from your existing story numbering, and outputs stories that BMAD's dev agents can pick up with `/dev-story` immediately.

---

## What PDX produces

A single `/design-sprint` run generates:

- **Research artifacts** — personas, journey maps, competitive audits, heuristic evaluations
- **Design artifacts** — user flows with Mermaid diagrams, swim lanes, wireframes, state diagrams
- **Visual polish** — hierarchy, spacing, typography, and color refinements with code fixes
- **Content artifacts** — all microcopy, error messages, empty states, onboarding copy
- **QA reports** — design review, accessibility audit, pre-handoff quality gate verdict
- **Dev handoff** — Jira stories with acceptance criteria, component specs with props/states/ARIA, design tokens in W3C DTCG format

Real-world test: PDX produced 14 artifacts (6,532 lines) for a React Native ski trip app in a single run — including 4 personas, 3 redesigned flows, 31 error messages, 15 empty states, and 12 sprint-ready stories across 3 epics.

---

## Installation

### Into a new project

```bash
mkdir my-project && cd my-project
npx bmad-method install          # Install BMAD core
cp -r /path/to/pdx-design-framework/src/modules/pdx/ ./src/modules/pdx/
mkdir -p _bmad-output/pdx-artifacts/components
```

### Into an existing BMAD project

```bash
cp -r /path/to/pdx-design-framework/src/modules/pdx/ ./src/modules/pdx/
```

Then add the PDX override to your project's CLAUDE.md:

```bash
cat src/modules/pdx/install/claude-md-snippet.md >> CLAUDE.md
```

This tells all BMAD agents that PDX is active and prevents them from
recommending Sally for UX design work.

Then open Claude Code and type `@pdx-orchestrator` to get started.

### Requirements

- [BMAD Method v6](https://github.com/bmad-code-org/BMAD-METHOD) installed
- Claude Code CLI (or any BMAD-compatible IDE: Cursor, Windsurf, Codex, Gemini CLI)
- Optional: Figma Pro + [Figma MCP](https://help.figma.com/hc/en-us/articles/32132100833559) for design tool integration
- Optional: [claude-talk-to-figma-mcp](https://github.com/arinspunk/claude-talk-to-figma-mcp) for native Figma element creation

---

## Integrations

### Figma MCP

PDX connects to Figma for reading design context, pushing live UI to Figma, and creating native Figma components. All 6 agents have an `/export-figma` command.

```bash
claude plugin install figma@claude-plugins-official
```

### BMAD Integration

PDX is a standard BMAD expansion module. It:
- Reads `sprint-status.yaml` and continues existing story numbering
- Outputs stories to `_bmad-output/implementation-artifacts/stories/`
- Uses BMAD's PM and SM agents for story review and sprint planning
- Replaces BMAD's built-in UX Designer agent with 7 specialized design agents
- Stories are immediately consumable by BMAD's `/dev-story` workflow

### Skyfleet / Gas Town

PDX is designed to integrate with multi-agent orchestration systems. Relay outputs structured artifacts with YAML frontmatter (status, version, references) that can be consumed as Beads in Gas Town or workflow units in Skyfleet. The handoff format is configurable.

---

## Module structure

```
src/modules/pdx/
├── module.yaml                          # Module configuration
├── agents/
│   ├── interaction-designer.agent.yaml  # Kai 🔀
│   ├── interaction-designer-sidecar/
│   │   └── knowledge-base/
│   ├── ux-researcher.agent.yaml         # Nova 🔍
│   ├── ux-researcher-sidecar/
│   │   └── knowledge-base/
│   ├── content-strategist.agent.yaml    # Echo ✍️
│   ├── content-strategist-sidecar/
│   │   └── knowledge-base/
│   ├── design-qa.agent.yaml             # Sage 🛡️
│   ├── design-qa-sidecar/
│   │   └── knowledge-base/
│   ├── design-ops.agent.yaml            # Relay 📦
│   ├── design-ops-sidecar/
│   │   └── knowledge-base/
│   ├── pdx-orchestrator.agent.yaml      # PDX 🎯
│   └── shared-sidecar/
│       └── figma-api-reference.md
├── tasks/
│   ├── create-artifact.md               # Kai's core task
│   ├── run-research.md                  # Nova's core task
│   ├── write-content.md                 # Echo's core task
│   ├── run-qa.md                        # Sage's core task
│   ├── create-handoff.md                # Relay's core task
│   ├── export-react.md                  # React prototype export
│   ├── export-to-figma.md               # Figma native export
│   └── audit-flow.md                    # Flow audit
├── templates/                           # 37+ structured templates
│   ├── user-flow-template.yaml
│   ├── swim-lane-template.yaml
│   ├── persona-template.yaml
│   ├── heuristic-eval-template.yaml
│   ├── journey-map-template.yaml
│   ├── ... (and 30+ more)
├── workflows/
│   └── design-sprint/
│       ├── workflow.md                  # Adaptive pipeline
│       └── config.yaml
├── checklists/
└── data/
```

---

## Design philosophy

**Research-driven** — Every design decision traces back to evidence from Nova. No assumptions, no "I think users want..."

**Artifact state machine** — Every artifact has a status (draft → in-review → approved) tracked in YAML frontmatter. Quality gates enforce transitions.

**Context flows downstream** — Nova's personas inform Kai's flows. Kai's wireframes get polished by Lux. Lux's refined specs give Echo copy context. Sage checks everything. Relay packages it all. No agent works in isolation.

**Error-first design** — Kai designs the error state before the happy path. Every flow includes edge cases, offline behavior, and recovery paths.

**Accessibility is not optional** — Nova includes accessibility needs in personas. Kai specifies ARIA and keyboard behavior. Sage runs WCAG checks. Echo writes screen-reader-friendly copy.

**Brownfield-first** — PDX assumes every project has existing context. It reads before it writes. It continues, not restarts.

---

## Roadmap

- [ ] Storybook MCP integration (auto-generate stories for components)
- [ ] Design token MCP server (bridge Figma Variables ↔ W3C DTCG ↔ Style Dictionary)
- [ ] Expanded UX prompt library (card sorting, A/B test plans, survey design)
- [ ] Figma native artifact output for all agents (flows as Figma diagrams, not just markdown)
- [ ] Skyfleet integration (PDX agents as Skyfleet workflow modules)
- [ ] npm package distribution (`npx bmad-method install` with PDX as selectable module)

---

## Inspiration

PDX draws direct inspiration from the [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) which proved that structured AI agents with phased workflows and quality gates can transform AI-assisted software development. PDX applies that same philosophy to the product design discipline.

Also inspired by [Whiteport Design Studio (WDS)](https://github.com/bmad-code-org/bmad-method-wds-expansion) for demonstrating that design-specific agents can be built on the BMAD foundation, and Steve Yegge's [Gas Town](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) for multi-agent orchestration patterns.

---

## Author

**Ayrehl Davis** — Senior UI/UX Designer & Design Technologist

---

## License

MIT — see [LICENSE](LICENSE) for details.
