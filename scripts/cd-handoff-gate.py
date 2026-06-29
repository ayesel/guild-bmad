#!/usr/bin/env python3
"""
cd-handoff-gate.py — GUILD-28: enforced Claude Design handoff gate (READ-ONLY).

Audits a screen/component being built from the Claude Design handoff BEFORE it
ships, against the REAL in-repo bundle (docs/guild/tokens.dtcg.json, pulled via
DesignSync — GUILD-27/31). Two hard, deterministic checks:

  1. 0-DRIFT TOKEN-TRACE — every colour the screen uses must trace to a bundle
     primitive. An untraceable colour = drift = FAIL.
  2. WCAG CONTRAST (hard gate) — every text/background pair must meet AA (>=4.5).
     A failing pair = FAIL (this is the enforced check Claude Design's opt-in
     "ask me to review" is not).

Usage:
  python3 scripts/cd-handoff-gate.py --screen path/to/screen.html
  python3 scripts/cd-handoff-gate.py --selftest     # proves: clean=GO, defect=NO-GO
"""
import os, re, sys, json, argparse

ROOT = os.getcwd()
DTCG = os.path.join(ROOT, "docs", "guild", "tokens.dtcg.json")
AA = 4.5

def _lin(c):
    c /= 255; return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
def _L(h):
    h = h.lstrip("#"); return 0.2126*_lin(int(h[0:2],16))+0.7152*_lin(int(h[2:4],16))+0.0722*_lin(int(h[4:6],16))
def contrast(a, b):
    la, lb = _L(a), _L(b); hi, lo = max(la, lb), min(la, lb); return (hi+0.05)/(lo+0.05)

def bundle_hexes():
    if not os.path.exists(DTCG):
        sys.exit(f"missing {DTCG} — pull the bundle (GUILD-27/31) first")
    d = json.load(open(DTCG))
    out = set()
    for grp in d.get("color", {}).values():
        if isinstance(grp, dict):
            for t in grp.values():
                v = t.get("$value") if isinstance(t, dict) else None
                if isinstance(v, str) and v.startswith("#"):
                    out.add(v.lower())
    return out

HEX = re.compile(r'#[0-9a-fA-F]{6}\b')

NEUTRALS = {"#ffffff", "#000000"}  # universally allowed; transparent handled separately

def gate(html, primitives):
    findings = []
    primitives = primitives | NEUTRALS
    used = set(m.group(0).lower() for m in HEX.finditer(html))
    # 1 — 0-drift token-trace
    drift = sorted(used - primitives)
    for d in drift:
        findings.append(("DRIFT", f"colour {d} does not trace to any bundle primitive"))
    # 2 — WCAG contrast per CSS rule block (color + background[-color])
    for block in re.findall(r'\{([^}]*)\}', html):
        fg = re.search(r'(?<!background-)\bcolor\s*:\s*(#[0-9a-fA-F]{6})', block)
        bg = re.search(r'background(?:-color)?\s*:\s*(#[0-9a-fA-F]{6})', block)
        if fg and bg:
            r = contrast(fg.group(1), bg.group(1))
            if r < AA:
                findings.append(("CONTRAST", f"{fg.group(1)} on {bg.group(1)} = {r:.2f}:1 < AA {AA}"))
    verdict = "GO" if not findings else "NO-GO"
    return verdict, findings

def run(html, label=""):
    v, f = gate(html, bundle_hexes())
    print(f"  [{v}] {label}")
    for kind, msg in f:
        print(f"     ✗ {kind}: {msg}")
    return v

CLEAN = """<style>
body { background-color:#211C17; color:#FBF7F1; }   /* ink bg / linen text — ~15:1 */
.btn { background-color:#B0421D; color:#FBF7F1; }    /* ember-600 / linen — ~5.6:1 */
.tag { background-color:#455935; color:#FBF7F1; }    /* sage-600 / linen */
</style><body><button class=btn>Save</button></body>"""

DEFECT = """<style>
body { background-color:#211C17; color:#FBF7F1; }
.muted { color:#8A7A66; background-color:#211C17; }  /* warm-500 on ink — low contrast */
.cta { background-color:#3B82F6; color:#FFFFFF; }     /* OFF-SYSTEM blue — drift */
</style><body><p class=muted>hi</p></body>"""

def selftest():
    print("GUILD-28 handoff-gate self-test (real bundle):")
    c = run(CLEAN, "clean screen (only bundle tokens, AA pairs)")
    d = run(DEFECT, "defective screen (off-system colour + low-contrast pair)")
    ok = (c == "GO" and d == "NO-GO")
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — clean→{c}, defect→{d} "
          f"(expect GO / NO-GO)")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--screen")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if not a.screen: sys.exit("pass --screen <file> or --selftest")
    v = run(open(a.screen).read(), a.screen)
    sys.exit(0 if v == "GO" else 1)

if __name__ == "__main__":
    main()
