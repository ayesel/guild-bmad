#!/usr/bin/env python3
"""
regenerate-note.py — render a comment→regenerate PICK NOTE (card f896cbc2).

The GUILD-79 lesson as law: the owner picks from RENDERED PIXELS, side by side —
never filenames, never descriptions. Reads a set's manifest + captured screenshots,
emits a self-contained HTML note (images base64-embedded) with one Pick button per
variant; a Pick fires a send_to_agent instruction that runs regenerate-pick.py.

  python3 scripts/regenerate-note.py --project <root> --set <slug>            # HTML to stdout
  python3 scripts/regenerate-note.py --project <root> --set <slug> --render   # create/update atrium note
  python3 scripts/regenerate-note.py --selftest
"""
import os, sys, json, html, base64, argparse, tempfile, subprocess

CLI = os.environ.get("ATRIUM_CLI_PATH", "atrium")
E = html.escape

CSS = """
:root{--bg:#100f0d;--panel:#1f1b16;--inset:#171512;--line:#2c2820;--line-soft:#221e18;
--ink:#f4ece2;--ink-dim:#aa9c8d;--ink-faint:#7c7063;--ember:#ce5328;--ember-tx:#f3bca1;
--sage:#728b5b;--sage-tx:#b7c9a6;--amber:#c9971f;
--mono:ui-monospace,"SF Mono",Menlo,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:13px;line-height:1.5;padding:16px}
h1{font-size:16px;margin-bottom:4px}
.comment{background:linear-gradient(180deg,#251e12,#1c1810);border:1px solid #3d311d;border-radius:11px;
padding:12px 14px;margin:12px 0;font-size:12.5px;color:#f3dca3;line-height:1.5}
.comment b{display:block;font-size:10px;font-family:var(--mono);letter-spacing:.1em;text-transform:uppercase;
color:var(--ink-faint);margin-bottom:5px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
.v{border:1px solid var(--line-soft);border-radius:12px;background:var(--panel);overflow:hidden;display:flex;flex-direction:column}
.vh{display:flex;align-items:center;gap:8px;padding:11px 13px;border-bottom:1px solid var(--line-soft)}
.vh .k{width:24px;height:24px;border-radius:7px;background:var(--inset);border:1px solid var(--line);
display:grid;place-items:center;font-family:var(--mono);font-weight:700;font-size:11px;color:var(--ember-tx)}
.vh b{font-size:13.5px}.vh em{margin-left:auto;font-style:normal;font-family:var(--mono);font-size:9.5px;color:var(--ink-faint)}
.shots{display:grid;gap:6px;padding:8px;background:#0c0b09}
.shots img{width:100%;border-radius:7px;border:1px solid var(--line-soft);display:block}
.shots .cap{font-family:var(--mono);font-size:9px;color:var(--ink-faint);padding:0 2px}
.why{padding:11px 13px;font-size:12px;color:var(--ink-dim);line-height:1.5;flex:1}
.gates{display:flex;gap:10px;padding:0 13px 10px;font-family:var(--mono);font-size:10px;color:var(--sage-tx)}
.pick{margin:0 13px 13px;text-align:center;font-size:12.5px;font-weight:700;padding:10px;border-radius:9px;
border:none;cursor:pointer;background:var(--ember);color:#1d0f06}
.pick:hover{filter:brightness(1.1)}
.foot{margin-top:14px;font-size:11px;color:var(--ink-faint);line-height:1.5}
"""


def b64img(path):
    return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()


