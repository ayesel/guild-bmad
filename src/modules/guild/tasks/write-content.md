# Write Content

## Purpose
Create structured UX content using the specified template. This task is the core
content engine for the PDX Content Strategist agent.

## Pre-flight Checks

Before writing any content, perform these checks in order:

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
PDX artifacts in _bmad-output/guild-artifacts/ are ALWAYS the source of truth.
When BMAD documents (PRD, architecture, UX_Design.md) need design content:
- Write the FULL artifact to _bmad-output/guild-artifacts/ using PDX templates
- Write a SUMMARY in the BMAD document with key findings inline
- REFERENCE the full artifact: "See full details: _bmad-output/guild-artifacts/[filename].md"
- NEVER duplicate the full PDX artifact content inside a BMAD document
- The summary should be enough for a PM to understand; the full artifact is for designers and developers

### 1. Load Project Context
- Read `_bmad-output/planning-artifacts/project-context.md` if it exists
- Read `_bmad-output/planning-artifacts/prd.md` if it exists
- Read `_bmad-output/guild-artifacts/personas.md` if it exists
- Read any voice and tone guidelines in `_bmad-output/guild-artifacts/`
- Read any existing wireframes or flows from Kai in `_bmad-output/guild-artifacts/`
- Read any existing research from Nova in `_bmad-output/guild-artifacts/`

### 2. Gather Content Parameters from User
Ask the user for the following (skip any already provided):

**Required:**
- What screen, component, or feature needs content?
- What is the user's emotional state at this point in the flow?
- What action do we want the user to take?

**Contextual (ask if relevant to content type):**
- What voice and tone guidelines exist?
- What is the product's personality?
- Who is the target audience? (reference personas if available)
- Are there character or space constraints?
- What language/locale considerations exist?

### 3. Confirm Context
Before writing, restate the context back to the user:
- "Here's the context: I'll write [content type] for [screen/feature],
  targeting [persona/audience] who is feeling [emotional state].
  The goal is to get them to [desired action]. I'll provide [n] options
  with reasoning. Sound right?"

## Execution

### Output Format
All content deliverables must include:

1. **Header Block** — Title, content type, version, date, status
2. **Context Summary** — User state, emotional context, desired action
3. **Copy Options** — 2-3 options per element with reasoning
4. **Recommended Choice** — With detailed rationale
5. **Character Counts** — Per element
6. **Reading Level** — Flesch-Kincaid grade level assessment
7. **Screen Reader Transcript** — How the copy reads linearly for assistive tech
8. **Translation Notes** — Idioms, cultural references, or expansion concerns
9. **Next Steps** — What content needs attention next

### Content State
Set the frontmatter status field:
```yaml
---
artifact: [content type]
status: draft
version: 1.0
created: [date]
author: Echo (Content Strategist)
reading_level: "[grade level]"
voice_tone: "[voice attributes applied]"
references:
  - [list any referenced wireframes, personas, voice guidelines, or prior content]
---
```

### Quality Checks Before Delivery
- [ ] 2-3 options presented for each element
- [ ] Reasoning provided for recommended choice
- [ ] Reading level assessed (target: grade 6-8 consumer, 8-10 enterprise)
- [ ] No jargon or technical terms in user-facing copy
- [ ] Inclusive language check passed
- [ ] Screen reader experience considered
- [ ] Character counts within constraints
- [ ] Consistent with voice and tone guidelines (if they exist)
- [ ] All UI states have copy (empty, error, success, loading)

## Output Location
Save to: `_bmad-output/guild-artifacts/content-[type]-[scope].md`

## Post-Execution
After delivering the content:
1. Highlight the most critical copy decision and its reasoning
2. Flag any copy that needs user testing to validate
3. Note any translation or localization concerns
4. Suggest the logical next content activity
