
# GUILD IA-FACTORS RESEARCH (v1 — 2026-07-05)


## The Operational Factor-Space of Superb Information Architecture for AI Systems


---


## 1. VERDICT

The complete factor-space of information architecture splits cleanly into **three verification tiers**, and the shape of that split is the central finding: IA quality is **more human-bound than rendered-surface (UI) quality**. Where UI factors (contrast, geometry, saliency) are overwhelmingly MEASURE-tier (deterministic over pixels/DOM), IA factors distribute roughly one-third MEASURE, one-third LOOK (model-judgment against a rubric), and one-third ASK (real human testing) — because findability and comprehension are, at root, facts about human minds, not facts about artifacts.

The factor-space organizes into **five families**: (A) **Semantic/labeling** factors (information scent, terminology consistency, jargon) — the highest-leverage and most machine-tractable; (B) **Structural/graph** factors (depth/breadth, orphans, dead ends, cycles, content-model completeness) — the most fully MEASURE-able; (C) **Wayfinding/orientation** factors (you-are-here, breadcrumbs, the trunk test); (D) **Flow/task** factors (steps-per-task, detours, recovery paths); and (E) **Ground-truth human** factors (card-sort agreement, tree-test success, first-click correctness) that no automated proxy can currently replace.

**The single highest-leverage gap** in a provenance-only (spine-gated, evidence-cited-but-not-structurally-tested) IA practice is the absence of an **artifact-time semantic comprehension gate** — specifically, a **label-comprehension and information-scent check that simulates a first-click/tree-test at the artifact stage and blocks on ambiguity, jargon, and truncation before build.** This is exactly what would have caught the Hall blind-test round-1 failure: the decision cards read as ambiguous, the copy was jargon-heavy, and truncation hid meaning — all three are *semantic scent defects* that are detectable (as LOOK-tier simulation and partly as MEASURE-tier string checks) on the artifact model **before** anything renders. The provenance lane proves every IA claim traces to research; it never asks "does this label actually predict its destination to a naive reader?" That question is the gate. Its expected value is anchored by the strongest replicated finding in the field: across a dozen studies (2006–2009), Bailey & Wolfson found that *"if a user's first click on a website was down one of the optimal paths for the intended task, 87% of those users eventually succeeded… only 46% of users succeeded"* if not (reported via MeasuringU, *Do Click Tests Predict Live Site Clicks?*). A label-scent gate is therefore the highest-expected-value check that can be added first.

A critical honesty constraint runs through this entire report: **the LOOK-tier simulations (an LLM predicting first-clicks, scoring scent, or simulating a card sort) are simulations of an ASK-tier ground truth and must never be represented as equivalent to it.** The 2024–2026 evidence (below) shows these simulations are useful as *screens* (especially as expert/"power-user" lower bounds) but are measurably unreliable as *predictors of real human behavior*.


---


## 2. RANKED TAXONOMY

Each factor carries the five-part contract: **Evidence** (with verbatim quotes), **Machine Proxy**, **Thresholds**, **Check Tier**, **Failure Mode**. Factors are ranked by **impact × machine-checkability** (highest first). Tier legend: **MEASURE** = deterministic; **LOOK** = model judgment vs. rubric (simulation of a human test); **ASK** = mandatory human testing.


---


### FACTOR 1 — Terminology Consistency (one concept = one name everywhere)

**Rank rationale: highest. High impact, near-fully deterministic.**

**Evidence.** Nielsen's Heuristic #4 (Consistency and Standards): *"Users should not have to wonder whether different words, situations, or actions mean the same thing"* (NN/g, *10 Usability Heuristics*, updated 2020). NN/g's dedicated consistency article states the rule concretely: a page titled *"Photos"* should not be called *"Images"* or *"Photographs"* elsewhere on the site. Abby Covert (*How to Make Sense of Any Mess*, 2014) grounds it: *"Controlled vocabularies are the greatest thing since sliced bread… The goal is not simplifying. The goal is to know what you mean when you say what you say."*

**Machine Proxy.** Terminology drift = the same entity ID rendered under ≥2 distinct labels across nav-label / page-title / breadcrumb / button-verb. Build an entity→label map from the artifact model and DOM; flag any entity whose label set has cardinality >1 after normalizing for case/pluralization. Also flag verb drift (e.g., "Delete" vs "Remove" vs "Trash" for one action).

**Thresholds.** Deterministic pass/fail: **0 unresolved label variants per entity** = pass; ≥1 = flag. No literature specifies a tolerance because the rule is categorical; this is a synthesized (not fabricated) pass/fail derived directly from Heuristic #4's categorical statement.

**Check Tier. MEASURE.** (String comparison over a resolved entity map; no judgment needed once synonyms are declared.)

**Failure Mode.** The Hall case's jargon copy compounded by drift: an item called one thing on a card, another in its detail title. Catches "same run labeled 'Task' in the inbox and 'Job' in the timeline."


---


### FACTOR 2 — "Junk-Drawer" / Non-Mutually-Exclusive Categories

**Rank rationale: high impact, mostly deterministic with a LOOK backstop.**

**Evidence.** Rosenfeld, Morville & Arango (*Information Architecture for the Web and Beyond*, 4th ed., 2015 — the "polar bear book") distinguish **exact** organization schemes (alphabetical, chronological, geographical — "well defined and mutually exclusive") from **ambiguous** schemes (topic, task, audience). They warn that *"classification systems are made of language, and language is ambiguous."* Covert: *"There is no one right way to organize something,"* but categories must serve a goal.

**Machine Proxy.** (a) Junk-drawer smell = any category whose label ∈ {More, Other, Misc, Miscellaneous, General, Stuff, Extras} — deterministic string match. (b) Mutual-exclusivity check = for a stated exact scheme, verify no item appears in ≥2 sibling categories (unless polyhierarchy is declared). (c) Cohesion check (LOOK) = an LLM scores whether category members share an extractable common attribute.

