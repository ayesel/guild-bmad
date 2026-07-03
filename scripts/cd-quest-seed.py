#!/usr/bin/env python3
"""
cd-quest-seed.py — GUILD-32: automate Claude Design as a /guild-quest stage (seed-PUSH).

Assembles Guild's system (canonical DTCG tokens + Product Baseline) into a Claude Design
WRITE PLAN, gates it (GUILD-29 onboarding contrast), and either DRY-RUNS it or EMITS the
gated bundle to disk so DesignSync can push it. The script itself NEVER calls DesignSync —
it only produces the gated, on-disk bundle + a finalize_plan spec (plan.json). The actual
DesignSync finalize_plan + write_files (which MUTATES the owner's prod CD project) is the
agent's separate, OWNER-CONFIRMED step (the finalize_plan permission prompt IS the confirm).
A NO-GO gate refuses to emit — a bad token is caught BEFORE it can propagate into CD.

This is BOTH halves of the loop's write side: the programmatic SEED (prime CD's generation
with Guild's tokens + baseline) and the corrective PUSH-BACK use the same gated bundle.

  python3 scripts/cd-quest-seed.py --dry-run          # show the write plan + gate verdict
  python3 scripts/cd-quest-seed.py --emit <dir>       # gate, then write the bundle + plan.json
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

def emit_bundle(out_dir):
    """Gate, then write the bundle to disk + a plan.json (finalize_plan spec). NO-GO -> refuse."""
    seed = build_seed()
    fails = gate_seed(seed)
    if fails:
        print("=== CD seed-push: NO-GO — refusing to emit (bad token caught at source) ===")
        for x in fails:
            print("  ✗", x)
        sys.exit(1)
    out_dir = os.path.abspath(os.path.expanduser(out_dir))
    for s in seed:
        p = os.path.join(out_dir, s["path"])
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(s["content"])
    writes = [s["path"] for s in seed]
    plan = {"localDir": out_dir, "writes": writes, "gate": "GO",
            "note": "finalize_plan(localDir, writes) then write_files(planId, [{path, localPath: path}]) — owner-confirmed."}
    json.dump(plan, open(os.path.join(out_dir, "plan.json"), "w"), indent=2)
    print(f"=== CD seed-push bundle EMITTED (gated GO) -> {out_dir} ===")
    for w in writes:
        print(f"  wrote {w}")
    print("\nfinalize_plan spec: plan.json")
    print("  localDir:", out_dir)
    print("  writes:  ", writes)
    print("\nNEXT (agent, owner-confirmed): DesignSync finalize_plan(localDir, writes) — the permission")
    print("prompt IS the confirm — then write_files(planId, [{path, localPath: path} ...]).")
    sys.exit(0)


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
    ap.add_argument("--emit", metavar="DIR", help="gate, then write the bundle + plan.json to DIR for DesignSync push")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.emit: emit_bundle(a.emit)
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
