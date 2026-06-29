#!/usr/bin/env python3
"""
guild-canvas.py — the standing Guild -> atrium canvas renderer (GUILD-33 Phase 1).

THE DATA-INGESTION PATTERN: maps the repo-owned docs/guild/ registry into an
atrium canvas spec, so the dashboard is a PROJECTION of the files (no state of
its own). Re-runnable — wire it as a workspace-command on a watch/interval and
it keeps the panel live. This generalizes the one-off "agent patches the canvas"
trick into a reusable renderer.

Reads (relative to cwd, so it works in any Guild project):
  docs/guild/context.yaml     -> baseline health (laws/triggers/domain packs)
  docs/guild/artifacts.yaml   -> artifact cards (id/type/state/version/qa)
  docs/guild/runs/RUN-*.yaml  -> live run rows (id/state)

Modes:
  python3 scripts/guild-canvas.py              # print the canvas spec JSON (pipe it)
  python3 scripts/guild-canvas.py --render     # create-or-update the atrium canvas note (live)

--render persists the note id in docs/guild/.canvas-note-id so repeat runs update
the same panel instead of spawning new ones. Needs $ATRIUM_CLI_PATH.

ACTIONS (data out): buttons fire `send_to_agent` (hand an instruction to a Guild
agent pane, which runs the CLI). NOTE: atrium has no atrium://commands/task.create
or agent.launch verb yet, so spawning tasks/agents routes through send_to_agent.
"""
import os, sys, glob, json, subprocess
import yaml

ROOT = os.getcwd()
GUILD = os.path.join(ROOT, "docs", "guild")
PROJECT = os.path.basename(ROOT)
CLI = os.environ.get("ATRIUM_CLI_PATH", "atrium")
NOTE_ID_FILE = os.path.join(GUILD, ".canvas-note-id")

def load(path):
    p = os.path.join(GUILD, path)
    try:
        with open(p) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}

def gather():
    ctx = load("context.yaml")
    base = (ctx.get("baseline") or {})
    health = {
        "laws": len(base.get("laws") or []),
        "triggers": len(base.get("triggers") or []),
        "packs": len(base.get("domain_packs") or []),
        "taste": "taste_anchors" in ctx,
    }
    arts = (load("artifacts.yaml").get("artifacts")) or []
    art_rows = [{
        "id": a.get("artifact_id", "?"),
        "type": a.get("type", ""),
        "state": a.get("state", ""),
        "ver": (a.get("versions") or [""])[-1] if a.get("versions") else "",
        "qa": a.get("qa_status") or "—",
    } for a in arts]
    run_rows = []
    for rp in sorted(glob.glob(os.path.join(GUILD, "runs", "RUN-*.yaml"))):
        if os.path.basename(rp) == "RUN-schema.yaml":
            continue  # the schema, not a real run
        try:
            r = yaml.safe_load(open(rp)) or {}
        except Exception:
            continue
        run_rows.append({"id": r.get("run_id", os.path.basename(rp)), "state": r.get("state", "?")})
    return health, art_rows, run_rows

def action_btn(key, label, variant, instruction):
    return key, {
        "type": "Button",
        "props": {"label": label, "variant": variant},
        "children": [],
        "on": {"press": {"action": "send_to_agent",
                         "params": {"payload": {"$state": ""},
                                    "framing": "Guild dashboard action: " + instruction}}},
    }

