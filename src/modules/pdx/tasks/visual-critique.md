# Visual Critique

## Purpose
Provide a focused visual critique of a screen. Identify the top 3 visual issues
and provide specific fixes for each.

## Pre-flight Checks

### 0. Load BMAD Project State (BEFORE all other checks)
- Read `_bmad-output/implementation-artifacts/sprint-status.yaml` if it exists
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
PDX artifacts in _bmad-output/pdx-artifacts/ are ALWAYS the source of truth.
When BMAD documents (PRD, architecture, UX_Design.md) need design content:
- Write the FULL artifact to _bmad-output/pdx-artifacts/ using PDX templates
- Write a SUMMARY in the BMAD document with key findings inline
- REFERENCE the full artifact: "See full details: _bmad-output/pdx-artifacts/[filename].md"
- NEVER duplicate the full PDX artifact content inside a BMAD document
- The summary should be enough for a PM to understand; the full artifact is for designers and developers

### 1. Load Project Context
- Read `_bmad-output/pdx-artifacts/design-tokens.json` if it exists
- Read any existing voice/tone or style guidelines in `_bmad-output/pdx-artifacts/`

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

## Critique Framework

Evaluate in this order (stop at 3 issues — don't overwhelm):

### 1. Visual Hierarchy
- What does the eye see first? Is that the right thing?
- Are elements competing for attention at the same level?
- Is there a clear primary → secondary → tertiary reading order?

### 2. Spacing & Rhythm
- Is the spacing consistent (on the 4/8/12/16/24/32/48 scale)?
- Is there enough breathing room between groups?
- Do related elements feel grouped? Do unrelated elements feel separated?

### 3. Visual Noise
- Are there elements that can be removed without losing information?
- Are there redundant visual indicators (color + icon + text all saying the same thing)?
- Is chrome (borders, backgrounds, dividers) competing with content?

### 4. Typography
- Are there too many font sizes on screen? (max 3: primary, secondary, tertiary)
- Is the weight hierarchy clear? (one bold level, one regular, one light/muted)
- Is line height comfortable for reading?

### 5. Color
- Is color earning its place? (every color should communicate something)
- Are there too many colors competing? (max 2-3 semantic colors per screen)
- Is contrast sufficient for readability?

## Output Format

Keep it SHORT. This is a pairing session, not a report.

```
**Screen: [name]**

Your goal: [restate what they told you]

**Fix 1 (highest impact): [issue name]**
[1-2 sentence description of what's wrong and why]
[code fix]

**Fix 2: [issue name]**
[1-2 sentence description]
[code fix]

**Fix 3: [issue name]**
[1-2 sentence description]
[code fix]

Want me to apply any of these? Or show a before/after?
```

## Rules
- MAX 3 issues per critique. The designer can ask for more.
- EVERY issue gets a code fix — no "you should consider..." without code.
- Code fixes are React Native StyleSheet / Tailwind / CSS — match what the project uses.
- Keep descriptions under 2 sentences each.
- Don't critique things the designer didn't ask about unless they're critical.

## Output Location
Save to: `_bmad-output/pdx-artifacts/visual-critique-[scope].md`
