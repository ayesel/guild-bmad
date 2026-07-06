#!/usr/bin/env python3
"""
focus-gate.py - SPACE leg factor 3 gate: focus visibility + keyboard narrative.

Metrics judge for the driven focus/keyboard suite per
docs/guild/decisions/ui-factors-research.md (SS2 factor 3 "Focus visibility +
keyboard narrative", SS3 stage 1 "Perception + operability"). Consumes a JSON
produced by the Playwright driving harness (separate, later build) - this
schema IS the contract between harness and judge:

{
  "pages": [
    {
      "name": "checkout",
      "tabSequence": [
        {"selector": "#buy", "x": 0, "y": 0, "w": 120, "h": 44,
         "visible": true, "obscured": false,
         "indicator": {"contrastRatio": 3.2, "areaPx": 340, "styleDelta": true}}
      ],
      "interactives": [
        {"selector": "#buy", "reachable": true,
         "tabindexMinus1": false, "clickOnly": false}
      ],
      "landmarks": {"main": true, "nav": true, "h1Count": 1, "headingSkips": 0},
      "modals": [
        {"selector": "#dialog", "focusMovedIn": true, "focusReturned": true,
         "tabTrapped": true, "escCloses": true}
      ],
      "routeChanges": [
        {"to": "/done", "focusTarget": "h1", "focusLostToBody": false}
      ]
    }
  ]
}

BLOCK (exit 1): no-focus-indicator (styleDelta false OR indicator contrast
<3:1 OR area below the WCAG 2.4.13 1px-perimeter equivalent 2*(w+h)),
focus-obscured (obscured or invisible tab stop), keyboard-unreachable
(clickOnly / tabindex=-1 / unreachable actionable), tab-vs-visual-order
inversion rate, modal APG contract (focus-in / focus-return / trap / Esc),
route-focus-to-body.
ADVISE (reported, exit 0 if nothing blocks): missing main landmark,
h1Count != 1, heading level skips - per SS2 "BLOCK (heading order ADVISE)".

  python3 scripts/focus-gate.py --metrics focus.json [--json]
  python3 scripts/focus-gate.py --selftest
"""
import argparse
import json
import sys

BLOCK = "BLOCK"
ADVISE = "ADVISE"

INDICATOR_MIN_CONTRAST = 3.0   # WCAG 2.4.11/2.4.13 focus-appearance line
# House threshold: tab order may deviate from top-left reading order a little
# (composite widgets, sticky headers), but when >20% of tab-stop pairs are
# inverted relative to visual order the keyboard narrative is scrambled.
TAB_ORDER_INVERSION_MAX = 0.20


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def pages(metrics):
    if isinstance(metrics, list):
        return metrics
    return metrics.get("pages") or []


def check_indicators(where, seq, out):
    for stop in seq:
        sel = stop.get("selector", "<unknown>")
        ind = stop.get("indicator") or {}
        w = float(stop.get("w", 0) or 0)
        h = float(stop.get("h", 0) or 0)
        perimeter_px = 2 * (w + h)  # 1 CSS px outline equivalent (WCAG 2.4.13)
        reasons = []
        if not bool(ind.get("styleDelta", False)):
            reasons.append("no style delta")
        if float(ind.get("contrastRatio", 0) or 0) < INDICATOR_MIN_CONTRAST:
            reasons.append(
                f'contrast {float(ind.get("contrastRatio", 0) or 0):g} < {INDICATOR_MIN_CONTRAST}'
            )
        if float(ind.get("areaPx", 0) or 0) < perimeter_px:
            reasons.append(
                f'area {float(ind.get("areaPx", 0) or 0):g}px < 1px-perimeter {perimeter_px:g}px'
            )
        if reasons:
            out.append((BLOCK, f"{where}: no-focus-indicator {sel}: {'; '.join(reasons)}"))
        if bool(stop.get("obscured", False)) or not bool(stop.get("visible", True)):
            out.append((BLOCK, f"{where}: focus-obscured {sel}: focused control not visible to user"))


def check_tab_order(where, seq, out):
    pts = [s for s in seq if s.get("x") is not None and s.get("y") is not None]
    n = len(pts)
    if n < 2:
        return
    visual = sorted(range(n), key=lambda i: (float(pts[i]["y"]), float(pts[i]["x"])))
    rank = {idx: r for r, idx in enumerate(visual)}
    pairs = n * (n - 1) // 2
    inversions = sum(
        1 for i in range(n) for j in range(i + 1, n) if rank[i] > rank[j]
    )
    if inversions / pairs > TAB_ORDER_INVERSION_MAX:
        out.append((
            BLOCK,
            f"{where}: tab-vs-visual-order {inversions}/{pairs} pairs inverted "
            f"(> {TAB_ORDER_INVERSION_MAX:.0%} house threshold): tab order jumps against reading order",
        ))


