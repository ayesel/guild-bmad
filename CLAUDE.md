# Guild Design Framework

## Project Overview
Guild is an AI-powered design framework with 7 specialized design agents (Ranger, Rogue, Warlock, Mage, Sage, Healer, Guild Master) that run adaptive design-to-sprint pipelines. Guild works standalone or integrates with BMAD v6 when present.

## Modes
- **Standalone** (bmad_mode = false): Guild agents run a 6-phase pipeline (Ranger → Rogue → Mage → Warlock → Sage → Healer). Output goes to `guild-output/`.
- **With BMAD** (bmad_mode = true): Full pipeline including BMAD's PM, SM, Analyst, and Architect agents. Output goes to `_bmad-output/`. Guild replaces Sally.
- **Auto-detect** (default): Guild checks for `_bmad/core/config.yaml` and adapts automatically.

Configure in `guild.config.yaml` at the project root.

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
- Individual agents: `/guild-agent-ranger`, `/guild-agent-mage`, `/guild-agent-rogue`, `/guild-agent-warlock`, `/guild-agent-sage`, `/guild-agent-healer`
- Individual commands: `/guild-heuristic-eval`, `/guild-critique`, `/guild-user-flow`, etc.
- Raid skills (3-model comparison via atrium): `/guild-raid`, `/ranger-raid`, `/rogue-raid`, `/mage-raid`, `/warlock-raid`, `/sage-raid`, `/healer-raid`, `/guild-master-raid`

## When BMAD is present
- Do NOT use Sally (/bmad-agent-bmm-ux-designer) — Guild replaces her
- After PRD/epic changes, ALWAYS run Guild design sprint before dev implementation
- The workflow is: PM scopes changes → Guild design sprint → then dev implements
- Never go straight from PM to dev on UI-facing changes without running Guild first
