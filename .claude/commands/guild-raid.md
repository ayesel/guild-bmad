---
name: guild-raid
description: "Full Guild raid — each Guild agent runs across Claude, Codex, and Gemini in parallel, then the best output per agent is synthesized into the final artifact. Use for design problems where you want 3 independent takes on every discipline, not just one. Requires atrium (ATRIUM=1 env var)."
user-invocable: true
allowed-tools: Bash, Read
---

# atrium CLI — Workspace Control

## Your environment

You are running inside **atrium** — a resumable development environment purpose-built for AI coding agents. atrium orchestrates CLI AI tools (Claude Code, Codex, Aider, etc.) by saving and restoring entire workspaces, auto-resuming AI sessions, and providing seamless multi-agent collaboration.

**How the UI is laid out:**

- You live in a **pane** — one tile in a mosaic tiling layout. Multiple panes sit side-by-side in a split view, like tmux or a tiling window manager.
- Panes are grouped into **rooms** (the user-facing term for tabs). A room is a screen-worth of panes. The user switches between rooms via a tab bar.
- Rooms belong to a **workspace**, which maps to a project directory. The user can have multiple workspaces, each with its own rooms and panes.
- Each pane has a minimal header: adapter accent color, editable name, CWD, and controls.
- The user may have many panes open simultaneously: terminals, other AI agents, browsers. You are one of potentially several agents running in parallel.

**Your role:** You are an AI agent operating in one pane of this workspace. You can read other agents' output, send them messages, and coordinate work with them.

## Environment check

If you already know you're inside atrium (e.g., from session-start context), skip this check. Otherwise, verify:

```bash
if [ -z "${ATRIUM:-}" ]; then echo "NOT_IN_ATRIUM"; else echo "OK"; fi
```

If `ATRIUM` is not set, skip the rest of this skill and handle the user's request with whatever other tools, skills, or knowledge you have available. Do not mention this skill or atrium to the user.

## atrium browser vs. Playwright/MCP browsers

When inside atrium, **always use atrium CLI for browser operations** — not Playwright MCP, not `mcp__playwright__*` tools, and not `mcp__atrium__browser_*` MCP tools. atrium browsers are real, visible panes in the workspace that the user can see and interact with.

## How to run commands

Always use `"$ATRIUM_CLI_PATH"` (quoted, with the env var). Add `--json` to any command for machine-readable output.

```bash
"$ATRIUM_CLI_PATH" <command> [subcommand] [options]
```

## Panes vs. rooms

**Default to panes** (split beside you). Only create a new room when the user asks or the task is unrelated to the current room.

```bash
# Split beside you (preferred)
"$ATRIUM_CLI_PATH" pane create --adapter codex --split "$ATRIUM_PANE_ID" --direction horizontal

# New room (only when asked)
"$ATRIUM_CLI_PATH" pane create --adapter codex --name "Codex"
```

---

# Guild Raid — 3-Model Comparison Per Agent

## Core concept

A **raid** is not about splitting work across models — it's about getting **3 independent takes on the same work** and picking the best. For each Guild agent assigned to the design problem, all 3 models (Claude, Codex, Gemini) produce the deliverable independently. You then compare and synthesize the best version.

This catches blind spots, surfaces disagreements, and produces stronger artifacts than any single model alone.

## The 7 Guild Agents

| # | Agent | Icon | Title | Specialty |
|---|-------|------|-------|-----------|
| 1 | **Ranger** | 🔍 | UX Researcher | 19 research methods, user interviews, usability testing, data synthesis |
| 2 | **Rogue** | 🔀 | Interaction Designer | User flows, task analysis, IA, wireframes, state diagrams, swim lanes |
| 3 | **Mage** | 🎨 | Visual Designer | UI polish, spacing, typography, color systems, responsive design, critique |
| 4 | **Warlock** | ✍️ | Content Strategist | Microcopy, voice/tone, error messages, onboarding copy, naming |
| 5 | **Sage** | 🛡️ | Design QA | Accessibility audit, design system compliance, pattern checks, quality gates |
| 6 | **Healer** | 📦 | Design Ops | Handoff specs, Jira stories, design tokens, component specs, export |
| 7 | **Guild Master** | 🎯 | Sprint Orchestrator | Pipeline coordination, project state detection, agent routing |

