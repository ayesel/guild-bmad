#!/usr/bin/env python3
"""
guild-canvas.py — the standing Guild -> atrium dashboard renderer (GUILD-33 Phase 1).

Maps the repo-owned docs/guild/ registry into a DESIGNED, content-rich atrium
HTML note (the dashboard is a PROJECTION of the files — no state of its own).
Re-runnable; wire as a workspace-command (--watch) to keep it live.

Reads (relative to cwd; works in any Guild project, sections render only if present):
  context.yaml          baseline (laws / triggers / domain packs) + taste
  design-system.yaml    real palette swatches + components + guidelines (GUILD-27 snapshot)
  trust.yaml            autonomy tiers
  definition-of-done.yaml  hard stops
  qa-tiers.yaml         calibrated QA tiers
  artifacts.yaml        artifact rows
  runs/RUN-*.yaml       live run rows

Modes:  (default) print HTML | --render create/update the note | --watch keep live
HTML buttons fire send_to_agent via postMessage (a Guild agent pane runs the CLI).
"""
import os, sys, glob, json, subprocess, html
import yaml

ROOT = os.getcwd()
GUILD = os.path.join(ROOT, "docs", "guild")
PROJECT = os.path.basename(ROOT)
CLI = os.environ.get("ATRIUM_CLI_PATH", "atrium")
NOTE_ID_FILE = os.path.join(GUILD, ".canvas-note-id")
E = html.escape

def load(path):
    try:
        return yaml.safe_load(open(os.path.join(GUILD, path))) or {}
    except FileNotFoundError:
        return {}

ICONS = {"ranger": "🔍", "rogue": "🔀", "mage": "🎨", "warlock": "✍️", "sage": "🛡️",
         "healer": "📦", "tinker": "🔧", "cartographer": "🗺️", "guild-master": "🎯"}

def agent_dirs():
    return [os.path.join(ROOT, "_bmad/guild/agents"),
            os.path.expanduser("~/.claude/guild/_bmad/guild/agents")]

def parse_agents():
    """Live capability catalog: each agent + its menu items, from the compiled .md."""
    import re
    base = next((d for d in agent_dirs() if os.path.isdir(d)), None)
    if not base:
        return []
    out = []
    for p in sorted(glob.glob(os.path.join(base, "*.md"))):
        stem = os.path.basename(p)[:-3]
        try:
            t = open(p).read()
        except OSError:
            continue
        m = re.search(r'<agent\b[^>]*\bname="([^"]+)"', t)
        name = m.group(1) if m else stem.replace("-", " ").title()
        caps = []
        for it in re.finditer(r'<item\s+cmd="([^"]+)"[^>]*>(.*?)</item>', t, re.S):
            label = re.sub(r'^\[[^\]]*\]\s*', '', it.group(2)).strip()
            label = re.split(r'\s+—\s+', label)[0]  # short label, drop the description
            if label.lower().startswith("help"):
                continue
            caps.append(label)
        out.append((ICONS.get(stem, "•"), name, stem, caps))
    return out

def runs():
    out = []
    for rp in sorted(glob.glob(os.path.join(GUILD, "runs", "RUN-*.yaml"))):
        if os.path.basename(rp) == "RUN-schema.yaml":
            continue
        try:
            r = yaml.safe_load(open(rp)) or {}
        except Exception:
            continue
        out.append((r.get("run_id", os.path.basename(rp)), r.get("state", "?")))
    return out

