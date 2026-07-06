# Operational Factor Taxonomy for "Superb" UI — Machine-Actionable Audit Specification for Guild's Mage Agent

*Scope: the rendered visual surface only (pixels, geometry, computed styles, screenshots). Mental-model / IA factors are out of scope (covered in ui-mental-model-research.md). Baseline already shipped in Guild is extended, not re-derived. Current date of research: July 2026; design-system guidance dates noted where they drift.*

## 1. VERDICT

The complete factor space for "what makes rendered pixels superb" decomposes into three concentric shells. The **inner shell is fully deterministic (MEASURE-tier)**: contrast, target size, overflow/reflow, type-ramp discipline, spacing-scale conformance, and — critically — the whole family of *geometric* checks (sibling overlap, row-height rhythm, content-start alignment, radius/shadow/border vocabulary size). Guild already lives here and expanded it after Round 3. The **middle shell is model-judgment (LOOK-tier)**: visual hierarchy / squint-test saliency, Gestalt grouping legibility, affordance honesty (does-it-look-clickable), state-completeness plausibility, microcopy quality, and dark-mode parity — each has a *partial* machine proxy that narrows but cannot fully close the question, so a vision model scores it against stated criteria. The **outer shell is human-only (ASK-tier)**: blind comprehension, emotional/reflective resonance, trust felt over time, and whether motion *actually* aids understanding.

The single highest-leverage gap after contrast+geometry is **visual hierarchy / saliency ordering** — the "squint test." Round 3's geometry failures were a *symptom* of this larger gap: a UI can pass every geometric rhythm check and still fail to make the primary action pop, or make three sibling panels read as equally important when one should dominate. This is measurable to a first approximation today (blur the screenshot, threshold luminance/saturation clusters, check that the largest high-salience blob coincides with the semantic primary action), and it is the next embarrassment waiting to happen because it is exactly the thing an owner "sees instantly" that no contrast or geometry gate looks at. The second-highest gap is **affordance honesty** (clickable-looking non-buttons and unstyled real buttons), partially measurable by cross-referencing computed cursor/role/tabindex against visual styling.

## 2. RANKED TAXONOMY

Scoring: **Impact** (effect on perceived quality, 1–5) × **Checkability** (how completely a machine can verify, 1–5). Score = I×C (max 25). Grouped so related factors stay together; leverage noted per factor. All factors generalize across surface types (dashboard, form, marketing, mobile) unless flagged **surface-specific**.

---

### F1. Visual hierarchy & saliency (squint/blur test) — Impact 5 × Check 3 = 15 — **LOOK** (partial MEASURE)
**(a) Evidence.** The squint test is a long-standing designer heuristic; Polypane documents it operationally: *"The squint test is a quick way to check if your page is still on the right track because it hides those details and lets you focus on the larger patterns... Is the primary focus of the page clear? ... When squinting, can you still detect whether a link is clickable?"* (Polypane, "Debug your visual hierarchy with the squint test"). NN/g frames hierarchy as maximizing signal: *"Maximize the 'signal'... Minimize the 'noise'—elements with low informational value"* (NN/g, "Aesthetic and Minimalist Design," Kate Moran). Refactoring UI (Wathan/Schoger) frames hierarchy through three levers — size, weight, color — and advises designing in greyscale first. **Weak-evidence flag:** conversion multipliers ("larger CTAs increase clicks up to 300%") come from a marketing blog (DeveloperUX) — illustrative only, not load-bearing.
**(b) Machine proxy.** Render screenshot → Gaussian blur (σ ≈ 8–16px at 1× density) → compute saliency map (luminance-contrast + saturation clustering). Identify the top-1 high-salience blob; check its bounding box overlaps the DOM element that is semantically the primary action (largest button, `type=submit`, aria-primary, or the single filled/high-contrast button). Also cluster computed `font-size × font-weight × color-contrast` across text nodes — a healthy page shows 3–5 tiers, not a flat 1 or a chaotic 10+.
**(c) Thresholds.** No agreed numeric threshold in literature for saliency overlap; Refactoring UI implies "≤ ~3 emphasis levels." Whole-page tier count 3–5 is a heuristic, not a spec'd number — pass/flag only.
**(d) Tier.** LOOK — the blur-and-locate computation runs deterministically, but confirming the located blob *should* be primary requires model judgment about intent.
**(e) Failure mode.** Three dashboard sidebar panels rendered at identical size/weight/background so the blurred screenshot shows three equal-salience blobs — the user cannot tell which panel is primary. (Generalizes the Round 3 "equal-looking sidebars" complaint into a saliency check.)

---

