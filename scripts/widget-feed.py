#!/usr/bin/env python3
"""
widget-feed.py — the GUILD widget's DATA LAYER (card 026d669e).

ONE feed builder per project: gate exits, runs, needs-you (open exceptions +
decision packets), journey (quest/state phases), suggestions, artifact library.
The renderer (guild-widget.py) is a pure projection of this feed — the SAME
feed backs the atrium canvas note today and Jonny's pane API later. No state
of its own; everything is read from the project's files on every call.

  python3 scripts/widget-feed.py --project ~/Developer/apps/nourish   # JSON to stdout
  python3 scripts/widget-feed.py --selftest
"""
import os, re, sys, json, glob, argparse, subprocess

try:
    import yaml
except ImportError:
    yaml = None


def _yaml(path):
    if not os.path.exists(path): return {}
    if yaml:
        try: return yaml.safe_load(open(path)) or {}
        except Exception: return {}
    return {}



def _trunc(s, n):
    s = re.sub(r"\s+", " ", str(s)).strip()
    if len(s) <= n: return s
    cut = s[:n].rsplit(" ", 1)[0]
    return cut + " …"

def _out_root(root):
    for cand in ("_bmad-output", "guild-output"):
        p = os.path.join(root, cand)
        if os.path.isdir(p): return p
    return None   # engine-repo self mode


def _phases_from_state(out_root):
    """Newest *state.yaml with a phases: map wins (quest-state, v2-redesign-state, ...)."""
    states = sorted(glob.glob(os.path.join(out_root, "*state*.yaml")), key=os.path.getmtime, reverse=True)
    for s in states:
        d = _yaml(s)
        if isinstance(d.get("phases"), dict):
            out = []
            for name, ph in d["phases"].items():
                ph = ph or {}
                out.append({"name": name, "status": str(ph.get("status", "")),
                            "note": str(ph.get("note", ""))[:140]})
            title = d.get("quest") or os.path.basename(s)
            stop = d.get("stop-point") or d.get("stop_point") or ""
            return {"title": str(title), "phases": out, "stop_point": str(stop)[:200], "source": os.path.basename(s)}
    return None


def _phases_from_forge(root):
    """Engine-repo self mode: the FORGE queue IS the journey."""
    fp = os.path.join(root, "docs", "guild", "FORGE-PROMPT.md")
    if not os.path.exists(fp): return None
    text = open(fp, encoding="utf-8").read()
    m = re.search(r"## 3\. THE QUEUE.*?\n(.*?)\n## ", text, re.S)
    if not m: return None
    phases = []
    for line in m.group(1).splitlines():
        item = re.match(r"^(\d+)\.\s+(.*)", line.strip())
        if not item: continue
        body = item.group(2)
        done = body.startswith("~~")
        name = re.sub(r"[~*]|\(card [^)]*\)", "", body.split("—")[0].split(":")[0]).strip()
        phases.append({"name": name[:60], "status": "done" if done else "queued", "note": ""})
    return {"title": "GUILD forge queue", "phases": phases, "stop_point": "", "source": "FORGE-PROMPT.md"} if phases else None


def _runs(art_root):
    runs = []
    for p in sorted(glob.glob(os.path.join(art_root, "runs", "RUN-*.yaml")), reverse=True):
        # skip schema/template docs (e.g. RUN-schema.yaml) — they match the glob but aren't runs
        if re.search(r"(schema|template|example)", os.path.basename(p), re.I): continue
        d = _yaml(p)
        if not d: continue
        # a real run has an identity/state; a bare schema doc does not
        if not (d.get("run_id") or d.get("state") or d.get("checkpoints") or d.get("objective")): continue
        runs.append({
            "id": d.get("run_id", os.path.basename(p)),
            "state": d.get("state", "unknown"),
            "objective": re.sub(r"\s+", " ", str(d.get("objective", "")))[:160],
            "checkpoints": len(d.get("checkpoints") or []),
            "open_exceptions": [str(x) for x in (d.get("open_exceptions") or [])],
            "path": p,
        })
    return runs


def _gate_exits(runs):
    """Pull 'X EXIT n' evidence from the newest run's checkpoints."""
    gates = []
    if not runs: return gates
    d = _yaml(runs[0]["path"])
    for c in d.get("checkpoints") or []:
        for m in re.finditer(r"([a-z0-9-]+(?:-gate|-lint(?:ers)?|smoke|build|suite)?[^:\"]{0,24}?)\s+EXIT\s+(\d)", str(c), re.I):
            name = m.group(1).strip().split()[-1][:28]
            gates.append({"gate": name, "exit": int(m.group(2))})
    seen, out = set(), []
    for g in gates:
        if g["gate"] in seen: continue
        seen.add(g["gate"]); out.append(g)
    return out[:10]


