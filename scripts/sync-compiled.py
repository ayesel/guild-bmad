#!/usr/bin/env python3
"""
sync-compiled.py — repair compiled Guild agents after an external BMAD recompile.

WHY THIS EXISTS (read before "improving" it):
  The compiled _bmad/guild/agents/*.md are produced by an EXTERNAL BMAD compiler
  that is not vendored in this repo. That compiler injects content the source
  .agent.yaml does not contain (per-agent <activation> step-2 text, the
  `capabilities=` attr, boilerplate <rules>, name->slug ids), so we CANNOT
  regenerate the compiled files from source without losing data. What the
  external compiler reliably *breaks* on every run is the menu `target=`
  attribute (documented in CLAUDE.md; guarded by validate.sh check [4]).

  This script automates the documented manual fix: re-inject every compiled
  menu item's `target=` from the source .agent.yaml `menu[].target`, matched
  1:1 by the item's `cmd` (which equals the source `trigger` verbatim). It is
  SAFE (touches only the target= attribute of existing items), DETERMINISTIC,
  and IDEMPOTENT (a second run is a no-op). Run it after any recompile, then
  run validate.sh.

  It does NOT rewrite <rules>/critical_actions: the external compiler reroutes
  some critical_actions into <activation>, so the source .agent.yaml stays the
  single source of truth for those (edit yaml + compiled together, or re-run a
  recompile + this script).

Usage:
  python3 scripts/sync-compiled.py            # repair in place
  python3 scripts/sync-compiled.py --check    # report only, exit 1 if repairs needed
"""
import os, re, sys, glob
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src/modules/guild/agents")
CMP = os.path.join(ROOT, "_bmad/guild/agents")

ITEM_RE = re.compile(r'(<item\s+cmd="(?P<cmd>[^"]*)")(?P<mid>(?:\s+target="(?P<target>[^"]*)")?)(?P<rest>\s*>)')

def source_targets(yaml_path):
    """Map {trigger: target} from a source agent's menu (skip entries without a target)."""
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    out = {}
    menu = (((data or {}).get("agent") or {}).get("menu")) or []
    for entry in menu:
        if not isinstance(entry, dict):
            continue
        trig, tgt = entry.get("trigger"), entry.get("target")
        if trig and tgt:
            out[trig.strip()] = tgt.strip()
    return out

def sync_one(name, check):
    yaml_path = os.path.join(SRC, f"{name}.agent.yaml")
    md_path = os.path.join(CMP, f"{name}.md")
    if not (os.path.exists(yaml_path) and os.path.exists(md_path)):
        return 0, 0
    targets = source_targets(yaml_path)
    text = open(md_path).read()
    repairs = []

    def repl(m):
        cmd = m.group("cmd").strip()
        want = targets.get(cmd)
        have = m.group("target")
        if want is None or want == have:
            return m.group(0)  # no source target, or already correct
        repairs.append((cmd, have, want))
        return f'{m.group(1)} target="{want}"{m.group("rest")}'

    new = ITEM_RE.sub(repl, text)
    if repairs and not check:
        open(md_path, "w").write(new)
    total_items = len(ITEM_RE.findall(text))
    return total_items, len(repairs), repairs

def main():
    check = "--check" in sys.argv
    names = sorted(os.path.basename(p)[:-len(".agent.yaml")]
                   for p in glob.glob(os.path.join(SRC, "*.agent.yaml")))
    grand = 0
    print(("CHECK" if check else "SYNC") + f" menu target= across {len(names)} agents")
    for name in names:
        items, n, repairs = sync_one(name, check)
        flag = "✗" if (check and n) else ("→" if n else "✓")
        print(f"  {flag} {name:13} {items} items, {n} target= {'drift' if check else 'repaired'}")
        for cmd, have, want in repairs:
            print(f"        [{cmd.split(' ')[0]}] {have or '(missing)'} -> {want}")
        grand += n
    if check and grand:
        print(f"FAIL — {grand} menu item(s) need target= repair. Run: python3 scripts/sync-compiled.py")
        sys.exit(1)
    print(("OK — compiled menus match source" if not grand else f"DONE — repaired {grand} target= attribute(s)"))

if __name__ == "__main__":
    main()
