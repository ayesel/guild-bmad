#!/usr/bin/env python3
"""guild-suggest — proactive HCI improvement suggestions (owner ask 2026-07-02).

The brain doesn't just gate what exists — it proposes what SHOULD exist. This
sweeps a project's UI surfaces and emits ranked, evidence-cited UX/interaction
improvement suggestions from three honest sources:

  1. affordance canon gaps   — docs/guild/affordances.yaml via affordance-check
                                (required affordances the surface fired but lacks)
  2. baseline trigger misses — product-baseline T-table heuristics detectable
                                statically (collections without find controls,
                                destructive actions without undo/confirm,
                                icon-only buttons, missing empty states)
  3. pattern opportunities   — ~/.config/guild/patterns/patterns.yaml patterns
                                whose data-shape keywords appear in the code but
                                whose affordances don't

Static analysis is honest about its limits: every suggestion cites file +
evidence, and heuristic ones are marked confidence: check (verify by eye)
vs firm (canon-required). Output: {artifacts}/guild-artifacts/suggestions.yaml
+ a readable summary. Advisory by default (exit 0); --gate exits 1 on firm gaps.
"""
import argparse, glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATTERN_STORE = os.path.expanduser("~/.config/guild/patterns/patterns.yaml")

UI_GLOBS = ["src/**/*.tsx", "src/**/*.jsx", "src/**/*.vue", "src/**/*.svelte",
            "app/**/*.tsx", "*.html", "src/**/*.html", "templates/**/*.html"]
SKIP = re.compile(r"(\.test\.|\.spec\.|__tests__|node_modules|\.next|dist/)")


def ui_files(root, cap=40):
    out = []
    for g in UI_GLOBS:
        out += [f for f in glob.glob(os.path.join(root, g), recursive=True) if not SKIP.search(f)]
    out = sorted(set(out), key=lambda f: -os.path.getsize(f))
    return out[:cap]


def artifacts_dir(root):
    for base in ("_bmad-output", "guild-output"):
        d = os.path.join(root, base, "guild-artifacts")
        if os.path.isdir(os.path.join(root, base)):
            os.makedirs(d, exist_ok=True)
            return d
    d = os.path.join(root, "guild-output", "guild-artifacts")
    os.makedirs(d, exist_ok=True)
    return d


def rel(root, f):
    return os.path.relpath(f, root)


# ── source 1: affordance canon (firm — these are required by docs/guild/affordances.yaml)
# Page-level surfaces only: a component's internal .map doesn't owe search controls — its page does.
PAGE_LEVEL = re.compile(r"(page|screen|view|route|index)\.(tsx|jsx|vue|svelte)$|\.html$", re.I)


# jargon stays in `detail` for agents; `title`/`why` speak plain English (owner rule 2026-07-02)
PLAIN = {
    "search": ("Let people search this", "the list can grow, but there is no way to type and find something in it"),
    "filter": ("Let people narrow this list", "no way to cut the list down to just what matters right now"),
    "sort": ("Let people reorder this list", "no way to change the order - newest first, biggest first, A to Z"),
    "empty-state": ("Show something helpful when this is empty", "an empty list shows blank space instead of telling people what to do next"),
    "zero-results": ('Say "no matches" when a search finds nothing', "a search that finds nothing looks broken unless the screen says so"),
    "row-actions": ("Let people act on each item in place", "people expect to edit or act on an item right where they see it, not hunt another screen"),
    "totals": ("Show the totals", "a list of numbers is expected to add up somewhere visible"),
    "count": ("Show how many there are", "a simple count tells people the size of what they are looking at"),
    "text-labels": ("Put words on the icons", "icons alone make people guess what a button does"),
    "grouping": ("Group items by category", "records with categories should arrive grouped, with subtotals"),
    "bulk-actions": ("Let people select several and act once", "doing the same thing twenty times is the app's job, not the user's"),
    "undo": ("Give people an undo", "mistakes need a way back"),
}


def canon_gaps(root, files):
    sugg = []
    for f in files:
        if not PAGE_LEVEL.search(f):
            continue
        try:
            r = subprocess.run([sys.executable, os.path.join(HERE, "affordance-check.py"),
                                "--screen", f, "--json"], capture_output=True, text=True, timeout=30)
            data = json.loads(r.stdout or "{}")
        except Exception:
            continue
        for g in data.get("gaps", []):
            name = (g.split(":")[-1].strip() if ":" in g else g).split(" ")[0]
            title, why = PLAIN.get(name, (f"Add {name}", f"screens like this are expected to have {name}, and it is not there"))
            sugg.append({"title": title, "why": why, "evidence": rel(root, f), "detail": g,
                         "source": "affordance-canon", "confidence": "firm"})
    return sugg