def check_interactives(where, interactives, out):
    for el in interactives:
        sel = el.get("selector", "<unknown>")
        reasons = []
        if bool(el.get("clickOnly", False)):
            reasons.append("click-only handler")
        if bool(el.get("tabindexMinus1", False)):
            reasons.append("tabindex=-1 on actionable")
        if not bool(el.get("reachable", True)):
            reasons.append("not in tab sequence")
        if reasons:
            out.append((BLOCK, f"{where}: keyboard-unreachable {sel}: {'; '.join(reasons)}"))


def check_modals(where, modals, out):
    # APG modal-dialog contract: each leg is a named failure.
    for modal in modals:
        sel = modal.get("selector", "<unknown>")
        if not bool(modal.get("focusMovedIn", False)):
            out.append((BLOCK, f"{where}: modal-no-focus-in {sel}: focus did not move into dialog on open (APG)"))
        if not bool(modal.get("focusReturned", False)):
            out.append((BLOCK, f"{where}: modal-no-focus-return {sel}: focus did not return to trigger on close (APG)"))
        if not bool(modal.get("tabTrapped", False)):
            out.append((BLOCK, f"{where}: modal-tab-escapes {sel}: Tab not trapped inside open dialog (APG)"))
        if not bool(modal.get("escCloses", False)):
            out.append((BLOCK, f"{where}: modal-esc-no-close {sel}: Esc does not close dialog (APG)"))


def check_routes(where, routes, out):
    for route in routes:
        if bool(route.get("focusLostToBody", False)):
            out.append((
                BLOCK,
                f"{where}: route-focus-to-body -> {route.get('to', '<unknown>')}: "
                "SPA route change dropped focus to <body> instead of landmark/heading",
            ))


def check_landmarks(where, landmarks, out):
    if not landmarks:
        return
    if not bool(landmarks.get("main", False)):
        out.append((ADVISE, f"{where}: landmarks missing <main>"))
    h1 = landmarks.get("h1Count")
    if h1 is not None and int(h1) != 1:
        out.append((ADVISE, f"{where}: h1Count={int(h1)}; expected exactly 1"))
    skips = int(landmarks.get("headingSkips", 0) or 0)
    if skips > 0:
        out.append((ADVISE, f"{where}: heading order skips {skips} level(s)"))


def check_page(page):
    findings = []
    where = str(page.get("name") or "page")
    seq = page.get("tabSequence", [])
    check_indicators(where, seq, findings)
    check_tab_order(where, seq, findings)
    check_interactives(where, page.get("interactives", []), findings)
    check_modals(where, page.get("modals", []), findings)
    check_routes(where, page.get("routeChanges", []), findings)
    check_landmarks(where, page.get("landmarks", {}), findings)
    return findings


def gate(metrics):
    findings = []
    plist = pages(metrics)
    if not plist:
        return [(BLOCK, "metrics file has no pages")]
    for page in plist:
        findings.extend(check_page(page))
    return findings


def split(findings):
    return (
        [msg for sev, msg in findings if sev == BLOCK],
        [msg for sev, msg in findings if sev == ADVISE],
    )


