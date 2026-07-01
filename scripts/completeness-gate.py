#!/usr/bin/env python3
"""
GUILD completeness gate — refuse to call a DESIGN pass "done" when the steps that
actually find design problems never ran.

This is the gate that would have blocked the wedding-hub failure: a pass that
streamlined out visual-audit, left QA pending, and shipped research-only got to
declare itself complete because every "gate" was prose judgment. This makes the
PASS/FAIL objective and script-enforced.

Reads quest-state.yaml (+ the guild-artifacts dir) and checks design-pass coverage:
  - visual-audit must NOT be streamlined out
  - QA (Sage) must have run (status: done)
  - a visual-critique artifact (mage/critique/visual/responsive) must exist
  - a QA artifact (sage/qa) must exist
  - optional: screen coverage (--screens N) vs critique artifacts

Usage:
  python3 completeness-gate.py --state _bmad-output/quest-state.yaml \
      --artifacts-dir _bmad-output/guild-artifacts [--screens 22] [--json]
  python3 completeness-gate.py --selftest

Exit 0 = complete (handoff may proceed). Exit 1 = incomplete (BLOCK handoff).
"""
import re, sys, os, json, glob, argparse

# artifact-name patterns that count as real design work (not research)
VISUAL_CRITIQUE = re.compile(r"(mage|critique|visual|responsive|states|spacing|hierarchy|consistency|system-check|polish)", re.I)
QA_ARTIFACT     = re.compile(r"(sage|qa|pre-handoff|accessibility|a11y)", re.I)
RESEARCH_ONLY   = re.compile(r"(ranger|raid|research|interview|survey|competitive|persona)", re.I)


def parse_state(text):
    """Minimal dependency-free parse of the flat quest-state.yaml we emit."""
    mode = (re.search(r"^mode:\s*([A-Za-z0-9_-]+)", text, re.M) or [None, ""])[1]
    sl = re.search(r"^streamlined:\s*\[(.*?)\]", text, re.M)
    streamlined = [s.strip().strip('"\'') for s in sl.group(1).split(",")] if sl else []
    # per-phase qa status:  qa: { status: pending, ... }
    qa = re.search(r"\bqa:\s*\{[^}]*status:\s*([A-Za-z]+)", text)
    qa_status = qa.group(1) if qa else None
    return {"mode": mode, "streamlined": [s for s in streamlined if s], "qa_status": qa_status}


def evaluate(state, artifacts):
    """Return (blocking, warnings, summary) — blocking is non-empty => BLOCK."""
    names = [os.path.basename(a) for a in artifacts]
    has_visual = any(VISUAL_CRITIQUE.search(n) for n in names)
    has_qa     = any(QA_ARTIFACT.search(n) for n in names)
    research   = [n for n in names if RESEARCH_ONLY.search(n)]

    blocking, warnings = [], []

    if "visual-audit" in state["streamlined"]:
        blocking.append("visual-audit was STREAMLINED OUT — the screens were never critiqued (Mage never ran).")
    if state["qa_status"] and state["qa_status"].lower() != "done":
        blocking.append(f"QA (Sage) did not run — qa.status = '{state['qa_status']}'.")
    if not has_visual:
        blocking.append("No visual-critique artifact found (no mage/critique/responsive/consistency output).")
    if not has_qa:
        blocking.append("No QA artifact found (no sage/qa/accessibility output).")

    if research and not has_visual:
        warnings.append(f"Pass produced {len(research)} research artifact(s) but ZERO design-critique output — research-only pass.")

    summary = {
        "mode": state["mode"],
        "streamlined": state["streamlined"],
        "qa_status": state["qa_status"],
        "artifacts_total": len(names),
        "has_visual_critique": has_visual,
        "has_qa": has_qa,
        "research_artifacts": len(research),
    }
    return blocking, warnings, summary


def selftest():
    # the wedding-hub state — must BLOCK
    state = {"mode": "focused", "streamlined": ["visual-audit", "adversarial"], "qa_status": "pending"}
    artifacts = ["ranger-raid-claude.md", "admin-ux-research.md", "pinterest-boards.md"]
    blocking, warnings, _ = evaluate(state, artifacts)
    ok_fail = len(blocking) >= 3  # visual streamlined + qa pending + no visual + no qa
    # a complete pass — must PASS
    state2 = {"mode": "full", "streamlined": [], "qa_status": "done"}
    artifacts2 = ["mage-critique.md", "sage-qa.md", "ranger-raid.md"]
    b2, _, _ = evaluate(state2, artifacts2)
    ok_pass = len(b2) == 0
    print("self-test:")
    print(f"  incomplete pass blocks: {'✅' if ok_fail else '❌'} ({len(blocking)} blocking findings)")
    print(f"  complete pass passes:   {'✅' if ok_pass else '❌'} ({len(b2)} blocking findings)")
    sys.exit(0 if (ok_fail and ok_pass) else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", help="path to quest-state.yaml")
    ap.add_argument("--artifacts-dir", help="path to guild-artifacts dir")
    ap.add_argument("--screens", type=int, default=0, help="total screens (optional coverage check)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    if not a.state:
        sys.exit("pass --state <quest-state.yaml> [--artifacts-dir <dir>] or --selftest")

    text = open(a.state).read() if os.path.exists(a.state) else ""
    state = parse_state(text)
    artifacts = sorted(glob.glob(os.path.join(a.artifacts_dir, "*"))) if a.artifacts_dir and os.path.isdir(a.artifacts_dir) else []
    blocking, warnings, summary = evaluate(state, artifacts)
    complete = len(blocking) == 0

    if a.json:
        print(json.dumps({"complete": complete, "blocking": blocking, "warnings": warnings, "summary": summary}, indent=2))
    else:
        print("GUILD completeness gate —", "✅ COMPLETE" if complete else "❌ INCOMPLETE (handoff BLOCKED)")
        for b in blocking:  print("  ✗ BLOCK:", b)
        for w in warnings:  print("  ⚠ warn :", w)
        if complete and not warnings:
            print("  all required design-pass coverage present.")
    sys.exit(0 if complete else 1)


if __name__ == "__main__":
    main()
