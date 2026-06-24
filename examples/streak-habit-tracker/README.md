# Streak Habit Tracker

This is a public-facing Guild example showing what the framework produces for a real React app: a tokenized design system, working primitives, composed product screens, and the artifacts that explain the design decisions.

Start with `src/system/tokens.json`, then inspect `src/system/primitives/`, and finally open `src/screens/Dashboard.jsx` to see how the token layer and primitives shape the app.

## Run Locally

```bash
npm install
npm run dev
```

## What Is Included

```text
guild-output/
  guild-artifacts/
    design-direction-brief.md
    design-system-foundation.md
    personas.md
    component-registry.md
src/
  system/
    tokens.json
    tokens.css
    primitives/
  screens/
    Dashboard.jsx
    AddHabit.jsx
```

## Guild Artifacts

`design-direction-brief.md` captures the Phase 0 product direction: Linear as the anchor, subtle motion energy, the signature easing curve, and the reduced-motion branch.

`design-system-foundation.md` records the foundation gate report with contrast measurements, token coverage, component coverage, and motion coverage.

`personas.md` grounds the example in two realistic users: Maya the Juggler and Dev the Checklister, both managing cross-project habits in busy parent lives.

`component-registry.md` documents the primitive component contract for Button, Input, Card, and Badge.

## Guild Quickstart

For the broader framework workflow, see the main Guild quickstart in the repository root.
