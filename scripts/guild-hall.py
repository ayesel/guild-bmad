#!/usr/bin/env python3
"""
guild-hall.py — GUILD HALL v1: the delegated-work inbox (mission control).

The owner surface, rebuilt on the researched mental model
(docs/guild/decisions/ui-mental-model-research.md): you are a manager; agents
are teammates you DELEGATE work to; decisions come back as provenance-bearing
cards in an inbox. ONE primitive (the quest/run item); every view is a
non-mutating lens; inbox vocabulary only (Needs you / Runs / Library).

Local-first, zero dependencies (stdlib http.server), device-light. The write
channel is REAL: Approve/Waive records verdicts, Pick executes
regenerate-pick.py (incl. taste capture).

  python3 scripts/guild-hall.py --serve [--port 4400]
  python3 scripts/guild-hall.py --projects           # show the registry
  python3 scripts/guild-hall.py --selftest

Projects registry: ~/.config/guild/hall-projects.yaml (operator-owned).
"""
import os, sys, json, html, time, argparse, importlib.util, subprocess, datetime, threading, uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
UNDO_WINDOW = 8.0   # seconds — deferred commit, same pattern as Nourish's undo toast
PENDING = {}        # token -> threading.Timer
REG = os.path.expanduser("~/.config/guild/hall-projects.yaml")
E = html.escape