def _pending_picks(art_root):
    picks = []
    for m in glob.glob(os.path.join(art_root, "regenerate", "*", "manifest.yaml")):
        d = _yaml(m)
        if d and d.get("pick") in (None, "null"):
            picks.append({"id": "PICK", "title": f"Pick a treatment · {d.get('set','?')}",
                          "detail": _trunc(d.get("comment", ""), 140),
                          "link": m, "variants": len(d.get("variants") or {})})
    return picks


def _needs_you(art_root, runs):
    needs = list(_pending_picks(art_root))
    packets = sorted(glob.glob(os.path.join(art_root, "batched-review-*.md")), key=os.path.getmtime, reverse=True)
    packet = packets[0] if packets else None
    if packet:
        text = open(packet, encoding="utf-8").read()
        for m in re.finditer(r"\*\*(D\d+)\s*—\s*([^*]{5,90})\*\*\s*([^\n]{0,220})", text):
            detail = re.sub(r"\s+", " ", m.group(3)).strip(" —-") or "open the packet for the evidence"
            if detail and detail[0].islower(): detail = "… " + detail
            needs.append({"id": m.group(1), "title": m.group(2).strip().rstrip("?.").strip(),
                          "detail": _trunc(detail, 200), "link": packet})
    if runs:
        for x in runs[0]["open_exceptions"]:
            first = x.split(":")[0].strip()
            title = (first[:57] + "…") if len(first) > 58 else first
            if any(n["id"] in x[:12] for n in needs): continue   # D1-D4 already listed via packet
            needs.append({"id": "note", "title": title, "detail": _trunc(x, 200), "link": runs[0]["path"]})
    return needs[:6], packet


def _library(art_root, limit=40):
    """The product-design hub: EVERYTHING the project's design work produced,
    grouped — decisions, research, design artifacts, specs — 2 levels deep."""
    groups = {"decisions": [], "research": [], "design": [], "specs & docs": [], "other": []}
    def classify(base):
        b = base.lower()
        if "batched-review" in b or "decision" in b or "verdict" in b or "pick" in b: return "decisions"
        if "spine" in b or "persona" in b or "research" in b or "synthesis" in b or "interview" in b: return "research"
        if b.endswith((".png", ".html", ".svg", ".gif")) or "mock" in b or "wireframe" in b or "screenshot" in b \
           or "prototype" in b or "render" in b or "figma" in b or "regenerate" in b: return "design"
        if b.endswith((".md", ".yaml", ".json")): return "specs & docs"
        return "other"
    if not os.path.isdir(art_root): return []
    for entry in sorted(glob.glob(os.path.join(art_root, "*")), key=os.path.getmtime, reverse=True):
        base = os.path.basename(entry)
        if base == "runs" or base.startswith("."): continue
        if os.path.isdir(entry):
            kids = sorted(glob.glob(os.path.join(entry, "*")), key=os.path.getmtime, reverse=True)
            for k in kids[:6]:
                kb = os.path.basename(k)
                if kb.startswith("."): continue
                groups[classify(kb)].append({"name": f"{base}/{kb}"[:56], "path": k,
                                             "mtime": int(os.path.getmtime(k))})
        else:
            groups[classify(base)].append({"name": base[:56], "path": entry,
                                           "mtime": int(os.path.getmtime(entry))})
    out = []
    for g, items in groups.items():
        for it in items[:12]:
            it["kind"] = g
            out.append(it)
    out.sort(key=lambda x: (x["kind"], -x["mtime"]))
    return out[:limit]


def _suggestions(root, runs, needs):
    sug_file = _yaml(os.path.join(root, "docs", "guild", "suggestions.yaml"))
    if isinstance(sug_file, dict) and sug_file.get("suggestions"):
        return [{"title": str(s.get("title", s))[:90], "cite": str(s.get("cite", ""))[:80]}
                for s in sug_file["suggestions"][:3]]
    out = [{"title": f"Answer {n['id']} — {n['title']}", "cite": os.path.basename(n["link"] or "")} for n in needs[:3]]
    if not out and runs:
        out = [{"title": "Review latest run record", "cite": runs[0]["id"]}]
    return out


def _cards():
    cli = os.environ.get("ATRIUM_CLI_PATH")
    if not cli: return []
    try:
        r = subprocess.run([cli, "task", "list", "--json"], capture_output=True, text=True, timeout=10)
        tasks = json.loads(r.stdout)
        tasks = tasks if isinstance(tasks, list) else tasks.get("tasks", [])
        live = [t for t in tasks if str(t.get("status", {}).get("name", t.get("status", ""))) in ("In Progress", "In Review")]
        return [{"title": t.get("title", "")[:60],
                 "status": str(t.get("status", {}).get("name", t.get("status", "")))} for t in live[:4]]
    except Exception:
        return []



_WALK_PRUNE = {"node_modules", ".git", "dist", "build", ".next", ".venv", "__pycache__", "_backups"}

