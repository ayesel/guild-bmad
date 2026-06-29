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

## Externally grounded (GUILD-43)
Every **Fix** MUST cite an **external signal** from `docs/guild/self-heal.yaml`
(`wcag_fail`, `token_lint`, `fidelity_diff`, `broken_test`, `state_coverage_gap`,
`baseline_trigger_miss`, `handoff_gate_fail`, `jury_below_calibration`). A repair with
no recognized external signal is **REJECTED** — the loop never self-polishes on
introspection (that loops candidates back to the mean). Exploratory / "looks better"
critique is advisory only: surfaced once in the batched review, never its own
auto-repair round. **Subjective passes are capped at 1**; objective rounds are bounded
by `definition-of-done.yaml` `max_iterations`. Guard: `scripts/self-heal-guard.py`.

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
