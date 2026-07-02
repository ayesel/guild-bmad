#!/usr/bin/env python3
"""
guild-render.py — spec-once, render-anywhere fan-out (the north-star adapter thesis).

Takes ONE canonical artifact model and renders it to multiple platforms in one
command. The brain decides once; platforms are output formats.

Targets (v1):
  figjam — figjam-renderer.py (deterministic layout + semantic style + board-craft
           QA, exit-code gated) -> <out>/board.json ready for the Figma MCP push
  html   — a self-contained, device-light, interactive wireframe prototype
           (reduced-motion safe, guild aesthetic) -> <out>/prototype.html

  python3 scripts/guild-render.py --artifact <model.json> --targets figjam,html --out <dir>
  python3 scripts/guild-render.py --selftest
Exit 0 = every requested target rendered AND passed its gate; 1 = any failure.
"""
import os, sys, json, html, argparse, importlib.util, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape


def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def render_figjam(model, out_dir):
    fr = _load("fr", "figjam-renderer.py")
    board = fr.render(model)
    qa = fr.post_render_qa(model, board)
    path = os.path.join(out_dir, "board.json")
    json.dump(board, open(path, "w"), indent=2)
    for x in qa: print("  ✗ board-craft:", x)
    print(f"  figjam: {len(board['nodes'])} nodes -> {path} · QA findings: {len(qa)}")
    return len(qa) == 0


HTML_CSS = """
:root{--bg:#100f0d;--panel:#1f1b16;--inset:#171512;--line:#2c2820;--line-soft:#221e18;
--ink:#f4ece2;--ink-dim:#aa9c8d;--ink-faint:#7c7063;--ember:#ce5328;--ember-tx:#f3bca1;
--sage:#728b5b;--sage-tx:#b7c9a6;--amber:#c9971f;
--mono:ui-monospace,"SF Mono",Menlo,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:14px;line-height:1.5;padding:20px;max-width:840px;margin:0 auto}
h1{font-size:17px;margin-bottom:3px}.sub{font-size:11px;color:var(--ink-faint);font-family:var(--mono);margin-bottom:16px}
.node{border:1px solid var(--line-soft);border-radius:11px;background:var(--panel);padding:13px 15px;margin:10px 0;
transition:border-color .18s ease,transform .18s ease}
.node:hover{border-color:rgba(206,83,40,.4);transform:translateX(2px)}
.node b{font-size:13.5px;display:block}
.node .kind{font-family:var(--mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-faint)}
.node.decision{border-style:dashed;background:var(--inset)}
.node.step{margin-left:26px}
.node .reuse{display:inline-block;margin-top:5px;font-family:var(--mono);font-size:9.5px;color:var(--sage-tx);
background:rgba(143,174,125,.12);border:1px solid rgba(143,174,125,.25);border-radius:5px;padding:1px 7px}
.edge{margin-left:12px;color:var(--ink-faint);font-family:var(--mono);font-size:10px;padding:1px 0}
details{margin-top:14px;border:1px solid var(--line-soft);border-radius:9px;padding:10px 13px;background:var(--inset)}
summary{cursor:pointer;font-size:12px;font-weight:650;color:var(--ink-dim)}
.foot{margin-top:16px;font-size:10.5px;color:var(--ink-faint);font-family:var(--mono)}
@media(prefers-reduced-motion:reduce){.node{transition:none}}
"""


def render_html(model, out_dir):
    nodes = {n["id"]: n for n in model.get("nodes", [])}
    children = {}
    roots = set(nodes)
    for e in model.get("edges", []):
        children.setdefault(e["from"], []).append(e["to"])
        roots.discard(e["to"])

    def emit(nid, depth=0, seen=None):
        seen = seen or set()
        if nid in seen or nid not in nodes: return ""
        seen.add(nid)
        n = nodes[nid]
        label = n["label"]
        reuse = ""
        if "[reuse:" in label:
            label, r = label.split("[reuse:", 1)
            reuse = f'<span class="reuse">↺ reuse: {E(r.rstrip("] "))}</span>'
        out = (f'<div class="node {E(n.get("type",""))}" style="margin-left:{depth*26}px">'
               f'<span class="kind">{E(n.get("type","node"))}</span><b>{E(label.strip())}</b>{reuse}</div>')
        for c in children.get(nid, []):
            out += f'<div class="edge" style="margin-left:{depth*26+14}px">└─▸</div>' + emit(c, depth + 1, seen)
        return out

    body = "".join(emit(r) for r in sorted(roots))
    n_reuse = sum(1 for n in model.get("nodes", []) if "[reuse:" in n["label"])
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<style>{HTML_CSS}</style></head><body>'
           f'<h1>{E(model.get("title", "GUILD artifact"))}</h1>'
           f'<div class="sub">living wireframe · rendered by guild-render from the canonical model · '
           f'{len(nodes)} nodes · {n_reuse} pattern reuses</div>'
           f'{body}'
           f'<details><summary>Canonical model (the single source both renders share)</summary>'
           f'<pre style="font-size:10px;overflow-x:auto;margin-top:8px">{E(json.dumps(model, indent=1))}</pre></details>'
           f'<div class="foot">spec-once · render-anywhere — same model feeds FigJam (collab) and this prototype (click-through)</div>'
           f'</body></html>')
    path = os.path.join(out_dir, "prototype.html")
    open(path, "w").write(doc)
    kb = os.path.getsize(path) / 1024
    print(f"  html: {len(nodes)} nodes -> {path} ({kb:.0f}kb, self-contained)")
    return kb < 200   # device-light guard


TARGETS = {"figjam": render_figjam, "html": render_html}


def selftest():
    import tempfile
    model = {"type": "screen-structure", "title": "T", "layout_contract": {"engine": "tree"},
             "nodes": [{"id": "a", "label": "Root [reuse: x]", "type": "page"},
                       {"id": "b", "label": "Child", "type": "step"}],
             "edges": [{"from": "a", "to": "b"}]}
    with tempfile.TemporaryDirectory() as td:
        ok = render_figjam(model, td) and render_html(model, td)
        h = open(os.path.join(td, "prototype.html")).read()
        ok = ok and "reuse: x" in h and "prefers-reduced-motion" in h and os.path.exists(os.path.join(td, "board.json"))
    print("guild-render self-test:", "✅ PASS" if ok else "❌ FAIL")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact"); ap.add_argument("--targets", default="figjam,html")
    ap.add_argument("--out"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if not (a.artifact and a.out): sys.exit("need --artifact <model.json> --out <dir> (or --selftest)")
    model = json.load(open(a.artifact))
    os.makedirs(a.out, exist_ok=True)
    ok = True
    for t in a.targets.split(","):
        t = t.strip()
        if t not in TARGETS: sys.exit(f"unknown target '{t}' (have: {', '.join(TARGETS)})")
        print(f"rendering -> {t}")
        ok = TARGETS[t](model, a.out) and ok
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
