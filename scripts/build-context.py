#!/usr/bin/env python3
"""
build-context.py — GUILD-1. Generate docs/guild/context.yaml FROM the prose
Product Baseline (single source of truth), so a run loads baseline + taste +
token pointers as structured data instead of re-asking the owner (the
"too much prompting" complaint).

  source : src/modules/guild/agents/shared-sidecar/product-baseline.md
  output : docs/guild/context.yaml   (GENERATED — never hand-edit)

Run: npm run build-context   (or python3 scripts/build-context.py [--check])
--check exits 1 if the committed context.yaml is stale vs the baseline.
"""
import os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src/modules/guild/agents/shared-sidecar/product-baseline.md")
OUT = os.path.join(ROOT, "docs/guild/context.yaml")
SRC_REL = "src/modules/guild/agents/shared-sidecar/product-baseline.md"

HEADER = (
    "# GENERATED from product-baseline.md by scripts/build-context.py — DO NOT EDIT BY HAND.\n"
    "# Regenerate: npm run build-context.  Single source of truth = the baseline markdown.\n"
    "# A run loads this so it does NOT re-ask brand / taste / baseline (GUILD-1).\n"
)

def _section(text, start, end):
    s = text.find(start)
    if s < 0:
        return ""
    e = text.find(end, s + len(start)) if end else len(text)
    return text[s : (e if e > 0 else len(text))]

def parse(text):
    # Layer 0 — universal laws: "- **Name** — rule"
    laws = []
    for m in re.finditer(r'^- \*\*(.+?)\*\*\s+—\s+(.+)$', _section(text, "## Layer 0", "## Layer 1"), re.M):
        laws.append({"name": m.group(1).strip(), "rule": m.group(2).strip()})
    # Layer 1 — trigger table: "### T1 — Title"
    triggers = []
    for m in re.finditer(r'^### (T\d+)\s+—\s+(.+)$', text, re.M):
        triggers.append({"id": m.group(1), "title": m.group(2).strip()})
    # Layer 2 — domain packs: "- **Name** (…) → …" or "- **Name** → …"
    packs = []
    for m in re.finditer(r'^- \*\*(.+?)\*\*', _section(text, "## Layer 2", "## How to apply"), re.M):
        packs.append(re.sub(r'\s*\(.*?\)\s*$', '', m.group(1)).strip())
    return laws, triggers, packs

def build():
    text = open(SRC).read()
    laws, triggers, packs = parse(text)
    if len(triggers) < 8:
        sys.exit(f"build-context: expected >=8 triggers (T1–T8), parsed {len(triggers)} — baseline format changed, fix the parser")
    if not laws:
        sys.exit("build-context: parsed 0 Layer-0 laws — baseline format changed")
    ctx = {
        "baseline": {
            "source": SRC_REL,
            "laws": laws,
            "triggers": triggers,
            "domain_packs": packs,
        },
        # Per-project slots — a run reads these instead of re-eliciting. Filled by
        # /guild-design-direction (taste) and the token surface (DTCG pointer).
        "taste_anchors": {
            "design_direction": "docs/design-direction.md",
            "taste_model": "docs/guild/taste-model.yaml",   # GUILD-14 owner taste model (retrieved at raid start)
            "references": [],
            "note": "per-project: the owner's design-direction + taste model + north-star refs so runs do not re-ask taste",
        },
        "tokens": {
            "format": "DTCG",
            "source": None,
            "note": "per-project: pointer to the design tokens (tokens.json / tailwind.config.js / Figma variables export)",
        },
    }
    return HEADER + yaml.safe_dump(ctx, sort_keys=False, width=100, allow_unicode=True)

def main():
    rendered = build()
    if "--check" in sys.argv:
        current = open(OUT).read() if os.path.exists(OUT) else ""
        if current != rendered:
            sys.exit("context.yaml is STALE vs product-baseline.md — run: npm run build-context")
        print("context.yaml is up to date with the baseline")
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(rendered)
    laws, triggers, packs = parse(open(SRC).read())
    print(f"wrote docs/guild/context.yaml — {len(laws)} laws, {len(triggers)} triggers, {len(packs)} domain packs")

if __name__ == "__main__":
    main()
