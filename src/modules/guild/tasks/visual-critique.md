# Visual Critique

## Purpose
Provide actionable design feedback on a screen or component, covering
UI patterns, accessibility, visual polish, and interaction design.

## Pre-flight Checks

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
- Read `{output_root}/guild-artifacts/design-tokens.json` if it exists
- Read any existing voice/tone or style guidelines in `{output_root}/guild-artifacts/`

## Input
User provides one of:
- A screenshot (image)
- A simulator capture
- A Figma frame URL
- A description of what they're looking at
- A reference to a specific component file

## Before Critiquing
Ask ONE question: "What are you going for with this screen? What should the user
focus on first?"

This prevents critiquing against the wrong goals. If the designer says "I want
the priority labels to be prominent," don't suggest hiding them.

## Critique Framework (evaluate ALL of these)

### 1. Pattern Check
- Is this the right UI pattern for the task? (reference ui-patterns-reference.md)
- Are patterns used correctly? (e.g., bottom sheet vs modal, tabs vs segmented control)
- Are there missing patterns? (e.g., no empty state, no loading state, no error handling)
- Anti-patterns present? (e.g., hamburger hiding primary nav on desktop)

### 2. Accessibility Audit (reference accessibility-reference.md)
- Color contrast: all text >= 4.5:1? Large text >= 3:1?
- Touch targets: all interactive elements >= 44dp?
- Focus indicators: visible and not hidden by overlays?
- Labels: every form field has a visible label (not just placeholder)?
- Color independence: info conveyed by more than just color?
- Screen reader: proper alt text, roles, labels, heading hierarchy?
- Keyboard: logical tab order, no traps, escape closes overlays?
- Motion: respects prefers-reduced-motion?

### 3. Visual Hierarchy
- Squint test: is the primary element obvious?
- One primary action per screen?
- Size/weight/color hierarchy consistent?
- Whitespace creating the right groupings?

### 4. Spacing & Layout
- On the 4/8/12/16/24/32/48 scale?
- Proximity principle: related items closer than unrelated?
- Consistent padding across similar containers?
- Safe areas respected (notch, home indicator)?

### 5. Typography
- Max 3 sizes per screen?
- Weight hierarchy: semibold for headings, medium for labels, regular for body?
- Line height: 1.5 for body text?
- Line length: 50-75 characters?

### 6. Color
- Semantic usage? (every color has a meaning)
- 60-30-10 ratio?
- Passes contrast in both light and dark mode?
- Not more than 4-5 distinct colors per screen?

### 7. States Coverage
For every interactive element and data container:
- [ ] Default/populated state
- [ ] Empty state (with guidance)
- [ ] Loading state (skeleton or spinner)
- [ ] Error state (with recovery action)
- [ ] Disabled state (with explanation)
- [ ] Selected/active state
- [ ] Hover/press state (feedback)

### 8. Platform Compliance
- iOS: follows HIG? (nav bars, tab bars, gestures, safe areas)
- Android: follows M3? (FAB, bottom nav, surface elevation)
- Web: follows established conventions? (breadcrumbs, skip nav, responsive)

### 9. Interaction Quality
- Clear affordances (buttons look tappable, links look like links)?
- Proper feedback on every interaction (pressed state, loading, result)?
- No dead ends (every screen has a way forward and a way back)?
- Error recovery (can the user undo, retry, or escape)?

## Output Format

Rate each area and give the top fixes:

```
**Screen: [name]** (captured at [viewport])

| Area | Rating | Key Issue |
|------|--------|-----------|
| UI Patterns | pass/warn/fail | [one-line summary] |
| Accessibility | pass/warn/fail | [one-line summary] |
| Visual Hierarchy | pass/warn/fail | [one-line summary] |
| Spacing | pass/warn/fail | [one-line summary] |
| Typography | pass/warn/fail | [one-line summary] |
| Color | pass/warn/fail | [one-line summary] |
| States | pass/warn/fail | [one-line summary] |
| Platform | pass/warn/fail | [one-line summary] |
| Interaction | pass/warn/fail | [one-line summary] |

**Top 3 Fixes (highest impact):**

**Fix 1: [issue] — [area]**
[What's wrong + what I see + why it matters]
[code fix]

**Fix 2: [issue] — [area]**
[What's wrong + why + fix]
[code fix]

**Fix 3: [issue] — [area]**
[What's wrong + why + fix]
[code fix]

Additional issues (lower priority): [list remaining]
```

## Rules
- Rate ALL 9 areas in the summary table, but only detail the top 3 fixes.
- The designer can ask for more detail on any area.
- EVERY issue gets a code fix — no "you should consider..." without code.
- Code fixes are React Native StyleSheet / Tailwind / CSS — match what the project uses.
- Keep fix descriptions under 2 sentences each.
- Don't critique things the designer didn't ask about unless they're critical (accessibility failures are always critical).

## Output Location
Save to: `{output_root}/guild-artifacts/visual-critique-[scope].md`
