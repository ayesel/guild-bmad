#!/usr/bin/env python3
"""
ia-evidence-guard.py — GUILD-68 (T1): evidence-driven IA loop + empirical-persona guardrail.

Information architecture must be driven by EMPIRICAL evidence (card-sort, tree-test,
usability, analytics) — never by synthetic/AI-generated "users" presented as research.
Two guards over the spine:
  - Synthetic-user firewall: a fact sourced from a synthetic/simulated/AI persona is
    INADMISSIBLE as evidence (cannot back an insight/IA).
  - IA-loop: an IA conclusion must trace to >=1 admissible EMPIRICAL fact.

  python3 scripts/ia-evidence-guard.py --spine nuggets.json
  python3 scripts/ia-evidence-guard.py --selftest
"""
import re, sys, json, argparse

SYNTH = re.compile(r'\b(synthetic|simulated|ai[- ]persona|llm[- ]?generated|gpt|fictional user|hypothetical user|imagined)\b', re.I)
EMPIRICAL = re.compile(r'\b(card[- ]?sort|tree[- ]?test|usability|interview|analytics|survey|observation|a/b|field study|diary)\b', re.I)

def _facts_for(node_id, by_id, seen=None):
    seen = seen or set()
    if node_id in seen or node_id not in by_id: return []
    seen.add(node_id); n = by_id[node_id]; out = [n] if n.get("type") == "fact" else []
    for p in n.get("derived_from", []): out += _facts_for(p, by_id, seen)
    return out

def guard(spine):
    by_id = {n["id"]: n for n in spine}
    findings = []
    for n in spine:
        blob = f"{n.get('citation','')} {n.get('content','')}"
        if n.get("type") == "fact" and SYNTH.search(blob):
            findings.append(f"{n['id']}: synthetic-user source — INADMISSIBLE as evidence (no synthetic-user-as-research)")
        if n.get("type") == "conclusion":
            facts = _facts_for(n["id"], by_id)
            admissible = [f for f in facts if not SYNTH.search(f"{f.get('citation','')} {f.get('content','')}")]
            empirical = [f for f in admissible if EMPIRICAL.search(f"{f.get('citation','')} {f.get('content','')}")]
            if facts and not empirical:
                findings.append(f"{n['id']}: IA conclusion not backed by any empirical fact "
                                f"(card-sort/tree-test/usability/analytics) — evidence-driven IA required")
    return findings

def selftest():
    spine = [
        {"id": "F1", "type": "fact", "content": "tree-test: 70% found settings", "citation": "tree-test#2"},
        {"id": "F2", "type": "fact", "content": "synthetic persona 'Sam' would prefer tabs", "citation": "ai-persona"},
        {"id": "I1", "type": "insight", "content": "nav grouping works", "derived_from": ["F1"]},
        {"id": "C1", "type": "conclusion", "content": "ship the tree", "derived_from": ["I1"]},        # empirical-backed
        {"id": "I2", "type": "insight", "content": "tabs preferred", "derived_from": ["F2"]},
        {"id": "C2", "type": "conclusion", "content": "use tabs", "derived_from": ["I2"]},             # only synthetic
    ]
    f = guard(spine)
    print("GUILD-68 IA evidence guard — self-test")
    for x in f: print("   ✗", x)
    ids = " ".join(f)
    ok = ("F2: synthetic-user source" in ids and "C2: IA conclusion not backed" in ids
          and "C1" not in ids and "F1" not in ids)
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — empirical fact + its conclusion pass; synthetic-user fact inadmissible; synthetic-only IA conclusion blocked.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spine"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.spine:
        f = guard(json.load(open(a.spine)))
        for x in f: print(" ✗", x)
        print("IA evidence OK" if not f else f"{len(f)} finding(s)"); sys.exit(0 if not f else 1)
    sys.exit("pass --spine <f> or --selftest")

if __name__ == "__main__":
    main()
