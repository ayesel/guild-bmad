# Guild Design Framework

## Project Overview
Guild is an AI-powered design framework with 9 specialized design agents (Ranger, Rogue, Warlock, Mage, Sage, Healer, Tinker, Cartographer, Enchanter) plus the Guild Master orchestrator that run adaptive design-to-sprint pipelines. Guild works standalone or integrates with BMAD v6 when present.

The agents:
- **Ranger 🔍** — UX Researcher
- **Rogue 🔀** — Interaction Designer
- **Mage 🎨** — Visual Designer
- **Warlock ✍️** — Content Strategist
- **Sage 🛡️** — Design QA (quality gate)
- **Healer 📦** — Design Ops (dev handoff)
- **Tinker 🔧** — Design System Engineer (Figma component architecture, tokens, Storybook/Code Connect parity)
- **Cartographer 🗺️** — Information Architect & System Mapper (IA, sitemaps, content models, FigJam composition)
- **Enchanter ✨** — Brand Identity Designer (brand strategy, verbal identity, logo/mark/icon/illustration & brand color+type DNA; the brand source-of-truth)
- **Guild Master 🎯** — Orchestrator

## Modes
- **Standalone** (bmad_mode = false): Guild agents run a 6-phase pipeline (Ranger → Rogue → Mage → Warlock → Sage → Healer). Output goes to `guild-output/`.
- **With BMAD** (bmad_mode = true): Full pipeline including BMAD's PM, SM, Analyst, and Architect agents. Output goes to `_bmad-output/`. Guild replaces Sally.
- **Auto-detect** (default): Guild checks for `_bmad/core/config.yaml` and adapts automatically.

Configure in `guild.config.yaml` at the project root.

**Tinker, Cartographer, and Enchanter are on-demand specialists**, not fixed steps in the sequential pipeline. Tinker is invoked for design-system/Figma component work (and backs the Phase 0.5 foundation gate when the token/primitive layer needs building). Cartographer is invoked for information-architecture and stakeholder system-mapping work. Enchanter is invoked for greenfield brand creation or rebrands — it owns the brand source-of-truth (strategy, verbal identity, logo/mark/icon/illustration, brand color+type DNA) and runs *upstream*, feeding brand intent to Tinker (tokens) and Mage (UI application); it sets the voice that Warlock speaks in. All three can be called at any point by the orchestrator or directly.

## Key Design Principles
- Brownfield-first — assume every project has existing state until proven otherwise
- Artifacts are source of truth — Guild artifacts live in `{output_root}/guild-artifacts/` and are never duplicated
- Each agent has a distinct persona and stays in character during sessions
- Design QA (Sage) is a quality gate — NO-GO stops the pipeline
- When BMAD is present, Guild follows BMAD conventions for stories and sprint tracking

## Project Structure
- `src/modules/guild/agents/` — Agent YAML source files
- `src/modules/guild/tasks/` — Task execution files
- `src/modules/guild/templates/` — Output templates (YAML)
- `src/modules/guild/workflows/` — Pipeline workflow definitions
- `_bmad/guild/agents/` — Compiled agents for short-name loading
- `.claude/commands/guild-*.md` — Slash commands for all Guild menu items
- `guild.config.yaml` — Guild configuration (bmad_mode, output_root)

## Running Guild
- `/guild-master` — Load the orchestrator for full pipeline control
- `/guild-design-sprint` — Run adaptive pipeline (auto-detects greenfield/brownfield and BMAD presence)
- Individual agents: `/guild-agent-ranger`, `/guild-agent-mage`, `/guild-agent-rogue`, `/guild-agent-warlock`, `/guild-agent-sage`, `/guild-agent-healer`, `/guild-agent-tinker`, `/guild-agent-cartographer`, `/guild-agent-enchanter`
- Individual commands: `/guild-heuristic-eval`, `/guild-critique`, `/guild-user-flow`, etc.
- Raid skills (3-model comparison via atrium): `/guild-raid`, `/ranger-raid`, `/rogue-raid`, `/mage-raid`, `/warlock-raid`, `/sage-raid`, `/healer-raid`, `/guild-master-raid`

## Maintenance & integrity

- **Run `./scripts/validate.sh` before any release or after regenerating agents.** It checks reference integrity: every command resolves to a real agent + menu code, every compiled menu item carries a `target=`, all task/template/workflow targets resolve, cross-IDE parity holds, and no duplicate command wiring. Exit 0 = clean, 1 = failures.
- **Compiled agents are generated, source-of-truth is `src/`.** The `_bmad/guild/agents/*.md` files are compiled (by the external BMAD compiler) from `src/modules/guild/agents/*.agent.yaml`. The compiler has historically dropped menu `target=` attributes when regenerating — `validate.sh` check [4] exists specifically to catch that regression. If you recompile and validation fails on missing `target=`, re-inject them from the source `.agent.yaml` menu targets.
- **Cross-IDE commands must stay in sync.** `.claude/commands/guild-*.md` is canonical; `.cursor/commands/*.md` are identical copies and `.gemini/commands/*.toml` are generated from them. Re-sync all three after adding or editing any Guild command.

## When BMAD is present
- Do NOT use Sally (/bmad-agent-bmm-ux-designer) — Guild replaces her
- After PRD/epic changes, ALWAYS run Guild design sprint before dev implementation
- The workflow is: PM scopes changes → Guild design sprint → then dev implements
- Never go straight from PM to dev on UI-facing changes without running Guild first
