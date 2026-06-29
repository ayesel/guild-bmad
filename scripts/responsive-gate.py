#!/usr/bin/env python3
"""
responsive-gate.py - GUILD-80 blocking responsive gate.

Consumes a breakpoint x state metrics JSON file and fails on the defects that
usually make generated UI feel desktop-squished on small devices:

  python3 scripts/responsive-gate.py --metrics responsive.json
  python3 scripts/responsive-gate.py --selftest

Metric shape:
{
  "breakpoints": [
    {
      "name": "compact", "width": 375, "state": "default",
      "scrollWidth": 390, "clientWidth": 375,
      "touchTargets": [{"selector": "button", "width": 40, "height": 48}],
      "textBlocks": [{"selector": ".copy", "measureCh": 82}],
      "boxes": [{"selector": ".card", "width": 0, "height": 42, "clipped": false}],
      "order": [{"selector": "#a", "domIndex": 0, "visualIndex": 1}]
    }
  ]
}
"""
import argparse
import json
import sys

TOUCH_MIN_CSS_PX = 44
TOUCH_MIN_DP = 48
MEASURE_MIN_CH = 45
MEASURE_MAX_CH = 75


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def entries(metrics):
    if isinstance(metrics, list):
        return metrics
    return metrics.get("breakpoints") or metrics.get("matrix") or []


def label(entry):
    bits = [str(entry.get("name") or entry.get("breakpoint") or "breakpoint")]
    if entry.get("state"):
        bits.append(str(entry["state"]))
    if entry.get("width"):
        bits.append(f'{entry["width"]}px')
    return " / ".join(bits)


def check_entry(entry):
    failures = []
    where = label(entry)
    scroll_width = int(entry.get("scrollWidth", entry.get("scroll_width", 0)) or 0)
    client_width = int(entry.get("clientWidth", entry.get("client_width", 0)) or 0)
    if client_width and scroll_width > client_width:
        failures.append(
            f"{where}: horizontal overflow scrollWidth={scroll_width} > clientWidth={client_width}"
        )

    touch_floor = int(entry.get("touchMin", entry.get("touch_min", TOUCH_MIN_CSS_PX)) or TOUCH_MIN_CSS_PX)
    touch_floor = max(touch_floor, TOUCH_MIN_CSS_PX)
    for target in entry.get("touchTargets", entry.get("touch_targets", [])):
        w = float(target.get("width", 0) or 0)
        h = float(target.get("height", 0) or 0)
        if w < touch_floor or h < touch_floor:
            failures.append(
                f"{where}: touch target {target.get('selector', '<unknown>')} is {w:g}x{h:g}px; min {touch_floor}px"
            )

    for target in entry.get("materialTouchTargets", entry.get("material_touch_targets", [])):
        w = float(target.get("width", 0) or 0)
        h = float(target.get("height", 0) or 0)
        if w < TOUCH_MIN_DP or h < TOUCH_MIN_DP:
            failures.append(
                f"{where}: Material touch target {target.get('selector', '<unknown>')} is {w:g}x{h:g}dp; min {TOUCH_MIN_DP}dp"
            )

    for block in entry.get("textBlocks", entry.get("text_blocks", [])):
        measure = block.get("measureCh", block.get("measure_ch"))
        if measure is None:
            continue
        measure = float(measure)
        if measure < MEASURE_MIN_CH or measure > MEASURE_MAX_CH:
            failures.append(
                f"{where}: text measure {block.get('selector', '<unknown>')} is {measure:g}ch; allowed {MEASURE_MIN_CH}-{MEASURE_MAX_CH}ch"
            )

    for box in entry.get("boxes", []):
        w = float(box.get("width", 0) or 0)
        h = float(box.get("height", 0) or 0)
        clipped = bool(box.get("clipped", False))
        if w <= 0 or h <= 0 or clipped:
            failures.append(
                f"{where}: reflow break {box.get('selector', '<unknown>')} width={w:g} height={h:g} clipped={clipped}"
            )

    order = entry.get("order", [])
    drift = [
        item for item in order
        if item.get("domIndex") is not None
        and item.get("visualIndex") is not None
        and int(item["domIndex"]) != int(item["visualIndex"])
    ]
    if drift:
        sample = ", ".join(str(i.get("selector", "<unknown>")) for i in drift[:4])
        failures.append(f"{where}: content reorder DOM order differs from visual order: {sample}")
    return failures


def gate(metrics):
    failures = []
    matrix = entries(metrics)
    if not matrix:
        return ["metrics file has no breakpoints/matrix entries"]
    for entry in matrix:
        failures.extend(check_entry(entry))
    return failures


def selftest():
    good = {
        "breakpoints": [{
            "name": "compact", "width": 375, "state": "default",
            "scrollWidth": 375, "clientWidth": 375,
            "touchTargets": [{"selector": "button", "width": 44, "height": 48}],
            "textBlocks": [{"selector": ".copy", "measureCh": 58}],
            "boxes": [{"selector": ".card", "width": 320, "height": 160, "clipped": False}],
            "order": [{"selector": "#a", "domIndex": 0, "visualIndex": 0}],
        }]
    }
    bad = {
        "breakpoints": [{
            "name": "compact", "width": 375, "state": "menu-open",
            "scrollWidth": 420, "clientWidth": 375,
            "touchTargets": [{"selector": ".tiny", "width": 32, "height": 40}],
            "textBlocks": [{"selector": ".measure", "measureCh": 88}],
            "boxes": [{"selector": ".collapsed", "width": 0, "height": 20}],
            "order": [{"selector": "#cta", "domIndex": 1, "visualIndex": 0}],
        }]
    }
    good_failures = gate(good)
    bad_failures = gate(bad)
    ok = not good_failures and len(bad_failures) == 5
    print("GUILD-80 responsive gate - self-test")
    print(f"   clean matrix failures: {len(good_failures)}")
    print(f"   defective matrix failures: {len(bad_failures)}")
    print(f"\n{'PASS' if ok else 'FAIL'} - overflow, touch, measure, reflow, and reorder checks exercised.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics", help="breakpoint x state metrics JSON")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    if not a.metrics:
        sys.exit("pass --metrics <responsive.json> or --selftest")
    failures = gate(load_json(a.metrics))
    if failures:
        print("[NO-GO] responsive gate failed")
        for failure in failures:
            print(f" - {failure}")
        sys.exit(1)
    print("[GO] responsive gate passed")


if __name__ == "__main__":
    main()
