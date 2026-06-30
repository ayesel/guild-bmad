#!/usr/bin/env python3
"""
plan-gate.py - GUILD-8: approve the plan before generation.

Plan Mode is the interactive approve-gate before a generation run. It emits a
concise plan (scope, approach, outputs), records approve/edit/reject, and exits
successfully only on approve.

  python3 scripts/plan-gate.py --scope "Today screen" --approach "static HTML" --produces "prototype.html" --decision approve
  python3 scripts/plan-gate.py --selftest
"""
import argparse
import json
import sys

VALID_DECISIONS = {"approve", "edit", "reject"}


def make_plan(scope, approach, produces):
    outputs = produces or []
    return {
        "scope": scope.strip(),
        "approach": approach.strip(),
        "produces": [p.strip() for p in outputs if p.strip()],
    }


def validate_plan(plan):
    missing = [k for k in ("scope", "approach", "produces") if not plan.get(k)]
    if missing:
        return [f"missing plan field(s): {', '.join(missing)}"]
    return []


def decide(plan, decision, edit=None):
    if decision not in VALID_DECISIONS:
        raise ValueError(f"decision must be one of: {', '.join(sorted(VALID_DECISIONS))}")
    result = {
        "plan": plan,
        "decision": decision,
        "approved": decision == "approve",
        "may_proceed": decision == "approve",
    }
    if decision == "edit":
        result["requested_edit"] = edit or "edit requested"
    if decision == "reject":
        result["rejection_reason"] = edit or "plan rejected"
    return result


def format_plan(plan):
    lines = [
        "PLAN",
        f"Scope: {plan['scope']}",
        f"Approach: {plan['approach']}",
        "Will produce:",
    ]
    lines.extend(f"- {item}" for item in plan["produces"])
    lines.append("Decision required: approve | edit | reject")
    return "\n".join(lines)


def selftest():
    plan = make_plan(
        "Nourish Today screen",
        "Generate two self-contained HTML candidates, then gate the winner.",
        ["codex-1.html", "codex-2.html"],
    )
    clean = not validate_plan(plan)
    approved = decide(plan, "approve")
    edited = decide(plan, "edit", "show macro variance earlier")
    rejected = decide(plan, "reject", "scope is wrong")
    text = format_plan(plan)
    ok = (
        clean
        and approved["may_proceed"] is True
        and edited["may_proceed"] is False
        and rejected["may_proceed"] is False
        and "Decision required" in text
    )
    print("GUILD-8 plan gate - self-test")
    print(f"   valid plan: {clean}")
    print(f"   approve proceeds: {approved['may_proceed']}")
    print(f"   edit blocks generation: {edited['may_proceed']}")
    print(f"   reject blocks generation: {rejected['may_proceed']}")
    print(f"\n{'PASS' if ok else 'FAIL'} - generation proceeds only on approve.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope")
    ap.add_argument("--approach")
    ap.add_argument("--produces", action="append", default=[])
    ap.add_argument("--decision", choices=sorted(VALID_DECISIONS))
    ap.add_argument("--edit", help="edit request or rejection reason")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
    if not (args.scope and args.approach and args.produces and args.decision):
        sys.exit("pass --scope --approach --produces <item> --decision approve|edit|reject, or --selftest")
    plan = make_plan(args.scope, args.approach, args.produces)
    failures = validate_plan(plan)
    if failures:
        for failure in failures:
            print(f"[NO-GO] {failure}")
        sys.exit(1)
    result = decide(plan, args.decision, args.edit)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_plan(plan))
        print(f"\nDecision: {args.decision}")
        print("Proceed: yes" if result["may_proceed"] else "Proceed: no")
    sys.exit(0 if result["may_proceed"] else 2)


if __name__ == "__main__":
    main()