## When to use Guild Raid

- You want the **strongest possible output** for each design discipline — not just one model's take
- The design problem is high-stakes or will go to stakeholders
- You want to surface where models **agree** (high confidence) and **disagree** (needs investigation)
- The user says "raid", "full guild", "3-model comparison", "get all perspectives", or similar

## How it works

```
/guild-raid [topic]
    |
    +-- Phase 1: Select Guild Agents
    |   Pick 3-5 agents relevant to the design problem
    |
    +-- Phase 2: Raid Rounds (one per agent)
    |   For EACH selected Guild agent:
    |   +-- Brief Claude, Codex, and Gemini with the SAME agent persona + task
    |   +-- Collect all 3 outputs
    |   +-- Compare: converging points, diverging points, unique insights
    |   +-- Synthesize best-of into the canonical agent deliverable
    |
    +-- Phase 3: Cross-Agent Synthesis
    |   +-- Combine all canonical deliverables into unified design artifact
    |   +-- Generate stakeholder executive brief
    |
    +-- Phase 4: Multi-Model Review (optional, user chooses)
        +-- Run BMAD review methodologies across models
```

---

## Phase 1: Select Guild Agents

Analyze the design problem and pick which Guild agents are needed.

**Example breakdowns:**

**"Design the customer portal dashboard"**
- 🔍 Ranger: Competitive audit of energy portal dashboards
- 🔀 Rogue: Dashboard navigation flow + wireframe
- 🎨 Mage: Visual hierarchy + spacing/typography
- ✍️ Warlock: Dashboard microcopy + empty states
- 🛡️ Sage: Accessibility audit of dashboard patterns

**"Redesign the pricing page"**
- 🔍 Ranger: JTBD analysis + competitive audit
- 🔀 Rogue: Pricing → checkout user flow
- ✍️ Warlock: Tier naming + CTA copy
- 🛡️ Sage: WCAG 2.2 audit

Not every problem needs all 7. Pick what's relevant.

Tell the user which agents you've selected and why before proceeding.

---

## Phase 2: Raid Rounds

### Setup: Launch agents

```bash
# Launch Codex
"$ATRIUM_CLI_PATH" pane create --adapter codex --split "$ATRIUM_PANE_ID" --direction horizontal

# Launch Gemini
"$ATRIUM_CLI_PATH" pane create --adapter gemini --split "$ATRIUM_PANE_ID" --direction horizontal
```

Get IDs:
```bash
"$ATRIUM_CLI_PATH" agent list --json
```

### For EACH selected Guild agent, run a raid round

A raid round means all 3 models produce the **same** deliverable using the **same** Guild agent persona. You (Claude) do yours locally; Codex and Gemini do theirs in their panes.

#### Step 1: Build the brief

Use this template for every raid round. All 3 models get the **identical brief** (except model-specific instructions like browser access).

```
You are participating in a Guild Raid. You are embodying a specific Guild agent persona and producing a design deliverable. Two other AI models are producing the SAME deliverable independently — your output will be compared and the best elements synthesized.

**Your Guild Agent:** [Agent name] — [Agent title] [Icon]
**Agent Persona:** [Key persona details from the agent definition file]
**Design Problem:** [topic from user]
**Your Deliverable:** [specific artifact this agent should produce]

**Agent Rules:**
[Copy the relevant <rules> from the agent definition]

**Output Structure:**
1. **Problem Statement** — the design problem from this agent's perspective
2. **Approach** — methodology, existing artifacts referenced, assumptions
3. **Deliverable** — the main artifact in structured markdown (use Mermaid for flows/diagrams)
4. **Key Decisions** — numbered list of design decisions with rationale
5. **Handoff Notes** — what downstream agents need to know
6. **Open Questions** — unknowns, risks, and what would increase confidence
7. **Confidence** — high / medium / low with rationale

**Important:**
- Stay in character as your Guild agent
- Reference existing project artifacts in _bmad-output/ if they exist
- Distinguish between evidence-based decisions and assumptions
- If you have browser access, use it to gather real data
- Be specific and opinionated — we're comparing outputs, so hedging is less useful than a strong take
```

