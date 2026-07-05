# Drift And Hallucination Proof Harness

Goal: prove whether GUILD stays grounded during representative work, and make drift visible when it happens.

## What This Proves

- Fact and insight claims can be checked against a fixed evidence packet.
- Unsupported claims, missing citations, wrong citations, and known-forbidden invented claims fail deterministically.
- Assumptions can still be useful, but only when explicitly labeled as assumptions.

## Benchmark

- Fixture: `docs/guild/evals/grounding-benchmark.json`
- Guard: `scripts/drift-guard.py`
- Sample checked output: `guild-artifacts/drift-proof/sample-guild-claims.json`

## Current Result

The first harness run is a source-grounding proof over the recent Hall work, not a claim that GUILD can never hallucinate. It proves the gate catches hallucinated claims and passes a grounded Hall summary.

Run:

```bash
python3 -m py_compile scripts/drift-guard.py
python3 scripts/drift-guard.py --selftest
python3 scripts/drift-guard.py --check --outputs guild-artifacts/drift-proof/sample-guild-claims.json
npm run validate
git diff --check
```

Result:

- `golden-pass`: pass, 0 unsupported claims.
- `golden-fail`: expected fail, 2 unsupported claims caught.
- `hall-agent-fronted-summary`: pass, 0 unsupported claims.
- Full validation: pass, 11 checks, 0 failures.

To prove live GUILD behavior, run representative Guild tasks, export each output as a claim ledger, then run:

```bash
python3 scripts/drift-guard.py --outputs guild-artifacts/drift-proof
```

## Pass Bar For A Real Study

- 0 unsupported fact or insight claims.
- 100% of fact and insight claims cite a benchmark source.
- All assumptions are labeled `ASSUMPTION`.
- Any failure becomes either a prompt fix, source-packet fix, or blocking artifact gate.

## Mitigation If Drift Appears

1. Add claim-ledger output to fact-heavy Guild artifacts.
2. Require `scripts/drift-guard.py --outputs <run-dir>` before marking the run verified.
3. Route unsupported claims into the exception queue instead of silently shipping them.
4. Expand `grounding-benchmark.json` with each owner-corrected hallucination so regressions stay caught.
