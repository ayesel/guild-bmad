#!/usr/bin/env python3
"""GUILD-74 native SVG/HTML read-only artifact renderer."""
import argparse
import sys

from render_artifact_common import NODE_H, NODE_W, bounds, esc, layout, load_artifact, node_by_id, normalize, sample_artifact, selftest_model, validate_model, write_or_print


def render_svg(model):
    model = normalize(model)
    failures = validate_model(model)
    if failures:
        raise SystemExit("; ".join(failures))
    positions = layout(model)
    size = bounds(positions)
    width = size["width"] + 240
    height = size["height"] + 120
    nodes = node_by_id(model)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-40 -64 {width} {height}" role="img" aria-label="{esc(model["title"])}">',
        "<defs><marker id=\"arrow\" markerWidth=\"10\" markerHeight=\"10\" refX=\"8\" refY=\"3\" orient=\"auto\"><path d=\"M0,0 L0,6 L9,3 z\" fill=\"#111827\"/></marker></defs>",
        f'<text x="0" y="-28" font-family="system-ui, sans-serif" font-size="22" font-weight="700">{esc(model["title"])}</text>',
    ]
    for edge in model["edges"]:
        a = positions[edge["from"]]
        b = positions[edge["to"]]
        x1, y1 = a["x"] + NODE_W, a["y"] + NODE_H / 2
        x2, y2 = b["x"], b["y"] + NODE_H / 2
        lines.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#111827" stroke-width="2" fill="none" marker-end="url(#arrow)"/>')
        if edge.get("label"):
            lines.append(f'<text x="{(x1 + x2) / 2}" y="{(y1 + y2) / 2 - 6}" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12">{esc(edge["label"])}</text>')
    for node in model["nodes"]:
        pos = positions[node["id"]]
        fill = "#dbeafe" if node.get("type") == "page" else "#dcfce7"
        lines.append(f'<g data-node-id="{esc(node["id"])}">')
        lines.append(f'<rect x="{pos["x"]}" y="{pos["y"]}" width="{NODE_W}" height="{NODE_H}" rx="8" fill="{fill}" stroke="#111827"/>')
        lines.append(f'<text x="{pos["x"] + NODE_W / 2}" y="{pos["y"] + NODE_H / 2 + 6}" text-anchor="middle" font-family="system-ui, sans-serif" font-size="16" font-weight="600">{esc(node["label"])}</text>')
        if node.get("provenance"):
            lines.append(f'<title>{esc(nodes[node["id"]]["label"])} evidence: {esc(", ".join(node["provenance"]))}</title>')
        lines.append("</g>")
    if model.get("legend"):
        lx = size["width"] + 48
        lines.append(f'<g class="legend"><text x="{lx}" y="0" font-family="system-ui, sans-serif" font-size="14" font-weight="700">Legend</text>')
        for index, (key, value) in enumerate(model["legend"].items()):
            y = 24 + index * 22
            lines.append(f'<text x="{lx}" y="{y}" font-family="system-ui, sans-serif" font-size="12">{esc(key)}: {esc(value)}</text>')
        lines.append("</g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def render_html(model):
    svg = render_svg(model)
    return f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(normalize(model)['title'])}</title>
<style>
  :root {{ color-scheme: light; font-family: system-ui, sans-serif; }}
  body {{ margin: 0; background: #f8fafc; color: #111827; }}
  main {{ min-block-size: 100vh; padding: clamp(1rem, 2vw, 2rem); box-sizing: border-box; }}
  .surface {{ overflow: auto; background: white; border: 1px solid #d1d5db; border-radius: 8px; }}
  svg {{ display: block; min-inline-size: 720px; max-inline-size: none; }}
</style>
<main>
  <div class="surface">
{svg}
  </div>
</main>
</html>
"""


def selftest():
    model = selftest_model()
    svg = render_svg(model)
    html = render_html(model)
    ok = "<svg" in svg and "Home" in svg and "Legend" in svg and "<!doctype html>" in html
    print("GUILD-74 SVG/HTML renderer - self-test")
    print(f"   svg bytes: {len(svg)} html bytes: {len(html)}")
    print(f"\n{'PASS' if ok else 'FAIL'} - sample artifact rendered to SVG and HTML.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact")
    ap.add_argument("--out")
    ap.add_argument("--format", choices=("svg", "html"), default="html")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
    model = load_artifact(args.artifact) if args.artifact else sample_artifact()
    write_or_print(render_svg(model) if args.format == "svg" else render_html(model), args.out)


if __name__ == "__main__":
    main()