### F2. Geometric layout integrity (overlap, rhythm, alignment, nesting) — Impact 5 × Check 5 = 25 — **MEASURE**
**(a) Evidence.** Round 3 territory Guild already shipped; design-literature backing is Gestalt "good continuation" and alignment discipline (Refactoring UI: consistent alignment, "avoid ambiguous spacing"). The DEV Community "incoherence" article (kiwibreaksme) — **weak evidence, blog** — names the failure well: *"a human designer would never make all of them on the same screen. A designer picks one corner style, one accent, one icon set, one light source — and repeats those decisions everywhere."*
**(b) Machine proxy.** (i) Sibling-rect overlap: for elements sharing a parent, flag any `getBoundingClientRect` intersection area > 0 that is not an intentional overlay. (ii) Row-height rhythm: rhythm outlier = any list/nav row whose height deviates >20% from the modal (most common) row height in that list. (iii) Content-start alignment: within a row of sibling panes, flag when left content-edge x-positions differ by >4px. (iv) Border-nesting depth: flag any element with ≥3 nested ancestors each carrying a visible border/background.
**(c) Thresholds.** Overlap >0px unintended = fail (calibration: 6px toggle/panel overlap). Rhythm >20% deviation = flag (calibration: 54px row in 40px rhythm = 35% over → fail). Alignment >4px content-start delta = flag (calibration: 107/91/105px spread = 16px → fail). Nesting depth ≥3 = flag. These are Guild-internal engineering conventions — **no external literature threshold exists**; stated as such.
**(d) Tier.** MEASURE — fully deterministic, gateable.
**(e) Failure mode.** Collapse toggle overlapping a panel corner by 6px; nav row wrapping to 54px in a 40px rhythm; content-start lines ragged at 107/91/105px. (The literal Round 3 failures.)

---

### F3. Alpha-composited contrast (WCAG 2.2 AA, 1.4.3 / 1.4.11) — Impact 5 × Check 5 = 25 — **MEASURE**
**(a) Evidence.** WCAG 2.2 SC 1.4.3 requires 4.5:1 for normal text, 3:1 for large text (≥18pt/24px, or 14pt/18.66px bold); SC 1.4.11 Non-text Contrast requires 3:1 for UI components and graphical objects (W3C WCAG 2.2 Understanding docs, current spec).
**(b) Machine proxy.** Already shipped: alpha-composite rgba stacks against effective background; for gradients walk stops and evaluate the worst-case stop. Compute luminance ratio per WCAG formula.
**(c) Thresholds.** 4.5:1 normal text, 3:1 large text and non-text/UI components (WCAG 2.2 AA). AAA is 7:1 / 4.5:1 (advise-only).
**(d) Tier.** MEASURE.
**(e) Failure mode.** rgba(0,0,0,0.5) label treated as opaque black → reported 21:1 when true composited ratio over a mid-gray panel is 2.9:1 (fail). (The Round 1 bug.)

---