def _feed_mod():
    spec = importlib.util.spec_from_file_location("wf", os.path.join(HERE, "widget-feed.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def projects():
    import yaml
    if not os.path.exists(REG): return []
    return (yaml.safe_load(open(REG)) or {}).get("projects", [])


# ── the ONE primitive: a work item ───────────────────────────────────────────
# Everything the HALL shows is a quest/run item: delegated to agents, assigned
# to the owner. Feeds are folded into items with an explicit agent state.

def items_for(feed, proj):
    """Fold a project feed into work items with explicit states."""
    out = []
    for n in feed["needs_you"]:
        out.append({"kind": "decision", "state": "waiting for you", "project": proj,
                    "title": n["title"], "why": n["detail"], "id": n["id"], "link": n.get("link", "")})
    for r in feed["runs"]:
        st = "finished" if r["state"] in ("completed", "done") else \
             "waiting for you" if r["state"] == "ready-for-review" else "executing"
        out.append({"kind": "run", "state": st, "project": proj, "title": r["id"],
                    "why": r["objective"], "id": r["id"], "link": r["path"],
                    "checkpoints": r["checkpoints"]})
    return out



def _calibration_count():
    cal = os.path.join(os.path.dirname(HERE), "docs", "guild", "evals", "calibration-set.yaml")
    if not os.path.exists(cal): return 0
    return sum(1 for l in open(cal) if l.strip().startswith("- {") or l.strip().startswith("- pair"))


def activity_events(wf, regs):
    """Cross-project feed of what agents DID — every row is a door, never just a number."""
    ev = []
    for i, p in enumerate(regs):
        try: feed = wf.build(p["path"])
        except Exception: continue
        for r in feed["runs"]:
            ts = os.path.getmtime(r["path"]) if os.path.exists(r["path"]) else 0
            d = wf._yaml(r["path"])
            last = str((d.get("checkpoints") or ["run recorded"])[-1])[:120]
            ev.append({"ts": ts, "project": p["name"], "pidx": i,
                       "text": f'{r["id"]}: {last}', "href": f"/p/{i}?view=runs",
                       "state": "finished" if r["state"] in ("completed", "done") else "executing"})
        for n in feed["needs_you"]:
            link = n.get("link", "")
            ts = os.path.getmtime(link) if link and os.path.exists(link) else 0
            kind = "waiting for you" if n["id"] != "note" else "for your awareness"
            ev.append({"ts": ts, "project": p["name"], "pidx": i,
                       "text": n["title"], "href": f"/p/{i}?view=needs", "state": kind})
        for it in feed["library"][:4]:
            ev.append({"ts": it["mtime"], "project": p["name"], "pidx": i,
                       "text": f'produced: {it["name"]}', "href": f"/p/{i}?view=library", "state": "finished"})
    ev.sort(key=lambda e: -e["ts"])
    return ev[:22]

CSS = """
:root{--bg:#100f0d;--panel:#1f1b16;--panel2:#282119;--inset:#171512;--line:#2c2820;--line-soft:#221e18;
--ink:#f4ece2;--ink-dim:#aa9c8d;--ink-faint:#7c7063;--ember:#ce5328;--ember-tx:#f3bca1;--ember-deep:#9e3f1e;
--sage:#728b5b;--sage-tx:#b7c9a6;--amber:#c9971f;--denim:#5b7a8b;--denim-tx:#a9c4d4;--gold-tx:var(--gold-tx);
--mono:ui-monospace,"SF Mono",Menlo,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}
@view-transition{navigation:auto}
::view-transition-old(root){animation-duration:.14s}
::view-transition-new(root){animation-duration:.18s}
*{box-sizing:border-box;margin:0;padding:0}
:focus-visible{outline:2px solid var(--ember-tx);outline-offset:2px;border-radius:4px}
body{background:linear-gradient(180deg,#12100e 0%,#100f0d 240px);color:var(--ink);font-family:var(--sans);font-size:14px;line-height:1.55;
-webkit-font-smoothing:antialiased;max-width:860px;margin:0 auto;padding:22px 18px 60px}
@media(min-width:1100px){body{max-width:1200px}}
@media(min-width:1500px){body{max-width:1400px}}
a{color:inherit;text-decoration:none}
.top{display:flex;align-items:center;gap:11px;margin-bottom:10px;position:sticky;top:0;z-index:40;background:linear-gradient(180deg,var(--bg) 82%,transparent);padding:10px 0 14px}
.gm{width:30px;height:30px;border-radius:8px;background:linear-gradient(150deg,var(--ember),var(--ember-deep));
display:grid;place-items:center;color:#1a0f08;font-weight:800;font-size:14px}
.top h1{font-size:19px;letter-spacing:-.01em}.top .crumb{color:var(--ink-faint);font-size:13px}
.top .home{margin-left:auto;font-size:12px;color:var(--ink-dim);border:1px solid var(--line);border-radius:7px;padding:5px 13px;display:inline-flex;align-items:center;min-height:44px}
.top .home:hover{color:var(--ink)}
.kic{width:30px;height:30px;border-radius:8px;background:var(--inset);border:1px solid var(--line);
display:inline-grid;place-items:center;font-size:14px;flex:0 0 auto}
.chip::before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor;opacity:.9}
.chip{display:inline-flex;align-items:center;gap:5px;font-family:var(--mono);font-size:10px;font-weight:700;
border-radius:6px;padding:2px 8px;white-space:nowrap}
.chip.wait{background:rgba(201,151,31,.16);color:var(--gold-tx)}
.chip.exec{background:rgba(206,83,40,.16);color:var(--ember-tx)}
.chip.done{background:rgba(143,174,125,.14);color:var(--sage-tx)}
.chip.think{background:var(--panel2);color:var(--ink-dim)}
.chip.proj{background:transparent;border:1px solid var(--line);color:var(--ink-faint)}.chip.proj::before{display:none}
.swbar{display:flex;gap:10px;align-items:center;margin:2px 0 6px}
.swlab{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-faint)}
.sw{font-size:11.5px;font-weight:650;color:var(--ink-dim);border:1px solid var(--line-soft);border-radius:22px;padding:5px 14px;display:inline-flex;align-items:center;min-height:44px}
.sw:hover{color:var(--ink);border-color:var(--line)}
.sect{font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-faint);margin:22px 0 9px;display:flex;align-items:center;gap:8px}
.sect:after{content:"";flex:1;height:1px;background:var(--line-soft)}
.card{border:1px solid var(--line-soft);border-radius:11px;background:linear-gradient(180deg,#211d17,#1f1b16);padding:14px 16px;margin:9px 0;display:block}
a.card{transition:transform .16s cubic-bezier(.22,1,.36,1),border-color .16s ease}
a.card:hover{border-color:var(--line);transform:translateX(3px)}
.card .row{display:flex;align-items:center;gap:10px}
.card b{font-size:14px;font-weight:660}
.card .why{font-size:12.5px;color:var(--ink-dim);margin-top:5px;line-height:1.5}
.card .who{font-size:11px;color:var(--ink-faint);margin-top:7px;font-family:var(--mono)}
.acts{display:flex;gap:7px;margin-top:11px;flex-wrap:wrap}
.shell{display:grid;grid-template-columns:212px minmax(0,1fr);gap:22px;align-items:start}
.snav{position:sticky;top:64px;display:flex;flex-direction:column;gap:2px;border:1px solid var(--line-soft);border-radius:12px;background:var(--panel);padding:10px}
.snav a{display:flex;justify-content:space-between;gap:8px;padding:8px 12px;border-radius:8px;font-size:12.5px;font-weight:650;color:var(--ink-dim);min-height:44px;align-items:center}
.snav a.on{background:rgba(206,83,40,.1);color:var(--ember-tx)}
.snav a:hover{background:var(--panel2);color:var(--ink)}
.snav .grp{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-faint);margin:10px 4px 3px}
.snav .cnt{font-family:var(--mono);font-size:10.5px;color:var(--ink-faint)}
.subfil{margin:0 0 6px 14px;padding-left:10px;display:flex;flex-direction:column;gap:3px;border-left:1px solid var(--line-soft)}
.subfil .fbtn{font-size:10.5px;padding:4px 10px;border-color:transparent;text-align:left;justify-content:flex-start}
.subfil .fbtn:hover{border-color:var(--line-soft)}
.subfil .fsel{font-size:10.5px}
@media (max-width:1100px){.shell{grid-template-columns:1fr}.snav{position:static;flex-direction:row;flex-wrap:wrap;align-items:center}.snav .grp{margin:0 2px}}
.sfilter{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin:8px 0 4px}
.fbtn{font-size:11px;font-weight:700;padding:6px 13px;border-radius:18px;border:1px solid var(--line-soft);background:transparent;color:var(--ink-dim);cursor:pointer;min-height:44px}
.fbtn.on{color:var(--ember-tx);border-color:rgba(206,83,40,.4);background:rgba(206,83,40,.08)}
.fbtn:hover{border-color:var(--line);color:var(--ink)}
.fsep{width:1px;height:24px;background:var(--line-soft)}
.fsel{background:var(--inset);color:var(--ink);border:1px solid var(--line);border-radius:9px;padding:8px 10px;min-height:44px;font-size:11.5px}
.spage{display:inline-flex;gap:6px;align-items:center;margin-left:auto}
.ghead{margin:14px 2px 4px;font-family:var(--mono);font-size:11px;color:var(--ink-faint)}
.card.feat{background:linear-gradient(150deg,#2c1d11,#1f1b16);border-color:rgba(206,83,40,.32)}
.card.feat .kic{background:rgba(206,83,40,.14);border-color:rgba(206,83,40,.3);font-size:16px}
.pick{margin-left:auto;font-size:10.5px;font-weight:650;color:var(--ink-faint);display:inline-flex;gap:6px;align-items:center;min-height:44px;cursor:pointer;flex-shrink:0}
.pickbox{width:16px;height:16px;accent-color:var(--ember);cursor:pointer}
.batchbar{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);display:flex;gap:12px;align-items:center;background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:10px 18px;z-index:60;font-size:12.5px;box-shadow:0 6px 24px rgba(20,15,10,.5)}
.batchbar button{font-size:12px;font-weight:700;padding:7px 16px;border-radius:8px;border:none;cursor:pointer;background:var(--ember);color:#fff;min-height:44px}
.batchbar .clearsel{background:transparent;color:var(--ink-dim);border:1px solid var(--line)}
.obtn{font-size:12px;font-weight:700;padding:7px 16px;border-radius:8px;border:1px solid var(--line);background:transparent;color:var(--ember-tx);cursor:pointer;min-height:44px;margin-left:auto;flex-shrink:0}
.obtn:hover{border-color:var(--ember-tx)}
button{font-family:var(--sans)}
.acts a{font-size:12px;font-weight:650;padding:7px 14px;border-radius:8px;border:1px solid var(--line-soft);background:transparent;color:var(--ember-tx);display:inline-flex;align-items:center;min-height:44px;text-decoration:underline;text-underline-offset:3px;cursor:pointer}
.acts button{font-size:12px;font-weight:700;padding:7px 16px;border-radius:8px;border:none;cursor:pointer;
background:var(--ember);color:#1d0f06;display:inline-flex;align-items:center;min-height:44px}
.acts .quiet{background:transparent;color:var(--ink-dim);border:1px solid var(--line)}
.acts .quiet:hover{color:var(--ink)}
.acts button:hover,.acts a:hover{filter:brightness(1.12)}
.acts button:active,.acts a:active{transform:scale(.96)}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px}
.pcard{border:1px solid var(--line-soft);border-radius:12px;background:var(--panel);padding:14px 15px}
.pcard{transition:transform .16s cubic-bezier(.22,1,.36,1),border-color .16s ease}
.pcard:hover{border-color:var(--line);transform:translateY(-2px)}
.pcard b{font-size:14.5px}.pcard .ph{font-size:12px;color:var(--ink-dim);margin-top:4px}
.pcard .meta{font-size:10.5px;color:var(--ink-faint);font-family:var(--mono);margin-top:9px;display:flex;gap:10px}
.badge{background:var(--amber);color:#241c08;font-family:var(--mono);font-weight:700;font-size:10.5px;
border-radius:12px;padding:1px 8px;margin-left:auto}
.badge.zero{background:var(--panel2);color:var(--ink-faint)}
.badge.fyi{background:var(--panel2);color:var(--ink-dim)}
.tabs{display:flex;gap:4px;margin:16px 0 4px;border-bottom:1px solid var(--line-soft);padding-bottom:0}
.tabs a{padding:12px 15px;font-size:13px;font-weight:650;color:var(--ink-faint);border-bottom:2px solid transparent;display:inline-flex;align-items:center;min-height:44px}
.tabs a.on{color:var(--ember-tx);border-bottom-color:var(--ember-tx)}
.tabs a:hover{color:var(--ink-dim)}
.quiet-empty{border:1px dashed var(--line);border-radius:11px;padding:22px;text-align:center;color:var(--ink-dim);
font-size:13px;margin:10px 0;line-height:1.6}
.quiet-empty .pulse{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--sage);margin-right:7px}
.tl{list-style:none;margin:8px 0}
.tl li{display:flex;gap:10px;padding:7px 0;border-bottom:1px solid var(--line-soft);font-size:12.5px;color:var(--ink-dim);line-height:1.5}
.tl li:before{content:"✓";color:var(--sage-tx);font-weight:700;flex:0 0 auto}
.confirm .undo{margin-left:10px;font-size:11px;font-weight:700;padding:4px 12px;border-radius:7px;border:1px solid var(--line);background:transparent;color:var(--ink-dim);cursor:pointer;min-height:44px;padding:4px 14px}
.confirm{background:rgba(143,174,125,.12);border:1px solid rgba(143,174,125,.3);border-radius:9px;
padding:10px 14px;color:var(--sage-tx);font-size:13px;margin:10px 0}
.lib{display:grid;grid-template-columns:auto 1fr auto;gap:11px;align-items:center;padding:10px 12px;
border:1px solid var(--line-soft);border-radius:10px;background:var(--panel);margin:7px 0}
.lib .th{width:36px;height:32px;border-radius:6px;background:var(--inset);border:1px solid var(--line);
display:grid;place-items:center;font-family:var(--mono);font-size:8.5px;color:var(--ink-faint)}
.lib b{font-size:13px}.lib .m{font-size:10.5px;color:var(--ink-faint);font-family:var(--mono)}
.foot{margin-top:26px;font-size:11px;color:var(--ink-faint);line-height:1.6}
.cardgrid{display:grid;grid-template-columns:1fr;gap:10px;margin:9px 0}
.cardgrid .card{margin:0;height:100%;display:flex;flex-direction:column}
.cardgrid .card .acts{margin-top:auto;padding-top:11px}
.cardgrid > .quiet-empty{grid-column:1/-1}
@media(min-width:1100px){.cardgrid{grid-template-columns:1fr 1fr;gap:12px}}
@media(min-width:1500px){.cardgrid{grid-template-columns:repeat(3,1fr)}}
.card .why{max-width:64ch}
.tl li{max-width:72ch}
.libgrid{display:grid;grid-template-columns:1fr;gap:8px}
.libgrid .lib{margin:0}
@media(min-width:900px){.libgrid{grid-template-columns:1fr 1fr}}
@media(min-width:1400px){.libgrid{grid-template-columns:repeat(3,1fr)}}
@media(prefers-reduced-motion:reduce){
*,::before,::after{transition-duration:.01ms!important;animation-duration:.01ms!important}
::view-transition-old(root),::view-transition-new(root){animation:none}}
"""



ROSTER = [
    ("Ranger", "🔍", "researches your users and market — interviews, synthesis, evidence", "/guild-agent-ranger"),
    ("Cartographer", "🗺️", "organizes the product — IA, sitemaps, user flows on boards", "/guild-agent-cartographer"),
    ("Rogue", "🔀", "designs interactions — flows, wireframes, states", "/guild-agent-rogue"),
    ("Mage", "🎨", "designs visuals — critique, polish, motion, variants", "/guild-agent-mage"),
    ("Warlock", "✍️", "writes the words — microcopy, errors, voice", "/guild-agent-warlock"),
    ("Tinker", "🔧", "builds the design system — components, tokens, Figma/Storybook", "/guild-agent-tinker"),
    ("Sage", "🛡️", "quality gate — accessibility, consistency, go/no-go", "/guild-agent-sage"),
    ("Healer", "📦", "hands off to dev — specs, stories, tokens", "/guild-agent-healer"),
    ("Guild Master", "🎯", "runs the whole pipeline — point it at a goal", "/guild-quest"),
]

def switcher(current=None):
    regs = projects()
    wf = _feed_mod()
    opts = [f'<option value="/"{" selected" if current is None else ""}>⌂ All projects</option>']
    for i, pr in enumerate(regs):
        try: n = sum(1 for x in wf.build(pr["path"])["needs_you"] if x.get("id") != "note")
        except Exception: n = 0
        opts.append(f'<option value="/p/{i}"{" selected" if current == i else ""}>'
                    f'{E(pr["name"])}{f" · {n} waiting" if n else ""}</option>')
    pb = f'<a href="/playbook{"?p=%d" % current if current is not None else ""}" class="sw" style="margin-left:auto">&#128214; Playbook</a>'
    return (f'<div class="swbar"><label class="swlab" for="projsel">Project</label>'
            f'<select id="projsel" class="fsel" onchange="location.href=this.value" aria-label="switch project">'
            f'{"".join(opts)}</select>{pb}</div>')


BMAD_ROSTER = [
    ("PM", "📋", "decides what to build and why — owns the product brief", "/bmad-agent-pm"),
    ("Analyst", "📊", "digs into requirements and edge cases before anyone designs", "/bmad-agent-analyst"),
    ("Architect", "🏛️", "shapes the technical plan — stack, data, boundaries", "/bmad-agent-architect"),
    ("Scrum Master", "🏃", "cuts the plan into buildable stories and keeps the sprint honest", "/bmad-agent-sm"),
    ("Dev", "💻", "builds the stories — code, tests, review", "/bmad-agent-dev"),
]


def recommends(feed, project_path):
    """Guild proposes the next UX process — with its REASONING and COST visible,
    so nobody spends tokens on an unexplained suggestion (owner rule 2026-07-02)."""
    recs = []
    art = os.path.join(project_path, "_bmad-output", "guild-artifacts")
    if not os.path.isdir(art): art = os.path.join(project_path, "guild-output", "guild-artifacts")
    has = (lambda name: any(name in f for f in os.listdir(art))) if os.path.isdir(art) else (lambda name: False)
    artrel = art.replace(project_path, ".")
    if feed["needs_you"]:
        recs.append(("Answer what's waiting first",
                     f'{len(feed["needs_you"])} decisions above — everything downstream moves faster once they land',
                     "top", f'checked: your inbox — {len(feed["needs_you"])} items waiting', "free — just your clicks"))
    if feed["spine_nuggets"] == 0:
        recs.append(("Give the brain evidence",
                     "run /guild-spine-backfill (existing research) or /guild-research-synthesis (fresh)",
                     "/guild-spine-backfill",
                     f"checked: this project has no research file yet ({artrel}) — so nothing here can point at evidence",
                     "medium — one agent session reading your existing docs (~5-15 min)"))
    if not has("design-direction") and not has("charter"):
        recs.append(("Capture your taste once",
                     "/guild-design-direction + /guild-charter stop every agent re-asking what you want",
                     "/guild-design-direction",
                     f"checked: {artrel} — no design-direction or charter file, so every future agent will ask you the same questions again",
                     "light — ~10 min, mostly YOUR answers; saves tokens on every later run"))
    if os.path.isdir(os.path.join(project_path, "src")) and not feed["runs"]:
        recs.append(("Audit what's built",
                     "/guild-auto-critique reviews every key screen for craft problems and missing basics in one pass",
                     "/guild-auto-critique",
                     "checked: src/ exists but zero run records — real code Guild has never judged; unknown gaps compound into rework",
                     "medium-heavy — one agent per key screen; scripted gates are free"))
    if os.path.isdir(os.path.join(project_path, "src")) and not has("suggestions"):
        recs.append(("Ask Guild for UX improvement ideas",
                     "/guild-suggest sweeps every screen for missing basics — no search on growing lists, deletes without undo, blank empty screens — plus ideas Guild remembers working before",
                     "/guild-suggest",
                     f"checked: Guild has never proposed improvements for this app's screens (no suggestions file in {artrel})",
                     "free — scripted static sweep, seconds, no agent"))
    if feed["runs"] and not has("batched-review"):
        recs.append(("Get a decision packet",
                     "/guild-pre-handoff turns findings into approve/waive decisions",
                     "/guild-pre-handoff",
                     f'checked: {len(feed["runs"])} run(s) recorded but no batched-review packet — findings exist that never became decisions',
                     "light-medium — one agent compiling what already exists"))
    if not recs:
        recs.append(("Ship or extend", "/guild-quest for the next feature, or /guild-comment on anything that feels off",
                     "/guild-quest", "checked: research, taste, runs, and decisions are all in place — this project is healthy",
                     "heavy — a full pipeline run; only start it deliberately"))
    return recs[:4]


def page(title, crumb, body, current=None):
    body = f'<nav aria-label="projects">{switcher(current)}</nav><main>' + body + '</main>'
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title) if title.startswith("GUILD") else "GUILD Hall · " + E(title)}</title><style>{CSS}</style></head><body>'
            f'<div class="top"><div class="gm">G</div><h1>{E(title)}</h1><span class="crumb">{crumb}</span>'
            f'{"" if crumb.startswith("everything") else chr(60)+chr(97)+chr(32)+chr(99)+chr(108)+chr(97)+chr(115)+chr(115)+chr(61)+chr(34)+chr(104)+chr(111)+chr(109)+chr(101)+chr(34)+chr(32)+chr(104)+chr(114)+chr(101)+chr(102)+chr(61)+chr(34)+chr(47)+chr(34)+chr(62)+chr(66)+chr(97)+chr(99)+chr(107)+chr(32)+chr(116)+chr(111)+chr(32)+chr(97)+chr(108)+chr(108)+chr(32)+chr(112)+chr(114)+chr(111)+chr(106)+chr(101)+chr(99)+chr(116)+chr(115)+chr(60)+chr(47)+chr(97)+chr(62)}</div>{body}'
            f'<div class="foot">GUILD HALL · your delegated-work inbox — agents do the work, decisions come to you. '
            f'Quiet inbox = agents working, nothing needs you.</div></body></html>')


