# `docs/guild/` — Guild's machine-readable registry

This directory is the **machine-readable home** that downstream Guild capabilities read and write. Humans author the prose sources (e.g. `src/modules/guild/agents/shared-sidecar/product-baseline.md`); the artifacts here are the *structured projection* agents and dev tooling consume so they don't re-ask what's already decided.

> Scaffolded by **GUILD-26** (P0 step 01). Populated by the cards below — do not hand-author the generated files; regenerate them from their source.

## Contents (filled in by later build steps)

| File | Owner card | Generated from | Purpose |
|---|---|---|---|
| `context.yaml` | GUILD-1 | `product-baseline.md` + brand/taste anchors + DTCG token pointer | Single context a run loads so it does NOT re-ask brand/taste/baseline. |
| `registry.yaml` / entity model | GUILD-16 | artifact files + `artifacts.yaml` schema | Typed registry of every Guild artifact (personas, flows, tokens, specs…). |
| `artifacts.yaml` (schema) | GUILD-16 | — | Schema that validates the registry. |
| `runs/RUN-*.yaml` | GUILD-19 | live agent runs | Run registry (rendered as atrium tasks; steerable). |

## Conventions

- **Single source of truth.** Each generated file names its source in a header comment. Never edit a generated file by hand — change the source and regenerate (this is the same drift trap that bit the compiled agents; see `scripts/sync-compiled.py`).
- **Story-frontmatter seam (GUILD-17).** BMAD/dev stories carry a `guild:` YAML frontmatter block pointing at the artifacts here, so a dev agent reads design context *from the story* without a separate handoff. The round-trip is proven by `scripts/selftest-roundtrip.sh`.
- **Reachable from any cwd.** Per the global-install fix (commit 710aefb), sidecars/tasks/templates resolve to absolute paths in the global install, so agents read this registry regardless of working directory.
