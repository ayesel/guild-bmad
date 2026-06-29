# AGENTS.md — Guild autonomy governance

How much each Guild agent may do without asking. Machine-readable source:
[`docs/guild/trust.yaml`](docs/guild/trust.yaml). This file is the human-readable
contract; the loop, QA gating, and Definition-of-Done read the YAML.

## Trust tiers (graduated)
| Tier | May | Never | Scope |
|---|---|---|---|
| **intern** | suggest | write, merge | recommendations only |
| **junior** | suggest, write | merge | mechanical / deterministic fixes (token swap, spacing, `target=` repair) |
| **senior** | suggest, write, merge | — | deterministic + *validated* checks only; never foundation guards |

Each agent has a default tier **per action class** (e.g. Sage gates deterministic
checks at `senior` but exploratory critique at `intern`). See `trust.yaml`.

## Foundation guards (never auto-overridable)
- Product Baseline triggers (T1–T8) and contrast / WCAG AA gates are never auto-waived.
- No destructive / irreversible action (delete, force-push, external publish, spend) without explicit human approval.
- No change to `context.yaml` taste/tokens without owner sign-off.

## How autonomy flows together
- **GUILD-11 charter** sets the run's `autonomy_level` (high/medium/low) — the ceiling.
- **trust.yaml** sets each agent's per-action tier — the floor per action.
- The effective permission = the *lower* of the two. Anything above it is **parked** to the exception queue and surfaces in the batched review (never a serial prompt).
- **GUILD-12** stops the loop (DoD met, or a hard stop); **GUILD-2** self-repairs within those limits before any human sees it.

## Per-workspace override
Drop a `guild.trust.yaml` at the project root to raise/lower tiers as trust in
the agents grows. Foundation guards still apply.
