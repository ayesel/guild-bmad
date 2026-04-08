# BMAD Integration Rules

## PM → PDX Handoff
When BMAD's PM agent creates a PRD, it may also generate PDX-format artifacts:
- Persona cards (saved to _bmad-output/guild-artifacts/)
- Journey maps (saved to _bmad-output/guild-artifacts/)
- Research summaries embedded in the PRD

These are valid PDX artifacts. Guild agents should:
- READ them as context
- REFERENCE them in downstream artifacts
- NOT recreate them unless explicitly asked
- EXTEND them if the scope has changed

## PDX → BMAD Dev Handoff
When PDX completes a design sprint:
- Stories go to _bmad-output/implementation-artifacts/stories/
- sprint-status.yaml is updated with new stories
- UX_Design.md is generated at _bmad-output/planning-artifacts/
- BMAD's dev agent picks up stories via /dev-story
- BMAD's SM agent manages sprint planning

## Sally Replacement
PDX replaces BMAD's built-in UX Designer (Sally). When PDX is installed:
- The PM should route to PDX after PRD, not to Sally
- If the PM offers "UX design" as a next step, it means "run PDX design sprint"
- The architecture phase should reference PDX artifacts, not Sally's UX_Design.md
- After architecture, Guild Master handles the rest

## Artifact Ownership
| Artifact | Owner | Location |
|----------|-------|----------|
| Product Brief | BMAD Analyst | _bmad-output/planning-artifacts/ |
| PRD | BMAD PM | _bmad-output/planning-artifacts/ |
| Architecture | BMAD Architect | _bmad-output/planning-artifacts/ |
| Personas | PDX Nova (or PM) | _bmad-output/guild-artifacts/ |
| Journey Maps | PDX Nova (or PM) | _bmad-output/guild-artifacts/ |
| User Flows | PDX Kai | _bmad-output/guild-artifacts/ |
| Wireframes | PDX Kai | _bmad-output/guild-artifacts/ |
| Microcopy | PDX Echo | _bmad-output/guild-artifacts/ |
| Error Messages | PDX Echo | _bmad-output/guild-artifacts/ |
| QA Reports | PDX Sage | _bmad-output/guild-artifacts/ |
| Component Specs | PDX Relay | _bmad-output/guild-artifacts/ |
| Design Tokens | PDX Relay | _bmad-output/guild-artifacts/ |
| UX_Design.md | PDX Relay (compiled) | _bmad-output/planning-artifacts/ |
| Stories | PDX Relay | _bmad-output/implementation-artifacts/stories/ |
| Sprint Status | BMAD SM | _bmad-output/implementation-artifacts/ |

## Flow for Existing Projects (Brownfield)

The typical brownfield flow when PM creates a PRD with PDX artifacts:

1. PM creates PRD → generates personas + journey maps as PDX artifacts
2. User runs @guild-master /design-sprint
3. Orchestrator detects: brownfield + existing personas + existing journey maps
4. Nova: skips persona/journey, runs only what's missing (heuristic eval, competitive audit)
5. Kai → Echo → Sage → Relay → PM review → SM → Dev

## Flow for New Projects (Greenfield)

1. Analyst creates product brief
2. PM creates PRD → may generate initial personas
3. @guild-master /design-sprint detects greenfield
4. Nova: validates/extends PM's personas, runs full research suite
5. Kai → Echo → Architect → Sage → Relay → PM review → SM → Dev
