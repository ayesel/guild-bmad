---
name: 'guild-auto-critique'
description: 'Auto-capture a screen from the running app and critique it — no screenshot upload needed'
---

IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND IN ORDER.

## STEP 1 — CAPTURE + CRITIQUE (Mage)

LOAD the FULL {project-root}/_bmad/guild/agents/mage.md, READ its entire contents, activate as the Mage Visual Designer agent, then immediately execute menu item "AC" — Auto-capture a screen from the running app and critique it — no screenshot upload needed.

## STEP 2 — CRAFT GATES (scripted, BLOCKING — measure, don't eyeball)

After the capture, run the craft gate suite against the screen's REAL files — the component source file(s) behind the captured screen, and the built CSS (`dist/**/*.css`) when a build exists. Use the global install path (`~/.claude/guild/scripts/`); fall back to `scripts/`:

```
python3 ~/.claude/guild/scripts/spacing-hierarchy.py --lint <component-src>
python3 ~/.claude/guild/scripts/subtraction-pass.py  --lint <component-src>
python3 ~/.claude/guild/scripts/type-conditional.py  --lint <component-src>
python3 ~/.claude/guild/scripts/token-lint.py        --file <component-src>
python3 ~/.claude/guild/scripts/state-motion-req.py  --screen <component-src>
python3 ~/.claude/guild/scripts/reduced-motion-gate.py --screen <built-css>   # when a build exists
```

ENFORCE THE EXIT CODES — a non-zero gate is a FINDING, not an opinion: report each finding verbatim in the critique (file, value, suggested token/fix) and mark the critique NO-GO until fixed or explicitly waived by the owner in the batched review. Scripted findings OUTRANK eyeballed impressions; never soften a gate finding into prose.
