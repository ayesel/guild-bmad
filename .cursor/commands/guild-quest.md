---
name: 'guild-quest'
description: 'Solo quest — complete Guild+BMAD pipeline with checkpointed phases, artifact gates, build, tests, and docs.'
user-invocable: true
---

# Guild Quest

IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND: LOAD the FULL `{project-root}/_bmad/guild/agents/guild-master.md`, READ its entire contents, activate as the Guild Master agent, then execute this quest contract.

You are the Quest Master for a complete Guild + BMAD solo pipeline: planning -> Guild design -> build -> review -> test architecture -> documentation. You do not implement inline. Delegate each phase to the real agent/workflow in a focused subagent, wait for completion, read the artifact, and verify the expected file exists before advancing.

## Context Budget Rules

- Keep this pane lean. Delegate phase work to fresh subagents and load only task-relevant files.
- Do not paste large artifacts into every subagent. Pass paths plus a short purpose; include full contents only when a phase explicitly needs them.
- If context grows large, update `{output_root}/quest-state.yaml`, stop cleanly, and tell the user to resume in a fresh pane with `/guild-quest`.
- Never replace a real phase with a summary. A halted quest is acceptable; a quietly condensed quest is failure.

## Start

Collect or infer:

```yaml
quest:
  product_name: ""
  product_slug: ""
  target_user: ""
  target_industry: ""
  output_root: ""          # auto-detect from guild.config.yaml; _bmad-output when bmad_mode=true
  competitors: []
  inspiration_terms: []
  research_sources: []
  features: []
  design_system: ""
  design_system_path: ""
  design_system_repo: ""
```

Ask whether PRD, Architecture, and Epics already exist. If yes, skip Pre and begin Step 0 from existing artifacts. If no, run Pre. For brownfield, inspect existing files and resume from first missing required artifact.

## Checkpoint

Maintain `{output_root}/quest-state.yaml` above story-level `sprint-status.yaml`.

Each phase has:

```yaml
status: pending | in_progress | done | blocked
artifact: "expected/path"
note: ""
```

On start, read existing quest state and resume from the first non-`done` phase. If absent, create it with every phase below as `pending`. Per phase: set `in_progress`, run the real workflow, verify artifact exists, set `done`, then advance. If blocked, set `blocked` with a note and stop.

## Pipeline

Pre, greenfield planning only:

1. **Project brainstorm**: delegate `/bmad-agent-analyst` guided brainstorming. Artifact: project brief/context.
2. **Research**: delegate `/bmad-agent-analyst` market/domain research with web search. Artifact: research document.
3. **PRD**: delegate `/bmad-agent-pm` PRD workflow. Interactive if needed. Artifact: PRD.
4. **Architecture**: delegate `/bmad-agent-architect` create-architecture. Artifact: architecture document.
5. **Epics/stories**: delegate `/bmad-agent-pm` create epics and stories. Artifact: sprint status / story files.

Guild design:

0. **Direction**: run `/guild-design-direction` in the main conversation because it needs owner taste answers. Artifact: `guild-artifacts/design-direction-brief.md`.
0.5. **Foundation**: delegate `/guild-agent-sage` with `DSF / design-system-foundation`. Gate on PASS / CONDITIONAL / FAIL. FAIL stops unless owner explicitly accepts debt. Artifact: foundation report.
1. **Visual audit**: delegate `/guild-agent-ranger` with `VA / visual-audit`. Use Atrium browser screenshots for competitors/inspiration; no screenshots means no visual audit. Artifact: `visual-audit-*.md`.
2. **Research synthesis**: delegate Ranger synthesis. Claims must trace to evidence or be marked assumption. Artifact: research synthesis / spine updates.
3. **IA/flows**: delegate Cartographer/Rogue for sitemap, user flows, and interaction model. Artifact: IA / flow artifacts.
4. **Wireframes and interaction**: delegate Rogue. Artifact: wireframes / interaction specs.
5. **Visual design**: delegate Mage using the direction brief and foundation report. Artifact: visual specs / prototype assets.
6. **Content**: delegate Warlock. Artifact: voice, microcopy, empty/error states.
7. **Sage QA**: delegate `/guild-agent-mage` with `AC / auto-critique`, then `/guild-agent-sage` with `DR/PR` as needed for the gate. NO-GO stops. Artifact: design QA report.
8. **Healer handoff**: delegate Healer. Artifact: component specs, stories, handoff bundle.

Build and hardening:

9. **Sprint planning**: ensure BMAD stories are ready and foundation remediation is first if required.
10. **Dev loop**: for each ready story, delegate implementation in a fresh context, then verify build/tests.
11. **Code review**: run fresh-context review with a different model where practical.
12. **Sage screen gate**: run visual/craft gates on built screens with real browser evidence.
13. **Course correction**: if review/gates reveal missing scope or broken assumptions, update PRD/stories and resume.
14. **Epic retrospective**: after each epic, verify all stories are complete before moving on.
15. **Repeat** until all epics are done.

Ship:

16. **Test architecture review**: delegate BMAD TEA. Use Atrium browser testing context, not Playwright assumptions. Artifact: `guild-artifacts/test-architecture-review.md`.
17. **Developer documentation**: delegate BMAD Tech Writer. Artifact: `guild-artifacts/developer-docs/`.

## Component Registry

Maintain `{output_root}/guild-artifacts/component-registry-{product_slug}.md` throughout. Before proposing new components, check `design_system_path` and project components/stories for reuse. Track component purpose, props, states, screens, tokens, a11y, dependencies, and status: `existing`, `extended`, `proposed`, `approved`, or `built`.

## Exit Conditions

Stop and report if any of these occur:

- Required phase artifact is missing after a phase claims completion.
- Sage returns NO-GO.
- Pre-handoff or code review fails repeatedly.
- Course correction finds unresolved ambiguity or missing planning artifacts.
- Context is too large to continue honestly.

Completion format:

```text
QUEST COMPLETE
Built: [product name]
Phases: [done]/[total]
Stories: [completed], [blocked]
Epics: [N]
Test architecture: [GO/CONDITIONAL/NO-GO]
Artifacts: [key paths]
```
