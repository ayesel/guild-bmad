# PDX Design Framework

## Project Overview
PDX (Product Design Experience) is an AI-powered design module built on BMAD v6. It adds 7 specialized design agents (Nova, Kai, Echo, Lux, Sage, Relay, PDX Orchestrator) that run adaptive design-to-sprint pipelines.

## Key Design Principles
- Guild agents are BMAD modules — they follow BMAD conventions for artifacts, stories, and sprint tracking
- Brownfield-first — assume every project has existing state until proven otherwise
- Artifacts are source of truth — Guild artifacts live in guild-artifacts/ and are referenced by BMAD docs, never duplicated into them
- Each agent has a distinct persona and stays in character during sessions
- Design QA (Sage) is a quality gate — NO-GO stops the pipeline

## Project Structure
- `src/modules/guild/agents/` — Agent YAML source files
- `src/modules/guild/tasks/` — Task execution files
- `src/modules/guild/templates/` — Output templates (YAML)
- `src/modules/guild/workflows/` — Pipeline workflow definitions
- `_bmad/guild/agents/` — Compiled agents for short-name loading
- `.claude/commands/guild-*.md` — Slash commands for all Guild menu items

## Running PDX
- `/guild-master` — Load the orchestrator for full pipeline control
- `/guild-design-sprint` — Run adaptive pipeline (auto-detects greenfield/brownfield)
- Individual agents: `/guild-agent-ranger`, `/guild-agent-mage`, `/guild-agent-rogue`, `/guild-agent-warlock`, `/guild-agent-sage`, `/guild-agent-healer`
- Individual commands: `/guild-heuristic-eval`, `/guild-critique`, `/guild-user-flow`, etc.

## PDX Design Framework — Active

This project uses PDX Design Framework for all UX/design work.
- Do NOT use Sally (/bmad-agent-bmm-ux-designer) — PDX replaces her
- After PRD/epic changes, ALWAYS run PDX design sprint before dev implementation
- When listing next steps, replace "Create UX Design with Sally" with "Run PDX Design Sprint (@guild-master)"
- The workflow is: PM scopes changes → PDX design sprint → then dev implements
- Guild agents are in src/modules/guild/agents/
- Never go straight from PM to dev on UI-facing changes without running PDX first
