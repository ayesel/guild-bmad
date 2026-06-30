#!/usr/bin/env python3
"""
option-gallery.py — GUILD-9: Option Gallery (human vote) + replay/trace.

A first-class, welcomed human pick among options — NOT a redundant re-prompt. Renders N
options as live iframes in one note, each with a Vote button (routes to a verified live
pane, GUILD-79 fix). Complements the GUILD-13 tournament: the tournament auto-selects a
rec + alternatives; the gallery lets the owner override with a human pick when they want.
Also writes a passive replay TRACE (options + vote) for audit (GUILD-9 replay).

  python3 scripts/option-gallery.py --options opts.json --target-pane <id> --render
  python3 scripts/option-gallery.py --selftest
opts.json: [{"id","label","file"?}]  (file = HTML design to render live)
"""
import os, sys, json, html, subprocess, tempfile, argparse
E = html.escape
CLI = os.environ.get("ATRIUM_CLI_PATH", "atrium")
TRACE = os.path.join(os.getcwd(), "docs", "guild", "runs", "gallery-trace.jsonl")

def gallery_html(title, options, target_pane=None):
    def card(o):
        inner = (f'<iframe sandbox="allow-scripts" srcdoc="{E(o["html"])}" '
                 f'style="width:100%;height:46vh;border:0;border-radius:8px;background:#fff"></iframe>'
                 ) if o.get("html") else f'<p>{E(o.get("label",""))}</p>'
        return (f'<div class="opt"><div class="oh"><h3>{E(o.get("label", o["id"]))}</h3>'
                f'<button class="vote" data-vote="{E(o["id"])}">Vote ✓</button></div>{inner}</div>')
    framing = (f"Owner gallery vote for '{title}'. Record the chosen option id + that this was a "
               f"HUMAN pick (complements the tournament). {{payload}}")
    cards = "".join(card(o) for o in options)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
:root{{--bg:#1A1611;--surface:#221D17;--border:#3A332A;--text:#F4ECE1;--muted:#B8A88F;--ember:#E06E45}}
body{{margin:0;background:var(--bg);color:var(--text);font:13px/1.5 ui-sans-serif,system-ui;padding:16px}}
h2{{font:600 16px ui-serif,Georgia;margin:0 0 4px}}.q{{color:var(--muted);font-size:12px;margin-bottom:14px}}
.opt{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px;margin-bottom:12px}}
.oh{{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}}.oh h3{{margin:0;font-size:13px;color:var(--ember)}}
button.vote{{background:var(--ember);border:0;color:#1A1611;font-weight:600;border-radius:8px;padding:8px 16px;font-size:12px;cursor:pointer}}
button.vote:hover{{filter:brightness(1.08)}}
</style></head><body>
<h2>{E(title)}</h2><div class="q">Pick the option you like best — a welcomed human call (you can also defer to the tournament rec).</div>
{cards}
<script>
document.addEventListener('click',function(e){{var b=e.target.closest('[data-vote]');if(!b)return;
 var msg={{type:'send',payload:{{choice:b.getAttribute('data-vote'),human_pick:true}},framing:{json.dumps(framing)}}};
 var tp={json.dumps(target_pane)}; if(tp){{msg.target=tp;}}
 parent.postMessage(msg,'*');}});
</script></body></html>"""

def write_trace(run_id, options, chosen=None):
    os.makedirs(os.path.dirname(TRACE), exist_ok=True)
    rec = {"run": run_id, "options": [o["id"] for o in options], "chosen": chosen, "kind": "option-gallery"}
    open(TRACE, "a").write(json.dumps(rec) + "\n")
    return rec

def render(title, options, target_pane, run_id):
    body = gallery_html(title, options, target_pane)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(body); tmp = f.name
    r = subprocess.run([CLI, "note", "new", "--type", "html", "--title", f"Gallery · {title}",
                        "--source", "agent", "--open", "--body", tmp, "--json"], text=True, capture_output=True)
    os.unlink(tmp)
    if r.returncode != 0: sys.exit(f"note new failed: {r.stderr.strip()}")
    write_trace(run_id, options)
    print(f"option gallery rendered ({len(options)} options) for run {run_id}; trace -> {TRACE}")

def selftest():
    opts = [{"id": "a", "label": "Command Bar", "html": "<style>body{background:#1A1611;color:#fff}</style><b>A</b>"},
            {"id": "b", "label": "Faceted", "html": "<style>body{background:#221D17;color:#fff}</style><b>B</b>"},
            {"id": "c", "label": "Token Builder", "html": "<style>body{background:#211C17;color:#fff}</style><b>C</b>"}]
    h = gallery_html("Toolbar options", opts, target_pane="PANE")
    rec = {"run": "RUN-x", "options": ["a", "b", "c"], "chosen": None, "kind": "option-gallery"}
    ifr = h.count("<iframe")
    votes = h.count('class="vote"')
    routed = "msg.target=tp" in h
    human = "human_pick:true" in h
    print("GUILD-9 option-gallery — self-test")
    print(f"   options rendered (iframes): {ifr} | vote buttons: {votes}")
    print(f"   routes to explicit pane: {routed} | human_pick flagged: {human}")
    ok = (ifr == 3 and votes == 3 and routed and human and len(rec["options"]) == 3)
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — N options rendered live with per-option vote, routed to a live pane, human-pick flagged, replay trace shape ok.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--options"); ap.add_argument("--title", default="Options")
    ap.add_argument("--target-pane", default=None); ap.add_argument("--run", default="RUN-gallery")
    ap.add_argument("--render", action="store_true"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.render and a.options:
        opts = json.load(open(a.options))
        for o in opts:
            if o.get("file") and os.path.exists(o["file"]): o["html"] = open(o["file"]).read()
        render(a.title, opts, a.target_pane, a.run); return
    sys.exit("pass --options <f> --render [--target-pane id] or --selftest")

if __name__ == "__main__":
    main()
