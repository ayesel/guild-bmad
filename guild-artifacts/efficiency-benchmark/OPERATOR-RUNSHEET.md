# Operator Run-Sheet — how you (the owner) run a scored task

You run. I (Claude) log. You do NOT touch the CSV or intervention files mid-task — that bookkeeping
would add to the very attention we're measuring. Just narrate; I timestamp and record.

## Your only job per run

1. Tell me: **"START task N, <method>, run R."** I stamp t=0.
2. Do the task through that method, using ONLY the brief's inputs (I'll paste them).
3. Every time you have to prompt / correct / steer / restart — just say it naturally. I log each as an
   **intervention** with a timestamp. (You don't have to say "intervention" — I detect and confirm.)
4. When you have a usable deliverable (or you give up), say **"DONE"** (or "GAVE UP"). I stamp elapsed.
5. I ask you two numbers only: **your attention-minutes** (how long YOU were actively engaged, not
   wall-clock) and a gut **usable? y/n**. I compute the rest from the log.

## Fixed protocol (don't rescue a failing method with cleverness)

- Stay within the brief's inputs. If a method needs more, that's a finding — tell me, don't quietly feed it.
- Keep to the task's timebox (Task 1: 20 min, Task 2: 30, Task 3: 25, Task 4: open/speed).
- If you improve GUILD mid-task, that's **rework** — I log the rerun separately; it does NOT count as
  first-pass.

## Run order (counterbalanced — reduces learning/order bias)

| Task | Run 1 | Run 2 |
|------|-------|-------|
| 1 | baseline first, then GUILD | GUILD first, then baseline |
| 2 | GUILD first | baseline first |
| 3 | baseline first | GUILD first |
| 4 | baseline first | GUILD first |

Rationale: whoever goes first learns the screen and speeds up the second method. Alternating cancels
the systematic advantage. Same-operator/same-screen replication still has a learning effect — I note it
in every run so a run-2 speedup isn't misread as a method win.

## Scoring (after all runs of a task)

Ideally a scorer who didn't operate scores the outputs from `rubric.md`, source hidden. If it's just
you, score with the blind-guess check filled in — we treat quality as suggestive, not clean (per rubric).

## What I produce as we go

- `logs/timing.csv` — one row per run, filled live.
- `logs/task-N-<method>-run-R.md` — the intervention log for that run.
- `runs/task-N/<method>/run-R/output.md` — the actual deliverable.
- At the end: `report.md` filled, win rule applied, claim level set.

**Ready when you are. Say "START task 1, baseline, run 1" and I'll paste the Task 1 inputs and stamp t=0.**
