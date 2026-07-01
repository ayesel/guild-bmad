#!/usr/bin/env python3
"""
GUILD persona-evidence gate — the empirical-persona guardrail, ENFORCED.

Personas are where AI most loves to fabricate ("synthetic users"). This gate refuses
a persona card whose claims don't trace to real evidence. Every claim bullet must carry
ONE marker:
  [E:<source>]      evidence-backed (cite the source: a call, a doc, research, the IA)
  [ASSUMPTION]      an explicit, owned assumption (allowed, but counted + surfaced)
  [DOCS-PENDING]    real but its source isn't filed yet (e.g. a confirmed partner, no doc)

A persona with ANY unmarked claim, or with ZERO evidence-backed claims (pure synthetic),
BLOCKS. Output is structured (--json) so the widget can surface "what's ungrounded."

Convention for a persona card (markdown):
  # <Persona name>
  ...prose...
  - <claim> [E:Buzby-call]
  - <claim> [ASSUMPTION]
  ## Evidence
  - Buzby-call: June 17 recorded call ...

Usage:
  python3 persona-evidence-gate.py --personas <file-or-dir> [--json]
  python3 persona-evidence-gate.py --selftest

Exit 0 = all personas grounded. Exit 1 = one or more block.
"""
import re, sys, os, json, glob, argparse

CLAIM = re.compile(r"^\s*[-*]\s+(.*\S)\s*$")
MARK_E = re.compile(r"\[E:[^\]]+\]")
MARK_A = re.compile(r"\[ASSUMPTION\]", re.I)
MARK_D = re.compile(r"\[DOCS-PENDING\]", re.I)
HEAD   = re.compile(r"^#\s+(.+)$")
EVID_H = re.compile(r"^#{1,6}\s*evidence", re.I)


def evaluate_card(text, name):
    """One persona card -> (blocking[], stats{})."""
    lines = text.splitlines()
    in_evidence = False
    cited = assumed = pending = unmarked = 0
    unmarked_examples = []
    for ln in lines:
        if EVID_H.match(ln):
            in_evidence = True
            continue
        m = CLAIM.match(ln)
        if not m:
            continue
        claim = m.group(1)
        if in_evidence:
            continue  # bullets under ## Evidence are the sources themselves
        if MARK_E.search(claim):       cited += 1
        elif MARK_A.search(claim):     assumed += 1
        elif MARK_D.search(claim):     pending += 1
        else:
            unmarked += 1
            if len(unmarked_examples) < 4:
                unmarked_examples.append(claim[:70])

    blocking = []
    if unmarked:
        blocking.append(f"{name}: {unmarked} claim(s) with NO evidence marker (e.g. {unmarked_examples}). "
                        f"Mark each [E:src] / [ASSUMPTION] / [DOCS-PENDING].")
    total_claims = cited + assumed + pending + unmarked
    if total_claims and cited == 0:
        blocking.append(f"{name}: ZERO evidence-backed claims — pure synthetic persona. Ground at least the core segment/goals.")
    stats = {"cited": cited, "assumption": assumed, "docs_pending": pending,
             "unmarked": unmarked, "total_claims": total_claims}
    return blocking, stats


def selftest():
    bad = "# Otha\n- runs a book of customers\n- wants real-time alerts\n"  # unmarked -> block
    good = ("# Levi Love (Sheetz)\n- energy & procurement lead, multi-site retail [E:Roadmap_Alignment-§7]\n"
            "- staged Beta->Broker->Referral [E:Roadmap_Alignment-§7]\n- may expand to UBM index products [ASSUMPTION]\n"
            "## Evidence\n- Roadmap_Alignment-§7: Chris anchor-account validation\n")
    b1,_ = evaluate_card(bad, "Otha")
    b2,_ = evaluate_card(good, "Levi")
    ok = len(b1) >= 1 and len(b2) == 0
    print("self-test:")
    print(f"  synthetic card blocks: {'✅' if b1 else '❌'} ({len(b1)})")
    print(f"  grounded card passes:  {'✅' if not b2 else '❌'} ({len(b2)})")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--personas", help="persona card file or directory of .md cards")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    if not a.personas:
        sys.exit("pass --personas <file-or-dir> or --selftest")

    files = ([a.personas] if os.path.isfile(a.personas)
             else sorted(glob.glob(os.path.join(a.personas, "*.md"))))
    all_blocking, per = [], {}
    for f in files:
        text = open(f).read()
        # split a multi-persona file on top-level "# " headers; else treat whole file as one
        heads = [(i, m.group(1)) for i, l in enumerate(text.splitlines()) for m in [HEAD.match(l)] if m]
        if len(heads) > 1:
            lines = text.splitlines()
            for idx, (start, nm) in enumerate(heads):
                end = heads[idx+1][0] if idx+1 < len(heads) else len(lines)
                b, s = evaluate_card("\n".join(lines[start:end]), nm)
                all_blocking += b; per[nm] = s
        else:
            nm = heads[0][1] if heads else os.path.basename(f)
            b, s = evaluate_card(text, nm)
            all_blocking += b; per[nm] = s

    grounded = len(all_blocking) == 0
    if a.json:
        print(json.dumps({"grounded": grounded, "blocking": all_blocking, "personas": per}, indent=2))
    else:
        print("GUILD persona-evidence gate —", "✅ GROUNDED" if grounded else "❌ UNGROUNDED (blocked)")
        for b in all_blocking: print("  ✗", b)
        for nm, s in per.items():
            print(f"  · {nm}: {s['cited']} cited, {s['assumption']} assumption, {s['docs_pending']} docs-pending, {s['unmarked']} UNMARKED")
    sys.exit(0 if grounded else 1)


if __name__ == "__main__":
    main()