def build_spec():
    health, arts, runs = gather()
    el = {}
    order = []
    def add(key, node):
        el[key] = node; order.append(key)

    add("hdr", {"type": "Heading", "props": {"text": f"🎯 Guild · {PROJECT}", "level": 3}, "children": []})
    add("health", {"type": "Text", "props": {
        "content": f"Baseline: {health['triggers']} triggers · {health['laws']} laws · {health['packs']} domain packs"
                   + ("  ·  taste ✓" if health["taste"] else ""),
        "tone": "muted"}, "children": []})
    add("sep1", {"type": "Separator", "props": {}, "children": []})

    add("runsH", {"type": "Label", "props": {"text": f"RUNS ({len(runs)})"}, "children": []})
    if runs:
        add("runs", {"type": "Table", "props": {
            "columns": [{"key": "id", "label": "Run"}, {"key": "state", "label": "State"}],
            "rows": runs}, "children": []})
    else:
        add("runs", {"type": "Text", "props": {"content": "No active runs.", "tone": "muted"}, "children": []})

    add("artsH", {"type": "Label", "props": {"text": f"ARTIFACTS ({len(arts)})"}, "children": []})
    if arts:
        add("arts", {"type": "Table", "props": {
            "columns": [{"key": "id", "label": "Artifact"}, {"key": "type", "label": "Type"},
                        {"key": "state", "label": "State"}, {"key": "ver", "label": "Ver"}, {"key": "qa", "label": "QA"}],
            "rows": arts}, "children": []})
    else:
        add("arts", {"type": "Text", "props": {"content": "No artifacts registered yet.", "tone": "muted"}, "children": []})

    add("sep2", {"type": "Separator", "props": {}, "children": []})
    add("doH", {"type": "Label", "props": {"text": "DO"}, "children": []})
    btns = []
    for key, node in [
        action_btn("bChart", "+ Charter", "secondary", "run the Raid Charter (raid-charter.md)."),
        action_btn("bDiv", "Diverge", "primary", "run Mage divergence (divergence-engine.md) on the component I name next."),
        action_btn("bQA", "Run QA", "secondary", "run Sage calibrated QA on this project."),
        action_btn("bHeal", "Self-heal", "ghost", "run the self-healing loop (self-healing-loop.md)."),
    ]:
        el[key] = node; btns.append(key)
    add("do", {"type": "Stack", "props": {"direction": "row", "gap": 8}, "children": btns})

    add("root", {"type": "Stack", "props": {"direction": "column", "gap": 12, "padding": 12},
                 "children": [k for k in order if k != "root"]})
    return {"root": "root", "elements": el, "state": {}}

def render(spec):
    note_id = None
    if os.path.exists(NOTE_ID_FILE):
        note_id = open(NOTE_ID_FILE).read().strip() or None
    body = json.dumps(spec)
    if note_id:
        r = subprocess.run([CLI, "note", "write", note_id, "--content", body],
                           text=True, capture_output=True)
        if r.returncode == 0:
            print(f"updated Guild canvas note {note_id}"); return
        print(f"(stale note id, recreating) {r.stderr.strip()[:120]}")
    # create
    r = subprocess.run([CLI, "note", "new", "--type", "canvas", "--title", f"Guild · {PROJECT}",
                        "--source", "agent", "--open", "--spec", "-", "--json"],
                       input=body, text=True, capture_output=True)
    if r.returncode != 0:
        sys.exit(f"note new failed: {r.stderr.strip()}")
    try:
        nid = json.loads(r.stdout).get("meta", {}).get("id") or json.loads(r.stdout).get("id")
    except Exception:
        nid = None
    if nid:
        open(NOTE_ID_FILE, "w").write(nid)
        print(f"created Guild canvas note {nid} (id saved to docs/guild/.canvas-note-id)")
    else:
        print("created note (could not parse id):", r.stdout[:200])

def _watch_sig():
    """Max mtime across docs/guild/ — cheap change signal for --watch."""
    latest = 0.0
    for dp, _, fs in os.walk(GUILD):
        for f in fs:
            if f == ".canvas-note-id":
                continue
            try:
                latest = max(latest, os.path.getmtime(os.path.join(dp, f)))
            except OSError:
                pass
    return latest

def main():
    if "--watch" in sys.argv:
        import time
        last = None
        print("Guild canvas renderer watching docs/guild/ — Ctrl-C to stop")
        while True:
            sig = _watch_sig()
            if sig != last:
                render(build_spec())
                last = sig
            time.sleep(2)
    spec = build_spec()
    assert spec["root"] in spec["elements"], "root element missing"  # well-formed check
    if "--render" in sys.argv:
        render(spec)
    else:
        print(json.dumps(spec, indent=2))

if __name__ == "__main__":
    main()
