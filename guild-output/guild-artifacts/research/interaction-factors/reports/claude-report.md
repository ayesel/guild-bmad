
# GUILD INTERACTION-FACTORS RESEARCH (v1 — 2026-07-05)


## Scope & Method

This is the TIME/interaction-over-time leg of the factors triptych (UI-FACTORS = space, IA-FACTORS = structure, this = behavior over time). It extends past Guild's existing token+envelope enforcement (which already gates presence-level things: tokenized durations, reduced-motion branch, per-primitive state coverage, >400ms flag / >500ms hard-fail) into **CHOREOGRAPHY, FEEDBACK, REVERSIBILITY, and FLOW**. Every factor carries the five-part contract: EVIDENCE, MACHINE PROXY, THRESHOLDS, CHECK TIER, FAILURE CAUGHT. Instrument set assumed: an agent that can drive the app — dispatch synthetic pointer/keyboard events, record frame sequences (`requestAnimationFrame`/screencast), diff DOM + accessibility tree before/after input, trace `document.activeElement`, script input timing, read `PerformanceObserver` entries (`event`, `layout-shift`, `longtask`), and inspect `getAnimations()`/computed styles. A check that requires driving the app is still **MEASURE** if deterministic; needing a human/vision-model to judge frame sequences is **LOOK**; needing a human to *feel* a quality is **ASK**.


---


# RANKED TAXONOMY

Factors scored **Impact (1–5) × Machine-checkability (1–5)**, sorted by product. Starting from the 15 scaffolded dimensions, I **split** scaffold #4 (drag) into direct-manipulation feel (F10) and pointer-cancellation/abort (F9, a distinct WCAG-anchored MEASURE check); **split** scaffold #8 into animation-never-blocks-input (F2) and interruptibility resolution; **promoted** reduced-motion-preserves-feedback to a standalone factor (F17) because Guild already gates *presence* of the branch but not its *feedback-preservation*; **added** optimistic/pessimistic decision (F16) as its own factor. Nothing was pruned — all 15 scaffold themes survive, reorganized into 20 factors.


---


## F1 — Input Acknowledgment Latency (≤100ms) [Impact 5 × Check 5 = 25]

**EVIDENCE.** Nielsen, *Response Time Limits* (NN/g): "0.1 second is about the limit for having the user feel that the system is reacting instantaneously, meaning that no special feedback is necessary except to display the result." Rooted in Miller (1968), *Response time in man-computer conversational transactions*, AFIPS Fall Joint Computer Conf. Vol. 33, 267–277; and Card, Robertson & Mackinlay (1991), *The information visualizer*, ACM CHI'91. Google's Core Web Vitals threshold doc (web.dev, updated 2024) grounds INP's line in the same tradition: "research points to 100 ms as a 'good' Interaction to Next Paint threshold… given users reported low quality levels for delays of 300 ms or more, ideally this would be the 'poor' threshold."
**MACHINE PROXY.** Drive the app: dispatch `pointerdown`/`click`/`keydown` on every interactive element; via `PerformanceObserver({type:'event'})` measure `processingStart − startTime` (input delay) and time-to-first-paint-change (frame diff or style/DOM mutation) after the event. Flag any interaction whose first visual acknowledgment (pressed state, spinner, optimistic change, skeleton) lands after 100ms even when the underlying operation is still pending.
**THRESHOLDS.** Acknowledge ≤100ms (Nielsen/Miller). Field INP: ≤200ms good, >500ms poor (web.dev, 75th percentile). The 200ms INP "good" line is an *achievability-adjusted* number; the *perceptual* target remains ~100ms.
**CHECK TIER.** MEASURE (deterministic under driving).
**FAILURE CAUGHT.** The core "clunky" complaint: a button that does nothing visible for 250ms after a tap, so the user taps again and double-fires. Catches missing pressed-states and missing optimistic/skeleton acknowledgment on slow async actions. [web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds)


## F2 — Animation Never Blocks Input / Interruptibility [Impact 5 × Check 4 = 20]

