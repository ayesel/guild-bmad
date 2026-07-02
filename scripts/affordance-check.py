#!/usr/bin/env python3
"""
affordance-check.py — proactive affordance-completeness (card cfff66c9).

The wedding-hub guest-table failure class, killed: the brain holds the canonical
affordance set per element type (docs/guild/affordances.yaml) and diffs a REAL
screen against it — so "add sort... now filter... now empty states" never has to
be prompted one-by-one again. Detects which sets FIRE from the source (collection,
form, navigation, wizard, dashboard), then reports present / MISSING / manual-check
per required affordance. JSX + Tailwind aware. Static analysis is honest about its
limits: affordances it cannot verify statically are reported for manual check, and
never fail the gate.

  python3 scripts/affordance-check.py --screen <src> [--json]
  python3 scripts/affordance-check.py --selftest
Exit 0 = every fired set's verifiable requirements present; 1 = real gaps.
"""
import os, re, sys, json, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(os.path.dirname(HERE), "docs", "guild", "affordances.yaml")

# --- which sets fire, from source markers -----------------------------------
FIRES = {
    "collection": r'\.map\(\s*\(?\w+.*?\)?\s*=>|<table|role="table"|<ul[\s>][\s\S]{0,400}<li',
    "form":       r'<form|onSubmit',
    "navigation": r'<nav[\s>]|role="navigation"',
    "wizard-flow": r'[Ss]tep\s+\d+\s+of\s+\d+|stepIndicator|currentStep',
    "dashboard-summary": r'progressbar|remaining|of\s+\{?\w*target',
}

# --- per-affordance detection: (regex, None=unverifiable-static) -------------
DETECT = {
    "search":        r'type="search"|(placeholder|aria-label|label)[^>]{0,60}[Ss]earch|>Search<',
    "filter":        r'["\'>][^"\'<]{0,40}[Ff]ilter|aria-label="[^"]*[Ff]ilter',
    "sort":          r'aria-sort|sort(By|able|Key|Dir)|setSort|["\'>][^"\'<]{0,20}Sort',
    "count":         r'\.length\}|\.length\s*[,)]|\b[cC]ount\b[^(]|result[s]?\b',
    "empty-state":   r'["\'>](No |Nothing|Empty|Add your first|Get started|nothing here)',
    "zero-results":  r'[Nn]o [\w ]{0,24}(results?|match(es)?|found)|[Zz]ero[- ]results|nothing (found|matches)',
    "row-actions":   r'aria-label="?(Edit|Remove|Delete|Open)|>(Edit|Remove|Delete)<',
    "complete-rollup": None,
    "group-by":      r'group(By|ed)?\b|[Gg]roup by',
    "sticky-header": r'sticky',
    "bulk-actions":  r'[Bb]ulk|[Ss]elect [Aa]ll',
    "pagination-or-virtualization": r'[Pp]agination|virtual|windowed|Load more|pageSize',
    "labels-above":  r'<label|htmlFor',
    "inline-validation": r'aria-invalid|onBlur[\s\S]{0,80}(error|valid)|(error|valid)[\s\S]{0,80}onBlur|fieldError',
    "submit-disabled-until-valid": r'disabled=\{[^}]*(valid|pending|submitting|!\w)',
    "loading-on-submit": r'(pending|loading|submitting|saving)[\s\S]{0,60}(submit|button)|(Sav|Load|Submitt)ing',
    "success-confirmation": r'[Ss]aved|[Ss]uccess|✓|confirmation',
    "error-recovery": r'role="alert"|formError|errorMessage|\{error',
    "field-help":    r'help(er)?[Tt]ext|aria-describedby',
    "keyboard-submit": None,
    "text-labels":   r'<nav[\s\S]{0,600}>[A-Za-z]',
    "active-state":  r'aria-current|[Aa]ctive',
    "grouped":       None,
    "max-seven":     None,
    "input-prominent": r'<input|<textarea',
    "results-list":  r'\.map\(',
    "loading-state": r'[Ll]oading|skeleton|<Spinner|pending',
    "result-count":  r'\.length\}|\b[cC]ount\b',
    "recent-or-suggested": r'[Rr]ecent|[Ss]uggest',
    "keyboard-nav":  None,
    "step-indicator": r'[Ss]tep\s+\d+\s+of|aria-label="[^"]*[Ss]tep',
    "back":          r'>Back<|aria-label="Back"|onBack',
    "finish":        r'>(Finish|Done|Complete)',
    "per-step-validation": r'error|invalid',
    "skip-optional-steps": r'[Ss]kip',
    "resume-where-left": None,
    "value-vs-target": r'of\s+\{|target|remaining',
    "totals":        r'[Tt]otal',
    "trend-over-time": r'[Tt]rend|chart|sparkline',
    "drill-in":      r'href=|onClick[\s\S]{0,40}(open|detail|navigate)',
    "hover-state":   r'\bhover:|:hover',
    "focus-visible": r'focus-visible',
    "disabled-state": r'disabled',
    "touch-target-44": None,
    "transition":    r'\btransition|animate-',
}


