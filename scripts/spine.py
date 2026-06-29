#!/usr/bin/env python3
"""
spine.py — GUILD-63: the Traceability Spine validator (the moat).

The atomic evidence chain: experiment -> fact -> insight -> conclusion -> constraint
-> ac -> adr. Every research nugget is a typed node; downstream artifacts carry the
nugget IDs they derive from, so any conclusion/AC traces to its evidence. This
validates a spine (well-formed lineage, no orphans, no cycles, facts cited) and
traces any node's lineage. Schema: docs/guild/spine-schema.yaml.

  python3 scripts/spine.py --spine nuggets.json [--trace AC1]
  python3 scripts/spine.py --selftest
nugget: {id, type, content, derived_from?:[ids], citation?}
"""
import os, sys, json, argparse
import yaml

SCHEMA = os.path.join(os.getcwd(), "docs", "guild", "spine-schema.yaml")

def schema():
    return yaml.safe_load(open(SCHEMA)) or {}

def validate(nuggets, parents):
    by_id = {n["id"]: n for n in nuggets}
    findings = []
    # cycle check via DFS
    WHITE, GREY, BLACK = 0, 1, 2
    color = {n["id"]: WHITE for n in nuggets}
    def dfs(i):
        color[i] = GREY
        for p in by_id[i].get("derived_from", []):
            if p in by_id:
                if color.get(p) == GREY: return True
                if color.get(p) == WHITE and dfs(p): return True
        color[i] = BLACK; return False
    for n in nuggets:
        if color[n["id"]] == WHITE and dfs(n["id"]):
            findings.append(f"CYCLE detected through {n['id']}")
    # per-node rules
    for n in nuggets:
        t = n.get("type"); allowed = parents.get(t, [])
        if t == "fact" and not n.get("citation"):
            findings.append(f"{n['id']} (fact) has no citation")
        ddf = n.get("derived_from", [])
        for p in ddf:
            if p not in by_id:
                findings.append(f"{n['id']} derives_from missing nugget {p}")
            elif by_id[p].get("type") not in allowed:
                findings.append(f"{n['id']} ({t}) derives_from {p} ({by_id[p].get('type')}) — not an allowed parent {allowed}")
        # orphan: types that REQUIRE a parent must have >=1 resolvable allowed parent
        if allowed and t != "fact":
            ok = any(by_id.get(p, {}).get("type") in allowed for p in ddf)
            if not ok:
                findings.append(f"{n['id']} ({t}) is an ORPHAN — needs >=1 {allowed} parent")
    return findings

def trace(nuggets, node_id):
    by_id = {n["id"]: n for n in nuggets}
    lineage, seen = [], set()
    def walk(i, depth):
        if i in seen or i not in by_id: return
        seen.add(i); n = by_id[i]
        lineage.append(("  " * depth) + f"{n['id']} [{n['type']}] {n.get('content','')[:48]}")
        for p in n.get("derived_from", []): walk(p, depth + 1)
    walk(node_id, 0)
    return lineage

def selftest():
    p = schema().get("parents") or {}
    good = [
        {"id": "E1", "type": "experiment", "content": "5 user interviews"},
        {"id": "F1", "type": "fact", "content": "4/5 missed the filter", "citation": "interview-notes#3", "derived_from": ["E1"]},
        {"id": "I1", "type": "insight", "content": "filter discoverability is low", "derived_from": ["F1"]},
        {"id": "C1", "type": "conclusion", "content": "surface filter affordance", "derived_from": ["I1"]},
        {"id": "AC1", "type": "ac", "content": "filter visible without scroll", "derived_from": ["C1"]},
    ]
    bad = good + [
        {"id": "F2", "type": "fact", "content": "uncited claim"},                 # no citation
        {"id": "I2", "type": "insight", "content": "orphan insight"},             # no fact parent
    ]
    gf, bf = validate(good, p), validate(bad, p)
    tr = trace(good, "AC1")
    print("GUILD-63 traceability spine — self-test")
    print(f"   well-formed spine findings: {len(gf)}")
    print(f"   broken spine findings: {len(bf)} -> {bf}")
    print("   trace(AC1):"); [print("     " + l) for l in tr]
    ok = (len(gf) == 0 and any("F2" in x for x in bf) and any("I2" in x and "ORPHAN" in x for x in bf)
          and len(tr) == 5)   # AC1->C1->I1->F1->E1
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — clean spine valid; uncited fact + orphan insight caught; AC traces to evidence.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spine"); ap.add_argument("--trace"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.spine:
        nuggets = json.load(open(a.spine)); p = schema().get("parents") or {}
        if a.trace:
            for l in trace(nuggets, a.trace): print(l)
        else:
            f = validate(nuggets, p)
            for x in f: print(" ✗", x)
            print("spine OK" if not f else f"{len(f)} finding(s)")
            sys.exit(0 if not f else 1)
        return
    sys.exit("pass --spine <file> [--trace ID] or --selftest")

if __name__ == "__main__":
    main()