def chip(state):
    cls = {"waiting for you": "wait", "executing": "exec", "finished": "done", "thinking": "think"}.get(state, "think")
    return f'<span class="chip {cls}">{E(state)}</span>'


def decision_card(item, pidx, project_name=""):
    why = (item.get("why") or item.get("detail") or "").strip().lstrip("\u2026.").strip().replace("`", "")
    when = ""
    try:
        when = time.strftime("prepared %b %d", time.localtime(os.path.getmtime(item.get("link", ""))))
    except OSError:
        pass
    proj = f'<span class="chip proj">{E(project_name)}</span>' if project_name else ""
    if item["id"] == "note":
        return (f'<div class="card" style="opacity:.75"><div class="row"><span class="kic">ℹ️</span><b>{E(item["title"])}</b>'
                f'<span class="chip think">for your awareness</span>{proj}</div>'
                f'<div class="why">{E(why)}</div>'
                f'<div class="who">a note from the last run — nothing to decide yet · {when}</div>'
                f'<div class="acts"><a class="quiet" href="/p/{pidx}?view=runs">See what the agents did</a></div></div>')
    if item["id"] == "PICK":
        slug = item["title"].split("·")[-1].strip()
        opts = "".join(f'<button class="quiet" onclick="act(this,{pidx},\'pick\',\'{E(slug)}\',\'{c}\')">Pick {c.upper()}</button>'
                       for c in ("a", "b", "c"))
        acts = (f'<div class="acts"><a href="/pick/{pidx}/{E(slug)}">See the options first</a>{opts}'
                f'<button class="quiet" onclick="act(this,{pidx},\'pick\',\'{E(slug)}\',\'none\')">None fit — try again</button></div>')
    elif item["id"].startswith("D"):
        acts = (f'<div class="acts"><a href="/doc/{pidx}?path={E(item["link"])}">Read the evidence first</a>'
                f'<button onclick="act(this,{pidx},\'approve\',\'{E(item["id"])}\',\'\')">Approve</button>'
                f'<button class="quiet" onclick="act(this,{pidx},\'waive\',\'{E(item["id"])}\',\'\')">Not now</button></div>')
    else:
        acts = f'<div class="acts"><a class="quiet" href="/open?path={E(item["link"])}">Open</a></div>'
    icon = {"PICK": "🎨", "note": "ℹ️"}.get(item["id"], "⚖️" if item["id"].startswith("D") else "▶")
    return (f'<div class="card"><div class="row"><span class="kic">{icon}</span><b>{E(item["title"])}</b>{chip(item["state"])}{proj}</div>'
            f'<div class="why">{E(why)}</div>'
            f'<div class="who">an agent prepared this — the decision is yours · {when}</div>{acts}</div>')


