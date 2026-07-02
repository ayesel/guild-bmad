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
.vsw{position:absolute;opacity:0;pointer-events:none}
.vtoggle{display:flex;gap:2px;margin:0 0 12px;border:1px solid var(--line-soft);border-radius:9px;padding:3px;background:var(--inset);width:max-content}
.vtoggle label{font-size:11px;font-weight:650;color:var(--ink-faint);padding:5px 14px;border-radius:7px;cursor:pointer}
.vtoggle label:hover{color:var(--ink-dim)}
#vw-grid:checked~.vtoggle label[for=vw-grid],#vw-line:checked~.vtoggle label[for=vw-line]{background:var(--panel);color:var(--ember-tx);border:1px solid var(--line)}
.grid{display:grid;grid-template-columns:repeat(var(--ncols,3),minmax(0,1fr));gap:12px}
#vw-line:checked~.grid{grid-template-columns:1fr;max-width:760px;margin:0 auto}
#vw-line:checked~.grid .shots{grid-template-columns:1fr;max-width:none}
#vw-line:checked~.grid .shots img{width:100%}
#vw-line:checked~.grid .v{max-width:none}
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
.shots img{cursor:zoom-in}
.zoom{position:fixed;inset:0;background:rgba(10,9,8,.94);display:none;place-items:center;z-index:99;cursor:zoom-out;padding:20px}
.zoom.on{display:grid}
.zoom img{max-width:96vw;max-height:88vh;width:auto;border-radius:9px;border:1px solid var(--line)}
.zoom .zcap{position:fixed;bottom:14px;left:0;right:0;text-align:center;font-size:12.5px;color:var(--ink)}
.shotwrap{position:relative;display:block}
.pin{position:absolute;width:20px;height:20px;border-radius:50%;background:var(--ember);color:#1d0f06;
font-family:var(--mono);font-weight:800;font-size:11px;display:grid;place-items:center;
border:2px solid #fff3;box-shadow:0 1px 6px rgba(0,0,0,.5);transform:translate(-50%,-50%)}
.legend{padding:9px 13px 0;display:grid;gap:4px}
.legend span{font-size:11px;color:var(--ink-dim);line-height:1.45;display:flex;gap:7px}
.legend b{flex:0 0 auto;width:16px;height:16px;border-radius:50%;background:var(--ember);color:#1d0f06;
font-family:var(--mono);font-weight:800;font-size:9.5px;display:grid;place-items:center;margin-top:1px}
.legend .np b{background:var(--panel2);color:var(--ink-dim)}
.seq{position:relative;border-radius:7px;border:1px solid var(--line-soft);overflow:hidden}
.seq img{width:100%;display:block}
.seq img+img{position:absolute;inset:0;opacity:0}
.seq .live{position:absolute;top:8px;left:8px;font-family:var(--mono);font-size:9px;font-weight:700;
letter-spacing:.08em;background:rgba(206,83,40,.9);color:#1d0f06;border-radius:5px;padding:2px 7px;z-index:9}
.strip{display:grid;grid-auto-flow:column;gap:4px;padding:6px 0 0}
.strip img{width:100%;border-radius:5px;border:1px solid var(--line-soft);display:block}
.strip .fn{font-family:var(--mono);font-size:8.5px;color:var(--ink-faint);text-align:center;padding-top:2px}
@media(prefers-reduced-motion:reduce){.seq img{animation:none !important;opacity:0}.seq img:first-child{opacity:1}}
"""


def b64img(path):
    return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()


def build_html(set_dir, manifest, embed=True):
    v = manifest["variants"]
    cards = []
    for key in sorted(v.keys()):
        m = v[key]
        shots = ""
        callouts = m.get("callouts") or []
        seq = m.get("sequence") or {}
        frames = seq.get("frames") or []
        if frames:
            n, T = len(frames), 0.8
            total = n * T
            kf_name = f"seqfade{key}"
            hold = round(100.0 / n, 2)
            kf = (f'@keyframes {kf_name}{{0%{{opacity:1}}{hold}%{{opacity:1}}'
                  f'{min(hold+4,99)}%{{opacity:0}}100%{{opacity:0}}}}')
            imgs = ""
            cells = ""
            for i, fr in enumerate(frames):
                fp = os.path.join(set_dir, fr)
                src = b64img(fp) if (embed and os.path.exists(fp)) else E(fp)
                imgs += (f'<img src="{src}" alt="frame {i+1}" '
                         f'style="animation:{kf_name} {total}s linear infinite;animation-delay:{i*T}s">')
                cells += f'<span><img src="{src}"><span class="fn">{i+1}</span></span>'
            shots += (f'<style>{kf}</style><span class="seq"><span class="live">▶ {E(seq.get("label","live preview"))}</span>'
                      f'{imgs}</span><span class="cap">animated: {E(seq.get("label",""))} — frames below</span>'
                      f'<span class="strip" style="grid-template-columns:repeat({n},1fr)">{cells}</span>')
        for img in m.get("images", []):
            if isinstance(img, dict):
                fname, label = img.get("file", ""), img.get("caption", "")
            else:
                fname = img
                label = "motion frozen mid-flight" if ("entrance" in img or "signature" in img) else "at rest"
            p = os.path.join(set_dir, fname)
            src = b64img(p) if (embed and os.path.exists(p)) else E(p)
            pins = "".join(f'<span class="pin" style="left:{c["x"]}%;top:{c["y"]}%">{c["n"]}</span>'
                           for c in callouts if c.get("image") == fname)
            shots += (f'<span class="shotwrap"><img src="{src}" alt="{E(m["name"])} — {label}" '
                      f'data-cap="{E(m["name"] + " — " + label)}" onclick="zoom(this)">{pins}</span>'
                      f'<span class="cap">{E(label)} · click to enlarge</span>')
        pinned_ns = {c["n"] for c in callouts}
        legend = "".join(
            f'<span class="{"" if i+1 in pinned_ns else "np"}"><b>{i+1}</b> {E(item)}</span>'
            for i, item in enumerate(m.get("legend") or []))
        legend_html = f'<div class="legend">{legend}</div>' if legend else ""
        gates = " ".join(f"✓ {E(g)}" for g, code in (m.get("gates") or {}).items() if code == 0)
        instr = (f"Record regenerate pick {key.upper()} — run: python3 ~/.claude/guild/scripts/regenerate-pick.py "
                 f"--project {manifest['project']} --set {manifest['set']} --pick {key} ; then run the project's "
                 f"test suite and build, and commit the applied change.")
        cards.append(
            f'<div class="v"><div class="vh"><span class="k">{key.upper()}</span><b>{E(m["name"])}</b>'
            f'<em>{E(m.get("lane",""))}</em></div>'
            f'<div class="shots">{shots}</div>'
            f'{legend_html}'
            f'<div class="why">{E(m["rationale"])}</div>'
            f'<div class="gates">{gates}</div>'
            f'<button class="pick" onclick=\'g({json.dumps(instr)})\'>Pick {key.upper()} — {E(m["name"])}</button></div>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<h1>Pick a treatment · {E(manifest["set"])}</h1>'
            f'<div class="comment"><b>Your comment</b>{E(manifest["comment"].strip())}</div>'
            f'<input type="radio" name="vw" id="vw-grid" class="vsw" checked>'
            f'<input type="radio" name="vw" id="vw-line" class="vsw">'
            f'<div class="vtoggle"><label for="vw-grid">◫ Side by side</label><label for="vw-line">☰ One per row</label></div>'
            f'<div class="grid" style="--ncols:{len(v)}">{"".join(cards)}</div>'
            f'<button class="pick" style="background:transparent;border:1px solid var(--line);color:var(--ink-dim);width:100%;margin-top:12px" '
            f'onclick=\'g({json.dumps(iterate_instr(manifest))})\'>None of these — keep iterating (tell Guild what is off)</button>'
            f'<div class="foot">Every candidate is a real implementation (patch + live-app render + gates). '
            f'Your pick applies instantly and teaches Guild your taste — rejected treatments become '
            f'calibration labels. Rejecting all three is also a pick: Guild records it and diverges again from your feedback.</div>'
            f'<div class="zoom" id="zx" onclick="this.classList.remove(\'on\')"><img id="zi"><span class="zcap" id="zc"></span></div>'
            f'<script>function g(t){{parent.postMessage({{type:"send",payload:{{instruction:t}},framing:t}},"*")}}'
            f'function zoom(el){{document.getElementById("zi").src=el.src;document.getElementById("zc").textContent=el.dataset.cap;'
            f'document.getElementById("zx").classList.add("on");event.stopPropagation()}}</script>'
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
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write(body); tmp = f.name
        r = subprocess.run([CLI, "note", "write", nid, "--from-file", tmp], text=True, capture_output=True)
        os.unlink(tmp)
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
    ok = all(x in h for x in ("Pick A", "Pick B", "Your comment", "regenerate-pick.py", "postMessage",
                              "vw-grid", "vw-line", "Side by side", "One per row"))
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
