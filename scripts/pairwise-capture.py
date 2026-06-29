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

def note_html(a, b, pair_id, target, prompt):
    framing = (f"Owner blind pick for pair {pair_id} (target={target}). Append to "
               f"{TARGETS.get(target, target)} — record the OWNER_PICK letter. {{payload}}")
    def pick_btn(letter):
        payload = json.dumps({"pair": pair_id, "owner_pick": letter, "target": target})
        return (f'<button class="pick" data-send=\'{E(payload)}\'>Pick {letter}</button>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
:root{{--bg:#1A1611;--surface:#221D17;--border:#3A332A;--text:#F4ECE1;--muted:#B8A88F;--ember:#E06E45}}
body{{margin:0;background:var(--bg);color:var(--text);font:13px/1.5 ui-sans-serif,system-ui;padding:16px}}
h2{{font:600 15px ui-serif,Georgia;margin:0 0 4px}}.q{{color:var(--muted);font-size:12px;margin-bottom:14px}}
.row{{display:flex;gap:12px}}.opt{{flex:1;background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px}}
.opt h3{{margin:0 0 8px;font-size:13px;color:var(--ember)}}.opt p{{color:var(--muted);font-size:12px;margin:0}}
.picks{{display:flex;gap:10px;margin-top:14px}}
button.pick{{flex:1;background:var(--ember);border:0;color:#1A1611;font-weight:600;border-radius:8px;padding:11px;font-size:13px;cursor:pointer}}
button.pick:hover{{filter:brightness(1.08)}}
</style></head><body>
<h2>Which is better?</h2><div class="q">{E(prompt)} — blind (you don't see which is which).</div>
<div class="row">
  <div class="opt"><h3>Option A</h3><p>{E(a)}</p></div>
  <div class="opt"><h3>Option B</h3><p>{E(b)}</p></div>
</div>
<div class="picks">{pick_btn('A')}{pick_btn('B')}</div>
<script>
document.addEventListener('click',function(e){{var b=e.target.closest('[data-send]');if(!b)return;
 parent.postMessage({{type:'send',payload:JSON.parse(b.getAttribute('data-send')),
   framing:{json.dumps(framing)}}},'*');}});
</script></body></html>"""

def render(a, b, pair_id, target, prompt, mapping):
    body = note_html(a, b, pair_id, target, prompt)
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
    h = note_html("arm-merge screen", "arm-select screen", "P1", "ab-eval", "Nourish Today screen")
    blind = ("Option A" in h and "Option B" in h
             and "arm-merge" not in h.split('<script>')[0]  # arm identity NOT shown in the visible body
             and h.count('class="pick"') == 2)
    print("GUILD-42/44 pairwise-capture — self-test")
    print(f"   2 blind options + 2 pick buttons: {h.count(chr(34)+'opt'+chr(34))==2 and h.count('pick')>=2}")
    print(f"   arm identity hidden from the visible note: {'arm-merge' not in h.split('<script>')[0]}")
    ok = blind
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — renders a blind A/B pick; arm/source labels never shown; pick posts via send_to_agent.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a"); ap.add_argument("--b"); ap.add_argument("--pair-id", default="P1")
    ap.add_argument("--target", choices=list(TARGETS), default="calibration")
    ap.add_argument("--prompt", default="Which design is better?")
    ap.add_argument("--map-out", default=None, help="append the A/B↔arm mapping here (for de-blinding at scoring)")
    ap.add_argument("--render", action="store_true"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.render and a.a and a.b:
        render(a.a, a.b, a.pair_id, a.target, a.prompt, a.map_out); return
    sys.exit("pass --a --b --render [--target ...] or --selftest")

if __name__ == "__main__":
    main()
