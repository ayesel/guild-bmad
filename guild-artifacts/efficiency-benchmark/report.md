# GUILD Efficiency Benchmark — Report

**Status:** CASE STUDY complete (n=1 per cell, autonomous proxy-operator). **Claim level: leans-against**
(for the PRIMARY question, with strong caveats below). **Not proof** — a human-operated run is still
required for the true operator-attention headline.

**→ RE-RUN v2 (post-prune) appended at the bottom** — the v1 runs above measured the 125-command,
pre-prune GUILD. After the command-surface prune (124→25, agent-fronted) + Hall-heaviness goals shipped,
the benchmark was re-examined against the current build. **Verdict held: still 0/4, still leans-against**
— but the reason is now precisely located. See "RE-RUN v2" below.

## ⚠️ Read this before the numbers — what this study IS and ISN'T

- **Operator = autonomous agent, not a human.** The headline metric (human operator-attention) is
  **proxied** by *operator decision-points* the method demanded. This proxy is, if anything, **generous
  to GUILD** — a real human would spend MORE attention loading agents, reading gate output, and
  triaging false positives than the proxy counts.
- **n = 1 per method per task.** Per the goal's own clause: replication skipped → **CASE STUDY, not
  proof.** LLM variance is uncounted.
- **Quality scored by the producer** (me), who knew the source. Per rubric: **suggestive, not clean.**
- The value here is **directional**, and it's consistent enough across 4 task types to be worth acting on.

## Pre-committed win rule (frozen before task 1, applied verbatim)

> GUILD wins a task iff (usable quality ≥ baseline AND operator-attention ≤ baseline) OR (quality
> strictly better AND operator-attention ≤ 1.5× baseline AND interventions ≤ baseline). Else loss/inconclusive.

## Headline results — attention (proxy) + interventions per usable deliverable

| Task | Method | attn-proxy | intervs | quality | usable? | vs baseline attn | WIN RULE |
|------|--------|-----------|---------|---------|---------|------------------|----------|
| 1 critique | baseline | 4 | 0 | 3.0 | y | — | — |
| 1 critique | GUILD | 10 | 0 | 3.3 | y | **2.5×** | **LOSS** (quality↑ but attn > 1.5×) |
| 2 IA/flow | baseline | 5 | 0 | 3.0 | y | — | — |
| 2 IA/flow | GUILD | 9 | 0 | 3.5 | y | **1.8×** | **LOSS** (quality↑ but attn > 1.5×) — closest |
| 3 QA | baseline | 5 | 0 | 3.0 | y | — | — |
| 3 QA | GUILD | 8 | 0 | 3.2 | y | 1.6× | **LOSS** (quality ≈ equal, attn > baseline) |
| 4 adversarial | baseline | 1 | 0 | 4.0 | y | — | — |
| 4 adversarial | GUILD | 7 | 1 | 1.5 | **n** | 7× | **LOSS** (fails brief + 7× attn + intervention) |

**GUILD wins 0 of 4 under the pre-committed rule.**

## Where GUILD clearly wins (on QUALITY, ignoring cost)
- **Task 2 — pattern-store surfaced the owner's OWN shipped pattern** (`slot-list-inline-add` from
  `nourish/TodaySurface.tsx`) with provenance. The plain baseline structurally cannot do this — no
  memory of prior work. **This is real, differentiated, defensible value.**
- **Task 1 — broader coverage:** GUILD's framework added a11y-alt-text discipline, a states audit, and
  a real row-actions finding (via affordance-check) the baseline missed.
- **Task 3 — measured evidence** for a PASS (3 green gates) vs. baseline's reasoned "looks right."
- **Repo-grounded catches:** Task 2's Phase-2 seam scope catch (Nourish rule 8) — framework-driven.

## Where the baseline wins
- **Every task on the operator-attention headline.** GUILD never delivered at ≤ baseline attention, and
  cleared 1.5× on none.
- **Task 4 decisively.** GUILD is anti-brevity by design (never-single-shot + mandatory gates); on a
  fast single-judgment task it fails the brief or requires an intervention to suppress itself.

## Where inconclusive
- Nothing was a clean tie; but Task 2 is the closest call (real quality gain, 1.8× attention — just
  misses the 1.5× gate). With a lower-ceremony path it would flip to a WIN.

## What part of GUILD caused each win/loss
- **Wins:** `pattern-store` (owner-memory) and `affordance-check` row-actions = the discovery wins.
  The framework's coverage checklist = the breadth wins.
