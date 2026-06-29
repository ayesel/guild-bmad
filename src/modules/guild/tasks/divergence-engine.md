# Mage Divergence Engine

**GUILD-21 · P2 novelty — THE core fix.** Guild's generic ("Bootstrap-flavored")
output is a PROCESS artifact: single-shot generation + LLM mode collapse / typicality
bias returns the statistical mean. Fix the process and the novelty appears. **Mage
never single-shots a component** — it generates a wide, structured candidate batch,
then hands it to constrain → score → gate (hosted by the tournament, GUILD-13).

## Diverge (this stage judges NOTHING — spread only)
1. **Verbalized Sampling** — prompt for **N candidates WITH estimated probabilities**, then select for SPREAD (favor lower-probability, far-apart options). +1.6–2.1× diversity, no training, works on all modern LLMs. This is the single highest-leverage move.
2. **4 ideation lanes ("Crazy 32") — run INDEPENDENTLY, hide prior candidates between lanes (branch isolation, fights fixation):**
   - 8 **Crazy-8** rapid sketches
   - 8 **SCAMPER** transforms (substitute / combine / adapt / modify / put-to-another-use / eliminate / reverse)
   - 8 **morphological recombinations** from the GUILD-22 matrix (far-apart cells)
   - 8 **reference-conditioned abstractions** from GUILD-25 (decomposed attributes, never copies)
3. **High-diversity sampling settings** during generation.

## Per-candidate tags (so downstream can constrain + score)
Each candidate carries: invariant contract (the LOCKED fields it honors), DS components used, token family, a11y mode, estimated probability, risk flag.

## Hand-off (never straight to the user)
Diverge → **CONSTRAIN** (GUILD-22 grammar: drop illegal axis values) → **SCORE** (GUILD-24 Fresh+Valid) → **GATE** (GUILD-4 QA tiers) → tournament synthesis (GUILD-13). The owner only sees the converged slate in the GUILD-11 batch.

## Done when
- Mage emits a LABELED candidate batch per request, not one design.
- Verbalized Sampling implemented (candidates carry probabilities); ≥3 isolated ideation lanes wired.
- Each candidate tagged (contract / components / token family / a11y / risk).
- Output flows into constrain→score→gate, not to the user.
- TEST: one component request → N **visibly distinct** candidates (vs single-shot's one averaged result).
