# Task 1 — UX/design critique of a screen (GUILD home turf)

**Real material:** Nourish `/today` rendered live at `localhost:3000/today`. NOTE: the live app has a
seeded active profile, so the rendered screen is the **populated TodaySurface** (calorie + macro rings
with targets, entry cards) — NOT the cold-start branch. Shared-input screenshots captured for both
methods: `runs/task-1/today-1440.png` and `runs/task-1/today-390.png`. Both methods critique THIS
screen. (The earlier `runs/task-1/*/calibration/` critiques were of the cold-start branch from source —
superseded by these real renders; kept only as harness proof.)

**Timebox:** fixed, **20 min** per method (record actual elapsed regardless).

**Inputs both methods receive (identical):**
- The rendered screen at desktop (1440) + mobile (390) widths (screenshots saved to the run folder).
- One sentence of context: "This is the screen a user lands on daily to log and see today's nutrition."
- Nothing else. No design system docs unless BOTH sides get them.

**Required output format:** a prioritized critique — top issues first, each with (a) what's wrong,
(b) why it matters, (c) a concrete fix. Max 15 findings.

**Method paths:**
- **GUILD:** the agent-fronted critique path (Mage / `guild-critique` / `guild-auto-critique`), whatever
  the Hall surfaces as the routine route. Log which path was used.
- **Baseline:** same model, plain prompt: "Critique this screen's UX. Prioritized, with concrete fixes."
  No Guild commands/agents/gates.

**Quality criteria:** rubric.md Q1–Q7. Coverage (Q5) especially weighs a11y + responsive here.

**Watch for (do not hide):** GUILD false positives (findings about elements not on screen),
generic advice, and rework needed before a dev could act.