def home(wf, view="inbox"):
    regs = projects()
    hometabs = "".join(f'<a href="/?view={v}" class="{"on" if view == v else ""}">{label}</a>'
                       for v, label in (("inbox", "Inbox"), ("activity", "Activity")))
    hometabs = f'<div class="tabs" style="margin-top:0">{hometabs}</div>'
    if view == "activity":
        ev = activity_events(wf, regs)
        waiting = sum(1 for e in ev if e["state"] == "waiting for you")
        execing = sum(1 for e in ev if e["state"] == "executing")
        cal = _calibration_count()
        pstore = os.path.expanduser("~/.config/guild/patterns/patterns.yaml")
        pats = 0
        if os.path.exists(pstore):
            import yaml as _y
            pats = len((_y.safe_load(open(pstore)) or {}).get("patterns", []))
        meters = (f'<div class="card"><div class="row" style="gap:16px;flex-wrap:wrap;font-family:var(--mono);font-size:11px">'
                  f'<span><b style="color:var(--gold-tx)">{waiting}</b> waiting on you</span>'
                  f'<span><b style="color:var(--ember-tx)">{execing}</b> agents executing</span>'
                  f'<span><b style="color:var(--sage-tx)">{pats}</b> patterns Guild remembers</span>'
                  f'<span><b style="color:var(--sage-tx)">{cal}</b> of 50 picks made — Guild is learning your taste</span></div>'
                  f'<div class="who">every row below is a door — click it</div></div>')
        rows = "".join(f'<a class="card" href="{e["href"]}" style="padding:10px 15px"><div class="row">'
                       f'<span class="chip proj">{E(e["project"])}</span><b style="font-size:13px;font-weight:600">{E(e["text"][:110])}</b>'
                       f'{chip(e["state"])}</div></a>' for e in ev)             or '<div class="quiet-empty"><span class="pulse"></span>No activity yet — delegate something.</div>'
        body = (f'{hometabs}<div style="font-size:11.5px;color:var(--ink-faint);margin:6px 2px 10px">'
                f'What agents did across every project, newest first — is the fleet healthy, what happened while you were away.</div>'
                f'{meters}<h2 class="sect">Recent activity</h2>{rows}')
        return page("GUILD Hall", "everything you delegated, one inbox", body)
    all_needs, grid = [], []
    for i, p in enumerate(regs):
        try: feed = wf.build(p["path"])
        except Exception: continue
        needs = feed["needs_you"]
        actn = [x for x in needs if x.get("id") != "note"]
        all_needs += [(i, n, feed) for n in needs[:8]]
        j = feed.get("journey") or {}
        phase = "no work started yet"
        if j.get("phases"):
            done = sum(1 for x in j["phases"] if x["status"] == "done")
            cur = next((x["name"] for x in j["phases"] if x["status"] != "done"), "all steps finished")
            phase = f"{done} of {len(j['phases'])} steps done · now: {cur[:34]}"
        if phase == "no work started yet" and feed["library"]:
            phase = f'{len(feed["library"])} outputs · no runs recorded yet'
        last = max((it["mtime"] for it in feed["library"]), default=0)
        ago = f'{int((time.time()-last)/3600)}h ago' if last else "—"
        badge = (f'<span class="badge">{len(actn)}</span>' if actn else
                 f'<span class="badge fyi">{len(needs)} fyi</span>' if needs else '<span class="badge zero">0</span>')
        grid.append(f'<a class="pcard" href="/p/{i}"><div style="display:flex;align-items:center"><b>{E(p["name"])}</b>{badge}</div>'
                    f'<div class="ph">{E(phase)}</div><div class="meta"><span>{len(feed["runs"])} runs</span>'
                    f'<span>last activity {ago}</span></div></a>')
    inbox = "".join(decision_card({"kind": "decision", "state": "waiting for you", **n[1]}, n[0], project_name=regs[n[0]]["name"]) for n in all_needs) \
        or ('<div class="quiet-empty"><span class="pulse"></span>Nothing needs you right now. '
            'Agents keep working and decisions will land here when they are yours to make.</div>')
    ndec = sum(1 for n in all_needs if n[1].get("id") != "note")
    nfyi = len(all_needs) - ndec
    hdr = f"{ndec} decisions" + (f", {nfyi} for your awareness" if nfyi else "")
    body = (f'{hometabs}<h2 class="sect">Needs you — across every project ({hdr})</h2><div class="cardgrid">{inbox}</div>'
            f'<h2 class="sect">Your projects</h2><div class="pgrid">{"".join(grid)}</div>{JS}')
    return page("GUILD Hall", "everything you delegated, one inbox", body)


