#!/usr/bin/env python3
"""
pareto-select.py — GUILD-41: two-axis (quality × novelty) Pareto selection.

Anti-blandness. The single-scalar blend collapsed quality and novelty into one
number, so the median-safe candidate always won and the bold one got averaged
away (Goodhart). Instead score the two axes INDEPENDENTLY and surface the Pareto
front: a balanced recommendation + the bold (high-novelty) non-dominated
alternatives — never one scalar (deepdive-3 R4 / SYNTHESIS-v3).

  quality axis  <- the diverse jury (GUILD-40 Bradley-Terry strength), normalized
  novelty axis  <- the novelty engine (VS distinctiveness / morphology coverage)

  python3 scripts/pareto-select.py --candidates cands.json   # [{id,quality,novelty},...]
  python3 scripts/pareto-select.py --selftest
"""
import sys, json, argparse

DISTINCTIVE_WEIGHT = 0.6   # weight novelty UP when picking the single rec (anti-blandness)

def pareto_front(cands):
    """Non-dominated set on (quality, novelty). c is dominated if some o is >= on both
    and strictly > on at least one."""
    front = []
    for c in cands:
        dom = any(o is not c and o["quality"] >= c["quality"] and o["novelty"] >= c["novelty"]
                  and (o["quality"] > c["quality"] or o["novelty"] > c["novelty"]) for o in cands)
        if not dom:
            front.append(c)
    return front

def select(cands, w=DISTINCTIVE_WEIGHT):
    front = pareto_front(cands)
    # single REC: balanced but distinctive-weighted (never just argmax-quality)
    rec = max(front, key=lambda c: c["quality"] + w * c["novelty"])
    # bold alternative: highest-novelty front member that isn't the rec
    bold_candidates = [c for c in front if c["id"] != rec["id"]]
    bold = max(bold_candidates, key=lambda c: c["novelty"]) if bold_candidates else None
    alternatives = [c for c in front if c["id"] != rec["id"]]
    dominated = [c["id"] for c in cands if c not in front]
    return {"front": [c["id"] for c in front], "rec": rec["id"],
            "bold_alternative": bold["id"] if bold else None,
            "alternatives": [c["id"] for c in alternatives], "dominated_out": dominated,
            "note": "two axes never collapsed to one scalar; bold distinct option preserved"}

def selftest():
    cands = [
        {"id": "bland",    "quality": 0.90, "novelty": 0.10},  # median-safe; old scalar winner
        {"id": "balanced", "quality": 0.80, "novelty": 0.70},
        {"id": "bold",     "quality": 0.60, "novelty": 0.95},  # distinctive — must survive
        {"id": "weak",     "quality": 0.50, "novelty": 0.40},  # dominated by balanced
    ]
    r = select(cands)
    print("GUILD-41 two-axis Pareto selection — self-test")
    print(json.dumps(r, indent=2))
    ok = (set(r["front"]) == {"bland", "balanced", "bold"}   # dominated 'weak' excluded
          and "weak" in r["dominated_out"]
          and r["rec"] == "balanced"                         # not the bland argmax-quality
          and r["bold_alternative"] == "bold")               # distinctive option preserved, not averaged away
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — Pareto front keeps the bold candidate; "
          f"rec is balanced (not the median-safe argmax-quality); dominated dropped; no single scalar.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.candidates:
        print(json.dumps(select(json.load(open(a.candidates))), indent=2)); return
    sys.exit("pass --candidates <file> or --selftest")

if __name__ == "__main__":
    main()