def _design_system(root):
    """Surface the project's design-system assets: Storybook, DTCG tokens, Claude Design bundles, DS specs.

    PERF (goal 2026-07-07 'make GUILD extremely fast'): one bounded, PRUNED walk
    (depth <=4, node_modules/.git/dist skipped BEFORE descent) replaces three
    recursive ** globs that walked the whole tree — that was 83% of a
    1.5s-per-project feed build (24k directory reads per page render)."""
    import fnmatch
    ds = []
    if os.path.isdir(os.path.join(root, ".storybook")):
        ds.append({"name": "Storybook", "kind": "storybook", "path": os.path.join(root, ".storybook"),
                   "hint": "component workshop — run its dev server to browse"})
    token_hits, cd_hits = [], []
    base_depth = root.rstrip(os.sep).count(os.sep)
    for dirpath, dirnames, filenames in os.walk(root):
        depth = dirpath.count(os.sep) - base_depth
        if depth >= 4:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in _WALK_PRUNE]
        for d in list(dirnames):
            if d in ("cd-seed", "claude-design-bundle") or fnmatch.fnmatch(d, "*claude-design*"):
                cd_hits.append(os.path.join(dirpath, d))
        for f in filenames:
            if fnmatch.fnmatch(f, "tokens*.json") or fnmatch.fnmatch(f, "*.dtcg.json"):
                token_hits.append(os.path.join(dirpath, f))
            elif fnmatch.fnmatch(f, "*claude-design*"):
                cd_hits.append(os.path.join(dirpath, f))
        if len(token_hits) >= 2 and len(cd_hits) >= 2:
            break
    for f in token_hits[:2]:
        ds.append({"name": os.path.basename(f), "kind": "tokens", "path": f, "hint": "design tokens (DTCG)"})
    for f in cd_hits[:2]:
        ds.append({"name": os.path.basename(f), "kind": "claude-design", "path": f, "hint": "Claude Design bundle"})
    for f in (os.path.join(root, "docs", "guild", "design-system.yaml"),):
        if os.path.exists(f):
            ds.append({"name": "design-system.yaml", "kind": "ds-spec", "path": f, "hint": "Guild design-system spec"})
    seen, out = set(), []
    for d in ds:
        if d["path"] in seen: continue
        seen.add(d["path"]); out.append(d)
    return out[:6]

def build(root):
    root = os.path.abspath(os.path.expanduser(root))
    out_root = _out_root(root)
    art_root = os.path.join(out_root, "guild-artifacts") if out_root else os.path.join(root, "guild-artifacts")
    runs_root = art_root if os.path.isdir(os.path.join(art_root, "runs")) else os.path.join(root, "docs", "guild")
    runs = _runs(runs_root)
    needs, packet = _needs_you(art_root, runs)
    journey = (_phases_from_state(out_root) if out_root else None) or _phases_from_forge(root)
    spine = os.path.join(art_root, "spine.json")
    spine_n = len(json.load(open(spine))) if os.path.exists(spine) else 0
    pstore = os.path.expanduser("~/.config/guild/patterns/patterns.yaml")
    patterns = len((_yaml(pstore) or {}).get("patterns", [])) if os.path.exists(pstore) else 0
    return {
        "patterns": patterns,
        "project": os.path.basename(root),
        "root": root,
        "mode": "project" if out_root else "engine",
        "journey": journey,
        "runs": runs[:4],
        "gates": _gate_exits(runs),
        "needs_you": needs,
        "packet": packet,
        "suggestions": _suggestions(root, runs, needs),
        "library": _library(art_root),
        "spine_nuggets": spine_n,
        "cards": _cards(),
        "design_system": _design_system(root),
    }


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        art = os.path.join(td, "_bmad-output", "guild-artifacts", "runs"); os.makedirs(art)
        open(os.path.join(td, "_bmad-output", "quest-state.yaml"), "w").write(
            'quest: "T"\nphases:\n  a: { status: done }\n  b: { status: now }\n')
        open(os.path.join(art, "RUN-2026-01-01-001.yaml"), "w").write(
            'run_id: "RUN-1"\nstate: done\nobjective: "x"\ncheckpoints:\n  - "responsive-gate EXIT 0"\n  - "fidelity-gate EXIT 1"\nopen_exceptions:\n  - "D9: decide something"\n')
        f = build(td)
        ok = (f["mode"] == "project" and f["journey"] and len(f["journey"]["phases"]) == 2
              and f["runs"][0]["id"] == "RUN-1"
              and {"gate": "responsive-gate", "exit": 0} in f["gates"]
              and {"gate": "fidelity-gate", "exit": 1} in f["gates"]
              and f["needs_you"])
    print("widget-feed self-test:", "✅ PASS" if ok else "❌ FAIL")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=os.getcwd())
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    json.dump(build(a.project), sys.stdout, indent=1)


if __name__ == "__main__":
    main()
