#!/usr/bin/env python3
"""GUILD-74 Miro payload stub render adapter; no network calls."""
import argparse
import json
import sys

from render_artifact_common import NODE_H, NODE_W, layout, load_artifact, normalize, sample_artifact, selftest_model, validate_model, write_or_print


def render_data(model):
    model = normalize(model)
    failures = validate_model(model)
    if failures:
        raise SystemExit("; ".join(failures))
    positions = layout(model)
    items = []
    for node in model["nodes"]:
        pos = positions[node["id"]]
        items.append({
            "type": "shape",
            "data": {"content": node["label"], "shape": "round_rectangle"},
            "style": {"fillColor": "#dbeafe" if node.get("type") == "page" else "#dcfce7"},
            "position": {"x": pos["x"], "y": pos["y"]},
            "geometry": {"width": NODE_W, "height": NODE_H},
            "guildNodeId": node["id"],
        })
    for edge in model["edges"]:
        items.append({
            "type": "connector",
            "startItem": {"guildNodeId": edge["from"]},
            "endItem": {"guildNodeId": edge["to"]},
            "captions": [{"content": edge.get("label", edge.get("type", ""))}],
        })
    return {"target": "miro-rest-v2", "operation": "create-board-items", "title": model["title"], "items": items}


def render(model):
    return json.dumps(render_data(model), indent=2) + "\n"


def selftest():
    model = selftest_model()
    data = render_data(model)
    ok = data["target"] == "miro-rest-v2" and len(data["items"]) == len(model["nodes"]) + len(model["edges"])
    print("GUILD-74 Miro payload renderer - self-test")
    print(f"   payload items: {len(data['items'])}")
    print(f"\n{'PASS' if ok else 'FAIL'} - sample artifact rendered to Miro REST payload stub.")
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
