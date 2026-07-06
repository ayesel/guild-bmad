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
from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
UNDO_WINDOW = 8.0   # seconds — deferred commit, same pattern as Nourish's undo toast
PENDING = {}        # token -> threading.Timer
REG = os.path.expanduser("~/.config/guild/hall-projects.yaml")
E = html.escape


_WF = None
_BUILD_CACHE = {}
_BUILD_TTL = 4.0  # a status inbox may lag reality by a few seconds; snappy pages matter more


def _feed_mod():
    # singleton + short-TTL build cache: home() and switcher() each build every
    # project's feed, so one page load was ~5s of duplicated work (2× per project).
    # Cache makes the second pass instant and warm navigation near-instant.
    global _WF
    if _WF is None:
        spec = importlib.util.spec_from_file_location("wf", os.path.join(HERE, "widget-feed.py"))
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        _raw = m.build

        def cached_build(path):
            now = time.time()
            hit = _BUILD_CACHE.get(path)
            if hit and now - hit[0] < _BUILD_TTL:
                return hit[1]
            res = _raw(path)
            _BUILD_CACHE[path] = (now, res)
            return res

        m.build = cached_build
        _WF = m
    return _WF


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
--ink:#f4ece2;--ink-dim:#aa9c8d;--ink-faint:#9a8d7d;--ember:#d55e2e;--ember-tx:#f3bca1;--ember-deep:#9e3f1e;
--sage:#728b5b;--sage-tx:#b7c9a6;--amber:#c9971f;--denim:#5b7a8b;--denim-tx:#a9c4d4;--gold-tx:#e8c15f;
--mono:ui-monospace,"SF Mono",Menlo,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}
@view-transition{navigation:auto}
::view-transition-old(root){animation-duration:.14s}
::view-transition-new(root){animation-duration:.18s}
*{box-sizing:border-box;margin:0;padding:0}
:focus-visible{outline:2px solid var(--ember-tx);outline-offset:2px;border-radius:4px}
body{background:linear-gradient(180deg,#12100e 0%,#100f0d 240px);color:var(--ink);font-family:var(--sans);font-size:14px;line-height:1.55;
-webkit-font-smoothing:antialiased;max-width:1400px;margin:0;padding:24px 24px 48px}
@media(min-width:1720px){body{margin:0 auto}}
@media(max-width:860px){body{max-width:100%;padding:16px 16px 48px}}
a{color:inherit;text-decoration:none}
.top{display:flex;align-items:center;gap:12px;margin-bottom:10px;position:sticky;top:0;z-index:40;background:linear-gradient(180deg,var(--bg) 82%,transparent);padding:8px 0 16px}
.gm{width:30px;height:30px;border-radius:8px;background:linear-gradient(150deg,#e06a3a,var(--ember));
display:grid;place-items:center;color:#1a0f08;font-weight:800;font-size:14px}
.top h1{font-size:19px;letter-spacing:-.01em}.top .crumb{color:var(--ink-faint);font-size:13px}
.top{flex-wrap:wrap}
.top .swlab{margin-left:auto}
.topsel{background:var(--inset);color:var(--ink);border:1px solid var(--line);border-radius:9px;padding:8px 8px;min-height:38px;font-size:12px;max-width:220px}
.top .home{font-size:12px;color:var(--ink-dim);border:1px solid var(--line);border-radius:7px;padding:4px 12px;display:inline-flex;align-items:center;min-height:44px;margin-left:12px}
.top .home:hover{color:var(--ink)}
.runner{margin-left:auto;position:relative}
.runner summary{list-style:none;display:inline-flex;align-items:center;gap:8px;min-height:38px;padding:6px 12px;border:1px solid var(--line);border-radius:9px;background:var(--inset);color:var(--ink-dim);font-size:12px;font-weight:650;cursor:pointer}
.runner summary::-webkit-details-marker{display:none}
.runner summary:before{content:"⚙";font-size:13px;color:currentColor}
.runner[open] summary{color:var(--ink);border-color:var(--line)}
.runcfg{position:absolute;right:0;top:46px;min-width:360px;max-width:min(520px,calc(100vw - 28px));z-index:80;display:grid;grid-template-columns:auto 1fr;gap:8px 12px;align-items:center;margin:0;padding:16px;border:1px solid var(--line);border-radius:10px;background:var(--panel);box-shadow:0 12px 36px rgba(0,0,0,.45)}
.runcfg .who{grid-column:1/-1}
@media(max-width:700px){.runner{margin-left:0}.runcfg{left:0;right:auto;min-width:min(360px,calc(100vw - 28px))}}
.kic{width:30px;height:30px;border-radius:8px;background:var(--inset);border:1px solid var(--line);
display:inline-grid;place-items:center;font-size:14px;flex:0 0 auto}
.chip::before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor;opacity:.9}
.chip{display:inline-flex;align-items:center;gap:4px;font-family:var(--mono);font-size:10px;font-weight:700;
border-radius:6px;padding:2px 8px;white-space:nowrap}
.chip.wait{background:rgba(201,151,31,.16);color:var(--gold-tx)}
.chip.exec{background:rgba(213,94,46,.16);color:var(--ember-tx)}
.chip.done{background:rgba(143,174,125,.14);color:var(--sage-tx)}
.chip.think{background:var(--panel2);color:var(--ink-dim)}
.chip.proj{background:transparent;border:1px solid var(--line);color:var(--ink-faint)}.chip.proj::before{display:none}
.swbar{display:flex;gap:8px;align-items:center;margin:2px 0 6px}
.cardmodel{font-size:11px;padding:4px 6px;border-radius:7px;background:var(--inset);color:var(--ink-dim);border:1px solid var(--line-soft);min-height:44px;margin-right:6px;align-self:center}
.swlab{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-faint)}
.sw{font-size:11px;font-weight:650;color:var(--ink-dim);border:1px solid var(--line-soft);border-radius:22px;padding:4px 16px;display:inline-flex;align-items:center;min-height:44px}
.sw:hover{color:var(--ink);border-color:var(--line)}
.sect{font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-faint);margin:24px 0 8px;display:flex;align-items:center;gap:8px}
.sect:after{content:"";flex:1;height:1px;background:var(--line-soft)}
.card{border:1px solid var(--line-soft);border-radius:9px;background:#1e1a15;padding:16px;margin:8px 0;display:block;box-shadow:none}
a.card{transition:transform .16s cubic-bezier(.22,1,.36,1),border-color .16s ease}
a.card:hover{border-color:var(--line);transform:translateX(3px)}
.card .row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;min-width:0}
.card b{font-size:14px;font-weight:660}
.card .why{font-size:12px;color:var(--ink-dim);margin-top:5px;line-height:1.45}
.card .who{font-size:11px;color:var(--ink-faint);margin-top:7px;font-family:var(--mono)}
.brief{font-size:12px;color:var(--ink-dim);line-height:1.45;margin-top:5px;max-width:68ch}
.metafold{margin-top:9px}
.metafold summary{cursor:pointer;list-style:none;font-family:var(--mono);font-size:10px;color:var(--ink-faint);letter-spacing:.08em;text-transform:uppercase;min-height:32px;display:inline-flex;align-items:center}
.metafold summary::-webkit-details-marker{display:none}
.metafold summary:before{content:"+";margin-right:7px;color:var(--ink-faint)}
.metafold[open] summary:before{content:"–"}
.kmeta{display:grid;grid-template-columns:38px 1fr;gap:8px;margin-top:8px;align-items:baseline}
.kmeta .klabel{font-family:var(--mono);font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-faint)}
.kmeta .kv{font-family:var(--mono);font-size:11px;color:var(--ink-dim);line-height:1.5}
.acts{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}
.shell{display:grid;grid-template-columns:212px minmax(0,1fr);gap:24px;align-items:start}
.shell.three{grid-template-columns:200px minmax(0,1fr) 288px;gap:24px}
.mainpane{min-width:0}
.ptog{border:1px solid var(--line-soft);background:var(--panel2);color:var(--ink-dim);width:26px;height:26px;flex-shrink:0;border-radius:7px;cursor:pointer;font-size:15px;line-height:1;display:grid;place-items:center;padding:0;transition:transform .15s ease,color .15s ease}
.ptog:hover{color:var(--ink);border-color:var(--line)}
.sbhead{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-shrink:0}
.snav .sbhead{margin:2px 0 4px}
.snav .sbhead .grp{margin:0 8px}
.rail .sbhead{margin-bottom:-4px}
.rail .sbhead .railh{margin:0}
@media(min-width:1181px){
html.navmin .shell.three{grid-template-columns:42px minmax(0,1fr) 288px}
html.railmin .shell.three{grid-template-columns:200px minmax(0,1fr) 42px}
html.navmin.railmin .shell.three{grid-template-columns:42px minmax(0,1fr) 42px}
html.navmin .snav{padding:8px 6px;background:transparent;border-color:transparent}
html.navmin .snav>*:not(.sbhead){display:none}
html.navmin .snav .sbhead{justify-content:center;margin:0}
html.navmin .snav .sbhead .grp{display:none}
html.navmin .snav .navtog{transform:rotate(180deg)}
html.railmin .rail{gap:0}
html.railmin .rail>*:not(.sbhead){display:none}
html.railmin .rail .sbhead{justify-content:center;margin:0}
html.railmin .rail .sbhead .railh{display:none}
html.railmin .rail .railtog{transform:rotate(180deg)}
}
@media(max-width:1180px){.ptog{display:none}}
/* ---- full-height app shell: header fixed, 3 columns each scroll independently ---- */
body.app{height:100vh;max-width:none;margin:0;padding:0;overflow:hidden;display:flex;flex-direction:column}
body.app .top{position:static;margin:0;padding:12px 24px;flex:0 0 auto;border-bottom:1px solid var(--line-soft);z-index:auto}
body.app>main{flex:1 1 auto;min-height:0;max-width:none;margin:0;padding:0;overflow:hidden}
body.app .shell{height:100%;gap:0;align-items:stretch}
body.app .snav{position:static;height:100%;overflow-y:auto;border:none;border-right:1px solid var(--line-soft);border-radius:0;padding:16px 12px}
body.app .mainpane{height:100%;overflow-y:auto;padding:24px 24px 48px}
body.app .rail{position:static;height:100%;overflow-y:auto;border-left:1px solid var(--line-soft);border-radius:0;padding:16px 16px 48px}
body.app .foot{display:none}
@media(max-width:1180px){body.app{height:auto;overflow:visible;display:block}
body.app>main{overflow:visible}
body.app .shell,body.app .snav,body.app .mainpane,body.app .rail{height:auto;overflow:visible}
body.app .rail{border-left:none}}
@media(max-width:860px){body.app .snav{border:none;padding:0}body.app .mainpane{padding:16px}body.app .rail{border:none;padding:0}}
.metrics{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin:0 0 4px}
.mtile{display:flex;flex-direction:column;gap:2px;padding:12px 12px 8px;border:1px solid var(--line-soft);border-radius:11px;background:linear-gradient(180deg,#241f18,#1f1b16);min-height:82px;overflow:hidden;color:var(--ink)}
.mtile:hover{border-color:var(--line)}
.mtile .mlab{font-family:var(--mono);font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-faint)}
.mtile .mnum{font-size:27px;font-weight:700;line-height:1.05;letter-spacing:-.02em}
.mtile .msub{font-size:10px;color:var(--ink-dim)}
.mtile .spark{margin-top:auto;width:100%;height:20px;color:var(--denim-tx);opacity:.7}
.mtile.hero{border-color:rgba(213,94,46,.42);background:linear-gradient(160deg,#2c1d11,#1f1b16)}
.mtile.hero .mnum{color:var(--ember-tx)}
.mtile.hero .mlab{color:var(--gold-tx)}
.yourmove{border:1px solid var(--line);border-radius:12px;background:linear-gradient(150deg,#271c13,#1c1813);padding:16px 16px 16px;display:flex;flex-direction:column;gap:4px;margin:0 0 4px}
.yourmove.calm{background:var(--panel);border-color:var(--line-soft)}
.ymlab{font-family:var(--mono);font-size:9px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-tx)}
.yourmove.calm .ymlab{color:var(--sage-tx)}
.ymtitle{font-size:19px;font-weight:670;letter-spacing:-.01em;line-height:1.22}
.ymwhy{font-size:13px;color:var(--ink-dim);line-height:1.5;max-width:66ch}
.ymacts{display:flex;gap:16px;align-items:center;margin-top:8px;flex-wrap:wrap}
.hbtn{background:var(--ember);color:#1d0f06;font-size:12px;font-weight:700;padding:0 16px;min-height:44px;border-radius:8px;border:none;cursor:pointer;display:inline-flex;align-items:center;text-decoration:none}
.hbtn:hover{filter:brightness(1.08)}
.hmore{font-size:12px;color:var(--ember-tx);font-weight:650;display:inline-flex;align-items:center;min-height:24px}
@media(max-width:1080px){.metrics{grid-template-columns:repeat(3,1fr)}}
@media(max-width:620px){.metrics{grid-template-columns:repeat(2,1fr)}.ymtitle{font-size:17px}}
.mainpane .cardgrid.feed{grid-template-columns:1fr}
.rail{display:flex;flex-direction:column;gap:16px;position:sticky;top:64px;align-self:start;min-width:0}
.railsect{padding:0}
.railh{font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-dim);margin:0 0 8px;display:flex;flex-direction:column;gap:2px}
.railh-sub{font-weight:400;letter-spacing:.01em;text-transform:none;font-size:10px;color:var(--ink-faint);font-family:var(--sans)}
.raillist{display:flex;flex-direction:column;gap:8px}
.rail .lib{display:flex;flex-wrap:wrap;align-items:flex-start;gap:8px;padding:12px;border:1px solid var(--line-soft);background:var(--panel);border-radius:10px;margin:0;min-height:0}
.rail .lib:hover{border-color:var(--line)}
.rail .lib b{font-size:13px}
.rail .lib .th{flex:0 0 auto;order:1;margin-top:1px}
.rail .lib > span:not(.th){flex:1 1 60%;min-width:0;order:2;display:flex;flex-direction:column;gap:1px}
.rail .lib span div{font-size:11px;color:var(--ink-faint);line-height:1.34;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.rail .lib .cardmodel{order:3;flex:1 1 90px;min-height:32px;font-size:10px;max-width:none;margin:0}
.rail .lib .obtn{order:4;flex:0 0 auto;font-size:11px;padding:4px 12px;min-height:32px;margin-left:auto}
.snav{position:sticky;top:64px;display:flex;flex-direction:column;gap:2px;border:1px solid var(--line-soft);border-radius:10px;background:#1c1813;padding:8px}
.snav .navitem{display:flex;align-items:center;gap:8px;padding:8px 8px;border-radius:8px;font-size:13px;font-weight:600;color:var(--ink-dim);min-height:40px;position:relative}
.snav .navitem .nvi{flex:0 0 18px;width:18px;text-align:center;font-size:13px;opacity:.85}
.snav .navitem .nvl{flex:1 1 auto}
.snav .navitem:hover{background:var(--panel2);color:var(--ink)}
.snav .navitem.on{background:var(--panel2);color:var(--ink)}
.snav .navitem.on::before{content:"";position:absolute;left:0;top:8px;bottom:8px;width:3px;border-radius:0 3px 3px 0;background:var(--ember)}
.snav .navitem.on .cnt{color:var(--ember-tx)}
.snav .grp{font-family:var(--mono);font-size:9px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-faint);margin:12px 8px 4px}
.snav .ngrp:first-of-type .grp{margin-top:2px}
.snav .cnt{font-family:var(--mono);font-size:11px;color:var(--ink-faint)}
.subfil{margin:0 0 6px 16px;padding-left:10px;display:flex;flex-direction:column;gap:4px;border-left:1px solid var(--line-soft)}
.subfil .fbtn{font-size:11px;padding:4px 8px;border-color:transparent;text-align:left;justify-content:flex-start}
.subfil .fbtn:hover{border-color:var(--line-soft)}
.subfil .fsel{font-size:11px}
@media (max-width:1180px){.shell.three{grid-template-columns:200px minmax(0,1fr)}
.shell.three .rail{grid-column:1/-1;flex-direction:row;flex-wrap:wrap;position:static;gap:16px}
.shell.three .railsect{flex:1 1 300px}}
@media (max-width:860px){.shell,.shell.three{grid-template-columns:1fr;gap:16px}
.shell.three .rail{grid-column:auto;flex-direction:column}
.snav{position:static;flex-direction:row;flex-wrap:wrap;align-items:flex-start;gap:8px;padding:0;background:transparent;border:none;border-radius:0}
.snav .ngrp{border:1px solid var(--line-soft);border-radius:10px;background:var(--panel);padding:6px 8px;margin:0;flex:1 1 220px}
.snav .grp{margin:0 4px 4px}}
.sfilter{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0 4px}
.fbtn{font-size:11px;font-weight:700;padding:6px 12px;border-radius:18px;border:1px solid var(--line-soft);background:transparent;color:var(--ink-dim);cursor:pointer;min-height:44px}
.fbtn.on{color:var(--ember-tx);border-color:rgba(213,94,46,.4);background:rgba(213,94,46,.08)}
.fbtn:hover{border-color:var(--line);color:var(--ink)}
.fsep{width:1px;height:24px;background:var(--line-soft)}
.fsel{background:var(--inset);color:var(--ink);border:1px solid var(--line);border-radius:9px;padding:8px 8px;min-height:44px;font-size:11px}
.filtermenu{position:relative}
.toolbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:2px 0 8px}
.toolbar .fbtn{min-height:36px}
.fmbtn{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:650;color:var(--ink-dim);border:1px solid var(--line);border-radius:8px;padding:0 12px;min-height:36px;background:var(--inset);user-select:none;white-space:nowrap}
.fmbtn::-webkit-details-marker{display:none}
.fmbtn:hover,.filtermenu[open] .fmbtn{color:var(--ink);border-color:var(--ink-faint)}
.fmdot{width:6px;height:6px;border-radius:50%;background:var(--ember);display:inline-block}
.fmpop{position:absolute;left:0;top:calc(100% + 6px);z-index:40;width:min(300px,86vw);background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:12px;box-shadow:0 12px 34px rgba(8,5,3,.55);display:flex;flex-direction:column;gap:12px}
.fmgroup{display:flex;flex-direction:column;gap:8px}
.fmlab{font-family:var(--mono);font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-faint)}
.fmchips{display:flex;flex-wrap:wrap;gap:6px}
.fmpop .fbtn{min-height:32px;font-size:11px}
.fmpop .fsel{width:100%;min-height:38px}
.widget{display:block}
.widget[hidden]{display:none}
.wtabs{display:inline-flex;border:1px solid var(--line);border-radius:9px;overflow:hidden;background:var(--inset);margin:0 0 16px}
.wtab{border:none;background:transparent;cursor:pointer;font-family:var(--sans);font-size:13px;font-weight:650;color:var(--ink-dim);padding:0 16px;min-height:40px;display:inline-flex;align-items:center;gap:8px}
.wtab+.wtab{border-left:1px solid var(--line)}
.wtab:not(.on):hover{color:var(--ink);background:var(--panel2)}
.wtab.on{background:var(--ember);color:#1d0f06}
.wtab .wtc{font-family:var(--mono);font-size:11px;color:var(--ink-faint);background:var(--panel2);border-radius:10px;padding:1px 8px}
.wtab.on .wtc{color:#1d0f06;background:rgba(255,255,255,.22)}
.spage{display:inline-flex;gap:6px;align-items:center;margin-left:auto}
.ghead{margin:16px 2px 4px;font-family:var(--mono);font-size:11px;color:var(--ink-faint)}
.wprov{cursor:pointer}.wprov input{width:16px;height:16px;accent-color:var(--ember);cursor:pointer}
.wprov:has(.wsel:checked){border-color:rgba(213,94,46,.4);background:linear-gradient(150deg,#241a12,#1f1b16)}
.card.feat{background:linear-gradient(150deg,#2c1d11,#1f1b16);border-color:rgba(213,94,46,.32)}
.card.feat .kic{background:rgba(213,94,46,.14);border-color:rgba(213,94,46,.3);font-size:16px}
.pick{margin-left:auto;font-size:11px;font-weight:650;color:var(--ink-faint);display:inline-flex;gap:8px;align-items:center;min-height:36px;cursor:pointer;flex-shrink:0;border:1px solid var(--line-soft);border-radius:8px;padding:0 12px;user-select:none;transition:border-color .15s ease,color .15s ease}
.pick:hover{color:var(--ink-dim);border-color:var(--line)}
.pick:has(input:checked){color:var(--ember-tx);border-color:rgba(213,94,46,.45);background:rgba(213,94,46,.07)}
.pick input[type="checkbox"]{appearance:none;-webkit-appearance:none;width:15px;height:15px;border:1.5px solid var(--ink-faint);border-radius:5px;margin:0;display:grid;place-items:center;cursor:pointer;background:transparent;flex-shrink:0}
.pick input[type="checkbox"]:checked{background:var(--ember);border-color:var(--ember)}
.pick input[type="checkbox"]:checked::after{content:"✓";font-size:10px;font-weight:800;color:#1d0f06;line-height:1}
.pickbox{cursor:pointer}
.batchbar{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);display:flex;gap:12px;align-items:center;background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:8px 16px;z-index:60;font-size:12px;box-shadow:0 6px 24px rgba(20,15,10,.5)}
.batchbar button{font-size:12px;font-weight:700;padding:8px 16px;border-radius:8px;border:none;cursor:pointer;background:var(--ember);color:#1a0f08;min-height:44px}
.batchbar .clearsel{background:transparent;color:var(--ink-dim);border:1px solid var(--line)}
.obtn{font-size:12px;font-weight:700;padding:8px 16px;border-radius:8px;border:1px solid var(--line);background:transparent;color:var(--ember-tx);cursor:pointer;min-height:44px;margin-left:auto;flex-shrink:0}
.obtn:hover{border-color:var(--ember-tx)}
button{font-family:var(--sans)}
.acts a{font-size:12px;font-weight:650;padding:8px 16px;border-radius:8px;border:1px solid var(--line-soft);background:transparent;color:var(--ember-tx);display:inline-flex;align-items:center;min-height:44px;text-decoration:underline;text-underline-offset:3px;cursor:pointer}
.acts button{font-size:12px;font-weight:700;padding:8px 16px;border-radius:8px;border:none;cursor:pointer;
background:var(--ember);color:#1a0f08;display:inline-flex;align-items:center;min-height:44px}
.acts .quiet{background:transparent;color:var(--ink-dim);border:1px solid var(--line)}
.acts .quiet:hover{color:var(--ink)}
.acts button:hover,.acts a:hover{filter:brightness(1.12)}
.acts button:active,.acts a:active{transform:scale(.96)}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:8px}
.pcard{border:1px solid var(--line-soft);border-radius:9px;background:#1c1813;padding:12px 16px}
.pcard{transition:transform .16s cubic-bezier(.22,1,.36,1),border-color .16s ease}
.pcard:hover{border-color:var(--line);transform:translateY(-2px)}
.pcard b{font-size:14px}.pcard .ph{font-size:12px;color:var(--ink-dim);margin-top:4px}
.pcard .meta{font-size:11px;color:var(--ink-faint);font-family:var(--mono);margin-top:9px;display:flex;gap:8px}
.badge{background:var(--amber);color:#241c08;font-family:var(--mono);font-weight:700;font-size:11px;
border-radius:12px;padding:1px 8px;margin-left:auto}
.badge.zero{background:var(--panel2);color:var(--ink-faint)}
.badge.fyi{background:var(--panel2);color:var(--ink-dim)}
.tabs{display:flex;gap:4px;margin:16px 0 4px;border-bottom:1px solid var(--line-soft);padding-bottom:0}
.tabs a{padding:12px 16px;font-size:13px;font-weight:650;color:var(--ink-faint);border-bottom:2px solid transparent;display:inline-flex;align-items:center;min-height:44px}
.tabs a.on{color:var(--ember-tx);border-bottom-color:var(--ember-tx)}
.tabs a:hover{color:var(--ink-dim)}
.quiet-empty{border:1px dashed var(--line);border-radius:9px;padding:16px;text-align:center;color:var(--ink-dim);
font-size:13px;margin:8px 0;line-height:1.6}
.quiet-empty .pulse{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--ink-faint);margin-right:7px}
.tl{list-style:none;margin:8px 0}
.tl li{display:flex;gap:8px;padding:8px 0;border-bottom:1px solid var(--line-soft);font-size:12px;color:var(--ink-dim);line-height:1.5}
.tl li:before{content:"✓";color:var(--sage-tx);font-weight:700;flex:0 0 auto}
.confirm .undo{margin-left:10px;font-size:11px;font-weight:700;padding:4px 12px;border-radius:7px;border:1px solid var(--line);background:transparent;color:var(--ink-dim);cursor:pointer;min-height:44px;padding:4px 16px}
.confirm{background:rgba(143,174,125,.12);border:1px solid rgba(143,174,125,.3);border-radius:9px;
padding:8px 16px;color:var(--sage-tx);font-size:13px;margin:8px 0}
.lib{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:12px;
border:1px solid var(--line-soft);border-radius:10px;background:var(--panel);margin:8px 0}
.lib .th{width:36px;height:32px;border-radius:6px;background:var(--inset);border:1px solid var(--line);
display:grid;place-items:center;font-family:var(--mono);font-size:10px;color:var(--ink-faint)}
.lib b{font-size:13px}.lib .m{font-size:11px;color:var(--ink-faint);font-family:var(--mono)}
.foot{margin-top:26px;font-size:11px;color:var(--ink-faint);line-height:1.6}
.cardgrid{display:grid;grid-template-columns:minmax(0,1fr);gap:12px;margin:8px 0}
.cardgrid .card{margin:0;min-width:0;height:100%;display:flex;flex-direction:column}
.cardgrid .card .acts{margin-top:auto;padding-top:12px}
.cardgrid > .quiet-empty{grid-column:1/-1}
@media(min-width:1100px){.cardgrid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}
@media(min-width:1500px){.cardgrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
.card .why{max-width:64ch}
.tl li{max-width:72ch}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:9px;overflow:hidden;background:var(--inset)}
.seg a{padding:6px 12px;font-size:12px;font-weight:650;color:var(--ink-dim);min-height:36px;display:inline-flex;align-items:center;gap:4px;letter-spacing:0;text-transform:none;font-family:var(--sans)}
.seg a+a{border-left:1px solid var(--line)}
.seg a.on{background:var(--ember);color:#1d0f06}
.seg a:not(.on):hover{color:var(--ink);background:var(--panel2)}
.seg .segi{font-size:11px;opacity:.9}
.sugc{position:relative}
.sugc .shot{display:block;margin:-16px -16px 12px;border-bottom:1px solid var(--line-soft);border-radius:9px 9px 0 0;overflow:hidden;background:#141110}
.sugc .shot img{display:block;width:100%;height:108px;object-fit:cover;object-position:top;opacity:.92;transition:opacity .15s ease}
.sugc .shot:hover img{opacity:1}
.srcopen{color:inherit;border-bottom:1px dotted var(--line);padding-bottom:1px;display:inline-flex;align-items:center;min-height:24px}
.srcopen:hover{color:var(--ink-dim);border-bottom-color:var(--ink-faint)}
.whorow{display:flex;align-items:center;gap:8px}
.whorow .chip{flex-shrink:0}
.whorow .srcopen{flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.whorow .pick{min-height:30px;padding:0 8px}
.acts .soft{background:rgba(213,94,46,.1);color:var(--ember-tx);border:1px solid rgba(213,94,46,.32)}
.acts .soft:hover{background:rgba(213,94,46,.17)}
.sugc .acts{align-items:center}
.sugc .acts .pick{margin-left:auto}
.libgrid{display:grid;grid-template-columns:1fr;gap:8px}
.libgrid .lib{margin:0}
@media(min-width:900px){.libgrid{grid-template-columns:1fr 1fr}}
@media(min-width:1400px){.libgrid{grid-template-columns:repeat(3,1fr)}}
@media(prefers-reduced-motion:reduce){
*,::before,::after{transition-duration:.01ms!important;animation-duration:.01ms!important}
::view-transition-old(root),::view-transition-new(root){animation:none}}
"""



ROSTER = [
    ("Ranger", "🔍", "researches users and market — interviews, evidence", "/guild-agent-ranger"),
    ("Cartographer", "🗺️", "organizes the product — IA, sitemaps, user flows on boards", "/guild-agent-cartographer"),
    ("Rogue", "🔀", "designs interactions — flows, wireframes, states", "/guild-agent-rogue"),
    ("Mage", "🎨", "designs visuals — critique, polish, motion, variants", "/guild-agent-mage"),
    ("Warlock", "✍️", "writes the words — microcopy, errors, voice", "/guild-agent-warlock"),
    ("Tinker", "🔧", "builds the design system — components, tokens", "/guild-agent-tinker"),
    ("Sage", "🛡️", "quality gate — accessibility, consistency, go/no-go", "/guild-agent-sage"),
    ("Healer", "📦", "hands off to dev — specs, stories, tokens", "/guild-agent-healer"),
    ("Guild Master", "🎯", "runs the whole pipeline — point it at a goal", "/guild-quest"),
]

AGENT_METHODS = [
    ("Ranger", "🔍", "Research", "Evidence, interviews, synthesis, method choice", "/guild-agent-ranger"),
    ("Cartographer", "🗺️", "Structure", "IA, sitemaps, content models, navigation", "/guild-agent-cartographer"),
    ("Rogue", "🔀", "Interaction", "Flows, wireframes, states, task paths", "/guild-agent-rogue"),
    ("Mage", "🎨", "Visual", "Critique, polish, hierarchy, motion", "/guild-agent-mage"),
    ("Warlock", "✍️", "Words", "Microcopy, empty states, naming, voice", "/guild-agent-warlock"),
    ("Tinker", "🔧", "System", "Components, tokens, variants, Storybook", "/guild-agent-tinker"),
    ("Sage", "🛡️", "Quality", "A11y, responsive, consistency, go/no-go", "/guild-agent-sage"),
    ("Healer", "📦", "Handoff", "Specs, stories, annotations, release notes", "/guild-agent-healer"),
    ("Guild Master", "🎯", "Orchestration", "Quest, sprint, review packet, routing", "/guild-agent-guild-master"),
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
    return (f'<label class="swlab" for="projsel">Project</label>'
            f'<select id="projsel" class="topsel" onchange="location.href=this.value" aria-label="switch project">'
            f'{"".join(opts)}</select>')


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
                     "summon Ranger to build a research file from existing evidence, or synthesize fresh research",
                     "/guild-agent-ranger — build the research file from existing evidence; if no real research exists, run research synthesis instead",
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
                     "summon Mage for auto-critique: capture key screens, critique craft, and run the scripted gates",
                     "/guild-agent-mage — run AC / auto-critique on the key screens, then report gate findings",
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
                     "summon Sage for the pre-handoff decision packet: approve / waive / redo",
                     "/guild-agent-sage — run PR / pre-handoff and compile one decision packet",
                     f'checked: {len(feed["runs"])} run(s) recorded but no batched-review packet — findings exist that never became decisions',
                     "light-medium — one agent compiling what already exists"))
    if not recs:
        recs.append(("Ship or extend", "/guild-quest for the next feature, or /guild-comment on anything that feels off",
                     "/guild-quest", "checked: research, taste, runs, and decisions are all in place — this project is healthy",
                     "heavy — a full pipeline run; only start it deliberately"))
    return recs[:4]


def sparkline(vals, w=112, h=20):
    """Device-light inline-SVG sparkline (no charting lib). Empty string if no signal."""
    vals = [v for v in (vals or [])]
    if not vals or sum(vals) == 0:
        return ""
    n, mx = len(vals), (max(vals) or 1)
    pts = []
    for i, v in enumerate(vals):
        x = round(i * (w / (n - 1)), 1) if n > 1 else 0
        y = round(h - (v / mx) * (h - 3) - 1.5, 1)
        pts.append(f"{x},{y}")
    return (f'<svg class="spark" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">'
            f'<polyline points="{" ".join(pts)}" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def _day_buckets(times, days=12):
    now = time.time()
    b = [0] * days
    for t in times:
        try:
            d = int((now - float(t)) / 86400)
        except (TypeError, ValueError):
            continue
        if 0 <= d < days:
            b[days - 1 - d] += 1
    return b


def mtile(href, num, label, sub="", spark="", accent=False):
    return (f'<a class="mtile{" hero" if accent else ""}" href="{href}">'
            f'<div class="mlab">{label}</div><div class="mnum">{num}</div>'
            f'<div class="msub">{E(sub)}</div>{spark}</a>')


def page(title, crumb, body, current=None, app=False):
    home_link = "" if crumb.startswith("everything") else '<a class="home" href="/">Back to all projects</a>'
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title) if title.startswith("GUILD") else "GUILD Hall · " + E(title)}</title><style>{CSS}</style>'
            f'<script>try{{var d=document.documentElement;["navmin","railmin"].forEach(function(k){{if(localStorage.getItem("hall_"+k)==="1")d.classList.add(k)}})}}catch(e){{}}</script></head><body class="{"app" if app else ""}">'
            f'<div class="top"><div class="gm">G</div><h1>{E(title)}</h1><span class="crumb">{crumb}</span>'
            f'<nav aria-label="switch project" style="display:contents">{switcher(current)}</nav>{home_link}'
            f'<details class="runner"><summary>Runner</summary><div class="runcfg"><span class="swlab">Default model</span>'
            f'<select id="runmodel" class="fsel" aria-label="model to launch runs with">'
            f'<option value="codex" selected>Codex</option><option value="claude-code">Claude</option>'
            f'<option value="gemini">Gemini</option><option value="cursor-agent">Cursor</option></select>'
            f'<label class="pick"><input type="checkbox" id="runreuse"> reuse one pane for short follow-ups</label>'
            f'<span class="who" style="margin:0">Codex by default to conserve Claude · use Claude for judgment-heavy critique/research · raids always use all 3 models</span></div></details></div>'
            f'<main>{body}</main>'
            f'<div class="foot">GUILD HALL · your delegated-work inbox — agents do the work, decisions come to you. '
            f'Quiet inbox = agents working, nothing needs you.</div></body></html>')


def chip(state):
    cls = {"waiting for you": "wait", "executing": "exec", "finished": "done", "thinking": "think"}.get(state, "think")
    return f'<span class="chip {cls}">{E(state)}</span>'


def kicon(kind):
    """Map a library/artifact kind to a clean glyph (beats cryptic kind[:5] truncation)."""
    k = (kind or "").lower()
    for needle, glyph in (("token", "🎨"), ("design-system", "🎨"), ("ds", "🎨"),
                          ("claude", "📦"), ("bundle", "📦"), ("cd", "📦"),
                          ("research", "🔍"), ("spec", "📐"), ("story", "📝"),
                          ("flow", "🔀"), ("wireframe", "▢"), ("figma", "🖼"),
                          ("run", "▶"), ("report", "📊")):
        if needle in k:
            return glyph
    return "📄"


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
        body = (f'{hometabs}<div style="font-size:11px;color:var(--ink-faint);margin:6px 2px 10px">'
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
    body = (f'{hometabs}<div class="brief">Across every project: {hdr}. Open a card only when the decision is yours.</div>'
            f'<h2 class="sect">Needs you</h2><div class="cardgrid">{inbox}</div>'
            f'<h2 class="sect">Your projects</h2><div class="pgrid">{"".join(grid)}</div>{JS}')
    return page("GUILD Hall", "everything you delegated, one inbox", body)


def chrome(wf, pidx, active="needs", feed=None):
    """Nav sidebar + context rail shared by every project page — keeps both sidebars always present."""
    p = projects()[pidx]
    if feed is None:
        feed = wf.build(p["path"])
    its = items_for(feed, p["name"])
    ndec = sum(1 for i in its if i["kind"] == "decision")
    nruns = sum(1 for i in its if i["kind"] == "run")
    nsugg = 0
    for base in ("_bmad-output", "guild-output"):
        sf = os.path.join(p["path"], base, "guild-artifacts", "suggestions.yaml")
        if os.path.exists(sf):
            import yaml as _y
            nsugg = len((_y.safe_load(open(sf)) or {}).get("suggestions", []))
            break
    hs = nsugg > 0
    def nv(href, label, icon, cnt=None, on=False, sec=None):
        c = f'<span class="cnt">{cnt}</span>' if cnt is not None else ""
        extra = f' data-navsec="{sec}"' if sec else ""
        return (f'<a href="{href}" class="navitem {"on" if on else ""}"{extra}>'
                f'<span class="nvi" aria-hidden="true">{icon}</span><span class="nvl">{label}</span>{c}</a>')
    def grp(title, links):
        t = f'<div class="grp">{title}</div>' if title else ""
        return f'<div class="ngrp">{t}' + "".join(links) + '</div>'
    side = ('<aside class="snav" aria-label="project navigation">'
            + '<div class="sbhead"><div class="grp">Decide</div>'
            + '<button class="ptog navtog" onclick="tpane(\'navmin\')" aria-label="collapse navigation" title="collapse sidebar">‹</button></div>'
            + grp(None, [
                nv(f"/p/{pidx}?view=needs#decisions", "Needs you", "📥", ndec, active == "needs", sec=("decisions" if hs else None)),
                nv(f"/p/{pidx}?view=needs#improve", "Improvements", "💡", nsugg, sec=("improve" if hs else None)),
                nv(f"/p/{pidx}?view=needs#recs", "What to run next", "⚡"),
                nv(f"/expedition?p={pidx}", "Expedition", "🧭", on=(active == "expedition"))])
            + grp("Watch", [nv(f"/p/{pidx}?view=runs", "Runs", "▶️", nruns, active == "runs")])
            + grp("Browse", [
                nv(f"/p/{pidx}?view=library", "Library", "📚", len(feed["library"]), active == "library"),
                nv(f"/playbook?p={pidx}", "Playbook", "📖", on=(active == "playbook"))])
            + grp("People", [
                nv(f"/p/{pidx}?view=needs#roster", "Your guild", "👥"),
                nv(f"/p/{pidx}?view=needs#bmad", "Build council", "🛠")])
            + '</aside>')
    def _rrow(name, icon, job, cmd):
        return (f'<div class="lib" title="{E(name)} — {E(job)}"><span class="th" style="font-size:15px">{icon}</span>'
                f'<span><b>{name}</b><div>{E(job)}</div></span>'
                f'<button class="obtn" onclick="run(this,{pidx},\'{cmd}\')">Summon</button></div>')
    rail = ('<div class="sbhead"><h3 class="railh">Your guild <span class="railh-sub">summon a specialist</span></h3>'
            '<button class="ptog railtog" onclick="tpane(\'railmin\')" aria-label="collapse context panel" title="collapse panel">›</button></div>'
            f'<section class="railsect" id="roster">'
            f'<div class="raillist">{"".join(_rrow(*r) for r in ROSTER)}</div></section>'
            f'<section class="railsect" id="bmad"><h3 class="railh">Build council <span class="railh-sub">plans &amp; builds in a full quest</span></h3>'
            f'<div class="raillist">{"".join(_rrow(*r) for r in BMAD_ROSTER)}</div></section>')
    return side, rail


def project_shell(wf, pidx, active, inner):
    """Wrap page-specific inner content in the standard project chrome (both sidebars + app shell)."""
    side, rail = chrome(wf, pidx, active)
    shell = f'<div class="shell three">{side}<section class="mainpane">{inner}</section><aside class="rail">{rail}</aside></div>'
    return page(projects()[pidx]["name"], "a project in your hall", shell + JS, current=pidx, app=True)


def _shot_for(proj_path, evidence):
    """Map a suggestion's evidence path (src/app/(app)/spend/page.tsx) to a captured
    screenshot of that screen, if one exists in guild-artifacts/screenshots/.
    Returns (output_base, filename, slug) or None."""
    segs = [s for s in evidence.split("/") if s not in ("src", "app", "pages") and not s.startswith("(")]
    segs = [s for s in segs if "." not in s]
    slug = segs[-1] if segs else "home"
    for base in ("_bmad-output", "guild-output"):
        d = os.path.join(proj_path, base, "guild-artifacts", "screenshots")
        if os.path.isdir(d):
            pngs = sorted(f for f in os.listdir(d) if f.endswith(".png"))
            for pref in (f"{slug}-desktop", slug):
                for f in pngs:
                    if f.startswith(pref):
                        return base, f, slug
    return None


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
    # Suggestion filters live WITH the suggestions (main content), not in the nav.
    sbar = ""
    if view == "needs" and ss:
        conf_chips = (f'<button class="fbtn on" data-k="conf" data-f="all" onclick="sflt(this)">All ({nsugg})</button>'
                      f'<button class="fbtn" data-k="conf" data-f="firm" onclick="sflt(this)">Missing a basic ({sfirm})</button>'
                      f'<button class="fbtn" data-k="conf" data-f="check" onclick="sflt(this)">Worth a look ({nsugg - sfirm})</button>')
        cat_chips = "".join(f'<button class="fbtn" data-k="cat" data-f="{E(c)}" onclick="sflt(this)">{sicon[c]} {E(c)} ({n})</button>'
                            for c, n in sorted(scats.items(), key=lambda kv: -kv[1]))
        screen_sel = (f'<select class="fsel" onchange="sscr(this)" aria-label="filter by screen">'
                      f'<option value="all">every screen ({len(sscreens)})</option>'
                      + "".join(f'<option value="{E(s)}">{E("/".join(s.split("/")[-2:]))} ({sum(1 for x in ss if x["evidence"] == s)})</option>' for s in sscreens)
                      + '</select>')
        sbar = ('<details class="filtermenu"><summary class="fmbtn">'
                '<span aria-hidden="true">⚑</span> Filters<span class="fmdot" id="fmdot" hidden></span></summary>'
                '<div class="fmpop" role="menu">'
                f'<div class="fmgroup"><span class="fmlab">Confidence</span><div class="fmchips">{conf_chips}</div></div>'
                f'<div class="fmgroup"><span class="fmlab">Category</span><div class="fmchips">{cat_chips}</div></div>'
                f'<div class="fmgroup"><span class="fmlab">Screen</span>{screen_sel}</div>'
                '</div></details>')
    side, rail = chrome(wf, pidx, view, feed=feed)
    explain = {"needs": "Decisions agents queued for you — everything else keeps moving without you.",
               "runs": "What agents did, step by step — each run is a checklist of completed work.",
               "library": "Everything this project produced, newest first."}
    body = f'<div class="brief">{explain[view]}</div>'
    if view == "needs":
        rec_data = recommends(feed, p["path"])
        def rec_card(title, why, cmd, because, cost, compact=False):
            if cmd == "top":
                return (f'<div class="card"><div class="row"><span class="kic">→</span><b>{E(title)}</b></div>'
                        f'<div class="brief">{E(why)}</div></div>')
            cta = "Run it" if compact else "Run it — Guild opens an agent and starts"
            return (
            f'<div class="card"><div class="row"><span class="kic">→</span><b>{E(title)}</b>'
            + f'</div><div class="brief">{E(why)}</div>'
            + f'<div class="acts"><button onclick="run(this,{pidx},\'{E(cmd)}\')">{cta}</button></div>'
            + f'<details class="metafold"><summary>Details, queue, model</summary>'
               f'<div class="kmeta"><span class="klabel">why</span><span class="kv">{E(because)}</span></div>'
               f'<div class="kmeta"><span class="klabel">cost</span><span class="kv">{E(cost)}</span></div>'
               f'<label class="pick" style="margin-left:0"><input type="checkbox" class="pickbox" data-pidx="{pidx}" data-cmd="{E(cmd)}">queue for batch</label>'
               f'<div class="who">Manual command: {E(cmd)}</div></details></div>')
        rec_rows = rec_card(*rec_data[0]) if rec_data else ""
        if len(rec_data) > 1:
            rec_rows += (f'<details class="metafold"><summary>More recommended runs ({len(rec_data)-1})</summary>'
                         f'<div class="cardgrid">{"".join(rec_card(*r, compact=True) for r in rec_data[1:])}</div></details>')
        cards = "".join(decision_card(i, pidx) for i in its if i["kind"] == "decision") \
            or ('<div class="quiet-empty"><span class="pulse"></span>Nothing needs you in this project. '
                'Agents keep working; decisions land here.</div>')
        sugg_rows = ""
        if ss:
            toggle = (f'<span class="seg" role="group" aria-label="view as cards or list">'
                      f'<a href="/p/{pidx}?view=needs&sv=cards" class="{"on" if sv == "cards" else ""}"><span class="segi" aria-hidden="true">▦</span> Cards</a>'
                      f'<a href="/p/{pidx}?view=needs&sv=list" class="{"on" if sv == "list" else ""}"><span class="segi" aria-hidden="true">☰</span> List</a></span>')
            pager = ('<span class="spage"><button class="fbtn" onclick="spg(-1)" aria-label="previous page">←</button>'
                     '<b id="spglab" style="font-size:11px;min-width:86px;text-align:center"></b>'
                     '<button class="fbtn" onclick="spg(1)" aria-label="next page">→</button></span>') if sv == "cards" else ""
            qall = '<button class="fbtn" id="qallbtn" onclick="qall()">Queue all</button>'
            shots = {ev: _shot_for(p["path"], ev) for ev in {s["evidence"] for s in ss}} if sv == "cards" else {}

            def _srow(s):
                icon, cat = s.get("icon", "💡"), s.get("category", "polish")
                conf = s["confidence"]
                cchip = f'<span class="chip {"wait" if conf == "firm" else "think"}">{"missing a basic" if conf == "firm" else "worth a look"}</span>'
                pick = (f'<label class="pick"><input type="checkbox" class="pickbox" data-pidx="{pidx}" '
                        f'data-cmd="/guild-comment {E(s["title"])} — {E(s["evidence"])}">queue</label>')
                attrs = f'data-conf="{conf}" data-screen="{E(s["evidence"])}" data-cat="{E(cat)}"'
                if sv == "list":
                    return (f'<div class="lib sugc" {attrs}><span class="th" style="font-size:13px">{icon}</span>'
                            f'<span><b>{E(s["title"])}</b><div class="m">{E(s["why"][:110])}</div></span>'
                            f'<span class="chip proj" style="flex-shrink:0">{E(cat)}</span>{cchip}{pick}</div>')
                sh = shots.get(s["evidence"])
                shot = ""
                if sh:
                    url = f'/img?p={pidx}&b={sh[0]}&f={E(sh[1])}'
                    shot = (f'<a class="shot" href="{url}" target="_blank" rel="noopener" title="open the {E(sh[2])} screen capture">'
                            f'<img src="{url}" loading="lazy" alt="capture of the {E(sh[2])} screen"></a>')
                src_link = (f'<a class="srcopen" href="/open?path={E(os.path.join(p["path"], s["evidence"]))}" '
                            f'title="open the source file">{E(s["evidence"])}</a>')
                return (f'<div class="card sugc" {attrs}>{shot}<div class="row"><span class="kic">{icon}</span>'
                        f'<b>{E(s["title"])}</b>{cchip}</div>'
                        f'<div class="why">{E(s["why"])}</div>'
                        f'<div class="who whorow"><span class="chip proj">{E(cat)}</span> {src_link}{pick}</div>'
                        f'<div class="acts"><button class="soft" onclick="run(this,{pidx},\'/guild-comment {E(s["title"])} — {E(s["evidence"])}\')">'
                        f'Have Guild fix it — 3 variants</button></div></div>')

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
            sugg_rows = (f'<h2 class="sect" id="improve">UX improvements Guild noticed</h2>'
                         f'<div class="toolbar">{sbar}{qall}{toggle}{pager}</div>'
                         f'<div class="cardgrid" id="sgrid" data-mode="{sv}">{sugg_rows}</div>')
        # ---- dashboard: signal metrics row + "your move" hero (owner-approved Desk pattern) ----
        working = sum(1 for r in feed["runs"] if r.get("state") == "executing")
        run_spark = sparkline(_day_buckets([os.path.getmtime(r["path"]) for r in feed["runs"] if os.path.exists(r.get("path", ""))]))
        art_spark = sparkline(_day_buckets([it.get("mtime") for it in feed["library"]]))
        metrics = ('<div class="metrics">'
                   + mtile(f'/p/{pidx}?view=needs#decisions', ndec, "needs you", "decisions waiting" if ndec else "all clear", accent=(ndec > 0))
                   + mtile(f'/p/{pidx}?view=runs', working, "agents working", "in flight" if working else "idle")
                   + mtile(f'/p/{pidx}?view=runs', len(feed["runs"]), "runs", "step logs", run_spark)
                   + mtile(f'/p/{pidx}?view=library', len(feed["library"]), "artifacts", "produced", art_spark)
                   + mtile(f'/p/{pidx}?view=needs#improve', nsugg, "ideas", "Guild noticed")
                   + '</div>')
        decs = [i for i in its if i["kind"] == "decision" and i.get("id") != "note"]
        if decs:
            top, more = decs[0], len(decs) - 1
            hero = (f'<div class="yourmove"><div class="ymlab">most urgent · your move</div>'
                    f'<div class="ymtitle">{E(top["title"])}</div>'
                    f'<div class="ymwhy">{E((top.get("why") or top.get("detail") or "")[:200])}</div>'
                    f'<div class="ymacts"><a class="hbtn" href="#decisions">Review it &rarr;</a>'
                    + (f'<a class="hmore" href="#decisions">{more} more move{"s" if more != 1 else ""} &rarr;</a>' if more > 0 else "")
                    + '</div></div>')
        elif rec_data and rec_data[0][2] != "top":
            t, more = rec_data[0], len(rec_data) - 1
            hero = (f'<div class="yourmove"><div class="ymlab">next move · recommended</div>'
                    f'<div class="ymtitle">{E(t[0])}</div><div class="ymwhy">{E(t[1][:200])}</div>'
                    f'<div class="ymacts"><button class="hbtn" onclick="run(this,{pidx},\'{E(t[2])}\')">Run it &rarr;</button>'
                    + (f'<a class="hmore" href="#recs">{more} more &rarr;</a>' if more > 0 else "")
                    + '</div></div>')
        else:
            hero = '<div class="yourmove calm"><div class="ymlab">all clear</div><div class="ymtitle">Nothing needs you</div><div class="ymwhy">Agents keep working; decisions land here when they are yours to make.</div></div>'
        body = metrics + hero
        # widget switcher: nav toggles between the Decisions and UX-improvements widgets
        if ss:
            body += (f'<div class="wtabs" role="tablist">'
                     f'<button class="wtab on" data-sec="decisions" onclick="focusW(\'decisions\')">Decisions waiting <span class="wtc">{ndec}</span></button>'
                     f'<button class="wtab" data-sec="improve" onclick="focusW(\'improve\')">UX improvements <span class="wtc">{nsugg}</span></button></div>')
        # header text lives in the widget-tab when the toggle is present; keep just the anchor
        dsect = '<span id="decisions"></span>' if ss else (f'<h2 class="sect" id="decisions">Decisions waiting</h2>' if any(i["kind"] == "decision" for i in its) else '<span id="decisions"></span>')
        w_dec = f'<section class="widget" data-sec="decisions" id="w-decisions">{dsect}<div class="cardgrid feed">{cards}</div></section>'
        w_imp = f'<section class="widget" data-sec="improve" id="w-improve" hidden>{sugg_rows}</section>' if ss else ""
        body += w_dec + w_imp + f'<h2 class="sect" id="recs">What Guild would run next</h2><div class="cardgrid feed">{rec_rows}</div>'

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
                body += (f'<div class="lib"><span class="th" style="font-size:15px">{kicon(d["kind"])}</span><span><b>{E(d["name"])}</b>'
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
            body += (f'<div class="lib"><span class="th" style="font-size:15px">{kicon(it["kind"])}</span><span><b>{E(it["name"])}</b></span>'
                     f'<span class="m">{when} · <a href="/open?path={E(it["path"])}" style="color:var(--ember-tx)">open</a></span></div>')
    shell = f'<div class="shell three">{side}<section class="mainpane">{body}</section><aside class="rail">{rail}</aside></div>'
    return page(p["name"], "a project in your hall", shell + JS, current=pidx, app=True)


JS = """<script>
function tpane(k){var d=document.documentElement;d.classList.toggle(k);try{localStorage.setItem('hall_'+k,d.classList.contains(k)?'1':'0');}catch(e){}}
function focusW(sec){
  if(!document.querySelector('.widget[data-sec="'+sec+'"]'))sec='decisions';
  document.querySelectorAll('.widget[data-sec]').forEach(function(w){w.hidden=(w.getAttribute('data-sec')!==sec);});
  document.querySelectorAll('.wtab[data-sec]').forEach(function(t){t.classList.toggle('on',t.getAttribute('data-sec')===sec);});
  document.querySelectorAll('.navitem[data-navsec]').forEach(function(a){a.classList.toggle('on',a.getAttribute('data-navsec')===sec);});
  try{localStorage.setItem('hall_sec',sec);}catch(e){}
}
(function(){
  if(!document.querySelector('.widget[data-sec]'))return;
  var sec='decisions';
  try{if(localStorage.getItem('hall_sec')==='improve')sec='improve';}catch(e){}
  if(location.hash==='#improve')sec='improve';
  if(location.hash==='#decisions')sec='decisions';
  focusW(sec);
  window.addEventListener('hashchange',function(){
    if(location.hash==='#improve')focusW('improve');
    else if(location.hash==='#decisions'||location.hash==='')focusW('decisions');
  });
})();
function launchCfg(){
  const m = document.getElementById('runmodel'), r = document.getElementById('runreuse');
  return {adapter: m ? m.value : 'codex', reuse: r ? r.checked : false};
}
(function(){
  const m = document.getElementById('runmodel'), r = document.getElementById('runreuse');
  try {
    if (m && localStorage.guildAdapter) m.value = localStorage.guildAdapter;
    if (r && localStorage.guildReuse === '1') r.checked = true;
  } catch(e){}
  if (m) m.addEventListener('change', () => { try { localStorage.guildAdapter = m.value; } catch(e){} });
  if (r) r.addEventListener('change', () => { try { localStorage.guildReuse = r.checked ? '1' : '0'; } catch(e){} });
})();
async function run(btn, pidx, cmd){
  const cm = btn.closest('.card,.lib')?.querySelector('.cardmodel'); const cfg = launchCfg();
  const label = btn.textContent; btn.disabled = true; btn.textContent = "launching agent…";
  const r = await fetch('/run', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({pidx, cmd, adapter: cm ? cm.value : cfg.adapter, reuse: cfg.reuse})});
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
        body: JSON.stringify({pidx: +c.dataset.pidx, cmd: c.dataset.cmd, ...launchCfg()})});
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
  const qb = document.getElementById('qallbtn');
  if (qb) { const bs = vis.map(c => c.querySelector('.pickbox')).filter(b => b && !b.disabled);
    qb.textContent = (bs.length && bs.every(b => b.checked)) ? 'Unqueue all' : 'Queue all'; }
}
function qall(){
  const g = document.getElementById('sgrid'); if (!g) return;
  const vis = [...g.querySelectorAll('[data-conf]')].filter(c => (SP.conf == 'all' || c.dataset.conf == SP.conf)
    && (SP.cat == 'all' || c.dataset.cat == SP.cat) && (SP.screen == 'all' || c.dataset.screen == SP.screen));
  const bs = vis.map(c => c.querySelector('.pickbox')).filter(b => b && !b.disabled);
  const all = bs.length && bs.every(b => b.checked);
  bs.forEach(b => { b.checked = !all; });
  syncbar(); sapply();
}
window.addEventListener('DOMContentLoaded', sapply);
async function explaunch(pidx){
  const provs = [...document.querySelectorAll('.wsel:checked')].map(c => c.value);
  const st = document.getElementById('expstatus');
  if (!provs.length) { st.innerHTML = '<div class="confirm" role="status">Pick at least one researcher first.</div>'; return; }
  const ask = (document.getElementById('expask').value || '').trim();
  const cmd = '/guild-expedition — providers: ' + provs.join(', ')
    + (ask ? ' — rough ask: ' + ask : ' — ask me for the rough question, then forge and run the wave');
  st.innerHTML = '<div class="confirm" role="status">launching ' + provs.length + ' researcher' + (provs.length>1?'s':'') + '…</div>';
  try {
    const r = await fetch('/run', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({pidx, cmd, ...launchCfg()})});
    const d = await r.json();
    st.innerHTML = '<div class="confirm" role="status">' + (d.ok ? '✓ ' : '✗ ') + d.message + '</div>';
  } catch (e) { st.innerHTML = '<div class="confirm" role="status">✗ ' + e + '</div>'; }
}
function injectCardModels(){
  const g = (document.getElementById('runmodel')||{}).value || 'codex';
  document.querySelectorAll('button[onclick*="run(this,"]').forEach(b => {
    if (b.dataset.hasmodel) return;
    const oc = b.getAttribute('onclick') || '';
    if (/raid/i.test(oc)) { b.dataset.hasmodel='1'; return; }   // raids use all 3 models
    b.dataset.hasmodel = '1';
    const s = document.createElement('select'); s.className = 'cardmodel';
    s.setAttribute('aria-label', 'model for this run');
    [['codex','Codex'],['claude-code','Claude'],['gemini','Gemini'],['cursor-agent','Cursor']].forEach(([v,l]) => {
      const o = document.createElement('option'); o.value = v; o.textContent = l;
      if (v === g) o.selected = true; s.appendChild(o);
    });
    const fold = b.closest('.card,.lib')?.querySelector('.metafold');
    if (fold) {
      const line = document.createElement('div'); line.className = 'who'; line.textContent = 'Model override';
      fold.appendChild(line); fold.appendChild(s);
    } else {
      b.parentNode.insertBefore(s, b);
    }
  });
}
window.addEventListener('DOMContentLoaded', injectCardModels);
function clearsel(){ document.querySelectorAll('.pickbox:checked').forEach(c => c.checked = false); syncbar(); sapply(); }
document.addEventListener('change', e => { if (e.target.classList.contains('pickbox')) { syncbar(); sapply(); } });
</script>"""


# ── the write channel ────────────────────────────────────────────────────────

# Organized by WORKFLOW PHASE, and within each phase by the DISCIPLINE that owns it.
# Each specialist's raid (that discipline across 3 models) lives with its discipline —
# ranger-raid is research, not "design & build" (owner, 2026-07-03).
PLAYBOOK = [
    ("Set up your project \u00b7 once", [
        ("/guild-design-direction", "Tell Guild your taste ONCE \u2014 ~10 min of questions about look, feel, references. Every agent afterward designs to your answers instead of re-asking.", "light \u2014 mostly your answers"),
        ("/guild-charter", "Set the autonomy contract: what agents may decide alone vs. must bring to you. This is why your inbox stays quiet.", "light \u2014 a short conversation"),
        ("/guild-agent-ranger — build the research file from existing evidence", "Already have research docs, notes, interviews? Ranger turns them into a research file Guild can cite, so decisions point at proof.", "medium \u2014 one agent reads your corpus"),
    ]),
    ("Research your users \u00b7 Ranger \U0001f50d", [
        ("/guild-agent-ranger — run RS / research synthesis", "Fresh research from zero \u2014 questions, sources, verified facts. Every claim ends up either backed by a source or honestly cut.", "medium-heavy \u2014 real research takes agent time"),
        ("/ranger-raid", "Your research question answered three ways \u2014 Ranger runs on Claude, Codex, and Gemini in parallel and the strongest findings are synthesized. Use when the research really matters.", "heavy \u2014 3 models researching at once"),
    ]),
    ("Map the structure \u00b7 Cartographer \U0001f5fa\ufe0f", [
        ("/guild-agent-cartographer — run IA / information architecture", "Plans the app's structure from the research \u2014 screen map, flows, what lives where. It refuses to invent structure without evidence.", "medium \u2014 needs the research step first"),
    ]),
    ("Design the experience \u00b7 Rogue / Mage / Warlock", [
        ("/guild-design-sprint", "The design phases in sequence (research \u2192 interaction \u2192 visual \u2192 content \u2192 QA), no code build. For when you want designs to react to first.", "medium-heavy"),
        ("/guild-render", "One design model fanned out to every platform at once \u2014 native FigJam board + clickable HTML prototype. Change the model, re-run, both update.", "light \u2014 scripted, seconds"),
        ("/rogue-raid", "Interaction & flow design from three engines at once, best take synthesized (Rogue \U0001f500).", "heavy \u2014 3 models"),
        ("/mage-raid", "Visual design three ways \u2014 three independent looks, the strongest synthesized (Mage \U0001f3a8).", "heavy \u2014 3 models"),
        ("/warlock-raid", "Content & copy three ways, best synthesized (Warlock \u270d\ufe0f).", "heavy \u2014 3 models"),
    ]),
    ("Judge & fix \u00b7 Sage \U0001f6e1\ufe0f", [
        ("/guild-agent-mage — run AC / auto-critique", "Point Mage at a screen: critique like a design lead + every craft gate runs (spacing, type, tokens, states, motion, a11y). Findings, not vibes.", "medium \u2014 one agent per screen; gates are free"),
        ("/guild-comment", "Anything feel off? Say it in plain words. Guild builds 3 real fixed variants and sends you a pick note with rendered pixels \u2014 you choose, it applies.", "medium \u2014 3 real patches get built"),
        ("/sage-raid", "Design QA from three engines \u2014 three independent quality reads, reconciled into one go/no-go.", "heavy \u2014 3 models"),
        ("/guild-agent-sage — run PR / pre-handoff", "Sweeps everything agents produced into ONE decision packet \u2014 approve / waive / redo. The end-of-run ritual before shipping.", "light-medium \u2014 compiles what exists"),
    ]),
    ("Run the whole pipeline", [
        ("/guild-quest", "THE BIG ONE. Idea in, working app out. BMAD plans it (PM scopes \u2192 Analyst digs into requirements \u2192 Architect shapes the tech \u2192 Scrum Master cuts it into stories), Guild designs it, then it gets built and tested \u2014 agents handing off to each other. Start it and watch this Hall.", "heavy \u2014 a full pipeline; start deliberately"),
        ("/guild-raid", "The FULL raid \u2014 EVERY specialist runs across all three models; the best take per discipline is synthesized. Heaviest option; big decisions only.", "heaviest \u2014 3\u00d7 everything"),
    ]),
    ("Summon one specialist", [
        ("/guild-agent-mage", "Talk to a single agent instead of a pipeline \u2014 Ranger (research), Cartographer (IA), Rogue (interaction), Mage (visual), Warlock (content), Sage (QA), Healer (handoff), Tinker (design systems). Every specialist runs solo like this OR as a 3-model raid. Full roster with Summon buttons lives on every project page.", "light \u2014 one conversation"),
    ]),
]

def _exp_mod():
    spec = importlib.util.spec_from_file_location("rf", os.path.join(HERE, "expedition.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def expedition_page(wf, pidx):
    p = projects()[pidx]
    rf = _exp_mod()
    default = set(rf.DEFAULT_PROVIDERS)
    cards = "".join(
        f'<label class="card wprov"><div class="row"><input type="checkbox" class="wsel" value="{slug}" '
        f'{"checked" if slug in default else ""}><b>{E(info["name"])}</b>'
        f'<span class="chip proj" style="margin-left:auto">{"on by default" if slug in default else "off"}</span></div>'
        f'<div class="why">{E(info.get("strength", ""))}</div></label>'
        for slug, info in rf.PROVIDERS.items())
    intro = ('<div class="card"><div class="why" style="font-size:13px">'
             'Guild forges your rough question into an excellent brief, then sends it to the deep-research '
             'products you pick below — each as a tab in one browser. Where they agree is solid; where they '
             'disagree is what you should look at. Runs take ~10–15 min each; pick your researchers, then launch.'
             '</div></div>')
    ask = ('<h2 class="sect">What do you want researched?</h2>'
           '<textarea id="expask" placeholder="A rough question is fine — Guild sharpens it into the brief. '
           'e.g. \'what mental model should Guild&#39;s UI adopt so it feels like a real app?\'" '
           'style="width:100%;min-height:90px;background:var(--inset);color:var(--ink);border:1px solid var(--line);'
           'border-radius:10px;padding:12px;font:inherit;font-size:13px"></textarea>')
    picker = f'<h2 class="sect">Pick your researchers</h2><div class="cardgrid">{cards}</div>'
    launch = ('<div class="acts" style="margin-top:16px"><button onclick="explaunch(%d)">'
              'Forge the brief &amp; launch the wave</button>'
              '<span class="who" style="align-self:center">opens each researcher as a tab in one browser</span></div>'
              '<div id="expstatus"></div>') % pidx
    inner = f'<h2 class="sect">Expedition — deep research wave</h2>{intro}{ask}{picker}{launch}'
    return project_shell(wf, pidx, "expedition", inner)


def playbook(wf=None, pidx=None):
    import re as _re
    runnable = pidx is not None and wf is not None
    pname = projects()[pidx]["name"] if pidx is not None else None
    heavy = ("/guild-quest", "/guild-raid", "/guild-design-sprint", "/ranger-raid", "/rogue-raid", "/mage-raid", "/warlock-raid", "/sage-raid")
    icons = {"/guild-design-direction": "🎨", "/guild-charter": "📜", "/guild-expedition": "🔭", "/guild-quest": "🏰",
             "/guild-design-sprint": "🖌️", "/guild-render": "🖼️", "/guild-raid": "⚔️",
             "/guild-comment": "💬", "/guild-agent-ranger": "🔍", "/guild-agent-cartographer": "🗺️",
             "/guild-agent-mage": "🎨", "/guild-agent-sage": "🛡️", "/guild-agent-guild-master": "🎯",
             "/ranger-raid": "🔍", "/rogue-raid": "🔀", "/mage-raid": "🎨", "/warlock-raid": "✍️", "/sage-raid": "🛡️"}
    agent_rows = "".join(
        f'<div class="lib"><span class="th">{icon}</span><span><b>{E(name)}</b>'
        f'<div class="m">{E(label)}</div><div style="font-size:11px;color:var(--ink-dim);margin-top:3px">{E(desc)}</div></span>'
        + (f'<button class="obtn" onclick="run(this,{pidx},\'{cmd}\')">Summon</button>' if runnable else '')
        + '</div>'
        for name, icon, label, desc, cmd in AGENT_METHODS)
    secs = []
    for title, cmds in PLAYBOOK:
        cards = []
        if title.startswith("Research your users") and runnable:
            cards.append(
                '<div class="card feat"><div class="row"><span class="kic">🔭</span>'
                '<b style="font-family:var(--mono);font-size:13px">/guild-expedition</b>'
                '<span class="chip wait">medium</span></div>'
                '<div class="brief">Send one research question to multiple deep-research products, then reconcile the reports.</div>'
                f'<div class="acts"><a href="/expedition?p={pidx}">Pick researchers &amp; run →</a></div>'
                '<details class="metafold"><summary>Details and cost</summary>'
                '<div class="why">Opens ChatGPT, Gemini, Perplexity, Claude as tabs in one browser. Where they agree is solid; where they disagree is what to inspect. Different from a raid: a raid runs Guild&#39;s own researcher on 3 reasoning models.</div>'
                '<div class="who">cost: medium — several browser runs, ~10–15 min each</div></details></div>')
        for cmd, what, cost in cmds:
            guard = (f"if(confirm('This starts a HEAVY run ({cmd}) on {pname} — proceed?'))" if cmd in heavy else "")
            display_cmd, intent = (cmd.split(" — ", 1) + [""])[:2] if " — " in cmd else (cmd, "")
            act = (f'<div class="acts"><button onclick="{guard}run(this,{pidx},\'{E(cmd)}\')">Run on {E(pname)}</button>'
                   f'<label class="pick"><input type="checkbox" class="pickbox" data-pidx="{pidx}" data-cmd="{E(cmd)}">queue</label></div>'
                   if runnable else f'<div class="who">open this Playbook from a project page to run it there</div>')
            tier = "heavy" if cmd in heavy else ("medium" if "medium" in cost else "light")
            tchip = {"light": "done", "medium": "wait", "heavy": "exec"}[tier]
            cards.append(f'<div class="card{" feat" if cmd in heavy else ""}"><div class="row">'
                         f'<span class="kic">{icons.get(display_cmd, "▶")}</span>'
                         f'<b style="font-family:var(--mono);font-size:13px">{E(display_cmd)}</b>'
                         f'<span class="chip {tchip}">{tier}</span></div>'
                         + (f'<div class="who">{E(intent)}</div>' if intent else '') +
                         f'<div class="brief">{E(what.split(" — ")[0])}</div>{act}'
                         f'<details class="metafold"><summary>Details and cost</summary>'
                         f'<div class="why">{E(what)}</div><div class="who">cost: {E(cost)}</div></details></div>')
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
    catalog = (f'<details class="metafold"><summary>Manual command surface ({len(rows)})</summary>'
               f'<div class="card" style="margin-top:10px">{"".join(rows)}</div></details>')
    intro = ('<div class="quiet-empty" style="text-align:left">'
             'Start with a specialist, not a catalog. Guild recommends work from each project page; this map is here when you want to drive directly.</div>')
    agents = f'<h2 class="sect">Talk to an agent</h2><div class="libgrid">{agent_rows}</div>'
    crumb = "pick an agent, not a command"
    title = f"Playbook \u00b7 {pname}" if runnable else "Playbook"
    inner = '<h2 class="sect">Playbook</h2>' + intro + agents + "".join(secs) + catalog
    if runnable:
        return project_shell(wf, pidx, "playbook", inner)
    html = page(title, crumb, inner + JS, current=pidx)
    if False:
        html = html.replace('<a class="home" href="/">',
                            f'<a class="home" href="/p/{pidx}">← Back to {E(pname)}</a>'
                            f'<a class="home" href="/">', 1)
    return html


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
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
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
        if u.path == "/expedition":
            return self._send(expedition_page(self.wf, int(q.get("p", ["0"])[0])))
        if u.path == "/playbook":
            pq = q.get("p", [None])[0]
            return self._send(playbook(self.wf, int(pq)) if pq is not None else playbook())
        if u.path.startswith("/p/") and u.path[3:].isdigit():
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
        if u.path == "/img":
            pidx = int(q.get("p", ["0"])[0])
            base = q.get("b", ["_bmad-output"])[0]
            fn = q.get("f", [""])[0]
            if base in ("_bmad-output", "guild-output"):
                d = os.path.realpath(os.path.join(projects()[pidx]["path"], base, "guild-artifacts", "screenshots"))
                fp = os.path.realpath(os.path.join(d, fn))
                if fp.startswith(d + os.sep) and os.path.exists(fp):
                    data = open(fp, "rb").read()
                    self.send_response(200)
                    self.send_header("Content-Type", "image/png")
                    self.send_header("Content-Length", str(len(data)))
                    self.send_header("Cache-Control", "max-age=300")
                    self.end_headers()
                    self.wfile.write(data)
                    return
            self.send_response(404); self.end_headers(); return
        if u.path == "/api/feed":
            pidx = int(q.get("pidx", ["0"])[0])
            return self._send(json.dumps(self.wf.build(projects()[pidx]["path"])), "application/json")
        self.send_response(404); self.end_headers()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        req = json.loads(self.rfile.read(n))
        _BUILD_CACHE.clear()  # a POST mutates state — next render must be fresh, not TTL-stale
        if self.path == "/run":
            pr = projects()[req["pidx"]]
            cli = os.environ.get("ATRIUM_CLI_PATH", "atrium")
            adapter = req.get("adapter") or "codex"
            if adapter not in ("claude-code", "codex", "gemini", "cursor-agent"):
                adapter = "codex"
            reuse = bool(req.get("reuse"))
            msg = (f'{req["cmd"]} — launched from GUILD Hall for the project at {pr["path"]}. '
                   f'Work in that project; deliver results to its guild-artifacts and the Hall inbox. '
                   f'Keep context lean: load only task-relevant files, summarize before long follow-ups, and prefer a fresh pane after large runs.')
            runner_file = os.path.expanduser("~/.config/guild/hall-runner.yaml")
            import yaml as _y
            try:
                pl = subprocess.run([cli, "pane", "list", "--json"], capture_output=True, text=True, timeout=10)
                panes = json.loads(pl.stdout)
            except Exception:
                panes = []
            live_ids = {x["id"] for x in panes}
            # reuse mode: one persistent "Guild Runner" pane PER adapter — feed successive
            # prompts into it (shared context, no pane sprawl). Dead runner -> re-created.
            if reuse:
                runners = (_y.safe_load(open(runner_file)) or {}) if os.path.exists(runner_file) else {}
                pane = runners.get(adapter)
                if pane in live_ids:
                    m = subprocess.run([cli, "agent", "message", pane, msg], capture_output=True, text=True, timeout=30)
                    return self._send(json.dumps({"ok": m.returncode == 0,
                        "message": f"sent to your {adapter} runner (same pane; summarize/clear after large runs) — running {req['cmd']}" if m.returncode == 0
                                   else (m.stderr or "message failed")[:140]}), "application/json")
            split = []
            hallpane = next((x["id"] for x in panes
                             if x.get("type") == "browser" and (x.get("name") or "").startswith("GUILD Hall")), None)
            if hallpane:
                split = ["--split", hallpane, "--direction", "right"]
            r = subprocess.run([cli, "pane", "create", "--adapter", adapter, "--cwd", pr["path"], *split],
                               capture_output=True, text=True, timeout=30)
            pane = ""
            for tok in (r.stdout + r.stderr).split():
                if len(tok) >= 8 and all(c in "0123456789abcdef-" for c in tok[:8]): pane = tok; break
            if r.returncode != 0 or not pane:
                return self._send(json.dumps({"ok": False, "message": (r.stderr or "pane create failed")[:140]}), "application/json")
            if reuse:
                runners = (_y.safe_load(open(runner_file)) or {}) if os.path.exists(runner_file) else {}
                runners[adapter] = pane
                os.makedirs(os.path.dirname(runner_file), exist_ok=True)
                _y.safe_dump(runners, open(runner_file, "w"))
            time.sleep(4)   # let the adapter boot before the instruction lands
            m = subprocess.run([cli, "agent", "message", pane, msg], capture_output=True, text=True, timeout=30)
            ok = m.returncode == 0
            where = (f"your new {adapter} runner (reuse only for short follow-ups)" if reuse
                     else "beside the Hall in this room" if split else "in a new room")
            return self._send(json.dumps({"ok": ok,
                "message": f"{adapter} agent launched {where} — running {req['cmd']}" if ok
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
            _BUILD_CACHE.clear()  # mutation happened — feed must reflect it (as the POST handler does live)
            pv2 = project_view(wf, 0, "needs")
            ok = ok and "Agents keep working" in pv2
            import re as _re
            used = set()
            for html in (h, pv, rv, playbook(wf, 0), playbook()):
                for m in _re.finditer(r'class="([^"]+)"', html):
                    used.update(c for c in m.group(1).split() if not c.startswith("shot"))
            unstyled = sorted(c for c in used if not _re.search(r"\." + _re.escape(c) + r"[ ,{:.>#\[]", CSS))
            blob = (h + pv + rv + playbook(wf, 0)).lower()
            leaked = [w for w in ("affordance", "fired pattern", "canon gap", "calibrated judgment",
                                  "spine.json", "evidence spine", "artifact model", "nugget") if w in blob]
            if leaked:
                print("   ✗ jargon leaked into owner-facing pages:", leaked)
                ok = False
            if unstyled:
                print("   ✗ classes used in markup with NO css rule:", unstyled)
                ok = False
            # spacing gate: every margin/padding/gap value sits on the 4-base scale.
            # (The 2026-07-06 audit found 53% of spacing off-scale — local hand-rolled
            # values are how rhythm inversions ship. This lint keeps the scale honest.)
            SCALE = {0, 1, 2, 4, 6, 8, 12, 16, 24, 32, 48}
            offscale = []
            for prop, val in _re.findall(r'\b(margin|padding|gap|row-gap|column-gap)\s*:\s*([^;}]+)', CSS):
                for v in _re.findall(r'-?\d+(?:\.\d+)?px', val):
                    if abs(float(v[:-2])) not in SCALE:
                        offscale.append(f"{prop}:{val.strip()}")
            if offscale:
                print("   ✗ off-scale spacing (allowed: 0/1/2/4/6/8/12/16/24/32/48):", offscale[:10])
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
        # ThreadingHTTPServer: a slow /run (subprocess + boot wait) must never block
        # other requests, or the pane appears dead. daemon_threads so shutdown is clean.
        srv = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
        srv.daemon_threads = True
        srv.allow_reuse_address = True
        print(f"GUILD HALL serving http://localhost:{a.port}  (registry: {REG})", flush=True)
        srv.serve_forever()
    ap.print_help()


if __name__ == "__main__":
    main()
