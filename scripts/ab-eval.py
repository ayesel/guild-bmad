#!/usr/bin/env python3
"""
ab-eval.py — GUILD-42: blind A/B eval — MERGE vs SELECT.

Settles the raid-restructure question with DATA, not opinion (the synthesis says
3-model creative-MERGE regresses to the mean; diverge-then-SELECT should win — but
prove it). For real Nourish screens generated two ways:
  arm MERGE  = current 3-model creative-merge raid output
  arm SELECT = diverge (GUILD-21 / GPT-5.5 lane) -> jury tournament (GUILD-40/41)
each paired screen is judged BLIND (anonymized, order-shuffled) by the new diverse
jury AND by a human (owner) pick. Report win-rates + agreement + a recommendation.
DOES NOT rescope raids — the DATA decides that.

  python3 scripts/ab-eval.py --verdicts verdicts.json   # [{pair, jury_pick, owner_pick}]
  python3 scripts/ab-eval.py --selftest
verdict pick values are "merge" | "select" (already de-blinded for scoring).
"""
import sys, json, argparse

MARGIN = 0.10   # win-rate must beat 50% by this margin to be a real signal

def evaluate(verdicts):
    n = len(verdicts)
    jury_sel = sum(1 for v in verdicts if v.get("jury_pick") == "select")
    owner_sel = sum(1 for v in verdicts if v.get("owner_pick") == "select")
    agree = sum(1 for v in verdicts if v.get("jury_pick") == v.get("owner_pick"))
    jr = jury_sel / n if n else 0
    orr = owner_sel / n if n else 0
    ag = agree / n if n else 0
    # recommendation: BOTH jury and owner must favor select beyond the margin
    if jr >= 0.5 + MARGIN and orr >= 0.5 + MARGIN:
        rec = ("RESTRUCTURE: data supports diverge-then-SELECT over creative-MERGE. "
               "Rescope the 3-model Mage/Warlock raids: keep raids for QA/research "
               "coverage, stop using them to MERGE creative artifacts.")
    elif orr <= 0.5 - MARGIN:
        rec = "KEEP MERGE: owner preferred merged output — do NOT restructure raids."
    else:
        rec = "INCONCLUSIVE: gather more paired screens before deciding the raid restructure."
    return {"pairs": n, "jury_select_winrate": round(jr, 3), "owner_select_winrate": round(orr, 3),
            "jury_owner_agreement": round(ag, 3), "recommendation": rec}

def report(r):
    print(f"  paired screens:        {r['pairs']}")
    print(f"  SELECT win-rate (jury):  {r['jury_select_winrate']}")
    print(f"  SELECT win-rate (owner): {r['owner_select_winrate']}")
    print(f"  jury-owner agreement:    {r['jury_owner_agreement']}")
    print(f"  → {r['recommendation']}")

def selftest():
    # synthetic: select wins 7/10 by jury, 8/10 by owner, high agreement -> RESTRUCTURE
    v = ([{"pair": f"P{i}", "jury_pick": "select", "owner_pick": "select"} for i in range(7)]
         + [{"pair": "P7", "jury_pick": "merge", "owner_pick": "select"}]
         + [{"pair": "P8", "jury_pick": "merge", "owner_pick": "merge"}]
         + [{"pair": "P9", "jury_pick": "select", "owner_pick": "merge"}])
    r = evaluate(v)
    print("GUILD-42 blind A/B eval (merge vs select) — self-test")
    report(r)
    ok = (r["pairs"] == 10 and r["jury_select_winrate"] == 0.8 and r["owner_select_winrate"] == 0.8
          and r["recommendation"].startswith("RESTRUCTURE"))
    # a merge-favored set must NOT recommend restructure
    vm = [{"pair": f"M{i}", "jury_pick": "merge", "owner_pick": "merge"} for i in range(8)] \
         + [{"pair": "M8", "jury_pick": "select", "owner_pick": "select"} for _ in range(2)]
    rm = evaluate(vm)
    ok = ok and rm["recommendation"].startswith("KEEP MERGE")
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — harness computes win-rates + agreement; "
          f"select-favored → RESTRUCTURE, merge-favored → KEEP MERGE. (Real Nourish run "
          f"needs both arms generated + the owner's blind pick.)")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verdicts")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.verdicts:
        report(evaluate(json.load(open(a.verdicts)))); return
    sys.exit("pass --verdicts <file> or --selftest")

if __name__ == "__main__":
    main()
