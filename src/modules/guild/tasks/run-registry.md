# Run Registry

**GUILD-19 · P3.** Autonomous / background runs (the GUILD-2 self-healing loop,
async delegation) need first-class IA — a chat transcript can't tell you which run
produced an artifact or let you steer a background agent. Owner: Guild Master.

## What
- Every run writes **`docs/guild/runs/RUN-*.yaml`** (schema: `RUN-schema.yaml`) — portable, survives outside atrium: objective, charter ref, agent roster, linked epic/story/artifacts, trace URI, checkpoints, open exceptions, output manifest, next action, state.
- Each run **also renders as an atrium task** (live monitor + interrupt).
- **Run-state machine:** queued → context-loading → planning → working → self-reviewing → blocked-needs-human → repairing → ready-for-review → handoff-ready → completed/failed/superseded.
- **Steering actions** (continue-with-default · answer-exception · pause/resume/cancel · fork-candidate · promote-version · bind-to-story · request-repair · send-to-BMAD) — each gated by `trust.yaml` autonomy tiers (GUILD-3) + the exception queue.
- **Find-by-artifact:** `artifacts.yaml` `source_run_id` → the RUN file (find the run that produced any artifact).

## Done when
- RUN-*.yaml written on every autonomous run; state machine implemented.
- Runs render as atrium tasks (monitor + interrupt); steering wired to autonomy tiers + exception queue.
- A user can find the run that produced any artifact.
- TEST: a RUN-*.yaml is written, shows as an atrium task, and can be steered.
