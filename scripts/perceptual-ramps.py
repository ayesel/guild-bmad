#!/usr/bin/env python3
"""
perceptual-ramps.py — GUILD-46 (V-B): perceptual color ramps.

Junior ramps step evenly in hex/HSL, which is perceptually LUMPY (big jumps in the
mids, tiny ones at the ends). Senior ramps step evenly in PERCEPTUAL lightness
(CIE L*). This audits each ramp in tokens.dtcg.json: compute L* per stop and flag
ramps whose L* steps are uneven (max/min step ratio over threshold) or non-monotonic.

  python3 scripts/perceptual-ramps.py            # audit the real ramps
  python3 scripts/perceptual-ramps.py --selftest
"""
import os, sys, json, argparse

DTCG = os.path.join(os.getcwd(), "docs", "guild", "tokens.dtcg.json")
EVENNESS_MAX = 2.5   # max acceptable (largest L* step / smallest L* step)

def _lin(c):
    c /= 255; return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
def lstar(hexs):
    h = hexs.lstrip("#"); r, g, b = (_lin(int(h[i:i+2], 16)) for i in (0, 2, 4))
    Y = 0.2126*r + 0.7152*g + 0.0722*b
    f = Y ** (1/3) if Y > 0.008856 else 7.787*Y + 16/116
    return 116*f - 16

def audit_ramp(hexes):
    ls = [lstar(h) for h in hexes]
    deltas = [abs(ls[i] - ls[i+1]) for i in range(len(ls)-1)]
    deltas = [d for d in deltas if d > 0.01] or [1]
    ratio = max(deltas) / min(deltas)
    monotonic = all(ls[i] > ls[i+1] for i in range(len(ls)-1)) or all(ls[i] < ls[i+1] for i in range(len(ls)-1))
    ok = ratio <= EVENNESS_MAX and monotonic
    return {"lstars": [round(x, 1) for x in ls], "step_ratio": round(ratio, 2),
            "monotonic": monotonic, "even": ok}

def ramps_from_dtcg():
    try: d = json.load(open(DTCG))
    except FileNotFoundError: return {}
    out = {}
    for name, grp in (d.get("color") or {}).items():
        if not isinstance(grp, dict): continue
        stops = [(k, t.get("$value")) for k, t in grp.items()
                 if isinstance(t, dict) and str(t.get("$value", "")).startswith("#")]
        if len(stops) >= 4:
            stops.sort(key=lambda kv: lstar(kv[1]), reverse=True)
            out[name] = [v for _, v in stops]
    return out

def selftest():
    even = ["#211C17", "#4E4438", "#8A7A66", "#B3A088", "#E7DACA", "#FBF7F1"]  # warm ramp ~even L*
    lumpy = ["#000000", "#0c0c0c", "#161616", "#222222", "#FFFFFF"]            # tiny steps then huge jump
    a, b = audit_ramp(even), audit_ramp(lumpy)
    print("GUILD-46 perceptual color ramps — self-test")
    print(f"   even ramp:  L* {a['lstars']}  ratio {a['step_ratio']}  even={a['even']}")
    print(f"   lumpy ramp: L* {b['lstars']}  ratio {b['step_ratio']}  even={b['even']}")
    ok = a["even"] is True and b["even"] is False
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — even-L* ramp passes; perceptually lumpy ramp flagged.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    ramps = ramps_from_dtcg()
    if not ramps: sys.exit("no ramps in tokens.dtcg.json")
    bad = 0
    for name, hexes in ramps.items():
        r = audit_ramp(hexes)
        flag = "" if r["even"] else "  ⚠ UNEVEN (smooth the L* steps)"
        if not r["even"]: bad += 1
        print(f"  {name:8} ratio {r['step_ratio']:>4}  monotonic={r['monotonic']}{flag}")
    print(f"\n{bad} ramp(s) flagged. Senior ramps step evenly in perceptual lightness.")

if __name__ == "__main__":
    main()
