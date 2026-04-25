# Run QA

## Purpose
Execute a structured design quality assurance check using the specified template. This task
is the core QA engine for the Guild Design QA agent.

## Pre-flight Checks

Before executing any QA activity, perform these checks in order:

### 0. Load BMAD Project State (BEFORE all other checks)
- Read `{output_root}/implementation-artifacts/sprint-status.yaml` if it exists
  - Note current sprint number
  - Note existing story count and highest story ID
  - Note which epics are active
  - Note what's TODO vs IN PROGRESS vs DONE
- **Brownfield vs Greenfield determination:**
  - IF sprint-status.yaml exists → this is BROWNFIELD. Continue from existing state. NEVER start numbering from 1. Adapt all output to fit the existing structure.
  - IF sprint-status.yaml does NOT exist → this is GREENFIELD. Start fresh but use BMAD-compatible formats.
- This context informs all artifact generation:
  - Don't redesign things that are already DONE
  - Reference existing story IDs when relevant
  - Align recommendations with current sprint priorities
  - Use the same naming conventions the project uses

### Artifact Source of Truth Rule
Guild artifacts in {output_root}/guild-artifacts/ are ALWAYS the source of truth.
When BMAD documents (PRD, architecture, UX_Design.md) need design content:
- Write the FULL artifact to {output_root}/guild-artifacts/ using Guild templates
- Write a SUMMARY in the BMAD document with key findings inline
- REFERENCE the full artifact: "See full details: {output_root}/guild-artifacts/[filename].md"
- NEVER duplicate the full Guild artifact content inside a BMAD document
- The summary should be enough for a PM to understand; the full artifact is for designers and developers

### 1. Load Project Context
- Read `{output_root}/planning-artifacts/project-context.md` if it exists
- Read `{output_root}/planning-artifacts/prd.md` if it exists
- Read `{output_root}/guild-artifacts/design-tokens.json` if it exists
- Read any existing heuristic evaluations from Ranger in `{output_root}/guild-artifacts/`
- Read any existing accessibility audits from Ranger in `{output_root}/guild-artifacts/`
- Read any existing flows or wireframes from Rogue in `{output_root}/guild-artifacts/`

### 2. Gather QA Parameters from User
Ask the user for the following (skip any already provided):

**Required:**
- What are we QA'ing? (screen, flow, component, full feature)
- What design system or token set applies?
- What is the target standard? (WCAG AA or AAA)

**Contextual (ask if relevant to QA type):**
- What breakpoints should we test? (default: 375px, 768px, 1440px)
- Is there a live implementation to compare against?
- Are there specific areas of concern?
- What's the target handoff date?

### 3. Confirm Scope
Before executing, restate the scope back to the user:
- "Here's what I'll check: [QA type] for [target], against [design system/standard],
  at [breakpoints]. I'll check [states] and flag issues by severity. Sound right?"

## Execution

### Output Format
All QA reports must include:

1. **Header Block** — Title, QA type, version, date, status (pass/fail/conditional-pass)
2. **Executive Summary** — Overall verdict with issue counts by severity
3. **Detailed Findings** — Category-by-category results with evidence
4. **Issue Table** — Every issue with severity, location, description, recommended fix, effort
5. **What's Done Well** — Positive findings worth preserving
6. **Blockers** — Issues that must be resolved before handoff
7. **Recommendations** — Prioritized fixes with effort estimates
8. **Next Steps** — Follow-up actions

### QA State
Set the frontmatter status field:
```yaml
---
artifact: [QA type]
status: [pass|fail|conditional-pass]
version: 1.0
created: [date]
author: Sage (Design QA)
target: [what was QA'd]
severity_summary:
  blocker: [count]
  major: [count]
  minor: [count]
  suggestion: [count]
verdict: "[READY FOR HANDOFF|CONDITIONAL — [n] blockers to resolve|NOT READY]"
references:
  - [list any referenced design system, prior audits, or artifacts]
---
```

### Severity Definitions
- **Blocker**: Prevents handoff — missing states, broken layout, accessibility violation
- **Major**: Must fix before ship — visual inconsistency, token violation, poor responsive behavior
- **Minor**: Fix in next sprint — cosmetic issues, minor spacing, non-critical enhancement
- **Suggestion**: Nice to have — optimization opportunities, polish items

### Quality Checks Before Delivery
- [ ] All states tested (empty, loading, error, populated, disabled)
- [ ] All specified breakpoints checked
- [ ] Accessibility baseline verified (contrast, keyboard, labels)
- [ ] Design system compliance scored
- [ ] Every finding has a recommended fix
- [ ] Every finding has a severity rating
- [ ] Every finding has an effort estimate (S/M/L)
- [ ] Positive patterns are documented alongside issues

## Output Location
Save to: `{output_root}/guild-artifacts/qa-[type]-[scope].md`

## Post-Execution
After delivering the QA report:
1. State the overall verdict (pass/fail/conditional)
2. Highlight the top blocker (if any)
3. Call out the strongest positive finding
4. Suggest next action (fix blockers → re-QA, or proceed to handoff)