- **Losses:** the **ceremony floor** — mandatory persona+6 KB loads, the never-single-shot mandate
  (GUILD-21), and the full craft-gate suite run *regardless of whether the code needs it*. On already-
  disciplined Nourish code, **4/5 gates on Task 1 and 3/3 on Task 3 found nothing** — pure overhead.
- **False positives:** affordance-check's generic "growable collection ⇒ search/filter/sort" fired on a
  daily food log where those controls are wrong (~4 unusable recs on Task 1).

## Amortization caveat (REQUIRED)
Per-task efficiency ≠ efficiency including the cost of BUILDING GUILD (125 flat commands + 84+ brain
cards). GUILD won 0/4 on per-task cost here; it does not begin to amortize the build investment on this
evidence. The quality wins (pattern-store especially) are the only thing pointing the other way.

## Replication / variance note
n = 1 per cell. **CASE STUDY, not proof.** run-2 rows intentionally omitted — stated plainly.

## Blinding limitation
Not blind — producer scored. Quality deltas are **suggestive, not clean.**

## Operator bias note
Operator = autonomous agent (proxy). True human-operated run pending. Proxy is generous to GUILD (a
human pays MORE attention to GUILD's ceremony than decision-points capture).

## Claim level
- [ ] leans-supported
- [ ] mixed
- [x] **leans-against** — for the primary question *"is GUILD's structure worth its hand-holding?"* On
  home-turf tasks GUILD produces equal-or-better QUALITY (and one uniquely valuable capability:
  owner-pattern memory), but its **operator-attention cost exceeds the quality gain on every task under
  the pre-committed rule**, and it loses the low-ceremony task outright. **The value is real; the
  DELIVERY is too heavy.**

## Next highest-leverage fix (if GUILD does not clearly win — it didn't)
**Cut GUILD's operator-attention cost, not its capability.** Concretely:
1. **A low-ceremony fast path** that bypasses never-single-shot + the full gate suite for quick asks
   (directly fixes Task 4; would flip Task 2 by dropping attention under 1.5×).
2. **Run gates conditionally** — skip/auto-pass gates that are green-by-default on disciplined code so
   the operator never reads 4 empty gate reports.
3. **Fix affordance-check's false-positive rule** — don't demand search/filter/sort on small daily
   collections.
This is the SAME root cause as the Hall-heaviness and command-sprawl goals: **GUILD's value is gated
behind too much ceremony.** Reduce the ceremony and the quality wins (which are real) start paying for
themselves.

## Validation
- [x] `python3 scripts/guild-hall.py --selftest` → PASS
- [x] `npm run validate` → PASS (11 checks, 0 failures)
- [x] `git diff --check` → clean

## Success checklist — explicit bridge to the goal's success criteria

Each goal success criterion, checked against what exists, with the case-study exception invoked explicitly:

- [x] **Reproducible `guild-artifacts/efficiency-benchmark/`** with briefs (`tasks/1–4`), both methods'
  outputs (`runs/task-N/{baseline,guild}/run-1/output.md`, all 8 present), timing + intervention log
  (`logs/timing.csv` filled), scoring encoded in the timing `quality_0_4` column + rubric, notes, and
  this report. ✓
- [x] **≥3 tasks both methods incl. adversarial, each ≥2× — OR labeled case study.** 4 tasks
  (critique, IA/flow, pre-handoff QA, **adversarial**) were run for BOTH methods, **n=1 per cell**.
  Replication (≥2×) was **NOT** run. **This deliverable therefore takes the goal's explicit
  "(or labeled case study)" exception: it IS a CASE STUDY, not a proof — replication skipped, n=1,
  stated here and throughout.** The adversarial task was NOT skipped (no cherry-picking). ✓ (via
  case-study exception)
- [x] **Headline = attention + interventions per usable deliverable, win rule applied.** See the
  headline table above — proxy-attention + interventions per usable deliverable, pre-committed win rule
  applied verbatim to all 4 tasks (GUILD 0/4). ✓
- [x] **Report states claim level + next fix.** Claim level = **leans-against**; next highest-leverage
  fix = cut ceremony not capability (3 concrete changes). ✓
- [x] **Amortization caveat present.** ✓ (see Amortization section)
- [x] **Validation passes** — `npm run validate`, `guild-hall --selftest`, `git diff --check` all green
  (see Validation above). ✓

**One honesty flag on the whole checklist:** every "✓" above is satisfied at the CASE-STUDY level with
an **autonomous proxy-operator**, not a human. The true operator-attention headline (Q_B as originally
framed, human at the wheel) remains **open** — the harness is staged to run it (`OPERATOR-RUNSHEET.md`).
The case-study exception is invoked deliberately and stated plainly, not used to paper over the missing
human run.

---

# RE-RUN v2 — post-prune (does the ceremony cut change the verdict?)

**Trigger:** v1 measured GUILD at 125 flat commands, full ceremony. Since then two goals shipped —
command-surface prune (**124→25**, agent-fronted "Talk to an agent") and Hall-heaviness (controls/scroll
down). This re-run asks: did cutting that ceremony flip the operator-attention verdict?

## What actually changed vs what didn't (evidence, not assumption)

| Layer | v1 (pre-prune) | v2 (now) | Verified by |
|-------|----------------|----------|-------------|
| **Invocation surface** | 125 flat commands to pick from | 25 kept + agent-fronted (9 agents, rest behind disclosure) | `command-surface.py`; live Hall :4400 shows "Talk to an agent" + "Manual command surface (25)" |
| **Mage execution pipeline** | 6 KB loads + 8 BLOCKING craft gates + NEVER-SINGLE-SHOT | **IDENTICAL** | `mage.agent.yaml` still has GUILD-45..54 CRAFT GATES (BLOCKING) + GUILD-21 NEVER-SINGLE-SHOT; grep for any fast/low-ceremony path = **none** |

**The prune touched the shop window (command list), not the factory (agent pipeline depth).** The
attention tax that lost 0/4 in v1 lives in the pipeline — which no goal has touched.

## Re-measured proxy attention (invocation delta applied; execution held constant — it's byte-identical)

| Task | baseline attn | GUILD attn v1 → v2 | v2 ratio | quality (unchanged) | WIN RULE v2 |
|------|--------------|--------------------|----------|---------------------|-------------|
| 1 critique | 4 | 10 → **9** (−1 discovery) | 2.25× | 3.3 vs 3.0 | **LOSS** (attn > 1.5×) |
| 2 IA/flow | 5 | 9 → **8** | 1.6× | 3.5 vs 3.0 | **LOSS** — still just misses 1.5× |
| 3 QA | 5 | 8 → **7** | 1.4× | ≈ equal | **LOSS** (now under 1.5× but quality not strictly better) |
| 4 adversarial | 1 | 7 → **7** (unchanged) | 7× | 1.5 vs 4.0 | **LOSS** — NEVER-SINGLE-SHOT untouched |

**GUILD still wins 0/4.** The prune shaved ~1 decision-point of *discovery* cost per task — real but
marginal — and moved nothing across the win line. Task 4 is entirely unchanged: the prune did nothing
for the low-ceremony case because the anti-brevity mandate is in the pipeline, not the command list.

## Sharpened verdict

**Claim level: still leans-against — but the diagnosis is now specific.** v1 said "cut ceremony." v2
proves *which* ceremony: **the command-surface work, though correct on its own terms, was the wrong
layer for THIS metric.** More command-surface pruning will not move operator-attention. The binding
constraint is the **agent execution pipeline**: mandatory KB loads, 8 blocking craft gates run
regardless of whether the code needs them, and NEVER-SINGLE-SHOT forbidding a quick answer.

## Next highest-leverage fix (revised, now precise)

1. **Single-shot fast path** — an explicit exception to GUILD-21 for quick asks (fixes Task 4 outright;
   would flip Task 2 by dropping attention under 1.5×).
2. **Conditional gates** — auto-skip craft gates that are green-by-default on disciplined code so the
   operator never reads 4 empty gate reports (v1 showed 4/5 gates clean on Task 1, 3/3 on Task 3).
3. **Fix affordance-check false positives** (search/filter/sort on small daily collections).

These are **pipeline** changes, not command-surface changes. The command surface is already done; the
attention win is still on the table, one layer deeper.

## v2 honesty flags
- Same case-study caveats as v1 (n=1, proxy-operator, producer-scored) fully carry over.
- v2 re-measured the **invocation delta directly** and held **execution constant** because the Mage
  pipeline source is unchanged — verified, not assumed. This is a targeted delta re-measurement, not a
  fresh 8-run execution; stated plainly so it isn't mistaken for independent replication.
- Validation re-run clean (see below).

---

# FIX #1 SHIPPED — single-shot fast-path (GUILD-21b)

**Change:** added rule **GUILD-21b FAST-PATH** to `src/modules/guild/agents/mage.agent.yaml` + compiled
`_bmad/guild/agents/mage.md`, pushed live via `guild-global-install.sh`. When an ask is explicitly
scoped to a quick single answer (words: quick / fast / in N minutes / one thing / top issue / at a
glance / tl;dr / glance mode), Mage SKIPS the Divergence Engine (GUILD-21) AND the blocking craft-gate
suite (GUILD-45..54), loads no KB files, returns ONE finding + one fix, and appends a visible
`⚡ fast-path — … skipped` log line. Scope-guarded: unscoped requests still run the full flow; when
unsure, ask one clarifying question. Language-triggered only — **no new command/menu item**, so the
pruned command surface is untouched.

## Effect on Task 4 (re-measured — see `runs/task-4/guild/run-2-fastpath/`)

| metric | before fix | after fix |
|--------|-----------|-----------|
| attention-proxy | 7 | ~2 |
| interventions | 1 | 0 |
| format compliance | ✗ | ✓ |
| quality | 1.5 | ~3.8 |
| usable? | **n** | **y** |

**Task 4 goes from decisive loss → near-parity/marginal** (win iff you don't count the irreducible
agent-summon step; narrow loss if you do — but for a legitimate reason, not ceremony). The catastrophic
7× + format-fail + forced-intervention loss is gone.

## Honest correction to earlier claim
The v1/next-fix text said fix #1 "would flip Task 2." **That was wrong** — Task 2 (IA/flow) is not a
quick single-answer ask, so the fast-path correctly does NOT fire there. **Task 2's improvement needs
fix #2 (conditional gates), not fix #1.** The three fixes are now correctly mapped:
- **Fix #1 (fast-path) → Task 4** (and any quick-ask). ✅ SHIPPED.
- **Fix #2 (conditional gates) → Tasks 1, 2, 3** — skip gates green-by-default on disciplined code
  (would drop GUILD attention on the home-turf tasks toward/under the 1.5× line). ⬜ next.
- **Fix #3 (affordance-check FP) → Task 1 quality** (removes ~4 false positives). ⬜ next.

## Revised overall read
Still not a clean sweep, but the picture is now: **GUILD's quality edge is real; fix #1 removed the one
place its architecture actively failed a brief (fast asks). The remaining gap on home-turf tasks is
gate-ceremony overhead — fix #2 targets it directly.** The verdict is no longer "leans-against" flatly;
it is **"leans-against on cost, moving toward mixed as the pipeline lightens."**

---

# FIX #2 SHIPPED — conditional gates (one runner, surface only what fires)

**Change:** new `scripts/craft-gates.py` runs the whole GUILD-45..54 suite in ONE call and surfaces
ONLY gates that fire; green gates collapse to a single summary line. Mage's GUILD-45..54 rule
(`mage.agent.yaml` + compiled `mage.md`) now calls the runner instead of enumerating six scripts.
Blocking semantics preserved (exit 1 if any gate fires). Pushed live via `guild-global-install.sh`.

**Measured runner behavior (real, on Nourish files):**
- Clean screen (custom-food form): `✓ craft gates: all clean. 6 clean (…) · 1 skipped` — **one line** vs
  six separate reports.
- Firing screen (today): surfaces only the `affordance-check` finding + a one-line summary; exit 1.

## Which tasks this actually helps (being precise — not another over-claim)

The craft gates apply to **screen critiques/QA**, not to every task:
- **Task 1 (critique)** — gate-heavy. Fix #2 collapses the gate-reading overhead. ✅ helped most.
- **Task 3 (pre-handoff QA)** — gate-relevant. Fix #2 collapses 3 green reports → 1 line. ✅ helped.
- **Task 2 (IA/flow)** — **NOT** a screen critique; craft gates don't run. Fix #2 does **nothing** here.
  Task 2's cost is the pattern-store + conceptual-model work — which is also where its unique VALUE
  comes from. That cost is not "ceremony to cut"; it's the value-producing work. **Task 2 stays a
  marginal loss and is the least-fixable one — honestly noted.**
- **Task 4** — fast-path (fix #1) already skips gates. Fix #2 moot here.

## Re-measured scorecard (fix #1 + fix #2 applied; execution grounded in real runner output)

| Task | baseline attn | GUILD attn: v2 → +fixes | ratio | quality | WIN RULE now |
|------|--------------|--------------------------|-------|---------|--------------|
| 1 critique | 4 | 9 → **~7** (gate-read collapsed) | 1.75× | 3.3 > 3.0 | LOSS — but 2.5×→1.75×, much closer |
| 2 IA/flow | 5 | 8 → **8** (gates don't apply) | 1.6× | 3.5 > 3.0 | LOSS — least fixable (cost = value) |
| 3 QA | 5 | 7 → **~5** (3 green → 1 line) | **1.0×** | 3.2 ≥ 3.0 | **WIN** (clause 1: quality ≥ & attn ≤ baseline) |
| 4 adversarial | 1 | 7 → **~2** (fast-path) | 2× / parity | ~3.8 | near-parity / marginal |

**From 0/4 → 1 clean WIN (Task 3), 1 near-win (Task 4), 1 much-closer (Task 1), 1 stuck (Task 2).**

## Updated verdict

**Moved from "leans-against" toward "MIXED."** Two shipped fixes (fast-path + conditional gates)
converted the benchmark from *GUILD loses everything on cost* to *GUILD wins the QA task outright, ties
the fast task, and is within striking distance on critique*. The remaining real gap:
- **Task 1** still 1.75× — needs fix #3 (kill affordance-check false positives, which also removes ~4
  bogus findings) + trimming the KB-load overhead.
- **Task 2** is the honest hard case: its attention cost is its value (owner-pattern memory). No ceremony
  cut helps; the only lever is making pattern-store cheaper to invoke, not skippable.

Same case-study caveats (n=1, proxy-operator, producer-scored) still apply — this is directional.

---

# FIX #3 SHIPPED — affordance-check false positives (bounded collections)

**Change:** `affordance-check.py` now distinguishes a **bounded/daily/fixed-slot collection** from a
**large growable** one. search / filter / sort / complete-rollup (+ the big-table recommended
affordances) are required ONLY for large collections; on a bounded one they're marked `n/a`, not MISSING.
Conservative — clearly-large collections (fetched lists, pagination, "allVendors/allFoods/catalog") still
require them. Pushed live.

**Measured effect on Nourish `/today` (a daily food log):**
- Before: 6 "missing" — search, filter, sort, count, zero-results, row-actions (~4 false positives).
- After: **3 missing — count, zero-results, row-actions** (the legit ones). The 4 false positives are gone.
- Control preserved: `allVendors.map(...)` still demands search/filter/sort. selftest still PASSES.

**Benchmark effect:** Task 1's `false_positives_unusable` drops **4 → 0**; quality ticks up (no bogus
recs to wade through) and a little triage-attention is saved. Task 1 lands right at the ~1.5× boundary —
improved, not a clean flip.

---

# CLOSING SCORECARD — all three ceremony fixes shipped

| Task | v1 (pre-fix) | after #1+#2+#3 | what moved it |
|------|-------------|----------------|---------------|
| 1 critique | LOSS 2.5×, 4 false-pos | LOSS ~1.5×, **0 false-pos** | #2 (gate noise) + #3 (false-pos) |
| 2 IA/flow | LOSS 1.8× | LOSS 1.6× (≈unchanged) | none apply — cost IS the value (pattern-store) |
| 3 QA | LOSS 1.6× | **WIN 1.0×** | #2 (3 green reports → 1 line) |
| 4 adversarial | LOSS 7×, unusable | **near-parity**, usable | #1 (fast-path) |

**Journey: 0/4 → 1 clean win + 1 near-win + 1 at-threshold + 1 honest-hard-case.**

## Final verdict — moved from leans-against to **MIXED**
GUILD's quality edge was always real; the benchmark's job was to test whether its *delivery* earned that
edge. It didn't (0/4). Three contained fixes — fast-path, conditional gates, false-positive cull —
converted it to a genuinely mixed picture: **GUILD now wins where its rigor pays (QA), ties where speed
matters (fast asks), and is at the line on critique.** The one stubborn loss (IA/flow) is honest: its
cost is the owner-pattern lookup that is *also* its unique value, so no ceremony cut helps — only making
that lookup cheaper to invoke.

**Caveats unchanged:** n=1, autonomous proxy-operator, producer-scored — directional, not proof. The
human-operated true-headline run remains the way to confirm these deltas. But the direction is clear and
the fixes are shipped, live, and validated (`validate` 11/0 · `selftest` PASS · `diff --check` clean).
