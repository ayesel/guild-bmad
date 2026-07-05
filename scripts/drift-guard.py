#!/usr/bin/env python3
"""Source-grounding benchmark for Guild outputs.

The guard validates a simple claim ledger:

{
  "case_id": "nourish-product-brief",
  "claims": [
    {"kind": "fact", "text": "...", "source": "NOURISH-1"},
    {"kind": "assumption", "text": "ASSUMPTION: ..."}
  ]
}

Fact and insight claims must match the benchmark's supported claims and cite an
allowed source. Assumptions are allowed only when labeled explicitly.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BENCHMARK = ROOT / "docs/guild/evals/grounding-benchmark.json"


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def benchmark_index(benchmark: dict) -> dict[str, dict]:
    cases = {}
    for case in benchmark.get("cases", []):
        supported = {}
        for claim in case.get("supported_claims", []):
            supported[normalize(claim.get("text", ""))] = claim
        source_ids = {source.get("id") for source in case.get("sources", [])}
        cases[case["id"]] = {
            "case": case,
            "supported": supported,
            "source_ids": source_ids,
            "forbidden": [normalize(x) for x in case.get("forbidden_phrases", [])],
        }
    return cases


def validate_output(output: dict, benchmark: dict) -> dict:
    cases = benchmark_index(benchmark)
    case_id = output.get("case_id")
    result = {
        "id": output.get("id", "output"),
        "case_id": case_id,
        "claims": len(output.get("claims", [])),
        "checked_claims": 0,
        "unsupported_claims": 0,
        "failures": [],
    }
    if case_id not in cases:
        result["failures"].append(f"unknown case_id: {case_id}")
        result["unsupported_claims"] += 1
        return result

    spec = cases[case_id]
    policy = benchmark.get("policy", {})
    for i, claim in enumerate(output.get("claims", []), start=1):
        kind = claim.get("kind", "fact")
        text = claim.get("text", "")
        text_norm = normalize(text)
        if not text_norm:
            result["failures"].append(f"claim {i}: empty text")
            result["unsupported_claims"] += 1
            continue
        for phrase in spec["forbidden"]:
            if phrase and phrase in text_norm:
                result["failures"].append(f"claim {i}: forbidden phrase in claim: {text}")
                result["unsupported_claims"] += 1
                break
        else:
            if kind == "assumption":
                if policy.get("assumptions_must_be_labeled", True) and "assumption" not in text_norm:
                    result["failures"].append(f"claim {i}: assumption is not labeled")
                    result["unsupported_claims"] += 1
                continue

            result["checked_claims"] += 1
            source = claim.get("source")
            if policy.get("fact_claims_require_source", True) and not source:
                result["failures"].append(f"claim {i}: fact/insight claim missing source")
                result["unsupported_claims"] += 1
                continue
            if source and source not in spec["source_ids"]:
                result["failures"].append(f"claim {i}: unknown source {source}")
                result["unsupported_claims"] += 1
                continue
            supported = spec["supported"].get(text_norm)
            if not supported:
                result["failures"].append(f"claim {i}: unsupported claim: {text}")
                result["unsupported_claims"] += 1
                continue
            if source and source not in supported.get("sources", []):
                result["failures"].append(f"claim {i}: source {source} does not support claim")
                result["unsupported_claims"] += 1

    checked = max(result["checked_claims"], 1)
    result["unsupported_claim_rate"] = result["unsupported_claims"] / checked
    max_rate = policy.get("max_unsupported_claim_rate", 0.0)
    result["pass"] = result["unsupported_claim_rate"] <= max_rate and not result["failures"]
    return result


def validate_benchmark(benchmark: dict) -> list[str]:
    failures = []
    seen = set()
    for case in benchmark.get("cases", []):
        case_id = case.get("id")
        if not case_id:
            failures.append("case missing id")
            continue
        if case_id in seen:
            failures.append(f"duplicate case id: {case_id}")
        seen.add(case_id)
        source_ids = {source.get("id") for source in case.get("sources", [])}
        for claim in case.get("supported_claims", []):
            for source in claim.get("sources", []):
                if source not in source_ids:
                    failures.append(f"{case_id}: claim {claim.get('id')} references unknown source {source}")
    return failures


def run_golden(benchmark: dict) -> tuple[list[dict], list[str]]:
    results = []
    failures = []
    for output in benchmark.get("golden_outputs", []):
        result = validate_output(output, benchmark)
        results.append(result)
        expected = bool(output.get("should_pass"))
        if result["pass"] != expected:
            failures.append(
                f"{output.get('id')}: expected pass={expected}, got pass={result['pass']}"
            )
    return results, failures


def collect_outputs(paths: list[str]) -> list[dict]:
    outputs = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for child in sorted(path.glob("*.json")):
                outputs.append(load_json(child))
        else:
            outputs.append(load_json(path))
    return outputs


def print_results(results: list[dict]) -> None:
    for result in results:
        status = "PASS" if result["pass"] else "FAIL"
        print(
            f"{status} {result['id']} case={result['case_id']} "
            f"claims={result['claims']} unsupported={result['unsupported_claims']} "
            f"rate={result['unsupported_claim_rate']:.2f}"
        )
        for failure in result["failures"]:
            print(f"  - {failure}")


def selftest() -> int:
    benchmark = load_json(DEFAULT_BENCHMARK)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "pass.json"
        path.write_text(json.dumps(benchmark["golden_outputs"][0]), encoding="utf-8")
        result = validate_output(load_json(path), benchmark)
    _, golden_failures = run_golden(benchmark)
    ok = result["pass"] and not golden_failures and not validate_benchmark(benchmark)
    print("GUILD drift guard - self-test")
    print(f"  golden outputs: {len(benchmark.get('golden_outputs', []))}")
    print(f"  temp pass output: {'PASS' if result['pass'] else 'FAIL'}")
    print(f"\n{'PASS' if ok else 'FAIL'} - grounding benchmark detects supported and unsupported claims.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark", default=str(DEFAULT_BENCHMARK))
    ap.add_argument("--outputs", nargs="*", default=[], help="claim-ledger JSON files or directories")
    ap.add_argument("--check", action="store_true", help="validate benchmark and golden examples")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    benchmark = load_json(Path(args.benchmark))
    failures = validate_benchmark(benchmark)
    results = []

    if args.check:
        golden_results, golden_failures = run_golden(benchmark)
        results.extend(golden_results)
        failures.extend(golden_failures)

    for output in collect_outputs(args.outputs):
        result = validate_output(output, benchmark)
        results.append(result)
        if not result["pass"]:
            failures.append(f"{result['id']}: {len(result['failures'])} grounding failure(s)")

    if args.json:
        print(json.dumps({"pass": not failures, "results": results, "failures": failures}, indent=2))
    else:
        if results:
            print_results(results)
        if failures:
            print("NO-GO - drift guard failed")
            for failure in failures:
                print(f"  - {failure}")
        else:
            print("PASS - drift guard benchmark and claim outputs are source-grounded")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
