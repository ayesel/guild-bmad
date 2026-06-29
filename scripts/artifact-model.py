#!/usr/bin/env python3
"""
artifact-model.py — GUILD-69 (T2): validate the Canonical Artifact Model.

One semantic model for every IA artifact; renderers (FigJam/D2/Mermaid/SVG) draw FROM
it. This validates an artifact is well-formed AND renderer-agnostic: known type, nodes
have id+label+type, edges reference real nodes, a layout CONTRACT with a known engine,
and NO pixel coordinates (layout is the renderer's job). Nodes may carry provenance
(spine nugget IDs) so the artifact traces to evidence. Schema: docs/guild/artifact-model.yaml.

  python3 scripts/artifact-model.py --artifact a.json
  python3 scripts/artifact-model.py --selftest
"""
import os, sys, json, argparse
import yaml

SCHEMA = os.path.join(os.getcwd(), "docs", "guild", "artifact-model.yaml")
PIXEL_KEYS = {"x", "y", "left", "top", "width", "height", "cx", "cy"}

def schema(): return yaml.safe_load(open(SCHEMA)) or {}

def validate(art, sch=None):
    sch = sch or schema()
    findings = []
    if art.get("type") not in (sch.get("artifact_types") or []):
        findings.append(f"unknown artifact type {art.get('type')!r}")
    nodes = art.get("nodes", []); ids = {n.get("id") for n in nodes}
    for n in nodes:
        if not (n.get("id") and n.get("label") and n.get("type")):
            findings.append(f"node {n.get('id','?')} missing id/label/type")
        if PIXEL_KEYS & set(n.keys()):
            findings.append(f"node {n.get('id','?')} carries pixel coords {PIXEL_KEYS & set(n.keys())} — model is renderer-agnostic")
    for e in art.get("edges", []):
        if e.get("from") not in ids or e.get("to") not in ids:
            findings.append(f"edge {e.get('from')}->{e.get('to')} references a missing node")
    lc = art.get("layout_contract") or {}
    engines = (sch.get("layout_contract") or {}).get("engine") or []
    if not lc:
        findings.append("missing layout_contract")
    elif lc.get("engine") not in engines:
        findings.append(f"layout_contract.engine {lc.get('engine')!r} not in {engines}")
    return findings

def selftest():
    sch = schema()
    good = {"type": "sitemap",
            "nodes": [{"id": "home", "label": "Home", "type": "page", "provenance": ["C1"]},
                      {"id": "about", "label": "About", "type": "page"},
                      {"id": "today", "label": "Today", "type": "page"}],
            "edges": [{"from": "home", "to": "about"}, {"from": "home", "to": "today"}],
            "layout_contract": {"engine": "tree", "direction": "TB"}}
    bad = {"type": "mindmap",                                   # unknown type
           "nodes": [{"id": "a", "label": "A", "type": "page", "x": 40, "y": 10}],  # pixel coords
           "edges": [{"from": "a", "to": "ghost"}],             # dangling edge
           "layout_contract": {"engine": "magic"}}             # unknown engine
    gf, bf = validate(good, sch), validate(bad, sch)
    print("GUILD-69 canonical artifact model — self-test")
    print(f"   valid sitemap findings: {len(gf)}")
    print(f"   broken artifact findings: {len(bf)}"); [print("     ✗", x) for x in bf]
    ok = (len(gf) == 0 and any("unknown artifact type" in x for x in bf)
          and any("pixel coords" in x for x in bf) and any("missing node" in x for x in bf)
          and any("engine" in x for x in bf))
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — valid model passes; unknown type / pixel coords / dangling edge / bad engine flagged.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.artifact:
        f = validate(json.load(open(a.artifact)))
        for x in f: print(" ✗", x)
        print("artifact model OK" if not f else f"{len(f)} finding(s)"); sys.exit(0 if not f else 1)
    sys.exit("pass --artifact <f> or --selftest")

if __name__ == "__main__":
    main()
