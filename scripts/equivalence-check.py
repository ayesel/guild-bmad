#!/usr/bin/env python3
"""
equivalence-check.py — component-equivalence / dedup v1 (card 605313e1).

Owner ask 2026-06-30: detect when 2+ UI elements do the SAME JOB but DON'T match
(two divergent primary buttons), even before the product is componentized.
v1 heuristic: scan an app's source for button-like elements, cluster by JOB
(the label's intent verb — save/add/remove/cancel/edit/open...), and inside each
job compare implementation signatures (component used + variant + class shape).
Same job + different signatures = a SUGGESTION to consolidate, with every
location cited. Suggests, never merges (GUILD-85: the owner picks the canonical).

  python3 scripts/equivalence-check.py --app <src-root> [--json]
  python3 scripts/equivalence-check.py --selftest
Exit 0 = no divergent same-job clusters; 1 = findings.
"""
import os, re, sys, json, glob, argparse
from collections import defaultdict

JOBS = {
    "save":    r'\b(save|submit|apply|confirm|done|finish)\b',
    "add":     r'\b(add|create|new|log|\+)\b',
    "remove":  r'\b(remove|delete|clear|discard)\b',
    "cancel":  r'\b(cancel|back|close|dismiss)\b',
    "edit":    r'\b(edit|rename|change|update)\b',
    "open":    r'\b(open|view|see|details?)\b',
}

BTN = re.compile(
    r'<(?P<comp>Button|button|IconButton|[A-Z]\w*Button)\b(?P<attrs>[^>]{0,400}?)>'
    r'(?P<label>[^<{]{0,60})', re.S)


def signature(comp, attrs):
    variant = (re.search(r'variant=["\{]*["\']?(\w+)', attrs) or [None, "-"])[1]
    classes = re.search(r'className=["\{]*["\']([^"\'}]+)', attrs)
    cls_shape = "-"
    if classes:
        toks = sorted({c.split("-")[0].split(":")[-1] for c in classes.group(1).split()[:12]})
        cls_shape = ",".join(toks[:8])
    return f"{comp}/{variant}/{cls_shape}"


def scan(app_root):
    hits = []
    for f in glob.glob(os.path.join(app_root, "**", "*.tsx"), recursive=True):
        if "__tests__" in f or ".test." in f: continue
        try: src = open(f, encoding="utf-8").read()
        except OSError: continue
        for m in BTN.finditer(src):
            label = m.group("label").strip()
            aria = re.search(r'aria-label=["\']([^"\']+)', m.group("attrs"))
            text = (label or (aria.group(1) if aria else "")).strip()
            if not text: continue
            job = next((j for j, pat in JOBS.items() if re.search(pat, text, re.I)), None)
            if not job: continue
            line = src[:m.start()].count("\n") + 1
            hits.append({"job": job, "text": text[:30], "sig": signature(m.group("comp"), m.group("attrs")),
                         "loc": f"{os.path.relpath(f, app_root)}:{line}"})
    return hits


def findings(hits):
    by_job = defaultdict(list)
    for h in hits: by_job[h["job"]].append(h)
    out = []
    for job, rows in by_job.items():
        sigs = defaultdict(list)
        for r in rows: sigs[r["sig"]].append(r)
        if len(sigs) > 1:
            out.append({
                "job": job,
                "implementations": {s: [f'{r["loc"]} ("{r["text"]}")' for r in rs] for s, rs in sigs.items()},
                "suggestion": f"{len(rows)} '{job}' actions use {len(sigs)} different implementations — "
                              f"consolidate to one canonical (owner picks which), or record why they differ.",
            })
    return out


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        open(os.path.join(td, "a.tsx"), "w").write(
            '<Button variant="primary">Save</Button><Button variant="primary">Save meal</Button>')
        open(os.path.join(td, "b.tsx"), "w").write(
            '<button className="bg-red px-2">Save now</button>')
        f = findings(scan(td))
        ok = len(f) == 1 and f[0]["job"] == "save" and len(f[0]["implementations"]) == 2
    print("equivalence-check self-test:", "✅ PASS" if ok else "❌ FAIL")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app"); ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if not a.app: sys.exit("pass --app <src root> or --selftest")
    f = findings(scan(os.path.expanduser(a.app)))
    if a.json: json.dump(f, sys.stdout, indent=1)
    else:
        for x in f:
            print(f"✗ {x['job']}: {x['suggestion']}")
            for sig, locs in x["implementations"].items():
                print(f"    [{sig}]")
                for l in locs[:4]: print(f"      {l}")
        if not f: print("✓ no divergent same-job implementations found")
    sys.exit(1 if f else 0)


if __name__ == "__main__":
    main()
