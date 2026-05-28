# Design Surface Modes — the pluggable front end over a shared spine

Guild treats the **design system as a token/contract layer**, not as something that lives inside any one
tool. Figma, Claude Design, code, and Storybook are all *projections* of that layer. The `design_surface`
setting in `guild.config.yaml` selects which **front-end sync adapters** are active; it does **not** change
the spine.

## The invariant (true in every mode)

The spine is ALWAYS active, regardless of `design_surface`:

- **Tokens** — W3C DTCG, primitive → semantic tiers.
- **Primitives** — the component contracts; screens compose them, never redefine them.
- **Contrast gate** — WCAG AA on every status + body-text pair (Sage DSF, step 4b).
- **Coherence gate** — 0 raw hex/px in screens, 0 inlined components, screens import primitives.
- **Motion layer** — tokenized motion + interaction-state coverage (Sage DSF, step 4c).

Only the **input adapter** changes per mode — i.e. *where the tokens come from* and *what artifact the
gate parses*. The gate math is identical; a Figma-variable resolver, a Claude Design bundle parser, and a
raw-CSS reader all feed the same WCAG/coherence checks.

## Modes

| Mode | Design surface(s) | Active front adapters | Tinker Figma menu | Handoff-bundle gate | Canonical default |
|---|---|---|---|---|---|
| `figma` | Figma | Figma→DTCG (`tinker-tokens`), Code Connect | **shown** | off | figma |
| `claude-design` | Claude Design | handoff-bundle parser, CD-ingest check | **dormant** | **on** | tokens |
| `both` | Figma + Claude Design | all of the above | **shown** | **on** | **must be declared** |
| `greenfield` | none (code only) | none | **dormant** | off | tokens |

## Detection (when `design_surface: auto`)

Mirror the `bmad_mode` detection pattern:

1. Figma plugin/MCP available **or** Code Connect files (`*.figma.ts` / `*.figma.tsx`) exist → `figma`
2. A Claude Design handoff bundle (tar with component-spec + tokens + README) or a linked CD org system is present → `claude-design`
3. Both signals present → `both`
4. Neither → `greenfield`

## `canonical_source` — the anti-drift rule

Every surface syncs to ONE source of truth. The danger mode is `both`: Figma variables, Claude Design's
auto-generated system, and the repo tokens can each drift independently — three "sources of truth" is worse
than one tool alone.

- **`figma`** — Figma variables are truth. `tinker-tokens` exports them to repo DTCG, which then feeds both
  code and Claude Design's codebase ingestion. Designers keep working in Figma.
- **`tokens`** — the repo's DTCG token file is truth. Figma variables and Claude Design's system both derive
  from it. Tool-agnostic; the cleaner long-term anchor.

In `both` mode, `canonical_source: auto` is **not acceptable** — the agent must require an explicit
`figma` or `tokens` choice before proceeding. Refusing to disambiguate here is the whole point.

## Who reads this

- **Tinker** — gates its Figma menu. In `claude-design`/`greenfield` Tinker's Figma component tooling is
  dormant; its surviving concerns (token export, WCAG) are handled by the canonical layer + Sage's gate.
- **Sage** — selects the DSF gate's input adapter: Figma variables (`figma`, via `tinker-wcag.md`), the
  Claude Design handoff bundle (`claude-design`/`both`, via `claude-design-handoff-gate.md`), or repo tokens
  (all modes, via `design-system-foundation.md` step 4b). The contrast + coherence checks themselves are
  unchanged across modes.
- **Healer** — when a gate FAILs, remediation targets the `canonical_source`, never a per-screen override.
