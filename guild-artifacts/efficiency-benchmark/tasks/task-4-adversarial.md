# Task 4 — ADVERSARIAL (mandatory): the 2-minute glance

**Purpose:** expose where GUILD is expected to LOSE. A fast, low-ceremony judgment call where a human
(or plain prompt) glance likely beats a multi-step pipeline. Skipping this task makes the whole
benchmark cherry-picked — it is NOT optional.

**Real material:** Nourish `src/app/onboarding/page.tsx` rendered at `localhost:3000/onboarding`,
mobile width (390). One screen, one screenshot.

**Timebox:** **open-ended time-to-answer** (this is the speed test — the only open-ended task).
Record wall-clock AND operator attention to first usable answer.

**The question (identical to both methods):**
> "In 2 minutes or less — what is the single most important thing wrong with this screen? One answer."

**Required output format:** ONE issue + one-line why. Anything longer is penalized as missing the
brief (the brief demands a single answer).

**Method paths:**
- **GUILD:** whatever the routine Hall path is for a quick look. If the shortest GUILD route still
  spins up an agent/pipeline, that IS the finding — log the ceremony cost.
- **Baseline:** same model, plain prompt: the question verbatim.

**Quality criteria:** did it name a real, top-tier issue? (Q2 correctness + Q3 specificity only —
coverage does NOT count here; a long thorough answer is a FAIL against the brief.)

**Headline for this task:** **time + interventions to first usable single answer.** GUILD likely loses
on ceremony; if it wins, that's a strong signal. If it loses, that's the honest boundary of where the
scaffolding helps — name it plainly in the report.
