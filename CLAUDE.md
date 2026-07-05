# Guild Design Framework

## Project Overview
Guild is an AI-powered design framework with 8 specialized design agents (Ranger, Rogue, Warlock, Mage, Sage, Healer, Tinker, Cartographer) plus the Guild Master orchestrator that run adaptive design-to-sprint pipelines. Guild works standalone or integrates with BMAD v6 when present.

The agents:
- **Ranger 🔍** — UX Researcher
- **Rogue 🔀** — Interaction Designer
- **Mage 🎨** — Visual Designer
- **Warlock ✍️** — Content Strategist
- **Sage 🛡️** — Design QA (quality gate)
- **Healer 📦** — Design Ops (dev handoff)
- **Tinker 🔧** — Design System Engineer (Figma component architecture, tokens, Storybook/Code Connect parity)
- **Cartographer 🗺️** — Information Architect & System Mapper (IA, sitemaps, content models, FigJam composition)
- **Guild Master 🎯** — Orchestrator

## Modes
- **Standalone** (bmad_mode = false): Guild agents run a 6-phase pipeline (Ranger → Rogue → Mage → Warlock → Sage → Healer). Output goes to `guild-output/`.
- **With BMAD** (bmad_mode = true): Full pipeline including BMAD's PM, SM, Analyst, and Architect agents. Output goes to `_bmad-output/`. Guild replaces Sally.
- **Auto-detect** (default): Guild checks for `_bmad/core/config.yaml` and adapts automatically.

Configure in `guild.config.yaml` at the project root.

**Tinker and Cartographer are on-demand specialists**, not fixed steps in the sequential pipeline. Tinker is invoked for design-system/Figma component work (and backs the Phase 0.5 foundation gate when the token/primitive layer needs building). Cartographer is invoked for information-architecture and stakeholder system-mapping work. Both can be called at any point by the orchestrator or directly.

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
- `.claude/commands/guild-*.md` — 25 agent-fronted slash commands (agent launchers + hot paths; everything else routes through agent menus — see `docs/guild/command-surface-prune.md`)
- `guild.config.yaml` — Guild configuration (bmad_mode, output_root)

## Running Guild
- `/guild-agent-guild-master` — Load the orchestrator for full pipeline control
- `/guild-design-sprint` — Run adaptive pipeline (auto-detects greenfield/brownfield and BMAD presence)
- Individual agents: `/guild-agent-ranger`, `/guild-agent-mage`, `/guild-agent-rogue`, `/guild-agent-warlock`, `/guild-agent-sage`, `/guild-agent-healer`, `/guild-agent-tinker`, `/guild-agent-cartographer`
- Specialist methods route through agent menus (e.g. `/guild-agent-ranger HE` for heuristic eval, `/guild-agent-rogue UF` for user flows) — full routing table in `docs/guild/command-surface-prune.md`
- Raid skills (3-model comparison via atrium): `/guild-raid`, `/ranger-raid`, `/rogue-raid`, `/mage-raid`, `/warlock-raid`, `/sage-raid`, `/healer-raid`
- Hall dashboard (durable launchd server on :4400): `npm run hall` (status) / `npm run hall:install` / `npm run hall:restart` — managed by `scripts/hall-daemon.sh`, NOT an atrium workspace-command

## Maintenance & integrity

- **Run `./scripts/validate.sh` before any release or after regenerating agents.** It checks reference integrity: every command resolves to a real agent + menu code, every compiled menu item carries a `target=`, all task/template/workflow targets resolve, cross-IDE parity holds, and no duplicate command wiring. Exit 0 = clean, 1 = failures.
- **Compiled agents are generated, source-of-truth is `src/`.** The `_bmad/guild/agents/*.md` files are compiled (by the external BMAD compiler, which is NOT vendored here) from `src/modules/guild/agents/*.agent.yaml`. The external compiler also injects content the source yaml does not contain (per-agent `<activation>` step-2 text, the `capabilities=` attr, boilerplate `<rules>`, name→slug ids), so the compiled files cannot be regenerated from source alone — do not try to rewrite the compiler.
- **After ANY recompile, run `python3 scripts/sync-compiled.py` (or `npm run postcompile`).** The external compiler reliably drops menu `target=` attributes (the recurring regression `validate.sh` check [4] guards). `sync-compiled.py` auto-re-injects every compiled item's `target=` from the source `.agent.yaml` `menu[].target` (matched 1:1 by `cmd`), safely and idempotently — it replaces the old manual re-injection step. `npm run postcompile` runs it then `validate.sh`. NOTE: it does NOT sync `critical_actions`/`<rules>` (the compiler reroutes some critical_actions into `<activation>`), so when you change a `critical_action`, edit the source `.agent.yaml` AND the compiled `.md` in tandem (or recompile + sync).
- **Cross-IDE commands must stay in sync.** `.claude/commands/guild-*.md` is canonical; `.cursor/commands/*.md` are identical copies and `.gemini/commands/*.toml` are generated from them. Re-sync all three after adding or editing any Guild command.

## When BMAD is present
- Do NOT use Sally (/bmad-agent-bmm-ux-designer) — Guild replaces her
- After PRD/epic changes, ALWAYS run Guild design sprint before dev implementation
- The workflow is: PM scopes changes → Guild design sprint → then dev implements
- Never go straight from PM to dev on UI-facing changes without running Guild first
