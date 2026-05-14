# Diagrammatic Communication Reference

**Load on:** WB (Whiteboard), SYS (System Map), ADR (ADR Diagram), CON (Conceptual Model) tasks

---

## Dan Brown — Communicating Design

From *Communicating Design: Developing Web Site Documentation for Design and Planning*:

**Core principle:** Design artifacts are communication tools, not records. A diagram that only the person who made it can read has failed its purpose, regardless of how technically accurate it is.

**The audience test:** Before producing any diagram, answer:
- Who will read this?
- What decision does it support?
- What do they already know?
- What do they need to know that they don't?

The answers determine every structural choice — scope, granularity, labels, level of detail.

**Four qualities of effective design documentation:**
1. **Appropriate:** matches the needs and knowledge of the audience
2. **Complete:** contains everything needed to support the decision without extraneous material
3. **Accurate:** reflects reality, not aspiration
4. **Consistent:** uses the same conventions throughout so the reader builds fluency

---

## Designer-made vs. engineer-made diagrams

This distinction matters because the failure mode (engineer-made output on a design task) is one of the most common problems in cross-functional teams.

### Engineer-made characteristics:
- Every element the same visual weight — no hierarchy
- Labels are technical identifiers, not communication (e.g., "UserService → AuthMiddleware → TokenStore" without explaining what any of those do for the user)
- Completeness over comprehension — every node and edge is present, regardless of whether they help the audience understand
- Reading order is implicit — the reader must work to decode structure
- Color is incidental — used for aesthetics or tool defaults, not meaning

### Designer-made characteristics:
- Visual hierarchy encodes importance — bigger, bolder, or higher-positioned elements are more important
- Labels are communication — they say what something does for the reader, not what it is technically
- Scope is intentional — elements are included because they serve the audience's decision, not because they exist in the system
- Reading order is explicit — the layout guides the eye
- Color is semantic — every color choice has a stated meaning in the legend

**The test:** Show the diagram to someone with no context for 5 seconds, then cover it and ask: "What is the most important thing in that diagram? What is the reading order?" If they can't answer, the hierarchy is wrong.

---

## Studio conventions — IDEO, Frog, Method, Cooper, Pentagram

Published artifacts from these studios share common conventions for explanatory diagrams:

### Hierarchy through scale
Parent/container nodes are visually larger than their children. The most important concept is the largest element or sits in the most prominent position (center or top-left).

### Restrained color palette
3–5 colors maximum for semantic categories. No rainbow charts. Typically: one neutral (background/context), one primary (main subject), one accent (highlight/callout), one for positive states, one for negative/risk states.

### Generous whitespace
Studio diagrams have significantly more whitespace than most team-produced diagrams. Whitespace creates hierarchy — clustered elements read as a group; separated elements read as distinct.

### Annotations as first-class elements
Studio artifacts include concise annotations explaining WHY, not just WHAT. A node labeled "Authentication Service" is less useful than "Authentication Service — validates user sessions; bottleneck during high-traffic events."

### Stated scope
Every studio artifact has a header block stating: what the diagram shows, what it excludes, who it is for, and when it was last updated.

---

## ADR visualization conventions

Architecture Decision Records have specific visualization needs:

**Structure of an ADR:**
1. **Title** — decision identifier and short description
2. **Context** — what situation forced this decision?
3. **Decision** — what was chosen?
4. **Consequences** — what changes as a result?
5. **Alternatives considered** — what was rejected and why?
6. **Status** — proposed / accepted / deprecated / superseded

**Visualization approach:**
- Use a card-per-ADR format. Each card contains: ADR number, title, status (color-coded), one-line context, one-line decision, key consequences (max 3 bullets)
- Group related ADRs in zones by domain (e.g., "Data Layer," "Auth," "UI Architecture")
- Use connectors to show relationships between ADRs (ADR-009 supersedes ADR-003; ADR-010 depends on ADR-008)
- Status colors: proposed = yellow, accepted = green, deprecated = red, superseded = grey

**Common mistake:** Making ADR cards too detailed. Cards in a visualization should be scannable, not complete. Link to the full ADR document for detail.

---

## Conceptual model conventions

A conceptual model shows how users think about a system — not how it is technically implemented.

**Key distinction:** A conceptual model is not a data model, entity-relationship diagram, or system architecture. It shows the user's mental model — the concepts they use to understand the product and the relationships between those concepts as they perceive them.

**Notation:**
- **Concepts:** rounded rectangles or circles (soft edges = cognitive, not technical)
- **Relationships:** labeled connectors (the label describes the relationship from the user's perspective)
- **Attributes:** small text below the concept node
- **Hierarchy:** vertical position (higher = more general)
- **Membership:** enclosure (a concept contained in a zone is a sub-type of the zone label)

**Validation:** Conceptual models should be validated with users. If users don't recognize the concepts or relationships, the model is wrong — it represents the team's mental model, not the user's.
