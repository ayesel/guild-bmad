# Quality Rubric — LOCKED before any scoring

Frozen as of harness creation. Written **before** any output was produced, so it cannot be tuned to
flatter either method. Scorer must NOT have produced the output being scored.

## Scoring

Each dimension scored **0–4**:

- **0** — absent / wrong
- **1** — present but weak, mostly unusable
- **2** — usable with meaningful rework
- **3** — usable, minor polish only
- **4** — excellent, ship-ready

## Dimensions (equal weight unless a task brief overrides)

| # | Dimension | What "4" looks like |
|---|-----------|---------------------|
| Q1 | **Completeness** | Covers the task's required scope; no major omissions |
| Q2 | **Correctness** | Claims are true; no hallucinated components/states/APIs |
| Q3 | **Specificity / actionability** | Concrete, do-this-next; not generic advice |
| Q4 | **Evidence grounding** | Findings tied to the actual artifact/source, not assumed |
| Q5 | **Coverage** | Edge states, a11y, responsive, design-system concerns addressed |
| Q6 | **Developer usability** | A dev could act on it without a decoder ring |
| Q7 | **Owner decision usefulness** | Helps the owner make a real decision |

**Task quality score** = mean of Q1–Q7 (0–4).

## "Usable deliverable" gate (defines the denominator of the headline metric)

An output counts as **one usable deliverable** iff task quality ≥ **2.0** AND no Q2 (correctness)
score of 0. Outputs below the gate are logged but do NOT count as delivered — they inflate attention
cost without producing value, which is exactly what the metric should punish.

## Blinding (honest limitation, not a promise)

Attempt to strip "Guild"/"manual" labels before scoring. **But GUILD output is structurally
distinctive** (gate headers, agent voice, length), so a scorer will often guess the source. Do NOT
claim true blind review. Record in each scoring sheet: `blind_guess_correct: yes/no` — if scorers
guess right most of the time, treat the quality comparison as **suggestive, not clean**.

## Anti-gaming notes

- Longer ≠ better. Penalize padding under Q3 (specificity).
- A confident wrong claim (Q2=0) gates the whole deliverable out — better to omit than fabricate.
- False positives / unusable recs are counted separately in `logs/` and drag Q3/Q6.
