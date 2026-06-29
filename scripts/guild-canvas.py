#!/usr/bin/env python3
"""
guild-canvas.py — the standing Guild -> atrium dashboard (GUILD-33).

Designed via a Guild quest (charter -> divergence -> tournament): the winning
SYNTHESIS = Command Cockpit spine (Do) + self-auditing Design-System specimens
(See) + a contextual Run strip. The panel is a PROJECTION of docs/guild/ + the
agent menus (no state of its own); re-runnable as a workspace-command (--watch).

Modes:  (default) print HTML | --render create/update the note | --watch live
Interactivity: postMessage {type:'send'} -> instruction to a Guild agent pane;
{type:'atrium',uri:'atrium://commands/...'} -> file.open / pane.create (limited verbs).
"""
import os, sys, glob, json, subprocess, html, re, tempfile, urllib.parse
import yaml

ROOT = os.getcwd()
GUILD = os.path.join(ROOT, "docs", "guild")
TASKS = os.path.join(ROOT, "src", "modules", "guild", "tasks")
PROJECT = os.path.basename(ROOT)
CLI = os.environ.get("ATRIUM_CLI_PATH", "atrium")
NOTE_ID_FILE = os.path.join(GUILD, ".canvas-note-id")
E = html.escape
INK, LINEN = "#211C17", "#FBF7F1"

def load(p):
    try: return yaml.safe_load(open(os.path.join(GUILD, p))) or {}
    except FileNotFoundError: return {}

# ---- contrast (the self-auditing badge) ----
def _lin(c):
    c /= 255; return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
def _L(hexs):
    h = hexs.lstrip("#"); r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return 0.2126*_lin(r)+0.7152*_lin(g)+0.0722*_lin(b)
def contrast(a, b):
    la, lb = _L(a), _L(b); hi, lo = max(la, lb), min(la, lb)
    return (hi+0.05)/(lo+0.05)
def best_aa(hexs):
    try: c = max(contrast(hexs, INK), contrast(hexs, LINEN))
    except Exception: return ("", False)
    return (f"{c:.1f}", c >= 4.5)

ICONS = {"ranger":"🔍","rogue":"🔀","mage":"🎨","warlock":"✍️","sage":"🛡️",
         "healer":"📦","tinker":"🔧","cartographer":"🗺️","guild-master":"🎯"}

def agent_dir():
    for d in (os.path.join(ROOT, "_bmad/guild/agents"),
              os.path.expanduser("~/.claude/guild/_bmad/guild/agents")):
        if os.path.isdir(d): return d
    return None

def parse_agents():
    base = agent_dir()
    if not base: return []
    out = []
    for p in sorted(glob.glob(os.path.join(base, "*.md"))):
        stem = os.path.basename(p)[:-3]
        try: t = open(p).read()
        except OSError: continue
        m = re.search(r'<agent\b[^>]*\bname="([^"]+)"', t)
        name = m.group(1) if m else stem.replace("-", " ").title()
        caps = []
        for it in re.finditer(r'<item\s+cmd="([^"]+)"(?:\s+target="([^"]*)")?[^>]*>(.*?)</item>', t, re.S):
            label = re.split(r'\s+—\s+', re.sub(r'^\[[^\]]*\]\s*', '', it.group(3)).strip())[0]
            if label.lower().startswith("help") or not label: continue
            tm = re.match(r'task\s+(\S+\.md)', it.group(2) or "")
            caps.append((label, tm.group(1) if tm else ""))
        out.append((ICONS.get(stem, "•"), name, caps))
    return out

def runs():
    out = []
    for rp in sorted(glob.glob(os.path.join(GUILD, "runs", "RUN-*.yaml"))):
        if os.path.basename(rp) == "RUN-schema.yaml": continue
        try: r = yaml.safe_load(open(rp)) or {}
        except Exception: continue
        out.append((r.get("run_id", os.path.basename(rp)), r.get("state", "?")))
    return out

def uri(verb, **params):
    q = urllib.parse.urlencode(params)
    return "atrium://commands/%s%s" % (verb, ("?"+q if q else ""))

