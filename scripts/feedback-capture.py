#!/usr/bin/env python3
"""
feedback-capture.py — GUILD-79 (T3): feedback → pairwise taste labels + 3-anchor pins.

Turns owner feedback into durable, schema-constrained pairwise taste labels and fits a
per-owner Bradley-Terry model. Extends the live capture (pairwise-capture.py routing
fix, GUILD-79) + the BT scorer (bradley-terry.py). Folds GUILD-60 (in-browser
commenting → a feedback item); feeds GUILD-59 (auto-suggest).

Recipe (P4 feedback-capture deep-dive):
  - explode a rank-K judgement into C(K,2) pairwise labels (winner = higher-ranked)
  - 3-ANCHOR PINS: 3 fixed reference exemplars pinned into every batch so BT scores are
    comparable across sessions (anchored scale)
  - FLAT, schema-constrained records: {id, a, b, winner, dim, lifecycle, anchor}
  - lifecycle: open → addressed → verified (no skipping)
  - uncertainty-driven next pick (closest BT strengths = most informative)

  python3 scripts/feedback-capture.py --selftest
"""
import os, sys, json, importlib.util, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
LIFECYCLE = ["open", "addressed", "verified"]

def _bt():
    spec = importlib.util.spec_from_file_location("bt", os.path.join(HERE, "bradley-terry.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def explode(rank, dim=None):
    """rank: [best..worst] -> C(K,2) flat pairwise labels (winner = higher-ranked)."""
    out = []
    for i in range(len(rank)):
        for j in range(i + 1, len(rank)):
            out.append({"id": f"{rank[i]}|{rank[j]}", "a": rank[i], "b": rank[j],
                        "winner": rank[i], "dim": dim, "lifecycle": "open", "anchor": False})
    return out

def with_anchors(labels, anchors):
    """Pin 3 anchors as flagged reference labels (anchor ordering = the reference scale)."""
    a = list(anchors)[:3]
    anchor_labels = []
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            anchor_labels.append({"id": f"anchor:{a[i]}|{a[j]}", "a": a[i], "b": a[j],
                                  "winner": a[i], "dim": "anchor", "lifecycle": "verified", "anchor": True})
    return anchor_labels + labels

def advance(item):
    """open -> addressed -> verified; no skipping."""
    i = LIFECYCLE.index(item["lifecycle"])
    if i + 1 < len(LIFECYCLE): item = {**item, "lifecycle": LIFECYCLE[i + 1]}
    return item

def valid_transition(frm, to):
    return to in LIFECYCLE and LIFECYCLE.index(to) == LIFECYCLE.index(frm) + 1

def fit(labels):
    comparisons = [(l["a"], l["b"], l["winner"]) for l in labels]
    return _bt().aggregate(comparisons)

def next_pick(strengths):
    """Most informative pair = closest BT strengths."""
    items = sorted(strengths, key=lambda k: strengths[k])
    best, pair = 1e9, None
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            gap = abs(strengths[items[i]] - strengths[items[j]])
            if gap < best: best, pair = gap, (items[i], items[j])
    return pair

def selftest():
    labels = explode(["A", "B", "C"], dim="hierarchy")          # C(3,2)=3 pairwise
    pinned = with_anchors(labels, ["GOOD", "MID", "BAD"])        # +3 anchor pairs
    rank = fit(labels)["ranking"]
    flat_ok = all(set(l) == {"id", "a", "b", "winner", "dim", "lifecycle", "anchor"} for l in labels)
    lc_ok = advance({"lifecycle": "open"})["lifecycle"] == "addressed" and not valid_transition("open", "verified")
    np_strengths = {"A": 2.0, "B": 1.9, "C": 0.0}
    np = next_pick(np_strengths)
    print("GUILD-79 feedback-capture — self-test")
    print(f"   explode rank[A,B,C] -> {len(labels)} pairwise; BT ranking: {rank}")
    print(f"   anchors pinned: {sum(1 for l in pinned if l['anchor'])} | flat schema: {flat_ok}")
    print(f"   lifecycle open->addressed ok, open->verified blocked: {lc_ok}")
    print(f"   uncertainty next-pick (closest pair): {np}")
    ok = (len(labels) == 3 and rank == ["A", "B", "C"] and flat_ok and lc_ok
          and sum(1 for l in pinned if l["anchor"]) == 3 and set(np) == {"A", "B"})
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — rank→C(K,2)→BT recovers order; 3 anchors pinned; flat schema; lifecycle gated; next-pick = most uncertain pair.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rank", help="comma-separated best..worst")
    ap.add_argument("--anchors", help="comma-separated 3 anchors")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.rank:
        labels = explode([x.strip() for x in a.rank.split(",")])
        if a.anchors: labels = with_anchors(labels, [x.strip() for x in a.anchors.split(",")])
        print(json.dumps({"labels": labels, "fit": fit(labels)}, indent=2)); return
    sys.exit("pass --rank a,b,c [--anchors g,m,b] or --selftest")

if __name__ == "__main__":
    main()
