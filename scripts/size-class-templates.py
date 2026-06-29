#!/usr/bin/env python3
"""
size-class-templates.py - GUILD-82 adaptive size-class layout templates.

Provides GUILD's platform-neutral compact/medium/expanded vocabulary and three
canonical layouts: feed, list-detail, and supporting-pane.

  python3 scripts/size-class-templates.py --layout list-detail --width 1024
  python3 scripts/size-class-templates.py --export docs/guild/exports/size-class-templates.json
  python3 scripts/size-class-templates.py --selftest
"""
import argparse
import json
import sys

SIZE_CLASSES = [
    {"name": "compact", "min": 0, "max": 599, "apple": "compact", "material": "compact"},
    {"name": "medium", "min": 600, "max": 839, "apple": "regular-width transitional", "material": "medium"},
    {"name": "expanded", "min": 840, "max": None, "apple": "regular", "material": "expanded"},
]

TEMPLATES = {
    "feed": {
        "compact": {
            "navigation": "bottom-tab-bar",
            "regions": ["top-app-bar", "single-column-feed", "bottom-tab-bar"],
            "grid": "1 column, minmax(0, 1fr)",
            "safe_area": "pad block-end and inline edges",
            "touch_target_min": 48,
        },
        "medium": {
            "navigation": "navigation-rail",
            "regions": ["navigation-rail", "feed-grid"],
            "grid": "rail + 2-column feed",
            "safe_area": "pad inline edges",
            "touch_target_min": 48,
        },
        "expanded": {
            "navigation": "sidebar",
            "regions": ["sidebar", "feed-grid", "optional-context-panel"],
            "grid": "sidebar + 3-column feed + optional panel",
            "safe_area": "pad inline edges",
            "touch_target_min": 44,
        },
    },
    "list-detail": {
        "compact": {
            "navigation": "bottom-tab-bar",
            "regions": ["list-or-detail-route", "bottom-tab-bar"],
            "grid": "1 column; detail replaces list",
            "safe_area": "pad block-end and inline edges",
            "touch_target_min": 48,
        },
        "medium": {
            "navigation": "navigation-rail",
            "regions": ["navigation-rail", "list", "detail"],
            "grid": "rail + minmax(18rem, 35%) + minmax(0, 1fr)",
            "safe_area": "pad inline edges",
            "touch_target_min": 48,
        },
        "expanded": {
            "navigation": "sidebar",
            "regions": ["sidebar", "list", "detail"],
            "grid": "16rem sidebar + 22rem list + minmax(0, 1fr)",
            "safe_area": "pad inline edges",
            "touch_target_min": 44,
        },
    },
    "supporting-pane": {
        "compact": {
            "navigation": "bottom-tab-bar",
            "regions": ["primary-route", "supporting-sheet-on-demand", "bottom-tab-bar"],
            "grid": "1 column; supporting pane becomes sheet",
            "safe_area": "pad block-end and inline edges",
            "touch_target_min": 48,
        },
        "medium": {
            "navigation": "navigation-rail",
            "regions": ["navigation-rail", "primary", "supporting-pane"],
            "grid": "rail + minmax(0, 1fr) + minmax(16rem, 30%)",
            "safe_area": "pad inline edges",
            "touch_target_min": 48,
        },
        "expanded": {
            "navigation": "sidebar",
            "regions": ["sidebar", "primary", "supporting-pane"],
            "grid": "16rem sidebar + minmax(0, 1fr) + minmax(20rem, 28rem)",
            "safe_area": "pad inline edges",
            "touch_target_min": 44,
        },
    },
}


def classify(width):
    for size in SIZE_CLASSES:
        if width >= size["min"] and (size["max"] is None or width <= size["max"]):
            return size["name"]
    return "expanded"


def render(layout, width):
    if layout not in TEMPLATES:
        raise SystemExit(f"unknown layout {layout}; choose one of {', '.join(sorted(TEMPLATES))}")
    size = classify(width)
    return {
        "layout": layout,
        "width": width,
        "size_class": size,
        "template": TEMPLATES[layout][size],
        "responsive_contract": {
            "platform_vocabulary": SIZE_CLASSES,
            "consistent": ["brand", "information_architecture", "core_flow", "content_model"],
            "diverge_by_platform": ["navigation", "gesture", "safe_area", "touch_target"],
        },
    }


def export_all():
    return {
        "size_classes": SIZE_CLASSES,
        "layouts": TEMPLATES,
        "rules": {
            "compact": "prioritize one task per view; use bottom navigation or sheets",
            "medium": "introduce rails and two-pane structure when content benefits",
            "expanded": "use persistent sidebars/supporting panes only when they reduce navigation cost",
        },
    }


def selftest():
    compact = render("list-detail", 375)
    expanded = render("list-detail", 1024)
    supporting = render("supporting-pane", 700)
    ok = (
        compact["size_class"] == "compact"
        and compact["template"]["navigation"] == "bottom-tab-bar"
        and expanded["size_class"] == "expanded"
        and expanded["template"]["navigation"] == "sidebar"
        and "supporting-pane" in supporting["template"]["regions"]
    )
    print("GUILD-82 size-class templates - self-test")
    print(f"   375px list-detail nav: {compact['template']['navigation']}")
    print(f"   1024px list-detail nav: {expanded['template']['navigation']}")
    print(f"   700px supporting regions: {', '.join(supporting['template']['regions'])}")
    print(f"\n{'PASS' if ok else 'FAIL'} - compact tab bar, expanded sidebar, and supporting pane verified.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layout", choices=sorted(TEMPLATES))
    ap.add_argument("--width", type=int, default=375)
    ap.add_argument("--export")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    data = export_all() if a.export else render(a.layout or "feed", a.width)
    if a.export:
        with open(a.export, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
    else:
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
