#!/usr/bin/env python3
"""
confidence-gate.py — GUILD-65 (T1): evidence-weighted confidence as a gate.

Every conclusion carries a confidence computed from its evidence lineage (how many
cited, verified, distinct-source facts support it). Low-confidence conclusions are
flagged ASSUMPTION and may NOT silently drive the build queue — they ride as explicit
assumptions until more evidence arrives. Steers IA + build prioritization.

  python3 scripts/confidence-gate.py --spine nuggets.json [--min 0.6]
  python3 scripts/confidence-gate.py --selftest
"""
import sys, json, argparse

MIN = 0.6

def _facts_for(node_id, by_id, seen=None):
    seen = seen or set()
    if node_id in seen or node_id not in by_id: return []
    seen.add(node_id); n = by_id[node_id]; out = []
    if n.get("type") == "fact": out.append(n)
    for p in n.get("derived_from", []): out.extend(_facts_for(p, by_id, seen))
    return out

def confidence(node_id, by_id):
    facts = {f["id"]: f for f in _facts_for(node_id, by_id)}.values()
    if not facts: return 0.0
    cited = sum(1 for f in facts if str(f.get("citation", "")).strip() and not f.get("opinion"))
    verified = sum(1 for f in facts if f.get("verified"))
    sources = len({f.get("citation") for f in facts if f.get("citation")})
    n = len(facts)
    # evidence weight: coverage of cited + verified, bonus for triangulated distinct sources
    base = (cited / n) * 0.5 + (verified / n) * 0.3
    triangulation = min(sources, 3) / 3 * 0.2
    return round(min(1.0, base + triangulation), 3)

def assess(nuggets, min_conf=MIN):
    by_id = {n["id"]: n for n in nuggets}
    rows = []
    for n in nuggets:
        if n.get("type") in ("conclusion", "constraint"):
            c = confidence(n["id"], by_id)
            rows.append({"id": n["id"], "confidence": c,
                         "flag": "ASSUMPTION" if c < min_conf else "evidence-backed",
                         "gates_build": c >= min_conf})
    return rows

def selftest():
    nuggets = [
        {"id": "E1", "type": "experiment", "content": "interviews"},
        {"id": "F1", "type": "fact", "content": "a", "citation": "test#1", "verified": True, "derived_from": ["E1"]},
        {"id": "F2", "type": "fact", "content": "b", "citation": "analytics", "verified": True, "derived_from": ["E1"]},
        {"id": "F3", "type": "fact", "content": "c", "citation": "survey", "verified": True},
        {"id": "I1", "type": "insight", "content": "strong", "derived_from": ["F1", "F2", "F3"]},
        {"id": "C1", "type": "conclusion", "content": "well-evidenced", "derived_from": ["I1"]},
        {"id": "F4", "type": "fact", "content": "weak", "citation": "", "verified": False},
        {"id": "I2", "type": "insight", "content": "thin", "derived_from": ["F4"]},
        {"id": "C2", "type": "conclusion", "content": "thinly-evidenced", "derived_from": ["I2"]},
    ]
    rows = assess(nuggets)
    print("GUILD-65 confidence-as-a-gate — self-test")
    for r in rows: print(f"   {r['id']}: conf {r['confidence']} -> {r['flag']} (gates_build={r['gates_build']})")
    c1 = next(r for r in rows if r["id"] == "C1")
    c2 = next(r for r in rows if r["id"] == "C2")
    ok = c1["gates_build"] is True and c2["flag"] == "ASSUMPTION" and c2["gates_build"] is False
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — well-evidenced conclusion gates the build; thin one flagged ASSUMPTION (blocked from silently driving build).")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spine"); ap.add_argument("--min", type=float, default=MIN); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.spine:
        for r in assess(json.load(open(a.spine)), a.min): print(r)
        return
    sys.exit("pass --spine <file> or --selftest")

if __name__ == "__main__":
    main()
