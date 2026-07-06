#!/usr/bin/env python3
"""
slop-fingerprint-gate.py - deterministic AI-slop aesthetic-fingerprint scanner.

Pattern set is a moving signature file — version and re-harvest; cite Krebs
repo (15 patterns shipped; blog says 16).

Modeled on Adrian Krebs' ai-design-checker (15 deterministic DOM/CSS tells);
this implements the statically-detectable subset over SOURCE files
(tsx/jsx/html screens + built or source css). Never replaced by an LLM judge.
Spec: docs/guild/decisions/anti-slop-survey.md §1.2 + adoption ledger.

  python3 scripts/slop-fingerprint-gate.py --screen src/Hero.tsx --css dist/app.css
  python3 scripts/slop-fingerprint-gate.py --screen a.tsx --screen b.tsx --json
  python3 scripts/slop-fingerprint-gate.py --selftest

Scoring per Krebs — each pattern counts at most once per screen:
  counted >= 4 (or --max N)   SLOP    exit 1
  counted 2-3                 MEDIUM  exit 0 (exit 1 with --strict)
  counted <= 1                CLEAN   exit 0
uniform-drop-shadow-spam is a weak signal: reported as WARN, never counted.
CSS findings are shared context and attribute to every screen scored.
Exit 2 = usage/input error.
"""
import argparse
import json
import re
import sys

SIGNATURE_VERSION = "2026-07-06.1"
DEFAULT_SLOP_MIN = 4
WARN_ONLY = {"uniform-drop-shadow-spam"}

# ---------------------------------------------------------------- signatures

DEFAULT_FONTS = r"(?:inter|roboto|arial|open[ _]?sans)"
RE_FONT = [
    re.compile(r"font-family\s*:\s*[\"']?\s*" + DEFAULT_FONTS + r"\b", re.I),
    re.compile(r"fontFamily\s*[:=]\s*[\"']" + DEFAULT_FONTS + r"\b", re.I),
    re.compile(r"font-\[[\"']?" + DEFAULT_FONTS + r"\b", re.I),
    re.compile(r"\b(?:sans|display|heading|body)\s*:\s*\[\s*[\"']" + DEFAULT_FONTS + r"[\"']", re.I),
]

VIBE_HEX = ["8B5CF6", "A78BFA", "7C3AED", "6D28D9", "9333EA"]
PURPLE_HEX = VIBE_HEX + ["A855F7", "C084FC", "D946EF"]
BLUE_HEX = ["3B82F6", "2563EB", "1D4ED8", "60A5FA", "6366F1", "4F46E5", "4338CA", "818CF8"]


def _hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


RE_VIBE_HEX = re.compile("#(?:" + "|".join(VIBE_HEX) + ")", re.I)
RE_VIBE_RGB = [re.compile(r"rgba?\(\s*%d\s*,\s*%d\s*,\s*%d\b" % _hex_rgb(h)) for h in VIBE_HEX]
RE_VIBE_TW = re.compile(
    r"\b(?:bg|from|to|via|text|border|ring|fill|stroke|outline|accent|decoration)"
    r"-(?:violet|purple)-(?:500|600)\b"
)

RE_GRADIENT = re.compile(r"linear-gradient\(", re.I)
RE_G_PURPLE = re.compile("#(?:" + "|".join(PURPLE_HEX) + r")|\b(?:purple|violet)\b", re.I)
RE_G_BLUE = re.compile("#(?:" + "|".join(BLUE_HEX) + r")|\b(?:blue|indigo|royalblue)\b", re.I)
RE_TW_FROM_P = re.compile(r"\bfrom-(?:purple|violet|fuchsia)-\d+")
RE_TW_TO_B = re.compile(r"\b(?:to|via)-(?:blue|indigo|sky)-\d+")
RE_TW_FROM_B = re.compile(r"\bfrom-(?:blue|indigo|sky)-\d+")
RE_TW_TO_P = re.compile(r"\b(?:to|via)-(?:purple|violet|fuchsia)-\d+")

