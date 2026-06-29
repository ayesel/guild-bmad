# v4 build partition — Claude (GF) ‖ parallel Codex builder

Conserve Claude quota: Codex builds the **self-contained** tiers in **different files**.
Hard rule: **Codex creates NEW files only** and never edits a file in GF's column.

## ✅ CODEX builds (safe — no overlap with GF's spine/artifact work)
- **T4 RESPONSIVE**
  - 80 `scripts/responsive-gate.py` (NEW) — blocking breakpoint×state matrix
  - 81 fluid tokens → emit a **NEW** file (e.g. `docs/guild/exports/fluid-tokens.css`); **do NOT edit `tokens.dtcg.json`**
  - 82 `scripts/size-class-templates.py` (+ template files, NEW)
- **T5 OPTIMIZATION**
  - 83 `scripts/perf-budget-gate.py` (NEW standalone gate reading `perf-budget.yaml`); **do NOT edit `fidelity-gate.py`** — GF wires it into the fidelity gate in a later reconcile
  - 84 `scripts/runtime-footprint.py` (NEW) — footprint measurement/controls

**Codex rules:** new files only · device-light per `perf-budget.yaml` (read-only) · run `validate.sh` but never edit it · **do NOT edit `package.json`** (GF reconciles all npm/`files` entries) · **do NOT touch `guild-canvas.py`** · one commit per card · verify exit codes independently (no `test && commit`).

## 🔒 CLAUDE / GF owns (Codex stays OUT)
- **T2 artifact engine:** `artifact-model.py` + coming 70 composers / 71 layout-engines / 72 style / 73 figjam / 74 render-adapters · `docs/guild/artifact-model.yaml`
- **T3 profile/personas/taste:** `taste-model.py`, `judge-calibration.py`, `pairwise-capture.py`, `docs/guild/exemplars/*`, `calibration-set.yaml`, operator-profile (new), `scoring.yaml`, `jury.yaml`
- **T1 spine:** `spine.py`, `verification-gate.py`, `confidence-gate.py`, `synthesis-ladder.py`, `living-repo.py`, `ia-evidence-guard.py`, `spine-schema.yaml`
- **GUILD-61/62:** `guild.config.yaml`, `handoff-adapters.yaml`, `handoff-adapter.py`, `create-handoff.md` + the BMAD inline-branch sweep (62 stays with GF — handoff-coupled)
- **`package.json`** — GF reconciles every npm/`files` entry (the #1 collision risk)

## 🤝 SHARED — RUN, don't EDIT (no edits without coordination)
`guild-canvas.py` (active 3rd context) · `validate.sh` · `sync-compiled.py` · `build-context.py` · `tokens.dtcg.json` · `fidelity-gate.py` · `dtcg-export.py`

## Merge hygiene
Codex commits per card on its own files → GF wires npm scripts + `files[]` in a reconcile pass → both run `validate.sh` before push. Distinct file sets = no git conflicts except `package.json`, which only GF edits.