**EVIDENCE.** Val Head, *Designing Interface Animation* (Rosenfeld Media, 2016, Ch.3 excerpt on UXmatters, Dec 2016): "design and build your interface animations so they are interruptible and don't block input… Interruptible animations are nonblocking animations." On the common shortcut: "menu items or buttons are visually disabled while page transitions or other transitions are occurring, in order to reduce logic complexity. But this isn't actually a better solution… it exaggerates the blocking behavior of the animation and doesn't solve the core issue." Material Design (m1 Motion) states motion should be designed so the user "never has to wait for the animation to finish." Mechanism reference: MDN, `pointer-events` — value `none` "instructs the pointer event to go 'through' the element and target whatever is 'underneath' that element instead."
**MACHINE PROXY.** Drive the app: begin an entrance/exit transition, then at t=50ms into it dispatch `pointerdown`/`click` at the target hit-box and a `keydown` to the focused control; assert (via state diff / handler instrumentation) the event registered and produced its effect. Separately scan computed styles during transitions for `pointer-events:none` on interactive nodes and detect full-screen transparent overlays intercepting hits mid-animation.
**THRESHOLDS.** No agreed numeric threshold; binary contract — input dispatched at any frame of a standard transition MUST register. (The existing envelope caps standard transitions at ≤500ms, bounding the exposure window.)
**CHECK TIER.** MEASURE (deterministic under driving) for "did the event register"; LOOK only if judging whether the *interrupted* animation resolves gracefully.
**FAILURE CAUGHT.** Exactly the post-hoc-motion-pass smell: motion added as a polish layer that swallows clicks during the 300–500ms it plays, so rapid users feel the UI "eat" their taps. Also catches `pointer-events:none` left on during a fade. [UXmatters](https://www.uxmatters.com/mt/archives/2016/12/designing-interface-animation.php)[UXmatters](https://www.uxmatters.com/mt/archives/2016/12/designing-interface-animation.php)


## F3 — Transition Coverage as a State-Pair Matrix [Impact 5 × Check 4 = 20]

**EVIDENCE.** The central defect condition named in the brief. No single external source defines it; it composes Material's choreography model (m2 Choreography: "sequencing… helps users understand what has changed on a screen, if elements were added or removed") with the flow-artifact requirement. External evidence is design-system practice only — **flagged as weak**; the *composition into a matrix diff* is a Guild construct.
**MACHINE PROXY.** Parse the flow artifact into a declared state graph; enumerate reachable state pairs. Drive the built app under scripted traversal (automated crawl), and for each observed transition record whether a tokenized transition fired (`getAnimations()`/`transition`/`animation` events) OR an explicit "cut" was declared. Diff: every reachable pair must map to {designed-motion | declared-cut}; any pair with neither is an **unspecified gap** = defect.
**THRESHOLDS.** 100% of reachable state pairs classified. Any unclassified pair fails.
**CHECK TIER.** MEASURE for coverage/diff (deterministic under driving); LOOK for whether the chosen motion is *appropriate* to the relationship.
**FAILURE CAUGHT.** The root cause the owner reports: transitions "defaulted" (browser jump-cut) rather than designed, invisible until someone notices the app feels abrupt. Turns "motion applied after static design" into a gate at flow-authoring time — this is the factor that ends the post-hoc-motion-pass incident class.


## F4 — Reversibility: Undo-over-Confirm & Forgiveness [Impact 5 × Check 4 = 20]

**EVIDENCE.** Nielsen's heuristics: #3 User control & freedom ("Support undo and redo"; users need a "clearly marked emergency exit"); #5 Error prevention ("Either eliminate error-prone conditions or check for them and present users with a confirmation option before they commit to the action"). NN/g (Sherwin, *Error Prevention*) confirms confirmation is reserved for consequential/irreversible actions, not routine ones. Apple HIG *Undo and redo*: undo "gives people easy ways to reverse many types of actions… explore and experiment safely." Gmail "Undo Send" is the canonical toast/undo-window pattern.
**MACHINE PROXY.** Classify each mutating action in the flow artifact by reversibility (reversible / soft-reversible / irreversible). Drive the app: trigger each destructive action; assert presence of an undo affordance (toast-with-undo, soft-delete + restore) within the acknowledgment window, OR — only for truly irreversible actions — a type-to-confirm gate. Flag confirm-dialogs guarding reversible actions as "confirm-wall smell."
**THRESHOLDS.** No agreed numeric undo-window; common practice 5–10s toast (practitioner-level, **weak evidence**). Binary: destructive action ⇒ undo present; irreversible action ⇒ explicit confirm.
**CHECK TIER.** MEASURE for presence of undo/confirm (deterministic under driving); ASK for whether an action is "truly catastrophic" enough to warrant a confirm wall.
**FAILURE CAUGHT.** Confirm-wall proliferation ("Are you sure?" on every delete) that trains click-through, while genuinely destructive actions lack undo. Implements the brief's "destructive actions offer undo rather than a confirm wall."


## F5 — Focus Management Through Time [Impact 5 × Check 5 = 25]

**EVIDENCE.** W3C WAI-ARIA APG, *Dialog (Modal) Pattern*: on open, focus moves into the dialog (first focusable element, or a `tabindex=-1` heading for content-heavy dialogs); "when it closes, the user's point of regard is maintained by returning focus to the element that triggered display of the dialog." APG *Alert Dialog*: for a destructive confirmation, "focus is automatically set to the first focusable element inside the dialog, which is the 'No' button… the least destructive action." WCAG 2.4.3 Focus Order (supporting). Esc-to-close and focus-trap are normative APG behaviors.
**MACHINE PROXY.** Drive route changes, modal opens/closes, disclosure/accordion toggles; trace `document.activeElement` before/after. Assert: (a) after modal open, focus is inside the dialog; (b) after close, focus returns to the trigger; (c) Tab is trapped within an open modal; (d) after SPA route change, focus moves to a landmark/heading rather than being lost to `<body>`; (e) Esc closes.
**THRESHOLDS.** Binary per APG. No numeric threshold.
**CHECK TIER.** MEASURE (deterministic under driving).
**FAILURE CAUGHT.** Keyboard/screen-reader users stranded: modal opens but focus stays behind it; after closing a dialog focus drops to `<body>` and Tab restarts from the top; SPA navigation leaves focus on a removed element. A silent, high-severity "clunky" defect invisible to mouse-only review.


## F6 — Cumulative Layout Shift as an Interaction Defect [Impact 4 × Check 5 = 20]

**EVIDENCE.** Google web.dev, *CLS*: "sites should strive to have a CLS score of 0.1 or less… Good CLS values are 0.1 or less. Poor values are greater than 0.25" (75th percentile). Threshold-definition doc: "levels of shift from 0.15 and higher were consistently perceived as disruptive, while shifts of 0.1 and lower were noticeable but not excessively disruptive." CLS uses session windows (start on shift, end after 1s quiet, max 5s). Shifts triggered *by user action* within 500ms are excluded as "expected."
**MACHINE PROXY.** `PerformanceObserver({type:'layout-shift'})` while driving through load and each interaction; sum unexpected shifts per session window; attribute shifts >500ms after an interaction (unexpected) vs within 500ms (expected).
**THRESHOLDS.** ≤0.1 good, >0.25 poor (web.dev). Treat any interaction-adjacent unexpected shift as an interaction defect regardless of aggregate.
**CHECK TIER.** MEASURE.
**FAILURE CAUGHT.** The "mis-tap" class of clunky: a button moves as an async skeleton resolves and the user clicks the wrong control; content reflows under the reading position after a late image or injected banner.


## F7 — Latency Choreography: Skeleton-to-Content & Progressive Rendering [Impact 4 × Check 4 = 16]

**EVIDENCE.** NN/g, *Skeleton Screens 101*: skeletons should mirror final layout to build a mental model; used with waits under 10s, progress bars for >10s. NN/g, *Response Time Limits*: >1s change cursor/indicate work; >10s show percent-done + interrupt. Peer-reviewed: Mejtoft, Långström & Söderström (2018), *The effect of skeleton screens: Users' perception of speed and ease of navigation*, ECCE'18 Article No. 22, pp. 1–4 (ACM, DOI 10.1145/3232078.3232086) — a 4-page short paper aiming "to evaluate the usefulness of skeleton screens as an alternative to spinners"; result is positive but small-scale, so treat as suggestive. **Disagreement flag:** the widely-circulated "skeletons perceived ~30% faster" figure is blog-level and *not* well-sourced; some controlled comparisons show no significant difference. Liikkanen & Gómez recommend prioritized/progressive load order.
**MACHINE PROXY.** Drive a slow-network profile; capture frame sequence; assert an indicator appears within the F1 window, that a skeleton (if used) approximates final geometry (compare skeleton bounding boxes to loaded content boxes — also gates CLS via F6), and that content order follows a declared priority. Indicator-presence vs Nielsen 0.1/1/10 is already an existing MEASURE gate — this factor extends into *sequencing quality*.
**THRESHOLDS.** Indicator within 1s of a >1s wait; percent-done + cancel for >10s (Nielsen). Skeleton geometry within CLS 0.1 of final.
**CHECK TIER.** MEASURE for indicator timing + skeleton-geometry/CLS; LOOK for whether progressive order surfaces "most important content first."
**FAILURE CAUGHT.** Skeletons that jump to a differently-shaped final layout (CLS + jarring); spinners where a shaped skeleton would reduce perceived wait; important content arriving last.


## F8 — Keyboard & Gesture Modality Parity [Impact 5 × Check 4 = 20]

**EVIDENCE.** WCAG 2.1.1 Keyboard (A): all functionality operable from a keyboard. WCAG 2.5.1 Pointer Gestures (A, verbatim): "All functionality that uses multipoint or path-based gestures for operation can be operated with a single pointer without a path-based gesture, unless a multipoint or path-based gesture is essential." WCAG 2.5.7 Dragging Movements (2.2, AA): dragging needs a single-pointer non-dragging alternative. WCAG 1.4.13 Content on Hover or Focus: hover-revealed content must be dismissable, hoverable, persistent.
**MACHINE PROXY.** Static + driven: for every element with pointer/drag/gesture handlers, assert a keyboard path exists (focusable + `keydown` produces the same state diff as the pointer path) and a single-pointer alternative exists for each path-based/multipoint gesture. For hover-triggered content, dispatch focus (not just hover) and assert it appears and is dismissable via Esc.
**THRESHOLDS.** Binary per SC. No numeric threshold.
**CHECK TIER.** MEASURE (deterministic under driving) for existence of equivalents; LOOK for whether the alternative is *discoverable*.
**FAILURE CAUGHT.** Drag-only reordering, swipe-only carousels, hover-only menus that are dead on keyboard and touch — a whole population locked out, and a "clunky" feel on touch devices where hover doesn't exist.


## F9 — Pointer Cancellation / Mid-Gesture Abort [Impact 4 × Check 5 = 20] *(added; split from scaffold #4)*

**EVIDENCE.** WCAG 2.5.2 Pointer Cancellation (A, verbatim): for single-pointer operation at least one of — "No Down-Event… Abort or Undo: Completion of the function is on the up-event, and a mechanism is available to abort the function before completion or to undo the function after completion… Up Reversal: The up-event reverses any outcome of the preceding down-event… Essential." APG examples: drag-and-drop where "releasing the pointer outside the drop target area reverts the action." Convention: Escape-to-cancel-drag.
**MACHINE PROXY.** Drive: begin a drag (`pointerdown`+`pointermove`), then dispatch `Escape` and/or release outside any drop target; assert the item returns to origin and no mutation persisted. For buttons, assert the action fires on `pointerup`/`click`, not `pointerdown` (dispatch down, move off target, up — assert no fire).
**THRESHOLDS.** Binary per SC 2.5.2 (one of four conditions must hold).
**CHECK TIER.** MEASURE.
**FAILURE CAUGHT.** The brief's "a drag can be cancelled mid-gesture": drags that commit on down-event or that can't be aborted, so an accidental grab reorders a list with no escape.


## F10 — Direct-Manipulation Drag Feel [Impact 3 × Check 4 = 12]

**EVIDENCE.** Shneiderman's direct-manipulation principles (continuous representation; rapid, reversible, incremental actions). Modern implementation defaults: dnd-kit documents an activation `distance` (pixels the pointer must move before drag starts) and a `delay`+`tolerance` combination; its default composable set is `Distance({value: 5})` **or** `Delay({value: 200, tolerance: 10})`, and its touch guidance is "dragging activates after a 250ms delay with 5px movement tolerance" (legacy TouchSensor example: "Press delay of 250ms, with tolerance of 5px"). **Disagreement flag:** these are library *configuration values*, not standards — Android's touch-slop, iOS's implicit thresholds, and dnd-kit's defaults all differ; there is **no agreed cross-platform drag distance/time threshold.**
**MACHINE PROXY.** Drive: assert a jitter below the activation distance does not start a drag and movement ≥ threshold does; measure drag-follow latency (pointer-to-element position lag) frame-by-frame; assert snap targets resolve deterministically.
**THRESHOLDS.** No agreed threshold; report the configured value and assert consistency across the app. dnd-kit defaults (5px distance; 200–250ms delay; 5–10px tolerance) are library values, not standards.
**CHECK TIER.** MEASURE for activation thresholds and follow-latency; ASK for whether the drag *feels* physical/weighted (momentum, rubber-banding) — cannot be captured by state diffs.
**FAILURE CAUGHT.** Drags that start on the tiniest jitter (accidental reorders) or lag behind the finger; inconsistent activation across surfaces.


## F11 — Choreography & Stagger [Impact 3 × Check 3 = 9]

**EVIDENCE.** Material Design (m1 Motion, *Choreography*, undated ~2014–16): "Do not wait for each item to fully animate before introducing the next item. Begin each item's staggered entrance no more than 20ms apart" — note this is a **ceiling ("no more than 20ms")**, not a fixed value, and is from legacy Material v1; m3 does not restate the number. Also: "List items have a slightly staggered entrance. Grid items populate left to right, and top to bottom." Library *examples* (not enforced defaults): GSAP docs `stagger: 0.1` = 0.1s between tween starts; Motion/Framer `stagger(0.1)`. React Spring has **no fixed ms default** (physics-based `useTrail`). Apple HIG publishes **no numeric stagger**, only "Prefer quick, precise animations."
**MACHINE PROXY.** Record frame sequence of list/grid entrances; extract per-item animation start times from `getAnimations()`/style timeline; compute inter-item delay and assert it is (a) nonzero when a cascade is intended and (b) within the declared budget. Assert order encodes reading direction (top-left first).
**THRESHOLDS.** Inter-item stagger ≤20ms per Material's ceiling (legacy, undated, **weak**); otherwise no authoritative standard — assert internal consistency against a Guild-chosen token.
**CHECK TIER.** MEASURE for stagger *timing/order*; LOOK for whether the resulting rhythm reads as intentional hierarchy.
**FAILURE CAUGHT.** All-at-once pop-in (no hierarchy) or sluggish over-staggered lists where the user waits for row 12 to appear. [material + 3](https://m1.material.io/motion/choreography.html)


## F12 — Spatial Continuity & Shared-Element Transitions [Impact 3 × Check 3 = 9]

**EVIDENCE.** Material Design container transform (MDC-Android `MaterialContainerTransform`): "a shared element transition… the shared element here refers to the bounding container… transforming its size and shape" to "reinforce their relationship and maintain a user's navigational context." Four Material patterns: Container Transform, Shared Axis, Fade Through, Fade. iOS/Android platform conventions for shared-element transitions.
**MACHINE PROXY.** For declared shared-element transitions, drive the navigation and track the shared node's bounding box across frames; assert continuous interpolation (no teleport/flash) between source and destination geometry. Detect presence of a persistent container element across the transition.
**THRESHOLDS.** No numeric threshold; binary — declared shared element must animate continuously (no discontinuity > one frame).
**CHECK TIER.** MEASURE for geometric continuity of a *declared* shared element; LOOK for whether the app's overall "spatial model" survives navigation.
**FAILURE CAUGHT.** List→detail navigations that jump-cut, breaking object permanence, so users lose their place — a subtle contributor to "feels disjointed."


## F13 — Form Interaction Timing [Impact 4 × Check 4 = 16]

**EVIDENCE.** WCAG 3.3.1 Error Identification (A) and 3.3.3 Error Suggestion (AA). Baymard Institute (*Usability Testing of Inline Form Validation*): validate inline but "premature validations must be avoided"; remove error when corrected; use positive inline validation. **Genuine disagreement, do not average:** Baymard and much practitioner consensus favor **validate-on-blur**; but Adam Silver ("Inline validation is problematic") and UX Movement argue on-blur is *itself* premature ("users have to go back to their previous field to correct their error") and prefer **validate-on-submit** with focus-to-first-error; keystroke validation is broadly rejected except for positive password-strength feedback. No universal consensus.
**MACHINE PROXY.** Drive: type invalid input and assert no error appears mid-keystroke; blur and assert behavior matches the declared policy; submit an invalid form and assert (a) errors programmatically associated (`aria-describedby`/`aria-invalid`), (b) focus moves to the first invalid field, (c) errors clear when corrected. Forgiving-format parsing: submit `(555) 123-4567` vs `5551234567` and assert both accepted where declared.
**THRESHOLDS.** Binary per declared policy + WCAG association. No agreed timing threshold (the blur-vs-submit dispute is unresolved).
**CHECK TIER.** MEASURE for error association, focus-to-first-error, clear-on-correct, format tolerance; ASK for which validation-timing policy best fits the audience.
**FAILURE CAUGHT.** "This field is required" flashing while the user is still typing the first character; submit that reports an error but doesn't move focus to it; rejection of a validly-formatted phone number.


## F14 — Feedback Channel Appropriateness (Visual/Haptic/Audio) [Impact 3 × Check 3 = 9]

**EVIDENCE.** Saffer, *Microinteractions* (O'Reilly, 2013): feedback is one of four parts (trigger → rules → feedback → loops/modes); feedback may be visual, auditory, or haptic; the "foghorn test" reserves prominent feedback for events critical enough to notice without looking. Apple HIG *Playing haptics* + *Feedback*; WWDC19 Core Haptics "harmony" principle: audio, haptics, visuals in the same tempo. Accessibility parity: haptic/audio feedback must have a visual equivalent.
**MACHINE PROXY.** Partial. MEASURE: detect that *some* feedback channel fires per event class, and that any haptic/audio call has a co-occurring visual state change (parity). Cannot deterministically judge whether the *chosen* channel is appropriate.
**THRESHOLDS.** Binary parity: haptic/audio ⇒ visual equivalent present. Channel-appropriateness: no threshold.
**CHECK TIER.** MEASURE for parity; ASK for whether the channel choice suits the event class.
**FAILURE CAUGHT.** Haptic-only or sound-only confirmations that give deaf/muted-device users nothing; events that warrant feedback getting none.


## F15 — Micro-interaction Completeness (Saffer anatomy) [Impact 4 × Check 3 = 12]

**EVIDENCE.** Saffer, *Microinteractions* (2013): every microinteraction = **trigger → rules → feedback → loops & modes**. Used as a per-element completeness checklist. "Designed" vs "browser-default": a designed interaction has explicit tokenized states/feedback; a browser-default has none beyond UA styling.
**MACHINE PROXY.** For each interactive element, drive the trigger and assert presence of: a defined rule (state change), feedback (visual/other), and correct loop/mode behavior (e.g., repeated triggers coalesce). Detect browser-default behavior = trigger fires but no tokenized state/feedback layer is present.
**THRESHOLDS.** Binary: all four parts present per interactive element where a microinteraction is declared.
**CHECK TIER.** MEASURE for presence of trigger/rule/feedback/loop; LOOK for whether feedback is *meaningful*.
**FAILURE CAUGHT.** Elements shipped with browser-default behavior (no hover/active/loading states) that were never "designed" — the defaulted-not-designed condition at the element level.


## F16 — Optimistic vs Pessimistic UI Decision [Impact 4 × Check 2 = 8] *(added)*

**EVIDENCE.** Denys Mishunov, *True Lies of Optimistic User Interfaces* (Smashing Magazine, Nov 2016), verbatim: "Optimistic UIs are based on the assumption that when the user clicks a button, the server should return a success response in 97 to 99% of cases," and optimistic interactions should apply "only to those elements that never wait longer than 2 seconds for a server response." **Disagreement flag (report all, don't average):** Ströer Labs (*Why are we pessimistic about optimistic UI for web applications?*) reverted to pessimistic UI because "Almost every action in our web interface is important" — and noted that because commands were so fast, "we had to artificially extend the time period for which we display the progress bar because otherwise, it would flash only for 100 ms and the user did not even notice it." Cris (criscmd), *Why I Never Use Optimistic Updates* (DEV): "Every time you write an optimistic update, you're creating an alternate reality… Multiply that across a large app and your UI becomes a ticking time bomb," using them only when "The failure state doesn't matter, like liking a post that no one else sees." The boundary is genuinely contested and domain-dependent.
**MACHINE PROXY.** Weak. MEASURE: detect *whether* the app updates before or after server confirmation (drive with a delayed/failed mock backend; observe whether UI changes pre- or post-response and whether a failed response rolls back). Cannot deterministically decide whether the chosen policy is *correct* for the action's stakes.
**THRESHOLDS.** No numeric threshold. Rule of thumb (Mishunov, **weak**): optimistic only where reversible + low-stakes + high success rate + <2s wait.
**CHECK TIER.** MEASURE for detecting the pattern + verifying rollback-on-failure; ASK for whether optimistic is *safe* for a given action.
**FAILURE CAUGHT.** Optimistic "success" shown for a payment that later fails; or pessimistic spinners on trivial toggles that make the app feel sluggish.


## F17 — Reduced-Motion as Redesigned Choreography (not deletion) [Impact 4 × Check 4 = 16] *(promoted from presence-only)*

**EVIDENCE.** WCAG 2.3.3 Animation from Interactions (AAA, verbatim): "Motion animation triggered by interaction can be disabled, unless the animation is essential to the functionality or the information being conveyed." WCAG 2.2.2 Pause, Stop, Hide (A) for auto-playing motion. Community/vendor best practice (TestParty/web.dev): "Some developers disable ALL animation when reduced motion is preferred. This removes essential feedback and can harm usability. Better approach: Replace motion with non-motion alternatives (opacity changes, color shifts) rather than removing feedback entirely." Presence of a reduced-motion branch is already Guild MEASURE — this factor extends into whether that branch **preserves feedback**.
**MACHINE PROXY.** Drive with `prefers-reduced-motion: reduce` emulated; for each interaction that gives feedback in the default branch, assert the reduced branch still produces a perceptible non-motion acknowledgment (opacity/color/text change) — not a total no-op. Diff feedback presence between branches.
**THRESHOLDS.** Binary: every feedback-bearing interaction retains an acknowledgment under reduced motion.
**CHECK TIER.** MEASURE (deterministic under driving).
**FAILURE CAUGHT.** Reduced-motion implemented as `* { animation: none }`, which silently deletes loading/confirmation feedback — motion-sensitive users left with no acknowledgment at all. [Testparty](https://testparty.ai/blog/wcag-animation-interactions-guide)


## F18 — Flow-Level Dynamics (auto-advance, back integrity, context preservation) [Impact 4 × Check 4 = 16]

**EVIDENCE.** Nielsen heuristics (user control; consistency & standards). Back-button integrity and context preservation are standard flow requirements; auto-advance vs explicit-continue is a documented tradeoff (auto-advance speeds single-select steps but removes control/undo). External sourcing is practitioner-level — **flagged weak**.
**MACHINE PROXY.** Drive multi-step flows: enter data, navigate Back, assert entered data persists; refresh mid-flow, assert state restoration where declared; assert Back never skips or duplicates steps; assert step-transition pattern is consistent across steps (same direction/motion token).
**THRESHOLDS.** Binary: Back preserves data + integrity; step transitions consistent.
**CHECK TIER.** MEASURE for data persistence, back integrity, transition consistency; ASK for whether auto-advance vs explicit-continue is right for the task.
**FAILURE CAUGHT.** Back button wipes a half-filled form; refresh loses progress; inconsistent step animations that disorient.


## F19 — Signature-Moment Budget [Impact 2 × Check 3 = 6]

**EVIDENCE.** Saffer's "Signature Moments" (microinteractions elevated to brand). Design principle: ration "delight"/personality motion to one hero moment per surface rather than scattering ambient flourish. No authoritative numeric budget exists — this is a Guild-imposed convention (**weak external evidence**), but Material and Carbon both formalize a productive-vs-expressive split enabling the count (Carbon: "Reserve expressive motion for occasional, important moments").
**MACHINE PROXY.** Count elements using the "expressive"/emphasized motion scheme (vs standard/productive) per surface; flag surfaces exceeding the declared budget (e.g., >1 hero moment).
**THRESHOLDS.** Guild-set budget (e.g., ≤1 expressive/hero motion per surface); no external numeric standard.
**CHECK TIER.** MEASURE for the count; ASK for whether the chosen hero moment is the *right* one.
**FAILURE CAUGHT.** Flourish everywhere → visual noise and slow feel; or zero personality → flat. Makes "delight" a countable budget rather than vibes.


## F20 — Sound & Haptics Surface-Appropriateness [Impact 2 × Check 3 = 6]

**EVIDENCE.** Apple HIG *Playing haptics* / Core Haptics (native/mobile primary). Mute-by-default norms for web audio (browsers block autoplay audio without a user gesture). **Surface flag:** haptics apply primarily to native/mobile (Taptic Engine); the Web Vibration API is limited and inconsistently supported; audio feedback on web should be opt-in/muted-by-default. Parity-with-visual per F14.
**MACHINE PROXY.** Detect haptic/audio API calls; assert (a) no auto-firing audio on web without a user gesture, (b) visual parity present. Surface type (native vs web) gates applicability.
**THRESHOLDS.** Binary parity + no-autoplay-audio on web.
**CHECK TIER.** MEASURE for parity/autoplay; ASK for whether an event class *warrants* haptic/audio at all.
**FAILURE CAUGHT.** Web pages that ding audio unprompted; native flows missing expected tactile confirmation on key actions.


---


# 1. VERDICT

The interaction-factor space has a clear shape: it decomposes into **latency/feedback** (F1, F7, F16), **reversibility/safety** (F4, F9, F17), **accessibility-through-time** (F5, F8, F14, F20), **choreography** (F2, F3, F11, F12, F19), **stability** (F6), **input feel** (F10, F15), and **flow/forms** (F13, F18). The decisive finding: **most of these are MEASURE-tier under an agent that can drive the app.** The deterministic-under-driving instrument set collapses much of what teams reflexively call "feel" into checkable contracts — acknowledgment latency, input-blocking, focus movement, layout shift, modality parity, pointer cancellation, reduced-motion feedback-preservation, and transition coverage are all deterministic. What remains genuinely ASK-tier is small and nameable (§4).

**The single highest-leverage gap in a "tokens + envelope only" practice:** a tokens+envelope gate verifies that motion values are *legal* (tokenized, within duration bounds, reduced-motion branch present). It verifies **that motion is well-formed — never that it is complete or non-harmful.** It cannot see the three defects the owner actually feels as "clunky": (1) **transition coverage** — that *every* reachable state pair was deliberately designed with motion or an explicit cut (F3); (2) **input never blocked** — that animation doesn't swallow input during the legal-but-nonzero window it plays (F2); and (3) **acknowledgment latency** — that every action is acknowledged ≤100ms even when the operation is slow (F1). The biggest blind spot is **F3, transition-coverage-as-a-matrix**, because it is the one factor that makes "motion applied as a post-hoc polish pass" *structurally impossible*: an undesigned transition becomes a build-time defect rather than something a person notices after ship. That is the leg that ends the post-hoc-motion-pass incident class.


---


# 2. THE GATE SPEC (ordered: BLOCK vs ADVISE)

**BLOCK (build-fails) — static (artifact/DOM alone):**

1. **Artifact completeness (extends the completeness-gate concept):** every reachable state pair in the flow artifact declares {designed-motion | explicit-cut}; every interactive element declares transition/feedback/reversibility/modality-parity fields (§3). Any unfilled field ⇒ block.
2. **Token/envelope (existing gate, unchanged):** no raw transition values; ≤500ms hard-fail for standard transitions; >400ms flag; reduced-motion branch present.

**BLOCK — requires driving the running app:**
3. **F1 Acknowledgment ≤100ms** on every interactive element (incl. slow-async via optimistic/skeleton).
4. **F2 Animation-never-blocks-input:** synthetic input mid-transition must register; no `pointer-events:none` on interactive nodes during standard transitions.
5. **F3 Transition-coverage diff:** declared state-pair matrix vs transitions observed under automated traversal; any unspecified gap ⇒ block.
6. **F5 Focus management:** focus-in/return/trap on modal; focus-reset on route change; Esc closes.
7. **F8/F9 Modality parity & pointer cancellation:** keyboard + single-pointer equivalents exist; destructive/drag actions abortable/undoable; actions fire on up-event.
8. **F6 CLS:** ≤0.1; zero unexpected interaction-adjacent shifts.
9. **F17 Reduced-motion preserves feedback:** every feedback-bearing interaction still acknowledges under `prefers-reduced-motion`.
10. **F13 Form error semantics:** programmatic error association + focus-to-first-error + clear-on-correct.

**ADVISE/WARN (driven or static):**
11. **F7** skeleton-geometry/sequencing; **F10** drag activation consistency; **F11** stagger timing/order; **F12** shared-element continuity; **F18** back-integrity/context preservation; **F19** signature-moment budget count; **F16** optimistic/pessimistic pattern detection + rollback verification; **F20** web-audio autoplay.

**Frame-judged LOOK-tier (route to the existing watch/critique auto-critique gate):**
12. Appropriateness of chosen motion to relationship (F3), progressive "most-important-first" order (F7), stagger rhythm reads as hierarchy (F11), spatial model survives navigation (F12), feedback is meaningful (F15).

**Extends which existing gates:** F1/F6/F7-timing extend the *responsive-scan-style* MEASURE gate; F2/F3/F5/F8/F9/F13/F17 are *new driven checks* layered onto the token/envelope gate; the LOOK items feed the *watch/critique* gate; §3 artifact fields feed the *general completeness-gate*.


---


# 3. THE ARTIFACT SPEC (required fields per state-pair and per interactive element)

Per **state pair** (every reachable transition in a state-diagram / user-flow / interaction-map):

- **Transition spec:** {motion token (easing family + duration token) | explicit intentional cut}. No blank. If motion: enter/exit asymmetry (exit ≈ enter × 0.75 per existing foundation), origin (spatial source), and pattern (container-transform / shared-axis / fade-through / fade).
- **Feedback spec:** acknowledgment channel + latency budget (default ≤100ms) for the triggering action.
- **Reversibility classification:** reversible / soft-reversible (undo-window) / irreversible (confirm-gate). Drives F4/F9 checks.
- **Modality-parity note:** keyboard equivalent + single-pointer equivalent + touch/hover degradation.

Per **interactive element:** Saffer completeness (trigger/rules/feedback/loops-modes); reduced-motion feedback-preserving variant; optimistic-vs-pessimistic declaration for async actions; signature-moment flag (counts against budget).

This makes interaction design a **flow-authoring-time** activity and makes the **artifact-vs-build diff (F3)** a checkable gate: an artifact field left blank blocks; a built transition that doesn't match its declared field blocks.


---


# 4. THE EYES-ONLY RESIDUE (bounded, named, routed)

Genuinely not capturable by state-diff or frames:

1. **"Feels responsive/weighted" (F10 momentum/physics).** → live user testing / owner watch session. (F10 *latency* is MEASURE; the *feel* is ASK.)
2. **Whether an action is "catastrophic enough" to warrant a confirm wall (F4).** → subjective owner/designer decision.
3. **Optimistic-safety for a specific action's stakes (F16).** → owner/designer decision, domain-dependent.
4. **Validation-timing policy choice, blur-vs-submit (F13).** → designer decision (genuine research dispute).
5. **Whether the chosen motion suits the relationship / spatial model survives (F3, F12); stagger reads as hierarchy (F11); feedback is meaningful (F15); progressive order surfaces the right content first (F7).** → the existing **watch/critique** LOOK gate (human or vision-model against rubric).
6. **Which single hero moment deserves the signature budget (F19); channel appropriateness for an event class (F14/F20).** → subjective owner/designer pick.

Everything else in the taxonomy is MEASURE-tier under driving and should NOT be routed to eyes.


---


# 5. WHAT DIDN'T SURVIVE

**Folklore that fails under sourcing:**

- **"Validate inline on blur is the consensus best practice."** It is *not* consensus. Baymard endorses inline-but-not-premature; Adam Silver and UX Movement argue on-blur is itself premature and prefer submit-time validation with focus-to-first-error. Report the dispute; don't gate a single timing policy (F13).
- **"Skeleton screens are ~30% faster perceived than spinners."** The "30%" figure is blog-level and not well-sourced; the peer-reviewed Mejtoft (2018) result is positive but small-scale, and some controlled comparisons find no significant difference. Keep skeleton-geometry/CLS as MEASURE; treat the perceived-speed magnitude as weak (F7).
- **"400ms (Doherty) and 100ms (Nielsen/Miller) are the same 'instant' number."** They are different research traditions. Miller/Nielsen's **100ms** is the *perceptual acknowledgment / direct-manipulation* limit; Doherty & Thadani's **400ms** (IBM Systems Journal, Nov 1982, *The Economic Value of Rapid Response Time*: "When a computer and its users interact at a pace that ensures that neither has to wait on the other, productivity soars, the cost of the work done on the computer tumbles") is a *productivity/flow* threshold that reset the prior 2-second standard. Many blogs conflate them. Guild's envelope already uses 400ms as a flag and 500ms as hard-fail for *durations* — keep that distinct from the 100ms *acknowledgment* contract (F1).
- **"Reduced motion = remove animation."** Directly contradicted by WCAG 2.3.3 intent and best practice: deleting animation can delete essential feedback (F17).
- **"Confirmation dialogs prevent errors."** Nielsen #5 endorses confirmation only for consequential/irreversible actions; routine confirm-walls train click-through and are a smell, not a safeguard (F4).

**Where authoritative sources genuinely disagree (report both, don't average):**

- **Duration norms across design systems:** Material m1 desktop 150–200ms; Material notes card expand 300ms / collapse 250ms; Carbon "most animations 100–300ms" with productive ≠ expressive and *dynamic* duration by distance; Apple HIG gives *no* numbers ("prefer quick, precise animations"). These do not reconcile to one number — Guild's token approach is correct, but the *values* are system-specific.
- **Gesture/drag thresholds:** no agreed cross-platform value; dnd-kit defaults (5px distance; 200–250ms delay; 5–10px tolerance) differ from Android touch-slop and iOS conventions (F10).
- **Validation timing:** Baymard (inline-on-blur, avoid premature) vs Silver/UX Movement (submit-time) (F13).
- **Optimistic-UI boundary:** Mishunov/Smashing (optimistic for low-stakes, <2s waits, 97–99% success) vs Ströer Labs (reverted to pessimistic for a whole console, "almost every action… is important") vs criscmd/DEV ("never" except when "the failure state doesn't matter") — contested and domain-dependent (F16).
- **Stagger magnitude:** Material's "no more than 20ms" ceiling (legacy v1, undated, not restated in m3) vs library *examples* of 100ms (GSAP/Framer) vs physics-based with no ms (React Spring) vs none (Apple) (F11).
- **INP "good" line:** research points to ~100ms perceptually, but Google set **200ms** as the *achievability-adjusted* "good" threshold — the numbers differ by design, not by error (F1).


---


# Sources

1. Nielsen, J. *Response Time Limits* (NN/g). [https://www.nngroup.com/articles/response-times-3-important-limits/](https://www.nngroup.com/articles/response-times-3-important-limits/)
2. Miller, R. B. (1968). *Response time in man-computer conversational transactions.* AFIPS Fall Joint Computer Conf. Vol. 33, 267–277.
3. Card, S. K., Robertson, G. G., Mackinlay, J. D. (1991). *The information visualizer.* ACM CHI'91.
4. NN/g, *Powers of 10: Time Scales in UX.* [https://www.nngroup.com/articles/powers-of-10-time-scales-in-ux/](https://www.nngroup.com/articles/powers-of-10-time-scales-in-ux/)
5. web.dev, *Interaction to Next Paint (INP).* [https://web.dev/articles/inp](https://web.dev/articles/inp)
6. web.dev, *How the Core Web Vitals metrics thresholds were defined.* [https://web.dev/articles/defining-core-web-vitals-thresholds](https://web.dev/articles/defining-core-web-vitals-thresholds)
7. web.dev, *Cumulative Layout Shift (CLS).* [https://web.dev/articles/cls](https://web.dev/articles/cls)
8. web.dev, *Optimize CLS.* [https://web.dev/articles/optimize-cls](https://web.dev/articles/optimize-cls)
9. Doherty, W. J., Thadani, A. J. (Nov 1982). *The Economic Value of Rapid Response Time.* IBM Systems Journal. (Summary via Laws of UX: [https://lawsofux.com/doherty-threshold/](https://lawsofux.com/doherty-threshold/))
10. Saffer, D. *Microinteractions: Designing with Details* (O'Reilly, 2013). [https://www.oreilly.com/library/view/microinteractions/9781491945957/](https://www.oreilly.com/library/view/microinteractions/9781491945957/)
11. Material Design (m1), *Choreography.* [https://m1.material.io/motion/choreography.html](https://m1.material.io/motion/choreography.html)
12. Material Design (m1), *Duration & Easing.* [https://m1.material.io/motion/duration-easing.html](https://m1.material.io/motion/duration-easing.html)
13. Material Design (m2), *Speed.* [https://m2.material.io/design/motion/speed.html](https://m2.material.io/design/motion/speed.html)
14. Material Design (m2), *Choreography.* [https://m2.material.io/design/motion/choreography.html](https://m2.material.io/design/motion/choreography.html)
15. Material Design (m3), *Motion — how it works.* [https://m3.material.io/styles/motion/overview/how-it-works](https://m3.material.io/styles/motion/overview/how-it-works)
16. MaterialContainerTransform / MDC-Android Motion. [https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)
17. Carbon Design System, *Motion.* [https://carbondesignsystem.com/elements/motion/overview/](https://carbondesignsystem.com/elements/motion/overview/)
18. IBM Design Language, *Motion UI basics.* [https://design-language-website.netlify.app/design/language/motion-ui/basics/](https://design-language-website.netlify.app/design/language/motion-ui/basics/)
19. Apple HIG, *Motion.* [https://developer.apple.com/design/human-interface-guidelines/motion](https://developer.apple.com/design/human-interface-guidelines/motion)
20. Apple HIG, *Feedback.* [https://developer.apple.com/design/human-interface-guidelines/feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)
21. Apple HIG, *Playing haptics.* [https://developer.apple.com/design/human-interface-guidelines/playing-haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)
22. Apple HIG, *Gestures.* [https://developer.apple.com/design/human-interface-guidelines/gestures](https://developer.apple.com/design/human-interface-guidelines/gestures)
23. Apple WWDC19, *Expanding the Sensory Experience with Core Haptics.* [https://developer.apple.com/videos/play/wwdc2019/223/](https://developer.apple.com/videos/play/wwdc2019/223/)
24. W3C, *Understanding SC 2.3.3 Animation from Interactions.* [https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html)
25. W3C, *Understanding SC 2.5.1 Pointer Gestures.* [https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html](https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html)
26. W3C, *Understanding SC 2.5.2 Pointer Cancellation.* [https://www.w3.org/WAI/WCAG21/Understanding/pointer-cancellation.html](https://www.w3.org/WAI/WCAG21/Understanding/pointer-cancellation.html)
27. W3C WAI-ARIA APG, *Dialog (Modal) Pattern.* [https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
28. W3C WAI-ARIA APG, *Alert Dialog Example.* [https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/examples/alertdialog/](https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/examples/alertdialog/)
29. Nielsen, J. *10 Usability Heuristics* (esp. #3, #5). [https://www.nngroup.com/articles/ten-usability-heuristics/](https://www.nngroup.com/articles/ten-usability-heuristics/)
30. NN/g (Sherwin), *Usability Heuristic 5: Error Prevention.* [https://www.nngroup.com/videos/usability-heuristic-error-prevention/](https://www.nngroup.com/videos/usability-heuristic-error-prevention/)
31. Apple HIG, *Undo and redo.* [https://developer.apple.com/design/human-interface-guidelines/undo-and-redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)
32. Baymard Institute, *Usability Testing of Inline Form Validation.* [https://baymard.com/blog/inline-form-validation](https://baymard.com/blog/inline-form-validation)
33. Silver, A. *Inline validation is problematic.* [https://medium.com/simple-human/inline-validation-is-problematic-399dd01d436f](https://medium.com/simple-human/inline-validation-is-problematic-399dd01d436f)
34. UX Movement, *Why Users Make More Errors with Instant Inline Validation.* [https://uxmovement.com/forms/why-users-make-more-errors-with-instant-inline-validation/](https://uxmovement.com/forms/why-users-make-more-errors-with-instant-inline-validation/)
35. NN/g, *Skeleton Screens 101.* [https://www.nngroup.com/articles/skeleton-screens/](https://www.nngroup.com/articles/skeleton-screens/)
36. Mejtoft, T., Långström, A., Söderström, U. (2018). *The effect of skeleton screens: Users' perception of speed and ease of navigation.* ECCE'18, Article No. 22, pp. 1–4 (ACM). [https://doi.org/10.1145/3232078.3232086](https://doi.org/10.1145/3232078.3232086)
37. Val Head, *Designing Interface Animation* (Rosenfeld Media, 2016), Ch.3 excerpt on UXmatters. [https://www.uxmatters.com/mt/archives/2016/12/designing-interface-animation.php](https://www.uxmatters.com/mt/archives/2016/12/designing-interface-animation.php)
38. MDN, *pointer-events.* [https://developer.mozilla.org/en-US/docs/Web/CSS/pointer-events](https://developer.mozilla.org/en-US/docs/Web/CSS/pointer-events)
39. Mishunov, D. *True Lies of Optimistic User Interfaces* (Smashing Magazine, Nov 2016). [https://www.smashingmagazine.com/2016/11/true-lies-of-optimistic-user-interfaces/](https://www.smashingmagazine.com/2016/11/true-lies-of-optimistic-user-interfaces/)
40. Ströer Labs, *Why are we pessimistic about optimistic UI for web applications?* [https://blog.stroeer-labs.com/optimistic-ui/](https://blog.stroeer-labs.com/optimistic-ui/)
41. criscmd, *Why I Never Use Optimistic Updates (And Why You Might Regret It Too)* (DEV Community). [https://dev.to/criscmd/why-i-never-use-optimistic-updates-and-why-you-might-regret-it-too-4jem](https://dev.to/criscmd/why-i-never-use-optimistic-updates-and-why-you-might-regret-it-too-4jem)
42. dnd-kit, *Pointer / Touch / Mouse Sensor docs.* [https://docs.dndkit.com/api-documentation/sensors/pointer](https://docs.dndkit.com/api-documentation/sensors/pointer)
43. GSAP, *Staggers.* [https://gsap.com/resources/getting-started/Staggers/](https://gsap.com/resources/getting-started/Staggers/)
44. Motion (Framer Motion), *stagger.* [https://motion.dev/docs/stagger](https://motion.dev/docs/stagger)
45. W3C, *Understanding SC 1.4.13 Content on Hover or Focus.* [https://www.w3.org/WAI/WCAG21/Understanding/content-on-hover-or-focus.html](https://www.w3.org/WAI/WCAG21/Understanding/content-on-hover-or-focus.html)
46. W3C, *Understanding SC 2.1.1 Keyboard.* [https://www.w3.org/WAI/WCAG21/Understanding/keyboard.html](https://www.w3.org/WAI/WCAG21/Understanding/keyboard.html)
47. W3C, *Understanding SC 3.3.1 Error Identification / 3.3.3 Error Suggestion.* [https://www.w3.org/WAI/WCAG21/Understanding/error-identification.html](https://www.w3.org/WAI/WCAG21/Understanding/error-identification.html)
48. W3C, *Understanding SC 2.5.7 Dragging Movements.* [https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)
