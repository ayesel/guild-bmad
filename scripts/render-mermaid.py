#!/usr/bin/env python3
"""GUILD-74 Mermaid render adapter."""
import argparse
import sys

from render_artifact_common import load_artifact, normalize, sample_artifact, selftest_model, slug, validate_model, write_or_print


def render(model):
    model = normalize(model)
    failures = validate_model(model)
    if failures:
        raise SystemExit("; ".join(failures))
    direction = (model.get("layout_contract") or {}).get("direction", "TB")
    lines = [f"---\ntitle: {model['title']}\n---", f"flowchart {direction}"]
    for node in model["nodes"]:
        shape = ("([" + node["label"] + "])") if node.get("type") == "flow" else ("[" + node["label"] + "]")
        lines.append(f"  {slug(node['id'])}{shape}")
    for edge in model["edges"]:
        label = f"|{edge['label']}|" if edge.get("label") else ""
        lines.append(f"  {slug(edge['from'])} -->{label} {slug(edge['to'])}")
    colors = {"page": "#dbeafe", "flow": "#dcfce7", "risk": "#fee2e2", "system": "#ede9fe"}
    types = sorted({node.get("type", "page") for node in model["nodes"]})
    for node_type in types:
        lines.append(f"  classDef {slug(node_type)} fill:{colors.get(node_type, '#f3f4f6')},stroke:#111827,color:#111827;")
    for node in model["nodes"]:
        lines.append(f"  class {slug(node['id'])} {slug(node.get('type', 'page'))};")
    return "\n".join(lines) + "\n"


def selftest():
    model = selftest_model()
    output = render(model)
    ok = "flowchart TB" in output and "Home" in output and "home -->|nav| browse" in output
    print("GUILD-74 Mermaid renderer - self-test")
    print(f"   nodes: {len(model['nodes'])} edges: {len(model['edges'])}")
    print(f"\n{'PASS' if ok else 'FAIL'} - sample artifact rendered to Mermaid.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
    model = load_artifact(args.artifact) if args.artifact else sample_artifact()
    write_or_print(render(model), args.out)


if __name__ == "__main__":
    main()
