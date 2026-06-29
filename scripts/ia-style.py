#!/usr/bin/env python3
"""
ia-style.py — GUILD-72 (T2): IA visual style system (semantic tokens + legend).

Renderers must NOT free-pick colors. This maps canonical-artifact node/edge TYPES to
SEMANTIC DTCG token refs (fill/border/text) + a shape, and emits a legend — so every
renderer (FigJam/D2/SVG) styles consistently, on-brand, and legibly. Token refs only,
no raw hex (device-light, brand-safe).

  python3 scripts/ia-style.py --artifact a.json
  python3 scripts/ia-style.py --selftest
"""
import sys, json, argparse

# node type -> (ramp, shape). Ramps are real DTCG color ramps (tokens.dtcg.json).
TYPE_STYLE = {
    "page": ("ember", "rect"), "screen": ("ember", "rect"),
    "step": ("sage", "rect"), "stage": ("denim", "rect"),
    "decision": ("honey", "diamond"), "start": ("sage", "pill"), "end": ("sage", "pill"),
    "group": ("warm", "rect"), "error": ("berry", "rect"),
}
DEFAULT = ("warm", "rect")

def style_for(t):
    ramp, shape = TYPE_STYLE.get(t, DEFAULT)
    return {"fill": f"{{color.{ramp}.100}}", "border": f"{{color.{ramp}.600}}",
            "text": "{color.warm.900}", "shape": shape}

def build(model):
    node_types = sorted({n.get("type") for n in model.get("nodes", []) if n.get("type")})
    styles = {t: style_for(t) for t in node_types}
    edge = {"stroke": "{color.warm.400}", "style": "solid"}
    legend = [{"type": t, "swatch": styles[t]["border"], "shape": styles[t]["shape"]} for t in node_types]
    return {"node_styles": styles, "edge_style": edge, "legend": legend}

def validate(model, spec):
    findings = []
    node_types = {n.get("type") for n in model.get("nodes", []) if n.get("type")}
    for t in node_types:
        if t not in spec["node_styles"]:
            findings.append(f"node type '{t}' has no style")
    blob = json.dumps(spec)
    import re
    raw = re.findall(r'#[0-9a-fA-F]{6}', blob)
    if raw:
        findings.append(f"raw hex in style spec (must be token refs): {raw}")
    if len(spec["legend"]) != len(node_types):
        findings.append("legend does not cover all node types")
    return findings

def selftest():
    model = {"type": "sitemap",
             "nodes": [{"id": "h", "type": "page"}, {"id": "d", "type": "decision"}, {"id": "g", "type": "group"}],
             "edges": [{"from": "h", "to": "d"}]}
    spec = build(model); f = validate(model, spec)
    print("GUILD-72 IA visual style — self-test")
    print(f"   page style:     {spec['node_styles']['page']}")
    print(f"   decision shape: {spec['node_styles']['decision']['shape']}")
    print(f"   legend entries: {len(spec['legend'])} | validation findings: {len(f)}")
    ok = (not f
          and spec["node_styles"]["page"]["fill"] == "{color.ember.100}"
          and spec["node_styles"]["decision"]["shape"] == "diamond"
          and "#" not in json.dumps(spec)                       # token refs only, no raw hex
          and len(spec["legend"]) == 3)
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — types map to semantic token refs (no raw hex), shapes correct, legend covers all types.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.artifact:
        model = json.load(open(a.artifact)); spec = build(model); f = validate(model, spec)
        print(json.dumps(spec, indent=2))
        for x in f: print(" ✗", x, file=sys.stderr)
        sys.exit(0 if not f else 1)
    sys.exit("pass --artifact <f> or --selftest")

if __name__ == "__main__":
    main()
