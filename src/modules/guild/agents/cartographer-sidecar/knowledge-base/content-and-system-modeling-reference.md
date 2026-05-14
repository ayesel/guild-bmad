# Content and System Modeling Reference

**Load on:** CM (Content Model), SYS (System Map), ADR (ADR Diagram), CON (Conceptual Model) tasks

---

## Content modeling

Content modeling defines what types of content exist in a system, what attributes each type has, and how types relate to each other.

### Why before what
Before modeling content, answer:
- What decisions will this model support? (developer implementation, editorial workflow, migration planning, IA restructuring?)
- Who owns each content type? (author? system? user?)
- What is the lifecycle of each type? (created once? updated frequently? user-generated?)

### Content type anatomy
Each content type has:
- **Name** — singular noun, not a page name ("Article," not "Articles Page")
- **Purpose** — one sentence on what job this content type does
- **Attributes** — fields: name, type (string/text/date/boolean/reference/media), required/optional, constraints
- **Relationships** — how it relates to other types (has-many, belongs-to, many-to-many)
- **Owner** — who creates/manages this content
- **Lifecycle** — how it is created, updated, and retired

### Visualization conventions
- **Rectangles** for content types
- **Lines with crow's-foot notation** for relationships (standard ERD notation)
- OR: **Card layout** (each type as a card listing attributes) with connector lines for relationships — more readable for non-engineers
- Color-code by domain (e.g., "User content" = blue, "Product content" = green, "System content" = grey)

### Common mistakes
- Modeling pages instead of content types — pages are containers, not types
- Conflating content model with navigation model — these are separate concerns
- Omitting relationship cardinality — "Article has Tags" is incomplete; "Article has zero-to-many Tags; Tag belongs-to zero-to-many Articles" is complete
- Over-engineering — if the model has more than 12 content types, verify each is genuinely distinct

---

## System mapping for stakeholders

System maps explain how components of a system relate to each other for an audience that doesn't need (or want) technical detail. They answer: "what exists and how does it connect?"

### Levels of abstraction
Choose the right level for the audience:
- **C-suite:** products, data flows, user groups — 5–10 nodes maximum
- **Product team:** services, features, integrations, user touchpoints — 10–25 nodes
- **Engineering:** services, APIs, databases, infrastructure — detailed technical diagram (not Cartographer's output — that's architecture diagrams for the Architect agent)

### System map structure
1. **User/actor layer** (top or left): who interacts with the system
2. **Interface layer**: what they interact through (products, surfaces, channels)
3. **Service/logic layer**: what processes their interactions
4. **Data/integration layer** (bottom or right): where data lives and what it connects to

### Conventions
- Swim lanes or color zones to separate layers
- Flows show direction of data or user action
- Third-party integrations clearly distinguished from owned components (dashed border, different color, or explicit "3P" label)
- State scope at the top: "Current state as of [date]" or "Future state — target [date]"

---

## Hierarchy and relationship encoding in diagrams

When a diagram must show both hierarchy and lateral relationships simultaneously:

**Hierarchy encoding:**
- Vertical position (parent above child) is most intuitive for hierarchy
- Size differential (parent larger) reinforces hierarchy
- Indentation in list-style diagrams
- Enclosure (parent zone contains child nodes)

**Lateral relationship encoding:**
- Connectors (lines) for relationships between peers
- Labels on connectors to name the relationship
- Color-coded connectors if multiple relationship types exist

**When hierarchy and lateral relationships conflict:**
- This usually signals that the IA itself needs work — content that belongs to two parents should either be duplicated (with canonical source marked), moved to a shared parent, or redesigned as a cross-referenced item

**The separation principle:** If a diagram is trying to show hierarchy AND lateral relationships simultaneously AND flow/sequence, split it into three diagrams. No single diagram should carry more than two of these three concerns without becoming unreadable.
