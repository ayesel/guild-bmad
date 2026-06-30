#!/usr/bin/env python3
"""
cd-onboarding-gate.py — GUILD-29: onboarding foundation gate (catch bad tokens at source).

When Claude Design auto-builds a design SYSTEM, audit its semantic colour pairings for
WCAG contrast BEFORE it propagates into apps (and before any seed-PUSH back, GUILD-32) —
so a broken token is caught at the source, not in every downstream screen. Complements
the handoff gate (GUILD-28, pre-build); this is pre-PROPAGATION (at onboarding).

  python3 scripts/cd-onboarding-gate.py            # audit docs/guild/design-system.yaml
  python3 scripts/cd-onboarding-gate.py --selftest
"""
import os, sys, argparse
import yaml

DS = os.path.join(os.getcwd(), "docs", "guild", "design-system.yaml")
AA, AA_LARGE = 4.5, 3.0

def _lin(c):
    c /= 255; return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
def _L(h):
    h = h.lstrip("#"); return 0.2126*_lin(int(h[0:2],16))+0.7152*_lin(int(h[2:4],16))+0.0722*_lin(int(h[4:6],16))
def contrast(a, b):
    la, lb = _L(a), _L(b); hi, lo = max(la, lb), min(la, lb); return (hi+0.05)/(lo+0.05)

WHITE, INK, LINEN = "#FFFFFF", "#211C17", "#FBF7F1"

def standard_pairings(pal):
    """The semantic pairings a CD-built system must get right (text-on-surface, text-on-accent)."""
    g = lambda k, d=None: (pal.get(k) or {}).get("hex", d)
    P = []
    P.append({"role": "body text on bg", "fg": g("ink", INK), "bg": g("linen", LINEN)})
    # dark accents take white text; the light 'warning' takes dark (ink) text
    for role, key, on in [("on-primary", "primary", WHITE), ("on-secondary", "secondary", WHITE),
                          ("on-danger", "danger", WHITE), ("on-info", "info", WHITE),
                          ("on-warning", "warning", INK)]:
        c = g(key)
        if c: P.append({"role": role, "fg": on, "bg": c})
    return P

def audit(pairings):
    fails = []
    for p in pairings:
        thr = AA_LARGE if p.get("large") else AA
        c = contrast(p["fg"], p["bg"])
        if c < thr:
            fails.append(f"{p['role']}: {p['fg']} on {p['bg']} = {c:.2f}:1 < {thr}")
    return fails

def selftest():
    pal = {"primary": {"hex": "#B0421D"}, "secondary": {"hex": "#455935"}, "warning": {"hex": "#C28A1C"},
           "danger": {"hex": "#B23423"}, "info": {"hex": "#3A6079"}, "ink": {"hex": "#211C17"}, "linen": {"hex": "#FBF7F1"}}
    clean = standard_pairings(pal)
    # a bad CD build: white text on the light 'warning' (should be dark) — catch at source
    bad = clean[:-1] + [{"role": "on-warning", "fg": WHITE, "bg": "#C28A1C"}]
    cf, bf = audit(clean), audit(bad)
    print("GUILD-29 CD onboarding gate — self-test")
    print(f"   clean system: {len(cf)} contrast fail(s) -> {'GO' if not cf else 'NO-GO'}")
    print(f"   bad system (white-on-light-warning): {len(bf)} fail(s) -> {'GO' if not bf else 'NO-GO'}")
    for x in bf: print("     ✗", x)
    ok = len(cf) == 0 and len(bf) >= 1 and any("on-warning" in x for x in bf)
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — clean CD system passes; a bad semantic pairing is blocked BEFORE it propagates.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    try: pal = (yaml.safe_load(open(DS)) or {}).get("palette") or {}
    except FileNotFoundError: sys.exit(f"missing {DS}")
    fails = audit(standard_pairings(pal))
    v = "GO" if not fails else "NO-GO"
    print(f"[{v}] CD onboarding contrast audit — {len(fails)} failing pairing(s)")
    for x in fails: print("  ✗", x)
    sys.exit(0 if v == "GO" else 1)

if __name__ == "__main__":
    main()
