#!/usr/bin/env python3
"""
dtcg-export.py — GUILD-35: canonical DTCG -> per-tool adapters (READ/EXPORT side).

One canonical token source (docs/guild/tokens.dtcg.json) fans out to every tool's
format, so a token change propagates everywhere with no drift. READ/EXPORT only —
all write/push-back adapters are PARKED (owner WRITE=OFF).

  python3 scripts/dtcg-export.py [--target css|figma|storybook|all] [--check]
Targets:
  css        -> docs/guild/exports/tokens.css           (CSS custom properties; Storybook/web consume)
  figma      -> docs/guild/exports/figma-tokens.json    (Tokens Studio import format)
  storybook  -> docs/guild/exports/tokens.stories.js    (a Design Tokens CSF story)
--check: regenerate in-memory and diff vs disk; non-zero exit if stale (CI guard).
"""
import os, sys, json, argparse

ROOT = os.getcwd()
DTCG = os.path.join(ROOT, "docs", "guild", "tokens.dtcg.json")
EXPORTS = os.path.join(ROOT, "docs", "guild", "exports")

def load():
    if not os.path.exists(DTCG):
        sys.exit(f"missing {DTCG} (run cd-tokens-to-dtcg.py / GUILD-31 first)")
    return json.load(open(DTCG))

def walk(doc):
    """Yield (path:list, token:dict) for every leaf DTCG token."""
    def rec(node, path):
        if isinstance(node, dict) and "$value" in node:
            yield path, node; return
        if isinstance(node, dict):
            for k, v in node.items():
                if k.startswith("$"): continue
                yield from rec(v, path + [k])
    yield from rec(doc, [])

def css_value(v):
    if isinstance(v, list):  # fontFamily or cubicBezier
        if all(isinstance(x, (int, float)) for x in v):
            return "cubic-bezier(%s)" % ", ".join(str(x) for x in v)
        return ", ".join(str(x) for x in v)
    s = str(v)
    # alias {a.b.c} -> var(--a-b-c)
    if s.startswith("{") and s.endswith("}"):
        return "var(--%s)" % s[1:-1].replace(".", "-")
    return s

def to_css(doc):
    lines = ["/* GENERATED from tokens.dtcg.json by dtcg-export.py — do not hand-edit. */", ":root {"]
    for path, tok in walk(doc):
        lines.append(f"  --{'-'.join(path)}: {css_value(tok['$value'])};")
    lines.append("}")
    return "\n".join(lines) + "\n"

def to_figma(doc):
    """Tokens Studio import shape: nested {group:{name:{value,type}}}."""
    out = {}
    for path, tok in walk(doc):
        node = out
        for seg in path[:-1]:
            node = node.setdefault(seg, {})
        val = tok["$value"]
        if isinstance(val, str) and val.startswith("{") and val.endswith("}"):
            val = "{" + val[1:-1] + "}"  # Tokens Studio also uses {alias}
        node[path[-1]] = {"value": val, "type": tok.get("$type", "other")}
    return json.dumps(out, indent=2) + "\n"

def to_storybook(doc):
    colors = [("-".join(p), t["$value"]) for p, t in walk(doc) if t.get("$type") == "color" and str(t["$value"]).startswith("#")]
    swatches = ",\n".join(f'    {{name:"{n}",hex:"{h}"}}' for n, h in colors)
    return ("// GENERATED from tokens.dtcg.json by dtcg-export.py — Design Tokens story.\n"
            "import './tokens.css';\n"
            "export default { title: 'Design System/Tokens (Hearth Works)' };\n"
            "const colors = [\n" + swatches + "\n];\n"
            "export const Colors = () => {\n"
            "  const wrap = document.createElement('div');\n"
            "  wrap.style.cssText = 'display:flex;flex-wrap:wrap;gap:12px;font-family:sans-serif';\n"
            "  colors.forEach(c => { const el = document.createElement('div');\n"
            "    el.style.cssText = 'width:88px;font-size:11px;color:#555';\n"
            "    el.innerHTML = `<div style=\"height:56px;border-radius:8px;border:1px solid #0001;background:${c.hex}\"></div>${c.name}<br>${c.hex}`;\n"
            "    wrap.appendChild(el); });\n"
            "  return wrap;\n"
            "};\n")

BUILDERS = {"css": ("tokens.css", to_css), "figma": ("figma-tokens.json", to_figma),
            "storybook": ("tokens.stories.js", to_storybook)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=list(BUILDERS) + ["all"], default="all")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    doc = load()
    targets = list(BUILDERS) if a.target == "all" else [a.target]
    os.makedirs(EXPORTS, exist_ok=True)
    stale = []
    for t in targets:
        fname, fn = BUILDERS[t]
        path = os.path.join(EXPORTS, fname)
        content = fn(doc)
        if a.check:
            cur = open(path).read() if os.path.exists(path) else None
            if cur != content: stale.append(fname)
        else:
            open(path, "w").write(content)
            print(f"  {t:10} -> docs/guild/exports/{fname}")
    if a.check:
        if stale: sys.exit("STALE exports (re-run dtcg-export.py): " + ", ".join(stale))
        print("exports current vs canonical ✓")

if __name__ == "__main__":
    main()
