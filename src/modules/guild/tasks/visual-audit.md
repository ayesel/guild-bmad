# Visual Audit

## Purpose
Conduct a visual UI audit of competing or comparable products by navigating to live applications,
capturing screenshots and accessibility snapshots, and analyzing visual patterns, layout structures,
information hierarchy, navigation models, and interaction paradigms. Produces a design reference
document that grounds visual design decisions in evidence from real products.

This is Ranger's "camera" — the same rigorous research methodology applied to what products
actually look like, not just what they claim to do.

## Pre-flight Checks

### 0. Load BMAD Project State (BEFORE all other checks)
- Read `{output_root}/implementation-artifacts/sprint-status.yaml` if it exists
  - Note current sprint number and existing state
  - Brownfield vs Greenfield determination applies
- This context informs which products to audit and what design decisions are pending

### Artifact Source of Truth Rule
Guild artifacts in {output_root}/guild-artifacts/ are ALWAYS the source of truth.
- Write the FULL artifact to {output_root}/guild-artifacts/ using the visual-audit template
- Write a SUMMARY in any BMAD document that references it
- REFERENCE the full artifact from summaries
- NEVER duplicate the full content inside a BMAD document

### 1. Check Existing Research
- Scan {output_root}/guild-artifacts/ for existing competitive-audit-*.md or visual-audit-*.md
- If a text-based competitive audit exists, use it to inform which products to visually audit
- If a visual audit already exists for the same scope, ask whether to update or extend

### 2. Detect Browser Environment
Determine which browser tool is available, in this priority order:

**Priority 1 — Atrium Browser (preferred)**
Check if `$ATRIUM_CLI_PATH` and `$ATRIUM_PANE_ID` are set.
If yes, use atrium browser commands:
```bash
# Find or create a browser pane
"$ATRIUM_CLI_PATH" pane list --json  # look for type: browser
# Or create one
"$ATRIUM_CLI_PATH" pane create --type browser --url "https://example.com" --split "$ATRIUM_PANE_ID"

# Navigate
"$ATRIUM_CLI_PATH" browser navigate <pane-id> "<url>"

# Capture accessibility tree (structured element data)
"$ATRIUM_CLI_PATH" browser snapshot <pane-id>

# Capture visual screenshot
"$ATRIUM_CLI_PATH" browser screenshot <pane-id>

# Scroll to see below-the-fold content
"$ATRIUM_CLI_PATH" browser scroll <pane-id> --direction down --amount 500

# Read element attributes
"$ATRIUM_CLI_PATH" browser eval <pane-id> "document.title"
```

**Priority 2 — Playwright MCP**
Check if Playwright MCP tools are available (mcp__playwright__*).
If yes, use Playwright navigation and screenshot tools.

**Priority 3 — WebFetch (last resort ONLY)**
Use WebFetch to fetch pages and analyze HTML structure.
Note: this cannot capture visual layout, only content and semantic structure.
Flag in the audit that visual analysis was limited to content-only.

**CRITICAL: You MUST use a real browser (Atrium or Playwright). Do NOT describe websites from memory or training data. Navigate to the actual URL, take actual screenshots, and analyze what you actually see on screen. Screenshots are the evidence. If you cannot take screenshots, you cannot do a visual audit — report this limitation immediately and ask the user to provide an environment with browser access.**

## Execution

### 1. Gather Audit Parameters from User

**Required:**
- What product category or feature area are we auditing?
- List of products/URLs to analyze (minimum 3, recommended 5-7)
- What specific UI patterns are we looking for? (dashboards, data tables, forms, navigation, etc.)

**Optional:**
- Specific screens or flows to capture (e.g., "the main dashboard", "the settings page")
- Device/viewport to audit (default: 1440px desktop)
- Any products the user already knows and wants to validate against

### 2. For Each Product

Execute this capture sequence:

#### a. Navigate & Orient
- Navigate to the product URL
- Capture the landing/login page
- Note: if the product is gated (login required), document what's visible without auth and note the limitation

#### b. Capture Key Screens
For each key screen (homepage, dashboard, list view, detail view, settings):
1. **Screenshot** — full viewport capture
2. **Snapshot** — accessibility tree showing element hierarchy, roles, labels
3. **Scroll capture** — scroll down and capture below-the-fold content
4. **Note observations** using the analysis framework below

#### c. Analysis Framework
For each captured screen, document:

**Layout & Structure:**
- Grid system (columns, gutters, max-width)
- Content regions (sidebar, main, panel splits)
- Information density (sparse, moderate, dense)
- White space usage

**Visual Hierarchy:**
- What does the eye see first?
- Heading levels and typography scale
- Use of color for emphasis or categorization
- Icon usage and meaning

**Navigation Model:**
- Primary nav pattern (sidebar, top bar, tabs, breadcrumbs)
- Secondary nav (filters, search, pagination)
- Wayfinding cues (active states, breadcrumbs, page titles)

**Data Presentation:**
- How is data displayed? (tables, cards, charts, maps, lists)
- Filtering and sorting patterns
- Empty states and loading states
- Data density vs. scannability tradeoff

**Interaction Patterns:**
- Primary actions (buttons, CTAs — placement, hierarchy)
- Inline editing vs. modal/drawer patterns
- Bulk actions and multi-select
- Feedback patterns (toasts, inline messages, status badges)

**Responsive Signals:**
- If viewport is resized, how does layout adapt?
- Mobile-first or desktop-first signals

### 3. Cross-Product Synthesis

After analyzing all products, synthesize:

**Pattern Frequency Matrix:**
| Pattern | Product A | Product B | Product C | Product D | Consensus? |
|---------|-----------|-----------|-----------|-----------|------------|
| Sidebar nav | ✅ | ✅ | ❌ | ✅ | Yes — 3/4 |
| Card-based list | ❌ | ✅ | ✅ | ✅ | Yes — 3/4 |
| ... | | | | | |

**Best-in-Class Examples:**
For each UI pattern area, identify which product does it best and why.

**Anti-Patterns Found:**
What did products do poorly? What should we avoid?

**Design Recommendations:**
Based on the visual evidence, what patterns should we adopt, adapt, or avoid?

## Output Format

Use the visual-audit-template.yaml structure. Save to:
`{output_root}/guild-artifacts/visual-audit-{scope-name}.md`

Include screenshots as references (file paths or descriptions of what was captured).
When using Atrium browser, screenshots are saved automatically and can be referenced by path.

## Quality Checks Before Delivery
- [ ] Minimum 3 products analyzed
- [ ] Each product has at least 2 screens captured
- [ ] Analysis framework applied consistently across all products
- [ ] Pattern frequency matrix completed
- [ ] Best-in-class examples identified with reasoning
- [ ] Anti-patterns documented
- [ ] Design recommendations are specific and actionable
- [ ] Browser tool limitations are documented (e.g., couldn't access gated product)
- [ ] Accessibility observations included (heading structure, ARIA, contrast)
- [ ] Confidence level stated with rationale

## Post-Execution
After delivering the visual audit artifact:
1. Summarize the top 3 UI patterns the team should adopt
2. Call out the most surprising finding (something that challenges assumptions)
3. Identify which competitor is the visual benchmark and why
4. Suggest the logical next design activity (typically Rogue wireframes informed by these patterns)