RE_BLUR = re.compile(r"backdrop-filter\s*:[^;}\n]*blur|\bbackdrop-blur(?:-\w+|\[[^\]]*\])?", re.I)
RE_ALPHA_BG_CSS = re.compile(r"background(?:-color)?\s*:[^;}\n]*(?:rgba|hsla)\([^)]*,\s*(0?\.\d+|0)\s*\)", re.I)
RE_ALPHA_BG_TW = re.compile(r"\bbg-[\w-]+/(\d{1,3})\b|\bbg-opacity-(\d{1,3})\b")
GLASS_WINDOW = 3

BORDER_COLOR_WORDS = (
    r"red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo"
    r"|violet|purple|fuchsia|pink|rose"
)
RE_BL_TW_SIZE = re.compile(r"\bborder-l-[24]\b")
RE_BL_TW_COLOR = re.compile(r"\bborder-(?:" + BORDER_COLOR_WORDS + r")-\d{2,3}\b")
RE_CARDISH = re.compile(r"rounded|shadow|card|\bp-\d")
RE_BL_CSS = re.compile(r"border-left(?:-color)?\s*:\s*([^;}]+)", re.I)
NEUTRAL_NAMES = {"black", "white", "gray", "grey", "silver", "gainsboro",
                 "transparent", "currentcolor", "inherit", "initial", "none", "unset"}
CSS_COLOR_NAMES = re.compile(
    r"\b(red|orange|gold|yellow|green|teal|cyan|blue|indigo|violet|purple|magenta"
    r"|pink|crimson|tomato|coral|salmon|orchid|plum|navy|royalblue|dodgerblue"
    r"|steelblue|rebeccapurple|mediumpurple|slateblue)\b", re.I)

RE_ICON = re.compile(r"<svg\b|<[A-Z][A-Za-z0-9]*Icon\b|<[A-Z][A-Za-z0-9]*\b[^>\n]*className=[\"'][^\"'\n]*\b[hw]-\d")
RE_HEADING = re.compile(r"<h[1-6]\b|\bfont-(?:semibold|bold)\b.*\btext-(?:lg|xl)\b|\btext-(?:lg|xl)\b.*\bfont-(?:semibold|bold)\b")
RE_GRIDFLEX = re.compile(r"\bgrid\b|grid-cols|\bflex\b|display\s*:\s*(?:grid|flex)")
RE_MAP = re.compile(r"\.map\s*\(")

RE_STEP_TEXT = re.compile(r">\s*0?([123])\s*<")
RE_STEP_QUOTED = re.compile(r"[\"']0([123])[\"']")

RE_BADGE = re.compile(r"rounded-full")
RE_BADGE_PX = re.compile(r"\bpx-\d")
RE_BADGE_TXT = re.compile(r"\btext-(?:xs|sm)\b")
RE_H1 = re.compile(r"<h1\b", re.I)
BADGE_WINDOW = 6

RE_BEZIER = re.compile(r"cubic-bezier\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)", re.I)
RE_EASE_CTX = re.compile(r"ease|easing|transition|animation|animate|spring", re.I)
RE_EASE_KEY = re.compile(r"\b(?:elastic|bounce)\b", re.I)
RE_SPRING_BOUNCE = re.compile(r"\bbounce\s*[:=]\s*(0?\.\d+|[1-9][\d.]*)")

RE_SHADOW_CSS = re.compile(r"box-shadow\s*:\s*([^;}]+)", re.I)
RE_SHADOW_TW = re.compile(r"(?<![\w-])shadow(?:-(?:sm|md|lg|xl|2xl))?\b")
SHADOW_SPAM_MIN = 4

RE_EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿]")
RE_BTN_HEAD = re.compile(r"<button\b|<Button\b|<h[1-6]\b|role=[\"']button", re.I)
EMOJI_MIN = 3


def _f(file, n, line):
    return {"file": file, "line": n + 1, "evidence": line.strip()[:100]}


# ------------------------------------------------------------------- checks
# Each check takes [(file, lines)] sources, returns list of findings.

def check_inter_default_hero(sources):
    out = []
    for file, lines in sources:
        for i, line in enumerate(lines):
            if any(rx.search(line) for rx in RE_FONT):
                out.append(_f(file, i, line))
    return out


