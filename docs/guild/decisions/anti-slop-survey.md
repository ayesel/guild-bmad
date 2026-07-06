# Anti-Slop Survey — Reconciled Verdict (v1, 2026-07-06)

Reconciliation of two independent deep-research surveys of wild slop-prevention
mechanisms, graded against GUILD's declared baseline (the prompt carried the
baseline into the search — both reports returned NOVEL/CORROBORATES verdicts
per technique). Raw reports:
`guild-output/guild-artifacts/research/anti-slop/reports/` (chatgpt.md,
claude-report.md). The Claude report is the stronger of the two — it ran
primary-source verification and *debunked* two circulating numbers (the
"Tessl 1.59x Impeccable benchmark" fails verification and is arithmetically
inconsistent; the "~500-token prompt-bloat threshold" is a lean-prompt target,
not an empirical finding — real degradation data sits near ~3,000 tokens).
Disagreements kept, not averaged.

---

## 1. Verdict

The wild has converged on three mechanism families GUILD does not have, and
one empirical finding that challenges a GUILD habit:

1. **Negative constraints beat positive guidance** — the single most important
   result in either report. A controlled study (arXiv 2605.04361 "When Context
   Hurts") found anti-pattern lists produce the largest single improvement of
   any context artifact with the least exploratory damage; a separate
   controlled component test (Solo Studio) found written "be distinctive"
   guidance scored *equal-to-worse than no skill* on 5 of 6 components — the
   model reads "be distinctive" as "add more," and more is the slop. Only
   mechanical gates reversed failures. **Implication for GUILD: our
   aspirational prose in agent rules is unmeasured and possibly negative;
   our gate-heavy posture is vindicated, but we lack banned-pattern lists.**
2. **Deterministic slop-fingerprint scanning** — a verification axis orthogonal
   to everything we gate. Krebs' open-source `ai-design-checker` (1,590 pages
   scored, 15 deterministic DOM/CSS patterns, 165 ground-truth labels, ~5–10%
   false positives): Inter-hero, vibe-purple, glassmorphism, colored left
   borders, icon-topped card grids, badge-above-hero-H1. We gate correctness
   (contrast/geometry/tokens/states); nobody's gate catches *aesthetic
   genericness* — this one does, without an LLM judge.
3. **Portable design-context files with maintenance primitives** — Google's
   now-open-source DESIGN.md spec (lint + diff as first-class CLI verbs),
   tool-native adapters (v0 safe-component surfaces, Figma Make kits). GUILD
   has the content (design-system.yaml, tokens.dtcg, product baseline, charter)
   but not the *portable single artifact + lint/diff* packaging.

Where GUILD is **ahead of everything surveyed** (both reports, explicitly):
cross-screen/flow-level consistency gating (named the biggest unsolved gap;
"this is where your deterministic-gate strength is most differentiated"),
owner-taste calibration, and the over-constraint canary (no source has one —
"you'd be first," and our efficiency benchmark is already its seed).

## 2. Adoption ledger (merged, by convergence strength)

| Mechanism | Sources (A=chatgpt, B=claude) | Verdict | GUILD slot |
|---|---|---|---|
| Anti-reference / banned-pattern lists | A:3 + B:7 + controlled study | ADOPT NOW | Design-direction brief gains an anti-references section; product-baseline gains a banned-patterns block (Inter/Roboto default heroes, vibe-purple gradients, glassmorphism, uniform shadows, bounce easing, colored-left-border cards, icon-topped grids, card-in-card) |
| Deterministic slop-fingerprint gate | A:5 + B:3 (Krebs/Impeccable/Hallmark/Design Auditor) | ADOPT NOW — new gate | `slop-fingerprint-gate.py` modeled on Krebs' 15 patterns (cite the repo, not the blog — repo ships 15, blog says 16); joins the conditional craft suite; never replaced by an LLM judge |
| Brand test + structural-honesty checks | B:2 (OpenAI guidance; Anthropic SKILL.md) | ADOPT NOW — cheap | auto-critique rubric additions: "remove the nav — could this be any brand?"; "do 01/02/03 markers encode a real sequence or decorate?" |
| APCA perceptual contrast | B:2 | ADOPT — supplement | contrast gate addendum for dark themes / thin type (Lc ≥75 body / ≥45 large / ≥30 non-text); WCAG stays the legal AA line |
| Anti-attractor self-enumeration | B:1 (Impeccable v2, self-reported 13→2 anti-patterns/page) | PILOT | one added step in the divergence engine: model enumerates its reflex defaults, then rejects them, before generating variants |
| Positive-guidance A/B canary | B (Solo Studio) + A (Impeccable eval framework) | PILOT — honest self-test | run ab-eval on our own agent prose: same brief with and without the aspirational rules; if prose scores ≤ baseline, cut it and keep gates |
| Job separation (taste → image-model exploration → extract system → build) | A:3 + B:3 (Superdesign; NN/g partial) | PILOT | maps onto the GUILD-34 prototype lane; image-model exploration proposes layouts coding agents avoid |
| Persona/seed diversification in generate-N | B:2 (arXiv 2504.13868 — stories, not UI) | PILOT — measure against gates | divergence engine variant seeding; unproven for UI, may raise clutter |
| Portable DESIGN.md packaging | A:5 + B:2 | WATCH | Google spec is alpha; GUILD's content already exists — adopt the lint/diff idea (validate-style checks on design-context files), skip the format churn until it stabilizes |
| Mock-data-first prompting | A:2 + B:3 | ALREADY COVERED-ish | product baseline reads data shape; formalize "realistic sample data, never lorem" as an explicit baseline line |
| Specialized UI models (Base44) | A:2 | WATCH | claims ahead of public proof ("outputs didn't differ dramatically") |

