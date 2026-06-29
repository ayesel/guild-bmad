#!/usr/bin/env python3
"""
judge-calibration.py — GUILD-44: score the jury against the owner golden-set.

The jury (GUILD-40) is only trustworthy if it agrees with the owner. This computes:
  - judge-vs-owner AGREEMENT on the calibration set (docs/guild/evals/calibration-set.yaml),
  - whether it clears accuracy_bar (below => jury is ADVISORY, may not gate),
  - the OFFLINE-ONLINE GAP meta-metric (jury/owner picks vs real-signal winners) —
    should shrink over time.

Inputs:
  calibration-set.yaml  : owner pairwise labels (+ optional online_winners)
  --jury <file>         : JSON {labelId: jury_pick} — the jury's pick per labelled pair
                          (from bradley-terry.py aggregate; pick = higher BT strength)

  python3 scripts/judge-calibration.py --jury jury-picks.json
  python3 scripts/judge-calibration.py --selftest
"""
import os, sys, json, argparse
import yaml

CAL = os.path.join(os.getcwd(), "docs", "guild", "evals", "calibration-set.yaml")

def load_cal(path=CAL):
    try: return yaml.safe_load(open(path)) or {}
    except FileNotFoundError: return {}

def score(cal, jury_picks):
    labels = cal.get("labels") or []
    bar = (cal.get("meta") or {}).get("accuracy_bar", 0.7)
    scored = [(l["id"], l["owner_pick"], jury_picks.get(l["id"]))
              for l in labels if l.get("id") in jury_picks]
    n = len(scored)
    agree = sum(1 for _, owner, j in scored if owner == j)
    agreement = round(agree / n, 3) if n else None

    # offline-online gap: of the real-signal winners, how many did the jury NOT prefer?
    online = cal.get("online_winners") or []
    gap = None
    if online:
        miss = sum(1 for o in online if jury_picks.get(o.get("id")) not in (None, o.get("winner")))
        gap = round(miss / len(online), 3)

    trusted = (agreement is not None and agreement >= bar)
    return {"labels_scored": n, "agreement": agreement, "accuracy_bar": bar,
            "jury_gates": trusted, "offline_online_gap": gap}

def report(r):
    print(f"  labels scored:        {r['labels_scored']}")
    print(f"  jury-owner agreement: {r['agreement']}  (bar {r['accuracy_bar']})")
    print(f"  jury may GATE:        {r['jury_gates']}  ({'gates' if r['jury_gates'] else 'ADVISORY only — owner ground truth'})")
    print(f"  offline-online gap:   {r['offline_online_gap']}  (should shrink over time)")

def selftest():
    # 5 synthetic owner labels; a jury that agrees on 4/5 -> 0.8 >= bar 0.7 => gates.
    cal = {"meta": {"accuracy_bar": 0.7},
           "labels": [{"id": f"L{i}", "owner_pick": "A"} for i in range(1, 6)],
           "online_winners": [{"id": "L1", "winner": "A"}, {"id": "L2", "winner": "A"}]}
    jury = {"L1": "A", "L2": "A", "L3": "A", "L4": "A", "L5": "B"}  # 4/5 agree; online 2/2 match
    r = score(cal, jury)
    print("GUILD-44 judge-calibration — self-test")
    report(r)
    ok = (r["labels_scored"] == 5 and r["agreement"] == 0.8 and r["jury_gates"] is True
          and r["offline_online_gap"] == 0.0)
    # and a poorly-calibrated jury must NOT gate
    bad = score(cal, {"L1": "B", "L2": "B", "L3": "B", "L4": "A", "L5": "A"})  # 2/5 = 0.4
    ok = ok and bad["agreement"] == 0.4 and bad["jury_gates"] is False
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — agreement+gap computed; low agreement => jury advisory-only.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jury", help="JSON {labelId: jury_pick}")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    cal = load_cal()
    if not (cal.get("labels")):
        print("calibration set is empty — gather ~50-100 owner pairwise labels "
              "(docs/guild/evals/calibration-set.yaml). Jury runs ADVISORY-only until then.")
        return
    jury = json.load(open(a.jury)) if a.jury else {}
    report(score(cal, jury))

if __name__ == "__main__":
    main()
