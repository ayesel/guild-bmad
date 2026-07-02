---
name: 'guild-widget'
description: 'Open the live GUILD widget for this project — Now/Journey/Library rendered from the project''s own feed (runs, gates, needs-you, artifacts)'
---

IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND IN ORDER.

## STEP 1 — RENDER

Render the widget for the current project (or the path the user passed as an argument):

```
python3 ~/.claude/guild/scripts/guild-widget.py --project <project-root> --render
```

(fallback: `scripts/guild-widget.py` inside the guild-bmad repo). The data layer (`widget-feed.py`) auto-detects the project shape: `_bmad-output/` or `guild-output/` projects render their quest journey, runs, gate exits, needs-you decisions, and artifact library; the engine repo renders the forge queue; a project with no Guild outputs yet renders an honest empty state — that's correct, not an error.

## STEP 2 — OPEN

The render prints the note id (`created/updated GUILD widget note <id>`). Open it as a pane:

```
"$ATRIUM_CLI_PATH" note open <id>
```

The note is workspace-scoped: run this from the project's OWN workspace so the viewer lives with the project (engine/client separation applies to viewers too).

## STEP 3 — OFFER THE LIVE WATCHER (optional)

Tell the user the widget can self-update: `python3 ~/.claude/guild/scripts/guild-widget.py --project <root> --watch` as a workspace-command (`atrium workspace-command create`) re-renders the note within seconds of any change (new run, gate exit, answered decision). Offer to set it up; don't do it unasked.
