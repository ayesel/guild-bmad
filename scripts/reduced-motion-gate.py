#!/usr/bin/env python3
"""
reduced-motion-gate.py — GUILD-50 (V-C): reduced-motion HARD gate.

Any UI with transitions/animations MUST honor prefers-reduced-motion (vestibular
accessibility). This is a HARD gate: a stylesheet that animates but has no
`@media (prefers-reduced-motion: reduce)` block → NO-GO.

  python3 scripts/reduced-motion-gate.py --screen <file>   # GO / NO-GO (exit 0/1)
  python3 scripts/reduced-motion-gate.py --selftest
"""
import re, sys, argparse

ANIM = re.compile(r'(transition\s*:|animation\s*:|@keyframes)', re.I)
GUARD = re.compile(r'@media[^{]*prefers-reduced-motion\s*:\s*reduce', re.I)

def gate(css):
    animates = bool(ANIM.search(css))
    guarded = bool(GUARD.search(css))
    if animates and not guarded:
        return "NO-GO", "animates (transition/animation/@keyframes) but no @media (prefers-reduced-motion: reduce) block"
    return "GO", ("static, no motion" if not animates else "motion guarded by prefers-reduced-motion")

def selftest():
    bad = ".x{transition:transform 220ms ease}"
    good = (".x{transition:transform 220ms ease}"
            "@media (prefers-reduced-motion: reduce){.x{transition:none}}")
    static = ".x{color:#fff}"
    rb, rg, rs = gate(bad)[0], gate(good)[0], gate(static)[0]
    print("GUILD-50 reduced-motion hard gate — self-test")
    print(f"   animated, unguarded: {rb}   guarded: {rg}   static: {rs}")
    ok = rb == "NO-GO" and rg == "GO" and rs == "GO"
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — unguarded motion blocked; guarded + static pass.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--screen")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.screen:
        v, why = gate(open(a.screen).read())
        print(f"[{v}] {why}"); sys.exit(0 if v == "GO" else 1)
    sys.exit("pass --screen <file> or --selftest")

if __name__ == "__main__":
    main()
