---
name: 'bmad-autonomous-build'
description: 'Full autonomous pipeline — runs Guild design + BMAD reviews + dev build loop end-to-end'
---

# Autonomous Build

You are the orchestrator. You do NOT implement anything directly — you delegate every step to a subagent using the Agent tool and wait for it to complete before proceeding to the next step. Between steps, you read outputs and make routing decisions.

You run the COMPLETE Guild + BMAD pipeline in order. Do NOT skip steps. Do NOT batch steps. Each step must complete before the next begins.

## Phase 1: Research

### Step 1: Visual Audit
Invoke a subagent to run `/guild-visual-audit`. Provide it with:
- The product category and competitor URLs to analyze
- Instruction to use Atrium browser if available (`$ATRIUM_CLI_PATH`)
- Instruction to also search Dribbble and Behance for design inspiration
Wait for it to complete. Read the output artifact at `{output_root}/guild-artifacts/visual-audit-*.md`.

### Step 2: Research Synthesis
Invoke a subagent to run `/guild-research-synthesis`. It should synthesize:
- Any existing research artifacts in `{output_root}/guild-artifacts/`
- The visual audit from Step 1
- Any user interviews or stakeholder feedback
- Any Confluence documentation referenced in the project
Wait for it to complete. Read the output artifact.

## Phase 2: Design

### Step 3: Content & Microcopy
Invoke a subagent to run `/guild-agent-warlock`. Provide the research synthesis as context. The Warlock should write all page/screen copy, labels, empty states, error messages, and microcopy.
Wait for it to complete.

### Step 4: Editorial Review
Invoke a subagent to run `/bmad-editorial-review-prose` on the Warlock's copy output. This polishes the content before it gets designed around.
Wait for it to complete. If significant changes, update the copy artifact.

### Step 5: Interaction Design
Invoke a subagent to run `/guild-agent-rogue`. Provide the polished copy and research synthesis. The Rogue should produce wireframes, user flows, state diagrams, and interaction maps.
Wait for it to complete.

### Step 6: Visual Design
Invoke a subagent to run `/guild-agent-mage`. Provide the wireframes, copy, and visual audit (for design references). The Mage applies visual design.
Wait for it to complete.

### Step 7: Design QA
Invoke a subagent to run `/guild-agent-sage`. The Sage reviews everything for accessibility, design system compliance, and quality.
Wait for it to complete. **READ THE VERDICT.**

**IF SAGE SAYS NO-GO: STOP.** Report the NO-GO findings to the user and do not proceed. The pipeline halts until issues are resolved.

**IF SAGE SAYS GO or CONDITIONAL GO:** Proceed to Phase 3.

## Phase 3: Review

### Step 8: Multi-Agent Review
Invoke a subagent to run `/bmad-party-mode`. Have multiple agents review the complete design — look for gaps, contradictions, and missed edge cases.
Wait for it to complete.

### Step 9: Edge Case Sweep
Invoke a subagent to run `/bmad-review-edge-case-hunter` on the design artifacts. This catches boundary conditions and unhandled scenarios.
Wait for it to complete. If critical issues found, loop back to the relevant design step.

## Phase 4: Handoff

### Step 10: Dev Handoff
Invoke a subagent to run `/guild-agent-healer`. Produce the complete dev handoff spec with component inventory, spacing, states, and copy.
Wait for it to complete.

### Step 11: Pre-Handoff Quality Gate
Invoke a subagent to run `/guild-pre-handoff`. Full quality gate before dev.
Wait for it to complete. If NO-GO, loop back to fix issues.

### Step 12: UX Spec
Invoke a subagent to run `/guild-ux-spec`. Package all Guild artifacts into BMAD-compatible UX_Design.md.
Wait for it to complete.

### Step 13: Generate Stories
Invoke a subagent to run `/guild-jira-stories`. Generate dev subtasks from the design artifacts.
Wait for it to complete.

## Phase 5: Build

### Step 14: Sprint Planning
Invoke a subagent to run `/bmad-sprint-planning`. Set up sprint-status.yaml from the generated epics and stories.
Wait for it to complete. Read sprint-status.yaml to confirm stories are ready.

### Step 15: Dev Loop
Repeat the following until all epics in `sprint-status.yaml` are marked `done`:

#### 15a. Create Story
Invoke a subagent to run `/bmad-create-story`. Wait for it to complete. Read the resulting story file path.

#### 15b. Dev Story
Invoke a subagent to run `/bmad-dev-story <story-file-path>`. Wait for it to complete.

#### 15c. Code Review
Simultaneously:
* Invoke a subagent to run `/bmad-code-review`. Wait for it to complete. Check the story status.
* Invoke a subagent to run `/bmad-create-story` for the next story so it's ready.

#### 15d. Review Fix Loop
If story status is NOT `done` after code review:
a. Invoke a subagent to run `/bmad-dev-story <story-file-path>` on the same story.
b. Invoke a subagent to run `/bmad-code-review`.
c. Repeat until done or 3 cycles reached.

#### 15e. Commit
Commit all changes for the completed story. Do not commit the next story.

#### 15f. Next Story
Return to 15b. When an epic completes, continue to the next. Do not wait for human approval.

## Exit Conditions

* All epics in `sprint-status.yaml` are `done` — report completion
* Sage issues NO-GO — halt and report to user (Step 7)
* Pre-handoff gate fails — halt and report to user (Step 11)
* A story fails code review 3 times — skip it, mark blocked, continue to next
* A critical error blocks progress — stop and report to user

## Progress Report

After each step, output:
```
Phase [N]/5 — Step [N]/15: [Step Name] — [COMPLETE/IN PROGRESS/BLOCKED]
```

After each story completion in Phase 5:
```
Story [ID] complete. [N] remaining in sprint. [done]/[total] stories completed.
```
