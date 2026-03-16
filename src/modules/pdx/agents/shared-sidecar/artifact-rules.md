# PDX Artifact Rules

## Source of Truth Pattern
PDX artifacts are always the canonical source. Other documents reference them.

### How it works:
1. PDX agent generates full artifact → saves to _bmad-output/pdx-artifacts/
2. If a BMAD document needs that content → write a summary + reference link
3. If the artifact is updated → the reference still works, no need to update the BMAD doc
4. Developers follow references from stories → PDX artifacts for full design context

### What goes in PDX artifacts (full detail):
- Complete persona cards with all demographics, behaviors, scenarios
- Full journey maps with emotional arcs, all phases, backstage actions
- Complete user flows with all error states and edge cases
- Full component specs with all props, states, ARIA, responsive behavior
- All design tokens with descriptions and usage guidelines

### What goes in BMAD documents (summary + reference):
- Persona overview table (name, archetype, primary goal)
- Top 3 journey pain points and critical moments of truth
- Mermaid flow diagrams (compact enough to inline)
- Component props table (developers need this directly)
- Token names and values (developers need this directly)
- Final copy strings (developers need this directly)
- Everything else: "See full details: _bmad-output/pdx-artifacts/[file].md"

### Why this matters:
- Single source of truth — update one place, references stay valid
- PRDs don't bloat with 200 lines of journey map detail
- Stories link to full specs instead of trying to contain them
- Design artifacts maintain their PDX template structure (quality gates, confidence ratings, etc.)
- PM reads the summary, designer reads the full artifact, developer follows the reference
