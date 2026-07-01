<!-- Diverge-then-select exploration (2026-07-01): should GUILD's surface be MORE than a widget?
     Recommendation delivered as a DECISION PACKET for the owner — not decided autonomously. -->

# GUILD Surface — Diverge → Select (2026-07-01)

**Question:** should GUILD's surface be just an atrium widget, or MORE?
**Inputs read:** NORTH-STAR.md, `widget-mocks/claude-final.html` (converged Now/Journey/Library mock), Nourish `batched-review-v2-speedrun.md` (the real D1–D4 decision packet), owner's parked IA-site idea.

---

## Concept 1 — "SIGIL": Atrium-Native Pane Widget (deep integration)

**Pitch.** GUILD lives *inside* the owner's actual workspace as a first-class atrium pane — the converged 3-view mock (Now / Journey / Library) made real, with cards that ARE atrium tasks, agent runs that ARE atrium agents, and artifacts that open into sibling panes. GUILD isn't an app you visit; it's ambient presence in the room where work already happens. The widget is per-project: open the nourish room, get the nourish GUILD.

**IA.** Single pane, labeled horizontal tab bar (per converged direction): **Now** (needs-you queue, live runs, ranked suggestions, gate tiles) · **Journey** (persistent 7-phase pipeline strip + "briefing so far" narrative) · **Library** (artifact index with provenance chips, drift flags, versions, filter chips). Persistent journey strip across all views. Footer quick-actions (Quest / Diverge / QA / Heal).

**Owner asks →**
- *Comment→regenerate:* comment on an artifact opened in a sibling atrium pane; the widget's Now view surfaces "3 variants ready → pick"; the pick is captured to the taste model. Depends entirely on atrium relaying comment events.
- *Suggestions + pattern memory:* the Now suggestions zone, ranked and cited (already in the mock).
- *Component-equivalence:* Library provenance rows ("this = Hearth `Card/Elevated`, 94% match — adopt?").
- *Needs-you packets:* the D1–D4 packet renders as the Needs-you zone; each Dn is an accept/waive card that becomes an atrium task.

**Uniquely enables.** Zero-context-switch design ops; GUILD actions create real atrium tasks; agents/sigils visible in-room; the "GUILD is alive in your workspace" feeling nothing else gives.

**Costs.** Build: medium (mock exists; wiring is the work). Maintenance: low-medium. **Dependency on Jonny's API: TOTAL** — until the pane API exists, this ships as a canvas HTML note: read-mostly, actions are cosmetic, no comment events, no deep links. Single-user, single-project by construction.

**Failure mode.** Hostage. The pane API slips → GUILD's surface stays a static poster for months, the comment→regenerate loop (the owner's #1 ask) never closes, and "usable by others" collapses to "usable by people who run atrium," which today is a set of size ~2.

---

## Concept 2 — "GUILD HALL": Standalone Multi-Project Cockpit (web app)

**Pitch.** A small local-first web app (`guild serve` → localhost, deployable anywhere) that reads the per-project feed JSON directly and renders the cockpit for **every** GUILD project at once — nourish, the widget quest, Claude Design pulls — with the converged Now/Journey/Library IA as its per-project drill-in. It is GUILD's own front door: Jonny opens a URL and sees the same brain the owner sees, no atrium, no CLI, no repo spelunking required. Atrium, when its API lands, embeds this exact app as a pane — the surface itself obeys the north star: **one canonical feed, many hosts, the host is an adapter.**

**IA.** **Home** (multi-project grid: per-project phase, needs-you count, drift flags, last-activity) → **Project** (= the converged 3-view widget verbatim: Now / Journey / Library) → **Packet** (full-screen decision-packet reader: the D1–D4 layout with evidence tables, gate results, screenshots inline, Approve/Waive/Discuss per decision) → **Artifact** (rendered artifact with a comment layer, see asks). Global nav: labeled tabs Home / Inbox (all needs-you across projects) / Patterns (the taste + pattern memory, browsable).

