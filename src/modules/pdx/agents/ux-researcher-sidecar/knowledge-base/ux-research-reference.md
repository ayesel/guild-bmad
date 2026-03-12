# UX Research Knowledge Base

## Research Method Selection Guide

| Research Question Type | Best Methods | When to Use |
|------------------------|-------------|-------------|
| "What are users doing?" | Analytics, heatmaps, session recordings | You have a live product with traffic |
| "Why are users doing it?" | User interviews, contextual inquiry | You need motivations and mental models |
| "How well does it work?" | Usability testing, heuristic evaluation | You have a prototype or live product |
| "What should we build?" | JTBD interviews, diary studies, surveys | Early discovery, feature prioritization |
| "Who are our users?" | Interviews, surveys, analytics segmentation | Persona creation, audience definition |
| "How do users feel?" | Journey mapping, diary studies, interviews | Experience optimization, pain point ID |
| "What do competitors do?" | Competitive audit, feature benchmarking | Market positioning, feature gaps |
| "Is it accessible?" | WCAG audit, assistive tech testing | Compliance, inclusive design |
| "Does it meet standards?" | Heuristic evaluation, expert review | Quick quality assessment |
| "What's the impact?" | A/B testing, analytics, surveys (SUS, NPS) | Measuring design changes |

## Nielsen's Severity Rating Scale

| Rating | Label | Description |
|--------|-------|-------------|
| 0 | Not a problem | No usability issue identified |
| 1 | Cosmetic | Cosmetic issue only — fix if time allows |
| 2 | Minor | Minor usability problem — low priority fix |
| 3 | Major | Major usability problem — important to fix, high priority |
| 4 | Catastrophic | Usability catastrophe — must fix before release |

## System Usability Scale (SUS) Interpretation

| Score Range | Grade | Adjective | Percentile |
|------------|-------|-----------|------------|
| 84.1-100 | A+ | Best Imaginable | 96-100 |
| 80.8-84.0 | A | Excellent | 90-95 |
| 71.4-80.7 | B | Good | 70-89 |
| 50.9-71.3 | C | OK | 16-69 |
| 35.7-50.8 | D | Poor | 5-15 |
| 0-35.6 | F | Worst Imaginable | 0-4 |

**SUS Benchmark**: Industry average is 68. Scores above 68 are above average.

**SUS Calculation**: 10 questions, alternating positive/negative. For odd items subtract 1 from score. For even items subtract score from 5. Sum all values and multiply by 2.5. Result is 0-100.

## Interview Question Principles (TEDW)

Use open-ended stems that invite storytelling:

- **Tell** me about a time when...
- **Explain** how you currently...
- **Describe** what happens when...
- **Walk me through** your process for...

### Follow-up Probes
- "Can you tell me more about that?"
- "What happened next?"
- "How did that make you feel?"
- "What were you expecting to happen?"
- "Why do you think that is?"
- "Can you show me what you mean?"

### Questions to Never Ask
| Bad Question | Why It's Bad | Better Alternative |
|-------------|-------------|-------------------|
| "Do you like this feature?" | Leading, binary, hypothetical | "Tell me about the last time you used this" |
| "Would you use this?" | Hypothetical — people can't predict behavior | "How do you currently solve this problem?" |
| "Is this easy to use?" | Leading, subjective | "Walk me through how you'd complete [task]" |
| "What features do you want?" | Users design solutions, not articulate needs | "What's the hardest part of [task] today?" |
| "On a scale of 1-10..." | Arbitrary, no actionable insight | "Describe your experience with [specific moment]" |
| "Don't you think...?" | Leading, biased | "What are your thoughts on...?" |

## Bias Checklist

Acknowledge and mitigate these biases in every research activity:

