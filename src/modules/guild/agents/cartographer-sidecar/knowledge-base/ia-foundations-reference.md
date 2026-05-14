# IA Foundations Reference

**Load on:** every Cartographer task (always loaded at activation)

---

## Garrett's Five Planes

Jesse James Garrett's model from *The Elements of User Experience* describes five layers of UX, each dependent on the one below:

| Plane | Concern | Questions it answers |
|-------|---------|---------------------|
| **Strategy** | User needs + product goals | What do we want? What do users want? |
| **Scope** | Features + content requirements | What are we building? What content exists? |
| **Structure** | IA + interaction design | How is it organized? How does it behave? |
| **Skeleton** | Navigation + interface + information design | Where does it go? How is it presented? |
| **Surface** | Visual design | What does it look like? |

Cartographer operates primarily at the **Structure** plane, and informs the Skeleton. Mage operates at the Surface. Rogue operates at Structure (interaction) and Skeleton (interface). Tinker operates at Skeleton/Surface for design system elements.

**Why it matters:** IA decisions at the Structure plane constrain every plane above it. A navigation model chosen at Structure determines what skeleton patterns are even possible. Always establish structure before skeleton.

---

## Rosenfeld & Morville — Four IA Components

From *Information Architecture for the Web and Beyond* (the polar bear book):

### 1. Organization Systems
How information is categorized and structured.
- **Exact schemes:** alphabetical, chronological, geographical — unambiguous, best for known-item search
- **Ambiguous schemes:** topical, task-based, audience-based, metaphor-driven — best for browsing
- **Hierarchical:** tree structures, parent/child relationships — most common in product IA
- **Database:** faceted classification, record/field model — best for large, structured content sets
- **Hypertext:** nodes and links — best for associative, non-linear content

**Rule:** Match the organization scheme to how users think about the content, not how the organization thinks about it.

### 2. Labeling Systems
How information is named and represented.
- Labels must be consistent in scope, format, and specificity across the system
- Avoid internal jargon users don't share
- Test labels with card sorts before committing — assumed clarity is often wrong
- Navigation labels, heading labels, and index labels each follow different conventions

**Rule:** A label is a promise. Every label must deliver exactly what it promises.

### 3. Navigation Systems
How users move through the information space.
- **Global navigation:** appears everywhere, orients users within the whole
- **Local navigation:** contextual, within a section or content type
- **Contextual navigation:** inline, associative — "see also," related content
- **Supplemental navigation:** search, index, site map, breadcrumbs

**Rule:** Navigation should answer three questions at every point: Where am I? Where have I been? Where can I go?

### 4. Search Systems
How users find information directly.
- Search is a fallback when navigation fails — don't rely on it to compensate for poor IA
- Faceted search (filter by attribute) is more useful than full-text search for product content
- Zero-results and partial-results states need as much design attention as success states

---

## Abby Covert — Sense-Making Framework

From *How to Make Sense of Any Mess*:

**Core concept:** Information architecture is the practice of deciding how to arrange the parts of something to be understandable. Before you diagram anything, answer:
1. **Intent** — what do you want to accomplish?
2. **Current state** — what exists now?
3. **Gap** — what's missing or broken?
4. **Actors** — who interacts with this information?
5. **Context** — when and where does interaction happen?

**Language matters:** The words you choose to organize information carry implicit meaning. If your labels conflict with users' mental models, no amount of visual design fixes the disconnect.

**Ontology → Taxonomy → Choreography:**
- **Ontology** — what things mean (definitions)
- **Taxonomy** — how things are grouped (categories)
- **Choreography** — how things move and change (flows, states)

Cartographer works at all three levels. Rogue works primarily at choreography. Cartographer defines ontology and taxonomy before handing off to Rogue.

---

## Peter Morville — Findability & Information Ecology

**Findability:** Users must be able to locate information — either by browsing the IA or by searching. Findability fails when:
- Labels don't match users' vocabulary
- Hierarchy doesn't match users' mental models
- Content lives in more than one place without clear cross-references
- Search returns too many results with no way to narrow

**Information ecology:** IA exists in a system — users, content, context, and technology all interact. A diagram that ignores any one of these will break when deployed.

**The ambient findability question:** Could a user with no prior knowledge of this system find what they need? If not, the IA is incomplete regardless of how logical it seems to the team.
