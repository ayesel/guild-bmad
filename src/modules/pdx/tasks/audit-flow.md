# Audit Flow

## Purpose
Evaluate an existing user flow, wireframe, or interaction design for usability issues,
dead ends, missing states, accessibility gaps, and logical inconsistencies.

## Input
The user provides one of:
- A flow diagram (Mermaid, image description, or text)
- A URL to audit (requires Playwright MCP)
- A Figma link (requires Figma MCP)
- A text description of the current flow
- An existing PDX artifact from `_bmad-output/pdx-artifacts/`

## Audit Framework

Evaluate the flow against these 6 dimensions:

### 1. Completeness
- [ ] All user entry points accounted for
- [ ] All exit points (success, error, abandonment) documented
- [ ] Every decision point has all branches defined
- [ ] Error states exist for every action that can fail
- [ ] Empty, loading, partial, and populated states covered
- [ ] Edge cases documented (timeout, offline, concurrent edits, etc.)

### 2. Usability (Nielsen's Heuristics Applied to Flows)
- [ ] **Visibility of system status** — User knows where they are in the flow
- [ ] **Match real world** — Flow matches user's mental model, not system architecture
- [ ] **User control** — Can undo, go back, or exit at every step
- [ ] **Consistency** — Similar actions work the same way throughout
- [ ] **Error prevention** — Design prevents errors before they happen
- [ ] **Recognition over recall** — User doesn't need to remember info between steps
- [ ] **Flexibility** — Supports both novice and expert paths
- [ ] **Aesthetic/minimal** — No unnecessary steps or information
- [ ] **Error recovery** — Clear, actionable error messages with recovery paths
- [ ] **Help** — Contextual help available at complex decision points

### 3. Accessibility
- [ ] Flow is completable via keyboard alone
- [ ] Screen reader announcements at state transitions
- [ ] No information conveyed by color alone
- [ ] Time-dependent steps have adequate time or extensions
- [ ] Focus management defined for dynamic content
- [ ] Error messages are associated with their fields

### 4. Logic
- [ ] No orphan nodes (unreachable states)
- [ ] No infinite loops without exit conditions
- [ ] No dead ends (states with no outbound transitions)
- [ ] Decision criteria are unambiguous
- [ ] All conditional branches are mutually exclusive and exhaustive

### 5. Performance
- [ ] No unnecessary round-trips or redundant steps
- [ ] Long operations have progress indicators
- [ ] Optimistic UI considered where appropriate
- [ ] Data fetching strategy defined (eager vs lazy)

### 6. Handoff Readiness
- [ ] Artifact is specific enough for a developer to implement
- [ ] All states have content/copy defined
- [ ] API endpoints or data requirements are noted
- [ ] Animation/transition specifications included where relevant

## Output Format

Generate a structured audit report:

```markdown
---
artifact: Flow Audit
target: [what was audited]
status: complete
severity_summary:
  critical: [count]
  major: [count]
  minor: [count]
  suggestion: [count]
---

## Audit Summary
[One paragraph overview of findings]

## Critical Issues
[Issues that block the flow from working correctly]

## Major Issues
[Issues that significantly degrade the user experience]

## Minor Issues
[Issues that are suboptimal but not blocking]

## Suggestions
[Opportunities for improvement]

## Recommended Fixes
[Prioritized list of fixes with estimated effort]
```

## Output Location
Save to: `_bmad-output/pdx-artifacts/audit-[target-name].md`