#### Step 2: Send to all models

```bash
# Send to Codex
"$ATRIUM_CLI_PATH" agent message <codex-id> "<brief>"

# Send to Gemini
"$ATRIUM_CLI_PATH" agent message <gemini-id> "<brief>"
```

Do your own version locally in parallel.

#### Step 3: Collect all 3 outputs

```bash
"$ATRIUM_CLI_PATH" pane read <codex-pane-id>
"$ATRIUM_CLI_PATH" pane read <gemini-pane-id>
```

#### Step 4: Compare and synthesize

For each raid round, produce a **Raid Comparison** that becomes the canonical deliverable:

```markdown
## Raid Round: [Icon] [Agent Name] — [Agent Title]

### Model Comparison

| Dimension | Claude | Codex | Gemini |
|-----------|--------|-------|--------|
| Approach | [summary] | [summary] | [summary] |
| Key insight | [strongest point] | [strongest point] | [strongest point] |
| Confidence | [H/M/L] | [H/M/L] | [H/M/L] |
| Unique contribution | [what only this model caught] | [what only this model caught] | [what only this model caught] |

### Converging Points (high confidence — all models agree)
- [point 1]
- [point 2]

### Diverging Points (investigate further — models disagree)
- [point 1]: Claude says X, Codex says Y, Gemini says Z
- [point 2]: ...

### Synthesized Deliverable
[The best-of version — cherry-pick the strongest elements from each model's output, resolve conflicts, produce the canonical artifact]

### Synthesis Rationale
[Why you picked what you picked from each model]
```

#### Sequencing raid rounds

You can run raid rounds in **parallel** (brief all agents for multiple Guild agents at once) or **sequential** (wait for Ranger output before briefing Rogue, so Rogue has research context).

**Recommended approach:**
1. **Parallel first wave**: Agents with no dependencies (Ranger + Warlock can often run simultaneously)
2. **Sequential second wave**: Agents that benefit from upstream context (Rogue after Ranger, Mage after Rogue, Sage after all others)

When running sequentially, include the synthesized output from the prior round in the next brief:

```
**Context from prior raid round:**
[Paste the synthesized deliverable from the upstream agent]
```

### Agent-specific briefing notes

**Ranger (Research):**
- Specify which of the 19 research methods to use
- Always ask for findings vs. insights distinction
- Request confidence levels and evidence citations

**Rogue (Interaction Design):**
- Request Mermaid diagrams for all flows
- Require entry points, exit points, and error states
- Ask for edge case documentation

**Mage (Visual Design):**
- If reviewing existing UI: ask for screenshot-based critique
- If designing new: ask for spacing, typography, and color specs
- Request responsive considerations

**Warlock (Content Strategy):**
- Specify the copy context (onboarding, error, empty state, CTA, etc.)
- Request voice/tone alignment notes
- Ask for copy variations (A/B options)

**Sage (Design QA):**
- Specify audit type (accessibility, pattern check, system check, states audit)
- Request GO / CONDITIONAL GO / NO-GO verdict
- Ask for prioritized findings (critical vs. minor)

**Healer (Design Ops):**
- Specify output type (handoff spec, Jira stories, design tokens, component spec)
- Request developer-ready format
- Ask for acceptance criteria on all stories

### Ranger's 19 Research Methods

