#!/usr/bin/env python3
"""GUILD-74 Notion structured export payload stub; no network calls."""
import argparse
import json
import sys

from render_artifact_common import load_artifact, normalize, sample_artifact, selftest_model, validate_model, write_or_print


def render_data(model):
    model = normalize(model)
    failures = validate_model(model)
    if failures:
        raise SystemExit("; ".join(failures))
    edge_index = {}
    for edge in model["edges"]:
        edge_index.setdefault(edge["from"], []).append(edge)
    rows = []
    for node in model["nodes"]:
        rows.append({
            "Name": node["label"],
            "Node ID": node["id"],
            "Type": node.get("type", ""),
            "Outgoing": ", ".join(edge["to"] for edge in edge_index.get(node["id"], [])),
            "Evidence": ", ".join(node.get("provenance", [])),
        })
    return {
        "target": "notion-database",
        "database_title": model["title"],
        "properties": ["Name", "Node ID", "Type", "Outgoing", "Evidence"],
        "rows": rows,
    }


def render(model):
    return json.dumps(render_data(model), indent=2) + "\n"


def selftest():
    model = selftest_model()
    data = render_data(model)
    ok = data["target"] == "notion-database" and len(data["rows"]) == len(model["nodes"]) and data["rows"][0]["Evidence"]
    print("GUILD-74 Notion payload renderer - self-test")
    print(f"   rows: {len(data['rows'])}")
    print(f"\n{'PASS' if ok else 'FAIL'} - sample artifact rendered to Notion database payload stub.")
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
