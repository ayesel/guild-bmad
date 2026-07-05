#!/usr/bin/env python3
"""
token-footprint.py - GUILD prompt/context footprint measurement.

Measures the static prompt surfaces most likely to enter agent context: slash
commands, agent specs, compiled agents, sidecar references, and core context.
The estimate is deterministic and dependency-free so it can run in CI.

  python3 scripts/token-footprint.py --report
  python3 scripts/token-footprint.py --check
  python3 scripts/token-footprint.py --selftest
"""
import argparse
import glob
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SURFACES = [
    {
        "name": "claude_commands",
        "label": "Claude slash commands",
        "patterns": [".claude/commands/guild-*.md"],
        "max_file_tokens": 8000,
        "warn_file_tokens": 5500,
        "max_total_tokens": 50000,
    },
    {
        "name": "cursor_commands",
        "label": "Cursor slash commands",
        "patterns": [".cursor/commands/guild-*.md", ".cursor/commands/*.md"],
        "max_file_tokens": 8000,
        "warn_file_tokens": 5500,
        "max_total_tokens": 50000,
    },
    {
        "name": "gemini_commands",
        "label": "Gemini slash commands",
        "patterns": [".gemini/commands/guild-*.toml", ".gemini/commands/*.toml"],
        "max_file_tokens": 8000,
        "warn_file_tokens": 5500,
        "max_total_tokens": 50000,
    },
    {
        "name": "source_agents",
        "label": "Source agent YAML",
        "patterns": ["src/modules/guild/agents/*.agent.yaml"],
        "max_file_tokens": 6000,
        "warn_file_tokens": 4000,
        "max_total_tokens": 40000,
    },
    {
        "name": "compiled_agents",
        "label": "Compiled agent prompts",
        "patterns": ["_bmad/guild/agents/*.md"],
        "max_file_tokens": 6000,
        "warn_file_tokens": 4000,
        "max_total_tokens": 35000,
    },
    {
        "name": "sidecar_refs",
        "label": "Sidecar references",
        "patterns": [
            "src/modules/guild/agents/*-sidecar/**/*.md",
            "src/modules/guild/agents/shared-sidecar/*.md",
        ],
        "max_file_tokens": 6000,
        "warn_file_tokens": 4000,
        "max_total_tokens": 65000,
    },
    {
        "name": "core_context",
        "label": "Core context docs",
        "patterns": [
            "CLAUDE.md",
            "AGENTS.md",
            "docs/guild/WAKE-PROMPT.md",
            "docs/guild/context.yaml",
        ],
        "max_file_tokens": 6000,
        "warn_file_tokens": 3500,
        "max_total_tokens": 16000,
    },
]

POLICY = {
    "token_estimate": "ceil(words * 1.33 + punctuation * 0.08)",
    "max_hot_surface_tokens": 250000,
    "warn_hot_surface_tokens": 200000,
    "surfaces": SURFACES,
}


def estimate_tokens(text):
    words = len(re.findall(r"\w+", text))
    punctuation = len(re.findall(r"[^\w\s]", text))
    return int(math.ceil(words * 1.33 + punctuation * 0.08))


def rel(path):
    return os.path.relpath(path, ROOT)


def files_for(patterns):
    seen = set()
    out = []
    for pattern in patterns:
        for path in glob.glob(os.path.join(ROOT, pattern), recursive=True):
            if not os.path.isfile(path) or path in seen:
                continue
            seen.add(path)
            out.append(path)
    return sorted(out)


def measure_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return {
        "path": rel(path),
        "bytes": len(text.encode("utf-8")),
        "words": len(re.findall(r"\w+", text)),
        "tokens_est": estimate_tokens(text),
    }


def measure(policy=POLICY):
    surfaces = []
    hot_total = 0
    for spec in policy["surfaces"]:
        rows = [measure_file(path) for path in files_for(spec["patterns"])]
        total = sum(row["tokens_est"] for row in rows)
        hot_total += total
        surfaces.append({
            "name": spec["name"],
            "label": spec["label"],
            "file_count": len(rows),
            "tokens_est": total,
            "max_total_tokens": spec["max_total_tokens"],
            "warn_file_tokens": spec["warn_file_tokens"],
            "max_file_tokens": spec["max_file_tokens"],
            "top_files": sorted(rows, key=lambda row: row["tokens_est"], reverse=True)[:10],
        })
    return {
        "token_estimate": policy["token_estimate"],
        "hot_surface_tokens_est": hot_total,
        "warn_hot_surface_tokens": policy["warn_hot_surface_tokens"],
        "max_hot_surface_tokens": policy["max_hot_surface_tokens"],
        "surfaces": surfaces,
    }