**Thresholds.** Junk-drawer label present = flag (deterministic). Card-sort agreement provides the human ground-truth threshold: standardized-category agreement **≥60% is "good," ≥80% is the target** (Optimal Workshop, UXtweak, and UserTesting help documentation converge on these bands; this is practitioner-tier, not independently replicated — see weak-evidence flags in §5).

**Check Tier. MEASURE** for (a) and (b); **LOOK** for (c) cohesion; **ASK** for true grouping validity (card sort).

**Failure Mode.** A "More" menu accreting unrelated owner actions; an item findable under two sibling categories so users second-guess which is "right."


---


### FACTOR 3 — Information Scent / Label Predictiveness

**Rank rationale: highest impact on findability; partly LOOK, partly MEASURE.**

**Evidence.** Pirolli & Card's information foraging theory (*Information Foraging*, Psychological Review 106, 1999): users maximize **Rate of gain = Information value / Cost of obtaining it**, following *"information scent — the (imperfect) perception of the value, cost, or access path of information sources obtained from proximal cues."* NN/g operationalizes: *"Vague verbs (such as Explore, Discover, Learn, Partner) are not effective category names — they offer too little differentiation."* NN/g's *Better Link Labels* quotes a study participant: *"These Learn more links… It's just not very specific… I have no idea what to expect, that's why I never click those."* NN/g's *Writing Hyperlinks* rule: links should be *"Salient, Descriptive, Start with Keyword."* [Cmu + 2](https://act-r.psy.cmu.edu/wordpress/wp-content/uploads/2012/12/280uir-1999-05-pirolli.pdf)

**Machine Proxy.** (a) Generic-label detector (MEASURE): flag labels ∈ {Click here, Learn more, Read more, Explore, Discover, More info, Details} and CTAs lacking a noun object. (b) Front-loading check (MEASURE): does the label's first token carry meaning or is it a filler verb/article? (c) Scent-decay/first-click simulation (LOOK): an LLM, given only the labels at each level and a task, predicts which branch it would click; low confidence or wrong branch = flag.

**Thresholds.** No agreed numeric scent threshold exists in the literature. The Bailey & Wolfson first-click benchmark anchors the *human* target: across a dozen studies (2006–2009), *"87% of those users eventually succeeded"* when the first click was on an optimal path versus *"only 46%"* when it was not. MeasuringU's replication found a smaller but real effect (**70% vs. ~24%** in one dataset; and a more modest ~13-point gap in a separate 5-site, 21-task, 750-participant study) — report the disagreement, do not average (see §5).

**Check Tier. MEASURE** for (a)/(b); **LOOK** for (c), explicitly a **simulation of an ASK-tier first-click test**.

**Failure Mode.** Hall's ambiguous decision cards — labels that don't predict destination. Directly the round-1 blind-test failure.


---


### FACTOR 4 — Jargon / Reading-Level / Match to User Vocabulary

**Rank rationale: high impact (Hall calibration case), MEASURE + LOOK.**

**Evidence.** Nielsen Heuristic #2 (Match Between System and Real World): use *"words, phrases, and concepts familiar to the user, rather than internal jargon."* NN/g's *Error-Message Guidelines* set a hard readability bar: error text *"should be written at a 7–8th-grade reading level (Flesch-Kincaid formula) or lower."* GOV.UK: *"using technical jargon… alienates many more [users]."* Covert warns against *"nonsense jargon."* [Nielsen Norman Group](https://www.nngroup.com/articles/error-messages-scoring-rubric/)[Blog](https://designnotes.blog.gov.uk/2018/11/05/how-we-document-components-and-patterns-in-the-gov-uk-design-system/)

**Machine Proxy.** (a) Reading-level (MEASURE): compute Flesch-Kincaid over labels/microcopy; flag > grade 8. (b) Jargon detector (LOOK/MEASURE hybrid): flag tokens absent from the product's declared controlled vocabulary / a general-domain frequency list; flag unexpanded acronyms on first use. (c) Domain-term coverage (MEASURE): compare label vocabulary against extracted user-facing vocabulary.

**Thresholds.** **Flesch-Kincaid ≤ grade 8** for microcopy (NN/g, cited). No agreed threshold for "jargon density" exists in the literature.

**Check Tier. MEASURE** for reading level and acronym expansion; **LOOK** for jargon judgment against audience.

**Failure Mode.** Hall's "jargon-heavy copy" — precisely this factor. Catches "run spine 'reconciliation' surfaced to owners who don't know the term."


---


### FACTOR 5 — Meaning-Hiding Truncation

**Rank rationale: high impact (direct Hall failure), MEASURE.**

**Evidence.** This sits at the IA/render boundary. NN/g's link-label research stresses front-loading keywords precisely because *"users scan"* and later words are lost — truncation that removes the disambiguating token destroys scent. Krug's *Don't Make Me Think* principle: elements must be self-evident without effort.

**Machine Proxy.** (MEASURE) For each label/title with a max-width or line-clamp, simulate truncation at the rendered character budget and test whether the surviving prefix is still unique and meaningful within its sibling set (i.e., does the truncated form collide with a sibling, or drop the only distinguishing token?). Flag if the distinguishing token falls beyond the truncation point.

**Thresholds.** Deterministic: truncated prefix must remain **unique among siblings** and **retain the head noun**. No external numeric literature threshold; derived from front-loading evidence.

**Check Tier. MEASURE.**

**Failure Mode.** Hall's "truncation hid meaning" — e.g., "Approve vendor payment for…" clipped to "Approve vendor payment fo…" or two runs truncating to identical prefixes.


---


