# GUILD Efficiency Benchmark — does the structure earn its complexity?

**Status:** CASE STUDY complete (4 tasks × 2 methods, n=1, autonomous proxy-operator) ·
report.md filled, win rule applied, claim level = **leans-against** (value real, delivery too heavy) ·
validation passes · **true human-operated run still pending** for the real attention headline.

## The question

**Q_B (PRIMARY, runnable now):** Does GUILD's structure (agents / gates / pipeline) produce
equal-or-better *usable* output than the **same model with no Guild commands**, for **less
operator attention**? Decision it informs: keep investing in the scaffolding, or just prompt Claude?

**Q_A (aspirational, optional):** Does GUILD beat a skilled *human*? Only run if a real human
baseline exists. A "manual AI baseline" is NEVER presented as human proof.

Baseline for Q_B = **manual AI baseline**: same assistant, same model, same source materials,
**no Guild commands/agents/gates**, labeled honestly.

## Headline metric (this decides it)

- **operator-attention-minutes per usable deliverable**
- **operator interventions per usable deliverable** (prompts, corrections, steering, restarts)

Wall-clock and agent/token runtime are **secondary and NEVER counted as free**.

> Directly tests the owner's standing complaint: *GUILD needs too much prompting / hand-holding.*

## Pre-committed win rule — LOCKED before task 1 (do not edit after any run)

GUILD **wins** a task iff:
1. usable quality **≥** baseline **AND** operator-attention **≤** baseline, **OR**
2. usable quality **strictly better** **AND** operator-attention **≤ 1.5×** baseline **AND** interventions **≤** baseline.

Otherwise → **loss** or **inconclusive**. This block is frozen as of harness creation; any change
invalidates runs made under the prior rule.

## Operator protocol (who runs it, and the honesty rule)

The headline metric measures the **human operator's** attention. Therefore:
- A single autonomous agent running *both* sides cannot measure operator attention (it reads ~0 for
  both and discriminates nothing). Scored runs REQUIRE a human operator driving each method.
- Operator follows a **fixed protocol** and may NOT rescue GUILD (or the baseline) with clever
  off-script prompting. Every prompt/correction/steer is logged as an intervention.
- If the owner runs it, note the expert-hands bias: intervention counts will read low vs. a cold
  operator. State this in the report.

## Protocol per task

- **Fixed timebox** per task, same for both methods (compares quality-at-equal-time). Open-ended
  time-to-done ONLY for the adversarial speed task.
- Same source materials; no hidden context beyond what the baseline receives.
- **Replication ≥ 2× per method.** If skipped → the deliverable is labeled a **CASE STUDY, not a proof**.
- Reruns/steering logged as **REWORK** — never counted as first-pass. Do not fix GUILD mid-task and
  count the fixed rerun as baseline speed.

## Tasks (real material — Nourish app / live Hall; no toys unless marked calibration)

| # | Task | Turf | Timebox | Real material |
|---|------|------|---------|---------------|
| 1 | UX/design critique of a screen | GUILD home turf | fixed | Nourish screen / Hall surface |
| 2 | IA / flow / feature-structure planning | GUILD home turf | fixed | Nourish feature area |
| 3 | Pre-handoff QA / implementation-readiness review | GUILD home turf | fixed | Nourish component/screen |
| 4 | **ADVERSARIAL (mandatory)** — "in 2 min, the single most important thing wrong with this screen?" | expected GUILD LOSS | open-ended speed | one screen |

Briefs in `tasks/`. Task 4 is mandatory; skipping it makes the benchmark cherry-picked.

## Folder map

```
efficiency-benchmark/
  README.md            ← this file (protocol + LOCKED win rule)
  rubric.md            ← quality rubric, LOCKED before any scoring
  tasks/               ← 4 task briefs
  runs/task-N/{guild,baseline}/run-{1,2}/   ← outputs + raw notes
  logs/                ← timing.csv + intervention-log.md (per run)
  scoring/             ← scoring sheets (scorer ≠ producer)
  report.md            ← final analysis + claim level
```

## Constraints (from the goal)

No cherry-picking (task 4 mandatory) · attention separate from wall-clock · agent runtime never free
· hide no failures/false-positives/unusable recs · reruns = rework · real material unless marked
calibration · win rule + rubric pre-committed.

## Definition of done

- ≥ 3 tasks run end-to-end both methods **incl. task 4**, each ≥ 2× (or report labeled case study).
- Headline reported as attention + interventions per usable deliverable, win rule applied.
- `report.md` states claim level (leans-supported / mixed / leans-against — never "proven", n is small)
  + names the next highest-leverage fix + amortization caveat.
- Validation passes: `npm run validate`, `python3 scripts/guild-hall.py --selftest`, `git diff --check`.
