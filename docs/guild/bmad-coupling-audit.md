# BMAD-coupling audit (GUILD-61 step 1, read-only)

**Verdict: Guild is already ~80% decoupled.** A standalone mode exists and the output
path is already abstracted. GUILD-61 is mostly *formalizing + isolating* the remaining
coupling into ONE optional handoff adapter — not a rewrite.

## Coupling map (by severity)

### ✅ Already adapter-shaped (no work)
- **Config** — `guild.config.yaml` already has `bmad_mode: auto|true|false` and a
  **standalone** path (`false` → `guild-output/`, Guild-only pipeline, standard story
  format). The seam exists.
- **Output paths** — 313 source refs all go through the resolved `output_root`
  variable (auto → `_bmad-output` | `guild-output`). That's the abstraction *working*,
  not hard-coupling.

### 🟡 Medium — inline BMAD branches (isolate behind an interface)
- Dozens of tasks carry "if BMAD present" conditionals (≈5 refs each: BMAD story
  format vs standard, `sprint-status.yaml` checks). Today they're inline; they should
  call a **handoff-adapter** method instead of branching in every task.
- 3 source agents reference BMAD: `healer` (handoff), `guild-master` (orchestration
  detect), `mage` (minor).

### 🔴 High — the actual coupling = the HANDOFF (extract as the adapter)
- `create-handoff.md` (15 refs) + `export-ux-design.md` (10) + Sally-replacement /
  `bmm-ux` / `sprint-status` logic (36 files mention BMAD handoff). This is the real
  BMAD surface and exactly what GUILD-61 should pull out into **one optional adapter**.
- **Toolchain note:** the compiled `_bmad/guild/agents/` path + the external BMAD
  compiler (`sync-compiled.py` assumes `_bmad/`) is a *separate* build-time coupling —
  flag it; don't conflate with runtime coupling.

## GUILD-61 recommendation (core + adapters)
1. **Standalone = the default.** Flip `bmad_mode` default to `false`; BMAD becomes
   explicit opt-in. Auto-detect stays as a convenience, never a dependency.
2. **Extract a BMAD handoff adapter.** Put `create-handoff` / `export-ux-design` /
   BMAD-story-format / `sprint-status` behind a `handoff-adapter` interface. Ship a
   generic standalone handoff (guild-output + standard stories) as the default impl.
3. **Replace inline `if BMAD` branches** in tasks with adapter calls (one seam, not
   N conditionals).
4. **Decouple the toolchain** (separate track): the compiled-agent path shouldn't
   hard-require BMAD's compiler — note as its own sub-task.

Effort: MEDIUM. The hard part (a working standalone pipeline) already exists; this is
promotion + extraction, not new architecture.