CSS = """
:root{--bg:#1A1611;--surface:#221D17;--raised:#2B251E;--border:#3A332A;--text:#F4ECE1;
--muted:#B8A88F;--subtle:#8E7E69;--ember:#E06E45;--sage:#97AD80;--r:9px}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);
font:13px/1.5 ui-sans-serif,Inter,system-ui;padding:14px}
h1{font:600 17px/1.2 ui-serif,Georgia;margin:0;display:flex;gap:8px;align-items:center}
.sub{color:var(--muted);font-size:11px;margin:2px 0 10px}
.lbl{font:600 10px/1 ui-sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--sage);margin:14px 0 7px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:11px}
/* run strip */
.run{display:flex;align-items:center;gap:8px;background:var(--surface);border:1px solid var(--border);
border-left:3px solid var(--ember);border-radius:var(--r);padding:8px 11px;margin-bottom:10px;font-size:12px}
.run .st{margin-left:auto;color:var(--ember);font-weight:600}
.run button{background:var(--raised);border:1px solid var(--border);color:var(--text);border-radius:6px;padding:3px 9px;font-size:11px;cursor:pointer}
/* tabs */
.tabs{display:flex;gap:6px;border-bottom:1px solid var(--border);margin-bottom:4px}
.tab{padding:7px 14px;cursor:pointer;color:var(--muted);font-weight:600;font-size:12px;border-bottom:2px solid transparent}
.tab.on{color:var(--text);border-bottom-color:var(--ember)}
.panel{display:none}.panel.on{display:block}
/* cockpit */
.search{width:100%;background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
color:var(--text);padding:9px 12px;font-size:13px;margin:10px 0 4px}
.search:focus{outline:none;border-color:var(--ember)}
.cnt{color:var(--subtle);font-size:11px;margin-bottom:8px}
details.ag{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);margin-bottom:6px}
details.ag>summary{cursor:pointer;padding:8px 11px;font-weight:600;list-style:none;display:flex;gap:8px;align-items:center}
details.ag>summary::-webkit-details-marker{display:none}
details.ag .c{color:var(--subtle);font-weight:400;font-size:11px;margin-left:auto}
.caps{display:flex;gap:5px;flex-wrap:wrap;padding:0 11px 11px}
.cap{display:inline-flex;align-items:center;gap:5px;background:var(--bg);border:1px solid var(--border);
border-radius:6px;padding:3px 4px 3px 9px;font-size:11px;color:var(--muted)}
.cap .go{cursor:pointer}.cap:hover{border-color:var(--ember);color:var(--text)}
.cap .open{opacity:.5;cursor:pointer;padding:0 4px;border-left:1px solid var(--border)}
.cap .open:hover{opacity:1;color:var(--ember)}
.acts{display:flex;gap:7px;flex-wrap:wrap;margin:10px 0}
button.act{border-radius:7px;border:1px solid var(--border);background:var(--raised);color:var(--text);padding:7px 13px;font-size:12px;cursor:pointer}
button.act.pri{background:var(--ember);border-color:var(--ember);color:#1A1611;font-weight:600}
button.act:hover{border-color:var(--ember)}
/* specimens */
.sw{display:inline-flex;flex-direction:column;align-items:center;gap:3px;margin:0 8px 8px 0}
.sw i{width:42px;height:42px;border-radius:8px;border:1px solid rgba(255,255,255,.08);display:block}
.sw b{font-size:9px;color:var(--subtle);font-weight:400}
.aa{font-size:8px;padding:1px 4px;border-radius:4px}
.aa.ok{background:rgba(151,173,128,.18);color:var(--sage)}.aa.no{background:rgba(224,110,69,.18);color:var(--ember)}
.ramp{display:flex;height:16px;border-radius:6px;overflow:hidden;margin:3px 0}.ramp i{flex:1}
.rk{font-size:10px;color:var(--subtle)}
.trg{display:flex;gap:8px;padding:5px 0;border-bottom:1px solid var(--border)}.trg:last-child{border:0}
.trg b{color:var(--ember);font-variant-numeric:tabular-nums;min-width:26px}
.pill{background:var(--raised);border:1px solid var(--border);border-radius:999px;padding:2px 9px;font-size:11px;color:var(--muted);margin:0 4px 4px 0;display:inline-block}
.kv{display:flex;justify-content:space-between;padding:3px 0;color:var(--muted)}.kv b{color:var(--text);font-weight:500}
.empty{color:var(--subtle);font-style:italic}
"""