### F4. Target size (WCAG 2.5.8 AA / 2.5.5 AAA) — Impact 4 × Check 5 = 20 — **MEASURE**
**(a) Evidence.** W3C WCAG 2.2 SC 2.5.8: *"The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except where: Spacing: Undersized targets... a 24 CSS pixel diameter circle... do not intersect... Inline... Essential..."* AAA SC 2.5.5 requires 44×44. Apple HIG recommends 44×44pt; Material recommends 48×48dp. (Note: WCAG issue #1831 explicitly disputes the 24px basis — see §5.)
**(b) Machine proxy.** For each interactive element (a, button, input, [role=button], [onclick]): measure hit-rect incl. padding; flag < 24×24 unless it satisfies the spacing exception (24px-diameter circles centered on bounding boxes don't intersect) or is inline text.
**(c) Thresholds.** 24×24 CSS px = AA fail below (W3C). 44×44 (Apple) / 48×48 (Material) = advise for touch primary actions.
**(d) Tier.** MEASURE.
**(e) Failure mode.** 16×16 icon-only close button with 2px spacing from an adjacent pagination link → fails both size and spacing.

---

### F5. Reflow / responsiveness across breakpoints incl. mid-bands (WCAG 1.4.10) — Impact 5 × Check 4 = 20 — **MEASURE**
**(a) Evidence.** W3C WCAG 2.1/2.2 SC 1.4.10 Reflow: *"Content can be presented without loss of information or functionality, and without requiring scrolling in two dimensions for: Vertical scrolling content at a width equivalent to 320 CSS pixels... Except for parts of the content which require two-dimensional layout for usage or meaning."* Exceptions: maps, data tables, diagrams.
**(b) Machine proxy.** Sweep viewport widths (320, 360, 768, the awkward 900–1200px band in ~50px steps, plus 1440); at each, detect `scrollWidth > clientWidth` (horizontal overflow), clipped content, and sibling overlaps that appear only at that width. "Reflow not truncate": flag `overflow:hidden` + `text-overflow:ellipsis` on containers that lose content at narrow widths.
**(c) Thresholds.** No horizontal scroll at 320px = WCAG fail below. The 900–1200px audit band is a Guild convention (Round 2), not a WCAG number — stated as such.
**(d) Tier.** MEASURE.
**(e) Failure mode.** Layout breaks at ~1100px — a fixed 300px sidebar + `min-width:820px` main column exceed the viewport and collide. (The Round 2 failure.)

---

### F6. Typography craft — line length, line-height, type scale — Impact 4 × Check 4 = 16 — **MEASURE (metrics) + LOOK (rag/widow)**
**(a) Evidence.** Butterick, *Practical Typography* ("Summary of key rules," confirmed verbatim): *"Point size should be 10–12 points in printed documents, 15-25 pixels on the web. Line spacing should be 120–145% of the point size. The average line length should be 45–90 characters (including spaces)."* Bringhurst (quoted): *"Anything from 45–75 characters is widely regarded as a satisfactory length of line... The 66-character line... is widely regarded as ideal... For multiple column work, a better average is 40–50 characters."* Modular-scale ratios (Major Third 1.25, Perfect Fourth 1.333) are standard; Material uses 1.25.
**(b) Machine proxy.** Line length: for body text blocks, measure rendered `width / average glyph advance` → chars-per-line. Line-height: computed `line-height / font-size`. Type scale: collect distinct `font-size` values; test whether they fit a single geometric ratio within tolerance; flag whole-pixel violations and scale outliers. Widow/orphan and rag: rendered line-box inspection (LOOK).
**(c) Thresholds.** Line length 45–90 chars (Butterick) vs. 45–75 (Bringhurst) — **sources disagree; see §5**; recommend 45–75 for single-column body. Line-height 1.2–1.45 body (Butterick 120–145%). Butterick web body 15–25px.
**(d) Tier.** MEASURE for chars-per-line, line-height, scale conformance; LOOK for rag/widows/orphans.
**(e) Failure mode.** Body paragraph at 140 chars/line on a wide container with no max-width (eye-tracking fatigue); or an H2 at 27px fitting no ratio between 24px body-large and 32px H1.

---

### F7. Spacing & proximity (Gestalt grouping) — Impact 4 × Check 4 = 16 — **MEASURE**
**(a) Evidence.** Gestalt proximity, operationalized by Refactoring UI's "avoid ambiguous spacing," quoted via DEV Community (kiwibreaksme, **weak/blog** but quoting Refactoring UI): *"the space around a group must be clearly larger than the space within it... When everything is evenly spaced, the eye can't tell what belongs together."* Spacing-scale (4/8/12/16/24/32/48) is Refactoring UI / 8-point grid canon.
**(b) Machine proxy.** For a group of sibling items, measure intra-group gaps vs. gap to the next group; flag when intra ≥ inter (ambiguous grouping). Spacing-scale conformance: flag margins/paddings off the 4px base. Padding symmetry: flag containers whose opposing paddings differ without cause.
**(c) Thresholds.** Rule of thumb (Refactoring UI): inter-group gap measurably larger than intra — common operationalization inter ≥ ~2× intra. **No peer-reviewed numeric threshold** — heuristic, stated as such.
**(d) Tier.** MEASURE.
**(e) Failure mode.** A form where label-to-input gap (16px) equals input-to-next-label gap (16px), so fields don't visually bind to their labels.

---

### F8. Alignment & grids (distinct edge count, optical alignment) — Impact 4 × Check 4 = 16 — **MEASURE (edges) + LOOK (optical)**
**(a) Evidence.** Refactoring UI on alignment discipline; Gestalt continuity. Optical vs. mathematical alignment (icons, quote marks, arrowheads) is standard typographic craft.
**(b) Machine proxy.** Count distinct left-edge x-positions among primary content elements per region; a clean region collapses to a small set. Baseline rhythm: check text baselines land on a consistent grid. Optical alignment (icon mathematically centered but looking off) is LOOK.
**(c) Thresholds.** No literature number for "max distinct edges"; heuristic ≤ ~3–4 alignment lines per coherent region. Flag-only.
**(d) Tier.** MEASURE for edge counting/baseline; LOOK for optical adjustments.
**(e) Failure mode.** A card with title at x=24, body at x=24, but a metadata row at x=27 (accidental 3px indent), producing a ragged left edge.

---

### F9. Color systems — semantic roles, state derivation, neutral temperature, dark-mode parity — Impact 4 × Check 3 = 12 — **MEASURE (drift/temperature) + LOOK (harmony/parity)**
**(a) Evidence.** Refactoring UI: pure grays look lifeless, add saturation (cool UI blue tint e.g. `#64748b`, warm UI yellow/brown tint e.g. `#78716c`); derive lighter/darker by rotating hue toward 60° / toward 0°/240°. IBM Carbon and Material define semantic color roles/tokens. Token-drift (stale hex vs. token) already shipped in Guild.
**(b) Machine proxy.** Neutral temperature: convert near-gray colors to HSL; flag mixed hue signs (some blue-tinted, some yellow-tinted grays) on one surface = inconsistent temperature. Semantic coverage: check distinct tokens for success/warning/error/info. Dark-mode parity: diff element inventory light vs. dark; flag elements that lose contrast or disappear. Hue harmony = LOOK.
**(c) Thresholds.** No agreed harmony threshold. Temperature consistency = binary flag (mixed signs). "No agreed threshold" for harmony.
**(d) Tier.** MEASURE for temperature-sign consistency and dark-mode contrast diff; LOOK for hue harmony.
**(e) Failure mode.** Neutrals mix `#64748b` (blue-gray) headers with `#78716c` (warm-gray) borders on the same surface — a subtly "off," incoherent palette.

---

### F10. Consistency & craft polish — radius/shadow/border/icon vocabulary size — Impact 4 × Check 5 = 20 — **MEASURE**
**(a) Evidence.** Refactoring UI on shadows: *"add a vertical offset. It looks a lot more natural because it simulates a light source shining down from above."* The "one choice per axis" coherence rule (DEV/kiwibreaksme, **weak/blog** but quoting Refactoring UI/Material/HIG): *"A designer picks one corner style, one accent, one icon set, one light source — and repeats those decisions everywhere."* Fluent 2: *"Consistent shadow direction conveys a perceived light source."*
**(b) Machine proxy.** Count distinct non-zero `border-radius` values (flag > ~3–4). Shadow coherence: parse all `box-shadow`; flag inconsistent x/y offset *direction* (multiple implied light sources). Border-weight vocabulary: count distinct border widths. Icon optical sizing: compare rendered icon bounding boxes across a toolbar; flag >~15% size variance among peer icons.
**(c) Thresholds.** No literature hard number; Guild convention ≤3 corner radii, single shadow light direction, ≤2–3 border weights. Engineering convention.
**(d) Tier.** MEASURE.
**(e) Failure mode.** A page mixing 4/6/8/12px radii on peer cards, plus shadows cast down-right on some and straight-down on others (two light sources) — reading as "templated/assembled from parts."

---

### F11. Affordance & signifiers (two-way clickability audit) — Impact 5 × Check 3 = 15 — **LOOK (partial MEASURE)**
**(a) Evidence.** Norman, *Design of Everyday Things* (rev. 2013): affordances are action possibilities, signifiers communicate where/how. *"Affordances determine what actions are possible. Signifiers communicate where the action should take place. We need both."* Refactoring UI: raised/shadowed elements read as clickable ("the closer something is to the user... the more interactive it appears").
**(b) Machine proxy.** Two-way cross-reference: (i) Looks-clickable-but-isn't: elements with button-like styling (border-radius + fill + padding, or `cursor:pointer`, or underline+color) that have no click handler, `href`, or interactive role. (ii) Clickable-but-doesn't-look-it: elements with click handlers / `role=button` / `href` lacking any signifier (no cursor:pointer, no hover style, no distinguishing color/underline/border).
**(c) Thresholds.** Binary handler/signifier mismatch — no numeric threshold; confirming styling "reads as" clickable is LOOK.
**(d) Tier.** LOOK — the handler/role/cursor cross-reference is deterministic, but judging whether styling genuinely signals interactivity needs vision.
**(e) Failure mode.** A `<div>` styled as a filled blue rounded rectangle ("Save") with no handler (dead button); or a real `<a>` "Learn more" rendered as plain body text with no color/underline (invisible link).

---

### F12. State completeness matrix (hover/focus/active/disabled/loading/empty/error/skeleton) — Impact 4 × Check 3 = 12 — **LOOK (partial MEASURE)**
**(a) Evidence.** WCAG 2.4.7 Focus Visible / 2.4.11 Focus Appearance (states must be perceivable). NN/g empty-state and error-message guidance (see F13/F16). State coverage as component-completeness discipline is design-system canon (Carbon, Polaris, Material component specs each enumerate states).
**(b) Machine proxy.** For each interactive component, probe computed styles across pseudo-states (`:hover`, `:focus-visible`, `:active`, `:disabled`) — flag when a state produces *no* computed-style delta. Detect presence of skeleton/empty/error components for data-driven regions. Full matrix coverage requires exercising the app = LOOK/ASK.
**(c) Thresholds.** Focus state must produce a visible change (WCAG 2.4.7). Others: pass/flag per cell, no numeric threshold.
**(d) Tier.** LOOK — focus/hover deltas are MEASURE; empty/error/loading coverage needs app exercise + judgment.
**(e) Failure mode.** A primary button with identical `:hover` and default styling (no feedback), and a data table with no defined empty state (blank void at zero rows).

---

### F13. Accessibility beyond contrast — focus order, focus indicator, keyboard reach, landmarks — Impact 5 × Check 4 = 20 — **MEASURE (mostly) + ASK (SR narrative)**
**(a) Evidence.** WCAG 2.2 SC Focus Appearance: *"an area of the focus indicator... is at least as large as the area of a 1 CSS pixel thick perimeter of the unfocused component, or has an area of at least 4 CSS pixels along the shortest side... and has a contrast ratio of at least 3:1 between the... focused and unfocused states."* On 2.4.11 Focus Not Obscured, TPGi/Vispero note: *"This SC can be entirely tested by automation, and is the only WCAG 2.2 criterion that can."*
**(b) Machine proxy.** Focus order vs. visual order: compare DOM/tabindex sequence to spatial reading order (top-left→bottom-right); flag divergences. Focus indicator: verify a visible `:focus-visible` style delta meeting 3:1 / size test. Keyboard reachability: flag interactive elements with `tabindex=-1` or click-only handlers. Landmarks/headings: check `<main>/<nav>/<header>`, single `<h1>`, no skipped heading levels. Focus-not-obscured: check focused element isn't fully covered by sticky headers/overlays.
**(c) Thresholds.** Focus indicator 3:1 contrast + size test (WCAG 2.2). Heading order: no skipped levels. Screen-reader *narrative coherence* = ASK.
**(d) Tier.** MEASURE for focus order/indicator/landmarks/obscuring; ASK for whether the SR narrative "makes sense."
**(e) Failure mode.** A modal whose close button is `tabindex=-1` (keyboard trap); or a focus ring removed via `outline:none` with no replacement (0:1 delta).

---

### F14. Density & information design — data-ink, Hick's Law choice count — Impact 3 × Check 3 = 9 — **LOOK (partial MEASURE)**
**(a) Evidence.** Tufte, *Visual Display of Quantitative Information*: data-ink ratio = *"the proportion of a graphic's ink devoted to the non-redundant display of data-information"*; maximize it, *"erase non-data-ink... erase redundant data-ink."* Hick's Law: *RT = a + b·log₂(n+1)* — decision time grows logarithmically with number of equally-probable choices (Hick 1952, Hyman 1953). **surface-specific:** data-ink applies mainly to charts/dashboards.
**(b) Machine proxy.** Choice count: count simultaneous top-level actionable items in a menu/toolbar; flag very high counts. Data-ink (SVG charts only): ratio of data-mark pixels to total chart-region pixels (gridlines/backgrounds/borders = non-data-ink). Progressive disclosure: presence of accordions/"show more" for dense regions.
**(c) Thresholds.** **No agreed data-ink threshold** (Tufte said "within reason"; Inbar 2007 found users often *prefer* lower data-ink/"chartjunk"). Hick's Law has no universal max-n. "No agreed threshold."
**(d) Tier.** LOOK — counts are MEASURE, but "is this too dense" is judgment.
**(e) Failure mode.** A toolbar exposing 22 equally-weighted icon buttons with no grouping/overflow (choice overload); a bar chart where gridlines and 3-D bevels outweigh the bars.

---

### F15. Motion — duration/easing norms, purpose, interruptibility, reduced-motion — Impact 3 × Check 4 = 12 — **MEASURE (tokens/reduced-motion) + LOOK (purpose)**
**(a) Evidence.** **Named numeric tokens (sources disagree — see §5):** Material Design 3 duration scale (m3.material.io, `md-sys-motion`): short1=50, short2=100, short3=150, short4=200, medium1=250, medium2=300, medium3=350, medium4=400, long1=450, long2=500, long3=550, long4=600, extra-long1=700ms (scale continues to extra-long4=1000ms); M3 standard **and** emphasized easing = `cubic-bezier(0.2, 0, 0, 1)`. IBM Carbon (carbondesignsystem.com, "Last updated 03 July 2026"): fast-01=70ms, fast-02=110ms, moderate-01=150ms, moderate-02=240ms, slow-01=400ms, slow-02=700ms; productive standard easing `cubic-bezier(0.2,0,0.38,0.9)`; Carbon checklist: *"Do micro-interactions fall within a static duration ranging from 90–120 ms?"* NN/g (Laubheimer, "Executing UX Animations," 2020, confirmed verbatim): *"At 500ms, animations start to feel like a real drag for users... In most cases, a range of 100–400 ms is appropriate, with 400ms being a very slow animation, to be used only for big movements across large screens."* Apple HIG: no ms numbers — *"Prefer quick, precise animations"* and *"Make motion optional... when the Reduce Motion accessibility setting is on, be sure to minimize or eliminate animations."*
**(b) Machine proxy.** Parse `transition-duration`/`animation-duration`: flag >500ms for standard UI transitions, warn >400ms. Check easing is not `linear` for spatial moves. Reduced-motion: verify a `@media (prefers-reduced-motion: reduce)` block exists and actually neutralizes transforms/animations (partly shipped). Interruptibility/purpose = LOOK.
**(c) Thresholds.** Warn >400ms, fail >500ms for standard transitions (NN/g). Micro-interactions 90–120ms (Carbon). `prefers-reduced-motion` block present = pass/fail. **Cross-system numbers disagree — §5.**
**(d) Tier.** MEASURE for duration/easing/reduced-motion presence; LOOK for whether motion serves a purpose or harms.
**(e) Failure mode.** A 900ms ease-in-out modal entrance that feels sluggish; or a parallax/spin animation with no `prefers-reduced-motion` fallback (nausea risk per Apple's Reduced-Motion criteria).

---

### F16. Microcopy & content shape — labels, errors, empty states — Impact 4 × Check 2 = 8 — **LOOK**
**(a) Evidence.** NN/g Error-Message Guidelines (via Nielsen Heuristic #9): *"Error messages should be expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution."* NN/g Empty-State guidance: *"Do not default to totally empty states... use the empty state to provide help cues. Tell the user what could be displayed, and how to populate the area... Provide direct pathways (i.e., links)."* IBM Carbon empty-state pattern: state what isn't there, then give a next step.
**(b) Machine proxy.** Detect presence/absence: does an error region contain actionable text + a recovery affordance? Does an empty container have >0 guidance text + a CTA vs. being truly blank? Front-loading: check labels/headings aren't excessively long. *Quality* of wording = LOOK (vision/LLM judgment against NN/g criteria).
**(c) Thresholds.** No numeric threshold; presence-of-guidance is binary, wording quality is judged.
**(d) Tier.** LOOK — presence is MEASURE-ish, "is this error message good" is model judgment.
**(e) Failure mode.** An empty projects list showing only gray "No data" (NN/g's explicit anti-pattern); an error reading "Error 0x0007" with no plain-language cause or fix.

---

### F17. Perceived performance — response thresholds, skeletons, optimistic UI — Impact 4 × Check 3 = 12 — **MEASURE (indicator logic) + ASK (felt speed)**
**(a) Evidence.** Nielsen response-time limits (NN/g, "Response Time Limits"): *"0.1 second... feeling that the system is reacting instantaneously... 1.0 second... limit for the user's flow of thought to stay uninterrupted... 10 seconds... limit for keeping the user's attention focused."* NN/g skeleton screens: *"reduces the perception of a long loading time by providing clues for how the page will ultimately look."* NN/g: percent-done indicators for >10s. Mejtoft et al. (ECCE'18, peer-reviewed) found skeleton screens scored higher on perceived speed than spinners.
**(b) Machine proxy.** Static analysis: check async actions render a state change <0.1s (optimistic/immediate feedback); operations expected >1s show a loading indicator; >10s show percent-done + cancel. Detect skeleton vs. spinner components. Felt speed = partly runtime-measurable, partly ASK.
**(c) Thresholds.** 0.1s / 1s / 10s (Nielsen). >10s requires percent-done + cancel (NN/g).
**(d) Tier.** MEASURE for indicator-presence logic; ASK for genuinely perceived speed.
**(e) Failure mode.** A "Save" button showing no feedback for 2.5s then jumping to done (violates the 1s flow limit with no indicator); a 15s export with an indeterminate spinner and no cancel.

---

### F18. Aesthetic-usability effect & emotional design (Norman tiers) — Impact 3 × Check 1 = 3 — **ASK**
**(a) Evidence.** Kurosu & Kashimura (1995), "Apparent Usability vs. Inherent Usability" (CHI'95 Companion): 26 ATM layout variations rated by 252 subjects (156 design students, 96 psych students); *"Relatively high correlation (0.589) was obtained between these two scales which suggests that the apparent usability is somewhat related to the aesthetic aspect of the layout pattern"* (inter-rater agreement 0.679 apparent usability, 0.783 beauty). Tractinsky, Katz & Ikar (2000), "What is beautiful is usable" (*Interacting with Computers* 13(2):127–145) replicated it: *"Pre-experimental measures indicate strong correlations between system's perceived aesthetics and perceived usability. Post-experimental measures indicated that the strong correlation remained intact"* — reported that the strong correlation held without publishing a single competing coefficient, so **r = 0.589 (Kurosu & Kashimura) is the one defensible anchor number**; discard the unsourced "r > 0.9" that circulates secondhand. Norman, *Emotional Design*: three levels — visceral (appearance), behavioral (use), reflective (meaning/identity). NN/g: the effect *"can mask usability problems"* and has limits (fails for major usability breakdowns).
**(b) Machine proxy.** **No direct machine proxy for the causal effect or reflective resonance.** The proxies for F1/F6/F7/F10 (hierarchy, type, spacing, coherence) are the measurable *inputs* that tend to raise visceral appeal, but the effect itself is measured only by human perception.
**(c) Thresholds.** No pass/fail threshold; the empirical correlation r ≈ 0.589 quantifies the *phenomenon*, not a gate.
**(d) Tier.** ASK.
**(e) Failure mode.** A functionally-correct dashboard that testers rate "hard to use" purely because it looks unpolished — invisible to every deterministic gate.

---

### F19. Trust & honesty — provenance, indicator honesty, dark-pattern avoidance — Impact 4 × Check 3 = 12 — **MEASURE (checklist) + LOOK/ASK (intent)**
**(a) Evidence.** Brignull (2010, *Deceptive Patterns* 2023) original 12-pattern taxonomy: trick questions, sneak into basket, roach motel, privacy zuckering, confirmshaming, disguised ads, forced continuity, hidden costs, bait and switch, misdirection, price comparison prevention, friend spam. Brignull's inflection point: *"A countdown timer on a flash sale that is actually a flash sale is persuasive design. The same timer with a fake reset is a Misdirection-class dark pattern."*
**(b) Machine proxy.** Checkable subset: confirmshaming (detect guilt-laden decline text via LLM), asymmetric choice styling (accept high-contrast/large vs. decline hidden/low-contrast — measurable style delta), preselected opt-in checkboxes, hidden costs appearing only at final step, roach-motel (signup 1 click vs. cancel buried). Fake-urgency countdowns that reset = requires runtime observation.
**(c) Thresholds.** Style-asymmetry between paired choices = flag (measurable contrast/size delta); no canonical number. Intent (is this timer fake) = ASK.
**(d) Tier.** MEASURE for style-asymmetry and preselected-opt-in; LOOK/ASK for intent-dependent patterns.
**(e) Failure mode.** A cookie banner with a bright filled "Accept All" and a nearly-invisible low-contrast "Reject" link (asymmetric-choice dark pattern, measurable).

---

**Ranked leverage summary (score, tier):** F2 Geometry 25 MEASURE · F3 Contrast 25 MEASURE · F4 Target size 20 MEASURE · F5 Reflow 20 MEASURE · F10 Craft vocabulary 20 MEASURE · F13 A11y-beyond-contrast 20 MEASURE · F6 Typography 16 MEASURE/LOOK · F7 Spacing 16 MEASURE · F8 Alignment 16 MEASURE/LOOK · F1 Hierarchy 15 LOOK · F11 Affordance 15 LOOK · F9 Color 12 MEASURE/LOOK · F12 States 12 LOOK · F15 Motion 12 MEASURE/LOOK · F17 Perceived perf 12 MEASURE/ASK · F19 Trust 12 MEASURE/LOOK · F14 Density 9 LOOK · F16 Microcopy 8 LOOK · F18 Aesthetic-usability 3 ASK.

## 3. THE AUDIT SPEC — ordered, implementable gate list

Three passes mapped to Guild's existing gates. **BLOCK** = fails the build; **ADVISE** = warns only.

### Pass A — Deterministic gates (extends Guild's MEASURE pipeline). All MEASURE-tier. Cheap DOM/style checks before render-dependent ones.
1. **Contrast (F3)** — alpha-composited, gradient worst-stop. **BLOCK** on AA text/non-text failures. *(existing)*
2. **Target size (F4)** — 24×24 + spacing exception. **BLOCK** on AA fail. *(extends existing)*
3. **Reflow/overflow sweep (F5)** — 320/360/768 + 900–1200 band + 1440. **BLOCK** on horizontal overflow/clipping at 320px and on mid-band overlap. *(extends responsive-scan gate)*
4. **Geometry integrity (F2)** — overlap / rhythm / content-start / nesting. **BLOCK** on unintended overlap, >20% rhythm outlier, >4px content-start spread; **ADVISE** on nesting depth ≥3. *(existing, expanded)*
5. **Type metrics (F6)** — chars-per-line, line-height ratio, scale conformance, whole-pixel. **ADVISE** (BLOCK only when line issues induce horizontal overflow). *(extends type-ramp gate)*
6. **Spacing/proximity + scale conformance (F7)** — ambiguous-grouping + off-scale values. **ADVISE.** *(extends spacing-scale gate)*
7. **Alignment edges/baseline (F8)** — distinct-edge count, baseline grid. **ADVISE.**
8. **Craft vocabulary (F10)** — radius / shadow-direction / border-weight / icon-size counts. **ADVISE** (coherence signal). *(extends token-drift gate)*
9. **Color temperature + token drift + dark-mode contrast diff (F9)** — mixed-gray-temperature flag, stale hex, dark-mode contrast loss. **BLOCK** on dark-mode AA contrast loss; **ADVISE** on temperature inconsistency. *(extends token-drift gate)*
10. **Focus & keyboard a11y (F13)** — focus order vs. visual order, focus-indicator 3:1/size, keyboard reachability, landmarks/headings, focus-not-obscured. **BLOCK** on missing focus indicator, keyboard trap, focus obscured; **ADVISE** on heading-order. *(extends existing a11y)*
11. **Motion tokens + reduced-motion (F15)** — duration >500ms, non-`prefers-reduced-motion` animation. **BLOCK** on missing reduced-motion for transform/parallax; **ADVISE** on >400ms. *(extends reduced-motion gate)*
12. **Perceived-performance indicator logic (F17)** — feedback <0.1s, loading >1s, percent-done+cancel >10s. **ADVISE** (static analysis can't always see runtime).
13. **State deltas (F12, measurable subset)** — hover/focus produce a computed-style change. **ADVISE.**
14. **Affordance cross-reference (F11, measurable subset)** — handler/role/cursor mismatches. **ADVISE**, but **BLOCK** the clear dead-button case (button-styled element with zero interactivity).
15. **Dark-pattern style-asymmetry + preselected opt-in (F19, measurable subset)** — **ADVISE** (escalate to LOOK).

### Pass B — Model-judgment review (maps to Guild's auto-critique gate). LOOK-tier, screenshot + vision model against stated criteria.
16. **Saliency / squint test (F1)** — blur screenshot, confirm primary-action blob dominance + 3–5 weight tiers. **ADVISE** (strong warn — this is the #1 gap).
17. **Affordance honesty visual confirmation (F11)** — do styled elements read as clickable. **ADVISE.**
18. **State-matrix completeness (F12)** — exercise components; empty/error/loading/skeleton present & sensible. **ADVISE.**
19. **Microcopy quality (F16)** — errors/empty states vs. NN/g criteria. **ADVISE.**
20. **Color harmony + dark-mode parity look (F9)** — **ADVISE.**
21. **Optical alignment + density judgment (F8/F14)** — **ADVISE.**
22. **Dark-pattern intent (F19)** — confirmshaming wording, misdirection. **ADVISE.**

### Pass C — Human/user testing (maps to completeness-gate; cannot be automated). ASK-tier. See §4.
23. Blind comprehension / first-impression testing; emotional-reflective resonance; felt trust over time; felt performance; whether motion genuinely aids. **Advisory to release owner** — never build-blocking, but the completeness-gate should record whether these were reviewed.

**Rule for BLOCK vs ADVISE:** BLOCK only where a cited external standard (WCAG) or a calibrated Guild geometric threshold is violated with low false-positive risk. Everything model-judged ADVISES. This keeps LOOK-tier noise from failing builds while ensuring the Round-3 class of geometric issues (now MEASURE) *does* block.

## 4. THE EYES-ONLY RESIDUE (bounded ASK/unmeasurable scope)

No machine proxy exists for these; they define exactly where human or model-visual review remains mandatory:

1. **Whether the primary action is the *right* primary action** — saliency finds the dominant blob; it cannot know business intent. (LOOK confirms dominance; ASK confirms correctness.)
2. **Comprehension** — does a first-time user understand what the screen is for? Only blind user testing answers this.
3. **Emotional/reflective resonance (Norman reflective tier)** — pride, identity, "delight." No proxy.
4. **The causal aesthetic-usability effect itself** — measurable inputs (F1/F6/F7/F10) correlate (r ≈ 0.589), but the felt "this is beautiful therefore trustworthy" is human-only.
5. **Wording quality nuance** — tone, brand voice, wit vs. flippancy in microcopy (NN/g warns against joking in serious errors); a model can approximate, a human judges.
6. **Whether motion aids or harms understanding** — duration/easing are measurable; *purpose* and *interruptibility-in-practice* are judged.
7. **Screen-reader narrative coherence** — landmark/heading structure is measurable; whether the spoken narrative "tells a sensible story" is ASK.
8. **Felt performance / patience** — thresholds are measurable; whether *this* audience tolerates *this* wait is ASK.
9. **Dark-pattern intent** — style asymmetry is measurable; whether a countdown is an honest deadline or a manipulative fake is ASK.
10. **Optical (vs. mathematical) alignment fine-tuning** — icons/quotes/arrowheads mathematically centered but looking wrong.
11. **Cultural/contextual appropriateness of aesthetics** — Kurosu (Japan) vs. Tractinsky (Israel) showed cross-cultural variance in aesthetic preference; no universal proxy.

## 5. WHAT DIDN'T SURVIVE / SOURCE CONTRADICTIONS

**Discarded or weak-evidence claims:**
- **"Larger CTAs boost clicks up to 300%," "high contrast improves readability by 50%," "44×44 targets get 23% more engagement"** (DeveloperUX blog) — no primary source; discarded as load-bearing, retained only as illustrative and flagged weak.
- **"Skeleton screens perceived 30% faster / reduce bounce 9–20%"** — *direction* supported by Mejtoft et al. (ECCE'18, peer-reviewed) and NN/g, but the specific percentages trace to secondary blogs (UI-Deploy, DEV) citing unnamed "studies." Keep the qualitative finding (skeletons > spinners for perceived speed); discard the precise percentages.
- **Data-ink ratio as a pass/fail gate** — Tufte's own "within reason" caveat plus Inbar et al. (2007), who found users often *prefer* higher "chartjunk," means there is **no defensible numeric data-ink threshold**. Kept as ADVISE/LOOK only.
- **A single "correct" aesthetic-usability correlation** — the durable published figure is Kurosu & Kashimura's **r = 0.589**; the frequently-repeated "r > 0.9" is unsourced secondhand inflation and was discarded. Tractinsky (2000) confirmed persistence of the correlation without publishing a competing single coefficient.

**Authoritative sources that genuinely contradict each other (surfaced, not averaged):**
1. **Line length.** Butterick: **45–90 characters**. Bringhurst: **45–75** (66 ideal), **40–50 multi-column**. Web "golden rule": 45–80. → Recommend 45–75 (the intersection for single-column body) and flag outside it, noting the disagreement rather than splitting silently.
2. **Motion duration numbers.** Material short1=**50ms** vs. Carbon fast-01=**70ms**; Material short2=**100ms** vs. Carbon fast-02=**110ms**; Carbon caps its static slow token at **700ms** while Material's scale runs to **1000ms**; NN/g calls **400ms** "very slow" and **500ms** a "drag," while Val Head accepts up to **500ms** for large motion; Carbon's checklist wants micro-interactions in **90–120ms**. → No single cross-system truth. Recommend adopting **NN/g's 100–400ms usable / >500ms fail** as the *audit* bound (safest upper limit); treat token scales as reference, not gate.
3. **Target size.** WCAG 2.5.8 AA = **24×24**; WCAG 2.5.5 AAA and Apple HIG = **44×44**; Material = **48×48dp**. WCAG issue #1831 explicitly disputes the 24px basis, arguing 44px is better founded. → BLOCK at 24 (the legal AA line); ADVISE toward 44/48 for touch.
4. **Carbon's own motion guidance drifted between versions** — legacy v9 said "100–300ms" with different easing curves than the current (2026, "Last updated 03 July 2026") productive/expressive curves. → Always cite the current version; design-system guidance is a moving target.
5. **Minimalism/data-ink vs. user preference** — Tufte's maximize-data-ink vs. Inbar (2007) showing users often prefer chartjunk; NN/g's aesthetic-minimalist heuristic vs. the aesthetic-usability finding that richer visuals can raise *perceived* usability. → A real tension between objective parsimony and subjective appeal; treat density as ADVISE/LOOK, never a gate.

---

### Confidence notes (adversarial verification)
- **High confidence (primary spec text, multiply corroborated):** F3 contrast, F4 target size, F5 reflow, F13 focus criteria (all verbatim from W3C WCAG 2.2); F6 line-length/line-height (Butterick verbatim, confirmed by enricher); F17 response limits (NN/g verbatim); F18 aesthetic-usability r=0.589 (Kurosu & Kashimura CHI'95, confirmed by enricher).
- **Medium confidence (authoritative but version-drifting or internally disputed):** F15 motion tokens (Material page is JS-gated — token list verified via Carbon's dated primary doc and a high-quality Material mirror; recommend confirming against a first-party Material token file before locking into a gate); F4 44 vs 24 debate.
- **Lower confidence / heuristic (no external numeric threshold — Guild convention):** F2 geometric thresholds, F7 proximity ratio, F8 edge counts, F10 craft-vocabulary counts, F1 tier-count 3–5. These are the calibrated conventions to tune against real audits, not literature constants.
- **Explicitly no machine proxy:** F18 (causal effect) and the eleven §4 residue items.