#!/usr/bin/env python3
"""
layout-engine.py — GUILD-71 (T2): deterministic layout engines + validators.

The canonical model (GUILD-69) holds NO coordinates — LLMs free-handing x/y is where
artifacts go wrong. This computes node positions DETERMINISTICALLY from the model's
layout_contract engine (tree / sequence / swimlane / grid / force→grid fallback), as a
SEPARATE positions map (the model stays coord-free). Validates: no overlaps, and same
input -> same output (deterministic).

  python3 scripts/layout-engine.py --artifact a.json --out positions.json
  python3 scripts/layout-engine.py --selftest
"""
import os, sys, json, math, argparse

NW, NH, GAP = 160, 60, 40   # node box + gap (renderer scales via DTCG tokens)

def _layers(nodes, edges):
    ids = [n["id"] for n in nodes]
    incoming = {i: 0 for i in ids}
    children = {i: [] for i in ids}
    for e in edges:
        if e["to"] in incoming: incoming[e["to"]] += 1
        if e["from"] in children: children[e["from"]].append(e["to"])
    roots = [i for i in ids if incoming[i] == 0] or ids[:1]
    depth = {}
    frontier = [(r, 0) for r in roots]
    while frontier:
        nid, d = frontier.pop(0)
        if nid in depth: continue
        depth[nid] = d
        for c in children.get(nid, []):
            if c not in depth: frontier.append((c, d + 1))
    for i in ids:                    # any disconnected node
        depth.setdefault(i, 0)
    return depth

def layout(model):
    nodes = model.get("nodes", []); edges = model.get("edges", [])
    engine = (model.get("layout_contract") or {}).get("engine", "grid")
    ids = [n["id"] for n in nodes]
    pos = {}
    if engine in ("tree", "hierarchical"):
        depth = _layers(nodes, edges)
        by_d = {}
        for i in sorted(ids):                       # sorted => deterministic ordering
            by_d.setdefault(depth[i], []).append(i)
        for d, row in by_d.items():
            for x, i in enumerate(sorted(row)):
                pos[i] = {"x": x * (NW + GAP), "y": d * (NH + GAP)}
    elif engine == "sequence":
        for x, i in enumerate(ids):
            pos[i] = {"x": x * (NW + GAP), "y": 0}
    elif engine == "swimlane":
        lanes = sorted({n["type"] for n in nodes})
        lane_idx = {t: k for k, t in enumerate(lanes)}
        order = {}
        for n in nodes:
            t = n["type"]; order[t] = order.get(t, 0)
            pos[n["id"]] = {"x": order[t] * (NW + GAP), "y": lane_idx[t] * (NH + GAP) * 2}
            order[t] += 1
    else:   # grid (and force -> deterministic grid fallback)
        cols = max(1, math.ceil(math.sqrt(len(ids))))
        for k, i in enumerate(ids):
            pos[i] = {"x": (k % cols) * (NW + GAP), "y": (k // cols) * (NH + GAP)}
    return pos

def overlaps(pos):
    items = list(pos.items()); bad = []
    for a in range(len(items)):
        for b in range(a + 1, len(items)):
            (ia, pa), (ib, pb) = items[a], items[b]
            if abs(pa["x"] - pb["x"]) < NW and abs(pa["y"] - pb["y"]) < NH:
                bad.append((ia, ib))
    return bad

def selftest():
    tree = {"type": "sitemap", "layout_contract": {"engine": "tree"},
            "nodes": [{"id": "home", "type": "page"}, {"id": "today", "type": "page"},
                      {"id": "log", "type": "page"}, {"id": "settings", "type": "page"}],
            "edges": [{"from": "home", "to": "today"}, {"from": "home", "to": "log"}, {"from": "home", "to": "settings"}]}
    flow = {"type": "user-flow", "layout_contract": {"engine": "sequence"},
            "nodes": [{"id": "s0", "type": "step"}, {"id": "s1", "type": "step"}, {"id": "s2", "type": "step"}], "edges": []}
    p1, p2 = layout(tree), layout(tree)
    fp = layout(flow)
    det = p1 == p2
    ov = overlaps(p1)
    root_above = p1["home"]["y"] < p1["today"]["y"]          # tree: parent above children
    seq_linear = fp["s0"]["x"] < fp["s1"]["x"] < fp["s2"]["x"] and fp["s0"]["y"] == fp["s2"]["y"]
    print("GUILD-71 layout engine — self-test")
    print(f"   tree deterministic (run1==run2): {det} | overlaps: {len(ov)} | parent-above-children: {root_above}")
    print(f"   sequence linear (x increasing, y constant): {seq_linear}")
    ok = det and not ov and root_above and seq_linear
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — deterministic, no overlaps, tree hierarchy + sequence linearity correct (model stays coord-free).")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact"); ap.add_argument("--out"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.artifact:
        model = json.load(open(a.artifact)); pos = layout(model); ov = overlaps(pos)
        out = a.out or "positions.json"; json.dump(pos, open(out, "w"), indent=2)
        print(f"laid out {len(pos)} nodes ({(model.get('layout_contract') or {}).get('engine')}) -> {out}; overlaps: {len(ov)}")
        sys.exit(0 if not ov else 1)
    sys.exit("pass --artifact <f> or --selftest")

if __name__ == "__main__":
    main()
