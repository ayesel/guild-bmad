#!/usr/bin/env python3
"""
auto-suggest.py — GUILD-59: proactive auto-suggestion engine.

The brain shouldn't wait to be asked. This composes the TIER-1 gates over the current
spine into a RANKED list of proactive next-actions — fed by GUILD-64 (verification),
65 (confidence), 66 (synthesis), 67 (drift), 68 (IA evidence), and the calibration
state (44/79). Output is surfaced in the dashboard (docs/guild/suggestions.yaml).

  python3 scripts/auto-suggest.py --spine nuggets.json [--artifacts arts.json] [--write]
  python3 scripts/auto-suggest.py --selftest
"""
import os, sys, json, importlib.util, argparse
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.getcwd(), "docs", "guild", "suggestions.yaml")
PRI = {"high": 0, "medium": 1, "low": 2}

def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def suggest(spine, artifacts=None):
    s = []
    ver = _load("ver", "verification-gate.py")
    for f in ver.gate(spine):
        s.append({"priority": "high", "source": "verification(64)", "action": "cite/verify or strip", "why": f})
    conf = _load("conf", "confidence-gate.py")
    for r in conf.assess(spine):
        if r["flag"] == "ASSUMPTION":
            s.append({"priority": "medium", "source": "confidence(65)", "action": "gather evidence before building",
                      "why": f"{r['id']} confidence {r['confidence']} < bar — flagged ASSUMPTION"})
    syn = _load("syn", "synthesis-ladder.py")
    for f in syn.check(spine):
        s.append({"priority": "medium", "source": "synthesis(66)", "action": "triangulate (>=2 sources)", "why": f})
    ia = _load("ia", "ia-evidence-guard.py")
    for f in ia.guard(spine):
        s.append({"priority": "high", "source": "ia-evidence(68)", "action": "replace synthetic evidence / add empirical", "why": f})
    if artifacts:
        lr = _load("lr", "living-repo.py")
        for f in lr.detect(spine, artifacts):
            s.append({"priority": "high", "source": "drift(67)", "action": "reconcile research↔product", "why": f})
    s.sort(key=lambda x: PRI.get(x["priority"], 9))
    return s

def selftest():
    spine = [
        {"id": "E1", "type": "experiment", "content": "interviews"},
        {"id": "F1", "type": "fact", "content": "uncited claim", "derived_from": ["E1"]},            # -> verification high (uncited+unverified)
        {"id": "F2", "type": "fact", "content": "synthetic persona says tabs", "citation": "ai-persona", "verified": True},  # -> ia high
        {"id": "I1", "type": "insight", "content": "thin", "derived_from": ["F1"]},                  # -> synthesis (1 fact/1 source)
        {"id": "C1", "type": "conclusion", "content": "ship it", "derived_from": ["I1"]},            # -> confidence ASSUMPTION (lineage = uncited F1)
    ]
    sg = suggest(spine)
    print("GUILD-59 auto-suggest — self-test")
    for x in sg: print(f"   [{x['priority']:6}] {x['source']:16} {x['action']} — {x['why'][:60]}")
    highs = [x for x in sg if x["priority"] == "high"]
    ok = (len(sg) >= 4 and sg[0]["priority"] == "high"            # ranked, high first
          and any("verification" in x["source"] for x in sg)
          and any("ia-evidence" in x["source"] for x in sg)
          and any("confidence" in x["source"] for x in sg)
          and any("synthesis" in x["source"] for x in sg))
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — composes the brain's gates into ranked proactive suggestions (high first), spanning verification/confidence/synthesis/IA.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spine"); ap.add_argument("--artifacts"); ap.add_argument("--write", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.spine:
        spine = json.load(open(a.spine))
        arts = json.load(open(a.artifacts)) if a.artifacts else None
        sg = suggest(spine, arts)
        if a.write:
            yaml.safe_dump({"suggestions": sg}, open(OUT, "w"), sort_keys=False)
            print(f"wrote {len(sg)} suggestions -> {OUT} (dashboard surfaces these)")
        else:
            print(json.dumps(sg, indent=2))
        return
    sys.exit("pass --spine <f> [--artifacts f] [--write] or --selftest")

if __name__ == "__main__":
    main()
