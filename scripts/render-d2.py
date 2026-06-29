#!/usr/bin/env python3
"""GUILD-74 D2 render adapter."""
import argparse
import sys

from render_artifact_common import load_artifact, normalize, sample_artifact, selftest_model, slug, validate_model, write_or_print


def render(model):
    model = normalize(model)
    failures = validate_model(model)
    if failures:
        raise SystemExit("; ".join(failures))
    lines = [
        f"# {model['title']}",
        "direction: down",
        "classes: {",
        "  page: { style.fill: \"#dbeafe\" }",
        "  flow: { style.fill: \"#dcfce7\" }",
        "}",
    ]
    for node in model["nodes"]:
        node_id = slug(node["id"])
        lines.append(f"{node_id}: {node['label']!r} {{")
        lines.append(f"  class: {slug(node.get('type', 'page'))}")
        if node.get("provenance"):
            lines.append(f"  tooltip: \"evidence: {', '.join(node['provenance'])}\"")
        lines.append("}")
    for edge in model["edges"]:
        label = f": {edge['label']!r}" if edge.get("label") else ""
        lines.append(f"{slug(edge['from'])} -> {slug(edge['to'])}{label}")
    if model.get("legend"):
        lines.append("legend: {")
        for key, value in model["legend"].items():
            lines.append(f"  {slug(key)}: {value!r}")
        lines.append("}")
    return "\n".join(lines) + "\n"


def selftest():
    model = selftest_model()
    output = render(model)
    ok = "Home" in output and "home -> browse" in output and "legend" in output
    print("GUILD-74 D2 renderer - self-test")
    print(f"   nodes: {len(model['nodes'])} edges: {len(model['edges'])}")
    print(f"\n{'PASS' if ok else 'FAIL'} - sample artifact rendered to D2.")
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