| # | Method | Best for |
|---|--------|----------|
| 1 | Heuristic Evaluation | Auditing existing UI against Nielsen's 10 |
| 2 | Competitive Audit | Comparing against competitors |
| 3 | Persona Generation | Building evidence-based user profiles |
| 4 | Journey Map | Mapping emotional arc and pain points |
| 5 | Interview Script | Structuring user conversations |
| 6 | Research Synthesis | Combining multiple data sources |
| 7 | Usability Test | Defining task scenarios and success metrics |
| 8 | Accessibility Audit | WCAG 2.2 compliance review |
| 9 | JTBD | Mapping functional, emotional, social jobs |
| 10 | Card Sort | Information architecture validation |
| 11 | A/B Test | Hypothesis and variant planning |
| 12 | Survey | Validated questionnaire design |
| 13 | Stakeholder Interview | Internal discovery |
| 14 | Workshop | Collaborative ideation |
| 15 | Affinity Diagram | Thematic clustering of raw data |
| 16 | Service Blueprint | Frontstage/backstage mapping |
| 17 | Empathy Map | User segment mental models |
| 18 | Story Map | User stories organized by journey |
| 19 | Diary Study | Longitudinal behavior tracking |

---

## Phase 3: Cross-Agent Synthesis

After all raid rounds are complete, combine the canonical (best-of) deliverables into a unified artifact.

Save to: `_bmad-output/guild-artifacts/guild-raid-[topic].md`

```markdown
---
artifact: guild-raid-synthesis
status: draft
version: 1.0
created: [date]
author: Guild Raid (3-Model Comparison Session)
confidence: [high|medium|low]
confidence_rationale: "[basis for rating]"
agents_used: [list Guild agents]
models: [claude, codex, gemini]
raid_rounds: [number of rounds completed]
references: [sources cited]
---

# Guild Raid Synthesis: [Topic]

## Executive Summary
[3-5 bullet points — the most important design decisions, highlighting where all 3 models converged]

## Raid Results by Agent

### [Icon] [Agent Name] — [Agent Title]
**Models agreed on:** [key converging points]
**Models disagreed on:** [key diverging points and resolution]
**Canonical deliverable:** [the synthesized best-of artifact]

[... repeat for each agent ...]

## Cross-Agent Alignment
[Design decisions reinforced across multiple agents' canonical deliverables]

## High-Confidence Decisions (3-model convergence)
[Decisions where all 3 models independently arrived at the same answer — these are your strongest recommendations]

## Investigation Needed (model divergence)
[Decisions where models disagreed — ranked by impact, with recommended next step for each]

## Integrated Design Recommendations
[Unified, prioritized list of design decisions]

## Open Questions
[Grouped by which agent should investigate]

## Pipeline Next Steps
[What should happen next in the Guild pipeline]
```

### Executive brief

Save to: `_bmad-output/guild-artifacts/[topic]-executive-brief.md`

```markdown
# [Topic]: Design Brief for Review

**Date:** [date]
**Prepared by:** Product Design (Guild Raid — 3-model comparison across [N] design disciplines)
**Status:** Ready for feedback

---

## What We Did
[2-3 sentences: which Guild agents, 3-model comparison methodology, key deliverables]

## The Big Finding
[1-2 paragraphs — the most important design insight, especially where all 3 models converged]

## High-Confidence Recommendations
[Table: recommendation | rationale | all models agreed? | effort level]

## Key Design Decisions
[Numbered list with reasoning]

## Needs Further Investigation
[Where models disagreed — stakeholder input or additional research needed]

## Open Questions for [Stakeholder]
[Decisions that need stakeholder input]

## Supporting Artifacts
[Table linking to raid round comparisons and canonical deliverables]
```

---

## Phase 4: Multi-Model Review (optional)

After synthesis, run structured reviews to catch weaknesses before stakeholder review.

### Review types

| # | Review | Methodology | What It Catches |
|---|--------|-------------|----------------|
| 1 | **Adversarial Review** | `/bmad-review-adversarial-general` | Weak claims, logical gaps, overconfidence |
| 2 | **Structural Editorial** | `/bmad-editorial-review-structure` | Poor organization, redundancy, readability |
| 3 | **Design QA (Sage)** | Guild Sage agent | Accessibility, pattern issues, design system compliance |
| 4 | **Edge Case Hunter** | `/bmad-review-edge-case-hunter` | Unhandled scenarios, boundary conditions, blind spots |

### Review modes

Ask the user:

