# Multi-Model Bake-Off — Engine-Fit Reference for Guild

*Empirical results from a controlled bake-off run 2026-06-24 inside atrium, with
all four engines spawned as live agent panes against identical inputs. This doc
exists so future raid + engine-selection decisions in Guild are grounded in
evidence, not folklore.*

## Top-line lesson

**The biggest lever isn't model tier — it's evidence-gathering method.** A
"weaker" model that probes the DOM and measures values beats a "stronger" model
that opines from a screenshot. **Bake measurement into the task spec** and any
engine produces evidence-grounded findings; ship the spec without it and you
get opinion regardless of which engine you picked.

This is why the **"Measure, Don't Eyeball"** rule was added to Mage's
`critical_actions` and to `tasks/visual-critique.md`.

## The bake-offs

### Bake-off 1 — Coding (Claude vs Codex vs Antigravity-Pro)

Task: implement `flatten.js` (Node module) against a pre-written 8-test suite.
Same skeleton, same story, same tests for all three engines.

| | Claude | Codex (gpt-5.5 medium) | Antigravity (Gemini 3.1 Pro) |
|---|---|---|---|
| Tests | **8/8** in 729ms | **8/8** in 1125ms | **8/8** in 666ms |
| Lines | 28 | 31 | 29 |
| Style | Single `walk`, explicit `Array.isArray` branch, **inline edge-case comment**, modern `??` | `isExpandable` helper (slight over-decomposition), one opaque `!path` guard | Single `recurse`, defensive `String(key)`, no helper, verbose ternary instead of `??` |

**Verdict:** Effective 3-way tie on correctness; Claude takes a small clarity
edge from the inline edge-case comment. All three are production-acceptable.

**Implication:** *On small, well-specified, test-driven dev tasks, engine choice
barely moves the needle.* Engine-fit differences for code likely emerge at
larger scope (multi-file features, complex refactors, debugging real failures),
not on a 30-line utility.

### Bake-off 2 — Visual critique (4 engine/tier runs on linear.app)

Task: senior visual-designer critique of https://linear.app — same brief for
all four engines.

| Engine | Method | Distinctive contribution |
|---|---|---|
| **Claude** (Opus, high effort) | Slow + thorough thinking (6m 49s, 15.7k tokens) | Pinpoint **sub-AA on `1.0 / 2.0 / 3.0` section index labels** (`rgb(98,102,109)` ≈ 3.4:1). Only one to *positively* call out the "spec-document brand system" as the strongest asset. |
| **Codex** (gpt-5.5 medium) | Prose from screenshots; eyeballed measurements | Sharpest on **IA repetition** (5 feature sections, identical hierarchy). Caught **hero CTA hierarchy** issue. *Its contrast claim was later disproved by Antigravity-Flash's actual measurement.* |
| **Antigravity / Gemini 3.5 Flash** | **Spawned its own atrium browser pane, DOM-eval'd live**, probed multiple viewports | **Measured** contrast (proving Codex wrong on body text — real issue is **code-diff highlights**). **Responsive: testimonials hidden on mobile/laptop** (no one else found this). Captured exact CSS (`Inter Variable`, `Berkeley Mono`, `-1.408px` tracking, class names). |
| **Antigravity / Gemini 3.1 Pro** | Pure observational critique — **never probed DOM** | Higher-level designerly judgments: "Z-pattern" layout reading, "monospaced numbering injects command-line aesthetic." **Substantively disagreed with Flash on the quote cards** (Flash: vibrant break; Pro: jarring) — a real designer debate. |

**Verdict:** Each engine surfaced **substantially different findings with very
little overlap.** No single winner. The union of all four was materially
richer than any solo run.

**Key observation:** Pro vs Flash showed that the rigor difference was the
*evidence-gathering choice*, not the model tier. Flash chose to spawn a browser
and measure; Pro didn't. Same engine, opposite working styles, different
findings. Two competent designers also genuinely disagreed on the quote cards
(no objectively right answer) — that's real value the raid surfaced.