def check_vibe_purple(sources):
    out = []
    for file, lines in sources:
        for i, line in enumerate(lines):
            if RE_VIBE_HEX.search(line) or RE_VIBE_TW.search(line) or any(rx.search(line) for rx in RE_VIBE_RGB):
                out.append(_f(file, i, line))
    return out


def check_purple_blue_gradient(sources):
    out = []
    for file, lines in sources:
        for i, line in enumerate(lines):
            if RE_GRADIENT.search(line) and RE_G_PURPLE.search(line) and RE_G_BLUE.search(line):
                out.append(_f(file, i, line))
            elif (RE_TW_FROM_P.search(line) and RE_TW_TO_B.search(line)) or \
                 (RE_TW_FROM_B.search(line) and RE_TW_TO_P.search(line)):
                out.append(_f(file, i, line))
    return out


def _translucent(line):
    m = RE_ALPHA_BG_CSS.search(line)
    if m and float(m.group(1)) < 1:
        return True
    m = RE_ALPHA_BG_TW.search(line)
    if m:
        val = int(m.group(1) or m.group(2))
        return val < 100
    return False


def check_glassmorphism(sources):
    out = []
    for file, lines in sources:
        for i, line in enumerate(lines):
            if not RE_BLUR.search(line):
                continue
            lo, hi = max(0, i - GLASS_WINDOW), min(len(lines), i + GLASS_WINDOW + 1)
            if any(_translucent(lines[j]) for j in range(lo, hi)):
                out.append(_f(file, i, line))
    return out


