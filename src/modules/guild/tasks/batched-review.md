# Batched Human-Delta Review

**GUILD-11 · P1 autonomy.** The ONE human touchpoint at the end of a run. Replaces
every mid-run "what do you think?" with a single decision-oriented packet, so the
owner reviews once instead of being pinged serially.

## When to run
- LAST step of a quest/sprint, after the pipeline produces its result, before "done".
- Only surfaces when `raid-charter.yaml` `review.mode: batched` (the default).

## What it shows (decision-oriented, NOT an artifact dump)
Cap at `charter.review.max_items` (default 7). Include ONLY:
1. **Final recommendation** — the chosen result, one line + link to the artifact.
2. **Rejected alternatives** — what else was considered and the one-line reason each lost (so the owner can override with context).
3. **Decisions taken under defaults** — every place the run acted on an `autonomy_level` default instead of asking (the parked items from `raid-charter.md`), each with the default chosen.
4. **Unresolved high-risk / irreversible items ONLY** — the things that genuinely need a human (destructive, costly, externally-visible, or outside the charter).

Do NOT include: routine artifacts, anything the charter/context already settled, low-risk choices already defaulted (list those under #3 as FYI, not as questions).

## Format
Each item is **decision-oriented**: a clear ask with Approve / Edit / Reject. Prefer an atrium canvas or a compact checklist. No prose essays.

## Done when
- One packet presented; ≤ max_items; every item is approvable/editable/rejectable.
- TEST: across the whole run the owner saw exactly ONE review (this packet), not per-phase prompts; the packet contains deviations + unresolved risks, not an artifact dump.

## Persona-capped review packet (GUILD-76/77)
Cap the decision-packet size by operator persona (`scripts/operator-profile.py` -> `scripts/persona-elicit.py`): **regular <=3**, **power <=7**, **designer unlimited**. Gate any irreversible decision through `scripts/reversibility-gate.py` — it pauses for confirmation regardless of autonomy level.