def project_view(wf, pidx, view, sv="cards"):
    regs = projects()
    p = regs[pidx]
    feed = wf.build(p["path"])
    its = items_for(feed, p["name"])
    ndec = sum(1 for i in its if i["kind"] == "decision")
    nruns = sum(1 for i in its if i["kind"] == "run")
    ss = []
    for base in ("_bmad-output", "guild-output"):
        sf = os.path.join(p["path"], base, "guild-artifacts", "suggestions.yaml")
        if os.path.exists(sf):
            import yaml as _y
            ss = (_y.safe_load(open(sf)) or {}).get("suggestions", [])
            break
    nsugg = len(ss)
    sfirm = sum(1 for s in ss if s["confidence"] == "firm")
    scats, sicon = {}, {}
    for s in ss:
        c = s.get("category", "polish")
        scats[c] = scats.get(c, 0) + 1
        sicon.setdefault(c, s.get("icon", "💡"))
    sscreens = sorted({s["evidence"] for s in ss})
    sfil = ""
    if view == "needs" and ss:
        sfil = ('<div class="subfil">'
                f'<button class="fbtn on" data-k="conf" data-f="all" onclick="sflt(this)">All ({nsugg})</button>'
                f'<button class="fbtn" data-k="conf" data-f="firm" onclick="sflt(this)">Missing a basic ({sfirm})</button>'
                f'<button class="fbtn" data-k="conf" data-f="check" onclick="sflt(this)">Worth a look ({nsugg - sfirm})</button>'
                + "".join(f'<button class="fbtn" data-k="cat" data-f="{E(c)}" onclick="sflt(this)">{sicon[c]} {E(c)} ({n})</button>'
                          for c, n in sorted(scats.items(), key=lambda kv: -kv[1]))
                + f'<select class="fsel" onchange="sscr(this)" aria-label="filter by screen" style="margin-top:4px;width:100%">'
                + f'<option value="all">every screen ({len(sscreens)})</option>'
                + "".join(f'<option value="{E(s)}">{E("/".join(s.split("/")[-2:]))} ({sum(1 for x in ss if x["evidence"] == s)})</option>' for s in sscreens)
                + '</select></div>')
    def nv(href, label, cnt=None, on=False):
        c = f'<span class="cnt">{cnt}</span>' if cnt is not None else ""
        return f'<a href="{href}" class="{"on" if on else ""}">{label}{c}</a>'
    side = ('<aside class="snav" aria-label="project sections">'
            '<div class="grp">Decide</div>'
            + nv(f"/p/{pidx}?view=needs", "Needs you", ndec, view == "needs")
            + nv(f"/p/{pidx}?view=needs#improve", "UX improvements", nsugg) + sfil
            + nv(f"/p/{pidx}?view=needs#recs", "What to run next")
            + '<div class="grp">Watch</div>'
            + nv(f"/p/{pidx}?view=runs", "Runs", nruns, view == "runs")
            + '<div class="grp">Browse</div>'
            + nv(f"/p/{pidx}?view=library", "Library", len(feed["library"]), view == "library")
            + nv(f"/playbook?p={pidx}", "Playbook")
            + '<div class="grp">People</div>'
            + nv(f"/p/{pidx}?view=needs#roster", "Your guild")
            + nv(f"/p/{pidx}?view=needs#bmad", "Build council")
            + '</aside>')
    explain = {"needs": "Decisions agents queued for you — everything else keeps moving without you.",
               "runs": "What agents did, step by step — each run is a checklist of completed work.",
               "library": "Everything this project produced, newest first."}
    body = f'<div style="font-size:11.5px;color:var(--ink-faint);margin:2px 2px 2px">{explain[view]}</div>' 
    if view == "needs":
        rec_rows = "".join(
            f'<div class="card"><div class="row"><span class="kic">→</span><b>{E(title)}</b>'
            f'<span class="chip think">Guild recommends</span>'
            + (f'<label class="pick"><input type="checkbox" class="pickbox" data-pidx="{pidx}" data-cmd="{E(cmd)}">queue</label>' if cmd != "top" else "")
            + f'</div><div class="why">{E(why)}</div>'
            f'<div class="who" style="margin-top:6px">why: {E(because)}</div>'
            f'<div class="who">cost: {E(cost)}</div>'
            + (f'<div class="acts"><button onclick="run(this,{pidx},\'{E(cmd)}\')">Run it — Guild opens an agent and starts</button>'
               f'<span class="who" style="align-self:center">or type {E(cmd)} yourself</span></div>' if cmd != "top" else "")
            + '</div>'
            for title, why, cmd, because, cost in recommends(feed, p["path"]))
        cards = "".join(decision_card(i, pidx) for i in its if i["kind"] == "decision") \
            or ('<div class="quiet-empty"><span class="pulse"></span>Nothing needs you in this project. '
                'Agents keep working; decisions land here.</div>')
        roster_rows = "".join(
            f'<div class="lib"><span class="th" style="font-size:15px">{icon}</span>'
            f'<span><b>{name}</b><div style="font-size:11.5px;color:var(--ink-dim)">{job}</div></span>'
            f'<button class="obtn" onclick="run(this,{pidx},\'{cmd}\')">Summon</button></div>'
            for name, icon, job, cmd in ROSTER)
        sugg_rows = ""
        if ss:
            toggle = (f'<span style="margin-left:auto;font-family:var(--sans);font-size:11.5px;letter-spacing:0;text-transform:none">'
                      f'<a href="/p/{pidx}?view=needs&sv=cards" style="color:{"var(--ember-tx)" if sv == "cards" else "var(--ink-faint)"};margin-right:10px">Cards</a>'
                      f'<a href="/p/{pidx}?view=needs&sv=list" style="color:{"var(--ember-tx)" if sv == "list" else "var(--ink-faint)"}">List</a></span>')
            pager = ('<div class="sfilter"><span class="spage" style="margin-left:0"><button class="fbtn" onclick="spg(-1)" aria-label="previous page">←</button>'
                     '<b id="spglab" style="font-size:11px;min-width:86px;text-align:center"></b>'
                     '<button class="fbtn" onclick="spg(1)" aria-label="next page">→</button></span></div>') if sv == "cards" else ""

            def _srow(s):
                icon, cat = s.get("icon", "💡"), s.get("category", "polish")
                conf = s["confidence"]
                cchip = f'<span class="chip {"wait" if conf == "firm" else "think"}">{"missing a basic" if conf == "firm" else "worth a look"}</span>'
                pick = (f'<label class="pick"><input type="checkbox" class="pickbox" data-pidx="{pidx}" '
                        f'data-cmd="/guild-comment {E(s["title"])} — {E(s["evidence"])}">queue</label>')
                attrs = f'data-conf="{conf}" data-screen="{E(s["evidence"])}" data-cat="{E(cat)}"'
                if sv == "list":
                    return (f'<div class="lib" {attrs}><span class="th" style="font-size:13px">{icon}</span>'
                            f'<span><b>{E(s["title"])}</b><div class="m">{E(s["why"][:110])}</div></span>'
                            f'<span class="chip proj" style="flex-shrink:0">{E(cat)}</span>{cchip}{pick}</div>')
                return (f'<div class="card" {attrs}><div class="row"><span class="kic">{icon}</span><b>{E(s["title"])}</b>'
                        f'<span class="chip proj">{E(cat)}</span>{cchip}{pick}</div>'
                        f'<div class="why">{E(s["why"])}</div><div class="who">where: {E(s["evidence"])}</div>'
                        f'<div class="acts"><button onclick="run(this,{pidx},\'/guild-comment {E(s["title"])} — {E(s["evidence"])}\')">'
                        f'Have Guild fix it — 3 variants to pick from</button></div></div>')

            if sv == "list":
                bysrc = {}
                for s in ss:
                    bysrc.setdefault(s["evidence"], []).append(s)
                rows = []
                for src, group in sorted(bysrc.items(), key=lambda kv: -len(kv[1])):
                    rows.append(f'<div class="ghead" data-screen="{E(src)}">{E(src)} — {len(group)}</div>')
                    rows += [_srow(s) for s in group]
                sugg_rows = f'<div style="grid-column:1/-1">{"".join(rows)}</div>'
            else:
                sugg_rows = "".join(_srow(s) for s in ss)
            sugg_rows = (f'<h2 class="sect" id="improve">UX improvements Guild noticed{toggle}</h2>{pager}'
                         f'<div class="cardgrid" id="sgrid" data-mode="{sv}">{sugg_rows}</div>')
        body += f'<div class="cardgrid">{cards}</div>' + sugg_rows + f'<h2 class="sect" id="recs">What Guild would run next</h2><div class="cardgrid">{rec_rows}</div>' \
              + f'<h2 class="sect" id="roster">Your guild — summon a specialist</h2><div class="libgrid">{roster_rows}</div>'
        bmad_rows = "".join(
            f'<div class="lib"><span class="th" style="font-size:15px">{icon}</span>'
            f'<span><b>{name}</b><div style="font-size:11.5px;color:var(--ink-dim)">{job}</div></span>'
            f'<button class="obtn" onclick="run(this,{pidx},\'{cmd}\')">Summon</button></div>'
            for name, icon, job, cmd in BMAD_ROSTER)
        body += f'<h2 class="sect" id="bmad">The build council (BMAD) — plans and builds inside every full quest</h2><div class="libgrid">{bmad_rows}</div>'

    elif view == "runs":
        for i in [x for x in its if x["kind"] == "run"]:
            d = wf._yaml(i["link"])
            tl = "".join(f"<li>{E(str(c)[:180])}</li>" for c in (d.get("checkpoints") or [])[:14])
            body += (f'<div class="card"><div class="row"><b>{E(i["title"])}</b>{chip(i["state"])}</div>'
                     f'<div class="why">{E(i["why"])}</div>'
                     f'<div class="who">{i["checkpoints"]} steps completed</div><ul class="tl">{tl}</ul></div>')
        if not any(x["kind"] == "run" for x in its):
            body += (f'<div class="quiet-empty">No runs yet — delegate work with /guild-quest or /guild-comment '
                     f'(<a href="/playbook?p={pidx}" style="color:var(--ember-tx)">what do these do?</a>).</div>')
    else:
        ds = feed.get("design_system") or []
        if ds:
            body += '<h2 class="sect">Design system</h2>'
            for d in ds:
                body += (f'<div class="lib"><span class="th">{E(d["kind"][:5])}</span><span><b>{E(d["name"])}</b>'
                         f'<div style="font-size:11px;color:var(--ink-faint)">{E(d.get("hint",""))}</div></span>'
                         f'<span class="m"><a href="/open?path={E(d["path"])}" style="color:var(--ember-tx)">open</a></span></div>')
        else:
            body += ('<h2 class="sect">Design system</h2><div class="quiet-empty">No Storybook, tokens file, or '
                     'Claude Design bundle registered here yet — Tinker can set one up — find Summon under &quot;Your guild&quot; on the Needs-you tab.</div>')
        current_group = None
        for it in feed["library"]:
            if it["kind"] != current_group:
                current_group = it["kind"]
                body += f'<h2 class="sect">{E(current_group)}</h2>'
            when = time.strftime("%b %d %H:%M", time.localtime(it["mtime"]))
            body += (f'<div class="lib"><span class="th">{E(it["kind"][:5])}</span><span><b>{E(it["name"])}</b></span>'
                     f'<span class="m">{when} · <a href="/open?path={E(it["path"])}" style="color:var(--ember-tx)">open</a></span></div>')
    return page(p["name"], "a project in your hall", f'<div class="shell">{side}<div>{body}</div></div>' + JS, current=pidx)