**Owner asks →**
- *Comment→regenerate:* artifacts render inside the app with an element-level comment layer (click element → comment → "generate 3 variants" → side-by-side pick → applied; pick written to taste-model.yaml with provenance). **Closes the loop with zero atrium dependency** — the app owns both the comment surface and the action channel (writes intents to the feed dir; the GUILD engine watches).
- *Suggestions + pattern memory:* Inbox aggregates ranked, cited suggestions across projects; **Patterns** view makes the taste model a first-class, inspectable object (this is new capability, not just parity).
- *Component-equivalence:* equivalence findings appear both in Library rows and in Patterns ("3 projects re-implement `StatTile` — canonize?"), which only a multi-project surface can even ask.
- *Needs-you packets:* the Packet reader is the flagship screen — Nourish's speedrun packet becomes a clickable review with recorded verdicts, not a markdown file the owner scrolls.

**Uniquely enables.** The "usable by others" play for real: Jonny (and anyone) reviews packets and picks variants from a link. Cross-project brain views (pattern memory, equivalence, portfolio drift) that no single-room widget can express. Ships **now** — feed JSON is the only prerequisite, and it's already being built.

**Costs.** Build: medium-high (a real app: static viewer is a week-scale effort; the write channel — verdicts/picks/comments back to the engine — is the honest cost). Maintenance: medium (it's yours forever). **Dependency on Jonny's API: ZERO to ship; optional to embed.**

**Failure mode.** The dashboard graveyard: yet another localhost app nobody opens because the work happens in atrium and the terminal. Mitigation is structural — it must be the *only* place packets can be decided, and `guild` CLI output must deep-link into it.

---

## Concept 3 — "ATLAS": Dedicated IA-Collab Surface (the parked idea, absorbed)

**Pitch.** The parked 2026-06-30 idea as the whole product: a site where the **live IA itself** — sitemap, conceptual model, journeys, personas, flows — is the canvas. Every node/edge/persona-attribute is commentable and threaded; comments carry research citations inline (R-12 style chips); "this node drifted from R-08" is rendered *on the node*. Comment→regenerate operates on **structure**: comment on the onboarding branch → GUILD proposes 3 IA restructures → pick → the canonical artifact model updates and every downstream renderer re-derives. Better than FigJam because the board *is* the model, not a picture of it.

**IA.** **Map** (zoomable live IA, drift heat, evidence chips per node) · **Journeys** (persona × journey lanes, commentable stages) · **Threads** (all comments/decisions, filterable by node/persona/status) · **History** (model versions; every accepted pick is a diff with provenance).

**Owner asks →**
- *Comment→regenerate:* native and strongest here — but scoped to IA/structural artifacts, not rendered visual elements (the Nourish "make this ring livelier" class of comment has no home).
- *Suggestions + pattern memory:* structural suggestions only ("collapse these two nav branches — tree-test data says users conflate them").
- *Component-equivalence:* expressible as model-level equivalence (two screens instantiate one conceptual object) — elegant, but not the component-library sense the owner means.
- *Needs-you packets:* poor fit; a D1–D4 gate packet (perf gates, motion passes, DTCG registration) isn't an IA object. Would need a bolted-on inbox.

**Uniquely enables.** True multi-person structural collaboration on the thing GUILD says is its core competency (IA); the canonical artifact model gets a face; Jonny can argue about the nav *in* the nav.

**Costs.** Build: **high** — live graph rendering, threaded multiplayer comments, auth, model-diffing. Maintenance: high. Jonny-API dependency: zero. It is, candidly, a product.

**Failure mode.** Building a FigJam competitor with an audience of two. Months of collab-infra work while the daily loop (packets, gates, variant picks) still has no surface — the brain gets a beautiful face and still no hands.

---

## Concept 4 — "POSSESSION": No Surface — GUILD Haunts the Artifacts

**Pitch.** The anti-widget: GUILD has *no* home of its own. Every artifact GUILD renders — prototype HTML, Figma file, decision packet — ships with a tiny injected overlay (a `<script>` in every generated prototype; a comment layer in Figma via the existing plugin tools). You comment where you're already looking; a floating GUILD chip on any artifact shows needs-you count and suggestions *for that artifact*. Decision packets are interactive HTML documents (the packet IS an app). The surface is maximally adapter-shaped: GUILD's presence is a protocol, not a place.

**IA.** None global — per-artifact overlay: comment pins · variant strip (A/B/C picker) · provenance drawer · "needs-you" chip. Packets: self-contained HTML with Approve/Waive buttons posting to the feed.

**Owner asks →** *Comment→regenerate:* strongest possible ergonomics (comment literally on the rendered element in the running prototype). *Suggestions:* only artifact-local — no ranked global queue. *Equivalence:* shown at point-of-use ("this button ≡ Hearth `Button/Primary`"). *Packets:* good as interactive documents, but scattered — no inbox, no journey strip, no "where am I."

**Uniquely enables.** Zero-friction feedback at the exact pixel; purest north-star reading (surface = protocol).

**Costs.** Build: medium (overlay lib + packet template). Maintenance: low. Jonny dependency: zero. **Failure mode.** No wayfinding: nothing answers "what needs me across my projects / what phase am I in" — the exact questions the converged widget was designed for. It's a limb, not a body.

---

## Scoring (1–5; maintenance: 5 = low burden)

| | 1 SIGIL (atrium pane) | 2 GUILD HALL (cockpit) | 3 ATLAS (IA-collab) | 4 POSSESSION (overlay) |
|---|---|---|---|---|
| **Brain north-star fit** | 3 — binds the brain's face to one host; the host isn't an adapter, it's a landlord | **5** — one canonical feed, host-agnostic; atrium becomes literally an adapter that embeds it | 4 — makes the canonical model first-class, but privileges one artifact class | 5 — surface-as-protocol is the purest reading |
| **Owner-asks coverage** | 4 — all four asks mapped, but comment→regenerate is blocked on the API | **5** — all four native, incl. the only real home for D1–D4 packets and pattern memory | 2 — nails structural comment→regenerate, whiffs on packets, visual comments, equivalence-as-meant | 3 — best-in-class comment loop, weak suggestions/packets aggregation |
| **Usable-by-others** | 1 — requires running atrium; audience ≈ 2 today | **5** — a URL; Jonny reviews a packet from a link with no install | 4 — collaborative by design, once built | 2 — others can comment on an artifact they're handed, but can't see the brain |
| **Time-to-useful** | 2 — useful *now* only as a static note; the loop waits on Jonny | **4** — read-only cockpit over existing feed JSON in days; write channel in weeks | 1 — quarters, honestly | 4 — overlay + packet template are small |
| **Maintenance burden** | 4 — small surface, but tracks two moving targets (atrium + feed) | 3 — a real app you own forever | 1 — collab infra, graph engine, auth | 4 — one small lib, many injection points to keep working |
| **TOTAL** | 14 | **22** | 12 | 18 |

---

## Recommendation: **Concept 2 — GUILD HALL** (standalone multi-project cockpit)

It is the only concept that closes the owner's #1 loop (comment→variant→pick→taste) **without waiting on an API that doesn't exist**, the only one where "usable by others" is a link instead of an install, the only home the D1–D4 packet class has ever had, and — decisively — the one that best obeys the north star: the widget question dissolves, because *the atrium widget becomes the cockpit's embed adapter*, not a competing surface. The converged Now/Journey/Library direction is not discarded; it is verbatim the cockpit's per-project view, so the design work already done ships inside the winner.

**Rejected, with grafts to take later:**
- **SIGIL** — rejected as the *primary* surface (hostage to the API), but its deep-integration moves (cards = atrium tasks, artifacts open as panes, agent presence) are exactly what the Jonny spec below requests; graft them the day the API lands.
- **ATLAS** — rejected as a product; graft its one killer idea as a cockpit view later: a read-only live-IA map with drift heat and per-node comments (no multiplayer canvas, no auth epic).
- **POSSESSION** — rejected as a body; graft its limb immediately: the per-artifact comment overlay is *how* the cockpit's Artifact view implements comment→regenerate, and interactive-HTML packets are the fallback for anyone the cockpit can't reach.

---

## Jonny Spec — Atrium Pane API for GUILD HALL (one page)

**Model:** GUILD HALL is a self-contained web app (served locally or hosted). Atrium hosts it as an **embedded web pane** and exchanges events over a `postMessage` bridge (or WS equivalent — transport is yours; the contract below is what matters). Everything is optional-degrade: the app works with zero atrium; each capability you add upgrades it.

### 1. Pane lifecycle
- `atrium.pane.register({ id: "guild-hall", url, icon, minSize })` — plugin manifest registers GUILD as an openable pane type; openable per-room.
- Host → app on mount: `{ type:"atrium.context", room, projectPath, theme:{tokens}, user:{id,name}, capabilities:[...] }`. `projectPath` lets the pane auto-scope to that room's project; `capabilities` tells the app which of the events below actually work.
- Host → app: `atrium.resize {w,h}` and `atrium.theme` on change; app must render from widget-strip (≈360px) to full-pane.
- App → host: `guild.ready`, `guild.badge {count}` (needs-you count for the pane tab/sigil).

### 2. Feed refresh
- The app owns its data (feed JSON per project). Atrium does **not** proxy the feed. One assist: `atrium.fs.watch(projectPath + "/guild-artifacts/feed/") → atrium.fs.changed {paths}` so the pane updates without polling. If unavailable, app polls; nothing breaks.

### 3. Deep links (host → world, both directions)
- App → host, fire-and-forget intents:
  - `atrium.open.task {taskId}` — focus a task card on the board.
  - `atrium.open.note {noteId, anchor?}` — open a canvas/HTML note.
  - `atrium.open.pane {kind:"browser"|"terminal"|"figma", target}` — e.g. open a rendered prototype in a browser pane beside GUILD.
  - `atrium.open.url {url}` — fallback.
- Host → app: atrium URIs like `atrium://guild/packet/<id>` or `atrium://guild/artifact/<id>?comment=<cid>` route into the pane (so a task card can link back to the exact decision). This is the single most valuable item after embed itself.

### 4. Comment events OUT (atrium → GUILD)
When a user comments on anything GUILD-provenanced (task, note, browser pane showing a GUILD artifact), emit:
```json
{ "type":"atrium.comment", "id":"c-…", "author":{"id","name"},
  "target":{"kind":"task|note|pane","id":"…","selector":"<element/anchor if known>"},
  "body":"markdown", "ts":"iso8601" }
```
`selector` is best-effort (DOM path / note anchor); GUILD maps it to an artifact element and feeds the comment→regenerate loop. Also emit `atrium.comment.resolved {id}`.

### 5. Action events IN (GUILD → atrium)
- `guild.task.create {title, body, status, links:[atrium://guild/...], labels}` → returns `{taskId}`. (Needs-you decisions and drift flags become real board cards.)
- `guild.task.update {taskId, status|body}` — e.g. auto-close the drift card when re-validation passes.
- `guild.notify {level:"info|needs-you", title, body, link}` — room-level toast/inbox entry ("Batched review ready: 4 decisions").
- `guild.agent.status {runId, agent:"mage", phase, progress}` — optional, powers agent presence/sigils in-room.

### 6. Guarantees GUILD needs from you
- **Idempotency + IDs:** task/comment IDs stable across sessions; GUILD stores them in the feed for round-tripping.
- **Capability negotiation:** every message above individually optional; app degrades per-capability (that's the whole design).
- **Auth/user identity** on comments and verdicts — picks train the taste model *per person*; anonymous comments can't.
- **Versioning:** `{ "atriumApi": "1" }` in the context message; GUILD pins per-version behavior.

**Minimum viable slice (in order of value):** (1) embed pane + context message → (2) deep-link intents `open.task` / `open.pane` → (3) `guild.task.create` → (4) comment events out. Slice 1 alone replaces the static HTML-note widget; slices 1–4 are full SIGIL-grade integration.
