#!/usr/bin/env python3
"""
composers.py — GUILD-70 (T2): artifact-specific composers.

Turn structured IA input into a CANONICAL artifact model (GUILD-69) — one composer per
artifact type. Composers emit only structure + a layout CONTRACT (no pixel coords);
GUILD-71 lays it out, GUILD-73/74 render it. Output is validated by artifact-model.py.

  python3 scripts/composers.py --type sitemap --input tree.json --out art.json
  python3 scripts/composers.py --selftest
"""
import os, sys, json, subprocess, tempfile, argparse

HERE = os.path.dirname(os.path.abspath(__file__))

def compose_sitemap(tree, prov=None):
    """tree: {label: {child: {...}}} nested dict -> tree model."""
    nodes, edges = [], []
    def slug(s): return s.lower().replace(" ", "-")
    def walk(label, children, parent=None):
        nid = slug(label)
        n = {"id": nid, "label": label, "type": "page"}
        if prov and prov.get(label): n["provenance"] = prov[label]
        nodes.append(n)
        if parent: edges.append({"from": parent, "to": nid})
        for c, gc in (children or {}).items():
            walk(c, gc, nid)
    for root, kids in tree.items():
        walk(root, kids)
    return {"type": "sitemap", "nodes": nodes, "edges": edges,
            "layout_contract": {"engine": "tree", "direction": "TB", "spacing": "var(--space-6)"}}

def compose_flow(steps):
    """steps: [labels] -> linear sequence model."""
    nodes = [{"id": f"s{i}", "label": s, "type": "step"} for i, s in enumerate(steps)]
    edges = [{"from": f"s{i}", "to": f"s{i+1}"} for i in range(len(steps) - 1)]
    return {"type": "user-flow", "nodes": nodes, "edges": edges,
            "layout_contract": {"engine": "sequence", "direction": "LR", "spacing": "var(--space-5)"}}

def compose_journey(stages):
    """stages: [labels] -> swimlane journey model."""
    nodes = [{"id": f"st{i}", "label": s, "type": "stage"} for i, s in enumerate(stages)]
    edges = [{"from": f"st{i}", "to": f"st{i+1}"} for i in range(len(stages) - 1)]
    return {"type": "journey-map", "nodes": nodes, "edges": edges,
            "layout_contract": {"engine": "swimlane", "direction": "LR", "spacing": "var(--space-6)"}}

COMPOSERS = {"sitemap": compose_sitemap, "user-flow": compose_flow, "journey-map": compose_journey}

def _validate(model):
    """Round-trip through the GUILD-69 validator (real integration)."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(model, f); tmp = f.name
    r = subprocess.run([sys.executable, os.path.join(HERE, "artifact-model.py"), "--artifact", tmp],
                       text=True, capture_output=True, cwd=os.path.dirname(HERE))
    os.unlink(tmp)
    return r.returncode == 0, r.stdout.strip()

def selftest():
    print("GUILD-70 composers — self-test")
    sm = compose_sitemap({"Home": {"Today": {}, "Log": {}, "Settings": {}}}, prov={"Today": ["AC1"]})
    fl = compose_flow(["Open app", "Log meal", "See progress"])
    jr = compose_journey(["Discover", "Onboard", "Habit"])
    results = []
    for name, m, eng in [("sitemap", sm, "tree"), ("user-flow", fl, "sequence"), ("journey-map", jr, "swimlane")]:
        ok, out = _validate(m)
        good = ok and m["layout_contract"]["engine"] == eng and len(m["nodes"]) >= 3
        results.append(good)
        print(f"   {name}: {len(m['nodes'])} nodes, engine={m['layout_contract']['engine']}, valid={ok}")
    prov_ok = any(n.get("provenance") for n in sm["nodes"])   # carries spine nugget IDs
    print(f"   sitemap carries provenance (spine link): {prov_ok}")
    allok = all(results) and prov_ok
    print(f"\n{'✅ PASS' if allok else '❌ FAIL'} — composers emit valid canonical models (pass GUILD-69), correct engines, provenance preserved.")
    sys.exit(0 if allok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", choices=list(COMPOSERS)); ap.add_argument("--input"); ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.type and a.input:
        model = COMPOSERS[a.type](json.load(open(a.input)))
        out = a.out or f"{a.type}.artifact.json"
        json.dump(model, open(out, "w"), indent=2)
        print(f"composed {a.type} -> {out} ({len(model['nodes'])} nodes)")
        return
    sys.exit("pass --type <t> --input <f> [--out f] or --selftest")

if __name__ == "__main__":
    main()