def gate(report):
    failures = []
    warnings = []
    hot = report["hot_surface_tokens_est"]
    if hot > report["max_hot_surface_tokens"]:
        failures.append(f"hot prompt surface {hot} > {report['max_hot_surface_tokens']} tokens")
    elif hot > report["warn_hot_surface_tokens"]:
        warnings.append(f"hot prompt surface {hot} > warning {report['warn_hot_surface_tokens']} tokens")

    for surface in report["surfaces"]:
        if surface["tokens_est"] > surface["max_total_tokens"]:
            failures.append(
                f"{surface['label']} total {surface['tokens_est']} > {surface['max_total_tokens']} tokens"
            )
        for row in surface["top_files"]:
            if row["tokens_est"] > surface["max_file_tokens"]:
                failures.append(
                    f"{row['path']} {row['tokens_est']} > {surface['max_file_tokens']} tokens"
                )
            elif row["tokens_est"] > surface["warn_file_tokens"]:
                warnings.append(
                    f"{row['path']} {row['tokens_est']} > warning {surface['warn_file_tokens']} tokens"
                )
    return failures, warnings


def print_report(report, failures=None, warnings=None):
    print("GUILD token footprint")
    print(f"  estimate: {report['token_estimate']}")
    print(
        f"  hot surface: {report['hot_surface_tokens_est']} tokens "
        f"(warn {report['warn_hot_surface_tokens']}, max {report['max_hot_surface_tokens']})"
    )
    for surface in report["surfaces"]:
        print(
            f"\n{surface['label']}: {surface['tokens_est']} tokens across "
            f"{surface['file_count']} files (max {surface['max_total_tokens']})"
        )
        for row in surface["top_files"][:5]:
            print(f"  {row['tokens_est']:>6}  {row['path']}")
    if warnings:
        print("\nWarnings")
        for warning in warnings:
            print(f"  [WARN] {warning}")
    if failures:
        print("\nFailures")
        for failure in failures:
            print(f"  [NO-GO] {failure}")


def selftest():
    tiny = estimate_tokens("Guild keeps prompts lean.")
    verbose = estimate_tokens(("word " * 1000) + ("!" * 100))
    fake = {
        "hot_surface_tokens_est": 260000,
        "warn_hot_surface_tokens": 200000,
        "max_hot_surface_tokens": 250000,
        "surfaces": [{
            "label": "Fake surface",
            "tokens_est": 9000,
            "max_total_tokens": 8000,
            "warn_file_tokens": 1000,
            "max_file_tokens": 1200,
            "top_files": [{"path": "fake.md", "tokens_est": 1400}],
        }],
    }
    failures, warnings = gate(fake)
    ok = tiny > 0 and verbose > tiny and len(failures) == 3 and not warnings
    print("GUILD token footprint - self-test")
    print(f"   tiny estimate: {tiny}")
    print(f"   verbose estimate: {verbose}")
    print(f"   over-budget failures: {len(failures)}")
    print(f"\n{'PASS' if ok else 'FAIL'} - token estimator and budget gate exercised.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail on hard budget violations")
    ap.add_argument("--json", action="store_true", help="print report as JSON")
    ap.add_argument("--policy", action="store_true", help="print policy as JSON")
    ap.add_argument("--report", action="store_true", help="print human-readable report")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        selftest()
    if args.policy:
        print(json.dumps(POLICY, indent=2))
        return

    report = measure()
    failures, warnings = gate(report)
    if args.json:
        report["warnings"] = warnings
        report["failures"] = failures
        print(json.dumps(report, indent=2))
    else:
        print_report(report, failures if failures else None, warnings)

    if args.check and (failures or (args.strict and warnings)):
        sys.exit(1)


if __name__ == "__main__":
    main()