def build_html(set_dir, manifest, embed=True):
    v = manifest["variants"]
    cards = []
    for key in sorted(v.keys()):
        m = v[key]
        shots = ""
        for img in m.get("images", []):
            p = os.path.join(set_dir, img)
            src = b64img(p) if (embed and os.path.exists(p)) else E(p)
            label = "motion frozen mid-flight" if ("entrance" in img or "signature" in img) else "at rest"
            shots += f'<img src="{src}" alt="{E(m["name"])} — {label}"><span class="cap">{E(label)}</span>'
        gates = " ".join(f"✓ {E(g)}" for g, code in (m.get("gates") or {}).items() if code == 0)
        instr = (f"Record regenerate pick {key.upper()} — run: python3 ~/.claude/guild/scripts/regenerate-pick.py "
                 f"--project {manifest['project']} --set {manifest['set']} --pick {key} ; then run the project's "
                 f"test suite and build, and commit the applied change.")
        cards.append(
            f'<div class="v"><div class="vh"><span class="k">{key.upper()}</span><b>{E(m["name"])}</b>'
            f'<em>{E(m.get("lane",""))}</em></div>'
            f'<div class="shots">{shots}</div>'
            f'<div class="why">{E(m["rationale"])}</div>'
            f'<div class="gates">{gates}</div>'
            f'<button class="pick" onclick=\'g({json.dumps(instr)})\'>Pick {key.upper()} — {E(m["name"])}</button></div>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<h1>Pick a treatment · {E(manifest["set"])}</h1>'
            f'<div class="comment"><b>Your comment</b>{E(manifest["comment"].strip())}</div>'
            f'<div class="grid">{"".join(cards)}</div>'
            f'<button class="pick" style="background:transparent;border:1px solid var(--line);color:var(--ink-dim);width:100%;margin-top:12px" '
            f'onclick=\'g({json.dumps(iterate_instr(manifest))})\'>None of these — keep iterating (tell Guild what is off)</button>'
            f'<div class="foot">Every candidate is a real implementation (patch + live-app render + gates). '
            f'Your pick applies instantly and teaches Guild your taste — rejected treatments become '
            f'calibration labels. Rejecting all three is also a pick: Guild records it and diverges again from your feedback.</div>'
            f'<script>function g(t){{parent.postMessage({{type:"send",payload:{{instruction:t}},framing:t}},"*")}}</script>'
            f'</body></html>')



def iterate_instr(manifest):
    return (f"Owner rejected ALL variants in regenerate set {manifest['set']} — record it "
            f"(python3 ~/.claude/guild/scripts/regenerate-pick.py --project {manifest['project']} "
            f"--set {manifest['set']} --pick none), ask the owner what was off about A/B/C in one "
            f"question, then re-run the diverge (STEP 2 of /guild-comment) with that critique added "
            f"to the comment — new lanes, never repeats of rejected directions.")

def find_set(project, slug):
    for out in ("_bmad-output", "guild-output", "."):
        d = os.path.join(project, out, "guild-artifacts", "regenerate", slug)
        if os.path.isdir(d): return d
    sys.exit(f"regenerate set '{slug}' not found under {project}")


def render(set_dir, manifest, body):
    nf = os.path.join(set_dir, ".pick-note-id")
    nid = open(nf).read().strip() if os.path.exists(nf) else None
    if nid:
        r = subprocess.run([CLI, "note", "write", nid, "--content", body], text=True, capture_output=True)
        if r.returncode == 0: print(f"updated pick note {nid}"); return
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(body); tmp = f.name
    r = subprocess.run([CLI, "note", "new", "--type", "html",
                        "--title", f"Pick · {manifest['set']} ({manifest.get('project','').split('/')[-1]})",
                        "--source", "agent", "--body", tmp, "--json"], text=True, capture_output=True)
    os.unlink(tmp)
    if r.returncode != 0: sys.exit(f"note new failed: {r.stderr.strip()}")
    try:
        d = json.loads(r.stdout); nid = d.get("meta", {}).get("id") or d.get("id")
    except Exception: nid = None
    if nid: open(nf, "w").write(nid); print(f"created pick note {nid}")


def selftest():
    manifest = {"set": "t", "project": "/tmp/p", "comment": "too static",
                "variants": {"a": {"name": "A", "lane": "l", "rationale": "r", "images": [], "gates": {"build": 0}},
                             "b": {"name": "B", "lane": "l", "rationale": "r", "images": [], "gates": {"build": 0}}}}
    h = build_html("/tmp", manifest, embed=False)
    ok = all(x in h for x in ("Pick A", "Pick B", "Your comment", "regenerate-pick.py", "postMessage"))
    print("regenerate-note self-test:", "✅ PASS" if ok else "❌ FAIL")
    sys.exit(0 if ok else 1)


def main():
    import yaml
    ap = argparse.ArgumentParser()
    ap.add_argument("--project"); ap.add_argument("--set", dest="slug")
    ap.add_argument("--render", action="store_true"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if not (a.project and a.slug): sys.exit("need --project --set (or --selftest)")
    project = os.path.abspath(os.path.expanduser(a.project))
    set_dir = find_set(project, a.slug)
    manifest = yaml.safe_load(open(os.path.join(set_dir, "manifest.yaml")))
    body = build_html(set_dir, manifest)
    if a.render: render(set_dir, manifest, body)
    else: sys.stdout.write(body)


if __name__ == "__main__":
    main()
