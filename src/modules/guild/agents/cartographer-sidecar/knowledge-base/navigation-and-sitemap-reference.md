# Navigation and Sitemap Reference

**Load on:** IA (Information Architecture), SM (Sitemap), NAV (Navigation Audit), CS (Card Sort), TT (Tree Test) tasks

---

## Navigation models

### Hierarchical (tree)
Most common. Single root → categories → subcategories → content. Works when content has clear, non-overlapping categories and users know what category their target belongs to.

**Strengths:** Predictable, learnable, works well with breadcrumbs
**Weaknesses:** Items that fit multiple categories are hard to place; deep hierarchies require many clicks; fails when users don't share the team's category model

**Rule:** Maximum 3–4 levels deep before findability degrades. If depth exceeds 4, flatten or restructure.

### Flat (matrix)
All content accessible from a single level. Works for small content sets (<20 items) or highly homogeneous content (e.g., a media gallery).

**Strengths:** No hierarchy to learn; browse-friendly
**Weaknesses:** Doesn't scale; no wayfinding context

### Hub and spoke
Central hub with direct access to independent sections. Each section is its own space with limited cross-linking. Common for dashboards and tool suites.

**Strengths:** Sections can evolve independently; clear home base
**Weaknesses:** Moving between sections requires returning to hub; sections feel siloed

### Faceted
Content filtered by multiple independent attributes (e.g., e-commerce filters: color × size × price). Not a traditional navigation model — works alongside hierarchical nav for large, structured content sets.

**Use when:** Users approach content from multiple equally valid angles

---

## Sitemap conventions

### Standard notation
- **Rectangles** for pages/screens
- **Lines** for navigation relationships (parent-to-child = direct nav; dotted = secondary/utility nav)
- **Diamonds** or **hexagons** for decision points (authenticated vs. unauthenticated, conditional access)
- **Cylinders** for data sources (when data drives content)
- **Numbered IDs** on each node (1.0, 1.1, 1.2, 2.0...) for reference in other artifacts

### Depth and breadth tradeoffs
| Structure | Trade-off |
|-----------|-----------|
| Broad and shallow (many items per level, few levels) | Easy to scan, hard to find in large sets |
| Narrow and deep (few items per level, many levels) | Easy to filter down, requires more clicks |
| Balanced (7±2 items per level, 3–4 levels max) | Standard starting point; adjust based on content volume and user mental models |

### What to include
- All primary navigation destinations
- Secondary/utility navigation (account, settings, help)
- Auth states (public vs. authenticated views)
- Key modal/overlay destinations if they are meaningful waypoints

### What to exclude from sitemaps
- Individual data records (don't map every article — map "Article detail" as a template node)
- Transient states (loading, error) — those belong in Rogue's state diagrams
- Third-party destinations (link out from the sitemap, don't diagram inside it)

---

## Navigation audit

Audit existing navigation against these criteria:

| Criterion | Pass condition |
|-----------|---------------|
| **Clarity** | Every navigation label unambiguously communicates its destination |
| **Completeness** | Every primary destination is reachable from global nav |
| **Consistency** | Same labels used for same destinations across all surfaces |
| **Depth** | No more than 3–4 levels to any content |
| **Wayfinding** | User can always determine: where am I / where have I been / where can I go |
| **Scent** | Labels provide sufficient information scent — user can predict what they'll find |
| **Mental model alignment** | Category structure matches how users think about the content (validate with card sort) |

---

## Card sorting

Card sorting reveals users' mental models for categorizing content — what groups make sense to them.

### Open card sort
Users create their own groups and label them. Use to discover: what categories users naturally form, what vocabulary they use.

**When to use:** Early in IA design when the category structure is unknown

### Closed card sort
Users sort cards into pre-defined categories. Use to validate: whether an existing or proposed category structure works.

**When to use:** After initial IA is designed, before committing to it

### Card sort planning checklist
- [ ] 30–40 cards is the practical maximum before participant fatigue
- [ ] Cards should be content items, not features or tasks
- [ ] Card labels should be user-facing labels, not internal names
- [ ] Include a "doesn't fit anywhere" pile option
- [ ] Minimum 15–20 participants for quantitative analysis; 5–8 for qualitative insights
- [ ] Use Optimal Workshop (OptimalSort) for remote, quantitative card sorts

### Analysis
- **Similarity matrix:** how often each pair of cards was sorted together
- **Dendrogram:** hierarchical cluster diagram showing which cards naturally group
- **Categories by frequency:** which proposed categories attracted the most cards
- **Agreement score:** how consistently participants sorted the same cards together (>70% = high agreement)

---

## Tree testing

Tree testing validates an existing navigation structure by asking users to find specific items without visual design cues — only the text hierarchy.

### Why tree testing
Tree testing isolates navigation structure from visual design. A user who succeeds in tree testing is finding items based on labels and structure alone, not on recognizing UI patterns. Failures reveal structural or labeling problems, not visual problems.

### Task design
- Write 10–15 task scenarios: "Where would you go to do X?"
- Tasks should reflect real user goals, not site structure
- Include tasks for items at different hierarchy depths
- Include 2–3 tasks that have no correct destination (tests whether users recognize when something isn't there)

### Success metrics
- **Directness:** did the user navigate directly to the target, or explore multiple paths?
- **Success rate:** what percentage of users found the correct destination?
- **Time on task:** how long to find the item?
- **First-click accuracy:** was the first click in the correct branch? (High correlation with overall success)

**Thresholds:** Success rates below 70% on any task indicate a structural or labeling problem worth investigating. First-click accuracy below 60% indicates the top-level category label is wrong or misleading.

### Tools
Optimal Workshop (Treejack) for remote tree tests. Export results as similarity matrix and success-rate table for analysis.
