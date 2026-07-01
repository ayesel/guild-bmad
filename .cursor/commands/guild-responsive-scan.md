---
name: 'guild-responsive-scan'
description: 'Capture screen at multiple viewports and find responsive issues'
---

IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND IN ORDER.

## STEP 1 — MULTI-VIEWPORT CAPTURE (Mage)

LOAD the FULL {project-root}/_bmad/guild/agents/mage.md, READ its entire contents, activate as the Mage Visual Designer agent, then immediately execute menu item "RS" — Capture screen at multiple viewports and find responsive issues.

## STEP 2 — EMIT THE METRICS (measured from the live DOM, not eyeballed)

Preferred — ONE command (playwright required in the project or globally):

```
node ~/.claude/guild/scripts/responsive-capture.mjs --url <live-url> \
     --out {output_root}/guild-artifacts/responsive-metrics.json [--state "populated"]
```

No playwright? Evaluate `~/.claude/guild/scripts/responsive-metrics.browser.js` (`captureResponsiveMetrics()`) in ANY browser driver at each breakpoint × state and write `{output_root}/guild-artifacts/responsive-metrics.json` in the responsive-gate format:

```json
{"breakpoints": [{
  "name": "compact", "width": 375, "state": "default",
  "scrollWidth": <document.scrollingElement.scrollWidth>, "clientWidth": <clientWidth>,
  "touchTargets": [{"selector": "...", "width": N, "height": N}],
  "textBlocks":   [{"selector": "...", "measureCh": N}],
  "boxes":        [{"selector": "...", "width": N, "height": N, "clipped": bool}],
  "order":        [{"selector": "...", "domIndex": N, "visualIndex": N}]
}]}
```

Capture at minimum: 375 (compact), 768 (medium), 1280 (expanded) — in default AND one data-heavy state.

## STEP 3 — RESPONSIVE GATE (scripted, BLOCKING)

```
python3 ~/.claude/guild/scripts/responsive-gate.py --metrics {output_root}/guild-artifacts/responsive-metrics.json
```

(global install path first; fall back to `scripts/`). ENFORCE THE EXIT CODE — non-zero means real breakage (horizontal overflow, sub-44px touch targets, clipped boxes, >80ch measures, DOM-vs-visual order divergence): report each finding verbatim with its breakpoint × state, fix or file it, and re-run until 0 or the owner waives it in the batched review.
