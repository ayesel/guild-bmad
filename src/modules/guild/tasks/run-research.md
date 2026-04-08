# Run Research

## Purpose
Execute a structured UX research activity using the specified template. This task is the core
research engine for the PDX UX Researcher agent.

## Pre-flight Checks

Before executing any research activity, perform these checks in order:

### 0. Check for Existing Research Artifacts (BEFORE anything else)

Scan _bmad-output/guild-artifacts/ for any files matching the research type being requested:
- personas*.md
- journey-map*.md
- competitive-audit*.md
- heuristic-eval*.md
- research-synthesis*.md
- jtbd*.md
- interview-script*.md
- usability-test*.md
- accessibility-audit*.md

For each match found:
1. Read the file
2. Check when it was created (from frontmatter date)
3. Check what scope it covers (from frontmatter or content)
4. Decide: skip, update, or create new

If skipping, tell the user:
"[Artifact type] already exists at [path], created [date], covering [scope].
I'll reference this instead of recreating it. Want me to update/extend it instead?"

If the PM created PDX-format artifacts during PRD creation, those count as valid
PDX artifacts. Don't recreate work the PM already did.

### 0b. Load BMAD Project State
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
- Read `_bmad-output/guild-artifacts/research-synthesis.md` if it exists
- Read any prior research artifacts in `_bmad-output/guild-artifacts/` that are relevant

### 2. Gather Research Parameters from User
Ask the user for the following (skip any already provided):

**Required:**
- What is the research question or objective?
- What is the scope? (feature, product area, full product)
- Who are the target users? (reference personas if they exist)

**Contextual (ask if relevant to research type):**
- What existing data or prior research is available?
- What decisions will this research inform?
- What are the known constraints (time, budget, access to users)?
- Are there specific hypotheses to validate or invalidate?

### 3. Confirm Approach
Before executing, restate the approach back to the user:
- "Here's what I'll do: [research type] focused on [question/objective],
  targeting [users/scope]. I'll evaluate against [criteria/framework].
  The output will include [key deliverables]. Sound right?"

## Execution

### Output Format
All research deliverables must include:

1. **Header Block** — Title, research type, version, date, status, confidence level
2. **Executive Summary** — Key findings in 3-5 bullet points for stakeholders
3. **Methodology** — How the research was conducted, limitations, sample
4. **Findings** — What the data says (objective observations)
5. **Insights** — What the findings mean (interpretive analysis)
6. **Recommendations** — What to do about it (actionable next steps)
7. **Open Questions** — What we still don't know
8. **Next Steps** — What research or design activity should follow

### Research State
Set the frontmatter status and confidence fields:
```yaml
---
artifact: [research type]
status: draft
version: 1.0
created: [date]
author: Nova (UX Researcher)
confidence: [high|medium|low]
confidence_rationale: "[explain basis for confidence rating]"
references:
  - [list any referenced personas, PRDs, prior research, or data sources]
---
```

### Confidence Rating
- **High**: Based on direct user data, validated with multiple sources, large sample
- **Medium**: Based on heuristic analysis, expert review, limited user data, or analogous evidence
- **Low**: Based on assumptions, secondary sources, small sample, or extrapolation

### Quality Checks Before Delivery
- [ ] Research question is explicitly stated
- [ ] Methodology and limitations are documented
- [ ] Evidence is cited for every finding
- [ ] Findings are distinct from insights (what vs. what it means)
- [ ] Insights are distinct from recommendations (meaning vs. action)
- [ ] Recommendations are specific and actionable (not vague)
- [ ] Confidence level is stated with rationale
- [ ] Accessibility considerations are included where relevant
- [ ] Biases are acknowledged (confirmation, survivorship, anchoring, etc.)

## Output Location
Save to: `_bmad-output/guild-artifacts/[research-type]-[topic-name].md`

## Post-Execution
After delivering the research artifact:
1. Summarize the top 3 findings and their implications
2. Call out the most surprising or counterintuitive insight
3. State confidence level and what would increase it
4. Suggest the logical next research or design activity
