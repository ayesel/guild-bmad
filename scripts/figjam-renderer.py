#!/usr/bin/env python3
"""
figjam-renderer.py — GUILD-73 (T2): FigJam board-craft renderer + post-render QA.

Composes the canonical artifact model (GUILD-69) + deterministic layout (GUILD-71) +
semantic style (GUILD-72) into a FigJam BOARD spec, then runs board-craft QA so the
result isn't "just okay": every node placed + labeled + styled, no overlaps, a legend
present, framed with margins, token spacing. (The actual FigJam push is a thin execute
step over this spec via the Figma MCP; the renderer + QA is the card.)

  python3 scripts/figjam-renderer.py --artifact a.json --out board.json
  python3 scripts/figjam-renderer.py --selftest
"""
import os, sys, json, argparse, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
NW, NH, MARGIN = 160, 60, 48

def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def render(model):
    le = _load("le", "layout-engine.py"); st = _load("st", "ia-style.py")
    pos = le.layout(model)
    style = st.build(model)
    by_type = style["node_styles"]
    nodes = []
    for n in model.get("nodes", []):
        p = pos.get(n["id"], {"x": 0, "y": 0}); s = by_type.get(n.get("type"), {})
        nodes.append({"id": n["id"], "label": n.get("label", n["id"]),
                      "x": p["x"] + MARGIN, "y": p["y"] + MARGIN,
                      "fill": s.get("fill"), "border": s.get("border"), "shape": s.get("shape", "rect")})
    maxx = max([n["x"] for n in nodes], default=0) + NW + MARGIN
    maxy = max([n["y"] for n in nodes], default=0) + NH + MARGIN
    return {"title": model.get("type", "artifact"), "frame": {"w": maxx, "h": maxy},
            "nodes": nodes, "edges": model.get("edges", []), "legend": style["legend"],
            "edge_style": style["edge_style"]}

def post_render_qa(model, board):
    findings = []
    model_ids = {n["id"] for n in model.get("nodes", [])}
    board_ids = {n["id"] for n in board["nodes"]}
    missing = model_ids - board_ids
    if missing: findings.append(f"nodes not placed on the board: {sorted(missing)}")
    # overlaps
    bn = board["nodes"]
    for i in range(len(bn)):
        for j in range(i + 1, len(bn)):
            if abs(bn[i]["x"] - bn[j]["x"]) < NW and abs(bn[i]["y"] - bn[j]["y"]) < NH:
                findings.append(f"overlap: {bn[i]['id']} / {bn[j]['id']}")
    for n in bn:
        if not n.get("label"): findings.append(f"{n['id']}: no label")
        if not (n.get("fill") and n.get("border")): findings.append(f"{n['id']}: style not applied")
        if n["x"] < MARGIN or n["y"] < MARGIN: findings.append(f"{n['id']}: outside frame margin")
    if not board.get("legend"): findings.append("no legend (board-craft: every board needs a key)")
    return findings

def selftest():
    model = {"type": "sitemap", "layout_contract": {"engine": "tree"},
             "nodes": [{"id": "home", "label": "Home", "type": "page"},
                       {"id": "today", "label": "Today", "type": "page"},
                       {"id": "log", "label": "Log", "type": "step"},
                       {"id": "decide", "label": "Goal met?", "type": "decision"}],
             "edges": [{"from": "home", "to": "today"}, {"from": "home", "to": "log"}, {"from": "home", "to": "decide"}]}
    board = render(model)
    qa = post_render_qa(model, board)
    # broken board: drop a node + remove legend
    broken = json.loads(json.dumps(board)); broken["nodes"] = broken["nodes"][:-1]; broken["legend"] = []
    qb = post_render_qa(model, broken)
    print("GUILD-73 FigJam renderer + board-craft QA — self-test")
    print(f"   board: {len(board['nodes'])} nodes, frame {board['frame']['w']}x{board['frame']['h']}, legend {len(board['legend'])}")
    print(f"   clean board QA findings: {len(qa)} | broken board QA findings: {len(qb)}")
    ok = (len(qa) == 0 and len(board["nodes"]) == 4 and board["legend"]
          and any("not placed" in x for x in qb) and any("no legend" in x for x in qb))
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — composes 69+71+72 into a clean board (placed/styled/legend/no-overlap); broken board flagged.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact"); ap.add_argument("--out"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.artifact:
        model = json.load(open(a.artifact)); board = render(model); qa = post_render_qa(model, board)
        out = a.out or "board.json"; json.dump(board, open(out, "w"), indent=2)
        print(f"rendered {len(board['nodes'])}-node board -> {out}; board-craft QA: {len(qa)} finding(s)")
        for x in qa: print(" ✗", x)
        sys.exit(0 if not qa else 1)
    sys.exit("pass --artifact <f> or --selftest")

if __name__ == "__main__":
    main()
