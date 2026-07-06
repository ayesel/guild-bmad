#!/usr/bin/env python3
"""
ia-graph-gate.py - GUILD IA graph gate (ia-factors-research.md section 3, blockers 1 + 5).

Artifact-time graph health + addressability over the Cartographer sitemap
artifact. Deterministic, zero-threshold per the decision doc: orphans,
unintended dead ends, illegal cycles, list+detail completeness per entity
type, addressability (every node carries a URL; duplicate URLs are flagged),
and child-bearing hubs without a label.

  python3 scripts/ia-graph-gate.py --artifact sitemap.json
  python3 scripts/ia-graph-gate.py --artifact sitemap.json --json
  python3 scripts/ia-graph-gate.py --selftest

Artifact shape:
{
  "root": "home",
  "nodes": [
    {"id": "home", "type": "home",          # list|detail|hub|terminal|home
     "entity": "recipe",                    # optional entity-type id
     "label": "Home",
     "url": "/",                            # nullable
     "core_task": true}                     # optional
  ],
  "edges": [["home", "recipes"], ...],
  "polyhierarchy_declared": false
}

Failures block (exit 1). Flags warn (printed, JSON "flags", exit unaffected).
"""
import argparse
import json
import sys

HUBLIKE = {"hub", "home"}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def bfs(start, adj):
    seen = {start}
    queue = [start]
    while queue:
        cur = queue.pop()
        for nxt in adj.get(cur, []):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def sccs(node_ids, adj):
    """Iterative Kosaraju: returns list of strongly-connected components."""
    order, seen = [], set()
    for start in node_ids:
        if start in seen:
            continue
        stack = [(start, iter(adj.get(start, [])))]
        seen.add(start)
        while stack:
            node, it = stack[-1]
            advanced = False
            for nxt in it:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append((nxt, iter(adj.get(nxt, []))))
                    advanced = True
                    break
            if not advanced:
                order.append(node)
                stack.pop()
    radj = {nid: [] for nid in node_ids}
    for src, dsts in adj.items():
        for dst in dsts:
            radj[dst].append(src)
    comps, assigned = [], set()
    for start in reversed(order):
        if start in assigned:
            continue
        comp = bfs(start, {k: [d for d in v if d not in assigned] for k, v in radj.items()})
        comp -= assigned
        assigned |= comp
        comps.append(comp)
    return comps


def gate(artifact):
    failures, flags = [], []
    stats = {"list_detail_coverage": 100.0}
    nodes = artifact.get("nodes") or []
    if not nodes:
        return ["schema: artifact has no nodes"], flags, stats

    by_id = {}
    for node in nodes:
        nid = node.get("id")
        if nid is None:
            failures.append("schema: node without an id")
            continue
        if nid in by_id:
            failures.append(f"schema: duplicate node id '{nid}'")
        by_id[nid] = node

    root = artifact.get("root")
    if root not in by_id:
        failures.append(f"schema: root '{root}' is not a declared node")
        return failures, flags, stats

    adj = {nid: [] for nid in by_id}
    for edge in artifact.get("edges") or []:
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            failures.append(f"schema: malformed edge {edge!r}")
            continue
        src, dst = edge
        if src not in by_id or dst not in by_id:
            failures.append(f"schema: edge {list(edge)!r} references unknown node")
            continue
        adj[src].append(dst)

    # (a) orphans - nodes unreachable from root
    reachable = bfs(root, adj)
    for nid in by_id:
        if nid not in reachable:
            failures.append(f"orphan: node '{nid}' unreachable from root '{root}'")

    # (b) unintended dead ends - non-terminal nodes with out-degree 0
    #     or no forward path to any hub/home
    hublike_ids = {nid for nid, n in by_id.items() if n.get("type") in HUBLIKE}
    for nid, node in by_id.items():
        if node.get("type") == "terminal":
            continue
        if not adj[nid]:
            failures.append(f"dead end: non-terminal node '{nid}' has out-degree 0")
        elif not (bfs(nid, adj) & hublike_ids):
            failures.append(f"dead end: node '{nid}' has no path back to any hub/home")

    # (c) illegal cycles - SCCs > 1 node without declared polyhierarchy
    if not artifact.get("polyhierarchy_declared"):
        for comp in sccs(list(by_id), adj):
            if len(comp) > 1:
                members = ", ".join(sorted(comp))
                failures.append(
                    f"illegal cycle: nodes {{{members}}} form a cycle without polyhierarchy_declared"
                )

    # (d) list+detail completeness per entity type
    entities = sorted({n["entity"] for n in by_id.values() if n.get("entity")})
    if entities:
        complete = 0
        for ent in entities:
            has_list = any(n.get("entity") == ent and n.get("type") == "list" for n in by_id.values())
            has_detail = any(n.get("entity") == ent and n.get("type") == "detail" for n in by_id.values())
            if has_list and has_detail:
                complete += 1
            else:
                missing = [k for k, ok in (("list", has_list), ("detail", has_detail)) if not ok]
                failures.append(f"list+detail: entity '{ent}' missing {' and '.join(missing)} node")
        coverage = 100.0 * complete / len(entities)
        stats["list_detail_coverage"] = round(coverage, 1)
        if coverage < 100.0:
            failures.append(
                f"list+detail: coverage {coverage:.0f}% ({complete}/{len(entities)} entity types); required 100%"
            )

    # (e) addressability - every node has a url; duplicate urls flagged
    urls = {}
    for nid, node in by_id.items():
        url = node.get("url")
        if not url:
            failures.append(f"addressability: node '{nid}' has no url")
        else:
            urls.setdefault(url, []).append(nid)
    for url, ids in sorted(urls.items()):
        if len(ids) > 1:
            flags.append(f"duplicate url: '{url}' shared by nodes {', '.join(sorted(ids))}")

    # (f) child-bearing hubs without a label
    for nid, node in by_id.items():
        if node.get("type") == "hub" and adj[nid] and not str(node.get("label") or "").strip():
            failures.append(f"unlabeled hub: node '{nid}' has children but no label")

    return failures, flags, stats


