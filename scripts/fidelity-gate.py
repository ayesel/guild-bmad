#!/usr/bin/env python3
"""
fidelity-gate.py — GUILD-52 (V-D): deterministic design->prod fidelity gate.

Design->prod drift is usually unmeasured. GUILD already has the canonical tokens
(tokens.dtcg.json) — so a deterministic fidelity gate is the cheapest high-signal
gate it can build: score how much of a BUILT artifact's colour/space values trace
to canonical tokens; below threshold => the build drifted from the design system.
CI-friendly (exit 0/1).

  python3 scripts/fidelity-gate.py --screen <built.css> [--min 0.85]
  python3 scripts/fidelity-gate.py --selftest
"""
import os, re, sys, json, argparse

DTCG = os.path.join(os.getcwd(), "docs", "guild", "tokens.dtcg.json")
MIN = 0.85

def canonical():
    try: d = json.load(open(DTCG))
    except FileNotFoundError: return set(), set()
    colors, dims = set(), set()
    def walk(n):
        if isinstance(n, dict) and "$value" in n:
            v = str(n["$value"])
            if n.get("$type") == "color" and v.startswith("#"): colors.add(v.lower())
            if n.get("$type") == "dimension": dims.add(v)
            return
        if isinstance(n, dict):
            for k, x in n.items():
                if not k.startswith("$"): walk(x)
    walk(d)
    return colors, dims

def score(css, colors, dims):
    used_c = [m.lower() for m in re.findall(r'#[0-9a-fA-F]{6}', css)]
    used_d = re.findall(r'\b\d+(?:\.\d+)?(?:px|rem)\b', css)
    allow_c = colors | {"#ffffff", "#000000"}
    vals = used_c + used_d
    if not vals: return 1.0, []
    drift = [v for v in used_c if v not in allow_c] + [v for v in used_d if v not in dims and v not in ("0px", "1px")]
    fidelity = 1 - len(drift) / len(vals)
    return round(fidelity, 3), sorted(set(drift))

def selftest():
    colors, dims = {"#b0421d", "#211c17", "#f4ece1"}, {"1rem", "0.5rem", "12px"}
    clean = "a{color:#F4ECE1;background:#211C17;padding:1rem;border-radius:12px;gap:0.5rem}"
    drifted = "a{color:#3B82F6;background:#211C17;padding:1rem;margin:37px;gap:13px}"
    fc, dc = score(clean, colors, dims)
    fd, dd = score(drifted, colors, dims)
    print("GUILD-52 fidelity gate — self-test")
    print(f"   clean build:   fidelity {fc}  drift {dc}")
    print(f"   drifted build: fidelity {fd}  drift {dd}")
    ok = fc >= MIN and fd < MIN and "#3b82f6" in dd
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — clean build passes; drifted build fails the fidelity floor.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--screen"); ap.add_argument("--min", type=float, default=MIN)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if not a.screen: sys.exit("pass --screen <file> or --selftest")
    colors, dims = canonical()
    f, drift = score(open(a.screen).read(), colors, dims)
    v = "GO" if f >= a.min else "NO-GO"
    print(f"[{v}] fidelity {f} (min {a.min}); {len(drift)} off-token value(s): {drift[:8]}")
    sys.exit(0 if v == "GO" else 1)

if __name__ == "__main__":
    main()
