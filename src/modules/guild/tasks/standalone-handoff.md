# Standalone Handoff (GUILD-61) — the DEFAULT handoff adapter

The default way GUILD delivers a finished design pass when no BMAD pipeline is in play
(`bmad_mode: false` — the default — or `auto` with no `_bmad`). North-star: GUILD is the
brain; this adapter hands off WITHOUT BMAD. Resolver: `scripts/handoff-adapter.py`.
Registry: `docs/guild/handoff-adapters.yaml`.

## Emits → `guild-output/`
- **UX_Design.md** — consolidated design spec (IA, flows, components, states, tokens).
- **component specs + annotations**.
- **standard stories** — plain `title / context / acceptance-criteria` (NOT BMAD format).
- the **canonical artifact set** (`docs/guild/` artifacts + provenance), so any pipeline
  can pick it up.

## Contract
- Reads the canonical artifact model + `output_root` (`guild-output`).
- Produces a handoff bundle consumable by a plain repo / PR / Jira / Linear (each a
  future adapter over the same canonical model).
- Requires NO `sprint-status.yaml`, NO `_bmad`, NO Sally.

## Relationship to the BMAD adapter
The BMAD adapter (`create-handoff.md` + `export-ux-design.md`, `bmad_mode: true`) is the
opt-in equivalent: same contract, BMAD story format + sprint handoff → `_bmad-output/`.
Tasks must call the **resolved** adapter — they must NOT branch on BMAD inline.
