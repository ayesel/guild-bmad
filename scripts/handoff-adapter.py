#!/usr/bin/env python3
"""
handoff-adapter.py — GUILD-61: resolve the handoff adapter (standalone default / BMAD opt-in).

North-star: GUILD is the brain; the build pipeline (BMAD) is one swappable handoff
adapter. This resolves which adapter + output target a run uses from guild.config.yaml
`bmad_mode` and whether `_bmad/` is present — so tasks call the resolved adapter
instead of branching on BMAD inline. Registry: docs/guild/handoff-adapters.yaml.

  python3 scripts/handoff-adapter.py            # resolve for the current project
  python3 scripts/handoff-adapter.py --selftest
"""
import os, sys, argparse
import yaml

ROOT = os.getcwd()
REG = os.path.join(ROOT, "docs", "guild", "handoff-adapters.yaml")

def registry():
    return yaml.safe_load(open(REG)) or {}

def resolve(bmad_mode, bmad_present, reg=None):
    reg = reg or registry()
    mode = str(bmad_mode).lower()
    if mode == "true":
        name = "bmad"
    elif mode in ("false", "standalone"):
        name = "standalone"
    elif mode == "auto":
        name = "bmad" if bmad_present else "standalone"
    else:                                   # unknown/unset -> the registry default
        name = reg.get("default", "standalone")
    adapter = (reg.get("adapters") or {}).get(name, {})
    return {"adapter": name, "output_root": adapter.get("output_root"),
            "story_format": adapter.get("story_format"), "tasks": adapter.get("tasks", [])}

def selftest():
    reg = registry()
    cases = {
        "fresh project, no _bmad (default)":      (resolve("false", False, reg), "standalone", "guild-output"),
        "auto + no _bmad":                        (resolve("auto", False, reg), "standalone", "guild-output"),
        "unset/unknown -> registry default":      (resolve("", False, reg), "standalone", "guild-output"),
        "bmad_mode: true (opt-in)":               (resolve("true", True, reg), "bmad", "_bmad-output"),
        "auto + _bmad present":                   (resolve("auto", True, reg), "bmad", "_bmad-output"),
    }
    print("GUILD-61 handoff-adapter resolver — self-test")
    ok = reg.get("default") == "standalone"
    for label, (got, want_a, want_o) in cases.items():
        good = got["adapter"] == want_a and got["output_root"] == want_o
        ok = ok and good
        print(f"   {'✓' if good else '✗'} {label}: {got['adapter']} -> {got['output_root']}")
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — fresh/no-_bmad => standalone+guild-output (default); "
          f"bmad_mode:true => bmad+_bmad-output (adapter still works when enabled).")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    cfg = {}
    try: cfg = yaml.safe_load(open(os.path.join(ROOT, "guild.config.yaml"))) or {}
    except FileNotFoundError: pass
    present = os.path.exists(os.path.join(ROOT, "_bmad", "core", "config.yaml"))
    print(resolve(cfg.get("bmad_mode", "false"), present))

if __name__ == "__main__":
    main()