Corroborated (no action, confidence raised): component-first generation,
reference/style-name anchoring, separated critique (same-agent self-review
"mostly useless"), token-drift gates, states/a11y injection at generation
time, two-model write-then-review, live component mapping via MCP/Code Connect.

## 3. Disagreements (kept)

1. **Constraint volume** — specificity helps; bloat hurts. Real line: context
   rot degrades reasoning around ~3k tokens of low-signal material; the fix
   both camps converge on is *structured, modular* context (skills/files/
   detectors) over inflated inline prose. GUILD's trigger-table/lazy-load
   posture matches; the token-footprint budget is the right guard.
2. **LLM-as-judge for aesthetics** — scalable-default camp (~85% human
   agreement, general-purpose) vs Krebs' refusal ("introduces the exact bias
   you are trying to measure"). GUILD position stands: deterministic detectors
   gate; the jury is pairwise, owner-calibrated, and advisory until 0.70 —
   never a solo aesthetic grader.
3. **shadcn: customize or abandon** — its defaults are THE dominant
   fingerprint; one camp re-tokens it, the other says using it at all risks
   the tell. House: allowed with mandatory re-tokening; the slop-fingerprint
   gate arbitrates empirically.
4. **Full-page vs component-first** — resolved as phasing, not contradiction:
   image-model whole-layout exploration for divergence, component-first for
   build.

## 4. Gaps (where nobody has answers — GUILD's differentiation targets)

1. **Cross-screen homogenization/drift** — every screen locally correct,
   collectively identical or fragmenting. Impeccable admits per-generation
   scope. GUILD's equivalence-check + token gates are the closest thing in
   existence; a flow-level consistency gate (token usage + component
   equivalence + terminology + elevation hashed across a whole flow) is the
   named build.
2. **Product judgment** (emphasizing the wrong thing) — GUILD's IA lane +
   mental-model research is the bet; nobody else is even structured for it.
3. **Over-constraint degradation canary** — Solo Studio proved the failure is
   real and measurable; no one has productionized detection. The efficiency
   benchmark + ab-eval are the seed. "You'd be first."
4. **Novel-slop drift** — fingerprint sets are a moving target; detectors
   catch known tells only (~5–10% FP already). Treat the pattern list like a
   virus-signature file: versioned, periodically re-harvested.

## 5. Provenance notes

- Report B debunked the circulating Impeccable "Tessl benchmark" (secondhand
  only, arithmetically inconsistent, registry conflict-of-interest) — use
  Bakaus' self-reported 13→2 anti-pattern delta instead, labeled self-reported.
- Video/podcast angle came back thin in both reports (course marketing, no
  extractable timestamped technique) — angle honestly under-covered, not
  under-searched.
- Nearly all sources 2025-Q4→2026; nothing load-bearing is stale.

---

*Reconciled 2026-07-06 (Fable). Next: forge-queue the Stage-1 items
(banned-pattern block, slop-fingerprint-gate.py, brand/structural-honesty
rubric lines, APCA supplement) and the positive-guidance A/B canary — the
one that tests our own prose.*
