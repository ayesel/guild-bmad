# Claude Design quest stage (GUILD-32)

Automates Claude Design as a `/guild-quest` stage: **assemble → gate → confirm → push**.
The seed-PUSH writes Guild's system (canonical tokens + Product Baseline) back INTO the
owner's Claude Design project via DesignSync — so it mutates a PROD system and is
owner-gated.

1. **Assemble** — `scripts/cd-quest-seed.py` builds the write plan from `docs/guild/`
   (canonical `tokens.dtcg.json` → CSS + Product Baseline → a CD guideline card).
2. **Gate (catch the bad token at SOURCE, before it propagates):**
   - `scripts/cd-onboarding-gate.py` (GUILD-29) — semantic-pairing contrast on the system.
   - `scripts/cd-handoff-gate.py` (GUILD-28) — 0-drift + WCAG on the bundle.
   A NO-GO blocks the push.
3. **Confirm (owner) — MANDATORY for the first prod write:** the push MUTATES the owner's
   prod CD project (Hearth Works / Arise). Show the write plan (paths + what changes);
   require an explicit owner "push it". For the first real write, verify against a
   safe/known target first. NEVER auto-write prod.
4. **Push** — on confirm + gate GO, execute DesignSync `finalize_plan` (lock the exact
   write paths + localDir) then `write_files`; re-pull (`get_file`) to verify the write
   landed. Log the diff.

> Read-direction (pull → DTCG → gate) is GUILD-27/31/28; this is the WRITE-direction
> (push), authorized by the owner 2026-06-30 (reverses the earlier write-off).
