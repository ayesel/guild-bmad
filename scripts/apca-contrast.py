#!/usr/bin/env python3
"""
apca-contrast.py - APCA-W3 (0.1.9 / SAPC-4g) perceptual contrast utility.

Dark-theme supplement to the WCAG contrast gate — WCAG stays the legal AA
line; APCA catches the pairs WCAG mis-ranks on dark themes and thin type.
Thresholds per the anti-slop survey adoption ledger:

  body text        Lc >= 75   (default --min)
  large/bold text  Lc >= 45
  non-text UI      Lc >= 30

Faithful APCA-W3 0.1.9 math: sRGB -> linear via ^2.4, Y = 0.2126729 R +
0.7151522 G + 0.0721750 B, black soft-clamp Y += (0.022 - Y)^1.414 below
0.022; BoW SAPC = (Ybg^0.56 - Ytxt^0.57) * 1.14, WoB SAPC =
(Ybg^0.65 - Ytxt^0.62) * 1.14; low-contrast clip at |SAPC| < 0.1 -> 0,
else offset by 0.027; scaled x100. Polarity: positive Lc = dark-on-light,
negative Lc = light-on-dark. Pass = |Lc| >= threshold.

  python3 scripts/apca-contrast.py --fg '#888' --bg '#fff'
  python3 scripts/apca-contrast.py --fg 888888 --bg ffffff --min 45
  python3 scripts/apca-contrast.py --pairs pairs.json --json
  python3 scripts/apca-contrast.py --selftest

--pairs JSON: [{"fg": "#888", "bg": "#fff", "role": "body|large|nontext",
"name": "optional label"}] — batch mode exits 1 on any failing pair.
Exit 0 = all pass, 1 = any fail, 2 = usage/input error.
"""
import argparse
import json
import sys

# APCA-W3 0.1.9 (SA98G 4g) constants
S_TRC = 2.4
COEF_R, COEF_G, COEF_B = 0.2126729, 0.7151522, 0.0721750
BLK_THRS, BLK_CLMP = 0.022, 1.414
NORM_BG, NORM_TXT = 0.56, 0.57      # BoW (dark text on light bg)
REV_BG, REV_TXT = 0.65, 0.62        # WoB (light text on dark bg)
SCALE_BOW = SCALE_WOB = 1.14
LO_CLIP = 0.1
LO_BOW_OFFSET = LO_WOB_OFFSET = 0.027
DELTA_Y_MIN = 0.0005

ROLE_MIN = {"body": 75.0, "large": 45.0, "nontext": 30.0}


def parse_hex(s):
    h = s.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError("expected #RGB or #RRGGBB, got %r" % s)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def screen_luminance(rgb):
    r, g, b = ((c / 255.0) ** S_TRC for c in rgb)
    return COEF_R * r + COEF_G * g + COEF_B * b


def soft_clamp(y):
    return y if y >= BLK_THRS else y + (BLK_THRS - y) ** BLK_CLMP


def apca_lc(fg_hex, bg_hex):
    """Lc per APCA-W3 0.1.9. Positive = BoW, negative = WoB."""
    ytxt = soft_clamp(screen_luminance(parse_hex(fg_hex)))
    ybg = soft_clamp(screen_luminance(parse_hex(bg_hex)))
    if abs(ybg - ytxt) < DELTA_Y_MIN:
        return 0.0
    if ybg > ytxt:  # normal polarity: dark text on light background
        sapc = (ybg ** NORM_BG - ytxt ** NORM_TXT) * SCALE_BOW
        out = 0.0 if sapc < LO_CLIP else sapc - LO_BOW_OFFSET
    else:           # reverse polarity: light text on dark background
        sapc = (ybg ** REV_BG - ytxt ** REV_TXT) * SCALE_WOB
        out = 0.0 if sapc > -LO_CLIP else sapc + LO_WOB_OFFSET
    return out * 100.0


def check_pair(fg, bg, role="body", min_lc=None, name=None):
    threshold = float(min_lc) if min_lc is not None else ROLE_MIN[role]
    lc = apca_lc(fg, bg)
    return {"name": name or "%s on %s" % (fg, bg), "fg": fg, "bg": bg,
            "role": role, "lc": round(lc, 3), "min": threshold,
            "pass": abs(lc) >= threshold}


# ------------------------------------------------------------------ selftest

