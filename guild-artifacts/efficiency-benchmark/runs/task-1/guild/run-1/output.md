# Task 1 — GUILD path (Mage + craft gates) — CASE-STUDY run 1

> **Operator = autonomous agent (proxy), not human.** CASE STUDY, not proof. Same caveats as baseline
> run-1. **Input:** identical (`today-1440.png`/`today-390.png`). **Path:** mage.md CR + mandated craft
> gates actually executed on `apps/nourish/src/app/today/page.tsx`.

## Craft gates — ACTUALLY RUN (this is GUILD's differentiator; here's what it bought)

| Gate script | Result | Value added |
|-------------|--------|-------------|
| `token-lint` | clean — no hardcoded values | none (code already token-disciplined) |
| `spacing-hierarchy` | no flat-spacing findings | none |
| `subtraction-pass` | no over-decoration findings | none |
| `type-conditional` | no flat-type findings | none |
| `affordance-check` | **FIRED** — collection missing search/filter/sort/count/zero-results/row-actions | **MIXED — see below** |

**5 gates run, 4 clean, 1 fired.** Honest read of the one that fired:
- **row-actions — TRUE POSITIVE.** A food log needs edit/delete per entry; worth flagging. (Baseline
  did NOT catch this — real added coverage.)
- **zero-results / empty-state — TRUE-ish.** At 0 entries there's no explicit "no entries yet, add
  one" affordance. Legit.
- **count — FALSE POSITIVE.** "0 ENTRIES LOGGED" in the header IS the count. Gate didn't see it.
- **search / filter / sort — FALSE POSITIVES (the important ones).** A single day's food log is a
  handful of items; search/filter/sort is desktop-table thinking mis-applied by a generic "growable
  collection" rule. Following these would add controls the screen shouldn't have — the exact
  over-building this whole benchmark is checking for. **A dev acting on these wastes time.**

## Critique (Mage 9-area framework)

Findings 1–8 below substantially match the baseline run (wasted desktop space, missing log CTA,
duplicated calorie/protein data, "Room to spare" ×4, "Today" ×2, orphan N avatar, 0-state ring dot,
mobile subtitle wrap). *Not re-listed — see baseline run-1; the core diagnosis is the same.*

**GUILD-only additions beyond baseline:**
- **A11y (framework-driven):** rings must expose value-vs-target text alternatives + meet AA contrast
  (Nourish rule 9). Present as subtitle text — needs contrast measurement (NOT done here; flagged, not
  claimed). **Coverage baseline omitted.**
- **States audit:** entry-list states (empty/populated/loading/error) — only the 0-entries view is
  visible; loading/error unaddressed. **Coverage baseline omitted.**
- **Row-actions** (from affordance-check) — real, baseline missed.

## Honest accounting
- **Added real coverage over baseline:** a11y-alt-text discipline, states audit, row-actions. ~3 real
  extra findings.
- **Added false positives:** search/filter/sort/count (4). A dev would waste time on ≥3 of these.
- **Overlap:** the core 8 findings are identical to baseline — the framework added edges, not a
  different diagnosis.
- **4 of 5 gates produced nothing here** because the code is already disciplined — the ceremony cost
  was paid, the yield was 1 fired gate with a ~40% true-positive rate.
