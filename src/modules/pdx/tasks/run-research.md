# Run Research

## Purpose
Execute a structured UX research activity using the specified template. This task is the core
research engine for the PDX UX Researcher agent.

## Pre-flight Checks

Before executing any research activity, perform these checks in order:

### 1. Load Project Context
- Read `_bmad-output/planning-artifacts/project-context.md` if it exists
- Read `_bmad-output/planning-artifacts/prd.md` if it exists
- Read `_bmad-output/pdx-artifacts/personas.md` if it exists
- Read `_bmad-output/pdx-artifacts/research-synthesis.md` if it exists
- Read any prior research artifacts in `_bmad-output/pdx-artifacts/` that are relevant

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
Save to: `_bmad-output/pdx-artifacts/[research-type]-[topic-name].md`

## Post-Execution
After delivering the research artifact:
1. Summarize the top 3 findings and their implications
2. Call out the most surprising or counterintuitive insight
3. State confidence level and what would increase it
4. Suggest the logical next research or design activity
