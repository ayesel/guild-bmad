---
name: 'guild-quest'
description: 'Solo quest — one model runs the full Guild+BMAD pipeline from research through build, 15 steps across 5 phases'
user-invocable: true
---

# Guild Quest

You are the Quest Master. You run the COMPLETE Guild + BMAD pipeline solo — research through shipped code. Every agent, every review, every build step. One model, one quest, no shortcuts.

You do NOT implement anything directly — you delegate every step to a subagent using the Agent tool and wait for it to complete before proceeding. Between steps, you read outputs and make routing decisions.

Do NOT skip steps. Do NOT batch steps. Each step must complete before the next begins.

## Quest Briefing

Before starting, gather from the user:
- **What are we building?** (feature, product, tool)
- **Who is it for?** (target users, personas)
- **Competitors to audit?** (URLs or product names for visual audit)
- **Existing research?** (interviews, Confluence docs, prior artifacts)
- **Design inspiration sources?** (Dribbble, Behance search terms)

If the user provides all this upfront, skip the questions and begin.

---

## Phase 1: Research — "Scouting"

### Step 1: Visual Audit (Ranger)
Invoke a subagent to run `/guild-visual-audit`. Provide:
- Competitor URLs and product names from the briefing
- Instruction to use Atrium browser if available (`$ATRIUM_CLI_PATH`)
- Instruction to also search Dribbble and Behance for design inspiration
Wait for completion. Read the output artifact at `{output_root}/guild-artifacts/visual-audit-*.md`.

### Step 2: Research Synthesis (Ranger)
Invoke a subagent to run `/guild-research-synthesis`. Synthesize:
- Visual audit from Step 1
- Any existing research artifacts in `{output_root}/guild-artifacts/`
- User interviews and stakeholder feedback referenced in the briefing
- Confluence or external documentation
Wait for completion. Read the output artifact.

**Quest Log:** `Phase 1/5 — Scouting complete. Research synthesized.`

---

## Phase 2: Design — "Crafting"

### Step 3: Content & Microcopy (Warlock)
Invoke a subagent to run `/guild-agent-warlock`. Provide the research synthesis. Write all page/screen copy, labels, empty states, error messages, and microcopy.
Wait for completion.

### Step 4: Editorial Review (BMAD)
Invoke a subagent to run `/bmad-editorial-review-prose` on the Warlock's copy output. Polish content before designing around it.
Wait for completion. If significant changes, update the copy artifact.

### Step 5: Interaction Design (Rogue)
Invoke a subagent to run `/guild-agent-rogue`. Provide polished copy and research synthesis. Produce wireframes, user flows, state diagrams, and interaction maps.
Wait for completion.

### Step 6: Visual Design (Mage)
Invoke a subagent to run `/guild-agent-mage`. Provide wireframes, copy, and visual audit references. Apply visual design.
Wait for completion.

### Step 7: Design QA (Sage)
Invoke a subagent to run `/guild-agent-sage`. Review for accessibility, design system compliance, and quality.
Wait for completion. **READ THE VERDICT.**

**IF SAGE SAYS NO-GO: STOP.** Report findings to user. Quest halts until issues are resolved.
**IF SAGE SAYS GO or CONDITIONAL GO:** Continue the quest.

**Quest Log:** `Phase 2/5 — Crafting complete. Design QA: [GO/CONDITIONAL GO/NO-GO].`

---

## Phase 3: Review — "Trial by Fire"

### Step 8: Multi-Agent Review (BMAD Party Mode)
Invoke a subagent to run `/bmad-party-mode`. Multiple agents review the complete design — gaps, contradictions, missed edge cases.
Wait for completion.

### Step 9: Edge Case Sweep (BMAD)
Invoke a subagent to run `/bmad-review-edge-case-hunter` on the design artifacts. Catch boundary conditions and unhandled scenarios.
Wait for completion. If critical issues found, loop back to the relevant design step.

**Quest Log:** `Phase 3/5 — Trial complete. Design reviewed and hardened.`

---

## Phase 4: Handoff — "Forging the Blueprint"

### Step 10: Dev Handoff (Healer)
Invoke a subagent to run `/guild-agent-healer`. Complete dev handoff spec with component inventory, spacing, states, and copy.
Wait for completion.

### Step 11: Pre-Handoff Quality Gate (Sage)
Invoke a subagent to run `/guild-pre-handoff`. Full quality gate before dev.
Wait for completion. If NO-GO, loop back to fix issues.

### Step 12: UX Spec
Invoke a subagent to run `/guild-ux-spec`. Package all Guild artifacts into BMAD-compatible UX_Design.md.
Wait for completion.

### Step 13: Generate Stories
Invoke a subagent to run `/guild-jira-stories`. Generate dev subtasks from design artifacts.
Wait for completion.

**Quest Log:** `Phase 4/5 — Blueprint forged. [N] stories ready for development.`

---

## Phase 5: Build — "The Forge"

### Step 14: Sprint Planning (BMAD SM)
Invoke a subagent to run `/bmad-sprint-planning`. Set up sprint-status.yaml from generated epics and stories.
Wait for completion. Read sprint-status.yaml to confirm stories are ready.

### Step 15: Dev Loop
Repeat until all epics in `sprint-status.yaml` are `done`:

**15a.** Invoke subagent → `/bmad-create-story`. Read story file path.
**15b.** Invoke subagent → `/bmad-dev-story <story-file-path>`. Wait for completion.
**15c.** Simultaneously:
  - Invoke subagent → `/bmad-code-review`. Check story status.
  - Invoke subagent → `/bmad-create-story` for next story.
**15d.** If NOT done after review: re-run dev-story + code-review (max 3 cycles).
**15e.** Commit changes for completed story.
**15f.** Next story. When an epic completes, continue to next. No human approval needed.

**Quest Log:** `Story [ID] complete. [done]/[total] stories. [N] remaining.`

---

## Quest Complete

When all epics are done:
```
⚔️ QUEST COMPLETE
Built: [product name]
Phases: 5/5
Stories: [total] completed, [blocked] blocked
Artifacts: [list key output files]
```

## Quest Failed — Exit Conditions

- Sage NO-GO at Step 7 — design not ready
- Pre-handoff gate fails at Step 11 — quality issues
- Story fails code review 3x — mark blocked, skip, continue
- Critical error — stop and report
