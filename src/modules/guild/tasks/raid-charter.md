# Raid Charter (spec-once)

**GUILD-11 · P1 autonomy.** Capture the owner's intent ONCE at quest start so no
agent re-asks it mid-run. This is the single biggest lever on the owner's
"too much prompting / too many passes" complaint: spec once, review once.

## When to run
- FIRST step of `/guild-quest`, `/guild-design-sprint`, `/guild-party-quest` — before any phase.
- Standalone via `/guild-charter` to (re)establish the contract.
- Skip elicitation if `{output_root}/guild-artifacts/raid-charter.yaml` exists with `signoff: true` and the goal still matches — just load it.

## Procedure
1. **Load what's already known — do NOT re-ask it.** Read `docs/guild/context.yaml` (baseline + taste_anchors + tokens) and any existing `raid-charter.yaml`. Taste/brand/baseline come from context.yaml; the charter only records the per-quest delta.
2. **Elicit ONLY the gaps**, using `templates/raid-charter-template.yaml`. Ask in ONE batched message, not serially:
   - goal (one sentence) · audience · non-goals (what's out of scope) · acceptance criteria (done = …) · autonomy_level (high/medium/default medium) · review mode (default batched).
   - taste/brand: confirm context.yaml in one line ("Using your locked direction — overrides?"); record only overrides.
3. **One sign-off.** Present the filled charter; on owner approval set `signoff: true`. Persist to `{output_root}/guild-artifacts/raid-charter.yaml`.
4. **Announce the contract to the pipeline:** after sign-off, every downstream agent reads charter + context.yaml and is BOUND by the rule below.

## The contract (enforced by Guild Master + every agent)
- After `signoff: true`, **no agent may ask the owner anything the charter or context.yaml already answers.** If an answer exists, use it.
- For anything unspecified: act on the documented default per `autonomy_level` (high → auto all reversible; medium → auto reversible, surface only irreversible/high-risk; low → gate each phase) and **PARK** the decision (with the default taken) for the end-of-run batched review (`batched-review.md`).
- Non-blocking clarifications are NEVER serial "what do you think?" prompts — they go in the batch.

## Done when
- `raid-charter.yaml` exists with `signoff: true`, goal + non_goals + acceptance_criteria + autonomy_level set, taste/brand resolved (via context.yaml + overrides).
- TEST: a subsequent agent in the same run does NOT ask a question the charter/context already answers; deferred items appear in the final batched packet, not as mid-run prompts.
