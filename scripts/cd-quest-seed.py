#!/usr/bin/env python3
"""
cd-quest-seed.py — GUILD-32: automate Claude Design as a /guild-quest stage (seed-PUSH).

Assembles Guild's system (canonical DTCG tokens + Product Baseline) into a Claude Design
WRITE PLAN, gates it (GUILD-29 onboarding contrast + GUILD-28 handoff), and DRY-RUNS it.
The actual DesignSync write_files (which MUTATES the owner's prod CD project) is a
separate, OWNER-CONFIRMED step — this script never writes to CD; it only produces the
plan + gate verdict so a bad token is caught BEFORE it propagates.

  python3 scripts/cd-quest-seed.py --dry-run     # show the write plan + gate verdict
  python3 scripts/cd-quest-seed.py --selftest
"""
import os, sys, json, importlib.util, argparse
import yaml

ROOT = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))

def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def _yaml(p):
    try: return yaml.safe_load(open(os.path.join(ROOT, "docs", "guild", p))) or {}
    except FileNotFoundError: return {}

def build_seed():
    """The files Guild would push INTO the CD project (canonical tokens + baseline guideline)."""
    seed = []
    # 1) canonical tokens -> CD CSS (reuse the DTCG exporter)
    dtcg_path = os.path.join(ROOT, "docs", "guild", "tokens.dtcg.json")
    if os.path.exists(dtcg_path):
        exp = _load("exp", "dtcg-export.py")
        seed.append({"path": "tokens/guild-tokens.css", "content": exp.to_css(json.load(open(dtcg_path)))})
    # 2) Product Baseline -> a CD guideline card
    base = (_yaml("context.yaml").get("baseline") or {})
    trg = base.get("triggers") or []; laws = base.get("laws") or []
    rows = "".join(f"<li><b>{t.get('id','')}</b> {t.get('title','')}</li>" for t in trg)
    html = (f"<!-- @dsCard group=\"Guild\" -->\n<article><h2>Guild Product Baseline</h2>"
            f"<p>{len(laws)} laws · {len(trg)} triggers — mandatory UX defaults applied at generation.</p>"
            f"<ul>{rows}</ul></article>")
    seed.append({"path": "guidelines/guild-product-baseline.card.html", "content": html})
    return seed

def gate_seed(seed):
    """Run the onboarding contrast gate on the system before any push (catch bad token at source)."""
    og = _load("og", "cd-onboarding-gate.py")
    pal = (_yaml("design-system.yaml").get("palette") or {})
    fails = og.audit(og.standard_pairings(pal)) if pal else ["no palette to gate"]
    return fails

def selftest():
    seed = build_seed()
    fails = gate_seed(seed)
    print("GUILD-32 cd-quest-seed — self-test")
    for s in seed: print(f"   plan: {s['path']} ({len(s['content'])} bytes)")
    print(f"   onboarding gate (GUILD-29): {len(fails)} fail(s) -> {'GO' if not fails else 'NO-GO'}")
    ok = (len(seed) >= 2 and any(s["path"].endswith(".css") for s in seed)
          and any("baseline" in s["path"] for s in seed) and not fails)
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — assembles a gated CD write plan (tokens + baseline); gate clean; NO prod write performed (owner-confirmed step).")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.dry_run:
        seed = build_seed(); fails = gate_seed(seed)
        print("=== CD seed-push WRITE PLAN (dry-run — NOTHING written to Claude Design) ===")
        for s in seed: print(f"  WOULD write {s['path']}  ({len(s['content'])} bytes)")
        print(f"=== gate (GUILD-29 onboarding): {'GO ✓' if not fails else 'NO-GO ✗'} ===")
        for x in fails: print("  ✗", x)
        print("\nNEXT (owner-confirmed only): run GUILD-28 handoff-gate on the bundle, then on the owner's"
              "\nexplicit 'push it' execute DesignSync finalize_plan + write_files for these exact paths.")
        sys.exit(0 if not fails else 1)
    sys.exit("pass --dry-run or --selftest")

if __name__ == "__main__":
    main()