1. **Confirmation bias** — Seeking evidence that confirms existing beliefs. *Mitigation*: Actively look for disconfirming evidence. Have someone else review your analysis.
2. **Survivorship bias** — Only studying users who completed the flow, ignoring those who dropped off. *Mitigation*: Include dropout analysis. Recruit non-users and churned users.
3. **Anchoring bias** — Over-relying on the first piece of information encountered. *Mitigation*: Randomize order of data review. Use multiple independent coders.
4. **Social desirability bias** — Participants saying what they think you want to hear. *Mitigation*: Ask about past behavior, not hypothetical. Observe actions, not just words.
5. **Recency bias** — Giving more weight to recent events or data. *Mitigation*: Review historical data. Weight findings by sample size, not date.
6. **Selection bias** — Recruiting participants who don't represent the full user base. *Mitigation*: Define screening criteria. Include edge-case users and accessibility needs.
7. **Observer effect** — Participant behavior changes because they know they're being observed. *Mitigation*: Use unmoderated testing when possible. Allow warm-up tasks.

## WCAG 2.2 Quick Reference

### Level A (Minimum)
- All non-text content has text alternatives
- Captions for prerecorded audio/video
- Content is adaptable (meaningful sequence, sensory characteristics)
- Content is distinguishable (use of color not sole indicator)
- All functionality available via keyboard
- No keyboard traps
- Timing adjustable for time-limited content
- No content that flashes more than 3 times per second
- Skip navigation mechanism
- Pages have descriptive titles
- Logical focus order
- Link purpose determinable from text
- Multiple ways to find pages
- Labels or instructions for user input
- Error identification in text (not just color)

### Level AA (Recommended Standard)
- Captions for live audio
- Audio description for prerecorded video
- Contrast ratio minimum 4.5:1 (normal text), 3:1 (large text)
- Text resizable to 200% without loss
- Images of text avoided (use actual text)
- Consistent navigation across pages
- Consistent identification of components
- Error suggestion provided when detected
- Error prevention for legal/financial/data submissions
- Reflow at 320px width without horizontal scroll
- Non-text contrast minimum 3:1
- Text spacing adjustable without loss
- Content on hover/focus dismissible, hoverable, persistent
- Dragging alternatives available
- Target size minimum 24x24px
- Consistent help location
- Redundant entry avoided
- Accessible authentication (no cognitive function test)

### Level AAA (Enhanced)
- Sign language for prerecorded audio
- Extended audio description
- Contrast ratio minimum 7:1 (normal text), 4.5:1 (large text)
- No background audio or can be turned off
- Visual presentation customizable (line spacing, width, alignment)
- No timing on content
- No interruptions (can be postponed)
- Re-authentication without data loss
- Link purpose determinable from text alone
- Section headings organize content
- Pronunciation provided for ambiguous words
- Target size minimum 44x44px

## Maze REFINE Framework

A framework for structuring continuous research:

| Stage | Focus | Key Activities |
|-------|-------|---------------|
| **R**ecognize | Identify the problem space | Stakeholder interviews, analytics review, support ticket analysis |
| **E**xplore | Understand user context | User interviews, contextual inquiry, diary studies |
| **F**rame | Define the opportunity | JTBD mapping, persona creation, problem statements |
| **I**deate | Generate solutions | Design sprints, concept testing, card sorting |
| **N**urture | Refine and validate | Usability testing, A/B testing, prototype iteration |
| **E**valuate | Measure impact | Analytics tracking, SUS scores, task success rates |

## NNG Promptframes

Structured prompt patterns for generating research artifacts with AI:

- **Context frame**: "Given [user type] trying to [task] in [environment]..."
- **Evidence frame**: "Based on [data source], we observed [finding]..."
- **Insight frame**: "This suggests [interpretation] because [reasoning]..."
- **Action frame**: "We recommend [action] to address [problem] for [users]..."

## Research Repository File Structure

Recommended organization for research outputs:

```
_bmad-output/pdx-artifacts/
├── personas.md                    # Consolidated persona document
├── research-synthesis.md          # Cross-study synthesis
├── journey-map-[feature].md       # Journey maps by feature
├── heuristic-eval-[target].md     # Heuristic evaluations
├── competitive-audit-[scope].md   # Competitive analyses
├── usability-test-[feature].md    # Test plans and results
├── accessibility-audit-[scope].md # WCAG audits
├── interview-script-[study].md    # Interview guides
├── jtbd-[domain].md               # Jobs-to-be-Done maps
└── components/                    # Exported React prototypes
```
