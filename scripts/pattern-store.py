#!/usr/bin/env python3
"""
pattern-store.py — GUILD pattern memory (card f18c0a39). The amnesia cure.

Patterns are OPERATOR knowledge (like taste): descriptors of designs the owner
has already built/approved, with provenance pointers to the real project+file —
never client code copies. Stored in ~/.config/guild/patterns/ (per GUILD-75:
operator-owned, cross-project, private, travels with the operator not any repo).

Rogue/Mage query this BEFORE designing anything and PROPOSE reuse with
provenance: "you built a filterable status table in wedding-hub — reuse it?"

  python3 scripts/pattern-store.py seed --from <harvest.yaml>     # merge descriptors in
  python3 scripts/pattern-store.py list
  python3 scripts/pattern-store.py match --query "table with totals for tracked vendors"
  python3 scripts/pattern-store.py match --data-shape "growable collection"
  python3 scripts/pattern-store.py --selftest
"""
import os, re, sys, json, argparse

STORE = os.path.expanduser(os.environ.get("GUILD_PATTERN_STORE", "~/.config/guild/patterns"))
FILE = os.path.join(STORE, "patterns.yaml")


def _yaml():
    import yaml
    return yaml


def load():
    if not os.path.exists(FILE): return []
    return _yaml().safe_load(open(FILE)).get("patterns", []) or []


def save(patterns):
    os.makedirs(STORE, exist_ok=True)
    _yaml().safe_dump({"patterns": patterns}, open(FILE, "w"), sort_keys=False, allow_unicode=True, width=110)


def seed(from_path):
    incoming = _yaml().safe_load(open(from_path)).get("patterns", [])
    existing = {p["id"]: p for p in load()}
    added = updated = 0
    for p in incoming:
        if p["id"] in existing: updated += 1
        else: added += 1
        existing[p["id"]] = p
    save(list(existing.values()))
    print(f"pattern store: +{added} new, {updated} updated, {len(existing)} total -> {FILE}")


def _tokens(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def match(query="", data_shape="", top=5):
    q = _tokens(query) | _tokens(data_shape)
    scored = []
    for p in load():
        hay_kw = _tokens(" ".join(p.get("intent_keywords", []))) | _tokens(p.get("name", ""))
        hay_ds = _tokens(" ".join(p.get("data_shape", [])))
        hay_all = hay_kw | hay_ds | _tokens(p.get("problem", ""))
        score = 3 * len(q & hay_kw) + 3 * len(q & hay_ds) + len(q & hay_all)
        if score > 0:
            scored.append((score, p))
    scored.sort(key=lambda s: -s[0])
    return [(s, p) for s, p in scored[:top]]


def show_matches(results):
    if not results:
        print("no pattern matches — this may genuinely be new ground"); return
    for score, p in results:
        prov = p.get("provenance", {})
        print(f"[{score:>2}] {p['id']} — {p['name']}")
        print(f"     {p.get('problem','')[:110]}")
        print(f"     provenance: {prov.get('project')}:{prov.get('file')} ({prov.get('status')})")
        print(f"     includes: {', '.join(p.get('affordances', [])[:8])}")


def selftest():
    import tempfile
    global STORE, FILE
    with tempfile.TemporaryDirectory() as td:
        old_store, old_file = STORE, FILE
        STORE, FILE = td, os.path.join(td, "patterns.yaml")
        try:
            harvest = os.path.join(td, "h.yaml")
            open(harvest, "w").write("""
patterns:
  - id: t-table
    name: Filterable Table
    kind: surface
    problem: find records fast
    data_shape: ["growable collection", "status enum"]
    intent_keywords: [table, filter, tracker]
    affordances: [search, filter, sort]
    provenance: { project: p, file: f, status: shipped }
  - id: t-ring
    name: Progress Ring
    kind: component
    problem: value vs target at a glance
    data_shape: ["value-vs-target quantity"]
    intent_keywords: [ring, progress, goal]
    affordances: [sweep, count-up]
    provenance: { project: p, file: g, status: shipped }
""")
            seed(harvest)
            m1 = match(query="a tracker table with filters")
            m2 = match(data_shape="value-vs-target quantity")
            ok = (len(load()) == 2
                  and m1 and m1[0][1]["id"] == "t-table"
                  and m2 and m2[0][1]["id"] == "t-ring")
            seed(harvest)  # idempotent merge
            ok = ok and len(load()) == 2
        finally:
            STORE, FILE = old_store, old_file
    print("pattern-store self-test:", "✅ PASS" if ok else "❌ FAIL")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", choices=["seed", "list", "match"])
    ap.add_argument("--from", dest="from_path"); ap.add_argument("--query", default="")
    ap.add_argument("--data-shape", default=""); ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.cmd == "seed":
        if not a.from_path: sys.exit("seed needs --from <harvest.yaml>")
        seed(a.from_path)
    elif a.cmd == "list":
        for p in load():
            print(f"{p['id']:<32} {p.get('kind','?'):<14} {p.get('provenance',{}).get('project','?')}")
        print(f"{len(load())} patterns in {FILE}")
    elif a.cmd == "match":
        results = match(a.query, a.data_shape)
        if a.json: json.dump([p for _, p in results], sys.stdout, indent=1)
        else: show_matches(results)
    else:
        sys.exit("usage: pattern-store.py seed|list|match (or --selftest)")


if __name__ == "__main__":
    main()