def load_canon():
    import yaml
    return yaml.safe_load(open(CANON))["sets"]


def check(src, canon):
    fired, report, gaps = [], {}, []
    for set_name, fire_pat in FIRES.items():
        if set_name not in canon or not re.search(fire_pat, src):
            continue
        fired.append(set_name)
        rows = []
        for level in ("required", "recommended"):
            for aff in canon[set_name].get(level, []):
                pat = DETECT.get(aff, None)
                if pat is None:
                    status = "manual-check"
                elif re.search(pat, src):
                    status = "present"
                else:
                    status = "MISSING" if level == "required" else "missing (recommended)"
                    if level == "required":
                        gaps.append(f"{set_name}: {aff}")
                rows.append({"affordance": aff, "level": level, "status": status})
        report[set_name] = rows
    # interactive-universal is delegated to the wired gates — note it, never re-fail it here
    report["interactive-universal"] = "delegated to state-motion-req + responsive-gate (already wired)"
    return {"fired": fired, "sets": report, "gaps": gaps}


def selftest():
    complete = """
      <input aria-label="Search vendors" /> <button>Filter</button> aria-sort sortBy
      <span>{rows.length} results</span> {rows.map(r => (<li>
      <button aria-label="Edit">Edit</button></li>))}
      <p>No vendors yet — add your first.</p> <p>No results for that search.</p>
    """
    bare = "<ul>{items.map(i => (<li>{i.name}</li>))}</ul>"
    canon = load_canon()
    c = check(complete, canon)
    b = check(bare, canon)
    missing_names = {g.split(": ")[1] for g in b["gaps"]}
    ok = (not c["gaps"]
          and "collection" in b["fired"]
          and {"search", "filter", "sort", "empty-state", "row-actions"} <= missing_names
          and all(r["status"] != "MISSING" or r["level"] == "required"
                  for rows in c["sets"].values() if isinstance(rows, list) for r in rows))
    print("affordance-check self-test:")
    print(f"   complete fixture gaps: {len(c['gaps'])} (want 0)")
    print(f"   bare-list fixture gaps: {len(b['gaps'])} -> {sorted(missing_names)}")
    print(f"{'✅ PASS' if ok else '❌ FAIL'}")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--screen"); ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if not a.screen: sys.exit("pass --screen <src file> or --selftest")
    result = check(open(a.screen).read(), load_canon())
    if a.json:
        json.dump(result, sys.stdout, indent=1)
    else:
        print(f"fired sets: {', '.join(result['fired']) or 'none'}")
        for g in result["gaps"]: print("  ✗ MISSING", g)
        manual = [f"{s}: {r['affordance']}" for s, rows in result["sets"].items()
                  if isinstance(rows, list) for r in rows if r["status"] == "manual-check"]
        for m in manual: print("  ? manual ", m)
        if not result["gaps"]: print("  ✓ every verifiable required affordance present")
    sys.exit(1 if result["gaps"] else 0)


if __name__ == "__main__":
    main()
