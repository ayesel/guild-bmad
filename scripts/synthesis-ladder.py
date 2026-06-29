#!/usr/bin/env python3
"""
synthesis-ladder.py — GUILD-66 (T1): enforce the synthesis ladder.

A cluster is not an insight; an insight needs TRIANGULATION. Over the spine, every
insight must derive from >=2 facts drawn from >=2 DISTINCT sources (citations). A
single fact (or two facts from one source) is a clustered observation, not a
triangulated insight — flagged.

  python3 scripts/synthesis-ladder.py --spine nuggets.json [--min-sources 2]
  python3 scripts/synthesis-ladder.py --selftest
"""
import sys, json, argparse

MIN_SOURCES = 2

def check(nuggets, min_sources=MIN_SOURCES):
    by_id = {n["id"]: n for n in nuggets}
    findings = []
    for n in nuggets:
        if n.get("type") != "insight": continue
        facts = [by_id[p] for p in n.get("derived_from", []) if by_id.get(p, {}).get("type") == "fact"]
        sources = {f.get("citation") for f in facts if f.get("citation")}
        if len(facts) < 2 or len(sources) < min_sources:
            findings.append(f"{n['id']}: {len(facts)} fact(s) / {len(sources)} distinct source(s) — "
                            f"not triangulated (need >=2 facts from >={min_sources} sources). Cluster != insight.")
    return findings

def selftest():
    nuggets = [
        {"id": "F1", "type": "fact", "content": "a", "citation": "interview"},
        {"id": "F2", "type": "fact", "content": "b", "citation": "analytics"},
        {"id": "F3", "type": "fact", "content": "c", "citation": "interview"},
        {"id": "I_good", "type": "insight", "content": "triangulated", "derived_from": ["F1", "F2"]},   # 2 facts, 2 sources
        {"id": "I_single", "type": "insight", "content": "one fact", "derived_from": ["F1"]},           # 1 fact
        {"id": "I_onesrc", "type": "insight", "content": "same source", "derived_from": ["F1", "F3"]},  # 2 facts, 1 source
    ]
    f = check(nuggets)
    print("GUILD-66 synthesis-ladder — self-test")
    for x in f: print("   ✗", x)
    ids = " ".join(f)
    ok = "I_good" not in ids and "I_single" in ids and "I_onesrc" in ids
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — triangulated insight passes; single-fact + single-source 'insights' flagged.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spine"); ap.add_argument("--min-sources", type=int, default=MIN_SOURCES); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.spine:
        f = check(json.load(open(a.spine)), a.min_sources)
        for x in f: print(" ✗", x)
        print("synthesis OK" if not f else f"{len(f)} finding(s)"); sys.exit(0 if not f else 1)
    sys.exit("pass --spine <file> or --selftest")

if __name__ == "__main__":
    main()
