#!/usr/bin/env python3
"""
regression-firewall.py — GUILD-57 (V-E): golden-set regression firewall.

A change may improve the headline yet quietly REGRESS a protected dimension. The
firewall blocks any candidate that scores worse than the golden baseline on a
protected dim (WCAG, token fidelity, state coverage, task success) — "no quality
regression vs current." Pairs with the Do/Don't gallery (docs/guild/exemplars/
do-dont.yaml).

  python3 scripts/regression-firewall.py --candidate c.json --golden g.json
  python3 scripts/regression-firewall.py --selftest
scores: {dim: number} on the protected dims; higher = better.
"""
import sys, json, argparse

PROTECTED = ["wcag_contrast", "token_fidelity", "state_coverage", "task_success"]
EPS = 1e-9

def firewall(candidate, golden):
    regressions = []
    for dim in PROTECTED:
        if dim in golden and dim in candidate and candidate[dim] + EPS < golden[dim]:
            regressions.append(f"{dim}: {candidate[dim]} < golden {golden[dim]}")
    return {"verdict": "NO-GO" if regressions else "GO", "regressions": regressions}

def selftest():
    golden = {"wcag_contrast": 4.6, "token_fidelity": 0.90, "state_coverage": 1.0, "task_success": 0.8}
    good = {"wcag_contrast": 5.1, "token_fidelity": 0.95, "state_coverage": 1.0, "task_success": 0.82}
    bad = {"wcag_contrast": 3.2, "token_fidelity": 0.97, "state_coverage": 1.0, "task_success": 0.9}  # contrast regressed
    rg, rb = firewall(good, golden), firewall(bad, golden)
    print("GUILD-57 regression firewall — self-test")
    print(f"   improved candidate: {rg['verdict']}")
    print(f"   regressed contrast: {rb['verdict']}  {rb['regressions']}")
    ok = rg["verdict"] == "GO" and rb["verdict"] == "NO-GO" and any("wcag_contrast" in r for r in rb["regressions"])
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — improvement passes; a protected-dim regression is blocked even when the headline improves.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate"); ap.add_argument("--golden")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.candidate and a.golden:
        r = firewall(json.load(open(a.candidate)), json.load(open(a.golden)))
        print(json.dumps(r, indent=2)); sys.exit(0 if r["verdict"] == "GO" else 1)
    sys.exit("pass --candidate <f> --golden <f> or --selftest")

if __name__ == "__main__":
    main()
