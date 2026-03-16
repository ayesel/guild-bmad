# PDX Design Framework

## Project Overview
PDX (Product Design Experience) is an AI-powered design module built on BMAD v6. It adds 7 specialized design agents (Nova, Kai, Echo, Lux, Sage, Relay, PDX Orchestrator) that run adaptive design-to-sprint pipelines.

## Key Design Principles
- PDX agents are BMAD modules — they follow BMAD conventions for artifacts, stories, and sprint tracking
- Brownfield-first — assume every project has existing state until proven otherwise
- Artifacts are source of truth — PDX artifacts live in pdx-artifacts/ and are referenced by BMAD docs, never duplicated into them
- Each agent has a distinct persona and stays in character during sessions
- Design QA (Sage) is a quality gate — NO-GO stops the pipeline

## Project Structure
- `src/modules/pdx/agents/` — Agent YAML source files
- `src/modules/pdx/tasks/` — Task execution files
- `src/modules/pdx/templates/` — Output templates (YAML)
- `src/modules/pdx/workflows/` — Pipeline workflow definitions
- `_bmad/pdx/agents/` — Compiled agents for short-name loading
- `.claude/commands/pdx-*.md` — Slash commands for all PDX menu items

## Running PDX
- `/pdx-orchestrator` — Load the orchestrator for full pipeline control
- `/pdx-design-sprint` — Run adaptive pipeline (auto-detects greenfield/brownfield)
- Individual agents: `/pdx-ux-researcher`, `/pdx-visual-designer`, `/pdx-interaction-designer`, `/pdx-content-strategist`, `/pdx-design-qa`, `/pdx-design-ops`
- Individual commands: `/pdx-heuristic-eval`, `/pdx-critique`, `/pdx-user-flow`, etc.