CSS = """
:root{--bg:#1A1611;--surface:#221D17;--raised:#2B251E;--border:#3A332A;
--text:#F4ECE1;--muted:#B8A88F;--subtle:#8E7E69;--ember:#E06E45;--sage:#97AD80;--radius:10px}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);
font:13px/1.5 ui-sans-serif,Inter,system-ui;padding:16px}
h1{font:600 18px/1.2 ui-serif,Georgia;margin:0 0 2px;display:flex;gap:8px;align-items:center}
.sub{color:var(--muted);font-size:12px;margin-bottom:14px}
.sec{margin:16px 0 0}.sec>.lbl{font:600 10px/1 ui-sans-serif;letter-spacing:.12em;
text-transform:uppercase;color:var(--sage);margin-bottom:8px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:12px}
.swatches{display:flex;gap:6px;flex-wrap:wrap}
.sw{width:38px;height:38px;border-radius:8px;border:1px solid rgba(255,255,255,.08);position:relative}
.sw span{position:absolute;bottom:-15px;left:0;right:0;text-align:center;font-size:8px;color:var(--subtle)}
.ramp{display:flex;border-radius:6px;overflow:hidden;height:14px;margin:4px 0 2px}.ramp i{flex:1}
.pills{display:flex;gap:5px;flex-wrap:wrap}
.pill{background:var(--raised);border:1px solid var(--border);border-radius:999px;padding:2px 9px;font-size:11px;color:var(--muted)}
.trg{display:flex;gap:8px;padding:5px 0;border-bottom:1px solid var(--border)}
.trg:last-child{border:0}.trg b{color:var(--ember);font-variant-numeric:tabular-nums;min-width:26px}
.kv{display:flex;justify-content:space-between;padding:3px 0;color:var(--muted)}.kv b{color:var(--text);font-weight:500}
.empty{color:var(--subtle);font-style:italic}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.acts{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}
button.act{border-radius:8px;border:1px solid var(--border);background:var(--raised);
color:var(--text);padding:8px 14px;font-size:12px;cursor:pointer}
button.act.pri{background:var(--ember);border-color:var(--ember);color:#1A1611;font-weight:600}
button.act:hover{border-color:var(--ember)}
details.ag{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:6px}
details.ag>summary{cursor:pointer;padding:9px 12px;font-weight:600;list-style:none;display:flex;align-items:center;gap:8px}
details.ag>summary::-webkit-details-marker{display:none}
details.ag .cnt{color:var(--subtle);font-weight:400;font-size:11px;margin-left:auto}
.caps{display:flex;gap:5px;flex-wrap:wrap;padding:0 12px 12px}
.cap{background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:4px 9px;font-size:11px;color:var(--muted);cursor:pointer}
.cap:hover{border-color:var(--ember);color:var(--text)}
"""

def section(lbl, inner):
    return f'<div class="sec"><div class="lbl">{E(lbl)}</div>{inner}</div>'

def build_html():
    ctx = load("context.yaml"); base = ctx.get("baseline") or {}
    ds = load("design-system.yaml"); trust = load("trust.yaml")
    dod = load("definition-of-done.yaml"); qa = load("qa-tiers.yaml")
    arts = (load("artifacts.yaml").get("artifacts")) or []
    rns = runs()
    P = []

    P.append(f'<h1><span>🎯</span> Guild · {E(PROJECT)}</h1>')
    taste = "  ·  taste ✓" if "taste_anchors" in ctx else ""
    P.append(f'<div class="sub">{len(base.get("triggers") or [])} triggers · {len(base.get("laws") or [])} laws · {len(base.get("domain_packs") or [])} domain packs{taste}</div>')

    # ---- Design System (real swatches) ----
    if ds:
        pal = ds.get("palette") or {}
        sw = "".join(f'<div class="sw" style="background:{E(v["hex"])}"><span>{E(k)}</span></div>'
                     for k, v in pal.items() if isinstance(v, dict) and v.get("hex"))
        def ramp_html(rk, rv):
            bars = "".join('<i style="background:%s"></i>' % E(c) for c in rv)
            return ('<div style="font-size:10px;color:var(--subtle)">%s</div>'
                    '<div class="ramp">%s</div>') % (E(rk), bars)
        ramps = "".join(ramp_html(rk, rv) for rk, rv in (ds.get("ramps") or {}).items())
        comps = ds.get("components") or {}
        ncomp = sum(len(v) for v in comps.values() if isinstance(v, list))
        kits = ds.get("ui_kits") or []
        inner = (f'<div class="card"><div class="swatches" style="margin-bottom:22px">{sw}</div>{ramps}'
                 f'<div style="margin-top:10px;color:var(--muted);font-size:11px">{ncomp} components · '
                 f'{len(ds.get("guidelines") or [])} guidelines · kits: {E(", ".join(kits))}</div></div>')
        P.append(section(f'Design System — {E(ds.get("source",{}).get("name","") )}', inner))

    # ---- Agents & Capabilities (what Guild can DO) ----
    ags = parse_agents()
    if ags:
        blocks = []
        for icon, name, stem, caps in ags:
            cbtns = "".join(
                '<span class="cap" data-i="%s">%s</span>'
                % (E("Activate Guild's %s agent and run: %s" % (name, c)), E(c))
                for c in caps)
            blocks.append('<details class="ag"><summary>%s %s<span class="cnt">%d</span></summary>'
                          '<div class="caps">%s</div></details>' % (E(icon), E(name), len(caps), cbtns))
        total = sum(len(c) for _, _, _, c in ags)
        P.append(section("Agents & Capabilities — %d agents · %d commands" % (len(ags), total), "".join(blocks)))

    # ---- Product Baseline (browsable triggers) ----
    trg = base.get("triggers") or []
    if trg:
        rows = "".join(f'<div class="trg"><b>{E(t.get("id",""))}</b><span>{E(t.get("title",""))}</span></div>' for t in trg)
        packs = "".join(f'<span class="pill">{E(p)}</span>' for p in (base.get("domain_packs") or []))
        P.append(section("Product Baseline", f'<div class="card">{rows}'
                 + (f'<div class="pills" style="margin-top:8px">{packs}</div>' if packs else "") + '</div>'))

    # ---- Governance / Autonomy ----
    gov = []
    if trust.get("tiers"):
        gov.append('<div class="card"><div style="color:var(--sage);font-size:10px;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">Trust tiers</div>'
                   + "".join(f'<div class="kv"><span>{E(t)}</span><b>{E(", ".join((d or {}).get("may",[])))}</b></div>' for t, d in trust["tiers"].items()) + '</div>')
    if dod.get("hard_stops"):
        hs = dod["hard_stops"]
        gov.append('<div class="card"><div style="color:var(--sage);font-size:10px;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">Hard stops</div>'
                   + f'<div class="kv"><span>max iterations</span><b>{E(str(hs.get("max_iterations","-")))}</b></div>'
                   + f'<div class="kv"><span>no-progress passes</span><b>{E(str(hs.get("no_progress_passes","-")))}</b></div>'
                   + f'<div class="kv"><span>budget</span><b>{"set" if (hs.get("budget") or {}).get("tokens") else "inherit"}</b></div></div>')
    if gov:
        P.append(section("Autonomy / Governance", f'<div class="grid2">{"".join(gov)}</div>'))

    # ---- Runs / Artifacts ----
    if rns:
        rows = "".join(f'<div class="kv"><span>{E(i)}</span><b>{E(s)}</b></div>' for i, s in rns)
        P.append(section(f"Runs ({len(rns)})", f'<div class="card">{rows}</div>'))
    else:
        P.append(section("Runs", '<div class="card empty">No active runs.</div>'))
    if arts:
        rows = "".join(f'<div class="kv"><span>{E(a.get("artifact_id",""))} · {E(a.get("type",""))}</span><b>{E(a.get("state",""))}</b></div>' for a in arts)
        P.append(section(f"Artifacts ({len(arts)})", f'<div class="card">{rows}</div>'))
    else:
        P.append(section("Artifacts", '<div class="card empty">No artifacts registered — runs will populate this.</div>'))

    # ---- Actions ----
    acts = [("+ Charter", "", "run the Raid Charter (raid-charter.md)."),
            ("Diverge", "pri", "run Mage divergence (divergence-engine.md) on the component I name next."),
            ("Run QA", "", "run Sage calibrated QA on this project."),
            ("Self-heal", "", "run the self-healing loop (self-healing-loop.md)."),
            ("Seed Claude Design", "", "run the Claude Design seed (claude-design-seed.md).")]
    btns = "".join(f'<button class="act {c}" data-i="{E("Guild dashboard action: "+i)}">{E(l)}</button>' for l, c, i in acts)
    P.append(section("Do", f'<div class="acts">{btns}</div>'))

    script = ("<script>function g(t){parent.postMessage({type:'send',payload:{instruction:t},framing:t},'*')}"
              "document.addEventListener('click',function(e){var b=e.target.closest('[data-i]');if(b)g(b.getAttribute('data-i'))});</script>")
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(P)}{script}</body></html>'