JS = """<script>
async function run(btn, pidx, cmd){
  const label = btn.textContent; btn.disabled = true; btn.textContent = "launching agent…";
  const r = await fetch('/run', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({pidx, cmd})});
  const d = await r.json();
  const note = document.createElement('div'); note.className = 'confirm'; note.setAttribute('role','status'); note.setAttribute('aria-live','polite');
  note.textContent = (d.ok ? '✓ ' : '✗ ') + d.message;
  btn.closest('.card').appendChild(note);
  if (!d.ok) { btn.disabled = false; btn.textContent = label; }
}
async function act(btn, pidx, action, target, choice){
  btn.disabled = true; const label = btn.textContent; btn.textContent = "…";
  const r = await fetch('/act', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({pidx, action, target, choice})});
  const d = await r.json();
  const card = btn.closest('.card');
  const note = document.createElement('div'); note.className = 'confirm'; note.setAttribute('role','status'); note.setAttribute('aria-live','polite');
  if (d.ok && d.token) {
    let secs = Math.round(d.window);
    note.innerHTML = '✓ ' + d.message + ' <button class="undo">Undo (' + secs + 's)</button>';
    card.querySelectorAll('.acts button').forEach(b => b.disabled = true);
    const ub = note.querySelector('.undo');
    const tick = setInterval(() => { secs--; if (secs > 0) ub.textContent = 'Undo (' + secs + 's)';
      else { ub.remove(); clearInterval(tick); note.insertAdjacentText('beforeend', ' — done'); } }, 1000);
    ub.onclick = async () => {
      clearInterval(tick);
      const u = await fetch('/undo', {method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({token: d.token})});
      const ud = await u.json();
      note.textContent = ud.ok ? '↩ undone — nothing was recorded' : '✗ ' + ud.message;
      card.querySelectorAll('.acts button').forEach(b => { b.disabled = false; });
      btn.textContent = label;
    };
  } else {
    note.textContent = (d.ok ? '✓ ' : '✗ ') + d.message;
    if (d.ok) card.querySelectorAll('.acts button').forEach(b => b.disabled = true);
  }
  card.appendChild(note);
}

function syncbar(){
  const sel = [...document.querySelectorAll('.pickbox:checked')];
  let bar = document.getElementById('batchbar');
  if (!sel.length) { if (bar) bar.remove(); return; }
  if (!bar) { bar = document.createElement('div'); bar.id = 'batchbar'; bar.className = 'batchbar';
    bar.setAttribute('role','status'); document.body.appendChild(bar); }
  bar.innerHTML = '<b>' + sel.length + ' queued</b>' +
    '<button onclick="runbatch(this)">Run all ' + sel.length + ' — one agent each</button>' +
    '<button class="clearsel" onclick="clearsel()">Clear</button>';
}
async function runbatch(btn){
  btn.disabled = true;
  const sel = [...document.querySelectorAll('.pickbox:checked')];
  let done = 0, fail = 0;
  for (const c of sel) {
    btn.textContent = 'launching ' + (done + fail + 1) + '/' + sel.length + '…';
    try {
      const r = await fetch('/run', {method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({pidx: +c.dataset.pidx, cmd: c.dataset.cmd})});
      (await r.json()).ok ? done++ : fail++;
    } catch (e) { fail++; }
    c.checked = false; c.disabled = true;
  }
  btn.textContent = '✓ ' + done + ' agents launched' + (fail ? ' · ' + fail + ' failed' : '');
}
let SP = {conf:'all', cat:'all', screen:'all', page:0};
function sflt(b){
  if (b.dataset.k == 'conf') { SP.conf = b.dataset.f; if (b.dataset.f == 'all') SP.cat = 'all'; }
  else SP.cat = (SP.cat == b.dataset.f ? 'all' : b.dataset.f);
  SP.page = 0;
  document.querySelectorAll('.fbtn[data-k]').forEach(x => x.classList.toggle('on',
    (x.dataset.k == 'conf' && x.dataset.f == SP.conf) || (x.dataset.k == 'cat' && x.dataset.f == SP.cat)));
  sapply();
}
function sscr(sel){ SP.screen = sel.value; SP.page = 0; sapply(); }
function spg(d){ SP.page = Math.max(0, SP.page + d); sapply(); }
function sapply(){
  const g = document.getElementById('sgrid'); if (!g) return;
  const items = [...g.querySelectorAll('[data-conf]')];
  const vis = items.filter(c => (SP.conf == 'all' || c.dataset.conf == SP.conf)
    && (SP.cat == 'all' || c.dataset.cat == SP.cat)
    && (SP.screen == 'all' || c.dataset.screen == SP.screen));
  items.forEach(c => c.style.display = 'none');
  const per = g.dataset.mode == 'cards' ? 6 : 100000;
  const maxp = Math.max(0, Math.ceil(vis.length / per) - 1); if (SP.page > maxp) SP.page = maxp;
  vis.slice(SP.page * per, (SP.page + 1) * per).forEach(c => c.style.display = '');
  const lab = document.getElementById('spglab');
  if (lab) lab.textContent = vis.length ? ((SP.page * per + 1) + '–' + Math.min(vis.length, (SP.page + 1) * per) + ' of ' + vis.length) : 'none match';
  document.querySelectorAll('#sgrid .ghead').forEach(h => {
    h.style.display = vis.some(c => c.dataset.screen == h.dataset.screen && c.style.display == '') ? '' : 'none'; });
}
window.addEventListener('DOMContentLoaded', sapply);
function clearsel(){ document.querySelectorAll('.pickbox:checked').forEach(c => c.checked = false); syncbar(); }
document.addEventListener('change', e => { if (e.target.classList.contains('pickbox')) syncbar(); });
</script>"""


# ── the write channel ────────────────────────────────────────────────────────

PLAYBOOK = [
    ("Start a project (do these once)", [
        ("/guild-design-direction", "Tell Guild your taste ONCE — ~10 min of questions about look, feel, references. Every agent afterward designs to your answers instead of re-asking.", "light — mostly your answers"),
        ("/guild-charter", "Set the autonomy contract: what agents may decide alone vs. must bring to you. This is why your inbox stays quiet.", "light — a short conversation"),
        ("/guild-spine-backfill", "Already have research docs, notes, interviews? This turns them into a research file Guild can cite, so decisions point at proof.", "medium — one agent reads your corpus"),
    ]),
    ("Get evidence", [
        ("/guild-research-synthesis", "Fresh research from zero — questions, sources, verified facts. Every claim ends up either backed by a source or honestly cut.", "medium-heavy — real research takes agent time"),
        ("/guild-research-wave", "Turns a rough question into an excellent brief, sends it to ChatGPT + Gemini + Perplexity + Claude deep-research at once, and reconciles their reports — where they agree is solid, where they disagree is what you should look at.", "medium — several browser research runs, ~10-15 min each"),
        ("/guild-ia", "Plans the app's structure from the research — screen map, flows, what lives where. It refuses to invent structure without evidence.", "medium — needs the research step first"),
    ]),
    ("Design & build", [
        ("/guild-quest", "THE BIG ONE. Idea in, working app out. BMAD plans it (PM scopes → Analyst digs into requirements → Architect shapes the tech → Scrum Master cuts it into stories), Guild designs it, then it gets built and tested — agents handing off to each other. Start it and watch this Hall.", "heavy — a full pipeline; start deliberately"),
        ("/guild-design-sprint", "The design phases only (research → interaction → visual → content → QA), no code build. For when you want designs to react to first.", "medium-heavy"),
        ("/guild-render", "One design model fanned out to every platform at once — native FigJam board + clickable HTML prototype. Change the model, re-run, both update.", "light — scripted, seconds"),
        ("/guild-raid", "Every Guild agent runs on Claude, Codex AND Gemini in parallel; the best take per discipline is synthesized. Three independent design teams for the price of one prompt.", "heaviest — 3× everything; big decisions only"),
    ]),
    ("Judge & fix what exists", [
        ("/guild-auto-critique", "Point it at a screen: Mage critiques like a design lead + every craft gate runs (spacing, type, tokens, states, motion, a11y). Findings, not vibes.", "medium — one agent per screen; gates are free"),
        ("/guild-comment", "Anything feel off? Say it in plain words. Guild builds 3 real fixed variants and sends you a pick note with rendered pixels — you choose, it applies.", "medium — 3 real patches get built"),
        ("/guild-pre-handoff", "Sweeps everything agents produced into ONE decision packet — approve / waive / redo. The end-of-run ritual before shipping.", "light-medium — compiles what exists"),
    ]),
    ("Talk to one specialist", [
        ("/guild-agent-mage", "Summon a single agent instead of a pipeline — Mage (visual), Ranger (research), Rogue (interaction), Cartographer (IA), Sage (QA), Warlock (content), Healer (handoff), Tinker (design systems). Full roster with Summon buttons lives on every project page.", "light — one conversation"),
    ]),
]


