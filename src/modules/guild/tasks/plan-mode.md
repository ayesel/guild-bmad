# Plan Mode

**GUILD-8 - first-class approve-before-generation gate.** Before a generation run,
show the owner a concise plan and require an explicit approve/edit/reject decision.
Generation proceeds only on approval.

Plan Mode is the interactive sibling of **GUILD-11 Raid Charter**:
- `raid-charter.md` is the durable spec-once contract for the run.
- `plan-mode.md` is the just-in-time approval gate before a concrete generation step.

## When to run
- Before generating screens, artifacts, handoffs, copy, prototypes, or code from a
  prompt where scope or output shape could drift.
- Default-on for creative generation and high-impact output.
- Skip only when the Raid Charter or a prior approved plan already names the same
  scope, approach, and produced files for this exact generation step.

## Procedure
1. **Load the durable spec first.** Read `raid-charter.yaml` when present, plus
   `docs/guild/context.yaml` and any relevant task inputs. Do not re-ask settled
   charter/context questions.
2. **Emit one concise PLAN** with exactly:
   - Scope: what this generation will cover.
   - Approach: how the work will be produced.
   - Will produce: the files/artifacts/screens expected.
3. **Ask for one decision:**
   - `approve` - proceed with generation.
   - `edit` - stop generation and revise the plan.
   - `reject` - stop generation and return to scoping.
4. **Gate execution.** Run `scripts/plan-gate.py` or equivalent gate logic. Only
   `approve` allows the generation command to run. `edit` and `reject` are hard
   stops for the current generation attempt.

## Output contract
- The plan must be short enough to review quickly.
- The plan must name concrete outputs, not vague activity.
- The plan must not hide irreversible, external, or high-cost actions.
- The decision and approved plan should be recorded in the run log or artifact
  metadata when available.

## Done when
- A plan exists with scope, approach, and produced outputs.
- The owner decision is recorded as approve/edit/reject.
- TEST: `python3 scripts/plan-gate.py --selftest` passes, proving generation only
  proceeds on `approve`.
