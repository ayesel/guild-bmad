#!/usr/bin/env python3
"""
cd-tokens-to-dtcg.py — GUILD-31: map captured Claude Design CSS tokens -> DTCG.

Parses the captured token bundle (CSS custom properties) into a Design Tokens
Community Group (DTCG) JSON document — the canonical, tool-agnostic token truth
that every adapter (Storybook / Figma / Style Dictionary) round-trips through
(GUILD-35). Re-run after re-pulling the bundle via DesignSync.

  python3 scripts/cd-tokens-to-dtcg.py
  -> docs/guild/tokens.dtcg.json
"""
import os, re, json, sys

ROOT = os.getcwd()
SRC = os.path.join(ROOT, "docs", "guild", "claude-design-bundle", "tokens.bundle.css")
OUT = os.path.join(ROOT, "docs", "guild", "tokens.dtcg.json")

RAMPS = ("warm", "ember", "sage", "honey", "berry", "denim")

def parse_css(text):
    # last definition wins (light theme base)
    out = {}
    for m in re.finditer(r'--([\w-]+)\s*:\s*([^;]+);', text):
        out[m.group(1).strip()] = m.group(2).strip()
    return out

def cubic(v):
    m = re.search(r'cubic-bezier\(([^)]+)\)', v)
    if not m: return None
    try: return [float(x) for x in m.group(1).split(",")]
    except Exception: return None

def alias(v):
    m = re.match(r'var\(--([\w-]+)\)$', v.strip())
    return m.group(1) if m else None

def classify(name, val):
    """Return (group_path:list, dtcg_token:dict) or None to skip."""
    a = alias(val)
    def ref(n):  # best-effort DTCG alias path
        for r in RAMPS:
            if n.startswith(r + "-"):
                return "{color.%s.%s}" % (r, n[len(r)+1:])
        return "{%s}" % n
    # colors
    for r in RAMPS:
        if name.startswith(r + "-"):
            return (["color", r, name[len(r)+1:]], {"$type": "color", "$value": val})
    if name.startswith("color-"):
        v = ref(a) if a else val
        return (["color", "semantic", name[6:]], {"$type": "color", "$value": v})
    # space / radius
    if name.startswith("space-") or name in ("touch-target", "tap-min"):
        return (["space", name.replace("space-", "")], {"$type": "dimension", "$value": val})
    if name.startswith("radius-"):
        return (["radius", name[7:]], {"$type": "dimension", "$value": val})
    # shadow
    if name.startswith("shadow-") or name.startswith("elevation"):
        return (["shadow", name.split("-", 1)[-1]], {"$type": "shadow", "$value": val})
    # typography
    if name in ("font-sans", "font-mono", "font-numeric"):
        fams = [f.strip().strip("'\"") for f in val.replace("var(--font-mono)", "monospace").split(",")]
        return (["font", name.replace("font-", "")], {"$type": "fontFamily", "$value": fams})
    if name.startswith("weight-"):
        try: w = int(val)
        except Exception: return None
        return (["weight", name[7:]], {"$type": "fontWeight", "$value": w})
    if name.startswith("text-"):
        return (["fontSize", name[5:]], {"$type": "dimension", "$value": val})
    if name.startswith("leading-"):
        return (["lineHeight", name[8:]], {"$type": "number", "$value": float(val) if re.match(r'^[\d.]+$', val) else val})
    if name.startswith("tracking-"):
        return (["letterSpacing", name[9:]], {"$type": "dimension", "$value": val})
    # motion
    if name.startswith("dur-"):
        return (["duration", name[4:]], {"$type": "duration", "$value": val})
    if name.startswith("ease-"):
        c = cubic(val)
        return (["easing", name[5:]], {"$type": "cubicBezier", "$value": c} if c else {"$type": "other", "$value": val})
    return None

def main():
    if not os.path.exists(SRC):
        sys.exit(f"missing bundle: {SRC} (run the DesignSync pull / GUILD-27 first)")
    toks = parse_css(open(SRC).read())
    doc = {"$description": "Hearth Works tokens (DTCG) — generated from the Claude Design "
                           "capture by scripts/cd-tokens-to-dtcg.py. Do not hand-edit; re-pull + re-run."}
    n = 0
    for name, val in toks.items():
        c = classify(name, val)
        if not c: continue
        path, tok = c
        node = doc
        for seg in path[:-1]:
            node = node.setdefault(seg, {})
        node[path[-1]] = tok
        n += 1
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=2)
    groups = [k for k in doc if not k.startswith("$")]
    print(f"wrote {OUT}: {n} tokens across {len(groups)} groups → {', '.join(groups)}")

if __name__ == "__main__":
    main()
