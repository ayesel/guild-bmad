#!/usr/bin/env python3
"""
verification-gate.py — GUILD-64 (T1): factored verification + sycophancy firewall.

Anti-ResearchSlop. Over the spine's FACT nuggets (GUILD-63), runs factored checks:
  - CitationAgent — every fact has a real (non-placeholder) citation.
  - Sycophancy firewall — opinion-as-fact ("we believe / I think / users will love")
    and stakeholder-opinion-as-evidence are stripped (flagged, not counted).
  - qual/quant — a quantitative claim ("most / 80% / increased") must carry a number.
  - blind CoVe — each fact must be marked verified (chain-of-verification done),
    else flagged unverified.

  python3 scripts/verification-gate.py --spine nuggets.json
  python3 scripts/verification-gate.py --selftest
"""
import re, sys, json, argparse

PLACEHOLDER = {"", "tbd", "todo", "n/a", "none", "?"}
OPINION = re.compile(r'\b(i think|we believe|i feel|in my opinion|should|probably|users? will love|obviously)\b', re.I)
STAKEHOLDER = re.compile(r'\b(stakeholder|exec|the ceo|pm said|sales said|the client wants)\b', re.I)
QUANT = re.compile(r'\b(most|majority|many|few|increased?|decreased?|more|less|%|percent)\b', re.I)
HASNUM = re.compile(r'\d')

def gate(nuggets):
    findings = []
    for n in nuggets:
        if n.get("type") != "fact": continue
        i, c = n["id"], n.get("content", "")
        cite = str(n.get("citation", "")).strip().lower()
        if cite in PLACEHOLDER:
            findings.append(f"{i}: missing/placeholder citation")
        if STAKEHOLDER.search(cite) or STAKEHOLDER.search(c):
            findings.append(f"{i}: stakeholder opinion presented as fact — strip (not evidence)")
        if OPINION.search(c):
            findings.append(f"{i}: opinion language ('{OPINION.search(c).group(0)}') — fact must be observation")
        if QUANT.search(c) and not HASNUM.search(c):
            findings.append(f"{i}: quantitative claim without a number — qual/quant mismatch")
        if not n.get("verified"):
            findings.append(f"{i}: not verified (blind chain-of-verification not run)")
    return findings

def selftest():
    nuggets = [
        {"id": "F1", "type": "fact", "content": "4 of 5 participants missed the filter", "citation": "usability-test#3", "verified": True},
        {"id": "F2", "type": "fact", "content": "we believe users will love the redesign", "citation": "pm said", "verified": True},
        {"id": "F3", "type": "fact", "content": "most users churn in week 1", "citation": "analytics", "verified": True},
        {"id": "F4", "type": "fact", "content": "signup takes 3 steps", "citation": "tbd"},
    ]
    f = gate(nuggets)
    print("GUILD-64 verification + sycophancy firewall — self-test")
    for x in f: print("   ✗", x)
    ids = " ".join(f)
    ok = ("F1" not in ids                      # clean fact passes
          and "F2: stakeholder" in ids and "opinion language" in ids   # opinion+stakeholder caught
          and "F3: quantitative claim without a number" in ids          # unquantified caught
          and "F4: missing/placeholder citation" in ids and "F4: not verified" in ids)
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — cited+verified fact passes; opinion/stakeholder/unquantified/uncited+unverified flagged.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spine"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.spine:
        f = gate(json.load(open(a.spine)))
        for x in f: print(" ✗", x)
        print("verification OK" if not f else f"{len(f)} finding(s)"); sys.exit(0 if not f else 1)
    sys.exit("pass --spine <file> or --selftest")

if __name__ == "__main__":
    main()
