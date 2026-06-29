# Self-Healing Loop (MAPE-K)

**GUILD-2 · P1 autonomy — the category's new center of gravity.** Turns Guild from
one-shot into a standing watcher that detects design drift and self-repairs
*before* a human sees it. Depends on GUILD-1 (manifest = `docs/guild/context.yaml`),
GUILD-3 (trust tiers), GUILD-12 (hard stops), GUILD-4 (scored QA).

## Loop (Monitor · Analyze · Plan · Execute · Knowledge)
1. **Observe** — capture live state: Playwright/atrium browser (DOM, computed styles, screenshots), Figma API (variables/components), CI hooks, usage analytics where available.
2. **Detect** — score drift against the baseline manifest (`context.yaml` baseline+tokens, the design system): token misuse, WCAG/a11y regressions, doc drift, detached/duplicate instances. Each drift = a **scored finding** via `qa-tiers.yaml` (deterministic/validated gate; exploratory advisory).
3. **Suggest** — turn gating findings into concrete recommendations.
4. **Fix** — apply per `trust.yaml`: `senior`+deterministic → auto draft-PR; `junior` → write + draft-PR; `intern`/irreversible/foundation-guard → suggest only (Healer/BMAD story). Never touch a foundation guard.
5. **Learn** — record each accept/reject to `{output_root}/guild-artifacts/qa-calibration.yaml` to sharpen future suggestions (feeds GUILD-4 calibration + GUILD-14 taste model).

## Pre-human self-repair (the headline behavior)
Within the `trust.yaml` tiers AND the `definition-of-done.yaml` hard stops
(max_iterations, no_progress, budget), the loop **iterates Detect→Fix internally**
until DoD passes or a hard stop trips. The owner is shown the **converged result
(attempt N)** in the GUILD-11 batched review — NOT every intermediate pass
(1..N). If a hard stop trips before DoD, it escalates with the specific blocker.

## Modes
- **On-demand:** `/guild-self-heal` (or the `/guild-design-sprint` loop variant).
- **Schedulable:** an atrium cron / CI hook runs Observe→Detect on a cadence; gating drift opens a draft-PR or a Healer story per trust tier.

## Done when
- Drift detector compares the baseline manifest vs live Figma/tokens/code/DOM and emits scored findings.
- Approved fixes generate a draft PR or Healer story, gated by trust tiers.
- Accept/reject outcomes are recorded for Learn.
- TEST: the owner sees the converged attempt N (one batched packet), not passes 1..N; a foundation-guard drift is never auto-fixed.