REFERENCE = [  # canonical APCA-W3 documentation check values
    ("#888", "#fff", 63.056),
    ("#fff", "#888", -68.541),
    ("#000", "#aaa", 58.146),
    ("#aaa", "#000", -56.241),
]
REF_TOL = 0.5  # if implementation misses this, fix the math — never widen


def selftest():
    failures = []
    print("apca-contrast self-test (APCA-W3 0.1.9)")
    for fg, bg, expected in REFERENCE:
        got = apca_lc(fg, bg)
        ok = abs(got - expected) <= REF_TOL
        print("   %s on %s: Lc %.4f (expected %.3f, tol %.1f) %s"
              % (fg, bg, got, expected, REF_TOL, "ok" if ok else "MISMATCH"))
        if not ok:
            failures.append("reference %s/%s: got %.4f expected %.3f" % (fg, bg, got, expected))

    zero = apca_lc("#777", "#777")
    if zero != 0.0:
        failures.append("identical colors should yield Lc 0, got %.4f" % zero)

    good_batch = [check_pair("#000", "#fff", "body"),
                  ("#fff", "#0a0a0a", "body"),
                  ("#888", "#fff", "large"),     # 63.06 >= 45
                  ("#767676", "#fff", "nontext")]
    good_batch = [p if isinstance(p, dict) else check_pair(*p) for p in good_batch]
    if not all(p["pass"] for p in good_batch):
        failures.append("golden-pass batch had failures: %s"
                        % [p["name"] for p in good_batch if not p["pass"]])

    bad_batch = [check_pair("#888", "#fff", "body"),   # 63.06 < 75 -> fail
                 check_pair("#000", "#fff", "body")]   # ~106 -> pass
    bad = [p for p in bad_batch if not p["pass"]]
    if len(bad) != 1 or bad[0]["fg"] != "#888":
        failures.append("golden-fail batch: expected exactly #888/#fff body to fail, got %s"
                        % [p["name"] for p in bad])
    print("   golden-fail pair: %s Lc %.3f vs min %.0f -> %s"
          % (bad_batch[0]["name"], bad_batch[0]["lc"], bad_batch[0]["min"],
             "fail" if not bad_batch[0]["pass"] else "pass"))

    for msg in failures:
        print(" - %s" % msg)
    print("\n%s - reference values, polarity, zero-delta, and pass/fail thresholds exercised."
          % ("PASS" if not failures else "FAIL"))
    sys.exit(0 if not failures else 1)


# ---------------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser(description="APCA-W3 perceptual contrast (Lc)")
    ap.add_argument("--fg", help="text color, hex")
    ap.add_argument("--bg", help="background color, hex")
    ap.add_argument("--min", type=float, default=None,
                    help="required |Lc| (default 75 body; 45 large/bold, 30 non-text)")
    ap.add_argument("--pairs", help="JSON file: [{fg, bg, role: body|large|nontext, name?}]")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()

    try:
        if a.pairs:
            with open(a.pairs, "r", encoding="utf-8") as f:
                raw = json.load(f)
            if not isinstance(raw, list) or not raw:
                raise ValueError("--pairs must be a non-empty JSON array")
            results = [check_pair(p["fg"], p["bg"], p.get("role", "body"),
                                  p.get("min"), p.get("name")) for p in raw]
        elif a.fg and a.bg:
            results = [check_pair(a.fg, a.bg, "body", a.min if a.min is not None else 75.0)]
        else:
            print("pass --fg HEX --bg HEX, or --pairs <json>, or --selftest", file=sys.stderr)
            sys.exit(2)
    except (OSError, ValueError, KeyError, TypeError) as e:
        print("input error: %s" % e, file=sys.stderr)
        sys.exit(2)

    code = 0 if all(r["pass"] for r in results) else 1
    if a.as_json:
        print(json.dumps({"algorithm": "APCA-W3 0.1.9", "results": results, "exit": code}, indent=2))
        sys.exit(code)
    for r in results:
        print("[%s] %s (%s): Lc %+.3f, need |Lc| >= %g"
              % ("PASS" if r["pass"] else "FAIL", r["name"], r["role"], r["lc"], r["min"]))
    if code:
        print("[NO-GO] APCA contrast gate failed")
    else:
        print("[GO] APCA contrast gate passed")
    sys.exit(code)


if __name__ == "__main__":
    main()