def build_html():
    ctx = load("context.yaml"); base = ctx.get("baseline") or {}
    ds = load("design-system.yaml"); arts = (load("artifacts.yaml").get("artifacts")) or []
    ags = parse_agents(); rns = runs()
    P = []
    P.append(f'<h1>🎯 Guild · {E(PROJECT)}</h1>')
    P.append(f'<div class="sub">{len(base.get("triggers") or [])} triggers · {len(base.get("laws") or [])} laws · '
             f'{sum(len(c) for _,_,c in ags)} commands · {len(ags)} agents</div>')

    # ---- contextual run strip ----
    for rid, st in rns:
        P.append(f'<div class="run"><span>🎯 {E(rid)}</span><span class="st">{E(st)}</span>'
                 f'<button data-i="Guild Master: continue RUN {E(rid)} with the documented default.">Continue</button>'
                 f'<button data-i="Guild Master: pause RUN {E(rid)}.">Pause</button></div>')

    # ---- tabs ----
    P.append('<div class="tabs"><div class="tab on" data-tab="do">Do</div><div class="tab" data-tab="see">See</div></div>')

    # ===== DO panel (command cockpit) =====
    do = ['<div class="panel on" id="do">']
    acts = [("Diverge","pri","run Mage divergence (divergence-engine.md) on the component I name next."),
            ("Run QA","","run Sage calibrated QA on this project."),
            ("+ Charter","","run the Raid Charter (raid-charter.md)."),
            ("Self-heal","","run the self-healing loop (self-healing-loop.md).")]
    do.append('<div class="acts">' + "".join(
        f'<button class="act {c}" data-i="Guild dashboard action: {E(i)}">{E(l)}</button>' for l,c,i in acts) + '</div>')
    do.append('<input class="search" id="q" placeholder="Search 118 commands…" autocomplete="off">')
    do.append(f'<div class="cnt" id="cnt">{sum(len(c) for _,_,c in ags)} commands · {len(ags)} agents</div>')
    for icon, name, caps in ags:
        chips = []
        for label, taskfile in caps:
            launch = E("Activate Guild's %s agent and run: %s" % (name, label))
            open_btn = ""
            if taskfile:
                u = E(uri("file.open", path=os.path.join(TASKS, taskfile)))
                open_btn = f'<span class="open" data-uri="{u}" title="Open task definition">↗</span>'
            chips.append(f'<span class="cap" data-cap="{E((name+" "+label).lower())}">'
                         f'<span class="go" data-i="{launch}">{E(label)}</span>{open_btn}</span>')
        do.append(f'<details class="ag"><summary>{E(icon)} {E(name)}<span class="c">{len(caps)}</span></summary>'
                  f'<div class="caps">{"".join(chips)}</div></details>')
    do.append('</div>')
    P.append("".join(do))

    # ===== SEE panel (self-auditing design system + baseline + artifacts) =====
    see = ['<div class="panel" id="see">']
    if ds:
        pal = ds.get("palette") or {}
        sws = []
        for k, v in pal.items():
            if not (isinstance(v, dict) and v.get("hex")): continue
            ratio, ok = best_aa(v["hex"])
            sws.append(f'<span class="sw"><i style="background:{E(v["hex"])}"></i><b>{E(k)}</b>'
                       f'<span class="aa {"ok" if ok else "no"}">{"AA " if ok else ""}{E(ratio)}</span></span>')
        ramps = "".join('<div class="rk">%s</div><div class="ramp">%s</div>'
                        % (E(rk), "".join('<i style="background:%s"></i>' % E(c) for c in rv))
                        for rk, rv in (ds.get("ramps") or {}).items())
        comps = ds.get("components") or {}
        ncomp = sum(len(x) for x in comps.values() if isinstance(x, list))
        see.append('<div class="lbl">Design System — self-audited</div>')
        see.append(f'<div class="card"><div>{"".join(sws)}</div>{ramps}'
                   f'<div style="color:var(--muted);font-size:11px;margin-top:8px">{ncomp} components · '
                   f'{len(ds.get("guidelines") or [])} guidelines · kits: {E(", ".join(ds.get("ui_kits") or []))}</div></div>')
        see.append('<div class="lbl">Components</div>')
        see.append('<div class="card">' + "".join(
            f'<span class="pill">{E(c)}</span>' for grp in comps.values() if isinstance(grp, list) for c in grp) + '</div>')
    trg = base.get("triggers") or []
    if trg:
        see.append('<div class="lbl">Product Baseline — rulebook</div>')
        see.append('<div class="card">' + "".join(
            f'<div class="trg"><b>{E(t.get("id",""))}</b><span>{E(t.get("title",""))}</span></div>' for t in trg)
            + "".join(f'<span class="pill">{E(p)}</span>' for p in (base.get("domain_packs") or [])) + '</div>')
    see.append('<div class="lbl">Artifacts</div>')
    if arts:
        see.append('<div class="card">' + "".join(
            f'<div class="kv"><span>{E(a.get("artifact_id",""))} · {E(a.get("type",""))}</span><b>{E(a.get("state",""))}</b></div>'
            for a in arts) + '</div>')
    else:
        see.append('<div class="card empty">No artifacts yet — runs will register them here.</div>')
    see.append('</div>')
    P.append("".join(see))

    script = """<script>
function g(t){parent.postMessage({type:'send',payload:{instruction:t},framing:t},'*')}
function a(u){parent.postMessage({type:'atrium',uri:u},'*')}
document.addEventListener('click',function(e){
 var t=e.target.closest('.tab'); if(t){document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('on',x===t));
  document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('on',p.id===t.dataset.tab));return;}
 var o=e.target.closest('[data-uri]'); if(o){a(o.getAttribute('data-uri'));return;}
 var b=e.target.closest('[data-i]'); if(b){g(b.getAttribute('data-i'));}
});
var q=document.getElementById('q');
if(q)q.addEventListener('input',function(){var v=this.value.toLowerCase().trim();var n=0;
 document.querySelectorAll('.cap').forEach(function(c){var m=!v||c.dataset.cap.indexOf(v)>=0;c.style.display=m?'':'none';if(m)n++;});
 document.querySelectorAll('details.ag').forEach(function(d){d.open=!!v;});
 document.getElementById('cnt').textContent=n+' match'+(n==1?'':'es');});
</script>"""
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(P)}{script}</body></html>'

