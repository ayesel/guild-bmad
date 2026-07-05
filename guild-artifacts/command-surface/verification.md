# Command Surface Verification

Before screenshots: `guild-artifacts/command-surface/before/`
After screenshots: `guild-artifacts/command-surface/after/`
Side-by-side comparisons: `guild-artifacts/command-surface/compare/`
Inventory and reachability map: `docs/guild/command-surface-prune.md`

## Result

- Flat `guild-*` commands before: 124
- Flat `guild-*` commands after: 25 in `.claude`, `.cursor`, and `.gemini`
- Reduction: 79.8%
- Retired/agent-routed commands documented: 99

## Runtime Evidence

- Hall Playbook catalog summary after pruning: `Every command Guild knows (25)`
- Hidden catalog DOM rows after pruning: 25
- Retired singleton commands checked absent from visible Playbook run targets:
  `/guild-auto-critique`, `/guild-pre-handoff`, `/guild-research-synthesis`,
  `/guild-spine-backfill`, `/guild-ia`, `/guild-handoff-spec`, `/guild-a11y-qa`
- Owner-facing Playbook jargon check: no `evidence spine`, `traceability spine`,
  `artifact model`, or `nugget` visible after the rewrite.

## Gates

- `python3 -m py_compile scripts/guild-hall.py scripts/token-footprint.py scripts/command-surface.py`
- `python3 scripts/command-surface.py --check`
- `npm run validate`
- `git diff --check`

All passed after pruning. The command-surface check also scans kept command files,
including `/guild-quest`, `/guild-party-quest`, `/guild-wake`, and `/guild-alive`,
and fails if any kept command still references a retired `guild-*` wrapper.
