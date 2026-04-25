# BMAD Bundle (Standalone Only)

This folder contains BMAD v6 core files bundled for **standalone Guild installations** — projects that don't already have BMAD installed.

## When to use this

**You DON'T have BMAD installed** and want Guild with BMAD integration:
```bash
cp -r bmad-bundle/_bmad/core /path/to/your-project/_bmad/core
cp -r bmad-bundle/_bmad/_config /path/to/your-project/_bmad/_config
cp -r bmad-bundle/.claude/commands/bmad-*.md /path/to/your-project/.claude/commands/
```

## When NOT to use this

**You already have BMAD installed** — do NOT copy this folder. It would overwrite your existing BMAD core, config, and agent manifests. Guild works with your existing BMAD installation automatically.

## What's in here

- `_bmad/core/` — BMAD v6 core agents, tasks, and workflows
- `_bmad/_config/` — Agent manifests and configuration
- `.claude/commands/bmad-*.md` — BMAD slash commands (party mode, reviews, etc.)
