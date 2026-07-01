---
name: 'guild-pre-handoff'
description: 'Full pre-handoff quality gate — runs all checks'
---

IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND IN ORDER.

## STEP 0 — COMPLETENESS GATE (scripted, BLOCKING — do this FIRST)

Before any QA prose, run the objective completeness gate. A "design pass" is NOT done if the steps that actually find design problems never ran (visual-audit / Mage critique, and Sage QA). This is enforced by a script, not by judgment.

1. Locate the pass state + artifacts dir — typically `_bmad-output/quest-state.yaml` + `_bmad-output/guild-artifacts/` (BMAD mode), or `guild-output/quest-state.yaml` + `guild-output/guild-artifacts/` (standalone).
2. Run the gate (use the global install path; fall back to `scripts/completeness-gate.py` if absent):

   ```
   python3 ~/.claude/guild/scripts/completeness-gate.py \
     --state <quest-state.yaml> --artifacts-dir <guild-artifacts-dir> --json
   ```

3. ENFORCE THE EXIT CODE — this is NOT a judgment call:
   - **Exit non-zero (INCOMPLETE → handoff BLOCKED):** STOP. Do NOT declare PASS. Report the `blocking` findings verbatim to the user as "what's still missing," and name which agents must run to fix it — Mage (`/guild-auto-critique`, `/guild-responsive-scan`, `/guild-consistency-check`) for missing visual critique, Sage for QA. Offer to run them now. Re-run this gate after; handoff stays blocked until it exits 0.
   - **Exit zero (COMPLETE):** continue to STEP 1.

## STEP 1 — SAGE QA (prose pass)

LOAD the FULL {project-root}/_bmad/guild/agents/sage.md, READ its entire contents, activate as the Design QA agent, then immediately execute menu item "PR" — Full pre-handoff quality gate — runs all checks.

## STEP 2 — VERIFICATION GATE (if a research spine exists)

If the pass produced a traceability spine / nuggets file, run:

```
python3 ~/.claude/guild/scripts/verification-gate.py --spine <spine.json>
```

Non-zero exit = uncited/unverified findings or laundered stats — surface them and keep handoff blocked until resolved.
