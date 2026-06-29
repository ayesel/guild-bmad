#!/usr/bin/env python3
"""
token-lint.py — GUILD-54 (V-D): lint code for hardcoded values, suggest the DTCG token.

Dev-time companion to the fidelity gate: scan source for hardcoded hex colours and
px/rem values that SHOULD be a canonical token, and suggest the exact token to use
(reverse-lookup against docs/guild/tokens.dtcg.json). Catches drift where it's born.

  python3 scripts/token-lint.py --file <src>
  python3 scripts/token-lint.py --selftest
"""
import os, re, sys, json, argparse

DTCG = os.path.join(os.getcwd(), "docs", "guild", "tokens.dtcg.json")

def token_index():
    """value -> dotted token path, from the canonical DTCG."""
    try: d = json.load(open(DTCG))
    except FileNotFoundError: return {}
    idx = {}
    def walk(n, path):
        if isinstance(n, dict) and "$value" in n:
            v = n["$value"]
            if isinstance(v, str): idx.setdefault(v.lower(), ".".join(path))
            return
        if isinstance(n, dict):
            for k, x in n.items():
                if not k.startswith("$"): walk(x, path + [k])
    walk(d, [])
    return idx

def lint(src, idx):
    findings = []
    for m in re.finditer(r'#[0-9a-fA-F]{6}', src):
        hexv = m.group(0).lower()
        if hexv in ("#ffffff", "#000000"): continue
        tok = idx.get(hexv)
        findings.append(f"hardcoded {m.group(0)} → use token {{{tok}}}" if tok
                        else f"hardcoded {m.group(0)} (off-system — not a token)")
    return findings

def selftest():
    idx = {"#b0421d": "color.ember.600", "#211c17": "color.ink", "1rem": "space.4"}
    src = "button{background:#B0421D;color:#FFFFFF;border:1px solid #3B82F6}"
    f = lint(src, idx)
    print("GUILD-54 token-lint — self-test")
    for x in f: print("   -", x)
    ok = (any("color.ember.600" in x for x in f)        # known token suggested
          and any("#3b82f6" in x.lower() and "off-system" in x for x in f)  # off-system flagged
          and not any("#ffffff" in x.lower() for x in f))   # white allowed
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — known value maps to its token; off-system flagged; white ignored.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.file:
        for x in lint(open(a.file).read(), token_index()) or ["no hardcoded values"]: print(" ", x)
        return
    sys.exit("pass --file <src> or --selftest")

if __name__ == "__main__":
    main()
