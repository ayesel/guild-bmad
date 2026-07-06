#!/usr/bin/env python3
"""
interaction-gate.py - TIME leg v1 gate: ack latency + input blocking +
reduced-motion feedback + form semantics + interaction layout shift.

Metrics judge for the driven interaction suite per
docs/guild/decisions/interaction-factors-research.md (SS2 latency/choreography/
a11y groups, SS3 "BLOCK - driven" items 4/5/9/10/11, SS7 thin-slice pick).
Consumes a JSON produced by the Playwright driving harness (separate, later
build) - this schema IS the contract between harness and judge:

{
  "interactions": [
    {"selector": "#save", "event": "click", "ackMs": 42.0,
     "asyncOp": true, "ackKind": "pressed|optimistic|skeleton|spinner|none"}
  ],
  "blockingProbes": [
    {"transition": "panel-open", "probeAtMs": 50,
     "eventRegistered": true, "pointerEventsNone": false}
  ],
  "reducedMotion": [
    {"interaction": "#save click", "defaultFeedback": true, "reducedFeedback": true}
  ],
  "forms": [
    {"field": "#email", "errorBeforeBlur": false, "ariaAssociated": true,
     "focusToFirstError": true, "clearsOnCorrect": true}
  ],
  "layoutShifts": [
    {"source": "#toast", "value": 0.02, "interactionAdjacent": false, "expected": true}
  ]
}

All checks are BLOCK-tier (exit 1); the ADVISE/LOOK items from SS3 route to
the WA lane, not this gate. Failure names match the decision-doc vocabulary:
ack-latency, async-unacknowledged, input-blocked-mid-transition,
reduced-motion-deletes-feedback, premature-validation, error-not-associated,
no-focus-to-first-error, error-not-cleared-on-correct, layout-shift-budget,
interaction-adjacent-shift.

  python3 scripts/interaction-gate.py --metrics interaction.json [--json]
  python3 scripts/interaction-gate.py --selftest
"""
import argparse
import json
import sys

ACK_MAX_MS = 100.0   # Nielsen/Miller perceptual acknowledgment limit
                     # (distinct from INP 200ms and the 400/500ms duration envelope)
CLS_BUDGET = 0.1     # web.dev CLS "good" threshold, applied to unexpected shifts


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_interactions(items, out):
    for it in items:
        who = f'{it.get("selector", "<unknown>")} {it.get("event", "event")}'
        ack = float(it.get("ackMs", 0) or 0)
        if ack > ACK_MAX_MS:
            out.append(f"ack-latency: {who} first visual change at {ack:g}ms; limit {ACK_MAX_MS:g}ms")
        if bool(it.get("asyncOp", False)) and str(it.get("ackKind", "none")) == "none":
            out.append(
                f"async-unacknowledged: {who} slow async op with no pressed/optimistic/skeleton/spinner acknowledgment"
            )


def check_blocking_probes(items, out):
    for probe in items:
        where = f'{probe.get("transition", "<transition>")} @ {probe.get("probeAtMs", "?")}ms'
        reasons = []
        if not bool(probe.get("eventRegistered", True)):
            reasons.append("probe event swallowed")
        if bool(probe.get("pointerEventsNone", False)):
            reasons.append("pointer-events:none on interactive mid-transition")
        if reasons:
            out.append(f"input-blocked-mid-transition: {where}: {'; '.join(reasons)}")


def check_reduced_motion(items, out):
    for entry in items:
        if bool(entry.get("defaultFeedback", False)) and not bool(entry.get("reducedFeedback", False)):
            out.append(
                f'reduced-motion-deletes-feedback: {entry.get("interaction", "<interaction>")} '
                "acknowledges by default but goes silent under prefers-reduced-motion"
            )


def check_forms(items, out):
    for form in items:
        field = form.get("field", "<field>")
        if bool(form.get("errorBeforeBlur", False)):
            out.append(f"premature-validation: {field} errors mid-keystroke before blur/submit")
        if not bool(form.get("ariaAssociated", True)):
            out.append(f"error-not-associated: {field} error lacks aria-invalid/aria-describedby association")
        if not bool(form.get("focusToFirstError", True)):
            out.append(f"no-focus-to-first-error: {field} submit does not move focus to first invalid field")
        if not bool(form.get("clearsOnCorrect", True)):
            out.append(f"error-not-cleared-on-correct: {field} error persists after valid correction")


