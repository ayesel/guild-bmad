# Hall Heaviness Diagnosis

Baseline captured from the live visible Atrium Hall browser before layout edits:

- Screenshots: `guild-artifacts/hall-heaviness/before/`
- Metrics: `guild-artifacts/hall-heaviness/metrics/before.jsonl`

## Ranked Causes

1. **Visible control sprawl is the dominant weight.**
   - Needs-you first viewport: 17 controls at 360, 20 at 768, 29 at 1440.
   - Project list first viewport: 16-23 controls.
   - The global runner band, per-card model selects, queue checkboxes, nav links, and primary buttons all compete at once.

2. **Repeated chrome makes the page read like a control panel.**
   - Needs-you first viewport has 4-7 card/chrome blocks before any deeper scroll.
   - The runner configuration repeats across project list, Needs-you, Playbook, and run surfaces.
   - Recommendation cards repeat icon, chip, queue, model select, button, manual command copy, WHY, and COST.

3. **Copy density overwhelms action hierarchy.**
   - Needs-you copy/action ratio measured 100-129 words per first-viewport action.
   - Playbook and recommendation cards expose rationale and cost before the user asks for detail.
   - The routine action is available, but it sits inside dense explanatory cards rather than reading like a simple inbox item.

## Divergence

### A. Inbox Strip + Details

Collapse runner controls into a compact details element; recommendation cards show title, one sentence, and one primary action. WHY/COST/manual command move into details. Keeps all power one interaction away.

Score: best. Directly reduces control count, copy mass, and repeated chrome without changing behavior.

### B. Command Palette Drawer

Remove Playbook-like command surfaces from cards and place all run actions behind a palette/drawer. Needs page becomes almost purely inbox.

Score: strong but riskier. It could make commands feel hidden and requires more UI/state plumbing.

### C. Split Manager Dashboard

Use a calm status summary up top and push all run controls below the fold. Best visual calm, but routine “run next” becomes less immediate.

Score: rejected. It improves quietness by sacrificing one-click routine action visibility.

## Chosen Treatment

Implement A: progressive disclosure on runner/settings and detail-heavy rationale. Keep primary actions one click. Keep runner/model semantics intact.