### FACTOR 6 — Content-Model / Sitemap Graph Health (orphans, dead ends, cycles, list+detail completeness)

**Rank rationale: highest machine-checkability; fully MEASURE at artifact time.**

**Evidence.** Polar bear book frames IA as organization + navigation + labeling + search **systems**; a well-formed structure has no unreachable nodes. Shopify Polaris IA guidance: navigation should *"bridge content to other parts of the product"* and *"all screens should have meaningful navigation."* Krug's trunk test presumes every page situates within a reachable hierarchy.

**Machine Proxy.** (MEASURE) Build a directed graph from the sitemap/content model. Compute: (a) **orphans** = nodes with in-degree 0 (excluding the declared root/home); (b) **dead ends** = non-terminal content nodes with out-degree 0 or no path back to a hub; (c) **cycles** = strongly-connected components that shouldn't exist (circular parent references); (d) **completeness** = every content entity type has both a list/index view and a detail/"home" view.

**Thresholds.** Deterministic: **0 orphans, 0 unintended dead ends, 0 illegal cycles, 100% list+detail coverage** = pass. (No numeric tolerance in literature; graph-theoretic pass/fail.)

**Check Tier. MEASURE.** (Pure graph analysis over the artifact model — the highest-value artifact-time check.)

**Failure Mode.** A detail view with no list view (item exists but is unbrowsable); a run that, once opened, has no path back to the inbox.


---


### FACTOR 7 — Depth vs. Breadth of Hierarchy / Click-Depth to Core Tasks

**Rank rationale: high impact; MEASURE structure, but thresholds contested.**

**Evidence.** The classic menu-selection studies favor **moderate breadth over depth**: Miller (1981) found a two-level, eight-per-level (8×8) structure beat both flat (64×1) and deep (2⁶) arrangements; Kiger (1984) recommended *"menus of eight or nine selections each."* But the foundational *web* study, **Larson & Czerwinski (1998)**, complicates this: across 512-node trees (8×8×8, 16×32, 32×16), the **two-level structures beat the three-level** — mean times ≈ **36s (16×32), 46s (32×16, SD ≈ 26), 58s (8×8×8)** — and the deepest tree produced the most time-outs (9 for 8×8×8 vs. 2 for the shallower structures). Net: limiting depth mattered more than limiting breadth. Miller & Remington's modeling (2004) showed the result is dominated by **label ambiguity (information scent)**, not raw shape. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0020737384800188)

**Machine Proxy.** (MEASURE) Compute click-depth (shortest path from root) to each declared core task; compute tree breadth per level; compute depth distribution. Flag core tasks buried below a configurable depth and flag any single menu exceeding a configurable breadth.

**Thresholds.** **No universally agreed numeric threshold exists** — and the "magic number" thresholds are actively contested (see §5). Miller/Kiger suggest ~8–9 per level; Larson & Czerwinski show depth ≤2 outperforms for ~500 items. The **three-click rule is debunked** (§5) and must not be used as a hard threshold. Best practice: measure depth-to-core-task and *scent*, not a magic number.

**Check Tier. MEASURE** (for the geometry); the *interpretation* is advisory because thresholds are contested.

**Failure Mode.** Core owner task (e.g., "approve a run") buried 4+ levels deep; or an over-deep tree where each level adds an ambiguous choice.


---


### FACTOR 8 — Wayfinding: "You-Are-Here" / Current-Location Marking

**Rank rationale: high impact, MEASURE presence + LOOK correctness.**

**Evidence.** NN/g *Navigation: You Are Here*: *"Navigation should not only show where you can go but also where you are now… Failing to indicate the current location is probably the single most common mistake we see on website menus."* Krug's **trunk test**: dropped on a random deep page, can the user answer *what site is this, what page, what section, my options, where am I in the scheme, how do I search?* [Nielsen Norman Group](https://www.nngroup.com/articles/navigation-you-are-here/)

**Machine Proxy.** (a) MEASURE: does each page expose a current-location indicator (active nav item via `aria-current`, highlighted state)? (b) MEASURE: is the indicated location consistent with the page's actual position in the sitemap graph? (c) LOOK: automate the trunk test — feed a rendered page (stripped of prior context) to a model and ask it to answer Krug's six questions.

**Thresholds.** Deterministic presence check: **every non-home page marks current location** = pass. Trunk-test (LOOK) has no numeric literature threshold; rubric-scored.

**Check Tier. MEASURE** for presence/consistency; **LOOK** for the trunk-test simulation.

**Failure Mode.** A run-detail page that doesn't mark which inbox section it belongs to; user "dropped in" from a notification cannot orient.


---


### FACTOR 9 — Breadcrumbs / Hierarchical Path Integrity

**Rank rationale: moderate-high impact, MEASURE.**

