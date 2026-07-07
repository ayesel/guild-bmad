#!/usr/bin/env python3
"""
pairwise-capture.py — GUILD-42 + GUILD-44: blind pairwise-pick capture.

One primitive for both owner tasks: render a BLIND pairwise note (Option A / Option B,
no arm/source labels, order recorded) with Pick buttons that fire send_to_agent. The
receiving Guild agent appends the owner's pick to the target yaml:
  - GUILD-44 calibration: append to docs/guild/evals/calibration-set.yaml labels[]
  - GUILD-42 A/B:       append to an ab-eval verdicts file (de-blinded for scoring)

  python3 scripts/pairwise-capture.py --a "<A ref/desc>" --b "<B ref/desc>" \
     --pair-id P1 --target calibration --render
  python3 scripts/pairwise-capture.py --selftest

Blind: the note never shows which option is which arm/source — only A/B. The A↔arm
mapping lives in --map-out (written for the scorer), NOT in the note.
"""
import os, sys, json, html, subprocess, tempfile, argparse
E = html.escape
CLI = os.environ.get("ATRIUM_CLI_PATH", "atrium")

TARGETS = {
    "calibration": "docs/guild/evals/calibration-set.yaml (labels[])",
    "ab-eval": "an ab-eval verdicts file [{pair,owner_pick}]",
}

def note_html(a, b, pair_id, target, prompt, target_pane=None, a_html=None, b_html=None):
    framing = (f"Owner blind pick for pair {pair_id} (target={target}). Append to "
               f"{TARGETS.get(target, target)} — record the OWNER_PICK letter. {{payload}}")
    def pick_btn(letter):
        payload = json.dumps({"pair": pair_id, "owner_pick": letter, "target": target})
        return (f'<button class="pick" data-send=\'{E(payload)}\'>Pick {letter}</button>')
    def opt(label, ref, html):  # GUILD-79: RENDER the design (live iframe), not just a filename
        letter = label[-1]
        inner = (f'<iframe sandbox="allow-scripts" srcdoc="{E(html)}" '
                 f'style="width:100%;height:62vh;border:0;border-radius:8px;background:#fff"></iframe>'
                 ) if html else f'<p>{E(ref)}</p>'
        zoom = (f'<button class="zoom" data-zoom="{letter}" title="Maximize (then ←/→ to flip A/B, Esc to close)">⤢ maximize</button>'
                if html else '')
        return f'<div class="opt"><h3>{label} {zoom}</h3>{inner}</div>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