def _neutral_color(value):
    m = re.search(r"#([0-9a-fA-F]{3,8})", value)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) >= 6:
            r, g, b = _hex_rgb(h[:6].upper())
            return max(r, g, b) - min(r, g, b) <= 16
        return True
    m = re.search(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", value)
    if m:
        r, g, b = (int(m.group(k)) for k in (1, 2, 3))
        return max(r, g, b) - min(r, g, b) <= 16
    if CSS_COLOR_NAMES.search(value):
        return False
    return True  # named neutrals, vars, widths only — treat as neutral


def check_colored_left_border_card(sources):
    out = []
    for file, lines in sources:
        for i, line in enumerate(lines):
            m = RE_BL_CSS.search(line)
            if m and not _neutral_color(m.group(1)):
                out.append(_f(file, i, line))
            elif RE_BL_TW_SIZE.search(line) and RE_BL_TW_COLOR.search(line) and RE_CARDISH.search(line):
                out.append(_f(file, i, line))
    return out


def check_icon_topped_card_grid(sources):
    out = []
    for file, lines in sources:
        text = "\n".join(lines)
        if not RE_GRIDFLEX.search(text):
            continue
        occurrences, map_lines = [], [i for i, l in enumerate(lines) if RE_MAP.search(l)]
        for i, line in enumerate(lines):
            if not RE_ICON.search(line):
                continue
            if any(RE_HEADING.search(lines[j]) for j in range(i + 1, min(len(lines), i + 4))):
                occurrences.append(i)
        mapped = any(any(0 <= occ - m <= 15 for m in map_lines) for occ in occurrences)
        if len(occurrences) >= 3 or (occurrences and mapped):
            out.append(_f(file, occurrences[0], lines[occurrences[0]]))
    return out


def check_numbered_step_row(sources):
    out = []
    for file, lines in sources:
        seen = {}
        for i, line in enumerate(lines):
            for m in RE_STEP_TEXT.finditer(line):
                seen.setdefault(m.group(1), i)
            for m in RE_STEP_QUOTED.finditer(line):
                seen.setdefault(m.group(1), i)
        if {"1", "2", "3"} <= set(seen):
            first = min(seen.values())
            out.append(_f(file, first, lines[first]))
    return out


def check_badge_above_hero_h1(sources):
    out = []
    for file, lines in sources:
        for i, line in enumerate(lines):
            if RE_BADGE.search(line) and RE_BADGE_PX.search(line) and RE_BADGE_TXT.search(line):
                hi = min(len(lines), i + BADGE_WINDOW + 1)
                if any(RE_H1.search(lines[j]) for j in range(i, hi)):
                    out.append(_f(file, i, line))
    return out


def check_bounce_elastic_easing(sources):
    out = []
    for file, lines in sources:
        for i, line in enumerate(lines):
            hit = False
            for m in RE_BEZIER.finditer(line):
                coords = [float(m.group(k)) for k in (1, 2, 3, 4)]
                if any(c < 0 or c > 1 for c in coords):
                    hit = True
            if not hit and RE_EASE_CTX.search(line) and RE_EASE_KEY.search(line):
                hit = True
            if not hit:
                m = RE_SPRING_BOUNCE.search(line)
                if m and float(m.group(1)) > 0:
                    hit = True
            if hit:
                out.append(_f(file, i, line))
    return out


def check_uniform_drop_shadow_spam(sources):
    out = []
    for file, lines in sources:
        literals = {}
        for i, line in enumerate(lines):
            for m in RE_SHADOW_CSS.finditer(line):
                val = " ".join(m.group(1).lower().split())
                if val != "none":
                    literals.setdefault(val, []).append(i)
            for m in RE_SHADOW_TW.finditer(line):
                literals.setdefault(m.group(0), []).append(i)
        for val, where in literals.items():
            if len(where) >= SHADOW_SPAM_MIN:
                out.append(_f(file, where[0], "%dx identical shadow '%s'" % (len(where), val)))
    return out


def check_emoji_as_icon(sources):
    out = []
    for file, lines in sources:
        count, first = 0, None
        for i, line in enumerate(lines):
            if not RE_BTN_HEAD.search(line):
                continue
            n = len(RE_EMOJI.findall(line))
            if n and first is None:
                first = i
            count += n
        if count >= EMOJI_MIN:
            out.append(_f(file, first, "%d emoji in button/heading contexts; %s" % (count, lines[first].strip()[:60])))
    return out


SCREEN_AND_CSS = [
    ("inter-default-hero", check_inter_default_hero),
    ("vibe-purple", check_vibe_purple),
    ("purple-blue-gradient", check_purple_blue_gradient),
    ("glassmorphism", check_glassmorphism),
    ("colored-left-border-card", check_colored_left_border_card),
    ("bounce-elastic-easing", check_bounce_elastic_easing),
    ("uniform-drop-shadow-spam", check_uniform_drop_shadow_spam),
]
SCREEN_ONLY = [
    ("icon-topped-card-grid", check_icon_topped_card_grid),
    ("numbered-step-row", check_numbered_step_row),
    ("badge-above-hero-h1", check_badge_above_hero_h1),
    ("emoji-as-icon", check_emoji_as_icon),
]
ALL_PATTERNS = [n for n, _ in SCREEN_AND_CSS + SCREEN_ONLY]


# ------------------------------------------------------------------ scoring

def scan_screen(screen_file, screen_text, css_sources, slop_min):
    screen_src = (screen_file, screen_text.splitlines())
    shared = [screen_src] + [(f, t.splitlines()) for f, t in css_sources]
    findings = {}
    for name, fn in SCREEN_AND_CSS:
        hits = fn(shared)
        if hits:
            findings[name] = hits
    for name, fn in SCREEN_ONLY:
        hits = fn([screen_src])
        if hits:
            findings[name] = hits
    counted = sorted(n for n in findings if n not in WARN_ONLY)
    warned = sorted(n for n in findings if n in WARN_ONLY)
    if len(counted) >= slop_min:
        tier = "SLOP"
    elif len(counted) >= 2:
        tier = "MEDIUM"
    else:
        tier = "CLEAN"
    return {"screen": screen_file, "tier": tier, "counted": counted,
            "warned": warned, "findings": findings}


def exit_code(results, strict):
    if any(r["tier"] == "SLOP" for r in results):
        return 1
    if strict and any(r["tier"] == "MEDIUM" for r in results):
        return 1
    return 0


# ------------------------------------------------------------------ selftest

FAIL_TSX = """\
export default function Landing() {
  return (
    <main className="flex flex-col">
      <span className="rounded-full px-3 py-1 text-xs bg-purple-600 text-white">New</span>
      <h1 className="font-[Inter] bg-gradient-to-r from-purple-500 to-blue-500">Ship faster</h1>
      <section className="grid grid-cols-3 gap-6">
        <div className="rounded-xl shadow-lg p-6 border-l-4 border-purple-500">
          <Zap className="h-6 w-6" />
          <h3 className="text-lg font-semibold">Fast</h3>
        </div>
        <div className="rounded-xl shadow-lg p-6">
          <Shield className="h-6 w-6" />
          <h3 className="text-lg font-semibold">Safe</h3>
        </div>
        <div className="rounded-xl shadow-lg p-6">
          <Star className="h-6 w-6" />
          <h3 className="text-lg font-semibold">Loved</h3>
        </div>
      </section>
      <div className="backdrop-blur-md bg-white/10 rounded-2xl shadow-lg">glass</div>
      <ol>
        <li><span>01</span> Sign up</li>
        <li><span>02</span> Connect</li>
        <li><span>03</span> Profit</li>
      </ol>
      <button className="ease-[cubic-bezier(0.68,-0.55,0.265,1.55)]">\U0001F680 Launch</button>
      <button>\U0001F525 Buy now</button>
      <h2>✨ Features</h2>
    </main>
  );
}
"""

FAIL_CSS = """\
h1 { font-family: Inter, sans-serif; }
.hero { background: linear-gradient(135deg, #8B5CF6, #3B82F6); }
.card { border-left: 4px solid #7C3AED; }
.glass { backdrop-filter: blur(12px); background: rgba(255,255,255,0.08); }
.pop { transition: transform 300ms cubic-bezier(.68,-.6,.32,1.6); }
"""

PASS_TSX = """\
export default function Dashboard() {
  return (
    <main className="app-shell">
      <h1 className="font-display text-ink">Weekly report</h1>
      <nav className="tabs">
        <a className="tab">Overview</a>
        <a className="tab is-active">Trends</a>
      </nav>
      <section className="panel">
        <h2 className="panel-title">Revenue</h2>
        <p className="panel-copy">Steady growth across all regions.</p>
      </section>
      <button className="btn-primary">Export</button>
    </main>
  );
}
"""

PASS_CSS = """\
:root { --font-display: "Fraunces", Georgia, serif; --ink: #1a1a1a; }
h1 { font-family: var(--font-display); }
.btn-primary { background: var(--brand-700); transition: opacity 150ms ease-out; box-shadow: var(--elev-1); }
.panel { border: 1px solid var(--line); border-radius: 12px; }
"""

MEDIUM_TSX = """\
export default function Promo() {
  return (
    <div className="backdrop-blur-sm bg-black/40 text-violet-500 rounded-lg p-4">Promo</div>
  );
}
"""


def selftest():
    failures = []

    def expect(cond, msg):
        if not cond:
            failures.append(msg)

    bad = scan_screen("fail.tsx", FAIL_TSX, [("fail.css", FAIL_CSS)], DEFAULT_SLOP_MIN)
    hit = set(bad["findings"])
    for name in ALL_PATTERNS:
        expect(name in hit, "fail fixture missing pattern: %s" % name)
    expect(len(bad["counted"]) == len(ALL_PATTERNS) - len(WARN_ONLY),
           "fail fixture counted=%d expected %d" % (len(bad["counted"]), len(ALL_PATTERNS) - len(WARN_ONLY)))
    expect(bad["tier"] == "SLOP", "fail fixture tier=%s expected SLOP" % bad["tier"])
    expect(bad["warned"] == ["uniform-drop-shadow-spam"], "shadow spam should be WARN-only")
    expect(exit_code([bad], strict=False) == 1, "SLOP must exit 1")
    for f in bad["findings"].values():
        expect(all(isinstance(x["line"], int) and x["line"] >= 1 for x in f), "finding without line number")

    good = scan_screen("pass.tsx", PASS_TSX, [("pass.css", PASS_CSS)], DEFAULT_SLOP_MIN)
    expect(not good["findings"], "pass fixture tripped: %s" % sorted(good["findings"]))
    expect(good["tier"] == "CLEAN", "pass fixture tier=%s expected CLEAN" % good["tier"])
    expect(exit_code([good], strict=False) == 0, "CLEAN must exit 0")
    expect(exit_code([good], strict=True) == 0, "CLEAN must exit 0 even with --strict")

    med = scan_screen("medium.tsx", MEDIUM_TSX, [], DEFAULT_SLOP_MIN)
    expect(med["counted"] == ["glassmorphism", "vibe-purple"],
           "medium fixture counted=%s expected exactly glassmorphism+vibe-purple" % med["counted"])
    expect(med["tier"] == "MEDIUM", "medium fixture tier=%s expected MEDIUM" % med["tier"])
    expect(exit_code([med], strict=False) == 0, "MEDIUM must exit 0 without --strict")
    expect(exit_code([med], strict=True) == 1, "MEDIUM must exit 1 with --strict")

    custom = scan_screen("fail.tsx", FAIL_TSX, [("fail.css", FAIL_CSS)], len(ALL_PATTERNS) + 1)
    expect(custom["tier"] == "MEDIUM", "--max above hit count should downgrade SLOP to MEDIUM")

    print("slop-fingerprint-gate self-test (signature %s)" % SIGNATURE_VERSION)
    print("   fail fixture: %d/%d patterns, tier %s (counted %d, warn %d)"
          % (len(hit), len(ALL_PATTERNS), bad["tier"], len(bad["counted"]), len(bad["warned"])))
    print("   pass fixture: %d patterns, tier %s" % (len(good["findings"]), good["tier"]))
    print("   medium fixture: %s -> strict exits %d/%d"
          % (",".join(med["counted"]), exit_code([med], False), exit_code([med], True)))
    for msg in failures:
        print(" - %s" % msg)
    print("\n%s - golden-pass, golden-fail, tier math, and both --strict paths exercised."
          % ("PASS" if not failures else "FAIL"))
    sys.exit(0 if not failures else 1)


# ---------------------------------------------------------------------- cli

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError as e:
        print("input error: %s" % e, file=sys.stderr)
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description="deterministic AI-slop fingerprint gate")
    ap.add_argument("--screen", action="append", default=[], help="tsx/jsx/html screen source (repeatable)")
    ap.add_argument("--css", action="append", default=[], help="built or source css (repeatable, shared across screens)")
    ap.add_argument("--max", type=int, default=DEFAULT_SLOP_MIN, help="patterns needed for SLOP (default %d)" % DEFAULT_SLOP_MIN)
    ap.add_argument("--strict", action="store_true", help="MEDIUM also exits 1")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    if not a.screen:
        print("pass --screen <file> (repeatable) or --selftest", file=sys.stderr)
        sys.exit(2)
    if a.max < 2:
        print("--max must be >= 2 (MEDIUM band starts at 2)", file=sys.stderr)
        sys.exit(2)

    css_sources = [(p, read_file(p)) for p in a.css]
    results = [scan_screen(p, read_file(p), css_sources, a.max) for p in a.screen]
    code = exit_code(results, a.strict)

    if a.as_json:
        print(json.dumps({"signature_version": SIGNATURE_VERSION, "slop_min": a.max,
                          "strict": a.strict, "screens": results, "exit": code}, indent=2))
        sys.exit(code)

    for r in results:
        print("[%s] %s: %d counted pattern(s), threshold %d" % (r["tier"], r["screen"], len(r["counted"]), a.max))
        for name in r["counted"] + r["warned"]:
            tag = "warn " if name in WARN_ONLY else ""
            for f in r["findings"][name]:
                print(" - %s%s %s:%d: %s" % (tag, name, f["file"], f["line"], f["evidence"]))
    verdict = "NO-GO" if code else "GO"
    print("[%s] slop fingerprint gate (signature %s)" % (verdict, SIGNATURE_VERSION))
    sys.exit(code)


if __name__ == "__main__":
    main()
