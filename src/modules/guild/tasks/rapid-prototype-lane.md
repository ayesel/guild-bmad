# Rapid-Prototype Lane (GUILD-34)

A fast/cheap generation lane for Mage's Divergence Engine (GUILD-21): drive
**GPT-5.5 in an atrium browser pane** to produce N distinct ON-SYSTEM UI
prototypes, capture them, run the validity sieve, and graduate the winner to a
**Claude** production build.

> Division of labor: **GPT-5.5 = breadth / throwaway exploration; Claude = the
> production build of the winner only.** Stop spending Claude cycles on dead-end
> ideas.

## How it runs
`scripts/guild-prototype-lane.py --component "<request>" [--n 3] [--pane <id>]`

1. **Build prompt** from `docs/guild/{context,design-system,morphology-matrix}.yaml`
   so GPT diverges on-system (Product Baseline triggers + Hearth Works tokens +
   morphology axes) — not generic.
2. **Drive the browser** — type the prompt into the GPT-5.5 composer, send, wait
   for generation, capture the fenced `html` blocks (reuses the same browser-
   automation pattern as the Winter Bloom render agents). Uses a FRESH chat so it
   never touches the owner's other conversations.
3. **Sieve** (GUILD-24 spirit) — validity floor first: self-contained (inline
   `<style>`, no external/CDN/framework), size sane, on-brand, Baseline coverage
   (search/filter/sort, states). Invalid candidates are discarded.
4. **Graduate** — a single clear winner graduates. **On a tie, the lane does NOT
   pick on taste** — it hands survivors to the multi-judge **tournament**
   (`tournament.md` / GUILD-13: Mage/Sage/Tinker Pareto) for the real selection.
   Only the winner goes to the Claude build.

## Boundaries
- The deterministic sieve is a *floor*, not a taste judge — selection among valid
  survivors is the tournament's job.
- Throwaway prototypes land in `guild-artifacts/prototypes/` (gitignored); only
  the graduated winner becomes a tracked artifact when Claude builds it.
- Requires a logged-in GPT-5.5 browser session; the driver opens a new pane.
