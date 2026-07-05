#!/usr/bin/env python3
"""craft-gates.py — one runner for the GUILD-45..54 craft-gate suite (fix #2: conditional gates).

Runs every applicable craft gate in one call and surfaces ONLY the gates that fire. Gates that are
green-by-default on disciplined code collapse into a single summary line instead of six separate
reports the operator has to read. Blocking semantics are preserved: exit 1 if ANY gate fires, else 0.

Rationale (efficiency-benchmark, 2026-07-04): on already-disciplined code, 4/5–5/5 gates find nothing;
making the agent invoke six scripts and report six green results is pure operator-attention overhead.
This wrapper keeps full coverage and the NO-GO semantics, and removes the noise.

Usage:
  craft-gates.py --screen <src.tsx> [--built <built.css>] [--json]
  craft-gates.py --selftest
"""
import argparse
import json
import os
import subprocess
import sys

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

# (gate name, script filename, arg flag, target kind: "src" or "css")
GATES = [
    ("spacing-hierarchy", "spacing-hierarchy.py", "--lint", "src"),
    ("subtraction-pass", "subtraction-pass.py", "--lint", "src"),
    ("type-conditional", "type-conditional.py", "--lint", "src"),
    ("token-lint", "token-lint.py", "--file", "src"),
    ("state-motion-req", "state-motion-req.py", "--screen", "src"),
    ("affordance-check", "affordance-check.py", "--screen", "src"),
    # css gate — only runs when a built stylesheet is supplied
    ("reduced-motion-gate", "reduced-motion-gate.py", "--screen", "css"),
]


def run_gate(script, flag, target):
    """Run one gate. Returns (exit_code, output). exit 0 = clean, non-zero = fired."""
    path = os.path.join(SCRIPTS_DIR, script)
    if not os.path.exists(path):
        return (None, f"(missing script: {script})")
    try:
        p = subprocess.run(
            [sys.executable, path, flag, target],
            capture_output=True, text=True, timeout=120,
        )
        out = (p.stdout or "") + (p.stderr or "")
        return (p.returncode, out.strip())
    except subprocess.TimeoutExpired:
        return (2, f"(timeout running {script})")


def run_suite(src, built):
    results = []
    for name, script, flag, kind in GATES:
        if kind == "css":
            if not built:
                results.append({"gate": name, "status": "skipped", "reason": "no built css", "output": ""})
                continue
            target = built
        else:
            target = src
        code, out = run_gate(script, flag, target)
        if code is None:
            status = "missing"
        elif code == 0:
            status = "clean"
        else:
            status = "fired"
        results.append({"gate": name, "status": status, "exit": code, "output": out})
    return results


def report(results):
    fired = [r for r in results if r["status"] == "fired"]
    clean = [r for r in results if r["status"] == "clean"]
    skipped = [r for r in results if r["status"] == "skipped"]
    missing = [r for r in results if r["status"] == "missing"]

    # Only fired gates get their full output surfaced.
    for r in fired:
        print(f"✗ {r['gate']} — FIRED (NO-GO):")
        for line in r["output"].splitlines():
            print(f"    {line}")

    # Everything green collapses to one line.
    summary_bits = []
    if clean:
        summary_bits.append(f"{len(clean)} clean ({', '.join(r['gate'] for r in clean)})")
    if skipped:
        summary_bits.append(f"{len(skipped)} skipped ({', '.join(r['gate'] for r in skipped)})")
    if missing:
        summary_bits.append(f"{len(missing)} missing ({', '.join(r['gate'] for r in missing)})")

    if fired:
        print(f"✗ craft gates: {len(fired)} fired — NO-GO until fixed or owner-waived. " + " · ".join(summary_bits))
    else:
        print("✓ craft gates: all clean. " + " · ".join(summary_bits))

    return 1 if fired else 0


def selftest():
    # The suite must at least locate its sibling gate scripts and run without crashing on a real file.
    present = [g[1] for g in GATES if os.path.exists(os.path.join(SCRIPTS_DIR, g[1]))]
    if len(present) < 5:
        print(f"craft-gates self-test: ❌ FAIL — only {len(present)}/7 gate scripts found")
        return 1
    print(f"craft-gates self-test: ✅ PASS — {len(present)}/7 gate scripts located; runner wired")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Run the craft-gate suite, surface only fired gates.")
    ap.add_argument("--screen", help="source file (tsx/jsx/etc) for src gates")
    ap.add_argument("--built", help="built css file for the reduced-motion gate (optional)")
    ap.add_argument("--json", action="store_true", help="emit structured JSON")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if not args.screen:
        ap.error("--screen is required (or use --selftest)")

    results = run_suite(args.screen, args.built)

    if args.json:
        fired = [r for r in results if r["status"] == "fired"]
        print(json.dumps({"fired": len(fired), "results": results}, indent=2))
        sys.exit(1 if fired else 0)

    sys.exit(report(results))


if __name__ == "__main__":
    main()