def playbook(pidx=None):
    import re as _re
    runnable = pidx is not None
    pname = projects()[pidx]["name"] if runnable else None
    heavy = ("/guild-quest", "/guild-raid", "/guild-design-sprint")
    icons = {"/guild-design-direction": "🎨", "/guild-charter": "📜", "/guild-spine-backfill": "📚",
             "/guild-research-synthesis": "🔬", "/guild-research-wave": "🌊", "/guild-ia": "🧭", "/guild-quest": "🏰",
             "/guild-design-sprint": "🖌️", "/guild-render": "🖼️", "/guild-raid": "⚔️",
             "/guild-auto-critique": "🧪", "/guild-comment": "💬", "/guild-pre-handoff": "📦",
             "/guild-agent-mage": "🧙"}
    secs = []
    for title, cmds in PLAYBOOK:
        cards = []
        for cmd, what, cost in cmds:
            guard = (f"if(confirm('This starts a HEAVY run ({cmd}) on {pname} — proceed?'))" if cmd in heavy else "")
            act = (f'<div class="acts"><button onclick="{guard}run(this,{pidx},\'{E(cmd)}\')">Run on {E(pname)}</button>'
                   f'<label class="pick"><input type="checkbox" class="pickbox" data-pidx="{pidx}" data-cmd="{E(cmd)}">queue</label></div>'
                   if runnable else f'<div class="who">open this Playbook from a project page to run it there</div>')
            tier = "heavy" if cmd in heavy else ("medium" if "medium" in cost else "light")
            tchip = {"light": "done", "medium": "wait", "heavy": "exec"}[tier]
            cards.append(f'<div class="card{" feat" if cmd in heavy else ""}"><div class="row">'
                         f'<span class="kic">{icons.get(cmd, "▶")}</span>'
                         f'<b style="font-family:var(--mono);font-size:13px">{E(cmd)}</b>'
                         f'<span class="chip {tchip}">{tier}</span></div>'
                         f'<div class="why">{E(what)}</div><div class="who">cost: {E(cost)}</div>{act}</div>')
        secs.append(f'<h2 class="sect">{E(title)}</h2><div class="cardgrid">{"".join(cards)}</div>')
    # full catalog, straight from the real command files — never a stale hand-list
    cdir = os.path.join(os.path.dirname(HERE), ".claude", "commands")
    rows = []
    for f in sorted(os.listdir(cdir)) if os.path.isdir(cdir) else []:
        if not (f.startswith("guild-") and f.endswith(".md")): continue
        head = open(os.path.join(cdir, f), encoding="utf-8").read(2000)
        m = _re.search(r"^description:\s*['\"]?(.*?)['\"]?$", head, _re.M)
        desc = (m.group(1) if m else "").strip().replace("\\'", "'").replace('\\"', '"')
        for jargon, plain in (("canonical artifact model", "master design model"), ("artifact model", "master design model"),
                              ("evidence spine", "research file"), ("affordances", "expected controls"),
                              ("affordance", "expected control"), ("calibration", "taste-learning"),
                              ("nuggets", "verified facts"), ("nugget", "verified fact")):
            desc = desc.replace(jargon, plain).replace(jargon.capitalize(), plain)
        if len(desc) > 160: desc = desc[:160].rsplit(" ", 1)[0] + "\u2026"
        rows.append(f'<div style="padding:7px 2px;border-bottom:1px solid var(--line-soft)">'
                    f'<b style="font-family:var(--mono);font-size:12px;color:var(--ember-tx)">/{E(f[:-3])}</b> '
                    f'<span style="font-size:12px;color:var(--ink-faint)">— {E(desc)}</span></div>')
    catalog = (f'<details style="margin-top:22px"><summary style="cursor:pointer;font-size:12.5px;color:var(--ink-faint);'
               f'font-weight:650">Every command Guild knows ({len(rows)}) — the full catalog, read live from the command files</summary>'
               f'<div class="card" style="margin-top:10px">{"".join(rows)}</div></details>')
    intro = ('<div class="card"><div class="why" style="font-size:13px">'
             'You never need to memorize these. Guild recommends the right one at the right time on every project page — '
             'with its reasoning and cost. This page is the map for when you want to drive yourself.</div></div>')
    crumb = "what every command does, in plain words"
    title = f"Playbook \u00b7 {pname}" if runnable else "Playbook"
    html = page(title, crumb, intro + "".join(secs) + catalog + JS, current=pidx)
    if runnable:
        html = html.replace('<a class="home" href="/">',
                            f'<a class="home" href="/p/{pidx}">← Back to {E(pname)}</a>'
                            f'<a class="home" href="/" style="margin-left:10px">', 1)
    return html.replace('class="sw" style="margin-left:auto"',
                        'class="sw" style="margin-left:auto;color:var(--ember-tx);border-color:rgba(206,83,40,.4)"', 1)


def record_verdict(project_path, target, decision):
    """Approve/Waive a packet decision -> {art_root}/decisions.yaml, append-only."""
    wf = _feed_mod()
    out_root = wf._out_root(project_path)
    art = os.path.join(out_root, "guild-artifacts") if out_root else os.path.join(project_path, "guild-artifacts")
    path = os.path.join(art, "decisions.yaml")
    if not os.path.exists(path):
        open(path, "w").write("# Owner verdicts recorded by GUILD HALL (append-only)\ndecisions:\n")
    when = datetime.datetime.now().isoformat(timespec="seconds")
    with open(path, "a") as f:
        f.write(f'  - {{ id: "{target}", verdict: "{decision}", via: "guild-hall", at: "{when}" }}\n')
    return f"{target} {decision} recorded — agents will act on it"


