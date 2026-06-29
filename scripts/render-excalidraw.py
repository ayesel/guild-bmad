#!/usr/bin/env python3
"""GUILD-74 Excalidraw JSON render adapter."""
import argparse
import json
import sys

from render_artifact_common import NODE_H, NODE_W, layout, load_artifact, normalize, sample_artifact, selftest_model, validate_model, write_or_print


def element_id(prefix, value):
    return f"guild_{prefix}_{value}".replace("-", "_")


def render_data(model):
    model = normalize(model)
    failures = validate_model(model)
    if failures:
        raise SystemExit("; ".join(failures))
    positions = layout(model)
    elements = []
    for node in model["nodes"]:
        pos = positions[node["id"]]
        fill = "#dbeafe" if node.get("type") == "page" else "#dcfce7"
        rect_id = element_id("rect", node["id"])
        text_id = element_id("text", node["id"])
        elements.append({
            "id": rect_id, "type": "rectangle", "x": pos["x"], "y": pos["y"],
            "width": NODE_W, "height": NODE_H, "angle": 0, "strokeColor": "#111827",
            "backgroundColor": fill, "fillStyle": "solid", "strokeWidth": 1,
            "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": {"type": 3}, "seed": 1, "version": 1, "versionNonce": 1,
            "isDeleted": False, "boundElements": [{"type": "text", "id": text_id}],
            "updated": 1, "link": None, "locked": False,
        })
        elements.append({
            "id": text_id, "type": "text", "x": pos["x"] + 16, "y": pos["y"] + 24,
            "width": NODE_W - 32, "height": 24, "angle": 0, "strokeColor": "#111827",
            "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
            "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
            "seed": 1, "version": 1, "versionNonce": 1, "isDeleted": False,
            "boundElements": None, "updated": 1, "link": None, "locked": False,
            "text": node["label"], "fontSize": 18, "fontFamily": 1, "textAlign": "center",
            "verticalAlign": "middle", "containerId": rect_id, "originalText": node["label"],
            "lineHeight": 1.25,
        })
    for edge in model["edges"]:
        source = positions[edge["from"]]
        target = positions[edge["to"]]
        elements.append({
            "id": element_id("arrow", f"{edge['from']}_{edge['to']}"), "type": "arrow",
            "x": source["x"] + NODE_W, "y": source["y"] + NODE_H / 2,
            "width": target["x"] - source["x"] - NODE_W, "height": target["y"] - source["y"],
            "angle": 0, "strokeColor": "#111827", "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2, "roughness": 1, "opacity": 100,
            "groupIds": [], "frameId": None, "seed": 1, "version": 1, "versionNonce": 1,
            "isDeleted": False, "boundElements": None, "updated": 1, "link": None,
            "locked": False, "startBinding": None, "endBinding": None,
            "points": [[0, 0], [target["x"] - source["x"] - NODE_W, target["y"] - source["y"]]],
            "lastCommittedPoint": None, "startArrowhead": None, "endArrowhead": "arrow",
        })
    return {"type": "excalidraw", "version": 2, "source": "guild-bmad", "elements": elements, "appState": {"viewBackgroundColor": "#ffffff"}, "files": {}}


def render(model):
    return json.dumps(render_data(model), indent=2) + "\n"


def selftest():
    model = selftest_model()
    data = render_data(model)
    labels = {element.get("text") for element in data["elements"] if element["type"] == "text"}
    arrows = [element for element in data["elements"] if element["type"] == "arrow"]
    ok = "Home" in labels and len(arrows) == len(model["edges"])
    print("GUILD-74 Excalidraw renderer - self-test")
    print(f"   elements: {len(data['elements'])} arrows: {len(arrows)}")
    print(f"\n{'PASS' if ok else 'FAIL'} - sample artifact rendered to Excalidraw JSON.")
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