def render(body):
    nid = open(NOTE_ID_FILE).read().strip() if os.path.exists(NOTE_ID_FILE) else None
    if nid:
        r = subprocess.run([CLI, "note", "write", nid, "--content", body], text=True, capture_output=True)
        if r.returncode == 0:
            print(f"updated Guild dashboard note {nid}"); return
        print(f"(recreating) {r.stderr.strip()[:100]}")
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(body); tmp = f.name
    r = subprocess.run([CLI, "note", "new", "--type", "html", "--title", f"Guild · {PROJECT}",
                        "--source", "agent", "--open", "--body", tmp, "--json"], text=True, capture_output=True)
    os.unlink(tmp)
    if r.returncode != 0:
        sys.exit(f"note new failed: {r.stderr.strip()}")
    try:
        d = json.loads(r.stdout); nid = d.get("meta", {}).get("id") or d.get("id")
    except Exception:
        nid = None
    if nid:
        open(NOTE_ID_FILE, "w").write(nid); print(f"created Guild dashboard note {nid}")
    else:
        print("created (unparsed id):", r.stdout[:160])

def watch_sig():
    latest = 0.0
    for dp, _, fs in os.walk(GUILD):
        for f in fs:
            if f != ".canvas-note-id":
                try: latest = max(latest, os.path.getmtime(os.path.join(dp, f)))
                except OSError: pass
    return latest

def main():
    if "--watch" in sys.argv:
        import time
        last = None; print("Guild dashboard watching docs/guild/ — Ctrl-C to stop")
        while True:
            s = watch_sig()
            if s != last: render(build_html()); last = s
            time.sleep(2)
    body = build_html()
    if "--render" in sys.argv: render(body)
    else: sys.stdout.write(body)

if __name__ == "__main__":
    main()
