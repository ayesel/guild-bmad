#!/usr/bin/env python3
"""
type-conditional.py — GUILD-45 (V-B): size-conditional type.

Junior work applies one global line-height + letter-spacing to every size. Senior
craft makes them SIZE-CONDITIONAL (optical sizing): as size grows, leading TIGHTENS
and tracking goes NEGATIVE; small text gets looser leading + slightly positive
tracking. Cheapest "looks senior" win (SYNTHESIS-v3 layer 2).

Reads the font-size scale from docs/guild/tokens.dtcg.json and emits the conditional
leading/tracking per step; also LINTS a stylesheet for flat (same line-height across
many sizes) type.

  python3 scripts/type-conditional.py            # emit the conditional type map (CSS)
  python3 scripts/type-conditional.py --lint <f> # flag flat/global type
  python3 scripts/type-conditional.py --selftest
"""
import os, re, sys, json, argparse

ROOT = os.getcwd()
DTCG = os.path.join(ROOT, "docs", "guild", "tokens.dtcg.json")
OUT = os.path.join(ROOT, "docs", "guild", "exports", "type-conditional.css")

def _px(val):
    m = re.search(r'([\d.]+)\s*(rem|px|em)?', str(val))
    if not m: return None
    n = float(m.group(1)); unit = m.group(2) or "rem"
    return n * 16 if unit in ("rem", "em") else n

def scale_from_dtcg():
    try: d = json.load(open(DTCG))
    except FileNotFoundError: return {}
    fs = d.get("fontSize", {})
    out = {}
    for name, tok in fs.items():
        px = _px(tok.get("$value") if isinstance(tok, dict) else tok)
        if px: out[name] = px
    return out

def conditional(sizes):
    """Senior rules: leading tightens + tracking goes negative as size grows."""
    if not sizes: return []
    pxs = sorted(set(sizes.values()))
    lo, hi = pxs[0], pxs[-1]
    rng = (hi - lo) or 1
    rows = []
    for name, px in sorted(sizes.items(), key=lambda kv: kv[1]):
        t = (px - lo) / rng                      # 0 (smallest) .. 1 (largest)
        leading = round(1.6 - 0.55 * t, 3)        # 1.6 small -> ~1.05 display
        tracking = round(0.012 - 0.035 * t, 4)    # +0.012em small -> -0.023em display
        rows.append({"name": name, "px": round(px, 1), "line_height": leading,
                     "letter_spacing_em": tracking})
    return rows

def to_css(rows):
    out = ["/* GENERATED — size-conditional type (GUILD-45). leading tightens + tracking",
           "   goes negative as size grows. Do not apply one global line-height. */"]
    for r in rows:
        out.append(f".type-{r['name']} {{ font-size: {r['px']/16:.4g}rem; "
                   f"line-height: {r['line_height']}; letter-spacing: {r['letter_spacing_em']}em; }}")
    return "\n".join(out) + "\n"

def lint(css):
    """Flag flat type: the same line-height paired with >1 distinct font-size."""
    findings = []
    blocks = re.findall(r'\{([^}]*)\}', css)
    lh_to_sizes = {}
    for b in blocks:
        fs = re.search(r'font-size\s*:\s*([\d.]+\s*(?:rem|px|em))', b)
        lh = re.search(r'line-height\s*:\s*([\d.]+)', b)
        if fs and lh:
            lh_to_sizes.setdefault(lh.group(1), set()).add(fs.group(1).replace(" ", ""))
    for lh, ss in lh_to_sizes.items():
        if len(ss) > 1:
            findings.append(f"flat line-height {lh} across {len(ss)} sizes {sorted(ss)} "
                            f"— type is not size-conditional (GUILD-45)")
    return findings

def selftest():
    sizes = {"xs": 12, "sm": 14, "base": 16, "lg": 22, "xl": 28, "display": 40}
    rows = conditional(sizes)
    lhs = [r["line_height"] for r in rows]
    trs = [r["letter_spacing_em"] for r in rows]
    mono_lh = all(lhs[i] > lhs[i+1] for i in range(len(lhs)-1))     # leading tightens
    mono_tr = all(trs[i] > trs[i+1] for i in range(len(trs)-1))     # tracking goes negative
    flat = lint("h1{font-size:2rem;line-height:1.5} p{font-size:1rem;line-height:1.5}")
    cond = lint(to_css(rows))
    print("GUILD-45 size-conditional type — self-test")
    for r in rows: print(f"   {r['name']:7} {r['px']:>5}px  lh {r['line_height']}  tracking {r['letter_spacing_em']}em")
    print(f"   leading tightens with size: {mono_lh} | tracking negatives with size: {mono_tr}")
    print(f"   lint flat stylesheet: {len(flat)} finding(s) | lint conditional output: {len(cond)} finding(s)")
    ok = mono_lh and mono_tr and len(flat) == 1 and len(cond) == 0
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — leading+tracking are size-conditional; lint catches flat type.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lint")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.lint:
        for f in lint(open(a.lint).read()) or ["no flat-type findings"]: print(" ", f)
        return
    rows = conditional(scale_from_dtcg())
    if not rows: sys.exit("no fontSize tokens in tokens.dtcg.json")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(to_css(rows))
    print(f"wrote {OUT} ({len(rows)} size-conditional steps)")

if __name__ == "__main__":
    main()