# ── source 2: baseline trigger heuristics (check — static analysis, verify by eye)
HEUR = [
    (re.compile(r"\.map\(|\<table|v-for=|\{#each"), re.compile(r"search|filter|sort|query", re.I),
     "Give this collection find controls",
     "this list grows over time, but there's no way to search or narrow it — people will end up scrolling to hunt"),
    (re.compile(r"\b(delete|remove|destroy|clear[A-Z_]|reset[A-Z_])", re.I), re.compile(r"undo|confirm|dialog|are you sure|revert", re.I),
     "Guard the destructive action with undo or confirm",
     "something here deletes or clears, and there's no undo and no 'are you sure' — one slip loses work"),
    (re.compile(r"\.map\(|\{#each|v-for="), re.compile(r"empty|no [a-z]+ yet|nothing|zero.state|placeholder", re.I),
     "Design the empty state",
     "when this list is empty, people see blank space instead of what to do next"),
    (re.compile(r"status\s*[:=]|state\s*[:=]\s*['\"](?:pending|active|open|done)", re.I), re.compile(r"count|rollup|summary|total", re.I),
     "Roll up status counts",
     "items here have statuses, but nothing shows the counts at a glance — including the unhappy ones"),
]
# JSX attrs contain "=>" so we anchor on the CLOSE: an svg (or lone emoji) directly
# against </button> means the button renders no text.
ICON_ONLY = re.compile(r"(?:</svg>|[←-➿\U0001f300-\U0001faff])\s*</button>", re.I)


def heuristics(root, files):
    sugg = []
    for f in files:
        try:
            src = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for fires, satisfies, title, why in HEUR:
            if fires.search(src) and not satisfies.search(src):
                sugg.append({"title": title, "why": why, "evidence": rel(root, f),
                             "source": "product-baseline", "confidence": "check"})
        for m in ICON_ONLY.finditer(src):
            frag = src[max(0, m.start() - 500):m.end()]
            frag = frag[frag.rfind("<button"):]
            if "aria-label" not in frag and "title=" not in frag:
                sugg.append({"title": "Put words on the icon-only button",
                             "why": "a button is just a picture — no words anywhere, so people (and screen readers) have to guess",
                             "evidence": rel(root, f), "source": "product-baseline", "confidence": "firm"})
                break
    return sugg


# ── source 3: pattern memory — harvested patterns whose shape fits but affordances are absent
def pattern_opps(root, files):
    try:
        import yaml
        pats = (yaml.safe_load(open(PATTERN_STORE)) or {}).get("patterns", [])
    except Exception:
        return []
    corpus = ""
    for f in files[:20]:
        try:
            corpus += open(f, encoding="utf-8", errors="ignore").read().lower()
        except OSError:
            pass
    sugg = []
    for p in pats:
        kws = [k.lower() for k in p.get("intent_keywords", [])]
        hits = [k for k in kws if len(k) > 3 and k in corpus]
        affs = [a.lower().replace("-", "") for a in p.get("affordances", [])]
        present = any(a[:14] in corpus.replace("-", "").replace("_", "") for a in affs if len(a) > 8)
        if len(hits) >= 2 and not present:
            sugg.append({"title": f'Consider the "{p.get("name", p["id"])}" pattern',
                         "why": f'this screen deals with {", ".join(hits[:3])} — Guild remembers a design that solved '
                                f'this well before: {(p.get("problem") or "").strip()[:110]}',
                         "detail": p["id"],
                         "evidence": f'pattern memory · matched keywords: {", ".join(hits[:4])}',
                         "source": "pattern-memory", "confidence": "check"})
    return sugg[:5]


def dedupe(sugg):
    seen, out = set(), []
    for s in sugg:
        k = (s["title"], s["evidence"])
        if k not in seen:
            seen.add(k)
            out.append(s)
    return out


def run(root):
    files = ui_files(root)
    sugg = dedupe(canon_gaps(root, files) + heuristics(root, files) + pattern_opps(root, files))
    order = {"firm": 0, "check": 1}
    sugg.sort(key=lambda s: (order[s["confidence"]], s["source"]))
    return {"project": root, "screens_swept": [rel(root, f) for f in files], "suggestions": sugg}


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "src"))
        open(os.path.join(td, "src", "list.tsx"), "w").write(
            "export const L = ({items}) => <div>{items.map(i => <Row key={i.id} {...i}/>)}"
            "<button onClick={() => deleteAll()}><svg><path d='m0 0'/></svg></button></div>")
        r = run(td)
        titles = [s["title"] for s in r["suggestions"]]
        blob = " ".join(s["title"] + " " + s["why"] for s in r["suggestions"]).lower()
        jargon = [w for w in ("affordance", "canon", "fired pattern", "enum", "baseline t") if w in blob]
        if jargon:
            print("   jargon leaked into owner-facing text:", jargon)
        ok = (not jargon and any("find controls" in t for t in titles) and any("undo or confirm" in t for t in titles)
              and any("empty state" in t for t in titles) and any("icon-only" in t for t in titles))
        # a surface with nothing wrong stays quiet
        open(os.path.join(td, "src", "list.tsx"), "w").write(
            "export const L = () => <div>hello</div>")
        ok = ok and not run(td)["suggestions"]
    print("guild-suggest self-test:", "✅ PASS" if ok else "❌ FAIL")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".")
    ap.add_argument("--gate", action="store_true", help="exit 1 if any firm suggestion exists")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    root = os.path.abspath(os.path.expanduser(a.project))
    result = run(root)
    import yaml
    out = os.path.join(artifacts_dir(root), "suggestions.yaml")
    yaml.safe_dump(result, open(out, "w"), sort_keys=False, allow_unicode=True, width=110)
    firm = [s for s in result["suggestions"] if s["confidence"] == "firm"]
    print(f"guild-suggest · swept {len(result['screens_swept'])} screens · "
          f"{len(result['suggestions'])} suggestions ({len(firm)} firm) → {out}")
    for s in result["suggestions"][:12]:
        print(f"  [{s['confidence']:5}] {s['title']} — {s['evidence']}")
    sys.exit(1 if (a.gate and firm) else 0)


if __name__ == "__main__":
    main()
