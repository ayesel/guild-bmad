# Artifact Cards + Run Monitor (UI)

**GUILD-20 · P4.** Live artifacts + background runs need visible navigation +
steering — but the UI must RENDER the repo IA, not become a parallel store.
Owner: Mage + Cartographer. Rendered via atrium notes/canvas (see the atrium skill).

## Surface
- **Navigation:** Project → Epic → Run → Artifact → Story.
- **Artifact card** (one per `docs/guild/artifacts.yaml` entry): state badge · open-buttons (Figma / prototype preview / Storybook / repo file / linked BMAD story) · version selector · produced-by run (`source_run_id`) · QA summary (Sage/Tinker/Rogue gates) · "create/update BMAD story" action.
- **Live preview:** Mage/Tinker spin up an ephemeral atrium dev-server and attach the preview URL to the story frontmatter (GUILD-7 / GUILD-17).
- **Run monitor:** the GUILD-19 registry (`docs/guild/runs/RUN-*.yaml`) as a board — status, trace, exceptions queue, handoff readiness — with the steering controls from `RUN-schema.yaml` (gated by `trust.yaml`).

## Hard rule
**Nothing canonical lives only in the UI.** Cards/board are a *projection* of the repo manifests (`artifacts.yaml`, `runs/RUN-*.yaml`); the repo stays the source of truth. The UI reads + steers; it never owns data.

## Done when
- Artifact cards render from artifacts.yaml (not app-only state); open-buttons deep-link to each artifact's native home.
- Run monitor renders RUN-*.yaml with steer controls.
- Ephemeral preview servers attach URLs to story frontmatter.
- TEST: cards render from artifacts.yaml; the monitor steers runs; nothing canonical is UI-only.
