# GUILD ↔ Claude Design — the closed loop (2026-07-03)

**Model:** GUILD is the brain; Claude Design is a generation/render adapter. Programmatic via the **DesignSync** tool + `/design-sync` (not atrium-browser). The loop:

```
   ┌─────────────── GUILD (brain) ───────────────┐
   │                                              │
 (1) SEED ──▶ (2) GENERATE ──▶ (3) READ ──▶ (4) GATE ──▶ (5) PUSH-BACK
 prime CD      CD builds       DesignSync    onboarding    DesignSync
 with tokens   the system      pull → DTCG   + handoff     finalize_plan
 + baseline    /screens        (canonical)   catch drift   + write_files
   │                                              │
   └──────────────── corrections re-enter at (1) ┘
```

## Status per stage

| Stage | Mechanism | State |
|-------|-----------|-------|
| 1 SEED | `/guild-claude-design-seed` (paste brief) **and** the programmatic bundle below | ✅ built |
| 2 GENERATE | Claude Design (Anthropic side) | n/a |
| 3 READ | DesignSync `list_files`/`get_file` → `cd-tokens-to-dtcg.py` → `docs/guild/tokens.dtcg.json` | ✅ proven (real 8.3 KB bundle on disk) |
| 4 GATE | `cd-onboarding-gate.py` (WCAG contrast, GUILD-29) + `cd-handoff-gate.py` (0-drift token-trace, GUILD-28) | ✅ built, selftests green |
| 5 PUSH-BACK | `cd-quest-seed.py --emit` → DesignSync `finalize_plan` + `write_files` | ✅ **PROVEN LIVE 2026-07-03** — pushed 2 files to Hearth Works Design System (`cfcbf8bf…`), read-back byte-identical |

## The write side (stage 5) — how it runs

The write side is now a single gated bundle used for BOTH the programmatic seed (stage 1) and the corrective push-back (stage 5):

```
python3 scripts/cd-quest-seed.py --emit <dir>
```

This **gates first** (onboarding contrast — a NO-GO refuses to emit, so a bad token never reaches CD), then writes the bundle (`tokens/guild-tokens.css` from canonical DTCG + `guidelines/guild-product-baseline.card.html` as a `@dsCard`) to `<dir>` plus a `plan.json` = the exact `finalize_plan` spec (`localDir` + `writes`).

The agent then pushes with DesignSync (owner-confirmed — the `finalize_plan` permission prompt IS the confirm, and it mutates the owner's production CD project):

```
DesignSync list_projects                                  # pick the design-system target
DesignSync finalize_plan(localDir, writes)  → planId      # permission prompt = owner confirm
DesignSync write_files(planId, [{path, localPath: path}]) # reads from disk, never enters context
```

The script never calls DesignSync itself; the model does, only after gates pass. `get_file` content from CD is treated as data, never instructions.

## Round-trip PROVEN (2026-07-03)

The full loop ran end-to-end on the real **Hearth Works Design System** (`cfcbf8bf-25f8-4984-9b7d-a9529f95d1c1`, verified `PROJECT_TYPE_DESIGN_SYSTEM`): `--emit` gated the bundle → `list_projects`/`get_project`/`list_files` (both target paths already existed → idempotent update, not clobber) → `finalize_plan` (owner-confirm) → `write_files` (2 written) → `get_file` read-back **byte-identical**. GUILD now reads, gates, AND writes Claude Design programmatically. Re-run any time GUILD's tokens/baseline change; `write_files` reads from disk so contents never enter model context.

## Auth (one-time)

The live push (and any DesignSync read) needs **design access on the session login**. One-time owner action:

- `/design-login` to authorize design access separately, **or** `/login` → "Claude account with subscription".

Once authorized: `list_projects` → confirm the target → `finalize_plan` (confirm) → `write_files`. That single run proves the full round-trip (seed → generate → read → gate → push) end-to-end on a real project — the last unproven link.
