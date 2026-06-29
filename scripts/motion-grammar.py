#!/usr/bin/env python3
"""
motion-grammar.py — GUILD-49 (V-C): validate motion against the grammar.

LLMs pick easing badly (bouncy springs on everyday UI, linear fades). The motion
grammar (docs/guild/motion.yaml) maps each interaction to a required (easing,
duration); generation is constrained to that vocabulary. This validates a proposed
motion choice and flags off-grammar easing/duration or spring-outside-celebrate.

  python3 scripts/motion-grammar.py --check enter:in       # off-grammar -> flagged
  python3 scripts/motion-grammar.py --selftest
"""
import os, sys, argparse
import yaml

MOTION = os.path.join(os.getcwd(), "docs", "guild", "motion.yaml")

def load():
    return yaml.safe_load(open(MOTION)) or {}

def check(interaction, easing, m=None):
    m = m or load()
    g = (m.get("grammar") or {}).get(interaction)
    easings = m.get("easings") or {}
    if easing not in easings:
        return False, f"easing '{easing}' is off-vocabulary — use one of {list(easings)}"
    if not g:
        return False, f"unknown interaction '{interaction}' — grammar covers {list((m.get('grammar') or {}))}"
    if easing == "soft-spring" and interaction != "celebrate":
        return False, "spring (soft-spring) is allowed only for 'celebrate' — no bounce on everyday UI"
    if easing != g["easing"]:
        return False, f"{interaction} should use '{g['easing']}', not '{easing}' (off-grammar)"
    return True, f"{interaction} -> {g['easing']} / {g['duration']} ✓"

def selftest():
    m = load()
    cases = [(("enter", "out"), True), (("enter", "in"), False),
             (("press", "soft-spring"), False), (("celebrate", "soft-spring"), True),
             (("hover", "wobble"), False)]
    print("GUILD-49 motion grammar — self-test")
    results = []
    for (it, ea), want in cases:
        ok, msg = check(it, ea, m)
        results.append(ok == want)
        print(f"   {it}:{ea} -> {'OK' if ok else 'FLAG'} (want {'OK' if want else 'FLAG'})  {msg}")
    allok = all(results) and bool(m.get("grammar"))
    print(f"\n{'✅ PASS' if allok else '❌ FAIL'} — grammar accepts on-spec motion, flags off-grammar + misplaced spring.")
    sys.exit(0 if allok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", help="interaction:easing")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.check and ":" in a.check:
        it, ea = a.check.split(":", 1)
        ok, msg = check(it, ea)
        print(("OK: " if ok else "FLAG: ") + msg); sys.exit(0 if ok else 1)
    sys.exit("pass --check interaction:easing or --selftest")

if __name__ == "__main__":
    main()