def render(body):
    nid = open(NOTE_ID_FILE).read().strip() if os.path.exists(NOTE_ID_FILE) else None
    if nid:
        r = subprocess.run([CLI,"note","write",nid,"--content",body], text=True, capture_output=True)
        if r.returncode == 0: print(f"updated Guild dashboard {nid}"); return
        print(f"(recreating) {r.stderr.strip()[:90]}")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(body); tmp = f.name
    r = subprocess.run([CLI,"note","new","--type","html","--title",f"Guild · {PROJECT}",
                        "--source","agent","--open","--body",tmp,"--json"], text=True, capture_output=True)
    os.unlink(tmp)
    if r.returncode != 0: sys.exit(f"note new failed: {r.stderr.strip()}")
    try:
        d = json.loads(r.stdout); nid = d.get("meta",{}).get("id") or d.get("id")
    except Exception: nid = None
    if nid: open(NOTE_ID_FILE,"w").write(nid); print(f"created Guild dashboard {nid}")
    else: print("created (unparsed):", r.stdout[:140])

def watch_sig():
    latest = 0.0
    for dp,_,fs in os.walk(GUILD):
        for f in fs:
            if f != ".canvas-note-id":
                try: latest = max(latest, os.path.getmtime(os.path.join(dp,f)))
                except OSError: pass
    return latest

def main():
    if "--watch" in sys.argv:
        import time; last=None; print("Guild dashboard watching docs/guild/ — Ctrl-C to stop")
        while True:
            s = watch_sig()
            if s != last: render(build_html()); last = s
            time.sleep(2)
    body = build_html()
    if "--render" in sys.argv: render(body)
    else: sys.stdout.write(body)

if __name__ == "__main__":
    main()
