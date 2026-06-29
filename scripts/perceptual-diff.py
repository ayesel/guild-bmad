#!/usr/bin/env python3
"""
perceptual-diff.py — GUILD-53 (V-D): diff triage + determinism + fix-loop.

A raw visual diff is noise until it's TRIAGED: which changed regions are the
INTENDED change (declared in the changeset) vs an unintended REGRESSION? This is
the deterministic triage + fix-loop layer that sits on top of a perceptual diff
(the pixel/structural diff itself is produced by the renderer/Playwright; here we
classify its output reproducibly).

  python3 scripts/perceptual-diff.py --diff regions.json --changeset cs.json
  python3 scripts/perceptual-diff.py --selftest
diff regions: [{region, delta}]  changeset (declared intended): [region,...]
"""
import sys, json, argparse

REGRESSION_DELTA = 0.02   # below this, treat as rendering noise (determinism band)

def triage(regions, changeset):
    declared = set(changeset)
    intended, regressions, noise = [], [], []
    for r in sorted(regions, key=lambda x: x["region"]):     # sorted => deterministic
        if r["delta"] < REGRESSION_DELTA:
            noise.append(r["region"])
        elif r["region"] in declared:
            intended.append(r["region"])
        else:
            regressions.append(r["region"])
    verdict = "NO-GO" if regressions else "GO"
    fix_loop = [{"region": rg, "action": "regenerate region to match baseline"} for rg in regressions]
    return {"verdict": verdict, "intended": intended, "regressions": regressions,
            "noise": noise, "fix_loop": fix_loop}

def selftest():
    regions = [{"region": "header", "delta": 0.30}, {"region": "footer", "delta": 0.25},
               {"region": "sidebar", "delta": 0.005}]
    changeset = ["header"]   # only the header change was intended
    r1 = triage(regions, changeset)
    r2 = triage(regions, changeset)   # determinism: identical input -> identical output
    print("GUILD-53 perceptual-diff triage — self-test")
    print(f"   {json.dumps({k: r1[k] for k in ('verdict','intended','regressions','noise')})}")
    ok = (r1["verdict"] == "NO-GO" and r1["intended"] == ["header"]
          and r1["regressions"] == ["footer"] and r1["noise"] == ["sidebar"]
          and r1 == r2 and len(r1["fix_loop"]) == 1)
    print(f"   deterministic (run1==run2): {r1 == r2}")
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — intended change passes, undeclared regression blocks + queues a fix; noise ignored; deterministic.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diff"); ap.add_argument("--changeset")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.diff and a.changeset:
        r = triage(json.load(open(a.diff)), json.load(open(a.changeset)))
        print(json.dumps(r, indent=2)); sys.exit(0 if r["verdict"] == "GO" else 1)
    sys.exit("pass --diff <f> --changeset <f> or --selftest")

if __name__ == "__main__":
    main()