def selftest():
    good = {
        "root": "home",
        "polyhierarchy_declared": True,
        "nodes": [
            {"id": "home", "type": "home", "label": "Home", "url": "/"},
            {"id": "recipes", "type": "list", "entity": "recipe", "label": "Recipes",
             "url": "/recipes", "core_task": True},
            {"id": "recipe", "type": "detail", "entity": "recipe", "label": "Recipe",
             "url": "/recipes/:id"},
        ],
        "edges": [["home", "recipes"], ["recipes", "recipe"], ["recipe", "home"]],
    }
    bad = {
        "root": "home",
        "polyhierarchy_declared": False,
        "nodes": [
            {"id": "home", "type": "home", "label": "Home", "url": "/"},
            {"id": "ghost", "type": "hub", "label": "Ghost", "url": "/ghost"},
            {"id": "hub1", "type": "hub", "label": "", "url": "/hub1"},
            {"id": "leaf", "type": "list", "entity": "recipe", "label": "Recipes", "url": None},
            {"id": "cyc1", "type": "hub", "label": "C1", "url": "/dup"},
            {"id": "cyc2", "type": "hub", "label": "C2", "url": "/dup"},
        ],
        "edges": [["home", "hub1"], ["hub1", "leaf"], ["home", "cyc1"],
                  ["cyc1", "cyc2"], ["cyc2", "cyc1"]],
    }
    good_failures, good_flags, good_stats = gate(good)
    bad_failures, bad_flags, _ = gate(bad)
    blob = "\n".join(bad_failures)
    expected = ["orphan:", "dead end:", "illegal cycle:", "list+detail:",
                "addressability:", "unlabeled hub:"]
    missing = [name for name in expected if name not in blob]
    ok = (not good_failures and not good_flags
          and good_stats["list_detail_coverage"] == 100.0
          and not missing
          and any("duplicate url:" in f for f in bad_flags))
    print("GUILD ia-graph gate - self-test")
    print(f"   clean sitemap failures: {len(good_failures)} flags: {len(good_flags)}")
    print(f"   defective sitemap failures: {len(bad_failures)} flags: {len(bad_flags)}")
    if missing:
        print(f"   MISSING checks: {', '.join(missing)}")
    print(f"\n{'PASS' if ok else 'FAIL'} - orphan, dead-end, cycle, list+detail, addressability, and hub-label checks exercised.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact", help="sitemap artifact JSON")
    ap.add_argument("--json", action="store_true", help="structured JSON output")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    if not a.artifact:
        sys.exit("pass --artifact <sitemap.json> or --selftest")
    failures, flags, stats = gate(load_json(a.artifact))
    if a.json:
        print(json.dumps({
            "gate": "ia-graph",
            "status": "NO-GO" if failures else "GO",
            "failures": failures,
            "flags": flags,
            "list_detail_coverage": stats["list_detail_coverage"],
        }, indent=2))
        sys.exit(1 if failures else 0)
    if failures:
        print("[NO-GO] ia graph gate failed")
        for failure in failures:
            print(f" - {failure}")
        for flag in flags:
            print(f" ~ {flag}")
        sys.exit(1)
    print(f"[GO] ia graph gate passed (list+detail coverage {stats['list_detail_coverage']:g}%)")
    for flag in flags:
        print(f" ~ {flag}")


if __name__ == "__main__":
    main()