**Evidence.** NN/g has *"been recommending breadcrumbs since 1995… they provide many benefits to users at almost no cost."* User testing shows *"many benefits and no downsides to breadcrumbs for secondary navigation."* Critically: *"breadcrumbs should show the location of the current page in the site's IA, not the user's browsing history."* For polyhierarchy, a canonical path must be chosen. [Nielsen Norman Group + 2](https://www.nngroup.com/articles/breadcrumbs/)

**Machine Proxy.** (MEASURE) For each page with a breadcrumb, verify the trail equals the actual ancestor path in the sitemap graph (IA-based, not history-based); flag trails that don't terminate at root or that misrepresent parentage. Flag deep hierarchies (>3 levels) lacking breadcrumbs.

**Thresholds.** Deterministic: breadcrumb path == graph ancestor path. NN/g notes hierarchies **>3 levels** particularly benefit; ≤3 can sometimes omit them.

**Check Tier. MEASURE.**

**Failure Mode.** Breadcrumb reflecting click history rather than IA (user disoriented on refresh/deep-link).


---


### FACTOR 10 — Addressability / Deep-Link & State-in-URL Integrity

**Rank rationale: moderate-high impact, MEASURE.**

**Evidence.** Bailey & Wolfson note *"at least 50% of users may access a site from pages that are not the homepage"* — so every meaningful state must be addressable. GOV.UK's accordion work explicitly changed the design so *"the URL also changes when an accordion section is opened so users can still link to an open accordion section."* Krug's trunk test presumes arrival mid-site. [Webusability](http://webusability.com/firstclick-usability-testing/)[Blog](https://designnotes.blog.gov.uk/2017/06/29/designing-new-navigation-elements-for-gov-uk/)

**Machine Proxy.** (MEASURE) For each distinct IA location/state, verify a unique, stable URL exists; that refresh preserves location; that the URL round-trips (navigating to it reproduces the state). Flag states reachable only via in-session interaction.

**Thresholds.** Deterministic: **every distinct IA node/state has a shareable URL that survives refresh** = pass.

**Check Tier. MEASURE.**

**Failure Mode.** A run only viewable by clicking through the inbox; refreshing or sharing the link loses location — the "dropped in the trunk" user can't be linked there at all.


---


### FACTOR 11 — Task-Flow Efficiency (steps / detours / dead ends per core task)

**Rank rationale: high impact, MEASURE structure + ASK for real efficiency.**

**Evidence.** GOV.UK step-by-step navigation pattern was built over *"8 rounds of research with users, including those with disabilities and people with low digital literacy."* NN/g and Krug both stress removing navigation during focused flows (checkout/forms) but ensuring recovery. The debunking of the three-click rule (§5) reframes the metric: *"Users don't count clicks; they count progress"* — measure detours and dead ends, not raw clicks. [Icons8](https://icons8.com/blog/articles/three-click-rule/)

**Machine Proxy.** (MEASURE) Model each core task as a path in the flow graph. Count required steps/inputs/decisions; detect **backtracks** (edges returning to prior states), **detours** (paths longer than the optimal), and **dead ends** (states with no forward or recovery edge).

**Thresholds.** **No agreed numeric step threshold exists** (and click-count thresholds are debunked). Measure against the *task's own optimal path*; flag dead ends deterministically (0 tolerated).

**Check Tier. MEASURE** for graph properties; **ASK** for true task efficiency (usability test / task-time benchmark).

**Failure Mode.** An approval flow with a state offering no forward action and no back link — user stuck.


---


### FACTOR 12 — Recovery Paths (empty / error / 404 / permission-denied back into IA)

**Rank rationale: high impact, MEASURE presence + LOOK quality.**

**Evidence.** NN/g's Heuristic #9: *"Help Users Recognize, Diagnose, and Recover from Errors."* NN/g *Empty States*: *"Do not default to totally empty states… use the empty state to provide help cues… Provide direct pathways (i.e., links) to getting started with key tasks."* NN/g on 404s: error pages must be *"constructive in suggesting steps the user can take to correct the problem."* Different states need different recovery: a 404 should suggest where to go; a 403 should suggest who to contact.

**Machine Proxy.** (a) MEASURE: does every empty/error/404/403 state contain ≥1 navigational link back into the primary IA (not a dead end)? (b) MEASURE: does each state avoid raw error codes as the only content? (c) LOOK: does the recovery copy name a constructive next step (rubric-scored)?

**Thresholds.** Deterministic: **every terminal/error state has ≥1 in-IA recovery link** = pass; **0 states showing only a raw code** = pass.

**Check Tier. MEASURE** for presence; **LOOK** for constructiveness.

**Failure Mode.** A permission-denied wall with no "request access" or "back to inbox" link; an empty inbox that doesn't explain how to get work.


---


### FACTOR 13 — Progressive-Disclosure Architecture (default vs. behind-a-click; disclosure consistency)

**Rank rationale: moderate impact, LOOK-dominant.**

**Evidence.** Shopify Polaris: *"Don't over-simplify, but don't burden your user with choice. To do this in design, we use progressive disclosure, but this principle also applies to information architecture."* NN/g's scanability/progressive-disclosure work (noted as belonging to render-time gates in the UI-factors research).

**Machine Proxy.** (a) MEASURE: consistency of disclosure depth across sibling components (are like things disclosed alike?). (b) LOOK: is detail shown by default that should be deferred (premature exposure), or deferred that's task-critical (buried primary action)?

**Thresholds.** No agreed numeric threshold. Consistency is deterministic (siblings same depth); appropriateness is rubric-scored.

**Check Tier. MEASURE** for consistency; **LOOK** for appropriateness. (Overlaps render-time gates from UI-factors research — flagged as partially surface-specific.)

**Failure Mode.** One run type showing full detail inline while an identical sibling hides it; a primary decision hidden behind an expand.


---


### FACTOR 14 — Structural Semantics as Rendered: Heading/Landmark Outline as a Faithful IA Map

**Rank rationale: moderate impact, MEASURE well-formedness (elsewhere) + LOOK fidelity (here).**

**Evidence.** Krug's trunk test again (page must self-describe). The polar bear book treats structure as the thing labels must faithfully express. The distinction from the existing focus-gate is explicit: that gate checks the outline **exists / is well-formed**; this factor checks the outline is a **faithful map of the underlying IA**.

**Machine Proxy.** (a) MEASURE: extract the heading tree (h1–h6) and landmarks; (b) LOOK: compare the heading outline, *read in isolation*, against the artifact-model's intended IA for that page — does the outline alone tell the accurate story/shape? Flag headings that misrepresent the section's role, or an outline whose shape diverges from the content model.

**Thresholds.** Well-formedness (single h1, no skipped levels) is deterministic but **owned by the existing focus-gate**. Fidelity has no numeric threshold — rubric-scored (LOOK).

**Check Tier. LOOK** (fidelity), building on MEASURE well-formedness from the focus-gate.

**Failure Mode.** A page whose headings read as a coherent but *wrong* story (outline says "Settings › Billing" but content is run history) — an IA misrepresentation invisible to a well-formedness check.


---


### FACTOR 15 — Mental-Model Conformance (inbox / editor / feed / checkout patterns vs. bespoke)

**Rank rationale: high impact, LOOK + ASK. (Baseline already shipped; extended here with a checkable proxy.)**

**Evidence.** Jakob's Law (NN/g): *"Users spend most of their time on sites other than yours… [they] bring their expectations from other sites when"* they arrive. NN/g: deviating from a standard *"would almost certainly impose a much bigger cost in terms of confusion and reduced ability to navigate smoothly."* (The Hall interface already adopted inbox + run-timeline models on this basis — the baseline not to re-derive.)

**Machine Proxy.** (LOOK) Given the artifact model, an LLM classifies the intended pattern (inbox/editor/feed/checkout/dashboard) and checks whether the structure conforms to that pattern's canonical affordances (e.g., an "inbox" has list + read/unread + item detail + return-to-list). Flag bespoke structures that reinvent a known pattern without cause.

**Thresholds.** No numeric threshold; conformance is rubric-scored against a pattern library.

**Check Tier. LOOK** for pattern conformance; **ASK** for whether users' actual mental model matches (usability test).

**Failure Mode.** A delegated-work view that looks like an inbox but lacks return-to-list or read state, breaking the borrowed mental model.


---


### FACTOR 16 — Search ↔ Browse Balance / Zero-Result & No-Search Dead Ends

**Rank rationale: moderate impact, MEASURE + ASK. (Product-type-dependent — flagged.)**

**Evidence.** NN/g *Search Is Not Enough*: *"Navigation serves important functions: it shows people what they can find on the site, and teaches them about the structure of the search space."* NN/g *No Results* guidance: zero-result pages *"frequently become a dead end, where users get stuck, lost or confused,"* and must offer alternatives/suggestions. Smashing Magazine's practical rule: *"Once a month, look at what people searched for that returned zero results."* [Nielsen Norman Group](https://www.nngroup.com/articles/search-no-results-serp/)[Smashing Magazine](https://www.smashingmagazine.com/2026/03/site-search-paradox-why-big-box-always-wins/)

**Machine Proxy.** (a) MEASURE: does a zero-result state provide ≥1 forward path (suggestions, alternative spellings, browse links)? (b) MEASURE: are there content areas reachable *only* by search (no browse path) or *only* by browse (no index)? (c) ASK/analytics: zero-result query-log analysis (requires real usage data).

**Thresholds.** Deterministic: **no zero-result dead ends** (every no-results page has a forward path). Query-log thresholds require real data.

**Check Tier. MEASURE** for dead-end structure; **ASK** for zero-result rates (needs live query logs). **Flagged as partially product-type-specific** (search-heavy products).

**Failure Mode.** Internal search returning bare "No results" with no recovery; content that exists but is unreachable by browsing.


---


### FACTOR 17 — Cross-Surface Consistency (web / mobile / notification / email)

**Rank rationale: moderate impact, MEASURE. (Product-type-dependent — flagged.)**

**Evidence.** Shopify Polaris: *"Regardless of how our merchants access Shopify, it should feel like the same product… They might begin a task on one device and finish it on another."* Nielsen Heuristic #4 (internal consistency) applied across surfaces. [Shopify Polaris React](https://polaris-react.shopify.com/foundations/information-architecture)

**Machine Proxy.** (MEASURE) Compare entity labels, hierarchy, and primary actions across surface artifact models; flag an entity/action named or nested differently across web/mobile/email/notification.

**Thresholds.** Deterministic: **label/structure parity across surfaces** (allowing declared responsive omissions).

**Check Tier. MEASURE.** **Flagged as surface-spanning-product-specific.**

**Failure Mode.** A run called "Task" in email but "Run" in-app; different section nesting on mobile.


---


## 3. GATE SPEC — "Cartographer" (artifact-time) and "Sage" (QA)

**Design principle:** artifact-time checks are the **highest-value target** because they catch structural defects before build — exactly the "between IA-decided and IA-shipped" gap that let the Hall failure through. Ordering runs cheapest-and-most-deterministic first, then simulations, then human tests.


### ARTIFACT TIME — "Cartographer" (runs on sitemap / content-model / flow diagrams / vocabulary)

**BLOCKING (deterministic, MEASURE):**

1. **Graph health** (Factor 6): 0 orphans, 0 illegal cycles, 0 unintended dead ends, 100% list+detail coverage. *Extends the completeness-gate.*
2. **Terminology consistency** (Factor 1): 0 unresolved label variants per entity across nav/title/breadcrumb/button. *New lane; complements ia-evidence gate.*
3. **Generic-label / junk-drawer scan** (Factors 2a, 3a): 0 banned generic labels; 0 {More/Other/Misc/General} categories without declared rationale.
4. **Recovery-path presence** (Factor 12): every empty/error/permission state in the flow model has ≥1 in-IA forward link.
5. **Addressability** (Factor 10): every distinct IA node/state has a declared shareable URL.

**BLOCKING (LOOK — simulation of human ground truth; blocks only on high-confidence failures):**
6. **Label-scent / first-click simulation** (Factor 3c) — *the gate that catches the Hall failure.* An LLM predicts first-click per core task from labels alone; a wrong or low-confidence branch on a core task blocks. **Labeled as a SIMULATION of a first-click test, never as equivalent to one.**
7. **Jargon / reading-level** (Factor 4): Flesch-Kincaid > grade 8 on core labels/microcopy blocks; unexpanded acronyms block.

**ADVISORY (LOOK):**
8. Category cohesion (2c), mental-model conformance (15), progressive-disclosure appropriateness (13), depth-to-core-task interpretation (7, advisory because thresholds contested).


### RENDER TIME — "Sage" (runs on live DOM)

**BLOCKING (MEASURE):**
9. **Truncation meaning-check** (Factor 5): distinguishing token must survive truncation; siblings must not collide when clipped. *Catches Hall's "truncation hid meaning."*
10. **You-are-here presence + breadcrumb integrity** (Factors 8a/b, 9): current location marked; breadcrumb == graph ancestor path.
11. **Terminology/truncation reconciliation** against rendered labels (re-runs Factor 1 on actual DOM text).
12. **Zero-result / error-state dead-end check** (Factors 16a, 12): rendered states have forward paths; no raw-code-only errors.

**ADVISORY (LOOK):**
13. **Trunk-test simulation** (Factor 8c), **heading-outline fidelity** (Factor 14 — extends, does not duplicate, the focus-gate's well-formedness check), cross-surface consistency (17).


### HUMAN GATE — commissioned when Cartographer/Sage flag high-risk areas or before major releases

1. Tree test, card sort, first-click test, blind comprehension test (see §4). **The blind comprehension test is given a rubric (below) and positioned as the final ship-gate** — the check that, run between "IA decided" and "IA shipped," would have caught the Hall miss on round 1.

**How each check relates to existing gates:** The spine/ia-evidence/confidence gates verify **provenance** (is the claim cited?). Cartographer/Sage add the orthogonal **structural-quality** lane (is the IA well-formed, findable, comprehensible?). The completeness-gate is extended by Factor 6. The ad-hoc blind test is formalized and ordered last.


---


## 4. EYES-ONLY RESIDUE — what only humans can verify (bounded)

This is a first-class deliverable: the following **cannot** be safely downgraded to LOOK-tier simulation given 2024–2026 state of the art. The evidence that they can't is quantitative and recent.

| Residue item | Human method that owns it | Why simulation can't replace it (2024–2026 evidence) |
|---|---|---|
| **True grouping / category validity** | **Card sort** (open/closed/hybrid); success = standardized-category agreement ≥60% good, ≥80% target | LLM card sorts reach only moderate agreement with humans. MeasuringU (Sauro, Schiavone, Lewis, Jan 30 2024): ChatGPT-4 vs. **200 humans** on **40 Best Buy items** produced a **68% mean item-placement match** [measuringu](https://measuringu.com/comparing-chatgpt-to-card-sorting-results/) (runs 63/77/65%); against a **21% chance baseline** this gives **κ=.60, "bordering moderate and substantial agreement"** — on a *single* sort. The largest study — Kuric, Demcak & Krajcovic, *Card Sorting Simulator* (arXiv:2505.09478, May 2025), **28 studies / 1,399 participants** [arxiv](https://arxiv.org/pdf/2505.09478) — found **NMI ≈ 0.68** (best model Claude 0.73), [arxiv](https://arxiv.org/pdf/2505.09478) i.e. **~11–12 of 34 cards would need to move** to match humans, [arxiv](https://arxiv.org/pdf/2505.09478) degrading with more/harder cards. Authors' verdict: *"an augmented supplement to, rather than a replacement for, traditional card sorting."* [arxiv](https://arxiv.org/pdf/2505.09478) |
| **Findability of specific items** | **Tree test**; Albert & Tullis bands: 61–80% "good," 80–90% "very good," >90% "excellent"; directness ≥75% | MeasuringU (Sauro et al., Apr 2 2024): ChatGPT **found ~9–10/10 paths vs. ~51% human findability** [measuringu](https://measuringu.com/chatgpt4-tree-test/) — it *vastly outperforms* humans, so it *cannot* estimate human findability. Usable only as an **expert/power-user lower bound**: *"If ChatGPT can't find it, you probably have a problem."* [measuringu](https://measuringu.com/chatgpt4-tree-test/) The one validated screen use: ChatGPT's task-difficulty (SEQ) ratings correlated with human SEQ at **r=.62**. |
| **First-click correctness on real UI** | **First-click test** (correct first click → 87% success; Bailey & Wolfson) | Kuric et al., *What Would GPT Click* (arXiv:2605.18302, 2026; **12 studies / 3,431 participants**): [arxiv](https://arxiv.org/pdf/2605.18302) *"The hotspot clicked most frequently by GPT aligned with the human first choice in 71% of tasks. The average Rank-order Agreement was .16 (SD = .14)"* with *"statistically significant Distribution Difference in 53% of tasks"*; personas/chain-of-thought did not fix it. Verdict: *"inaccurate and unreliable as a predictor of human click behavior."* [arxiv](https://arxiv.org/pdf/2605.18302) |
| **Comprehension of copy/cards** (the Hall failure) | **Blind comprehension test** (rubric below) | Requires naive human interpretation; LLMs are sycophantic and *"one-dimensional… a flat approximation"* (NN/g, Rosala & Moran, Jun 21 2024). |
| **Attitude / satisfaction / real task efficiency** | Moderated usability test, SEQ, task-time | NN/g: *"Synthetic users cannot replace the depth and empathy gained from studying and speaking with real people… UX without real-user research isn't UX."* |

**Can any ASK factor be downgraded to LOOK today? No — with one narrow, honest exception.** The only validated simulation use is **task-difficulty prediction** in tree testing (ChatGPT SEQ correlated with human SEQ at **r=.62**, MeasuringU 2024) and using an LLM as an **expert-user lower-bound screen** ("if the model gets lost, humans will too"). These are *screens that reduce human-test load*, not replacements. Every primary source — including the two most AI-favorable (MeasuringU, Kuric et al.) — frames AI as **supplement, not replacement**. Kuric et al.'s explicit warning: *"Significant differences from mental models of real users also serve as a warning sign against potential attempts at leveraging AI as a fully automated replacement for real human feedback."* [measuringu](https://measuringu.com/chatgpt4-tree-test/)[arxiv](https://arxiv.org/pdf/2505.09478)

**Blind comprehension test — proposed rubric** (formalizing the existing ad-hoc practice; run as the final ship-gate): Show each decision card / key screen to a naive participant with no product context. Score (pass requires all): (1) **Identification** — can they say what the item/screen is? (2) **Action clarity** — can they state what each primary action does *before* clicking? (3) **Outcome prediction** — can they predict what happens after the primary action? (4) **No-jargon** — can they restate the label in their own words? (5) **No-truncation-loss** — is meaning intact at the rendered size? A single card failing (1)–(3) is the exact Hall round-1 failure and blocks ship.


---


## 5. WHAT DIDN'T SURVIVE / SOURCE DISAGREEMENTS

**IA folklore that fails verification:**

- **The three-click rule — DEAD.** NN/g: *"The big problem with the 3-click rule is that it has not been supported by data in any published studies to date… a study by Joshua Porter has debunked it; the study showed that user dropoff does not increase when the task involves more than 3 clicks, nor does satisfaction decrease."* Nielsen's own tests found users' *"ability to find products on an e-commerce site increased by 600 percent after the design was changed so that products were 4 clicks from the homepage instead of 3."* **Do not use click-count as a hard threshold** — measure scent, depth-to-core-task, and dead ends instead. [Nielsen Norman Group](https://www.nngroup.com/articles/3-click-rule/)
- **The "7±2 / magic menu-size cap" — DEAD as a hard IA threshold.** (Consistent with the UI-factors research's prior finding.) Miller's "7±2" is about short-term memory span, not menu design; Kiger/Miller's ~8-per-level is an *empirical optimum for specific tasks*, not a cap. Larson & Czerwinski showed **16- and 32-wide menus outperformed 8-wide** for ~500-item trees. Measure grouping and scent directly, not option count.
- **"Breadcrumbs fix bad IA" — FALSE.** NN/g: *"Breadcrumbs won't help a site answer users' questions or fix a hopelessly confused information architecture."* They're a secondary aid, not a structural remedy. [Nielsen Norman Group](https://www.nngroup.com/articles/breadcrumb-navigation-useful/)

**Genuine source disagreements (presented, not smoothed):**

1. **Breadth-vs-depth — menu studies vs. web studies.** Miller (1981)/Kiger (1984) → *moderate breadth (~8/level), limit depth*. Larson & Czerwinski (1998) on the *web* → *two levels beat three even at 16–32 wide*; depth hurt more than breadth. Miller & Remington (2004) reconcile: **label ambiguity (scent), not shape, dominates** — but the raw shape recommendations still conflict. **Verdict: prioritize scent; treat shape thresholds as contested.**
2. **First-click effect size.** Bailey & Wolfson (2006–2009): **87% vs. 46%**. MeasuringU replications: one found **70% vs. 24%**; another (5 sites, 21 tasks, 750 participants) found a **more modest ~13-point gap** (70% vs. 57%). The *direction* is robust and replicated; the *magnitude* is disputed. **Do not cite 87% as settled; cite the range.**
3. **Do LLM click tests predict live-site clicks?** Optimal Workshop's analysis of millions of responses affirms the first-click→success link; MeasuringU cautions that *image-based* click tests may not correspond to *live-site* first clicks, and (2026) that LLM click prediction is unreliable. **Verdict: the human first-click principle holds; the LLM simulation of it does not.**
4. **Synthetic users — vendor claims vs. researchers.** Vendor marketing claims LLM "testers" catch ~97–98% of usability issues (misapplying the Nielsen–Landauer n=10 formula to synthetic agents); NN/g and the academic HCI literature flatly reject this. **Verdict: vendor claims are unsupported; treat synthetic-user "coverage" numbers as marketing, not evidence.** [Uxia](https://www.uxia.app/blog/using-nn-g-research-to-achieve-98-usability-issue-detection-through-ai-powered-testers)

**Weak-evidence flags:** Card-sort/tree-test **agreement and success thresholds (60%/80%; 61–80%/80–90%/>90%)** trace to tool-vendor documentation (Optimal Workshop, UXtweak, Lyssna) citing Albert & Tullis (*Measuring the User Experience*) — credible but partly practitioner-tier. Notably, Albert & Tullis's review of tree-testing studies found a **median task success rate of 62% (interquartile range 37–83%)**, underscoring how context-dependent these numbers are; **NN/g explicitly cautions that "the best frame of reference is your own previous data,"** so treat the bands as calibration guides, not universal pass/fail lines. The **trunk test** is a practitioner heuristic (Krug), not an empirically validated instrument. Both arXiv studies (40, 41), while large and rigorous, are authored by researchers affiliated with UXtweak (a commercial UX-research vendor) and rely on proprietary datasets — a conflict-of-interest and reproducibility caveat, though their conclusions align with the independent NN/g and MeasuringU findings. Any factor whose only threshold is vendor-doc-sourced is marked accordingly above. [The Product Picnic](https://productpicnic.beehiiv.com/authors/a2d9e5f9-27c5-44a5-ab3c-353314c220a1)[Lyssna](https://www.lyssna.com/guides/tree-testing/analyzing-tree-testing-results/)


---


## 6. SOURCES

1. Pirolli, P. & Card, S. — *Information Foraging*, Psychological Review 106 (1999). act-r.psy.cmu.edu/…/280uir-1999-05-pirolli.pdf
2. NN/g — *Information Foraging: A Theory of How People Navigate on the Web.* nngroup.com/articles/information-foraging/
3. NN/g — *Information Scent: How Users Decide Where to Go Next.* nngroup.com/articles/information-scent/
4. NN/g — *3 Common IA Mistakes (Due to Low Information Scent).* nngroup.com/articles/3-ia-mistakes/
5. NN/g — *Better Link Labels: 4Ss for Encouraging Clicks.* nngroup.com/articles/better-link-labels/
6. NN/g — *Writing Hyperlinks: Salient, Descriptive, Start with Keyword.* nngroup.com/articles/writing-links/
7. NN/g — *"Learn More" Links: You Can Do Better.* nngroup.com/articles/learn-more-links/
8. Rosenfeld, Morville & Arango — *Information Architecture for the Web and Beyond*, 4th ed. (2015).
9. Morville — *The Polar Bear Book*, intertwingled.org/the-polar-bear-book/
10. Covert, A. — *How to Make Sense of Any Mess* (2014). abbycovert.com/make-sense/
11. NN/g — *10 Usability Heuristics for User Interface Design.* nngroup.com/articles/ten-usability-heuristics/
12. NN/g — *Maintain Consistency and Adhere to Standards (Heuristic #4).* nngroup.com/articles/consistency-and-standards/
13. NN/g — *3-Click Rule for Navigation Is False.* nngroup.com/articles/3-click-rule/
14. Miller, D.P. — *The Depth/Breadth Tradeoff in Hierarchical Computer Menus* (1981).
15. Kiger, J.I. — *The Depth/Breadth Trade-off in the Design of Menu-Driven User Interfaces*, Int. J. Man-Machine Studies 20 (1984).
16. Larson, K. & Czerwinski, M. — *Web Page Design: Implications of Memory, Structure and Scent for Information Retrieval*, CHI '98.
17. Miller, C.S. & Remington, R.W. — *Modeling Information Navigation: Implications for Information Architecture*, HCI 19 (2004). facsrv.cdm.depaul.edu/~cmiller/hci460/materials/hci2004.pdf
18. Bailey, R.W. & Wolfson, C. — *FirstClick Usability Testing* (2006–2009). webusability.com/firstclick-usability-testing/
19. MeasuringU — *Do Click Tests Predict Live Site Clicks?* measuringu.com/do-click-tests-predict-live-site-clicks/
20. NN/g — *Breadcrumbs: 11 Design Guidelines for Desktop and Mobile.* nngroup.com/articles/breadcrumbs/
21. NN/g — *Breadcrumb Navigation Increasingly Useful.* nngroup.com/articles/breadcrumb-navigation-useful/
22. NN/g — *Navigation: You Are Here.* nngroup.com/articles/navigation-you-are-here/
23. NN/g — *Polyhierarchies Improve Findability for Ambiguous IA Categories.* nngroup.com/articles/polyhierarchy/
24. Krug, S. — *Don't Make Me Think, Revisited* (2014) — the Trunk Test.
25. NN/g — *Search Is Not Enough: Synergy Between Navigation and Search.* nngroup.com/articles/search-not-enough/
26. NN/g — *3 Guidelines for Search Engine "No Results" Pages.* nngroup.com/articles/search-no-results-serp/
27. NN/g — *Designing Empty States in Complex Applications.* nngroup.com/articles/empty-state-interface-design/
28. NN/g — *Error-Message Guidelines* & *Error Messages Scoring Rubric.* nngroup.com/articles/error-message-guidelines/
29. NN/g — *Improving the Dreaded 404 Error Message.* nngroup.com/articles/improving-dreaded-404-error-message/
30. GOV.UK Design System — *Step by Step Navigation*; *How we document components* (jargon). design-system.service.gov.uk
31. GOV.UK — *Designing new navigation elements for GOV.UK* (accordion URL/breadcrumb). designnotes.blog.gov.uk
32. Shopify Polaris — *Information Architecture.* polaris-react.shopify.com/foundations/information-architecture
33. Shopify — *Navigation* (app design guidelines). shopify.dev/docs/apps/design/navigation
34. Optimal Workshop / UXtweak / UserTesting — card-sort agreement-score documentation (≥60%/≥80%).
35. NN/g — *Tree Testing Part 2: Interpreting the Results.* nngroup.com/articles/interpreting-tree-test-results/
36. Lyssna — *Tree Testing Guide* (Albert & Tullis success bands). lyssna.com/guides/tree-testing/
37. Spencer, D. — *Tree Testing for Websites* (treetesting.atlassian.net) & card-sorting literature.
38. MeasuringU — Sauro, Schiavone & Lewis, *Comparing ChatGPT to Card Sorting Results* (Jan 30 2024). measuringu.com/comparing-chatgpt-to-card-sorting-results/
39. MeasuringU — Sauro, Schiavone & Lewis, *Using ChatGPT in Tree Testing: Experimental Results* (Apr 2 2024). measuringu.com/chatgpt4-tree-test/
40. Kuric, E., Demcak, P. & Krajcovic, M. — *Card Sorting Simulator* (arXiv:2505.09478, May 2025). arxiv.org/abs/2505.09478
41. Kuric, E., Demcak, P. & Krajcovic, M. — *What Would GPT Click* (arXiv:2605.18302, 2026). arxiv.org/pdf/2605.18302
42. NN/g — Rosala, M. & Moran, K., *Synthetic Users: If, When, and How to Use AI-Generated "Research"* (Jun 21 2024). nngroup.com/articles/synthetic-users/
43. Samsonov, P. — *No, AI User Research is Not "Better Than Nothing"* (UX Magazine, May 30 2024).
44. NN/g — *Menu-Design Checklist: 17 UX Guidelines* & *Local Navigation Is a Valuable Orientation and Wayfinding Aid.* nngroup.com/articles/menu-design/