> "Raid synthesis and executive brief are ready. Before sharing, I can run quality reviews:
> - **Single model** — I run all 4 reviews myself (faster)
> - **All models** — Claude, Codex, and Gemini each run independent reviews (most thorough)
>
> Which do you prefer, or skip reviews?"

**All models distribution:**

| Agent | Reviews | Why |
|-------|---------|-----|
| **Claude** | Adversarial Review + Design QA (Sage) | Strongest at critical analysis and design system evaluation |
| **Codex** | Edge Case Hunter + Structural Editorial | Strong at systematic boundary checking and structural assessment |
| **Gemini** | Adversarial Review + Edge Case Hunter | Independent second opinion on the two most critical reviews |

Brief template for reviewers:

```
You are reviewing a design deliverable for quality before stakeholder review.

**Document to review:** [path to raid synthesis]
**Supporting artifacts:** [paths to individual raid round comparisons]

**Your review type:** [Adversarial Review / Edge Case Hunter / Structural Editorial / Design QA]

**Instructions:**
- [For Adversarial]: Challenge every design decision. Find the weakest rationale. Rate each as: solid / soft / unsupported.
- [For Edge Case Hunter]: Walk every flow and find scenarios where it breaks. What user types, device contexts, or edge cases would invalidate the design?
- [For Structural Editorial]: Propose cuts, reorganization, simplification. Is it scannable in 2 minutes?
- [For Design QA (Sage)]: Sage-style quality gate. Check accessibility, design system compliance, pattern appropriateness. Issue GO / CONDITIONAL GO / NO-GO.

**Output format:**
1. Overall assessment (GO / CONDITIONAL GO / REVISE)
2. Critical findings (must fix)
3. Minor findings (nice to fix)
4. What's strong (don't change)

Write to: _bmad-output/guild-artifacts/review-[type]-[topic].md
Then send summary via agent message.
```

Collect reviews, compile summary, apply fixes.

---

## Full workflow summary

```
/guild-raid [topic]
    |
    +-- Phase 1: Select Guild Agents (3-5 relevant to the problem)
    |
    +-- Phase 2: Raid Rounds
    |   For EACH agent:
    |   +-- Brief Claude + Codex + Gemini with SAME persona + task
    |   +-- Collect 3 independent outputs
    |   +-- Compare: converging / diverging / unique insights
    |   +-- Synthesize best-of into canonical deliverable
    |   (sequential or parallel depending on agent dependencies)
    |
    +-- Phase 3: Cross-Agent Synthesis
    |   +-- Combine canonical deliverables into unified artifact
    |   +-- Highlight 3-model convergence points (highest confidence)
    |   +-- Flag divergence points (needs investigation)
    |   +-- Generate stakeholder executive brief
    |
    +-- Phase 4: Multi-Model Review (optional)
        +-- Single model or all models
        +-- Adversarial + Edge Case + Structural + Design QA
```

---

## Tips

- **IDs**: Use `--json` to get agent/pane IDs programmatically.
- **Terminology**: Say "room" (not "tab") in user-facing text.
- **Source field**: Use `--source "adapter:claude-code"` when creating tasks/comments.
- **YOLO mode**: Launch Gemini with `--yolo` to skip permission prompts. Codex auto-detects from atrium.
- **Codex adapter issues**: If Codex gets zsh errors from agent messages, close and relaunch the pane.
- **Browser timeouts**: Brief agents to use fallback strategies if browser snapshots time out.
- **Not all agents every time**: 3-5 agents per raid is the sweet spot. All 7 on a small problem creates noise.
- **Parallel vs. sequential rounds**: Run independent agents in parallel (Ranger + Warlock). Run dependent agents sequentially (Rogue after Ranger). Include upstream context in sequential briefs.
- **When to raid vs. single-model**: Raid for high-stakes deliverables, stakeholder reviews, or when you want maximum confidence. Single-model Guild agents (`/guild-agent-ranger`, etc.) are fine for quick explorations.
- **Convergence is signal**: When all 3 models independently reach the same design decision, that's your highest-confidence recommendation. Lead with those in the executive brief.
