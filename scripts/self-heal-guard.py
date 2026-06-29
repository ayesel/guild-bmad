#!/usr/bin/env python3
"""
self-heal-guard.py — GUILD-43: keep the self-heal loop externally grounded.

Audit fix for GUILD-2: a naive self-heal that repairs on introspection ("looks
better") loops candidates back to the mean. This guard enforces two rules from
docs/guild/self-heal.yaml:
  1. EXTERNAL SIGNAL REQUIRED — every repair must cite a recognized objective trigger
     (wcag_fail, token_lint, fidelity_diff, broken_test, ...). No signal => REJECTED.
  2. SUBJECTIVE CAP — at most ONE subjective pass; objective rounds up to the
     definition-of-done max_iterations; then escalate to the owner.

  python3 scripts/self-heal-guard.py --selftest
  (library: allowed(repair) -> (ok, reason); plan_round(history, repair) -> (ok, reason))
"""
import os, sys, argparse
import yaml

ROOT = os.getcwd()
def _load(p, default=None):
    try: return yaml.safe_load(open(os.path.join(ROOT, "docs", "guild", p))) or {}
    except FileNotFoundError: return default if default is not None else {}

def config():
    cfg = _load("self-heal.yaml")
    signals = set(cfg.get("external_signals") or [])
    dod = _load("definition-of-done.yaml")
    obj_cap = ((dod.get("hard_stops") or {}).get("max_iterations")) or 5
    subj_cap = ((cfg.get("loop_caps") or {}).get("subjective_rounds"))
    subj_cap = 1 if subj_cap is None else subj_cap
    return signals, obj_cap, subj_cap

def allowed(repair, signals=None):
    """repair: {signal, subjective?}. Must cite a recognized external signal."""
    signals = signals if signals is not None else config()[0]
    sig = repair.get("signal")
    if sig not in signals:
        return False, f"no recognized external signal (got {sig!r}) — introspective repair REJECTED"
    return True, f"grounded in external signal: {sig}"

def plan_round(history, repair):
    """history: list of prior repairs already applied this loop. Enforce caps."""
    signals, obj_cap, subj_cap = config()
    ok, reason = allowed(repair, signals)
    if not ok:
        return False, reason
    subj_done = sum(1 for h in history if h.get("subjective"))
    obj_done = sum(1 for h in history if not h.get("subjective"))
    if repair.get("subjective"):
        if subj_done >= subj_cap:
            return False, f"subjective cap reached ({subj_cap}) — escalate to owner, do not self-polish"
    else:
        if obj_done >= obj_cap:
            return False, f"objective rounds hit DoD max_iterations ({obj_cap}) — hard stop"
    return True, reason

def selftest():
    signals, obj_cap, subj_cap = config()
    print("GUILD-43 self-heal-guard — self-test")
    print(f"  external signals: {len(signals)}  objective_cap(DoD): {obj_cap}  subjective_cap: {subj_cap}")
    checks = []
    # 1 — external-signal repair allowed
    checks.append(("wcag repair allowed", allowed({"signal": "wcag_fail"})[0] is True))
    # 2 — introspective repair rejected
    checks.append(("introspective rejected", allowed({"signal": "looks_better"})[0] is False))
    checks.append(("no-signal rejected", allowed({})[0] is False))
    # 3 — second subjective round blocked (cap 1)
    hist = [{"signal": "jury_below_calibration", "subjective": True}]
    checks.append(("2nd subjective blocked", plan_round(hist, {"signal": "jury_below_calibration", "subjective": True})[0] is False))
    # 4 — objective rounds allowed up to DoD cap, blocked after
    objhist = [{"signal": "wcag_fail"} for _ in range(obj_cap)]
    checks.append(("objective over-cap blocked", plan_round(objhist, {"signal": "wcag_fail"})[0] is False))
    checks.append(("objective under-cap allowed", plan_round(objhist[:-1], {"signal": "wcag_fail"})[0] is True))
    for name, ok in checks:
        print(f"   {'✓' if ok else '✗'} {name}")
    allok = all(ok for _, ok in checks)
    print(f"\n{'✅ PASS' if allok else '❌ FAIL'} — repairs require an external signal; "
          f"subjective passes capped at {subj_cap}; objective rounds bounded by DoD.")
    sys.exit(0 if allok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    sys.exit("pass --selftest")

if __name__ == "__main__":
    main()