def check_layout_shifts(items, out):
    unexpected = [s for s in items if not bool(s.get("expected", False))]
    total = sum(float(s.get("value", 0) or 0) for s in unexpected)
    if total > CLS_BUDGET:
        out.append(f"layout-shift-budget: cumulative unexpected shift {total:g} > {CLS_BUDGET:g}")
    for shift in unexpected:
        if bool(shift.get("interactionAdjacent", False)):
            out.append(
                f'interaction-adjacent-shift: {shift.get("source", "<source>")} '
                f'shifted {float(shift.get("value", 0) or 0):g} next to an interaction (defect regardless of aggregate)'
            )


def gate(metrics):
    failures = []
    if not isinstance(metrics, dict) or not any(
        metrics.get(k) for k in ("interactions", "blockingProbes", "reducedMotion", "forms", "layoutShifts")
    ):
        return ["metrics file has no interaction sections"]
    check_interactions(metrics.get("interactions", []), failures)
    check_blocking_probes(metrics.get("blockingProbes", []), failures)
    check_reduced_motion(metrics.get("reducedMotion", []), failures)
    check_forms(metrics.get("forms", []), failures)
    check_layout_shifts(metrics.get("layoutShifts", []), failures)
    return failures


def selftest():
    good = {
        "interactions": [
            {"selector": "#save", "event": "click", "ackMs": 42.0, "asyncOp": True, "ackKind": "spinner"},
            {"selector": "#tab", "event": "keydown", "ackMs": 16.0, "asyncOp": False, "ackKind": "pressed"},
        ],
        "blockingProbes": [
            {"transition": "panel-open", "probeAtMs": 50, "eventRegistered": True, "pointerEventsNone": False},
        ],
        "reducedMotion": [
            {"interaction": "#save click", "defaultFeedback": True, "reducedFeedback": True},
        ],
        "forms": [
            {"field": "#email", "errorBeforeBlur": False, "ariaAssociated": True,
             "focusToFirstError": True, "clearsOnCorrect": True},
        ],
        "layoutShifts": [
            {"source": "#accordion", "value": 0.3, "interactionAdjacent": True, "expected": True},
            {"source": "#banner", "value": 0.04, "interactionAdjacent": False, "expected": False},
        ],
    }
    bad = {
        "interactions": [
            {"selector": "#slow", "event": "click", "ackMs": 240.0, "asyncOp": False, "ackKind": "pressed"},
            {"selector": "#mute", "event": "click", "ackMs": 50.0, "asyncOp": True, "ackKind": "none"},
        ],
        "blockingProbes": [
            {"transition": "modal-fade", "probeAtMs": 50, "eventRegistered": False, "pointerEventsNone": False},
            {"transition": "drawer-slide", "probeAtMs": 50, "eventRegistered": True, "pointerEventsNone": True},
        ],
        "reducedMotion": [
            {"interaction": "#like tap", "defaultFeedback": True, "reducedFeedback": False},
        ],
        "forms": [
            {"field": "#password", "errorBeforeBlur": True, "ariaAssociated": False,
             "focusToFirstError": False, "clearsOnCorrect": False},
        ],
        "layoutShifts": [
            {"source": "#ad", "value": 0.08, "interactionAdjacent": False, "expected": False},
            {"source": "#button-jump", "value": 0.05, "interactionAdjacent": True, "expected": False},
        ],
    }
    good_failures = gate(good)
    bad_failures = gate(bad)
    ok = not good_failures and len(bad_failures) == 11
    print("interaction gate - self-test")
    print(f"   clean run failures: {len(good_failures)}")
    print(f"   defective run failures: {len(bad_failures)} (expect 11)")
    print(f"\n{'PASS' if ok else 'FAIL'} - ack, async-ack, blocking, reduced-motion, form semantics, and CLS checks exercised.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics", help="interaction metrics JSON from the driving harness")
    ap.add_argument("--json", action="store_true", help="emit machine-readable verdict")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    if not a.metrics:
        sys.exit("pass --metrics <interaction.json> or --selftest")
    failures = gate(load_json(a.metrics))
    if a.json:
        print(json.dumps({"status": "NO-GO" if failures else "GO", "block": failures}, indent=2))
        sys.exit(1 if failures else 0)
    if failures:
        print("[NO-GO] interaction gate failed")
        for failure in failures:
            print(f" - {failure}")
        sys.exit(1)
    print("[GO] interaction gate passed")


if __name__ == "__main__":
    main()