## Engine-fit recommendations for Guild

| Guild phase / task | Recommendation | Why |
|---|---|---|
| **Mage** — visual critique, design direction | **RAID** (multi-engine); include Antigravity for its in-CLI browser tool | Bake-off 2 proves it: union of findings >> any solo, and Antigravity uniquely measures live UI |
| **Ranger** — visual-audit / heuristic-eval subtasks targeting live UIs | Include **Antigravity** at minimum; raid for high-stakes | Same DOM-eval rigor advantage applies wherever the target is a live URL |
| **Ranger** — research synthesis (multi-source) | **RAID** | The Motion UX research raid earlier in this project established this pattern; bake-off 2 corroborates: different engines surface different findings |
| **Warlock, Sage, Healer, Cartographer, Guild Master** | **Solo Claude** | Prose / judgment / orchestration; no evidence that raid improves these. Switching adds coordination cost without payoff. |
| **BMAD dev side** (Dev, autonomous build) | **Codex is a viable swap** to experiment with | Bake-off 1 was effectively a tie; Codex was within striking distance. Don't *assume* Claude is best for code — A/B on real stories. |
| **Any visual-critique task** | Require **"Measure, Don't Eyeball"** in the spec (see `tasks/visual-critique.md`) | The biggest lever; baked into Mage's critical_actions |

## What Antigravity uniquely brings

The bake-off made it clear Antigravity isn't "Gemini in a different wrapper" —
it ships an **in-CLI browser tool** that lets the agent navigate, evaluate the
live DOM, and probe multiple viewports as part of its working loop. Claude Code
can drive Playwright/Figma MCPs *if available*; Antigravity has comparable
capability built in. For any task whose evidence lives in a live UI, this is
the differentiator. Position Antigravity in raid composition with that lens.

## What this does NOT prove

Honest limits, so we don't over-claim:

- **n = 1 per bake-off.** Directional, not statistical. The mechanism (different
  evidence-gathering methods → different findings) is structural, so it should
  generalize, but a single comparison can't prove it generalizes.
- **Small dev task.** The 30-line flatten utility doesn't exercise the
  differences that likely emerge at scale (large refactors, multi-file
  features, debugging real failures).
- **Static visual target.** linear.app's homepage doesn't expose the
  interaction or motion layer; critique of an app with rich micro-interactions
  would need additional methods.
- **The Mage rigor signal was a *method* choice, not a model class.** Pro and
  Flash are the same engine; Flash chose to probe, Pro didn't. The
  measure-discipline rule is what makes this consistent across engines.

## Practical raid composition

When running `mage-raid` or `ranger-raid` on a high-stakes visual-critique
task, the recommended composition is:

- **Claude** — for the slow, careful thinking + positive analysis lens
- **Antigravity** — for measured/DOM-grounded evidence + responsive probing
- **Codex** (optional, if you want a 3rd take) — for the IA / structural
  framing lens

The synthesis step then takes the union — each engine's distinctive contribution
typically survives the synthesis because they're surfacing different things.

## When NOT to raid

If the task is judgment- or prose-heavy and the inputs are textual (writing
microcopy, drafting personas from a research summary, framing a handoff spec),
solo Claude is the right default. The bake-off showed no evidence raid helps
when the work is taste-grounded rather than evidence-grounded.

## Provenance

- Run date: 2026-06-24
- Run by: this Guild project's "Perfect GUILD" effort (see `MEMORY.md`)
- Sandbox: `/tmp/guild-bakeoff/` (torn down post-run; full agent transcripts
  in atrium's session vault under search term "bakeoff")
- Bake-off panes were `mage-bakeoff` and `dev-bakeoff` rooms; the Antigravity
  re-run on Pro was done in `mage-bakeoff` after replacing the Flash pane
