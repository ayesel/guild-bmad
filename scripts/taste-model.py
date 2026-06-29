#!/usr/bin/env python3
"""
taste-model.py — GUILD-55/56 (V-E): exemplar retrieval + active-elicitation taste model.

Taste-as-prose is the floor. This adds (55) taste-ranked retrieval over the owner
exemplar library and (56) a per-owner taste MODEL: weights over the shared attribute
basis (docs/guild/exemplars/exemplars.yaml), learned from a SMALL set of accept/
reject labels, with ACTIVE elicitation — pick the most informative next pair to ask
(~15 labels gets a usable model; text-domain plateaus ~2 exemplars, so stay cheap).

  python3 scripts/taste-model.py --selftest
  (library: retrieve(query) / update(weights,label) / next_query(candidates,weights))
"""
import os, sys, argparse
import yaml

EX = os.path.join(os.getcwd(), "docs", "guild", "exemplars", "exemplars.yaml")

def load():
    try: return yaml.safe_load(open(EX)) or {}
    except FileNotFoundError: return {}

def basis():
    return (load().get("basis")) or []

def score(attrs, weights):
    return sum(weights.get(a, 0.0) for a in attrs)

def retrieve(query_attrs, exemplars, weights, k=3):
    """Taste-ranked: tag overlap with the query, weighted by the taste model + owner-approval."""
    ranked = []
    for ex in exemplars:
        overlap = len(set(query_attrs) & set(ex.get("attributes", [])))
        s = overlap + score(ex.get("attributes", []), weights) + (0.5 if ex.get("owner_approved") else 0)
        ranked.append((s, ex.get("id")))
    ranked.sort(reverse=True)
    return [i for _, i in ranked[:k]]

def update(weights, accepted_attrs, rejected_attrs, lr=0.3):
    """Move weights toward accepted attributes, away from rejected."""
    w = dict(weights)
    for a in accepted_attrs: w[a] = round(w.get(a, 0.0) + lr, 3)
    for a in rejected_attrs: w[a] = round(w.get(a, 0.0) - lr, 3)
    return w

def next_query(candidates, weights):
    """Active elicitation: ask about the pair whose taste-scores are CLOSEST (most
    uncertain / most informative), not random."""
    best, pair = 1e9, None
    for i in range(len(candidates)):
        for j in range(i+1, len(candidates)):
            gap = abs(score(candidates[i]["attributes"], weights) - score(candidates[j]["attributes"], weights))
            if gap < best:
                best, pair = gap, (candidates[i]["id"], candidates[j]["id"])
    return pair

def selftest():
    b = ["editorial-restraint", "distinctive-not-safe", "generous-whitespace", "busy", "safe-generic"]
    w = {a: 0.0 for a in b}
    # owner accepts distinctive/restrained, rejects busy/safe
    w = update(w, ["editorial-restraint", "distinctive-not-safe"], ["busy", "safe-generic"])
    exemplars = [{"id": "bold", "attributes": ["distinctive-not-safe", "editorial-restraint"], "owner_approved": True},
                 {"id": "generic", "attributes": ["safe-generic", "busy"]}]
    ranked = retrieve(["distinctive-not-safe"], exemplars, w)
    cands = [{"id": "A", "attributes": ["editorial-restraint"]},
             {"id": "B", "attributes": ["distinctive-not-safe"]},   # ~tied with A -> most informative
             {"id": "C", "attributes": ["busy", "safe-generic"]}]
    q = next_query(cands, w)
    print("GUILD-55/56 taste model — self-test")
    print("   learned weights:", {k: v for k, v in w.items() if v})
    print(f"   taste-ranked retrieval: {ranked}  (bold first)")
    print(f"   active next-query (most uncertain pair): {q}")
    ok = (ranked[0] == "bold" and w["distinctive-not-safe"] > 0 and w["busy"] < 0
          and set(q) == {"A", "B"})   # A,B are the closest-scoring => most informative
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — model learns owner taste; retrieval ranks bold first; active-query picks the most uncertain pair.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    print(f"taste basis: {basis() or '(none — seed docs/guild/exemplars/exemplars.yaml)'}")

if __name__ == "__main__":
    main()
