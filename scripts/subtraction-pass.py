#!/usr/bin/env python3
"""
subtraction-pass.py — GUILD-48 (V-B): the subtraction pass.

Senior craft REMOVES — it doesn't keep adding emphasis. When a component stacks
borders + shadows + multiple accent colors + many font-weights, the devices compete
and nothing reads as primary. This counts the competing "emphasis devices" per
component and flags over-decoration (the cue to subtract until it breaks).

  python3 scripts/subtraction-pass.py --lint <file>
  python3 scripts/subtraction-pass.py --selftest
"""
import os, re, sys, argparse

MAX_DEVICES = 4   # borders + shadows + accent colors + weights competing in one block

def _count(block):
    borders = len(re.findall(r'border(?:-\w+)?\s*:\s*(?!none)[^;]+', block, re.I))
    shadows = len(re.findall(r'box-shadow\s*:\s*(?!none)[^;]+', block, re.I))
    colors = len(set(re.findall(r'#[0-9a-fA-F]{6}', block)))
    weights = len(set(re.findall(r'font-weight\s*:\s*(\d{3})', block, re.I)))
    radii = len(set(re.findall(r'border-radius\s*:\s*([^;]+)', block, re.I)))
    total = borders + shadows + colors + weights
    return {"borders": borders, "shadows": shadows, "accent_colors": colors,
            "weights": weights, "radii": radii, "devices": total}

def lint(css):
    findings = []
    for i, block in enumerate(re.findall(r'\{([^}]*)\}', css)):
        c = _count(block)
        if c["devices"] > MAX_DEVICES:
            findings.append(f"block #{i+1}: {c['devices']} competing emphasis devices "
                            f"({c['borders']} border, {c['shadows']} shadow, {c['accent_colors']} colour, "
                            f"{c['weights']} weight) — subtract until it breaks (GUILD-48).")
        if c["radii"] > 1:
            findings.append(f"block #{i+1}: {c['radii']} different radii — one shape language.")
    return findings

def selftest():
    busy = ("{border:1px solid #B0421D; box-shadow:0 2px 8px #000; color:#455935; "
            "background:#C28A1C; font-weight:700; border-radius:4px}")
    busy = "x" + busy  # selector
    calm = "x{border:1px solid #3A332A; color:#F4ECE1; font-weight:600}"
    bz, cz = lint(busy), lint(calm)
    print("GUILD-48 subtraction pass — self-test")
    print(f"   over-decorated block: {len(bz)} finding(s)")
    for f in bz: print("     -", f)
    print(f"   restrained block:     {len(cz)} finding(s)")
    ok = len(bz) >= 1 and len(cz) == 0
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — over-decoration flagged; restrained component passes.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lint")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.lint:
        for f in lint(open(a.lint).read()) or ["no over-decoration findings"]: print(" ", f)
        return
    sys.exit("pass --lint <file> or --selftest")

if __name__ == "__main__":
    main()
