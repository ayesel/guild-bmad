#!/usr/bin/env python3
"""
state-motion-req.py — GUILD-51 (V-C): states + motion as a generation REQUIREMENT.

An interactive element isn't done until it declares its states (hover / focus /
active / disabled) AND the motion between them. Generators ship the resting state
and forget the rest. This lints for interactive elements missing required states or
their transition — a generation requirement, not a nice-to-have.

  python3 scripts/state-motion-req.py --screen <file>
  python3 scripts/state-motion-req.py --selftest
"""
import re, sys, argparse

INTERACTIVE = re.compile(r'(<button|<a[\s>]|<input|<select|<textarea|role=["\']button|\.btn\b)', re.I)

def lint(src):
    if not INTERACTIVE.search(src):
        return []   # nothing interactive to require states of
    findings = []
    if not re.search(r':focus(-visible)?', src):
        findings.append("interactive elements present but no :focus / :focus-visible (keyboard a11y) — required state missing")
    if not re.search(r':hover', src):
        findings.append("no :hover state on interactive elements")
    if not re.search(r':disabled|\[disabled\]|:disabled', src):
        findings.append("no disabled state defined")
    if not re.search(r'transition\s*:|animation\s*:', src):
        findings.append("no transition between states (motion is part of the component)")
    return findings

def selftest():
    incomplete = "<button class=btn>Go</button><style>.btn{background:#B0421D}</style>"
    complete = ("<button class=btn>Go</button><style>"
                ".btn{background:#B0421D;transition:background 140ms ease}"
                ".btn:hover{background:#8C3417}.btn:focus-visible{outline:2px solid #E06E45}"
                ".btn:disabled{opacity:.5}</style>")
    ic, co = lint(incomplete), lint(complete)
    print("GUILD-51 state+motion requirement — self-test")
    print(f"   incomplete button: {len(ic)} finding(s)")
    for f in ic: print("     -", f)
    print(f"   complete button:   {len(co)} finding(s)")
    ok = len(ic) == 4 and len(co) == 0
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — missing states+motion flagged; fully-stated component passes.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--screen")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.screen:
        for f in lint(open(a.screen).read()) or ["all required states + motion present"]: print(" ", f)
        return
    sys.exit("pass --screen <file> or --selftest")

if __name__ == "__main__":
    main()
