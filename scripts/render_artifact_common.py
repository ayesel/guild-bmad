#!/usr/bin/env python3
"""
Shared helpers for GUILD-74 render adapters.

The canonical artifact model stays renderer-agnostic and coordinate-free. These
helpers accept a small JSON instance of that model and compute deterministic,
device-light positions for output formats that need coordinates.
"""
import html
import json
import math
import re

NODE_W = 180
NODE_H = 72
GAP_X = 56
GAP_Y = 48


def sample_artifact():
    return {
        "artifact_type": "sitemap",
        "title": "Sample product IA",
        "layout_contract": {"engine": "hierarchical", "direction": "TB"},
        "nodes": [
            {"id": "home", "label": "Home", "type": "page", "provenance": ["nugget-1"]},
            {"id": "browse", "label": "Browse", "type": "page"},
            {"id": "detail", "label": "Detail", "type": "page"},
            {"id": "checkout", "label": "Checkout", "type": "flow"},
        ],
        "edges": [
            {"from": "home", "to": "browse", "type": "primary", "label": "nav"},
            {"from": "browse", "to": "detail", "type": "sequence", "label": "select"},
            {"from": "detail", "to": "checkout", "type": "sequence", "label": "buy"},
        ],
        "legend": {
            "page": "IA page or route",
            "flow": "Transactional flow",
            "primary": "Primary navigation",
            "sequence": "User sequence",
        },
    }


def load_artifact(path):
    with open(path, "r", encoding="utf-8") as f:
        return normalize(json.load(f))


def normalize(model):
    model = dict(model)
    model.setdefault("artifact_type", model.get("type", "artifact"))
    model.setdefault("title", model["artifact_type"].replace("-", " ").title())
    model.setdefault("nodes", [])
    model.setdefault("edges", [])
    model.setdefault("layout_contract", {"engine": "grid", "direction": "TB"})
    model.setdefault("legend", {})
    return model


def validate_model(model):
    failures = []
    ids = set()
    for node in model.get("nodes", []):
        for key in ("id", "label", "type"):
            if not node.get(key):
                failures.append(f"node missing {key}: {node}")
        if node.get("id") in ids:
            failures.append(f"duplicate node id: {node.get('id')}")
        ids.add(node.get("id"))
    for edge in model.get("edges", []):
        if edge.get("from") not in ids:
            failures.append(f"edge from unknown node: {edge}")
        if edge.get("to") not in ids:
            failures.append(f"edge to unknown node: {edge}")
    return failures


def slug(value):
    return re.sub(r"[^a-zA-Z0-9_]+", "_", str(value)).strip("_") or "node"


def esc(value):
    return html.escape(str(value), quote=True)


def node_by_id(model):
    return {node["id"]: node for node in model["nodes"]}


def layers(model):
    ids = [node["id"] for node in model["nodes"]]
    incoming = {node_id: 0 for node_id in ids}
    children = {node_id: [] for node_id in ids}
    for edge in model["edges"]:
        if edge["to"] in incoming:
            incoming[edge["to"]] += 1
        if edge["from"] in children:
            children[edge["from"]].append(edge["to"])
    roots = [node_id for node_id in ids if incoming[node_id] == 0] or ids[:1]
    depth = {}
    queue = [(root, 0) for root in roots]
    while queue:
        node_id, level = queue.pop(0)
        if node_id in depth:
            continue
        depth[node_id] = level
        for child in children.get(node_id, []):
            queue.append((child, level + 1))
    for node_id in ids:
        depth.setdefault(node_id, 0)
    return depth


def layout(model):
    model = normalize(model)
    nodes = model["nodes"]
    engine = (model.get("layout_contract") or {}).get("engine", "grid")
    direction = (model.get("layout_contract") or {}).get("direction", "TB")
    positions = {}
    if engine in ("hierarchical", "tree"):
        depth = layers(model)
        grouped = {}
        for node in nodes:
            grouped.setdefault(depth[node["id"]], []).append(node["id"])
        for level in sorted(grouped):
            row = sorted(grouped[level])
            for index, node_id in enumerate(row):
                x = index * (NODE_W + GAP_X)
                y = level * (NODE_H + GAP_Y)
                positions[node_id] = {"x": y if direction in ("LR", "RL") else x, "y": x if direction in ("LR", "RL") else y}
    elif engine in ("sequence", "swimlane"):
        for index, node in enumerate(nodes):
            positions[node["id"]] = {"x": index * (NODE_W + GAP_X), "y": 0}
    else:
        cols = max(1, math.ceil(math.sqrt(len(nodes))))
        for index, node in enumerate(nodes):
            positions[node["id"]] = {
                "x": (index % cols) * (NODE_W + GAP_X),
                "y": (index // cols) * (NODE_H + GAP_Y),
            }
    return positions


def bounds(positions):
    if not positions:
        return {"width": NODE_W, "height": NODE_H}
    max_x = max(point["x"] for point in positions.values()) + NODE_W
    max_y = max(point["y"] for point in positions.values()) + NODE_H
    return {"width": max_x, "height": max_y}


def write_or_print(text, out):
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text, end="" if text.endswith("\n") else "\n")


def selftest_model():
    model = normalize(sample_artifact())
    failures = validate_model(model)
    if failures:
        raise AssertionError("; ".join(failures))
    return model
