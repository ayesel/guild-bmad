# Task 3 — Pre-handoff QA / implementation-readiness review (GUILD home turf)

**Real material:** Nourish `src/app/foods/custom/page.tsx` (the custom-food creation form) — a form
screen with inputs, validation, and submission. Good QA surface: states, a11y, error handling,
design-system compliance.

**Timebox:** fixed, **25 min** per method.

**Inputs both methods receive (identical):**
- The rendered screen (desktop + mobile screenshots) AND the component source file.
- One sentence: "This form is about to be handed to a dev as done. Is it implementation-ready?"

**Required output format:** a pre-handoff QA report — pass/fail per area (states, a11y, responsive,
design-system, error handling, empty/loading), each with specific blocking issues vs. nits.

**Method paths:**
- **GUILD:** the pre-handoff gate path (Sage / `guild-pre-handoff` / `guild-system-check` /
  `guild-accessibility`), routine Hall route. Log which.
- **Baseline:** same model, plain prompt: "Do a pre-handoff QA review of this screen for
  implementation-readiness: states, a11y, responsive, design-system, errors. Blocking vs. nits."
  No Guild.

**Quality criteria:** rubric.md, with Q4 (evidence grounding) + Q5 (coverage) weighted — this is where
GUILD's gates should earn their keep if they earn it anywhere.

**Watch for:** GUILD checklist items marked "checked" without evidence (grounding failures), and
false blockers that would waste dev time.