def selftest():
    good = {
        "pages": [{
            "name": "clean",
            "tabSequence": [
                {"selector": "#a", "x": 0, "y": 0, "w": 120, "h": 44, "visible": True,
                 "obscured": False,
                 "indicator": {"contrastRatio": 3.5, "areaPx": 340, "styleDelta": True}},
                {"selector": "#b", "x": 0, "y": 60, "w": 120, "h": 44, "visible": True,
                 "obscured": False,
                 "indicator": {"contrastRatio": 4.0, "areaPx": 340, "styleDelta": True}},
            ],
            "interactives": [
                {"selector": "#a", "reachable": True, "tabindexMinus1": False, "clickOnly": False},
            ],
            "landmarks": {"main": True, "nav": True, "h1Count": 1, "headingSkips": 0},
            "modals": [
                {"selector": "#dlg", "focusMovedIn": True, "focusReturned": True,
                 "tabTrapped": True, "escCloses": True},
            ],
            "routeChanges": [
                {"to": "/done", "focusTarget": "h1", "focusLostToBody": False},
            ],
        }]
    }
    ok_ind = {"contrastRatio": 3.5, "areaPx": 340, "styleDelta": True}
    bad = {
        "pages": [
            {
                "name": "broken",
                "tabSequence": [
                    # ascending y -> tab order clean here; each stop fails one indicator leg
                    {"selector": "#nodelta", "x": 0, "y": 0, "w": 100, "h": 40, "visible": True,
                     "obscured": False,
                     "indicator": {"contrastRatio": 5.0, "areaPx": 300, "styleDelta": False}},
                    {"selector": "#lowcontrast", "x": 0, "y": 50, "w": 100, "h": 40, "visible": True,
                     "obscured": False,
                     "indicator": {"contrastRatio": 2.0, "areaPx": 300, "styleDelta": True}},
                    {"selector": "#thin", "x": 0, "y": 100, "w": 100, "h": 40, "visible": True,
                     "obscured": False,
                     "indicator": {"contrastRatio": 5.0, "areaPx": 100, "styleDelta": True}},
                    {"selector": "#hidden", "x": 0, "y": 150, "w": 100, "h": 40, "visible": True,
                     "obscured": True, "indicator": dict(ok_ind)},
                ],
                "interactives": [
                    {"selector": "#clicky", "reachable": True, "tabindexMinus1": False, "clickOnly": True},
                    {"selector": "#minusone", "reachable": True, "tabindexMinus1": True, "clickOnly": False},
                    {"selector": "#island", "reachable": False, "tabindexMinus1": False, "clickOnly": False},
                ],
                "landmarks": {"main": False, "nav": True, "h1Count": 2, "headingSkips": 1},
                "modals": [
                    {"selector": "#dlg", "focusMovedIn": False, "focusReturned": False,
                     "tabTrapped": False, "escCloses": False},
                ],
                "routeChanges": [
                    {"to": "/next", "focusTarget": None, "focusLostToBody": True},
                ],
            },
            {
                "name": "scrambled",
                # tab order A(y=200) B(y=0) C(y=100): 2/3 pairs inverted > 20%
                "tabSequence": [
                    {"selector": "#A", "x": 0, "y": 200, "w": 100, "h": 40, "visible": True,
                     "obscured": False, "indicator": dict(ok_ind)},
                    {"selector": "#B", "x": 0, "y": 0, "w": 100, "h": 40, "visible": True,
                     "obscured": False, "indicator": dict(ok_ind)},
                    {"selector": "#C", "x": 0, "y": 100, "w": 100, "h": 40, "visible": True,
                     "obscured": False, "indicator": dict(ok_ind)},
                ],
            },
        ]
    }
    advisory_only = {
        "pages": [{
            "name": "advisory",
            "tabSequence": good["pages"][0]["tabSequence"],
            "landmarks": {"main": False, "nav": False, "h1Count": 0, "headingSkips": 2},
        }]
    }
    good_block, good_advise = split(gate(good))
    bad_block, bad_advise = split(gate(bad))
    adv_block, adv_advise = split(gate(advisory_only))
    ok = (
        not good_block and not good_advise
        and len(bad_block) == 13 and len(bad_advise) == 3
        and not adv_block and len(adv_advise) == 3
    )
    print("focus gate - self-test")
    print(f"   clean pages: {len(good_block)} block / {len(good_advise)} advise")
    print(f"   defective pages: {len(bad_block)} block / {len(bad_advise)} advise (expect 13/3)")
    print(f"   advisory-only page: {len(adv_block)} block / {len(adv_advise)} advise (expect 0/3 -> GO)")
    print(f"\n{'PASS' if ok else 'FAIL'} - indicator, obscured, reach, tab-order, modal APG, route, landmark checks exercised.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics", help="focus/keyboard metrics JSON from the driving harness")
    ap.add_argument("--json", action="store_true", help="emit machine-readable verdict")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    if not a.metrics:
        sys.exit("pass --metrics <focus.json> or --selftest")
    block, advise = split(gate(load_json(a.metrics)))
    if a.json:
        print(json.dumps({"status": "NO-GO" if block else "GO", "block": block, "advise": advise}, indent=2))
        sys.exit(1 if block else 0)
    if block:
        print("[NO-GO] focus gate failed")
        for failure in block:
            print(f" - {failure}")
    else:
        print("[GO] focus gate passed")
    for note in advise:
        print(f" ~ ADVISE {note}")
    sys.exit(1 if block else 0)


if __name__ == "__main__":
    main()