:root{{--bg:#1A1611;--surface:#221D17;--border:#3A332A;--text:#F4ECE1;--muted:#B8A88F;--ember:#E06E45}}
body{{margin:0;background:var(--bg);color:var(--text);font:13px/1.5 ui-sans-serif,system-ui;padding:16px}}
h2{{font:600 15px ui-serif,Georgia;margin:0 0 4px}}.q{{color:var(--muted);font-size:12px;margin-bottom:14px}}
.row{{display:flex;gap:12px}}.opt{{flex:1;background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px}}
.opt h3{{margin:0 0 8px;font-size:13px;color:var(--ember)}}.opt p{{color:var(--muted);font-size:12px;margin:0}}
.picks{{display:flex;gap:10px;margin-top:14px}}
button.pick{{flex:1;background:var(--ember);border:0;color:#1A1611;font-weight:600;border-radius:8px;padding:11px;font-size:13px;cursor:pointer}}
button.pick:hover{{filter:brightness(1.08)}}
button.zoom{{float:right;background:transparent;border:1px solid var(--border);color:var(--muted);border-radius:6px;padding:2px 8px;font-size:11px;cursor:pointer}}
button.zoom:hover{{color:var(--text);border-color:var(--muted)}}
#max{{display:none;position:fixed;inset:0;background:rgba(10,8,6,.96);z-index:50;padding:14px;flex-direction:column;gap:10px}}
#max.on{{display:flex}}
#max .bar{{display:flex;align-items:center;gap:10px}}
#max .bar .which{{font:600 14px ui-serif,Georgia;color:var(--ember);min-width:90px}}
#max .bar button{{background:var(--surface);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:8px 14px;font-size:13px;cursor:pointer}}
#max .bar button:hover{{border-color:var(--muted)}}
#max .bar .hint{{color:var(--muted);font-size:11px;margin-left:auto}}
#max iframe{{flex:1;width:100%;border:0;border-radius:8px;background:#fff}}
#max button.pick{{flex:0 0 auto;padding:11px 22px}}
</style></head><body>
<h2>Which is better?</h2><div class="q">{E(prompt)} — blind (you don't see which is which). Tip: ⤢ maximize, then ←/→ flips A/B for direct comparison.</div>
<div class="row">{opt("Option A", a, a_html)}{opt("Option B", b, b_html)}</div>
<div class="picks">{pick_btn('A')}{pick_btn('B')}</div>
<div id="max">
  <div class="bar">
    <span class="which" id="maxWhich">Option A</span>
    <button id="prevB" title="Previous (←)">‹</button>
    <button id="nextB" title="Next (→)">›</button>
    <button class="pick" data-send-current="1">Pick this one</button>
    <span class="hint">←/→ flip A/B · Esc close</span>
    <button id="closeB" title="Close (Esc)">✕ close</button>
  </div>
  <iframe id="maxFrame" sandbox="allow-scripts"></iframe>
</div>
<script>
var SRC={{A:{json.dumps(a_html or "")},B:{json.dumps(b_html or "")}}};
var PAYLOADS={{A:{json.dumps(json.dumps({"pair": pair_id, "owner_pick": "A", "target": target}))},B:{json.dumps(json.dumps({"pair": pair_id, "owner_pick": "B", "target": target}))}}};
var cur='A';
function sendPick(payloadStr){{
 var msg={{type:'send',payload:JSON.parse(payloadStr),framing:{json.dumps(framing)}}};
 var tp={json.dumps(target_pane)}; if(tp){{msg.target=tp;}}   /* GUILD-79: explicit live target, no stale-pane drop */
 parent.postMessage(msg,'*');}}
function openMax(letter){{cur=letter;var m=document.getElementById('max');m.classList.add('on');
 document.getElementById('maxFrame').srcdoc=SRC[cur];document.getElementById('maxWhich').textContent='Option '+cur;}}
function flip(){{openMax(cur==='A'?'B':'A');}}
function closeMax(){{document.getElementById('max').classList.remove('on');}}
document.addEventListener('click',function(e){{
 var z=e.target.closest('[data-zoom]'); if(z){{openMax(z.getAttribute('data-zoom'));return;}}
 if(e.target.id==='prevB'||e.target.id==='nextB'){{flip();return;}}
 if(e.target.id==='closeB'){{closeMax();return;}}
 var c=e.target.closest('[data-send-current]'); if(c){{sendPick(PAYLOADS[cur]);closeMax();return;}}
 var b=e.target.closest('[data-send]'); if(b){{sendPick(b.getAttribute('data-send'));}}
}});
document.addEventListener('keydown',function(e){{
 var on=document.getElementById('max').classList.contains('on'); if(!on)return;
 if(e.key==='ArrowLeft'||e.key==='ArrowRight'){{flip();e.preventDefault();}}
 else if(e.key==='Escape'){{closeMax();}}
}});
</script></body></html>"""

def render(a, b, pair_id, target, prompt, mapping, target_pane=None, a_file=None, b_file=None):
    a_html = open(a_file).read() if a_file and os.path.exists(a_file) else None
    b_html = open(b_file).read() if b_file and os.path.exists(b_file) else None
    body = note_html(a, b, pair_id, target, prompt, target_pane, a_html, b_html)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(body); tmp = f.name
    r = subprocess.run([CLI, "note", "new", "--type", "html", "--title", f"Pick · {pair_id}",
                        "--source", "agent", "--open", "--body", tmp, "--json"], text=True, capture_output=True)
    os.unlink(tmp)
    if r.returncode != 0: sys.exit(f"note new failed: {r.stderr.strip()}")
    if mapping:
        open(mapping, "a").write(json.dumps({"pair": pair_id, "A": a, "B": b, "target": target}) + "\n")
    print(f"blind pick note created for {pair_id} (target={target}); A↔arm map -> {mapping or '(not saved)'}")

def selftest():
    # caller passes NEUTRAL content; the script labels only A/B and never injects the
    # source/arm. The A<->arm mapping lives in --map-out, never in the note.
    h = note_html("screen-x.html", "screen-y.html", "P1", "ab-eval", "Nourish Today screen")
    body = h.split('<script>')[0]
    # 2 inline pick buttons + 1 pick-from-maximize button (owner UX ask 2026-07-06:
    # maximize view with arrow-key A/B flip)
    two_opts = body.count('class="opt"') == 2 and h.count('class="pick"') == 3 and 'data-zoom' in h and 'ArrowLeft' in h
    no_arm_words = not any(w in h.lower() for w in ("merge", "select", "arm-", "source:"))  # script adds none
    posts = ('type:\'send\'' in h) and ('owner_pick' in h)
    print("GUILD-42/44 pairwise-capture — self-test")
    print(f"   2 options + 2 pick buttons: {two_opts}")
    print(f"   script injects no arm/source label: {no_arm_words}")
    print(f"   pick posts owner_pick via send_to_agent: {posts}")
    ok = two_opts and no_arm_words and posts
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — blind A/B (A↔arm map kept in --map-out, not the note); pick posts via send_to_agent.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a"); ap.add_argument("--b"); ap.add_argument("--pair-id", default="P1")
    ap.add_argument("--target", choices=list(TARGETS), default="calibration")
    ap.add_argument("--prompt", default="Which design is better?")
    ap.add_argument("--map-out", default=None, help="append the A/B↔arm mapping here (for de-blinding at scoring)")
    ap.add_argument("--target-pane", default=None, help="GUILD-79: explicit LIVE pane id to route the pick to (avoids stale-pane drop)")
    ap.add_argument("--a-file", default=None, help="GUILD-79: HTML design to RENDER as Option A (live iframe, not a filename)")
    ap.add_argument("--b-file", default=None, help="HTML design to RENDER as Option B")
    ap.add_argument("--render", action="store_true"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.render and a.a and a.b:
        render(a.a, a.b, a.pair_id, a.target, a.prompt, a.map_out, a.target_pane, a.a_file, a.b_file); return
    sys.exit("pass --a --b --render [--target ...] or --selftest")

if __name__ == "__main__":
    main()
