#!/usr/bin/env python3
"""
guild-widget.py — the GUILD widget RENDERER (card 026d669e).

A pure projection of widget-feed.py's feed JSON into the owner's converged
design (claude-final.html: GPT component styling + Claude logic/spacing +
Now/Journey/Library behind a CLEAR labeled horizontal tab bar — no icon spine).
The renderer owns ZERO data: same feed backs this atrium canvas note today and
the pane/GUILD-HALL embed later (docs/guild/decisions/widget-more-packet.md).

  python3 scripts/guild-widget.py --project <path>            # HTML to stdout
  python3 scripts/guild-widget.py --project <path> --render   # create/update the atrium note
  python3 scripts/guild-widget.py --project <path> --watch    # live re-render on change
  python3 scripts/guild-widget.py --selftest
"""
import os, sys, json, html, time, argparse, tempfile, subprocess, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
CLI = os.environ.get("ATRIUM_CLI_PATH", "atrium")
E = html.escape

def _feed_mod():
    spec = importlib.util.spec_from_file_location("wf", os.path.join(HERE, "widget-feed.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

CSS = """
:root{--bg:#100f0d;--pane:#14120f;--panel:#1f1b16;--panel2:#282119;--inset:#171512;
--line:#2c2820;--line-soft:#221e18;--ink:#f4ece2;--ink-dim:#aa9c8d;--ink-faint:#7c7063;
--ember:#ce5328;--ember-tx:#f3bca1;--ember-deep:#9e3f1e;--sage:#728b5b;--sage-tx:#b7c9a6;
--amber:#c9971f;--rose:#b23423;--denim:#3a6079;
--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}html,body{height:100%}
body{background:var(--pane);color:var(--ink);font-family:var(--sans);font-size:13px;line-height:1.5;
-webkit-font-smoothing:antialiased;display:grid;grid-template-rows:auto auto auto minmax(0,1fr) auto auto;height:100vh;overflow:hidden}
.phead{display:flex;align-items:center;gap:10px;padding:13px 15px 11px;border-bottom:1px solid var(--line-soft)}
.gm{width:26px;height:26px;border-radius:7px;background:linear-gradient(150deg,var(--ember),var(--ember-deep));display:grid;place-items:center;color:#1a0f08;font-weight:800;font-size:13px}
.phead .nm{font-weight:750;font-size:15px;letter-spacing:.2px}
.live{margin-left:auto;display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--sage-tx);font-family:var(--mono)}
.pulse{width:6px;height:6px;border-radius:50%;background:var(--sage);animation:pp 2.6s infinite}
@keyframes pp{0%{box-shadow:0 0 0 0 rgba(143,174,125,.45)}70%{box-shadow:0 0 0 5px rgba(143,174,125,0)}100%{box-shadow:0 0 0 0 rgba(143,174,125,0)}}
.jbar{display:flex;align-items:center;gap:8px;padding:9px 15px;border-bottom:1px solid var(--line-soft);background:#15170f}
.jbar .jt{font-size:11.5px;font-weight:600;color:var(--ink-dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.jdots{display:flex;align-items:center;gap:4px;margin-left:auto;flex:0 0 auto}
.jdot{width:8px;height:8px;border-radius:50%;background:var(--line);border:1px solid var(--line)}
.jdot.done{background:var(--sage);border-color:var(--sage-tx)}
.jdot.now{background:var(--ember);border-color:var(--ember-tx);box-shadow:0 0 0 3px rgba(239,138,77,.2)}
.jbar .pct{font-family:var(--mono);font-size:10px;color:var(--ember-tx);margin-left:4px}
.switch{position:absolute;opacity:0;pointer-events:none}
.tabs{display:flex;gap:2px;padding:8px 12px 0;border-bottom:1px solid var(--line-soft)}
.tabs label{flex:1;display:flex;align-items:center;justify-content:center;gap:7px;padding:9px 6px;border-radius:8px 8px 0 0;
font-size:12.5px;font-weight:650;color:var(--ink-faint);cursor:pointer;border-bottom:2px solid transparent;position:relative;top:1px}
.tabs label:hover{color:var(--ink-dim)}
.tabs label .bdg{font-family:var(--mono);font-size:9px;font-weight:700;background:var(--amber);color:#241c08;border-radius:10px;padding:0 5px;min-width:15px;text-align:center}
.bdg.n{background:var(--panel2);color:var(--ink-dim)}
.views{min-height:0;overflow-y:auto}
.views::-webkit-scrollbar{width:8px}.views::-webkit-scrollbar-thumb{background:#272b22;border-radius:4px}
.view{display:none;padding:13px;flex-direction:column;gap:12px}
#v-now:checked~.tabs label[for=v-now],#v-jrny:checked~.tabs label[for=v-jrny],#v-lib:checked~.tabs label[for=v-lib]{color:var(--ember-tx);border-bottom-color:var(--ember-tx)}
#v-now:checked~.views .view.now,#v-jrny:checked~.views .view.jrny,#v-lib:checked~.views .view.lib{display:flex}
.lbl{font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-faint);display:flex;align-items:center;gap:8px}
.lbl em{margin-left:auto;font-style:normal;color:var(--ember-tx);letter-spacing:.06em}
.health{display:flex;align-items:center;gap:12px;padding:8px 12px;border:1px solid var(--line-soft);border-radius:9px;background:var(--inset);font-family:var(--mono);font-size:10px;flex-wrap:wrap}
.health i{font-style:normal;color:var(--ink-faint);display:inline-flex;align-items:center;gap:5px}
.health i b{color:var(--sage-tx);font-weight:700}.health i.bad b{color:#e58c80}
.needs{background:linear-gradient(180deg,#251e12,#1c1810);border:1px solid #3d311d;border-radius:11px;padding:13px;overflow:hidden}
.nh{display:flex;align-items:center;gap:8px;font-weight:700;font-size:13px;color:#f3dca3}
.nh .b{margin-left:auto;background:var(--amber);color:#241c08;font-family:var(--mono);font-weight:700;font-size:10px;padding:1px 7px;border-radius:20px}
.nsub{font-size:11.5px;color:var(--ink-dim);margin-top:5px;line-height:1.45}
.nrow{display:grid;grid-template-columns:auto 1fr;gap:9px 10px;align-items:start;padding:11px;background:var(--inset);border:1px solid var(--line);border-radius:9px;margin-top:9px}
.ni{width:26px;height:26px;border-radius:7px;display:grid;place-items:center;font-size:13px;background:var(--panel2);color:var(--ink-dim);border:1px solid var(--line);font-family:var(--mono);font-size:10px;font-weight:700}
.nrow .t{min-width:0}.nrow .t b{font-size:12.5px;font-weight:650;line-height:1.35}.nrow .t span{display:block;font-size:11px;color:var(--ink-faint);margin-top:3px;line-height:1.4}
.nacts{grid-column:1/-1;display:flex;gap:6px;margin-top:1px}
.nb{flex:1;text-align:center;font-size:11px;font-weight:700;padding:7px 8px;border-radius:7px;border:none;cursor:pointer;background:var(--ember);color:#1d0f06}
.nb.g{background:transparent;color:var(--ink-dim);border:1px solid var(--line)}
.zone{border:1px solid var(--line-soft);border-radius:11px;background:var(--panel);overflow:hidden}
.zhead{display:flex;align-items:center;padding:11px 13px;position:relative;font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-dim)}
.zhead::after{content:"";position:absolute;left:13px;right:13px;bottom:0;height:1px;background:rgba(244,236,226,.16)}
.zhead em{margin-left:auto;font-style:normal;color:var(--ember-tx)}
.zbody{padding:10px;display:grid;gap:9px}
.run{padding:11px;border-radius:9px;background:var(--inset);border:1px solid var(--line-soft)}
.rtop{display:flex;align-items:flex-start;gap:9px}.rtop .ti{min-width:0;flex:1}
.rtop h3{font-size:13px;font-weight:700;display:flex;align-items:center;gap:8px}
.rdot{width:8px;height:8px;border-radius:50%;background:var(--sage)}
.rdot.on{background:var(--ember);box-shadow:0 0 7px 1px rgba(239,138,77,.5)}
.rtop p{font-size:11px;color:var(--ink-dim);margin-top:3px;line-height:1.45}
.rst{font-family:var(--mono);font-size:9.5px;font-weight:700;padding:2px 7px;border-radius:6px;background:var(--panel2);color:var(--ink-dim);white-space:nowrap}
.sug{display:grid;grid-template-columns:auto 1fr;gap:12px;align-items:center;padding:12px;border-radius:10px;background:var(--inset);border:1px solid var(--line-soft)}
.rk{width:24px;height:24px;border-radius:7px;background:var(--panel2);border:1px solid var(--line);color:var(--ink-dim);font-family:var(--mono);font-weight:700;font-size:11px;display:grid;place-items:center;align-self:flex-start}
.sug .st{min-width:0}.sug .st b{font-size:13px;font-weight:700;line-height:1.35;color:var(--ink)}
.sug .st .cite{display:block;font-size:11px;color:var(--ink-faint);margin-top:5px;line-height:1.45}
.sug .cite code{font-family:var(--mono);color:var(--ink-dim)}
.phase{display:grid;grid-template-columns:auto 1fr auto;gap:11px;align-items:center;padding:11px;border-radius:9px;background:var(--inset);border:1px solid var(--line-soft)}
.pnode{width:20px;height:20px;border-radius:50%;border:2px solid var(--line);display:grid;place-items:center;font-size:10px;color:var(--ink-faint);flex:0 0 auto}
.phase.done .pnode{background:var(--sage);border-color:var(--sage-tx);color:#10160c}
.phase.now .pnode{background:var(--ember);border-color:var(--ember-tx);color:#1a0f08;box-shadow:0 0 0 4px rgba(239,138,77,.18)}
.phase .pt{min-width:0}.phase .pt b{font-size:13px;font-weight:650}.phase .pt span{display:block;font-size:10.5px;color:var(--ink-faint);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.conf{font-family:var(--mono);font-size:9.5px;font-weight:700;padding:2px 7px;border-radius:6px}
.conf.hi{background:rgba(143,174,125,.16);color:var(--sage-tx)}.conf.lo{background:var(--panel2);color:var(--ink-faint)}
.brief{padding:12px;border-radius:10px;background:var(--panel);border:1px solid var(--line-soft)}
.brief p{font-size:12px;color:var(--ink-dim);margin-top:7px;line-height:1.5}.brief p b{color:var(--ink)}
.ltool{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.chip{font-family:var(--mono);font-size:10px;color:var(--ink-dim);background:var(--inset);border:1px solid var(--line-soft);border-radius:20px;padding:4px 10px}
.chip.on{background:#1c160f;border-color:rgba(239,138,77,.35);color:var(--ember-tx)}
.acard{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:10px;border-radius:11px;background:var(--panel);border:1px solid var(--line-soft)}
.thumb{width:40px;height:36px;border-radius:7px;border:1px solid var(--line);background:#0e100c;display:grid;place-items:center;font-family:var(--mono);font-size:9px;color:var(--ink-faint)}
.am{min-width:0}
.am .an{font-size:13px;font-weight:650;display:flex;align-items:center;gap:7px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.badge{font-family:var(--mono);font-size:8.5px;font-weight:700;padding:2px 6px;border-radius:5px;letter-spacing:.03em;flex:0 0 auto;background:var(--panel2);color:var(--ink-faint)}
.badge.ia{background:rgba(143,174,125,.16);color:var(--sage-tx)}.badge.packet{background:rgba(239,138,77,.16);color:var(--ember-tx)}
.am .meta{font-size:11px;color:var(--ink-dim);margin-top:4px;font-family:var(--mono);font-size:10px}
.obtn{font-size:10.5px;font-weight:700;color:var(--ink-dim);border:1px solid var(--line);border-radius:7px;padding:5px 10px;cursor:pointer;white-space:nowrap;background:transparent}
.obtn:hover{color:var(--ember-tx);border-color:rgba(239,138,77,.32)}
.lsec{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-faint);display:flex;align-items:center;gap:8px;margin-top:2px}
.lsec:after{content:"";flex:1;height:1px;background:var(--line-soft)}
.task{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;padding:10px 11px;border-radius:9px;background:var(--inset);border:1px solid var(--line-soft)}
.task .tt b{font-size:12.5px}
.task .col{font-family:var(--mono);font-size:9px;color:var(--ink-dim);border:1px solid var(--line);border-radius:6px;padding:3px 7px;white-space:nowrap}
.quick{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:9px 13px;border-top:1px solid var(--line-soft);background:#101210}
.quick button{display:flex;flex-direction:column;align-items:center;gap:4px;padding:7px 2px;border-radius:8px;background:var(--panel);border:1px solid var(--line-soft);color:var(--ink-dim);font-size:10px;font-weight:600;cursor:pointer}
.quick button:hover{border-color:var(--line);color:var(--ink)}.quick button .qi{font-size:14px}
.quick button.pri{border-color:rgba(206,83,40,.4);color:var(--ember-tx)}
.tray{display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:center;padding:11px 15px;border-top:1px solid var(--line-soft);background:#101210}
.av{width:28px;height:28px;border-radius:8px;background:linear-gradient(140deg,var(--sage),#5f7a4f);display:grid;place-items:center;color:#10160c;font-weight:700;font-size:10px}
.tray .pp b{font-size:12.5px}.tray .pp span{display:block;font-size:10px;color:var(--ink-faint);margin-top:1px;font-family:var(--mono)}
@media(prefers-reduced-motion:reduce){.pulse{animation:none}}
"""

JS = """<script>
function a(u){parent.postMessage({type:'atrium',uri:u},'*')}
function fo(p){a('atrium://commands/file.open?path='+encodeURIComponent(p))}
function g(t){parent.postMessage({type:'send',payload:{instruction:t},framing:t},'*')}
</script>"""


def _jdots(phases):
    dots = []
    for p in phases[:9]:
        cls = "done" if p["status"] == "done" else ("now" if p["status"] in ("now", "in-progress", "active") else "")
        dots.append(f'<span class="jdot {cls}"></span>')
    return "".join(dots)


def build_html(feed):
    f = feed
    j = f.get("journey") or {"title": "No journey yet", "phases": [], "stop_point": ""}
    done = sum(1 for p in j["phases"] if p["status"] == "done")
    pct = int(100 * done / len(j["phases"])) if j["phases"] else 0
    cur = next((p["name"] for p in j["phases"] if p["status"] not in ("done",)), "complete")
    needs, lib, sugs, runs = f["needs_you"], f["library"], f["suggestions"], f["runs"]

    health = "".join(
        f'<i class="{"bad" if g["exit"] else ""}"><b>{"✓" if g["exit"]==0 else "✗"}</b> {E(g["gate"])}</i>'
        for g in f["gates"][:6]) or '<i><b>—</b> no gate evidence yet</i>'
    health += (f'<i><b>{f["spine_nuggets"]}</b> nuggets</i><i><b>{len(runs)}</b> runs</i>'
               f'<i><b>{f.get("patterns", 0)}</b> patterns</i>')

    nrows = "".join(
        f'<div class="nrow"><div class="ni">{E(n["id"])}</div>'
        f'<div class="t"><b>{E(n["title"])}</b><span>{E(n["detail"])}</span></div>'
        f'<div class="nacts"><button class="nb" onclick="fo(\'{E(n["link"] or "")}\')">Open</button>'
        f'<button class="nb g" onclick="g(\'Owner decision on {E(n["id"])} — {E(n["title"][:60])}\')">Discuss</button></div></div>'
        for n in needs) or '<div class="nsub">Nothing needs you — the loop is clean.</div>'

    runrows = "".join(
        f'<div class="run"><div class="rtop"><div class="ti">'
        f'<h3><span class="rdot {"on" if r["state"] not in ("completed","done","ready-for-review") else ""}"></span>{E(r["id"])}</h3>'
        f'<p>{E(r["objective"][:110])}</p></div><span class="rst">{E(r["state"])}</span></div></div>'
        for r in runs[:3]) or '<div class="nsub" style="padding:4px 2px">No runs recorded yet.</div>'

    sugrows = "".join(
        f'<div class="sug"><div class="rk">{i+1}</div><div class="st"><b>{E(s["title"])}</b>'
        f'<span class="cite">Cites <code>{E(s["cite"])}</code></span></div></div>'
        for i, s in enumerate(sugs)) or '<div class="nsub" style="padding:4px 2px">No suggestions.</div>'

    phaserows = "".join(
        f'<div class="phase {"done" if p["status"]=="done" else ("now" if p["status"] in ("now","in-progress","active") else "")}">'
        f'<div class="pnode">{"✓" if p["status"]=="done" else i+1}</div>'
        f'<div class="pt"><b>{E(p["name"])}</b><span>{E(p["note"] or p["status"])}</span></div>'
        f'<span class="conf {"hi" if p["status"]=="done" else "lo"}">{E(p["status"])}</span></div>'
        for i, p in enumerate(j["phases"]))

    kinds = sorted({i["kind"] for i in lib})
    chips = '<span class="chip on">All</span>' + "".join(f'<span class="chip">{E(k)}</span>' for k in kinds)
    acards = "".join(
        f'<div class="acard"><div class="thumb">{E(i["kind"][:4])}</div>'
        f'<div class="am"><div class="an">{E(i["name"])} <span class="badge {E(i["kind"]) if i["kind"] in ("ia","packet") else ""}">{E(i["kind"])}</span></div>'
        f'<div class="meta">{time.strftime("%b %d %H:%M", time.localtime(i["mtime"]))}</div></div>'
        f'<button class="obtn" onclick="fo(\'{E(i["path"])}\')">open ↗</button></div>'
        for i in lib)

    taskrows = "".join(
        f'<div class="task"><div class="tt"><b>{E(c["title"])}</b></div><span class="col">{E(c["status"])}</span></div>'
        for c in f["cards"]) or ""
    tasksec = f'<div class="lsec">Cards · on the board</div>{taskrows}' if taskrows else ""

    brief = f'<div class="brief"><div class="lbl">Where this stops <em>{E(j.get("source",""))}</em></div><p>{E(j["stop_point"] or "No stop-point recorded.")}</p></div>'

    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<header class="phead"><div class="gm">G</div><div class="nm">GUILD · {E(f["project"])}</div>
<span class="live"><span class="pulse"></span>live · {E(f["mode"])} feed</span></header>
<div class="jbar"><span class="jt">{E(j["title"][:60])} · {E(cur[:36])}</span>
<span class="jdots">{_jdots(j["phases"])}</span><span class="pct">{pct}%</span></div>
<input type="radio" name="view" id="v-now" class="switch" checked>
<input type="radio" name="view" id="v-jrny" class="switch">
<input type="radio" name="view" id="v-lib" class="switch">
<div class="tabs">
<label for="v-now">Now <span class="bdg">{len(needs)}</span></label>
<label for="v-jrny">Journey</label>
<label for="v-lib">Library <span class="bdg n">{len(lib)}</span></label>
</div>
<div class="views">
<section class="view now">
<div class="health">{health}</div>
<div class="needs"><div class="nh">Needs you <span class="b">{len(needs)}</span></div>
<div class="nsub">Decisions waiting on the owner — everything else keeps moving.</div>{nrows}</div>
<div class="zone"><div class="zhead">Runs <em>{len(runs)} recorded</em></div><div class="zbody">{runrows}</div></div>
<div class="zone"><div class="zhead">Suggestions <em>ranked · cited</em></div><div class="zbody">{sugrows}</div></div>
</section>
<section class="view jrny">
<div class="lbl">Pipeline <em>{done} of {len(j["phases"])} done</em></div>
{phaserows}{brief}
</section>
<section class="view lib">
<div class="ltool"><span class="lbl" style="margin-right:auto">Artifacts · {len(lib)}</span>{chips}</div>
{acards}{tasksec}
</section>
</div>
<nav class="quick">
<button class="pri" onclick="g('/guild-quest')"><span class="qi">✦</span>Quest</button>
<button onclick="g('/guild-diverge')"><span class="qi">⑂</span>Diverge</button>
<button onclick="g('/guild-pre-handoff')"><span class="qi">✓</span>QA</button>
<button onclick="g('/guild-self-heal')"><span class="qi">⟲</span>Heal</button>
</nav>
<div class="tray"><div class="av">OP</div><div class="pp"><b>Operator</b><span>{E(f["root"])}</span></div></div>
{JS}</body></html>"""



def build_pointer(feed):
    """The atrium note is now a THIN POINTER to the HALL (one surface, not two)."""
    n = len(feed["needs_you"])
    line = f'{n} decision{"s" if n != 1 else ""} waiting for you' if n else "nothing needs you — agents keep working"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{background:#100f0d;color:#f4ece2;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,sans-serif;
display:grid;place-items:center;height:100vh;margin:0;text-align:center}}
.g{{width:34px;height:34px;border-radius:9px;background:linear-gradient(150deg,#ce5328,#9e3f1e);display:grid;
place-items:center;color:#1a0f08;font-weight:800;margin:0 auto 10px}}
h1{{font-size:15px;margin-bottom:4px}} p{{font-size:12.5px;color:#aa9c8d;line-height:1.6}}
.n{{display:inline-block;margin:12px 0 4px;font-size:13px;font-weight:700;color:#f3dca3;background:#251e12;
border:1px solid #3d311d;border-radius:9px;padding:8px 16px}}
code{{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:#b7c9a6}}</style></head><body><div>
<div class="g">G</div><h1>GUILD lives in the Hall now</h1>
<p>Your delegated-work inbox — every project, one surface.</p>
<div class="n">{line}</div>
<p>Open <code>http://localhost:4400</code><br>(start it: <code>python3 scripts/guild-hall.py --serve</code>)</p>
</div></body></html>"""


def note_id_file(feed):
    base = os.path.join(feed["root"], "_bmad-output", "guild-artifacts")
    if not os.path.isdir(base): base = os.path.join(feed["root"], "docs", "guild")
    return os.path.join(base, ".widget-note-id")


def render(feed, body):
    nf = note_id_file(feed)
    nid = open(nf).read().strip() if os.path.exists(nf) else None
    if nid:
        r = subprocess.run([CLI, "note", "write", nid, "--content", body], text=True, capture_output=True)
        if r.returncode == 0: print(f"updated GUILD widget note {nid}"); return nid
        print(f"(recreating) {r.stderr.strip()[:90]}")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(body); tmp = f.name
    r = subprocess.run([CLI, "note", "new", "--type", "html", "--title", f"GUILD · {feed['project']}",
                        "--source", "agent", "--body", tmp, "--json"], text=True, capture_output=True)
    os.unlink(tmp)
    if r.returncode != 0: sys.exit(f"note new failed: {r.stderr.strip()}")
    try:
        d = json.loads(r.stdout); nid = d.get("meta", {}).get("id") or d.get("id")
    except Exception: nid = None
    if nid: open(nf, "w").write(nid); print(f"created GUILD widget note {nid}")
    else: print("created (unparsed):", r.stdout[:140])
    return nid


def selftest():
    wf = _feed_mod()
    feed = {"project": "t", "root": "/tmp/t", "mode": "project", "spine_nuggets": 3, "cards": [],
            "journey": {"title": "Q", "phases": [{"name": "a", "status": "done", "note": ""},
                                                  {"name": "b", "status": "now", "note": "x"}], "stop_point": "s", "source": "q.yaml"},
            "runs": [{"id": "RUN-1", "state": "done", "objective": "o", "checkpoints": 2, "open_exceptions": [], "path": "/tmp/r"}],
            "gates": [{"gate": "responsive-gate", "exit": 0}, {"gate": "fidelity-gate", "exit": 1}],
            "needs_you": [{"id": "D1", "title": "Approve", "detail": "d", "link": "/tmp/p.md"}],
            "packet": "/tmp/p.md",
            "suggestions": [{"title": "S", "cite": "c"}],
            "library": [{"name": "spine.json", "kind": "IA", "path": "/tmp/s", "mtime": 1750000000}]}
    h = build_html(feed)
    ok = all(x in h for x in ('id="v-now"', 'id="v-jrny"', 'id="v-lib"', "Needs you", "RUN-1",
                              "fidelity-gate", "Approve", "spine.json", 'class="tabs"'))
    ok = ok and "icon-spine" not in h and hasattr(wf, "build")
    print("guild-widget self-test:", "✅ PASS" if ok else "❌ FAIL")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=os.getcwd())
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    wf = _feed_mod()
    if a.watch:
        print(f"GUILD widget watching {a.project} — Ctrl-C to stop")
        last = None
        while True:
            feed = wf.build(a.project)
            sig = json.dumps(feed, sort_keys=True, default=str)
            if sig != last: render(feed, build_pointer(feed)); last = sig
            time.sleep(3)
    feed = wf.build(a.project)
    if a.render: render(feed, build_pointer(feed))
    else: sys.stdout.write(build_html(feed))


if __name__ == "__main__":
    main()