def do_pick(project_path, slug, choice, dry=False):
    cmd = [sys.executable, os.path.join(HERE, "regenerate-pick.py"),
           "--project", project_path, "--set", slug, "--pick", choice] + (["--dry-run"] if dry else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    ok = r.returncode == 0
    msg = (r.stdout or r.stderr).strip().splitlines()
    return ok, (msg[-1] if msg else "done")


class Handler(BaseHTTPRequestHandler):
    wf = None

    def log_message(self, *a): pass

    def _send(self, body, ctype="text/html"):
        data = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", f"{ctype}; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path); q = parse_qs(u.query)
        if u.path == "/":
            return self._send(home(self.wf, q.get("view", ["inbox"])[0]))
        if u.path == "/playbook":
            pq = q.get("p", [None])[0]
            return self._send(playbook(int(pq) if pq is not None else None))
        if u.path.startswith("/p/"):
            return self._send(project_view(self.wf, int(u.path[3:]), q.get("view", ["needs"])[0],
                                           q.get("sv", ["cards"])[0]))
        if u.path.startswith("/pick/"):
            _, _, pidx, slug = u.path.split("/", 3)
            proj = projects()[int(pidx)]["path"]
            spec = importlib.util.spec_from_file_location("rn", os.path.join(HERE, "regenerate-note.py"))
            rn = importlib.util.module_from_spec(spec); spec.loader.exec_module(rn)
            import yaml as _y
            set_dir = rn.find_set(proj, slug)
            manifest = _y.safe_load(open(os.path.join(set_dir, "manifest.yaml")))
            body = rn.build_html(set_dir, manifest)
            back = ('<div style="position:sticky;top:0;background:#100f0dee;padding:10px 16px;font-family:-apple-system,sans-serif">'
                    f'<a href="/p/{pidx}?view=needs" style="color:#f3bca1;font-size:13px;font-weight:700;text-decoration:none">← Back to your inbox</a></div>')
            return self._send(body.replace("<body>", "<body>" + back, 1))
        if u.path.startswith("/doc/"):
            pidx = u.path.split("/")[2]
            path = q.get("path", [""])[0]
            text = open(path, encoding="utf-8").read() if os.path.exists(path) else "not found"
            md = E(text)
            import re as _re
            md = _re.sub(r"^### (.*)$", r"<h3>\1</h3>", md, flags=_re.M)
            md = _re.sub(r"^## (.*)$", r"<h2 style='margin-top:18px'>\1</h2>", md, flags=_re.M)
            md = _re.sub(r"^# (.*)$", r"<h1>\1</h1>", md, flags=_re.M)
            md = _re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", md)
            md = _re.sub(r"^- (.*)$", r"<div style='padding-left:14px'>• \1</div>", md, flags=_re.M)
            md = md.replace("\n\n", "<br><br>")
            body = (f'<div class="card" style="font-size:13px;line-height:1.65">{md}</div>')
            return self._send(page("Evidence", "read it, then decide from your inbox",
                                   f'<div style="margin-bottom:8px"><a href="/p/{pidx}?view=needs" style="color:var(--ember-tx);font-weight:700">← Back to your inbox</a></div>' + body))
        if u.path == "/open":
            p = q.get("path", [""])[0]
            cli = os.environ.get("ATRIUM_CLI_PATH")
            if cli and os.path.exists(p):
                subprocess.run([cli, "pane", "create", "--type", "browser", "--url", "file://" + p],
                               capture_output=True) if p.endswith(".html") else \
                    subprocess.run(["open", p], capture_output=True)
            elif os.path.exists(p):
                subprocess.run(["open", p], capture_output=True)
            return self._send('<script>history.back()</script>')
        if u.path == "/api/feed":
            pidx = int(q.get("pidx", ["0"])[0])
            return self._send(json.dumps(self.wf.build(projects()[pidx]["path"])), "application/json")
        self.send_response(404); self.end_headers()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        req = json.loads(self.rfile.read(n))
        if self.path == "/run":
            pr = projects()[req["pidx"]]
            cli = os.environ.get("ATRIUM_CLI_PATH", "atrium")
            split = []
            try:
                pl = subprocess.run([cli, "pane", "list", "--json"], capture_output=True, text=True, timeout=10)
                hallpane = next((x["id"] for x in json.loads(pl.stdout)
                                 if x.get("type") == "browser" and (x.get("name") or "").startswith("GUILD Hall")), None)
                if hallpane: split = ["--split", hallpane, "--direction", "right"]
            except Exception:
                pass
            r = subprocess.run([cli, "pane", "create", "--adapter", "claude-code", "--cwd", pr["path"], *split],
                               capture_output=True, text=True, timeout=30)
            pane = ""
            for tok in (r.stdout + r.stderr).split():
                if len(tok) >= 8 and all(c in "0123456789abcdef-" for c in tok[:8]): pane = tok; break
            if r.returncode != 0 or not pane:
                return self._send(json.dumps({"ok": False, "message": (r.stderr or "pane create failed")[:140]}), "application/json")
            time.sleep(4)   # let the adapter boot before the instruction lands
            msg = (f'{req["cmd"]} — launched from GUILD Hall for the project at {pr["path"]}. '
                   f'Work in that project; deliver results to its guild-artifacts and the Hall inbox.')
            m = subprocess.run([cli, "agent", "message", pane, msg], capture_output=True, text=True, timeout=30)
            ok = m.returncode == 0
            return self._send(json.dumps({"ok": ok,
                "message": (f"agent launched beside the Hall in this room — running {req['cmd']}" if split
                            else f"agent launched in a new room — running {req['cmd']}") if ok
                           else (m.stderr or "message failed")[:140]}), "application/json")
        if self.path == "/undo":
            timer = PENDING.pop(req.get("token", ""), None)
            if timer: timer.cancel(); return self._send(json.dumps({"ok": True, "message": "undone"}), "application/json")
            return self._send(json.dumps({"ok": False, "message": "too late — already applied"}), "application/json")
        if self.path != "/act":
            self.send_response(404); self.end_headers(); return
        p = projects()[req["pidx"]]["path"]
        dry = os.environ.get("HALL_DRY_RUN") == "1"

        def execute():
            PENDING.pop(token, None)
            try:
                if req["action"] == "pick":
                    do_pick(p, req["target"], req["choice"], dry=dry)
                elif not dry:
                    record_verdict(p, req["target"], req["action"])
            except Exception:
                pass

        token = uuid.uuid4().hex[:12]
        what = (f'picking {req["choice"].upper()} for {req["target"]}' if req["action"] == "pick"
                else f'{req["target"]}: {req["action"]}')
        timer = threading.Timer(UNDO_WINDOW, execute)
        PENDING[token] = timer; timer.start()
        self._send(json.dumps({"ok": True, "token": token, "window": UNDO_WINDOW,
                               "message": f"{what}{' [dry-run]' if dry else ''} — applying in {int(UNDO_WINDOW)}s"}),
                   "application/json")


def selftest():
    import tempfile, yaml
    wf = _feed_mod()
    with tempfile.TemporaryDirectory() as td:
        art = os.path.join(td, "_bmad-output", "guild-artifacts"); os.makedirs(os.path.join(art, "runs"))
        open(os.path.join(td, "_bmad-output", "quest-state.yaml"), "w").write('quest: "T"\nphases:\n  a: { status: done }\n')
        open(os.path.join(art, "runs", "RUN-1.yaml"), "w").write('run_id: "RUN-1"\nstate: ready-for-review\nobjective: "x"\ncheckpoints: ["step one EXIT 0"]\n')
        open(os.path.join(art, "batched-review-t.md"), "w").write("**D1 — Approve the thing** evidence\n")
        global REG
        old = REG; REG = os.path.join(td, "reg.yaml")
        yaml.safe_dump({"projects": [{"name": "t", "path": td}]}, open(REG, "w"))
        try:
            h = home(wf)
            pv = project_view(wf, 0, "needs")
            rv = project_view(wf, 0, "runs")
            msg = record_verdict(td, "D1", "approve")
            recorded = "D1" in open(os.path.join(art, "decisions.yaml")).read()
            ok = ("Needs you" in h and "Approve the thing" in h and "waiting for you" in pv
                  and "steps completed" in rv and "decision is yours" in pv
                  and recorded and "recorded" in msg
                  and "Nothing needs you" not in pv)
            # empty-inbox reads alive, not dead
            open(os.path.join(art, "batched-review-t.md"), "w").write("no decisions here\n")
            os.remove(os.path.join(art, "runs", "RUN-1.yaml"))
            pv2 = project_view(wf, 0, "needs")
            ok = ok and "Agents keep working" in pv2
            import re as _re
            used = set()
            for html in (h, pv, rv, playbook(0), playbook()):
                for m in _re.finditer(r'class="([^"]+)"', html):
                    used.update(c for c in m.group(1).split() if not c.startswith("shot"))
            unstyled = sorted(c for c in used if not _re.search(r"\." + _re.escape(c) + r"[ ,{:.>#\[]", CSS))
            blob = (h + pv + rv + playbook(0)).lower()
            leaked = [w for w in ("affordance", "fired pattern", "canon gap", "calibrated judgment",
                                  "spine.json", "evidence spine", "artifact model", "nugget") if w in blob]
            if leaked:
                print("   ✗ jargon leaked into owner-facing pages:", leaked)
                ok = False
            if unstyled:
                print("   ✗ classes used in markup with NO css rule:", unstyled)
                ok = False
        finally:
            REG = old
    print("guild-hall self-test:", "✅ PASS" if ok else "❌ FAIL")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--serve", action="store_true"); ap.add_argument("--port", type=int, default=4400)
    ap.add_argument("--projects", action="store_true"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.projects:
        for p in projects(): print(f'{p["name"]:<22} {p["path"]}')
        return
    if a.serve:
        Handler.wf = _feed_mod()
        print(f"GUILD HALL serving http://localhost:{a.port}  (registry: {REG})")
        HTTPServer(("127.0.0.1", a.port), Handler).serve_forever()
    ap.print_help()


if __name__ == "__main__":
    main()
