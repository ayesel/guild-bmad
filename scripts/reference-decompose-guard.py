#!/usr/bin/env python3
"""
reference-decompose-guard.py — GUILD-58 (V-E): harden reference decomposition.

Reference decomposition (GUILD-25) must extract ABSTRACT design attributes for
CONDITIONING — never pixel-copy the reference (that's plagiarism + overfitting). This
guard flags a decomposition output that smuggles in literal values (exact hex
colours, exact px sizes, verbatim copy) instead of abstract attributes.

  python3 scripts/reference-decompose-guard.py --file decomposition.txt
  python3 scripts/reference-decompose-guard.py --selftest
"""
import re, sys, argparse

LITERAL_HEX = re.compile(r'#[0-9a-fA-F]{6}')
LITERAL_PX = re.compile(r'\b\d{2,}px\b')
VERBATIM = re.compile(r'\b(copy exactly|pixel[- ]perfect|replicate|verbatim|exact same)\b', re.I)

def guard(text):
    findings = []
    if LITERAL_HEX.search(text):
        findings.append(f"literal hex colour(s) {sorted(set(LITERAL_HEX.findall(text)))} — extract an ABSTRACT "
                        f"palette attribute (e.g. 'warm low-chroma'), not the reference's exact value")
    if LITERAL_PX.search(text):
        findings.append(f"literal px value(s) {sorted(set(LITERAL_PX.findall(text)))} — extract a relationship "
                        f"(e.g. 'generous whitespace', '8px rhythm'), not copied measurements")
    if VERBATIM.search(text):
        findings.append("verbatim-copy language — decomposition conditions on attributes, it does not replicate")
    return findings

def selftest():
    bad = "Use #B0421D for the accent, 48px hero padding, and copy exactly the card layout."
    good = ("Warm low-chroma ember accent; confident display hierarchy; generous whitespace on the hero; "
            "editorial restraint; tight tracking on large type.")
    fb, fg = guard(bad), guard(good)
    print("GUILD-58 reference-decompose guard — self-test")
    print(f"   pixel-copy decomposition: {len(fb)} finding(s)")
    for f in fb: print("     -", f)
    print(f"   abstract decomposition:   {len(fg)} finding(s)")
    ok = len(fb) == 3 and len(fg) == 0
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — literal copies flagged; abstract-attribute decomposition passes.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.file:
        for f in guard(open(a.file).read()) or ["abstract decomposition — no literal copies"]: print(" ", f)
        return
    sys.exit("pass --file <f> or --selftest")

if __name__ == "__main__":
    main()
