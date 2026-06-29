#!/usr/bin/env python3
"""
spacing-hierarchy.py — GUILD-47 (V-B): hierarchical-spacing linter + depth tokens.

Junior spacing is FLAT — one gap everywhere, so nothing groups (no proximity
hierarchy). Senior spacing is HIERARCHICAL: tight within a group, loose between
groups. This lints a stylesheet for flat spacing and emits a depth (z-layer) token
scale (the missing elevation axis alongside shadow tokens).

  python3 scripts/spacing-hierarchy.py --lint <file>
  python3 scripts/spacing-hierarchy.py            # emit depth tokens
  python3 scripts/spacing-hierarchy.py --selftest
"""
import os, re, sys, argparse

OUT = os.path.join(os.getcwd(), "docs", "guild", "exports", "depth.tokens.css")
DEPTH = {"base": 0, "dropdown": 1000, "sticky": 1100, "overlay": 1200, "modal": 1300, "toast": 1400}

SPACE = re.compile(r'(?:gap|margin|padding)(?:-\w+)?\s*:\s*([\d.]+(?:rem|px|em))', re.I)

def lint(css):
    vals = [m.group(1).replace(" ", "") for m in SPACE.finditer(css)]
    findings = []
    if len(vals) >= 4:
        distinct = set(vals)
        dom = max((vals.count(v) for v in distinct), default=0) / len(vals)
        if len(distinct) <= 2 or dom > 0.70:
            findings.append(f"flat spacing — {len(distinct)} distinct value(s), dominant share "
                            f"{dom:.0%} over {len(vals)} declarations. No proximity hierarchy (GUILD-47).")
    return findings

def to_css():
    out = ["/* GENERATED — depth (z-layer) tokens (GUILD-47). The elevation AXIS that",
           "   pairs with shadow tokens; layers never collide. */", ":root {"]
    for k, v in DEPTH.items():
        out.append(f"  --z-{k}: {v};")
    out.append("}")
    return "\n".join(out) + "\n"

def selftest():
    flat = "a{gap:16px} b{margin:16px} c{padding:16px} d{gap:16px}"
    hier = "a{gap:4px} b{gap:8px} c{margin:24px} d{padding:12px}"
    fz, hz = lint(flat), lint(hier)
    zs = list(DEPTH.values())
    mono = all(zs[i] < zs[i+1] for i in range(len(zs)-1))
    print("GUILD-47 hierarchical spacing + depth — self-test")
    print(f"   flat stylesheet: {len(fz)} finding(s) | hierarchical: {len(hz)} finding(s)")
    print(f"   depth scale monotonic: {mono}  ({zs})")
    ok = len(fz) == 1 and len(hz) == 0 and mono
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — flat spacing flagged, hierarchical passes; depth layers ordered.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lint")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.lint:
        for f in lint(open(a.lint).read()) or ["no flat-spacing findings"]: print(" ", f)
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(to_css())
    print(f"wrote {OUT} ({len(DEPTH)} depth tokens)")

if __name__ == "__main__":
    main()
