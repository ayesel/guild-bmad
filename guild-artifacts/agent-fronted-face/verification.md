# Agent-Fronted Face Verification

Screenshot: `guild-artifacts/agent-fronted-face/playbook-agent-first-1440.png`

## Live Hall Check

- URL: `http://localhost:4400/playbook?p=4`
- First Playbook section: `Talk to an agent`
- Agent rows visible: 9
- Manual command disclosure: `Manual command surface (25)`
- Manual command rows inside disclosure: 25
- Retired catalog language absent: `command catalog`, `Every command Guild knows`, `full catalog`

## Install Hardening

- `scripts/guild-global-install.sh` now removes stale global `guild-*` command files before copying current commands.
- Generated Atrium `guild-*` skills are pruned before reinstall, so retired command skills do not survive.
- `scripts/install.sh` now removes stale project-local `.claude`, `.cursor`, and `.gemini` `guild-*` command files before copying current commands.

## Gates

- `python3 -m py_compile scripts/guild-hall.py scripts/command-surface.py scripts/token-footprint.py`
- `python3 scripts/guild-hall.py --selftest`
- `python3 scripts/command-surface.py --check`
- `bash -n scripts/guild-global-install.sh scripts/install.sh scripts/validate.sh`
- `npm run validate`
- `git diff --check`
